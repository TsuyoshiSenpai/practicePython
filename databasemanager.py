import sqlite3

class DatabaseManager:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_name)

    def disconnect(self):
        if self.conn:
            self.conn.close()

    def create_scores_table(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_name TEXT,
                score INTEGER
            )
        """)
        self.conn.commit()

    def insert_score(self, player_name, score):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO scores (player_name, score) VALUES (?, ?)", (player_name, score))
        self.conn.commit()

    def get_top_players(self, limit=5):
        cursor = self.conn.cursor()
        cursor.execute("SELECT player_name, score FROM scores ORDER BY score DESC LIMIT ?", (limit,))
        top_players = cursor.fetchall()
        return top_players
