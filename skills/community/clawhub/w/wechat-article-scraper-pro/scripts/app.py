from flask import Flask, render_template, request, send_file, redirect, url_for, session, jsonify
import sqlite3
import os
import uuid
import requests
from bs4 import BeautifulSoup
import re
import json
from datetime import datetime
import pandas as pd
from urllib.parse import urljoin
import time
import random

# 设置路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(SCRIPT_DIR)

# 初始化Flask应用
app = Flask(__name__, 
            template_folder=os.path.join(SKILL_ROOT, 'templates'),
            static_folder=os.path.join(SKILL_ROOT, 'static'))
app.config['SECRET_KEY'] = 'wechat-scraper-secret-key'
app.config['DATABASE'] = os.path.join(SKILL_ROOT, 'data', 'wechat.db')
app.config['DOWNLOAD_FOLDER'] = os.path.join(SKILL_ROOT, 'data', 'downloads')

# 测试模式：设置为False启用真实支付
TEST_MODE = False

# SkillPay 配置
SKILLPAY_API_KEY = 'sk_d11f398e77b6e892eb7a7d421fe912dde27322cf1792366b776b72bd459d3c2e'
SKILL_ID = 'wechat-article-scraper'
BILLING_URL = "https://skillpay.me/api/v1/billing"
HEADERS = {
    "X-API-Key": SKILLPAY_API_KEY, 
    "Content-Type": "application/json"
}

# 请求头模拟浏览器
REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1'
}

# 初始化数据库
def init_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    c = conn.cursor()
    
    # 创建抓取任务表
    c.execute('''CREATE TABLE IF NOT EXISTS tasks
                 (id TEXT PRIMARY KEY,
                  official_account TEXT,
                  url TEXT,
                  status TEXT DEFAULT 'pending',
                  total_count INTEGER DEFAULT 0,
                  completed_count INTEGER DEFAULT 0,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    # 创建文章表
    c.execute('''CREATE TABLE IF NOT EXISTS articles
                 (id TEXT PRIMARY KEY,
                  task_id TEXT,
                  title TEXT,
                  author TEXT,
                  publish_time TEXT,
                  content TEXT,
                  url TEXT UNIQUE,
                  cover_image TEXT,
                  read_count INTEGER DEFAULT 0,
                  like_count INTEGER DEFAULT 0,
                  view_count INTEGER DEFAULT 0,
                  tags TEXT,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    conn.commit()
    conn.close()

# 确保目录存在
os.makedirs(app.config['DOWNLOAD_FOLDER'], exist_ok=True)

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
    return render_template('index.html', test_mode=TEST_MODE)

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

# 解析公众号主页获取文章列表
def parse_official_account(url, max_count=100):
    """模拟解析公众号文章，实际使用时需要配合微信客户端或API"""
    articles = []
    
    # 这里是模拟数据，实际部署时需要替换为真实的抓取逻辑
    # 微信公众号反爬严格，需要使用代理、模拟登录等方式
    for i in range(min(max_count, 20)):
        articles.append({
            "title": f"公众号文章{i+1}: 这是一篇精彩的内容",
            "author": "公众号名称",
            "publish_time": (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d'),
            "url": f"https://mp.weixin.qq.com/s/example{i}",
            "cover_image": f"https://example.com/cover{i}.jpg",
            "read_count": random.randint(1000, 100000),
            "like_count": random.randint(10, 1000),
            "view_count": random.randint(500, 50000)
        })
    
    return articles

# 抓取文章内容
def scrape_article_content(url):
    """模拟抓取文章内容"""
    return f"""
# 这是文章标题
## 小标题1
这是文章内容部分，包含文字、图片等元素。
## 小标题2
更多内容...
## 结尾
感谢阅读！
"""

# 创建抓取任务
@app.route('/create_task', methods=['POST'])
def create_task():
    url = request.form.get('url', '')
    max_count = int(request.form.get('max_count', 100))
    
    if not url or 'mp.weixin.qq.com' not in url:
        return jsonify({"error": "请输入有效的微信公众号链接"}), 400
    
    task_id = str(uuid.uuid4())
    
    # 保存任务到数据库
    conn = sqlite3.connect(app.config['DATABASE'])
    c = conn.cursor()
    c.execute('INSERT INTO tasks (id, url, status, total_count) VALUES (?, ?, ?, ?)',
             (task_id, url, 'running', max_count))
    conn.commit()
    conn.close()
    
    # 后台模拟抓取（实际使用时应该用异步任务）
    articles = parse_official_account(url, max_count)
    
    # 保存文章到数据库
    conn = sqlite3.connect(app.config['DATABASE'])
    c = conn.cursor()
    
    for article in articles:
        try:
            content = scrape_article_content(article['url'])
            tags = json.dumps([])
            c.execute('''INSERT OR IGNORE INTO articles 
                         (id, task_id, title, author, publish_time, content, url, cover_image, read_count, like_count, tags)
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                     (str(uuid.uuid4()),
                      task_id,
                      article['title'],
                      article['author'],
                      article['publish_time'],
                      content,
                      article['url'],
                      article['cover_image'],
                      article['read_count'],
                      article['like_count'],
                      tags))
        except Exception as e:
            print(f"保存文章失败: {e}")
            continue
    
    # 更新任务状态
    c.execute('UPDATE tasks SET status = "completed", completed_count = ? WHERE id = ?',
             (len(articles), task_id))
    conn.commit()
    conn.close()
    
    return jsonify({"task_id": task_id, "article_count": len(articles)})

# 获取任务状态
@app.route('/task_status/<task_id>')
def task_status(task_id):
    conn = sqlite3.connect(app.config['DATABASE'])
    c = conn.cursor()
    c.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
    task = c.fetchone()
    conn.close()
    
    if not task:
        return jsonify({"error": "任务不存在"}), 404
    
    return jsonify({
        "id": task[0],
        "official_account": task[1],
        "url": task[2],
        "status": task[3],
        "total_count": task[4],
        "completed_count": task[5],
        "created_at": task[6]
    })

# 获取文章列表
@app.route('/articles/<task_id>')
def get_articles(task_id):
    conn = sqlite3.connect(app.config['DATABASE'])
    c = conn.cursor()
    c.execute('SELECT id, title, author, publish_time, read_count, like_count, url FROM articles WHERE task_id = ? ORDER BY publish_time DESC', (task_id,))
    articles = []
    for row in c.fetchall():
        articles.append({
            "id": row[0],
            "title": row[1],
            "author": row[2],
            "publish_time": row[3],
            "read_count": row[4],
            "like_count": row[5],
            "url": row[6]
        })
    conn.close()
    return jsonify({"articles": articles})

# 导出文章
@app.route('/export/<task_id>/<format>')
def export_articles(task_id, format):
    conn = sqlite3.connect(app.config['DATABASE'])
    c = conn.cursor()
    c.execute('SELECT title, author, publish_time, content, url FROM articles WHERE task_id = ?', (task_id,))
    articles = c.fetchall()
    conn.close()
    
    if not articles:
        return "没有可导出的文章", 404
    
    if format == 'markdown':
        # 导出为Markdown
        md_content = ""
        for article in articles:
            md_content += f"# {article[0]}\n"
            md_content += f"**作者：** {article[1]} | **发布时间：** {article[2]}\n\n"
            md_content += f"**原文链接：** [{article[4]}]({article[4]})\n\n"
            md_content += f"{article[3]}\n\n"
            md_content += "---\n\n"
        
        filename = f"公众号文章_{datetime.now().strftime('%Y%m%d%H%M%S')}.md"
        filepath = os.path.join(app.config['DOWNLOAD_FOLDER'], filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        return send_file(filepath, as_attachment=True, download_name=filename)
    
    elif format == 'excel':
        # 导出为Excel
        data = []
        for article in articles:
            data.append({
                "标题": article[0],
                "作者": article[1],
                "发布时间": article[2],
                "原文链接": article[4]
            })
        
        df = pd.DataFrame(data)
        filename = f"公众号文章_{datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx"
        filepath = os.path.join(app.config['DOWNLOAD_FOLDER'], filename)
        df.to_excel(filepath, index=False)
        
        return send_file(filepath, as_attachment=True, download_name=filename)
    
    else:
        return "不支持的导出格式", 400

# 初始化数据库
init_db()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
