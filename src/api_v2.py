import os
import requests
import pandas as pd

# parâmetros
symbol = 'BCP.LS' # empresa do nosso grupo

# Obter a API Key do ambiente
api_key = os.environ.get("API_KEY")
if not api_key:
    raise ValueError("A API Key não está definida. Configure a variável de ambiente 'API_KEY'.")

# Endpoint da API
url = 'https://www.alphavantage.co/query'

params = {
    'function': 'TIME_SERIES_MONTHLY_ADJUSTED',
    'symbol': symbol,
    'apikey': api_key,
    'datatype': 'json'
}

#fazendo a solicitação à API
response = requests.get(url, params=params)
data = response.json()
if "Monthly Adjusted Time Series" not in data:
    print("Erro: Não foram encontrados dados para o símbolo fornecido.")
else: None

# processar os dados
time_series = data["Monthly Adjusted Time Series"]
df = pd.DataFrame.from_dict(time_series, orient = "index")
df.index = pd.to_datetime(df.index)
df.index.name = "date"
df = df[["1. open", "2. high", "3. low", "4. close", "5. adjusted close", "6. volume", "7. dividend amount"]]
df.columns = ["open", "high", "low", "close", "adjusted_close", "volume", "dividend_amount"]
df = df.sort_index() # ordena por data

#salvar meu csv
output_path = r"C:\Users\carlo\Documents\Curso_DataOps\GALP_PROJECT\data\monthly_adjusted_data.csv"
df.to_csv(output_path)
print(df.head())