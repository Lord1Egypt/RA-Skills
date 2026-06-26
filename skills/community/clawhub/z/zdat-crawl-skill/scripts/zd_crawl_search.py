"""
ZDAT 情报抓取脚本 v1.0
支持按关键词类型搜索并归档
"""
import json, sys, os, yaml, hashlib, datetime
from pathlib import Path

WORKDIR = Path(os.getenv("WORKDIR", os.path.expanduser("~/.molili/workspaces/default")))
CONFIG_PATH = WORKDIR / "skill_config" / "zd_keyword.yaml"
SCHEDULE_PATH = WORKDIR / "skill_config" / "zd_crawl_schedule.yaml"

def load_keywords(key_type="all"):
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        kw = yaml.safe_load(f)
    mapping = {
        "core": "core_keywords",
        "industry": "industry_keywords",
        "intent": "intent_keywords",
        "risk": "risk_keywords",
    }
    if key_type == "all":
        all_kw = []
        for v in mapping.values():
            all_kw.extend(kw.get(v, []))
        return all_kw
    return kw.get(mapping.get(key_type, "core_keywords"), [])

def search_keyword(keyword):
    """模拟搜索（实际会调用 smart-search-reader / crawl4ai）"""
    print(f"  🔍 搜索: {keyword}")
    # TODO: 接入 smart-search-reader 或 crawl4ai
    return []

def classify_result(text, keywords):
    """简单分类"""
    for kw in keywords.get("risk_keywords", []):
        if kw in text:
            return "负面"
    for kw in keywords.get("intent_keywords", []):
        if kw in text:
            return "意向"
    for kw in keywords.get("industry_keywords", []):
        if kw in text:
            return "行业"
    return "普通"

def dedup_check(title, body, window_days=7):
    """标题+正文前50字符哈希去重"""
    text = (title or "") + (body or "")[:50]
    h = hashlib.md5(text.encode()).hexdigest()
    # TODO: 读取已抓取哈希库检查
    return True  # 临时返回不重复

def run(key_type="all"):
    keywords = load_keywords(key_type)
    print(f"\n📡 ZDAT 情报抓取 — {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"   关键词数: {len(keywords)}")
    print(f"   类型: {key_type}\n")
    for kw in keywords:
        search_keyword(kw)

if __name__ == "__main__":
    key_type = sys.argv[2] if len(sys.argv) > 2 else "all"
    run(key_type)
