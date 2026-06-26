#!/usr/bin/env python3.8
"""TravelMaster V7 - FlyAI真实票价集成版"""

import sys
sys.path.insert(0, '/home/admin/.openclaw/workspace/travel_swarm')

import os
import asyncio
import json
from flask import Flask, request, jsonify, send_file
from dotenv import load_dotenv

load_dotenv('/home/admin/.openclaw/workspace/travel_swarm/.env')

from backend.agents.travel_swarm_engine_v7 import TravelSwarmEngine

app = Flask(__name__, static_folder='/home/admin/.openclaw/workspace/travel_swarm/frontend')
engine = TravelSwarmEngine()

@app.route('/')
def index():
    """返回V7融合版前端（FlyAI+腾讯POI+高德导航）"""
    return send_file('/home/admin/.openclaw/workspace/travel_swarm/frontend/index_v7_fusion.html')

@app.route('/api/travel', methods=['POST'])
def travel_api():
    """Phase 1-3: 收敛→辩论→SPVC推荐"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(engine.process_user_message(message))
        loop.close()
        
        return jsonify(result)
    except Exception as e:
        return jsonify({
            "reply": f"❌ 错误: {str(e)}",
            "phase": "error",
            "thoughts": f"[ERROR] {str(e)}"
        }), 500

@app.route('/api/select_plan', methods=['POST'])
def select_plan():
    """Phase 4: 用户选择后生成HTML"""
    try:
        data = request.get_json()
        plan = data.get('plan', 'A')
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(engine.generate_final_html(plan))
        loop.close()
        
        return jsonify(result)
    except Exception as e:
        return jsonify({
            "reply": f"❌ 生成错误: {str(e)}",
            "phase": "error"
        }), 500

@app.route('/api/reset', methods=['POST'])
def reset_session():
    """重置会话"""
    engine.reset()
    return jsonify({"status": "ok", "message": "已重置"})

@app.route('/api/flights', methods=['GET'])
def get_flights():
    """获取真实航班数据"""
    return jsonify({
        "flights": engine.flight_data or [],
        "count": len(engine.flight_data or [])
    })

@app.route('/api/trains', methods=['GET'])
def get_trains():
    """获取真实火车数据"""
    return jsonify({
        "trains": engine.train_data or [],
        "count": len(engine.train_data or [])
    })

@app.route('/health')
def health():
    return jsonify({
        "status": "ok",
        "version": "V7",
        "features": ["FlyAI真实票价", "飞猪预订链接", "真实航班/火车查询"]
    })

if __name__ == '__main__':
    print("🧳 TravelMaster V7 FlyAI真实票价版启动")
    print("✅ FlyAI MCP已集成")
    print("✅ 真实航班票价查询")
    print("✅ 飞猪预订链接")
    app.run(host='0.0.0.0', port=7860)