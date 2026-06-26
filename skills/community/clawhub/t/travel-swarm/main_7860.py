#!/usr/bin/env python3
"""
TravelSwarm 旅游规划智能体 - 7860端口（5003已禁用）
使用 MiniMax TokenPlan + 高德真实API + 蜂群审核
"""

import sys
import os

# 添加项目路径
sys.path.insert(0, '/home/admin/.openclaw/workspace/travel_swarm')

import asyncio
import json
from flask import Flask, request, jsonify, render_template_string
from backend.agents.travel_swarm_engine import TravelSwarmEngine

# 加载环境变量
from dotenv import load_dotenv
load_dotenv('/home/admin/.openclaw/workspace/travel_swarm/.env')

# Flask应用
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# 全局引擎实例
engine = None

def init_engine():
    """初始化引擎"""
    global engine
    if engine is None:
        engine = TravelSwarmEngine()

# HTML模板
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>TravelSwarm - 旅游规划智能体</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Microsoft YaHei', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            max-width: 800px;
            width: 90%;
        }
        h1 { 
            color: #667eea;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .subtitle { color: #666; margin-bottom: 20px; }
        
        .chat-box {
            height: 400px;
            border: 2px solid #eee;
            border-radius: 10px;
            padding: 15px;
            overflow-y: auto;
            background: #f9f9f9;
            margin-bottom: 15px;
        }
        .message {
            margin: 10px 0;
            padding: 10px;
            border-radius: 8px;
        }
        .user-msg {
            background: #667eea;
            color: white;
            text-align: right;
        }
        .bot-msg {
            background: #e8e8e8;
            text-align: left;
        }
        
        .input-box {
            display: flex;
            gap: 10px;
        }
        input[type="text"] {
            flex: 1;
            padding: 12px;
            border: 2px solid #eee;
            border-radius: 8px;
            font-size: 16px;
        }
        button {
            padding: 12px 25px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover { background: #764ba2; }
        
        .status {
            margin-top: 20px;
            padding: 10px;
            background: #fffbe6;
            border-radius: 5px;
            font-size: 14px;
        }
        .status ok { color: green; }
        .status warn { color: orange; }
        
        .quick-btns {
            display: flex;
            gap: 10px;
            margin-top: 15px;
        }
        .quick-btn {
            padding: 8px 15px;
            background: #f0f0f0;
            border: 1px solid #ddd;
            border-radius: 5px;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧳 TravelSwarm</h1>
        <p class="subtitle">AI智能旅游规划 · MiniMax TokenPlan · 蜂群审核</p>
        
        <div class="chat-box" id="chatBox">
            <div class="message bot-msg">
                🐝 你好！我是TravelSwarm旅游规划助手。<br>
                告诉我你想去哪里玩，我会帮你生成完整行程~<br>
                <br>
                例如："我想去重庆玩2天，预算2000，2个人，喜欢火锅和夜景"
            </div>
        </div>
        
        <div class="input-box">
            <input type="text" id="userInput" placeholder="输入你的旅行想法..." />
            <button onclick="sendMessage()">发送</button>
        </div>
        
        <div class="quick-btns">
            <button class="quick-btn" onclick="quickPlan('重庆')">重庆2天</button>
            <button class="quick-btn" onclick="quickPlan('成都')">成都3天</button>
            <button class="quick-btn" onclick="quickPlan('西安')">西安2天</button>
            <button class="quick-btn" onclick="quickPlan('厦门')">厦门4天</button>
        </div>
        
        <div class="status" id="status">
            <span class="ok">✅ MiniMax TokenPlan</span> | 
            <span class="warn">⚠️ 高德API待配置</span>
        </div>
    </div>
    
    <script>
        const chatBox = document.getElementById('chatBox');
        const userInput = document.getElementById('userInput');
        
        function addMessage(text, isUser) {
            const msg = document.createElement('div');
            msg.className = 'message ' + (isUser ? 'user-msg' : 'bot-msg');
            msg.innerHTML = text;
            chatBox.appendChild(msg);
            chatBox.scrollTop = chatBox.scrollHeight;
        }
        
        async function sendMessage() {
            const text = userInput.value.trim();
            if (!text) return;
            
            addMessage(text, true);
            userInput.value = '';
            
            try {
                const resp = await fetch('/api/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({message: text})
                });
                const data = await resp.json();
                addMessage(data.response, false);
            } catch (e) {
                addMessage('❌ 网络错误，请重试', false);
            }
        }
        
        async function quickPlan(city) {
            addMessage('快速规划：' + city, true);
            try {
                const resp = await fetch('/api/quick', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({destination: city, days: 2, budget: 2000})
                });
                const data = await resp.json();
                addMessage(data.response, false);
            } catch (e) {
                addMessage('❌ 快速规划失败', false);
            }
        }
        
        userInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendMessage();
        });
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    """主页"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/chat', methods=['POST'])
def chat():
    """对话API"""
    init_engine()
    data = request.get_json()
    message = data.get('message', '')
    
    # 异步调用
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    response = loop.run_until_complete(engine.process_user_message(message))
    loop.close()
    
    return jsonify({'response': response})

@app.route('/api/quick', methods=['POST'])
def quick():
    """快速规划API"""
    init_engine()
    data = request.get_json()
    destination = data.get('destination', '重庆')
    days = data.get('days', 2)
    budget = data.get('budget', 2000)
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    response = loop.run_until_complete(engine.quick_plan(destination, days, budget))
    loop.close()
    
    return jsonify({'response': response})

@app.route('/api/status')
def status():
    """状态检查"""
    return jsonify({
        'status': 'ok',
        'port': 7860,
        'engine': 'TravelSwarm',
        'llm': 'MiniMax-M2.5',
        'amap': os.getenv('AMAP_API_KEY', '未配置')
    })

@app.route('/health')
def health():
    """健康检查"""
    return jsonify({'healthy': True})

if __name__ == '__main__':
    print("🧳 TravelSwarm 启动在 7860端口")
    print("✅ MiniMax TokenPlan + 蜂群审核")
    app.run(host='0.0.0.0', port=7860, debug=False)