from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import sqlite3
import os
import uuid
import requests
from datetime import datetime
import json

# 设置路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(SCRIPT_DIR)

# 初始化Flask应用
app = Flask(__name__, 
            template_folder=os.path.join(SKILL_ROOT, 'templates'),
            static_folder=os.path.join(SKILL_ROOT, 'static'))
app.config['SECRET_KEY'] = 'short-script-secret-key-2026'
app.config['DATABASE'] = os.path.join(SKILL_ROOT, 'data', 'scripts.db')

# 测试模式：设置为False启用真实支付
TEST_MODE = False

# SkillPay 配置
SKILLPAY_API_KEY = 'sk_d11f398e77b6e892eb7a7d421fe912dde27322cf1792366b776b72bd459d3c2e'
SKILL_ID = 'short-video-script-generator'
BILLING_URL = "https://skillpay.me/api/v1/billing"
HEADERS = {
    "X-API-Key": SKILLPAY_API_KEY, 
    "Content-Type": "application/json"
}

# 硅基流动API配置
SILICONFLOW_API_KEY = 'sk-ggfjehtmwgthcdyajhpipxhurytmnmqsnvpfzoripdgdmzar'
SILICONFLOW_API_URL = 'https://api.siliconflow.cn/v1/chat/completions'
AI_MODEL = 'Doubao-ai/doubao-seed-v2-18k'

# 初始化数据库
def init_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    c = conn.cursor()
    
    # 创建脚本表
    c.execute('''CREATE TABLE IF NOT EXISTS scripts
                 (id TEXT PRIMARY KEY,
                  user_id TEXT,
                  topic TEXT,
                  platform TEXT,
                  duration INTEGER,
                  hook TEXT,
                  shots TEXT,
                  voiceover TEXT,
                  subtitle TEXT,
                  bgm TEXT,
                  cta TEXT,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    conn.commit()
    conn.close()

# 调用AI生成脚本
def generate_script(topic, platform, duration):
    prompt = f"""
你是专业的短视频脚本创作专家，请为{platform}平台创作一个{duration}秒的短视频脚本，主题是：{topic}。

要求结构完整，严格按照以下JSON格式返回，不要有其他额外内容：
{{
  "hook": "前3秒的钩子文案，要足够吸引人停留",
  "shots": [
    {{
      "time": "0-3秒",
      "description": "镜头画面描述"
    }},
    {{
      "time": "3-8秒",
      "description": "镜头画面描述"
    }}
    // 更多镜头，覆盖整个{duration}秒时长
  ],
  "voiceover": "完整的口播词，和镜头时间对应",
  "subtitle": "同步的字幕文案，适合{platform}平台风格",
  "bgm": "背景音乐风格建议，适合{platform}和主题",
  "cta": "结尾引导语，符合{platform}平台的转化风格"
}}

注意：
1. 严格控制总时长为{duration}秒
2. 前3秒的hook必须足够有冲击力，能留住用户
3. 口播词要口语化，符合短视频节奏
4. 字幕要简洁，突出重点
5. CTA要明确，引导用户点赞/关注/评论/点击链接等
"""
    
    try:
        headers = {
            'Authorization': f'Bearer {SILICONFLOW_API_KEY}',
            'Content-Type': 'application/json'
        }
        payload = {
            'model': AI_MODEL,
            'messages': [{'role': 'user', 'content': prompt}],
            'temperature': 0.7,
            'max_tokens': 2000,
            'response_format': {"type": "json_object"}
        }
        resp = requests.post(SILICONFLOW_API_URL, headers=headers, json=payload, timeout=30)
        data = resp.json()
        content = data['choices'][0]['message']['content']
        return json.loads(content)
    except Exception as e:
        print(f"AI生成失败: {e}")
        # 兜底模拟数据
        return {
            "hook": f"3秒告诉你{topic}的秘密！",
            "shots": [
                {"time": "0-3秒", "description": "特写惊讶表情，配大字标题"},
                {"time": "3-8秒", "description": "展示{topic}相关内容"},
                {"time": "8-12秒", "description": "演示操作过程"},
                {"time": "12-15秒", "description": "展示结果，引导关注"}
            ],
            "voiceover": f"你知道吗？关于{topic}的这个技巧90%的人都不知道，今天我就告诉你，看完记得收藏哦！",
            "subtitle": f"{topic}技巧分享 | 90%的人不知道 | 收藏起来",
            "bgm": "轻快活泼的电子音乐，节奏120BPM",
            "cta": "觉得有用的话点赞关注，下期分享更多干货！"
        }

# SkillPay 支付相关函数
def charge_user(user_id: str):
    if TEST_MODE:
        return {"ok": True, "balance": 1000}
    try:
        resp = requests.post(f"{BILLING_URL}/charge", headers=HEADERS, json={
            "user_id": user_id, "skill_id": SKILL_ID, "amount": 0.001,
        }, timeout=10)
        data = resp.json()
        if data.get("success"):
            return {"ok": True, "balance": data.get("balance")}
        return {
            "ok": False, 
            "balance": data.get("balance"), 
            "payment_url": data.get("payment_url")
        }
    except Exception as e:
        print(f"扣费失败: {e}")
        return {"ok": False, "error": str(e)}

# 验证支付中间件
@app.before_request
def check_payment():
    if not TEST_MODE and request.endpoint not in ['index', 'pay', 'static'] and not session.get('payment_verified'):
        user_id = session.get('user_id', str(uuid.uuid4()))
        session['user_id'] = user_id
        charge_result = charge_user(user_id)
        if not charge_result.get('ok'):
            payment_url = charge_result.get('payment_url')
            return render_template('payment_required.html', payment_url=payment_url, test_mode=TEST_MODE) if payment_url else '余额不足，请先充值', 402
        session['payment_verified'] = True

# 路由
@app.route('/')
def index():
    if TEST_MODE and request.args.get('test_payment') == 'success':
        session['payment_verified'] = True
    return render_template('index.html')

@app.route('/pay')
def pay():
    user_id = session.get('user_id', str(uuid.uuid4()))
    session['user_id'] = user_id
    if TEST_MODE:
        return redirect(url_for('index', test_payment='success'))
    try:
        resp = requests.post(f"{BILLING_URL}/payment-link", headers=HEADERS, json={
            "user_id": user_id, "amount": 0.001,
        }, timeout=10)
        payment_url = resp.json().get("payment_url")
        return redirect(payment_url) if payment_url else '获取支付链接失败', 500
    except Exception as e:
        print(f"获取支付链接失败: {e}")
        return '获取支付链接失败', 500

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    topic = data.get('topic', '')
    platform = data.get('platform', '')
    duration = int(data.get('duration', 15))
    
    if not topic or not platform:
        return jsonify({"error": "请填写完整信息"}), 400
    
    script = generate_script(topic, platform, duration)
    
    # 保存到数据库
    user_id = session.get('user_id', str(uuid.uuid4()))
    script_id = str(uuid.uuid4())
    conn = sqlite3.connect(app.config['DATABASE'])
    c = conn.cursor()
    c.execute('''INSERT INTO scripts (id, user_id, topic, platform, duration, hook, shots, voiceover, subtitle, bgm, cta)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (script_id, user_id, topic, platform, duration, script['hook'], json.dumps(script['shots']),
               script['voiceover'], script['subtitle'], script['bgm'], script['cta']))
    conn.commit()
    conn.close()
    
    return jsonify({"success": True, "script": script, "id": script_id})

@app.route('/scripts', methods=['GET'])
def get_scripts():
    user_id = session.get('user_id', str(uuid.uuid4()))
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT id, topic, platform, duration, created_at FROM scripts WHERE user_id = ? ORDER BY created_at DESC', (user_id,))
    scripts = [dict(row) for row in c.fetchall()]
    conn.close()
    return jsonify({"success": True, "scripts": scripts})

@app.route('/script/<script_id>', methods=['GET'])
def get_script(script_id):
    user_id = session.get('user_id', str(uuid.uuid4()))
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM scripts WHERE id = ? AND user_id = ?', (script_id, user_id))
    row = c.fetchone()
    if not row:
        return jsonify({"error": "脚本不存在"}), 404
    script = dict(row)
    script['shots'] = json.loads(script['shots'])
    conn.close()
    return jsonify({"success": True, "script": script})

@app.route('/script/<script_id>', methods=['DELETE'])
def delete_script(script_id):
    user_id = session.get('user_id', str(uuid.uuid4()))
    conn = sqlite3.connect(app.config['DATABASE'])
    c = conn.cursor()
    c.execute('DELETE FROM scripts WHERE id = ? AND user_id = ?', (script_id, user_id))
    conn.commit()
    conn.close()
    return jsonify({"success": True})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5003, debug=True)
