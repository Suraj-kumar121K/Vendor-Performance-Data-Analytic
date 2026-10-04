import pandas as pd
import os
from sqlalchemy import create_engine
import time
import logging


logging.basicConfig(
    filename="logs/ingestion_db.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a"
)


engine = create_engine(
    "mssql+pyodbc://AS:Sur7aj6%40@localhost\\SQLEXPRESS/master"
    "?driver=ODBC+Driver+18+for+SQL+Server"
    "&Encrypt=yes"
    "&TrustServerCertificate=yes"
)


def ingest_db(df, table_name, engine):

    with engine.begin() as connection:

        df.to_sql(
            table_name,
            con=connection,
            if_exists="replace",
            index=False
        )


def load_raw_data():

    """This function will load the CSVs as DataFrames and ingest them into the database."""

    start = time.time()

    for file in os.listdir('data'):

        if file.endswith('.csv'):

            df = pd.read_csv('data/' + file)

            logging.info(f'Ingesting {file} into DB')

            ingest_db(df, file[:-4], engine)

    end = time.time()

    total_time = (end - start) / 60

    logging.info('------------Ingestion Complete------------')

    logging.info(f'\nTotal Time Taken: {total_time:.2f} minutes')


if __name__ == '__main__':
    load_raw_data()