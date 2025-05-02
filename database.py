import sqlite3
from datetime import datetime

DB_FILE = "sugestoes.db"

def inicializar_banco():
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # Criar a tabela, se não existir
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS sugestoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_hora TEXT NOT NULL,
            nome TEXT NOT NULL,
            username TEXT,
            user_id INTEGER NOT NULL,
            sugestao TEXT NOT NULL
        )
        """)

        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Erro ao inicializar o banco de dados: {e}")

def salvar_sugestao_no_banco(nome, username, user_id, sugestao):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # Inserir a sugestão no banco de dados
        cursor.execute("""
        INSERT INTO sugestoes (data_hora, nome, username, user_id, sugestao)
        VALUES (?, ?, ?, ?, ?)
        """, (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), nome, username, user_id, sugestao))

        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Erro ao salvar sugestão no banco de dados: {e}")