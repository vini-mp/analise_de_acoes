# Análise de Ações da Bolsa

Aplicação web desenvolvida em Python com [Dash](https://dash.plotly.com/) para consultar ações da B3. A partir do código (ticker) da empresa, a aplicação exibe os principais indicadores fundamentalistas e um gráfico interativo com a evolução do preço e as médias móveis, em diferentes períodos.

Os dados são obtidos do Yahoo Finance por meio da biblioteca `yfinance`.

## Funcionalidades

- Pesquisa de ações da B3 pelo ticker (por exemplo, `PETR4` ou `VALE3`)
- Exibição do nome da empresa, do setor e do segmento
- Painel de indicadores fundamentalistas em formato de cartões
- Gráfico interativo de preço com zoom, seleção de área e informações ao passar o mouse
- Sete períodos de análise, de 1 dia a 5 anos
- Médias móveis de 20, 50 e 200 períodos, que podem ser ativadas e desativadas
- Desabilitação automática das médias móveis que não fazem sentido para o período escolhido
- Indicador de carregamento durante a busca dos dados
- Mensagens de erro em caso de ticker inválido ou falha na consulta

## Requisitos

- Python 3 instalado
- Conexão com a internet (os dados são consultados em tempo real)
- Bibliotecas: `dash`, `yfinance`, `pandas` e `plotly`

## Instalação e execução

1. Baixe ou clone o repositório e acesse a pasta do projeto:

   ```bash
   git clone https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
   cd SEU_REPOSITORIO
   ```

2. (Recomendado) Crie e ative um ambiente virtual:

   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux / macOS
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Instale as dependências:

   ```bash
   pip install dash yfinance pandas plotly
   ```

4. Execute a aplicação:

   ```bash
   python app.py
   ```

5. Abra no navegador o endereço:

   ```
   http://127.0.0.1:8050
   ```

## Como usar

1. Digite o ticker no campo **Pesquisar Ação**. O sufixo `.SA` é adicionado automaticamente, portanto basta informar `PETR4`, e não `PETR4.SA`.
2. Clique em **Pesquisar**. Os indicadores e o gráfico são carregados somente após esse clique.
3. Escolha o período no primeiro menu suspenso acima do gráfico.
4. Selecione, no segundo menu, as médias móveis que deseja visualizar.

Ao alterar o período ou as médias móveis, o gráfico é atualizado sem necessidade de pesquisar novamente.

## Indicadores exibidos

| Indicador | Descrição |
|-----------|-----------|
| Preço atual | Cotação mais recente |
| P/L | Preço sobre lucro |
| P/VP | Preço sobre valor patrimonial |
| EV/EBITDA | Valor da firma sobre o EBITDA |
| ROE | Retorno sobre o patrimônio líquido |
| ROA | Retorno sobre os ativos |
| Margem líquida | Lucro líquido sobre a receita |
| Margem operacional | Resultado operacional sobre a receita |
| Dividend Yield | Rendimento de dividendos |
| Payout | Proporção do lucro distribuída em proventos |
| Valor de mercado | Capitalização de mercado da empresa |

Quando o Yahoo Finance não disponibiliza determinado dado para a empresa, o cartão exibe **N/D**.

## Períodos e médias móveis

Cada período define o intervalo dos candles usados no gráfico:

| Período | Intervalo dos dados |
|---------|---------------------|
| 1 dia | 5 minutos |
| 1 semana | 30 minutos |
| 1 mês | Diário |
| 6 meses | Diário |
| 1 ano | Diário |
| 3 anos | Diário |
| 5 anos | Diário |

As médias móveis (MM20, MM50 e MM200) são calculadas sobre o preço de fechamento. Uma média só fica disponível quando o período possui mais dias úteis do que a janela da média:

| Período | Dias úteis considerados | Médias disponíveis |
|---------|-------------------------|--------------------|
| 1 dia | 1 | Nenhuma |
| 1 semana | 5 | Nenhuma |
| 1 mês | 21 | MM20 |
| 6 meses | 126 | MM20 e MM50 |
| 1 ano | 252 | MM20, MM50 e MM200 |
| 3 anos | 756 | MM20, MM50 e MM200 |
| 5 anos | 1260 | MM20, MM50 e MM200 |

Ao trocar de período, as médias selecionadas que deixarem de ser válidas são removidas automaticamente.

> Como as médias são calculadas apenas com os dados do período exibido, as primeiras linhas de cada média ficam sem valor até que haja dados suficientes para a janela. Por exemplo, no período de 1 ano, a MM200 só aparece a partir do 200º dia do gráfico.

## Tecnologias

- Python
- [Dash](https://dash.plotly.com/) (interface web e callbacks)
- [Plotly](https://plotly.com/python/) (gráficos)
- [yfinance](https://github.com/ranaroussi/yfinance) (dados do Yahoo Finance)
- [pandas](https://pandas.pydata.org/) (manipulação de dados e cálculo das médias móveis)

## Estrutura do projeto

```
.
├── app.py       # aplicação completa (layout, callbacks e consulta de dados)
└── README.md
```

## Personalização

As configurações principais ficam no início do `app.py`:

- **Cores:** `COR_FUNDO_PAGINA`, `COR_FUNDO_DADOS` e `COR_FUNDO_GRAFICO`.
- **Períodos:** o dicionário `PERIODOS` define, para cada período, o número de dias corridos, o intervalo dos dados e a quantidade de dias úteis.
- **Médias móveis:** o dicionário `MEDIAS` define o nome e a janela de cada média. Para incluir, por exemplo, uma média de 100 períodos, basta adicionar `"MM100": 100`.

## Limitações

- Somente ações negociadas na B3 são suportadas, pois o sufixo `.SA` é sempre adicionado ao ticker.
- Os dados dependem do Yahoo Finance, que é uma fonte gratuita e não oficial. Podem existir atrasos, lacunas ou diferenças em relação aos números divulgados pelas empresas.
- O gráfico utiliza o preço de fechamento sem ajuste por proventos.
- Alguns indicadores podem não estar disponíveis para todas as empresas.
- Para períodos curtos, a disponibilidade de dados intradiários depende do horário de funcionamento do mercado.

## Aviso

Este projeto tem finalidade educacional e informativa. Nada aqui constitui recomendação de compra ou venda de ativos. Confira sempre as informações em fontes oficiais antes de tomar qualquer decisão de investimento.
