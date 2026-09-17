"""
Análise de ações da bolsa - Interface Web (Dash)

Bibliotecas necessárias:
pip install dash yfinance pandas plotly

Para rodar:
python app.py
Depois abra no navegador: http://127.0.0.1:8050
"""

from datetime import datetime, timedelta

from dash import Dash, dcc, html, Input, Output, State, no_update
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go


COR_FUNDO_PAGINA = "#4DCEF7"
COR_FUNDO_DADOS = "#7ED7F7"
COR_FUNDO_GRAFICO = "#FFFFFF"

PERIODOS = {
    "1 dia": {"dias_calendario": 1, "intervalo": "5m", "dias_uteis": 1},
    "1 semana": {"dias_calendario": 7, "intervalo": "30m", "dias_uteis": 5},
    "1 mês": {"dias_calendario": 30, "intervalo": "1d", "dias_uteis": 21},
    "6 meses": {"dias_calendario": 182, "intervalo": "1d", "dias_uteis": 126},
    "1 ano": {"dias_calendario": 365, "intervalo": "1d", "dias_uteis": 252},
    "3 anos": {"dias_calendario": 365 * 3, "intervalo": "1d", "dias_uteis": 756},
    "5 anos": {"dias_calendario": 365 * 5, "intervalo": "1d", "dias_uteis": 1260},
}

MEDIAS = {"MM20": 20, "MM50": 50, "MM200": 200}


def carregar_acao(ticker, periodo_label):
    ticker = ticker.upper()
    if not ticker.endswith(".SA"):
        ticker += ".SA"

    config = PERIODOS[periodo_label]
    data_fim = datetime.today()
    data_inicio = data_fim - timedelta(days=config["dias_calendario"])

    dados = yf.download(
        ticker,
        start=data_inicio,
        end=data_fim,
        interval=config["intervalo"],
        auto_adjust=False,
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
    }

    return indicadores


app = Dash(__name__)
app.title = "Análise de Ações"

app.layout = html.Div(
    style={
        "backgroundColor": COR_FUNDO_PAGINA,
        "minHeight": "100vh",
        "padding": "30px",
        "fontFamily": "Arial, sans-serif",
    },
    children=[
        html.H1("📈 Análise de Ações", style={"textAlign": "center", "color": "#ffffff"}),

        dcc.Store(id="store-ticker"),

        html.Div(
            style={
                "backgroundColor": COR_FUNDO_DADOS,
                "borderRadius": "12px",
                "padding": "20px",
                "maxWidth": "950px",
                "margin": "0 auto 20px auto",
            },
            children=[
                html.H3("Pesquisar Ação", style={"marginTop": 0}),
                html.Div(
                    style={"display": "flex", "gap": "10px", "flexWrap": "wrap", "alignItems": "center"},
                    children=[
                        dcc.Input(
                            id="input-ticker",
                            type="text",
                            value="PETR4",
                            placeholder="Digite o ticker (ex: PETR4, VALE3)",
                            style={"padding": "8px", "fontSize": "16px", "width": "220px", "borderRadius": "8px", "border": "1px solid #ccc"},
                        ),
                        html.Button(
                            "Pesquisar",
                            id="botao-pesquisar",
                            n_clicks=0,
                            style={
                                "padding": "10px 28px",
                                "fontSize": "16px",
                                "cursor": "pointer",
                                "borderRadius": "25px",
                                "border": "none",
                                "backgroundColor": "#1E88E5",
                                "color": "#ffffff",
                            },
                        ),
                    ],
                ),
            ],
        ),

        dcc.Loading(
            type="circle",
            children=[
                html.Div(
                    style={
                        "backgroundColor": COR_FUNDO_DADOS,
                        "borderRadius": "12px",
                        "padding": "20px",
                        "maxWidth": "950px",
                        "margin": "0 auto 20px auto",
                    },
                    children=[html.Div(id="area-indicadores")],
                ),
            ],
        ),

        html.Div(
            style={
                "backgroundColor": COR_FUNDO_GRAFICO,
                "borderRadius": "12px",
                "padding": "20px",
                "maxWidth": "950px",
                "margin": "0 auto",
            },
            children=[
                html.Div(
                    style={"display": "flex", "gap": "10px", "flexWrap": "wrap", "alignItems": "center", "marginBottom": "15px"},
                    children=[
                        dcc.Dropdown(
                            id="dropdown-periodo",
                            options=[{"label": nome, "value": nome} for nome in PERIODOS],
                            value="1 ano",
                            clearable=False,
                            style={"width": "180px"},
                        ),
                        dcc.Dropdown(
                            id="dropdown-medias",
                            options=[{"label": nome, "value": nome} for nome in MEDIAS],
                            value=["MM20", "MM50", "MM200"],
                            multi=True,
                            placeholder="Médias móveis",
                            style={"width": "280px"},
                        ),
                    ],
                ),
                dcc.Loading(
                    type="circle",
                    children=[dcc.Graph(id="grafico-acao")],
                ),
            ],
        ),
    ],
)


@app.callback(
    Output("dropdown-medias", "options"),
    Output("dropdown-medias", "value"),
    Input("dropdown-periodo", "value"),
    State("dropdown-medias", "value"),
)
def atualizar_opcoes_medias(periodo, selecionadas):
    dias_uteis = PERIODOS.get(periodo, {}).get("dias_uteis", 0)
    validas = [nome for nome, janela in MEDIAS.items() if dias_uteis > janela]

    opcoes = [
        {"label": nome, "value": nome, "disabled": nome not in validas}
        for nome in MEDIAS
    ]

    novas_selecionadas = [s for s in (selecionadas or []) if s in validas]

    return opcoes, novas_selecionadas


@app.callback(
    Output("area-indicadores", "children"),
    Output("store-ticker", "data"),
    Input("botao-pesquisar", "n_clicks"),
    State("input-ticker", "value"),
)
def atualizar_indicadores(n_clicks, ticker):
    if not ticker:
        return html.Div("Digite um ticker."), no_update

    ticker = ticker.strip()

    try:
        indicadores = obter_indicadores(ticker)

        def card(titulo, valor):
            return html.Div(
                style={
                    "backgroundColor": "#ffffff",
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
                html.P(f"{indicadores['Setor']} — {indicadores['Segmento']}", style={"color": "#333"}),
            ]
        )

        grade_indicadores = html.Div(
            style={"display": "flex", "flexWrap": "wrap", "gap": "10px"},
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
            ],
        )

        bloco_indicadores = html.Div([cabecalho, grade_indicadores])

        return bloco_indicadores, ticker

    except Exception as erro:
        mensagem_erro = html.Div(
            f"Ocorreu um erro ao buscar os indicadores de '{ticker}': {erro}",
            style={"color": "red"},
        )
        return mensagem_erro, no_update


@app.callback(
    Output("grafico-acao", "figure"),
    Input("dropdown-periodo", "value"),
    Input("dropdown-medias", "value"),
    Input("store-ticker", "data"),
)
def atualizar_grafico(periodo, medias_selecionadas, ticker):
    if not ticker:
        return go.Figure()

    try:
        dados = carregar_acao(ticker, periodo)

        if dados.empty:
            fig = go.Figure()
            fig.add_annotation(
                text=f"Não foi possível encontrar dados para '{ticker}' nesse período.",
                showarrow=False,
                font=dict(color="red"),
            )
            fig.update_layout(plot_bgcolor=COR_FUNDO_GRAFICO, paper_bgcolor=COR_FUNDO_GRAFICO)
            return fig

        for nome, janela in MEDIAS.items():
            dados[nome] = dados["Close"].rolling(window=janela).mean()

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dados.index, y=dados["Close"], name="Preço"))

        for nome in (medias_selecionadas or []):
            fig.add_trace(go.Scatter(x=dados.index, y=dados[nome], name=nome))

        fig.update_layout(
            title=f"Tendência de {ticker.upper()} ({periodo})",
            xaxis_title="Data",
            yaxis_title="Preço (R$)",
            template="plotly_white",
            plot_bgcolor=COR_FUNDO_GRAFICO,
            paper_bgcolor=COR_FUNDO_GRAFICO,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        )

        return fig

    except Exception as erro:
        fig = go.Figure()
        fig.add_annotation(
            text=f"Ocorreu um erro ao buscar os dados de '{ticker}': {erro}",
            showarrow=False,
            font=dict(color="red"),
        )
        fig.update_layout(plot_bgcolor=COR_FUNDO_GRAFICO, paper_bgcolor=COR_FUNDO_GRAFICO)
        return fig


if __name__ == "__main__":
    app.run(debug=True)