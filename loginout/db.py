import sqlite3
conn = sqlite3.connect("database.db")
conn.execute(
    """
    DROP TABLE board;
    """
)
conn.execute(
    """
    CREATE TABLE board (user text, pwd text);
    """)
conn.close()


