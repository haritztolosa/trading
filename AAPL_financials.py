from polygon import RESTClient
import pandas as pd

# Clave API de Polygon (debes reemplazarla con tu propia clave)
API_KEY = 'U1BceN0VNoyG1Qsv_AaVHmhVWuJ0RSXs'

# Crear el cliente y autenticarse con la clave API
client = RESTClient(API_KEY)

# Definir el ticker del stock
stock_ticker = 'AAPL'

# Lista para almacenar los datos financieros
data = []

# Solicitar datos financieros para el ticker AAPL desde el 1 de enero de 2022
for financial in client.vx.list_stock_financials(ticker=stock_ticker, filing_date_gte='2022-01-01'):
    data.append(financial)

# Crear listas para cada columna que deseas extraer
filing_dates = []
end_dates = []
start_dates = []
fiscal_years = []
fiscal_periods = []
company_names = []
tickers = []
income_statement_revenues = []

# Iterar sobre los datos y extraer la información relevante
for financial in data:
    filing_dates.append(financial.filing_date)
    end_dates.append(financial.end_date)
    start_dates.append(financial.start_date)
    fiscal_years.append(financial.fiscal_year)
    fiscal_periods.append(financial.fiscal_period)
    company_names.append(financial.company_name)

    # Acceder a los ingresos del estado de resultados si están disponibles
    if hasattr(financial.financials, 'income_statement') and hasattr(financial.financials.income_statement, 'revenues'):
        income_statement_revenues.append(financial.financials.income_statement.revenues.value)
    else:
        income_statement_revenues.append(None)

    # Manejar los tickers asociados si están disponibles
    tickers_list = financial.tickers if hasattr(financial, 'tickers') else []
    tickers.append(', '.join(tickers_list))

# Crear un DataFrame de Pandas con los datos recopilados
df = pd.DataFrame({
    'Filing Date': filing_dates,
    'End Date': end_dates,
    'Start Date': start_dates,
    'Fiscal Year': fiscal_years,
    'Fiscal Period': fiscal_periods,
    'Company Name': company_names,
    'Tickers': tickers,
    'Income Statement Revenues': income_statement_revenues
})

# Guardar el DataFrame en un archivo CSV
csv_file = 'financial_data_aapl.csv'
df.to_csv(csv_file, index=False)

print(f"Datos guardados exitosamente en {csv_file}")
