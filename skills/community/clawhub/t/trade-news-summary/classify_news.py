#!/usr/bin/env python3
import re
import requests

import os
WEBHOOK_URL = os.environ.get("FEISHU_WEBHOOK", "")
import os
NEWS_FILE = os.path.expanduser("~/trade-news.md")


CATEGORIES = {
    "帽子": ["hat", "cap", "beanie", "fedora", "beret", "sun hat", "hard hat", "gat", "headwear", "millinery", "snapback", "dad hat", "bucket hat", "visor", "cloche", "newsboy", "panama", "trilby", "cowboy", "outdoor hat"],
    
    "面料": ["fabric", "textile", "cloth", "material", "fibre", "yarn", "weave", "recycling", "spinning", "cotton", "polyester", "nylon", "wool", "linen", "hemp", "silk", "leather", "denim", "knit", "woven", "nonwoven", "technical fabric", "performance fabric", "breathable", "waterproof", "eco-friendly", "organic", "recycled", "sustainable"],
    
    "运动服饰": ["sportswear", "activewear", "athleisure", "gym", "yoga", "running", "training", "sports", "athletic", "fitness", "workout", "sports bra", "leggings", "joggers", "hoodie", "sweatshirt", "track", "jersey", "uniform", "team wear", "nike", "adidas", "under armour", "lululemon", "puma", "reebok", "new balance", "asics", "columbia", "the north face", "patagonia"],
    
    "运费": ["shipping", "freight", "logistics", "container", "port", "vessel", "cargo", "delivery", "supply chain", "transport", "haulage", "courier", "last mile", "fulfillment", "warehouse", "inventory", "stock", "distribution"],
    
    "关税": ["tariff", "duty", "tax", "customs", "levy", "surcharge", "electricity prices", "energy costs", "trade war", "trade barrier", "import", "export", "quota", "anti-dumping", "countervailing", "section 301", "trade agreement", "free trade", "fta", "gsp", "preferential", "rules of origin"],
    
    "电商": ["amazon", "ebay", "ecommerce", "e-commerce", "retail", "taobao", "shopify", "online", "marketplace", "d2c", "direct to consumer", "omni-channel", "cross-border", "aliexpress", "wish", "etsy", "walmart", "target", "costco", "shein", "temu", "tiktok shop", "instagram shop", "facebook marketplace"],
    
    "汇率": ["currency", "exchange", "forex", "yuan", "dollar", "euro", "yen", "rupee", "pound", "won", "real", "peso", "ringgit", "baht", "dong", "rupiah", "forex rate", "exchange rate", "appreciation", "depreciation", "devaluation", "revaluation", "currency war"],
    
    "国际关系": ["trade war", "trade dispute", "sanctions", "embargo", "tariff war", "diplomatic", "geopolitical", "bilateral", "multilateral", "wto", "imf", "world bank", "g20", "apec", "asean", "eu", "usmca", "cptpp", "rcep", "brexit", "china-us", "india-us", "europe", "middle east", "iran", "hormuz", "suez", "panama canal"],
    
    "合规": ["compliance", "regulation", "law", "act", "bill", "standard", "certification", "audit", "inspection", "testing", "safety", "environmental", "social", "labor", "human rights", "forced labor", "child labor", "modern slavery", "conflict mineral", "reach", "rohs", "cpsc", "astm", "iso", "oeko tex", "grs", "bc", "fair trade", "ethical", "sustainable"],
    
    "行业动态": ["brand", "launch", "release", "announce", "partnership", "acquisition", "merger", "investment", "funding", "ipo", "earnings", "revenue", "profit", "market share", "trend", "forecast", "outlook", "analysis", "report", "survey", "study", "research"]
}

def classify(title):
    for cat, kw in CATEGORIES.items():
        if any(k in title.lower() for k in kw):
            return cat
    return "其他"

try:
    with open(NEWS_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
except FileNotFoundError:
    print("新闻文件不存在，请先运行 daily-news.sh")
    exit(1)

pattern = r'\*\*(\d+)\.\s*\[(.+?)\]\((.+?)\)\*\*.*?-\s*中文:\s*(.+?)(?:\n|$)'
matches = re.findall(pattern, content, re.DOTALL)

if not matches:
    print("未找到新闻，请检查文件格式")
    exit(1)

rows = []
for match in matches:
    num, title_en, link, title_zh = match
    cat = classify(title_en)
    summary = title_zh[:20] + ("..." if len(title_zh) > 20 else "")
    rows.append(f"| {cat} | [{title_en[:40]}]({link}) | {summary} |")

table = "| 类别 | 标题 | 摘要 |\n|------|------|------|\n" + "\n".join(rows)
card = {
    "msg_type": "interactive",
    "card": {
        "config": {"wide_screen_mode": True},
        "header": {"title": {"tag": "plain_text", "content": "📊 外贸资讯分析报告"}, "template": "blue"},
        "elements": [{"tag": "div", "text": {"tag": "lark_md", "content": table}}]
    }
}

# 打印发送的 JSON 用于调试
print("发送的 JSON:", card)

resp = requests.post(WEBHOOK_URL, json=card)
print(f"✅ 分析报告已推送，状态码: {resp.status_code}")
print("响应内容:", resp.text)
