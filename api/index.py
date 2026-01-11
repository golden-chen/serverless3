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
@app.route('/api/test/123')
def test():
    return "嗨！這是test123發出的問候"
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
@app.route('/api/weather1')
def weather1():
    # 取得前端傳來的城市名稱，預設為 Taipei
    city = request.args.get('city', 'Taipei')
    
    try:
        # 動態將城市名稱放入網址
        url = f"https://wttr.in/{city}?format=j1"
        resp = requests.get(url, timeout=5)
        
        if resp.status_code != 200:
            return jsonify({"error": "找不到該城市或服務暫時不可用"}), 404
            
        data = resp.json()
        current = data['current_condition'][0]
        
        return jsonify({
            "city": city.capitalize(),
            "temp": f"{current['temp_C']}°C",
            "desc": current['weatherDesc'][0]['value'],
            "humidity": f"{current['humidity']}%"
        })
    except Exception as e:
        return jsonify({"error": "系統發生錯誤，請稍後再試"}), 500
