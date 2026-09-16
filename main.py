"""
Análise de ações da bolsa - Interface Web (Dash)

Bibliotecas necessárias:
pip install dash yfinance pandas plotly

Para rodar:
python app.py
Depois abra no navegador: http://127.0.0.1:8050
"""

from dash import Dash, dcc, html, Input, Output, State
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go


def carregar_acao(ticker, periodo="3y"):
    ticker = ticker.upper()

    if not ticker.endswith(".SA"):
        ticker += ".SA"

    dados = yf.download(
        ticker,
        period=periodo,
        auto_adjust=False
    )

    if isinstance(dados.columns, pd.MultiIndex):
        dados.columns = dados.columns.get_level_values(0)

    return dados


def obter_indicadores(ticker):
    ticker_yf = ticker.upper()

    if not ticker_yf.endswith(".SA"):
        ticker_yf += ".SA"

    acao = yf.Ticker(ticker_yf)
    info = acao.info

    def fmt_pct(valor):
        return f"{valor * 100:.2f}%" if valor else "N/D"

    def fmt_num(valor):
        return f"{valor:.2f}" if valor else "N/D"

    def fmt_moeda(valor):
        return f"R$ {valor:,.2f}".replace(",", ".") if valor else "N/D"

    indicadores = {
        "Empresa": info.get("longName", "N/D"),
        "Setor": info.get("sector", "N/D"),
        "Segmento": info.get("industry", "N/D"),

        "P/L": fmt_num(info.get("trailingPE")),
        "P/VP": fmt_num(info.get("priceToBook")),
        "P/S": fmt_num(info.get("priceToSalesTrailing12Months")),
        "EV/EBITDA": fmt_num(info.get("enterpriseToEbitda")),

        "ROE": fmt_pct(info.get("returnOnEquity")),
        "ROA": fmt_pct(info.get("returnOnAssets")),

        "Margem líquida": fmt_pct(info.get("profitMargins")),
        "Margem operacional": fmt_pct(info.get("operatingMargins")),

        "Dividend Yield": fmt_pct(info.get("dividendYield")),
        "Payout": fmt_pct(info.get("payoutRatio")),

        "Preço atual": fmt_moeda(info.get("currentPrice")),
        "Valor de mercado": fmt_moeda(info.get("marketCap")),
        "Beta": fmt_num(info.get("beta")),
    }

    return indicadores


app = Dash(__name__)
app.title = "Análise de Ações"

app.layout = html.Div(
    style={
        "fontFamily": "Arial, sans-serif",
        "maxWidth": "1000px",
        "margin": "0 auto",
        "padding": "20px",
    },
    children=[
        html.H1("📈 Análise de Ações", style={"textAlign": "center"}),

        html.Div(
            style={"display": "flex", "gap": "10px", "justifyContent": "center", "marginBottom": "20px"},
            children=[
                dcc.Input(
                    id="input-ticker",
                    type="text",
                    value="PETR4",
                    placeholder="Digite o ticker (ex: PETR4, VALE3)",
                    style={"padding": "8px", "fontSize": "16px", "width": "250px"},
                ),
                html.Button(
                    "Analisar",
                    id="botao-analisar",
                    n_clicks=0,
                    style={"padding": "8px 20px", "fontSize": "16px", "cursor": "pointer"},
                ),
            ],
        ),

        dcc.Loading(
            type="circle",
            children=[
                html.Div(id="area-indicadores"),
                dcc.Graph(id="grafico-acao"),
            ],
        ),
    ],
)


@app.callback(
    Output("area-indicadores", "children"),
    Output("grafico-acao", "figure"),
    Input("botao-analisar", "n_clicks"),
    State("input-ticker", "value"),
)
def atualizar_analise(n_clicks, ticker):
    if not ticker:
        return html.Div("Digite um ticker."), go.Figure()

    ticker = ticker.strip()

    try:
        indicadores = obter_indicadores(ticker)
        dados = carregar_acao(ticker)

        if dados.empty:
            mensagem = html.Div(
                f"Não foi possível encontrar dados para o ticker '{ticker}'. Verifique se o código está correto.",
                style={"color": "red"},
            )
            return mensagem, go.Figure()

        dados["MM20"] = dados["Close"].rolling(window=20).mean()
        dados["MM50"] = dados["Close"].rolling(window=50).mean()
        dados["MM200"] = dados["Close"].rolling(window=200).mean()

        def card(titulo, valor):
            return html.Div(
                style={
                    "border": "1px solid #ddd",
                    "borderRadius": "8px",
                    "padding": "10px 15px",
                    "minWidth": "150px",
                    "textAlign": "center",
                    "boxShadow": "1px 1px 4px rgba(0,0,0,0.08)",
                },
                children=[
                    html.Div(titulo, style={"fontSize": "13px", "color": "#666"}),
                    html.Div(valor, style={"fontSize": "18px", "fontWeight": "bold"}),
                ],
            )

        cabecalho = html.Div(
            [
                html.H3(f"{indicadores['Empresa']} ({ticker.upper()})"),
                html.P(f"{indicadores['Setor']} — {indicadores['Segmento']}", style={"color": "#666"}),
            ]
        )

        grade_indicadores = html.Div(
            style={"display": "flex", "flexWrap": "wrap", "gap": "10px", "marginBottom": "20px"},
            children=[
                card("Preço atual", indicadores["Preço atual"]),
                card("P/L", indicadores["P/L"]),
                card("P/VP", indicadores["P/VP"]),
                card("EV/EBITDA", indicadores["EV/EBITDA"]),
                card("ROE", indicadores["ROE"]),
                card("ROA", indicadores["ROA"]),
                card("Margem líquida", indicadores["Margem líquida"]),
                card("Margem operacional", indicadores["Margem operacional"]),
                card("Dividend Yield", indicadores["Dividend Yield"]),
                card("Payout", indicadores["Payout"]),
                card("Valor de mercado", indicadores["Valor de mercado"]),
                card("Beta", indicadores["Beta"]),
            ],
        )

        bloco_indicadores = html.Div([cabecalho, grade_indicadores])

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dados.index, y=dados["Close"], name="Preço"))
        fig.add_trace(go.Scatter(x=dados.index, y=dados["MM20"], name="MM20"))
        fig.add_trace(go.Scatter(x=dados.index, y=dados["MM50"], name="MM50"))
        fig.add_trace(go.Scatter(x=dados.index, y=dados["MM200"], name="MM200"))

        fig.update_layout(
            title=f"Tendência de {ticker.upper()}",
            xaxis_title="Data",
            yaxis_title="Preço (R$)",
            template="plotly_white",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        )

        return bloco_indicadores, fig

    except Exception as erro:
        mensagem_erro = html.Div(
            f"Ocorreu um erro ao buscar os dados de '{ticker}': {erro}",
            style={"color": "red"},
        )
        return mensagem_erro, go.Figure()


if __name__ == "__main__":
    app.run(debug=True)