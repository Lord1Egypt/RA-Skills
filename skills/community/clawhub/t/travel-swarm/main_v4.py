#!/usr/bin/env python3.8
"""
TravelMaster V4 - Flask后端API + 静态文件服务
"""

import sys
sys.path.insert(0, '/home/admin/.openclaw/workspace/travel_swarm')

import os
import asyncio
import json
from flask import Flask, request, jsonify, send_file
from dotenv import load_dotenv

load_dotenv('/home/admin/.openclaw/workspace/travel_swarm/.env')

from backend.agents.travel_swarm_engine import TravelSwarmEngine

app = Flask(__name__, static_folder='/home/admin/.openclaw/workspace/travel_swarm/frontend')
engine = TravelSwarmEngine()

@app.route('/')
def index():
    """返回V4前端HTML（无外部CDN依赖）"""
    return send_file('/home/admin/.openclaw/workspace/travel_swarm/frontend/index_v4_simple.html')

@app.route('/api/travel', methods=['POST'])
def travel_api():
    """核心API - 处理旅行请求"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        phase = data.get('phase', 'discovery')
        
        print(f"[API] 收到请求: {message[:50]}... phase={phase}")
        
        # 运行async引擎
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(engine.process_user_message(message))
        loop.close()
        
        print(f"[API] 返回: phase={result.get('phase')}, progress={result.get('progress')}")
        
        return jsonify(result)
        
    except Exception as e:
        print(f"[API Error] {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "reply": f"❌ 系统错误: {str(e)}",
            "phase": "error",
            "progress": 0,
            "thoughts": f"[ERROR] {str(e)}"
        }), 500

@app.route('/health')
def health():
    """健康检查"""
    return jsonify({"status": "ok", "service": "TravelMaster V4"})

if __name__ == '__main__':
    print("🧳 TravelMaster V4 工业级启动（端口7860）")
    print("📝 灯塔进度树 + SPVC决策框架 + 边缘情况处理")
    app.run(host='0.0.0.0', port=7860, debug=False)