#!/usr/bin/env python3
"""创建思考火花记录"""

import json
import sys
import os
from datetime import datetime

DATA_FILE = os.path.expanduser("~/.openclaw/workspace/collection/思考火花.json")

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {"schema_version": "1.0", "description": "思考火花与沉淀记录", "sparks": []}

def save_data(data):
    # 原子写入：临时文件 + rename
    tmp_file = DATA_FILE + ".tmp"
    with open(tmp_file, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp_file, DATA_FILE)

def generate_id():
    today = datetime.now().strftime("%Y%m%d")
    data = load_data()
    existing = [s["id"] for s in data["sparks"] if s["id"].startswith(today)]
    num = len(existing) + 1
    return f"{today}_{num:03d}"

def create_spark(content, tags=None, origin="spark", status="raw"):
    data = load_data()
    now = datetime.now().isoformat() + "Z"
    
    spark = {
        "id": generate_id(),
        "content": content,
        "polished_content": None,
        "tags": tags or [],
        "origin": origin,
        "status": status,
        "priority": 3,
        "confidence": 0.5,
        "source_refs": [],
        "created_at": now,
        "updated_at": now,
        "refined_at": None,
        "history": [{"action": "created", "timestamp": now}]
    }
    
    data["sparks"].append(spark)
    save_data(data)
    return spark["id"]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python create_spark.py <content> [tag1,tag2]")
        sys.exit(1)
    
    content = sys.argv[1]
    tags = sys.argv[2].split(",") if len(sys.argv) > 2 else []
    
    spark_id = create_spark(content, [t.strip() for t in tags if t.strip()])
    print(f"✅ Created spark: {spark_id}")
