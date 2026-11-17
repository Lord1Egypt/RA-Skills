#!/usr/bin/env python3
"""每日唐诗 - 从全唐诗数据集中随机选取一首，输出结构化JSON供AI撰写赏析"""
import json
import random
import os
from datetime import datetime

script_dir = os.path.dirname(os.path.abspath(__file__))
poems_file = os.path.join(script_dir, "..", "data", "tang-poems.json")
with open(poems_file, "r", encoding="utf-8") as f:
    poems = json.load(f)["poems"]

today = datetime.now().strftime("%Y-%m-%d")
seed = int(today.replace("-", ""))
rng = random.Random(seed)
poem = rng.choice(poems)

date_cn = datetime.now().strftime("%Y年%m月%d日")

result = {
    "date": date_cn,
    "title": poem["title"],
    "author": poem["author"],
    "dynasty": poem["dynasty"],
    "content": poem["content"],
    "author_info": poem["author_info"]
}

print(json.dumps(result, ensure_ascii=False, indent=2))
