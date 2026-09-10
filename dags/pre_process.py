import pandas as pd

def process_data():

    data = pd.read_csv("~/ip_files/or1.csv")

    data['total_price'] = data['UnitPrice'] * data['Quantity']

    g_data = data.groupby(
        ['StockCode', 'Description', 'Country'],
        as_index=False
    )['total_price'].sum()

    g_data.to_csv(
        "/usr/local/airflow/mysql_data/fin.csv",
        index=False
    )