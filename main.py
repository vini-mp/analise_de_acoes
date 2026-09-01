
"""
Análise de ações da bolsa

Bibliotecas necessárias:
pip install yfinance pandas matplotlib
"""

# Importa a biblioteca utilizada para buscar os dados das ações
import yfinance as yf

# Importa a biblioteca utilizada para criar os gráficos
import matplotlib.pyplot as plt


# ============================================================
# FUNÇÃO: CARREGAR AÇÃO
# ============================================================

def carregar_acao(ticker, periodo="3y"):
    # Converte o código da ação para letras maiúsculas
    ticker = ticker.upper()

    # O Yahoo Finance identifica ações brasileiras com o sufixo .SA
    # Exemplo: PETR4 → PETR4.SA
    if not ticker.endswith(".SA"):
        ticker += ".SA"

    # Baixa os dados históricos da ação
    dados = yf.download(
        ticker,

        # Define o período de histórico que será carregado
        period=periodo,

        # Mantém os preços sem ajustes
        auto_adjust=False
    )

    # Retorna os dados para o restante do programa
    return dados


# ============================================================
# FUNÇÃO: MOSTRAR INDICADORES
# ============================================================

def mostrar_indicadores(ticker):

    # Cria uma versão do ticker adequada para o Yahoo Finance
    ticker_yf = ticker.upper()

    # Adiciona .SA caso ainda não esteja presente
    if not ticker_yf.endswith(".SA"):
        ticker_yf += ".SA"

    # Cria um objeto que representa a ação no Yahoo Finance
    acao = yf.Ticker(ticker_yf)

    # Busca as informações fundamentalistas e de mercado da empresa
    info = acao.info

    # Cria uma linha visual para separar as informações
    print("\n" + "=" * 60)

    # Mostra o título dos indicadores
    print(f"                 INDICADORES - {ticker.upper()}")

    # Cria outra linha de separação
    print("=" * 60)


    # ========================================================
    # INFORMAÇÕES DA EMPRESA
    # ========================================================

    # Nome completo da empresa
    print(f"\nEmpresa:            {info.get('longName', 'N/D')}")

    # Setor de atuação
    print(f"Setor:              {info.get('sector', 'N/D')}")

    # Segmento/indústria
    print(f"Segmento:           {info.get('industry', 'N/D')}")


    # ========================================================
    # VALUATION
    # ========================================================

    print("\n--- VALUATION ---")

    # Preço sobre lucro
    pl = info.get("trailingPE")

    # Preço sobre valor patrimonial
    pvp = info.get("priceToBook")

    # Preço sobre vendas
    psr = info.get("priceToSalesTrailing12Months")

    # Valor da empresa sobre EBITDA
    ev_ebitda = info.get("enterpriseToEbitda")

    # Exibe P/L com duas casas decimais
    # Caso o dado não esteja disponível, mostra N/D
    print(
        f"P/L:               {pl:.2f}"
        if pl else
        "P/L:               N/D"
    )

    # Exibe P/VP
    print(
        f"P/VP:              {pvp:.2f}"
        if pvp else
        "P/VP:              N/D"
    )

    # Exibe P/S
    print(
        f"P/S:               {psr:.2f}"
        if psr else
        "P/S:               N/D"
    )

    # Exibe EV/EBITDA
    print(
        f"EV/EBITDA:         {ev_ebitda:.2f}"
        if ev_ebitda else
        "EV/EBITDA:         N/D"
    )


    # ========================================================
    # RENTABILIDADE
    # ========================================================

    print("\n--- RENTABILIDADE ---")

    # Retorno sobre o patrimônio líquido
    roe = info.get("returnOnEquity")

    # Retorno sobre os ativos
    roa = info.get("returnOnAssets")

    # Os valores retornados normalmente estão em formato decimal.
    # Exemplo: 0.215 = 21,5%
    print(
        f"ROE:               {roe * 100:.2f}%"
        if roe else
        "ROE:               N/D"
    )

    print(
        f"ROA:               {roa * 100:.2f}%"
        if roa else
        "ROA:               N/D"
    )


    # ========================================================
    # MARGENS
    # ========================================================

    print("\n--- MARGENS ---")

    # Margem de lucro líquido
    margem_lucro = info.get("profitMargins")

    # Margem operacional
    margem_operacional = info.get("operatingMargins")

    # Converte o valor decimal para porcentagem
    print(
        f"Margem líquida:     {margem_lucro * 100:.2f}%"
        if margem_lucro else
        "Margem líquida:     N/D"
    )

    print(
        f"Margem operacional: {margem_operacional * 100:.2f}%"
        if margem_operacional else
        "Margem operacional: N/D"
    )


    # ========================================================
    # DIVIDENDOS
    # ========================================================

    print("\n--- DIVIDENDOS ---")

    # Dividend Yield
    dy = info.get("dividendYield")

    # Percentual do lucro distribuído aos acionistas
    payout = info.get("payoutRatio")

    # Converte o Dividend Yield para porcentagem
    print(
        f"Dividend Yield:     {dy * 100:.2f}%"
        if dy else
        "Dividend Yield:     N/D"
    )

    # Converte o Payout para porcentagem
    print(
        f"Payout:             {payout * 100:.2f}%"
        if payout else
        "Payout:             N/D"
    )


    # ========================================================
    # DADOS DE MERCADO
    # ========================================================

    print("\n--- DADOS DE MERCADO ---")

    # Obtém o preço atual da ação
    preco = info.get("currentPrice")

    # Obtém o valor de mercado da empresa
    market_cap = info.get("marketCap")

    # Obtém o Beta da ação
    beta = info.get("beta")

    # Exibe o preço atual formatado em reais
    print(
        f"Preço atual:        R$ {preco:.2f}"
        if preco else
        "Preço atual:        N/D"
    )

    # Exibe o valor de mercado caso essa informação esteja disponível
    if market_cap:
        print(
            f"Valor de mercado:   R$ {market_cap:,.0f}"
            .replace(",", ".")
        )

    # Exibe o Beta da ação
    print(
        f"Beta:               {beta:.2f}"
        if beta else
        "Beta:               N/D"
    )

    # Linha final de separação
    print("\n" + "=" * 60)


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

# Define qual ação será analisada
ticker = "PETR4"


# Chama a função responsável por buscar e mostrar os indicadores
mostrar_indicadores(ticker)


# Chama a função responsável por baixar o histórico da ação
dados = carregar_acao(ticker)


# ============================================================
# CRIAÇÃO DO GRÁFICO
# ============================================================

# Define o tamanho da janela do gráfico
plt.figure(figsize=(12, 6))

# Plota a evolução do preço de fechamento ao longo do período
plt.plot(
    dados.index,
    dados["Close"],
    label=ticker
)

# Define o título do gráfico
plt.title(f"Gráfico de {ticker}")

# Define o nome do eixo horizontal
plt.xlabel("Data")

# Define o nome do eixo vertical
plt.ylabel("Preço (R$)")

# Adiciona uma grade para facilitar a leitura dos valores
plt.grid(True)

# Exibe a legenda
plt.legend()

# Abre a janela do gráfico
plt.show()

