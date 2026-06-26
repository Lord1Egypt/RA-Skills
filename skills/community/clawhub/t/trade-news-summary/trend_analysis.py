#!/usr/bin/env python3
import re
import json
import requests
from collections import Counter
from datetime import datetime, timedelta
import os
WEBHOOK_URL = os.environ.get("FEISHU_WEBHOOK", "")
if not WEBHOOK_URL:
    print("错误：请设置环境变量 FEISHU_WEBHOOK")
    exit(1)


NEWS_FILE = os.path.expanduser("~/trade-news.md")
HISTORY_DIR = os.path.expanduser("~/.openclaw/workspace/history")


os.makedirs(HISTORY_DIR, exist_ok=True)

CATEGORIES = {
    "帽子": ["hat", "cap", "beanie", "fedora", "beret", "sun hat", "hard hat", "gat", "headwear", "millinery"],
    "面料": ["fabric", "textile", "cloth", "material", "fibre", "yarn", "weave", "recycling", "spinning", "cotton", "polyester", "nylon", "wool", "linen"],
    "运动服饰": ["sportswear", "activewear", "athleisure", "gym", "yoga", "running", "training", "sports", "athletic", "fitness", "nike", "adidas", "under armour", "lululemon"],
    "运费": ["shipping", "freight", "logistics", "container", "port", "vessel", "cargo", "delivery", "supply chain", "warehouse"],
    "关税": ["tariff", "duty", "tax", "customs", "levy", "surcharge", "electricity prices", "energy costs", "trade war", "import", "export"],
    "电商": ["amazon", "ebay", "ecommerce", "e-commerce", "retail", "taobao", "shopify", "online", "marketplace", "shein", "temu"],
    "汇率": ["currency", "exchange", "forex", "yuan", "dollar", "euro", "yen", "rupee", "exchange rate"],
    "国际关系": ["trade war", "sanctions", "embargo", "geopolitical", "wto", "eu", "brexit", "middle east", "iran", "hormuz"],
    "合规": ["compliance", "regulation", "law", "standard", "certification", "safety", "environmental", "labor", "forced labor", "reach", "rohs"],
    "行业动态": ["brand", "launch", "release", "announce", "partnership", "acquisition", "investment", "funding", "earnings", "trend", "forecast"]
}

def classify(title):
    for cat, kw in CATEGORIES.items():
        if any(k in title.lower() for k in kw):
            return cat
    return "其他"

def get_today_news():
    try:
        with open(NEWS_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        return []
    pattern = r'\*\*(\d+)\.\s*(.+?)\*\*'
    matches = re.findall(pattern, content, re.DOTALL)
    categories = []
    for match in matches:
        title_en = match[1]
        cat = classify(title_en)
        categories.append(cat)
    return categories

def save_history(categories):
    today = datetime.now().strftime("%Y-%m-%d")
    history_file = os.path.join(HISTORY_DIR, f"{today}.json")
    with open(history_file, 'w', encoding='utf-8') as f:
        json.dump(categories, f)

def load_week_history():
    week_ago = datetime.now() - timedelta(days=7)
    all_cats = []
    for fname in os.listdir(HISTORY_DIR):
        if fname.endswith('.json'):
            date_str = fname.replace('.json', '')
            try:
                date = datetime.strptime(date_str, "%Y-%m-%d")
                if date >= week_ago:
                    with open(os.path.join(HISTORY_DIR, fname), 'r') as f:
                        all_cats.extend(json.load(f))
            except:
                pass
    return all_cats

def send_trend_report(counter, total):
    rows = [f"| {cat} | {count} | {count/total*100:.1f}% |" for cat, count in counter.most_common(10)]
    table = "| 类别 | 新闻数量 | 占比 |\n|------|----------|------|\n" + "\n".join(rows)
    card = {
        "msg_type": "interactive",
        "card": {
            "config": {"wide_screen_mode": True},
            "header": {"title": {"tag": "plain_text", "content": "📈 外贸资讯周报（近7天）"}, "template": "green"},
            "elements": [{"tag": "div", "text": {"tag": "lark_md", "content": table}}]
        }
    }
    try:
        resp = requests.post(WEBHOOK_URL, json=card)
        print(f"趋势报告已推送，状态码: {resp.status_code}")
    except Exception as e:
        print(f"推送失败: {e}")

if __name__ == "__main__":
    today_cats = get_today_news()
    if today_cats:
        save_history(today_cats)
        print(f"已保存今日 {len(today_cats)} 条分类数据")
    
    week_cats = load_week_history()
    if week_cats:
        counter = Counter(week_cats)
        send_trend_report(counter, len(week_cats))
    else:
        print("暂无历史数据，请等待几天后再查看趋势")
