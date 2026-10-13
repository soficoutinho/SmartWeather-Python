"""Persistência local do histórico em SQLite."""
import csv
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "historico.db"


def initialize():
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute("""CREATE TABLE IF NOT EXISTS consultas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            consultado_em TEXT DEFAULT CURRENT_TIMESTAMP,
            cidade TEXT NOT NULL, pais TEXT, horario TEXT,
            temperatura REAL, sensacao REAL, umidade REAL,
            precipitacao REAL, vento REAL, codigo INTEGER
        )""")


def save(data):
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute("""INSERT INTO consultas
            (cidade,pais,horario,temperatura,sensacao,umidade,precipitacao,vento,codigo)
            VALUES (?,?,?,?,?,?,?,?,?)""", tuple(data[key] for key in (
            "cidade", "pais", "horario", "temperatura", "sensacao", "umidade",
            "precipitacao", "vento", "codigo")))


def recent(limit=15):
    with sqlite3.connect(DB_PATH) as connection:
        return connection.execute("""SELECT consultado_em,cidade,pais,temperatura,
            sensacao,umidade,precipitacao,vento FROM consultas
            ORDER BY id DESC LIMIT ?""", (limit,)).fetchall()


def export_csv(path):
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.execute("""SELECT consultado_em,cidade,pais,horario,
            temperatura,sensacao,umidade,precipitacao,vento,codigo
            FROM consultas ORDER BY id DESC""")
        with open(path, "w", newline="", encoding="utf-8-sig") as file:
            writer = csv.writer(file)
            writer.writerow([column[0] for column in cursor.description])
            writer.writerows(cursor.fetchall())
