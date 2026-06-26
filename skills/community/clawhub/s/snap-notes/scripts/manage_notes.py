import os
import json
import argparse
import requests
from datetime import datetime
from pathlib import Path

# 路径配置
home = Path.home()
BASE_DIR = home / ".openclaw" / "workspace" / "memory" / "snapnotes"
BASE_DIR.mkdir(parents=True, exist_ok=True)
CONFIG_PATH = BASE_DIR / "config.json"

def load_config():
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH, "r") as f:
                return json.load(f)
        except: return None
    return None

def call_ai(prompt, config):
    if not config or not config.get("api_key"): return None
    headers = {"Authorization": f"Bearer {config['api_key']}", "Content-Type": "application/json"}
    payload = {
        "model": config.get("model", "google/gemini-3.1-pro-preview"),
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1
    }
    try:
        response = requests.post(f"{config['api_base'].rstrip('/')}/chat/completions", headers=headers, json=payload, timeout=60)
        return response.json()['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"⚠️ AI error: {e}")
        return None

def add_note_with_ai(content):
    config = load_config()
    db_path = BASE_DIR / f"notes_{datetime.now().strftime('%Y-%m')}.jsonl"
    
    metadata = {"tags": [], "entities": {}, "quality_score": 100, "suggestions": ""}
    
    if config:
        print("🤖 AI is analyzing the context for quality & entities...")
        prompt = f"""
分析以下销售/采购碎片化笔记内容："{content}"
1. 提取实体（Customer, Supplier, Product, Price, OrderNo 等），以 JSON 格式返回。
2. 如果是商务报价或需求记录，检查是否缺失关键环节（如：交期、税率、规格、支付方式）。
3. 如果有缺失，在 "suggestions" 中给出简短提醒。
4. 返回格式：{{"entities": {{...}}, "suggestions": "...", "tags": ["..."]}}
只返回 JSON。
"""
        res = call_ai(prompt, config)
        if res:
            try:
                # 过滤可能的 markdown 格式
                clean_res = res.replace("```json", "").replace("```", "").strip()
                ai_data = json.loads(clean_res)
                metadata.update(ai_data)
            except: pass

    entry = {
        "timestamp": datetime.now().isoformat(),
        "content": content,
        "metadata": metadata
    }
    
    with open(db_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    
    print(f"✅ Note snapped!")
    if metadata.get("suggestions"):
        print(f"💡 业务提醒: {metadata['suggestions']}")
    if metadata.get("entities"):
        print(f"🏷️ 识别到实体: {metadata['entities']}")

def analyze_notes():
    config = load_config()
    if not config:
        print("❌ Please configure AI to use analysis feature.")
        return

    all_content = []
    # 读取最近 30 天内的数据
    for file in sorted(BASE_DIR.glob("*.jsonl"), reverse=True)[:2]:
        with open(file, "r", encoding="utf-8") as f:
            for line in f:
                note = json.loads(line)
                all_content.append(f"{note['timestamp'][:10]}: {note['content']}")
    
    if not all_content:
        print("📭 No data to analyze.")
        return

    print("📊 Generating Business Focus Insights...")
    prompt = f"""
分析以下一段时间内的销售和采购记录，生成一份量化的业务洞察报告。
要求包含：
1. 提及频率最高的客户/供应商排名前三。
2. 本期关注的所有核心产品/SKU。
3. 发现的潜在问题或工作重心偏向。
4. 建议改进的业务细节。

数据如下：
{chr(10).join(all_content)}
"""
    report = call_ai(prompt, config)
    if report:
        print("\n" + "="*40)
        print(report)
        print("="*40)

def search_notes(query):
    config = load_config()
    all_notes = []
    for file in sorted(BASE_DIR.glob("*.jsonl"), reverse=True):
        with open(file, "r", encoding="utf-8") as f:
            for line in f:
                note = json.loads(line)
                time_str = note["timestamp"].split("T")[0] + " " + note["timestamp"].split("T")[1][:5]
                all_notes.append(f"[{time_str}] {note['content']}")

    print(f"🔍 Searching for: {query}")
    prompt = f"从以下笔记中，找出与'{query}'最相关的3条。如果有关于客户、产品或单号的隐含含义，请优先匹配。直接返回笔记原文。如果没有相关，返回 NONE。\n" + "\n".join(all_notes)
    
    res = call_ai(prompt, config)
    if res and res != "NONE":
        print(f"✨ AI Findings:\n{res}")
    else:
        # Fallback keyword search
        q_words = query.lower().split()
        matches = [n for n in all_notes if all(w in n.lower() for w in q_words)]
        if matches: print(f"🔍 Matches:\n" + "\n".join(matches))
        else: print("❌ Not found.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("add").add_argument("content")
    subparsers.add_parser("search").add_argument("query")
    subparsers.add_parser("list")
    subparsers.add_parser("analyze") # 新增分析功能
    args = parser.parse_args()

    if args.command == "add": add_note_with_ai(args.content)
    elif args.command == "search": search_notes(args.query)
    elif args.command == "analyze": analyze_notes()
    elif args.command == "list": 
        # 简单兼容之前的 list
        for file in sorted(BASE_DIR.glob("*.jsonl"), reverse=True):
            with open(file, "r", encoding="utf-8") as f:
                for line in f: print(line.strip())
