from flask import Flask, jsonify, request, abort
import subprocess
import sys
import os

app = Flask(__name__)

P = {
    "price": "0.01 USDC",
    "wallet": "0x1a9275EE18488A20C7898C666484081F74Ee10CA",
    "chain": "base"
}

# 支付验证
@app.before_request
def check_payment():
    if request.path == '/':
        return None
    if request.path.startswith(('/ssq', '/dlt')):
        x402 = request.headers.get('x402')
        if not x402:
            abort(402, description="Payment required: 0.01 USDC")

@app.route('/')
def index():
    return jsonify({
        "endpoints": ["/ssq", "/dlt"],
        "info": "Rich Lottery Analysis API",
        "pricing": P
    })

@app.route('/ssq')
def ssq():
    try:
        result = subprocess.run(
            [sys.executable, "scripts/lottery_analysis.py", "ssq"],
            capture_output=True,
            text=True,
            timeout=10,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        return result.stdout
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/dlt')
def dlt():
    try:
        result = subprocess.run(
            [sys.executable, "scripts/lottery_analysis.py", "dlt"],
            capture_output=True,
            text=True,
            timeout=10,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        return result.stdout
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
