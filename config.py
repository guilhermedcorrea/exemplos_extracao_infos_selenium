import pyodbc
from sqlalchemy import create_engine
import os
from urllib.parse import quote_plus
from sqlalchemy.engine import URL
from sqlalchemy import text


connection_url = URL.create(
    "mssql+pyodbc",
    username="Aplicacao.Guilherme",
    password="4PL1C4ÇAO_3STOQUF202#",
    host="w2019.hausz.com.br",
    database="HauszMapaDev2",
    query={
        "driver": "ODBC Driver 17 for SQL Server",
        "autocommit": "True",
    },
)


def get_engine():
    engine = create_engine(connection_url).execution_options(
        isolation_level="AUTOCOMMIT", future=True
    )
    return engine