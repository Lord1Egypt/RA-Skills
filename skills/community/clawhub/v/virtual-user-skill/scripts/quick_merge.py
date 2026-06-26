#!/usr/bin/env python3
"""快速清理字段并重新计算向量"""

import sys
import json
import random
import hashlib
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
from sentence_transformers import SentenceTransformer
import re

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from encrypt import EncryptManager

DOWNLOADS_DIR = Path.home() / "Downloads"
OUTPUT_DIR = Path(__file__).parent.parent / "data"
MODEL_NAME = 'shibing624/text2vec-base-chinese'
EXCLUDE_FILES = ['出境游专项 3719-已上传 AI studio (1).xlsx']

EMOTION_CATEGORIES = {
    '愤怒': ['愤怒', '生气', '恼火', '不满'],
    '焦虑': ['焦虑', '着急', '紧张', '担忧', '紧迫'],
    '失望': ['失望', '沮丧', '失落', '无奈'],
    '困惑': ['困惑', '迷茫', '不解', '疑惑'],
    '满意': ['满意', '开心', '高兴', '愉快'],
    '惊喜': ['惊喜', '意外', '赞叹'],
    '感激': ['感激', '感谢', '感动'],
    '疲惫': ['疲惫', '累', '辛苦'],
    '期待': ['期待', '盼望', '希望'],
    '中性': ['中性', '平静']
}

LAST_NAME_MAP = {'廖': 'Johnson', '沈': 'Smith', '张': 'Williams', '王': 'Brown', '李': 'Jones',
    '刘': 'Garcia', '陈': 'Miller', '杨': 'Davis', '赵': 'Rodriguez', '黄': 'Martinez',
    '周': 'Hernandez', '吴': 'Lopez', '徐': 'Gonzalez', '孙': 'Wilson', '胡': 'Anderson',
    '朱': 'Thomas', '马': 'Moore', '高': 'Jackson', '林': 'Martin', '何': 'Lee'}

FIRST_NAMES = ['James', 'Mary', 'John', 'Patricia', 'Robert', 'Jennifer', 'Michael', 'Linda',
    'William', 'Elizabeth', 'David', 'Barbara', 'Richard', 'Susan', 'Joseph', 'Jessica']

def safe_str(v): return '' if pd.isna(v) else str(v)

def anonymize_name(name, cache):
    if not name or name in cache: return cache.get(name, '')
    last = name[0] if name else None
    en = f"{random.choice(FIRST_NAMES)} {LAST_NAME_MAP.get(last, 'Smith')}"
    cache[name] = en
    return en

def sanitize_text(text):
    if not text: return ''
    for k, v in {'飞猪': '旅行平台', '阿里': '旅行平台', '淘宝': '旅行平台', '千问': '旅行平台'}.items():
        text = text.replace(k, v)
    return text

def extract_emotion(scenario):
    text = ' '.join([safe_str(scenario.get(f, '')) for f in ['痛点', '爽点', '用户具体场景', '任务', '底层需求']])
    for emotion, keywords in EMOTION_CATEGORIES.items():
        if any(k in text for k in keywords): return emotion
    return '中性'

def gen_hash(s):
    return hashlib.md5('|'.join([safe_str(s.get(f, '')) for f in ['用户姓名和背景信息', '用户具体场景', '任务', '痛点', '底层需求']]).encode()).hexdigest()

def load_existing():
    manager = EncryptManager()
    with open(OUTPUT_DIR / "scenario_library.json.enc", 'r') as f:
        return json.loads(manager.decrypt_data(f.read()))

def process_file(path, cache, hashes):
    try:
        df = pd.read_excel(path, sheet_name=pd.ExcelFile(path).sheet_names[0])
        new, dup = [], 0
        for row in df.to_dict('records'):
            s = {k: safe_str(row.get(k, '')) for k in ['序号', '用户姓名和背景信息', '内容范围', '是否出境游',
                '用户具体场景', '任务', '期待效果', '当前方案', '爽点', '痛点', '改进方向', '底层需求']}
            for f in ['用户姓名和背景信息', '用户具体场景', '任务', '当前方案', '改进方向']:
                s[f] = sanitize_text(s[f])
            if s.get('用户姓名和背景信息'):
                m = re.search(r'姓名\[([^\]]+)\]', s['用户姓名和背景信息'])
                if m: s['用户姓名和背景信息'] = s['用户姓名和背景信息'].replace(f'姓名[{m.group(1)}]', f'姓名[{anonymize_name(m.group(1), cache)}]')
            s['情绪标签'] = extract_emotion(row)
            h = gen_hash(s)
            if h not in hashes:
                hashes.add(h)
                new.append(s)
            else: dup += 1
        print(f"  {path.name[:50]:<50} {len(df):>5}条 → 新增{len(new):>5}条，重复{dup:>5}条")
        return new
    except Exception as e:
        print(f"  ❌ {path.name}: {e}")
        return []

def main():
    print("\n🚀 场景库合并 + 字段清理")
    print("=" * 60)
    
    # 1. 读取现有
    print("\n📂 读取现有场景库...")
    existing = load_existing()
    existing_hashes = set(gen_hash(s) for s in existing)
    print(f"   现有：{len(existing):,} 条")
    
    # 2. 加载模型
    print(f"\n🤖 加载模型：{MODEL_NAME}")
    model = SentenceTransformer(MODEL_NAME)
    
    # 3. 处理新文件
    print("\n📁 处理新文件...")
    files = [f for f in DOWNLOADS_DIR.iterdir() if f.suffix == '.xlsx' and f.name not in EXCLUDE_FILES and not f.name.startswith('.')]
    print(f"   文件数：{len(files)}")
    
    name_cache = {}
    all_new = []
    for i, f in enumerate(sorted(files), 1):
        print(f"[{i}/{len(files)}]", end='')
        all_new.extend(process_file(f, name_cache, existing_hashes))
    
    # 4. 合并
    all_scenarios = existing + all_new
    print(f"\n\n📊 合并结果:")
    print(f"   原有：{len(existing):,} 条")
    print(f"   新增：{len(all_new):,} 条")
    print(f"   总计：{len(all_scenarios):,} 条")
    
    # 5. 保存
    print("\n🔒 保存场景库...")
    manager = EncryptManager()
    json_data = json.dumps(all_scenarios, ensure_ascii=False, indent=2)
    with open(OUTPUT_DIR / "scenario_library.json.enc", 'w') as f:
        f.write(manager.encrypt_data(json_data.encode('utf-8')))
    print(f"   ✅ {OUTPUT_DIR / 'scenario_library.json.enc'}")
    
    # 6. 计算向量
    print("\n📐 计算向量...")
    texts = [" | ".join([f"{k}: {s.get(k, '')}" for k in ['用户具体场景', '任务', '痛点', '底层需求'] if s.get(k)]) for s in all_scenarios]
    embeddings = model.encode(texts, show_progress_bar=True, batch_size=32)
    np.save(OUTPUT_DIR / "scenario_embeddings.npy", embeddings)
    print(f"   ✅ 向量形状：{embeddings.shape}")
    
    # 7. 统计
    emotion_stats = {}
    for s in all_scenarios:
        e = s.get('情绪标签', '中性')
        emotion_stats[e] = emotion_stats.get(e, 0) + 1
    
    print("\n😊 情绪标签：")
    for e in sorted(emotion_stats.keys(), key=lambda x: emotion_stats[x], reverse=True):
        print(f"   {e}: {emotion_stats[e]:,} ({emotion_stats[e]/len(all_scenarios)*100:.1f}%)")
    
    print("\n✅ 完成!")
    print(f"字段：{list(all_scenarios[0].keys())}")

if __name__ == "__main__":
    random.seed(42)
    main()
