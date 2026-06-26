from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3
import os
import uuid
import requests
from datetime import datetime, timedelta
import random
import json

# 设置路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(SCRIPT_DIR)

# 初始化Flask应用
app = Flask(__name__, 
            template_folder=os.path.join(SKILL_ROOT, 'templates'),
            static_folder=os.path.join(SKILL_ROOT, 'static'))
app.config['SECRET_KEY'] = 'youtube-manager-secret-key'
app.config['DATABASE'] = os.path.join(SKILL_ROOT, 'data', 'youtube.db')

# 测试模式：设置为False启用真实支付
TEST_MODE = False

# SkillPay 配置
SKILLPAY_API_KEY = 'sk_d11f398e77b6e892eb7a7d421fe912dde27322cf1792366b776b72bd459d3c2e'
SKILL_ID = 'youtube-content-manager-pro'
BILLING_URL = "https://skillpay.me/api/v1/billing"
HEADERS = {
    "X-API-Key": SKILLPAY_API_KEY, 
    "Content-Type": "application/json"
}

# 硅基流动API配置
SILICONFLOW_API_KEY = 'sk-ggfjehtmwgthcdyajhpipxhurytmnmqsnvpfzoripdgdmzar'
SILICONFLOW_API_URL = 'https://api.siliconflow.cn/v1/chat/completions'
AI_MODEL = 'Doubao-ai/doubao-seed-v2-18k'

# 调用硅基流动API函数
def call_ai(prompt):
    headers = {
        'Authorization': f'Bearer {SILICONFLOW_API_KEY}',
        'Content-Type': 'application/json'
    }
    payload = {
        'model': AI_MODEL,
        'messages': [{'role': 'user', 'content': prompt}],
        'temperature': 0.7,
        'max_tokens': 4000
    }
    try:
        response = requests.post(SILICONFLOW_API_URL, headers=headers, json=payload, timeout=60)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            print(f"API调用失败: {response.status_code}, {response.text}")
            return None
    except Exception as e:
        print(f"API调用异常: {e}")
        return None

# 初始化数据库
def init_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    c = conn.cursor()
    
    # 创建选题表
    c.execute('''CREATE TABLE IF NOT EXISTS topics
                 (id TEXT PRIMARY KEY, 
                  niche TEXT, 
                  title TEXT, 
                  difficulty INTEGER, 
                  traffic_potential INTEGER,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    # 创建脚本表
    c.execute('''CREATE TABLE IF NOT EXISTS scripts
                 (id TEXT PRIMARY KEY,
                  topic_id TEXT,
                  title TEXT,
                  content TEXT,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    # 创建发布记录表
    c.execute('''CREATE TABLE IF NOT EXISTS publish_records
                 (id TEXT PRIMARY KEY,
                  topic TEXT,
                  title TEXT,
                  publish_date DATE,
                  views INTEGER DEFAULT 0,
                  ctr REAL DEFAULT 0.0,
                  likes INTEGER DEFAULT 0,
                  comments INTEGER DEFAULT 0,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    conn.commit()
    conn.close()

# 数据库操作装饰器
def with_db(func):
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect(app.config['DATABASE'])
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            return result
        finally:
            conn.close()
    return wrapper

# SkillPay 支付相关函数
def charge_user(user_id: str):
    if TEST_MODE:
        return {"ok": True, "balance": 1000}
    try:
        resp = requests.post(f"{BILLING_URL}/charge", headers=HEADERS, json={
            "user_id": user_id, "skill_id": SKILL_ID, "amount": 0,
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

# 路由
@app.route('/')
def index():
    if TEST_MODE and request.args.get('test_payment') == 'success':
        session['payment_verified'] = True
    # 传入当前日期
    current_date = datetime.now().strftime('%Y-%m-%d')
    return render_template('index.html', test_mode=TEST_MODE, current_date=current_date)

@app.route('/pay')
def pay():
    user_id = session.get('user_id', str(uuid.uuid4()))
    session['user_id'] = user_id
    if TEST_MODE:
        return redirect(url_for('index', test_payment='success'))
    try:
        resp = requests.post(f"{BILLING_URL}/payment-link", headers=HEADERS, json={
            "user_id": user_id, "amount": 8,
        }, timeout=10)
        payment_url = resp.json().get("payment_url")
        return redirect(payment_url) if payment_url else '获取支付链接失败', 500
    except Exception as e:
        print(f"获取支付链接失败: {e}")
        return '获取支付链接失败', 500

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

# 选题生成
@app.route('/generate_topics', methods=['POST'])
def generate_topics():
    niche = request.form.get('niche', '')
    if not niche:
        return jsonify({"error": "请输入内容领域"}), 400
    
    # 调用硅基流动AI生成选题
    prompt = f"""
你是专业的YouTube内容选题专家，擅长为{niche}领域创作高流量选题。
请生成30个适合YouTube的选题，要求：
1. 每个选题要吸引人，符合YouTube用户喜好
2. 每个选题标注难度（1-10分，越高越难制作）
3. 每个选题标注流量潜力（1-10分，越高流量潜力越大）
4. 返回格式为严格JSON，不需要其他说明：
[
  {{"title": "选题1标题", "difficulty": 5, "traffic_potential": 8}},
  {{"title": "选题2标题", "difficulty": 3, "traffic_potential": 6}}
]
"""
    
    ai_response = call_ai(prompt)
    
    # 如果AI调用失败，用模拟数据兜底
    if not ai_response:
        topics = []
        prefix_options = ["如何", "为什么", "2026年最新", "保姆级教程", "避坑指南"]
        suffix_options = ["技巧", "方法", "攻略", "经验", "分享"]
        for i in range(30):
            difficulty = random.randint(1, 10)
            traffic = random.randint(1, 10)
            topics.append({
                "id": str(uuid.uuid4()),
                "title": f"{niche}相关选题{i+1}: {random.choice(prefix_options)} {random.choice(suffix_options)}",
                "difficulty": difficulty,
                "traffic_potential": traffic,
                "score": difficulty * 0.3 + traffic * 0.7
            })
    else:
        try:
            # 解析AI返回的JSON
            import json
            ai_topics = json.loads(ai_response)
            topics = []
            for t in ai_topics:
                difficulty = t.get('difficulty', random.randint(1, 10))
                traffic = t.get('traffic_potential', random.randint(1, 10))
                topics.append({
                    "id": str(uuid.uuid4()),
                    "title": t.get('title', '未命名选题'),
                    "difficulty": difficulty,
                    "traffic_potential": traffic,
                    "score": difficulty * 0.3 + traffic * 0.7
                })
        except:
            # 解析失败用模拟数据
            topics = []
            for i in range(30):
                difficulty = random.randint(1, 10)
                traffic = random.randint(1, 10)
                topics.append({
                    "id": str(uuid.uuid4()),
                    "title": f"{niche}选题{i+1}",
                    "difficulty": difficulty,
                    "traffic_potential": traffic,
                    "score": difficulty * 0.3 + traffic * 0.7
                })
    
    # 按综合得分排序
    topics.sort(key=lambda x: x['score'], reverse=True)
    
    # 保存到数据库
    conn = sqlite3.connect(app.config['DATABASE'])
    c = conn.cursor()
    for topic in topics:
        c.execute('INSERT INTO topics (id, niche, title, difficulty, traffic_potential) VALUES (?, ?, ?, ?, ?)',
                 (topic['id'], niche, topic['title'], topic['difficulty'], topic['traffic_potential']))
    conn.commit()
    conn.close()
    
    return jsonify({"topics": topics})

# 脚本生成
@app.route('/generate_script', methods=['POST'])
def generate_script():
    topic_id = request.form.get('topic_id', '')
    topic_title = request.form.get('topic_title', '')
    
    if not topic_id or not topic_title:
        return jsonify({"error": "参数错误"}), 400
    
    # 调用硅基流动AI生成完整内容
    prompt = f"""
你是专业的YouTube内容创作者，现在要创作一个关于"{topic_title}"的视频，时长5-8分钟。
请按照以下要求生成内容，返回严格JSON格式，不需要其他说明：
{{
  "script": "完整的视频脚本，包含开场、各部分内容、结尾，分时间段标注",
  "titles": [
    {{"title": "标题1", "seo_score": 95, "is_best": true}},
    {{"title": "标题2", "seo_score": 85, "is_best": false}}
  ],
  "description": "500字左右的YouTube视频描述，要包含关键词，利于SEO",
  "tags": ["标签1", "标签2", "...共30个标签"],
  "thumbnail": {{
    "main_text": "缩略图上的大字文案，要吸引人",
    "sub_text": "副标题文案",
    "color_scheme": {{"bg": "#颜色代码", "text": "#颜色代码"}}
  }}
}}
要求：
- 脚本要口语化，适合YouTube风格，包含互动引导（比如点赞订阅）
- 生成5个标题，每个标注SEO得分（0-100），其中1个最优
- 标签要和内容相关，共30个，包含热门关键词
- 缩略图配色要醒目，适合YouTube风格
"""
    
    ai_response = call_ai(prompt)
    
    if ai_response:
        try:
            import json
            data = json.loads(ai_response)
            script_content = data.get('script', '')
            titles = data.get('titles', [])
            description = data.get('description', '')
            tags = data.get('tags', [])
            thumbnail = data.get('thumbnail', {})
        except:
            # 解析失败用模拟数据
            script_content = f"""# {topic_title}
（视频时长：约7分钟）
## 开场 (0:00-0:30)
大家好，今天我们来聊聊{topic_title}，这个问题很多人都遇到过，今天一次性给你讲清楚。
## 第一部分 (0:30-2:30)
首先我们来了解基本概念...
## 第二部分 (2:30-5:00)
接下来是实操步骤，总共分3步...
## 结尾 (6:30-7:00)
以上就是今天的全部内容，欢迎点赞订阅，我们下期再见！"""
            titles = [
                {"title": f"{topic_title}？看完这篇就够了", "seo_score": 95, "is_best": True},
                {"title": f"{topic_title}的3个秘密", "seo_score": 88, "is_best": False},
                {"title": f"2026年最新{topic_title}攻略", "seo_score": 85, "is_best": False},
                {"title": f"{topic_title}保姆级教程", "seo_score": 82, "is_best": False},
                {"title": f"{topic_title}避坑指南", "seo_score": 79, "is_best": False}
            ]
            description = f"今天给大家分享{topic_title}的详细教程，包含完整的实操步骤、常见问题解答，让你看完就能上手。视频内容适合新手入门，也适合有经验的创作者参考。看完记得点赞收藏，有问题欢迎在评论区留言。"
            tags = [topic_title, "YouTube", "创业", "副业", "教程", "经验分享", "2026", "新手", "入门", "攻略"] + [f"标签{i}" for i in range(20)]
            thumbnail = {
                "main_text": "保姆级教程",
                "sub_text": topic_title[:20] + "...",
                "color_scheme": {"bg": "#1E90FF", "text": "#FFFFFF"}
            }
    else:
        # API调用失败用模拟数据
        script_content = f"""# {topic_title}
（视频时长：约7分钟）
## 开场 (0:00-0:30)
大家好，今天我们来聊聊{topic_title}，这个问题很多人都遇到过，今天一次性给你讲清楚。"""
        titles = [{"title": f"{topic_title}教程", "seo_score": 90, "is_best": True}]
        description = f"{topic_title}详细教程"
        tags = [topic_title, "教程"]
        thumbnail = {"main_text": "干货", "sub_text": "", "color_scheme": {"bg": "#FF3366", "text": "#FFFFFF"}}
    
    # 保存脚本
    script_id = str(uuid.uuid4())
    conn = sqlite3.connect(app.config['DATABASE'])
    c = conn.cursor()
    c.execute('INSERT INTO scripts (id, topic_id, title, content) VALUES (?, ?, ?, ?)',
             (script_id, topic_id, topic_title, script_content))
    conn.commit()
    conn.close()
    
    return jsonify({
        "script_id": script_id,
        "content": script_content,
        "titles": titles,
        "description": description,
        "tags": tags,
        "thumbnail": thumbnail
    })

# 保存发布记录
@app.route('/save_publish', methods=['POST'])
def save_publish():
    data = request.json
    record_id = str(uuid.uuid4())
    
    conn = sqlite3.connect(app.config['DATABASE'])
    c = conn.cursor()
    c.execute('''INSERT INTO publish_records 
                 (id, topic, title, publish_date, views, ctr, likes, comments)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
             (record_id, 
              data.get('topic', ''),
              data.get('title', ''),
              data.get('publish_date', datetime.now().strftime('%Y-%m-%d')),
              data.get('views', 0),
              data.get('ctr', 0.0),
              data.get('likes', 0),
              data.get('comments', 0)))
    conn.commit()
    conn.close()
    
    return jsonify({"success": True, "id": record_id})

# 获取发布记录
@app.route('/get_records')
def get_records():
    conn = sqlite3.connect(app.config['DATABASE'])
    c = conn.cursor()
    c.execute('SELECT * FROM publish_records ORDER BY publish_date DESC')
    records = []
    for row in c.fetchall():
        records.append({
            "id": row[0],
            "topic": row[1],
            "title": row[2],
            "publish_date": row[3],
            "views": row[4],
            "ctr": row[5],
            "likes": row[6],
            "comments": row[7]
        })
    conn.close()
    return jsonify({"records": records})

# 数据分析
@app.route('/analyze')
def analyze():
    conn = sqlite3.connect(app.config['DATABASE'])
    c = conn.cursor()
    
    # 获取最近30天的数据
    thirty_days_ago = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    c.execute('''SELECT topic, SUM(views) as total_views, AVG(ctr) as avg_ctr 
                 FROM publish_records 
                 WHERE publish_date >= ?
                 GROUP BY topic
                 ORDER BY total_views DESC''', (thirty_days_ago,))
    
    analysis = []
    for row in c.fetchall():
        analysis.append({
            "topic": row[0],
            "total_views": row[1],
            "avg_ctr": row[2],
            "suggestion": f"该类选题表现优异，建议后续多产出{row[0]}相关内容" if row[1] > 10000 else "该类选题表现一般，建议优化方向"
        })
    
    # 高流量关键词统计
    c.execute('SELECT title FROM publish_records WHERE views > 10000')
    high_performance_titles = [row[0] for row in c.fetchall()]
    
    conn.close()
    
    # 计算最高播放量，处理空数据情况
    max_views = max([a['total_views'] for a in analysis]) if analysis else 0
    
    return jsonify({
        "topic_analysis": analysis,
        "high_performance_titles": high_performance_titles,
        "summary": f"近30天共发布{len(analysis)}类内容，最高播放量{max_views}次"
    })

# 初始化数据库
init_db()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
