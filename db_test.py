import sqlite3

conn = sqlite3.connect("tool_vision.db")
with conn:
    cur = conn.cursor()
    cur.execute("select * from TOOL_TABLE")
    rows = cur.fetchall()
    for row in rows:
        print(row)
