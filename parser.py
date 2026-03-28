import re, sqlite3, time
from datetime import datetime

DB = "/home/student/dashboard/events.db"
ALERT_FILE = "/var/log/snort/alert"

def init_db():
    conn = sqlite3.connect(DB)
    conn.execute("""CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, source_ip TEXT, dest_ip TEXT, severity TEXT, message TEXT)""")
    conn.commit()
    conn.close()

def classify(msg):
    m = msg.lower()
    if "scan" in m: return "WARNING"
    if "mysql" in m: return "WARNING"
    if "sql" in m: return "CRITICAL"
    return "INFO"

def parse_alerts():
    try:
        conn = sqlite3.connect(DB)
        with open(ALERT_FILE) as f:
            content = f.read()
        blocks = content.strip().split("\n\n")
        for block in blocks:
            lines = block.strip().split("\n")
            if len(lines) < 2: continue
            import re as r
            msg_m = r.search(r"\[\*\*\] .+? (.+?) \[\*\*\]", lines[0])
            ip_m = r.search(r"(\d+\.\d+\.\d+\.\d+):\d+ -> (\d+\.\d+\.\d+\.\d+)", block)
            if msg_m and ip_m:
                msg = msg_m.group(1).strip()
                src = ip_m.group(1)
                dst = ip_m.group(2)
                ex = conn.execute("SELECT id FROM events WHERE message=? AND source_ip=? LIMIT 1",(msg,src)).fetchone()
                if not ex:
                    conn.execute("INSERT INTO events (timestamp,source_ip,dest_ip,severity,message) VALUES (?,?,?,?,?)",(datetime.now().isoformat(),src,dst,classify(msg),msg))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

init_db()
parse_alerts()
print("Done parsing!")
