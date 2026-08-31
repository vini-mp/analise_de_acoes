"""
Análise de ações da bolsa

pip install yfinance pandas matplotlib
"""

import yfinance as yf
import matplotlib.pyplot as plt


def carregar_acao(ticker, periodo="3y"):
    ticker = ticker.upper()

    if not ticker.endswith(".SA"):
        ticker += ".SA"

    dados = yf.download(
        ticker,
        period=periodo,
        auto_adjust=False
    )

    return dados


# Ação que queremos consultar
ticker = "PETR4"

# Importar dados
dados = carregar_acao(ticker)

# Mostrar os últimos dados
print(dados.tail())

# Criar gráfico
plt.figure(figsize=(12, 6))

plt.plot(
    dados.index,
    dados["Close"],
    label=ticker
)

plt.title(f"Gráfico de {ticker}")
plt.xlabel("Data")
plt.ylabel("Preço (R$)")
plt.grid(True)
plt.legend()

plt.show()