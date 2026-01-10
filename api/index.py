from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# 功能 1: Hello
@app.route('/api/hello')
def hello():
    return "嗨！這是從 index.py 發出的問候"

# 功能 2: 加法
@app.route('/api/add')
def add():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return str(a + b)

# 功能 3: 天氣
@app.route('/api/weather')
def weather():
    try:
        # 抓取真實氣象資料
        resp = requests.get("https://wttr.in/Taipei?format=j1", timeout=5)
        data = resp.json()
        current = data['current_condition'][0]
        return jsonify({
            "city": "台北",
            "temp": f"{current['temp_C']}°C",
            "desc": current['weatherDesc'][0]['value']
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
