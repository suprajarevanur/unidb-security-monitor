from flask import Flask, jsonify, render_template_string
import sqlite3

app = Flask(__name__)
DB = "/home/student/dashboard/events.db"

def query(sql):
    conn = sqlite3.connect(DB)
    rows = conn.execute(sql).fetchall()
    conn.close()
    return rows

@app.route('/api/events')
def events():
    rows = query("SELECT * FROM events ORDER BY timestamp DESC LIMIT 100")
    return jsonify([{"id":r[0],"timestamp":r[1],"source_ip":r[2],"dest_ip":r[3],"severity":r[4],"message":r[5]} for r in rows])

@app.route('/api/stats')
def stats():
    total = query("SELECT COUNT(*) FROM events")[0][0]
    critical = query("SELECT COUNT(*) FROM events WHERE severity='CRITICAL'")[0][0]
    warning = query("SELECT COUNT(*) FROM events WHERE severity='WARNING'")[0][0]
    ips = query("SELECT COUNT(DISTINCT source_ip) FROM events")[0][0]
    return jsonify({"total":total,"critical":critical,"warning":warning,"unique_ips":ips})

@app.route('/')
def index():
    return render_template_string(open('/home/student/dashboard/index.html').read())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)
