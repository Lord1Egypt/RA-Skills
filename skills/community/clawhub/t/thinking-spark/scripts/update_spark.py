#!/usr/bin/env python3
"""更新/整理思考火花"""

import json
import sys
import os
from datetime import datetime

DATA_FILE = os.path.expanduser("~/.openclaw/workspace/collection/思考火花.json")

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {"sparks": []}

def save_data(data):
    tmp_file = DATA_FILE + ".tmp"
    with open(tmp_file, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp_file, DATA_FILE)

def update_spark(spark_id, action, value=None):
    data = load_data()
    sparks = data.get("sparks", [])
    
    for s in sparks:
        if s["id"] == spark_id:
            now = datetime.now().isoformat() + "Z"
            
            if action == "refine":
                s["polished_content"] = value
                s["status"] = "polished"
                s["refined_at"] = now
            elif action == "status":
                s["status"] = value
            elif action == "archive":
                s["status"] = "archived"
            elif action == "tag":
                tags = s.get("tags", [])
                if value and value not in tags:
                    tags.append(value)
                    s["tags"] = tags
            elif action == "ref":
                refs = s.get("source_refs", [])
                if value and value not in refs:
                    refs.append(value)
                    s["source_refs"] = refs
            
            s["updated_at"] = now
            s["history"].append({"action": action, "timestamp": now, "value": value})
            
            save_data(data)
            print(f"✅ Updated {spark_id}: {action}")
            return
    
    print(f"❌ Spark not found: {spark_id}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage:")
        print("  python update_spark.py <id> refine <polished_content>")
        print("  python update_spark.py <id> status <raw|refining|polished|archived>")
        print("  python update_spark.py <id> archive")
        print("  python update_spark.py <id> tag <tag>")
        print("  python update_spark.py <id> ref <article:xxx|project:xxx>")
        sys.exit(1)
    
    spark_id = sys.argv[1]
    action = sys.argv[2]
    value = sys.argv[3] if len(sys.argv) > 3 else None
    
    update_spark(spark_id, action, value)
