#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
场景库增量合并脚本 - 逐个文件处理并追加到现有场景库

使用方式：
    python3 incremental_merge.py [文件名]
    
    不传参数：处理所有新文件
    传文件名：只处理指定文件
"""

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


# ==================== 配置 ====================

DOWNLOADS_DIR = Path.home() / "Downloads"
OUTPUT_DIR = Path(__file__).parent.parent / "data"
MODEL_NAME = 'shibing624/text2vec-base-chinese'

# 已处理的文件（避免重复）
PROCESSED_FILES = [
    # 上午已处理的文件，如果有请添加
]

# 需要排除的文件
EXCLUDE_FILES = [
    '出境游专项 3719-已上传 AI studio (1).xlsx',
] + PROCESSED_FILES


# ==================== 情绪标签 ====================

EMOTION_CATEGORIES = {
    '愤怒': ['愤怒', '生气', '恼火', '不满', '气愤', '怒火'],
    '焦虑': ['焦虑', '着急', '紧张', '担忧', '不安', '恐慌', '紧迫'],
    '失望': ['失望', '沮丧', '失落', '灰心', '无奈', '遗憾'],
    '困惑': ['困惑', '迷茫', '不解', '疑惑', '糊涂'],
    '满意': ['满意', '开心', '高兴', '愉快', '舒适'],
    '惊喜': ['惊喜', '意外', '赞叹', '惊艳'],
    '感激': ['感激', '感谢', '感动', '欣慰'],
    '疲惫': ['疲惫', '累', '辛苦', '疲倦'],
    '期待': ['期待', '盼望', '希望', '憧憬'],
    '中性': ['中性', '平静', '客观']
}


# ==================== 姓名映射 ====================

LAST_NAME_MAP = {
    '廖': 'Johnson', '沈': 'Smith', '张': 'Williams', '王': 'Brown', '李': 'Jones',
    '刘': 'Garcia', '陈': 'Miller', '杨': 'Davis', '赵': 'Rodriguez', '黄': 'Martinez',
    '周': 'Hernandez', '吴': 'Lopez', '徐': 'Gonzalez', '孙': 'Wilson', '胡': 'Anderson',
    '朱': 'Thomas', '马': 'Moore', '高': 'Jackson', '林': 'Martin', '何': 'Lee',
    '郭': 'Perez', '罗': 'Thompson', '郑': 'White', '梁': 'Harris', '谢': 'Sanchez',
    '宋': 'Clark', '唐': 'Ramirez', '许': 'Lewis', '韩': 'Robinson', '冯': 'Walker',
    '邓': 'Young', '曹': 'Allen', '彭': 'King', '曾': 'Wright', '萧': 'Scott',
    '田': 'Torres', '董': 'Nguyen', '袁': 'Hill', '潘': 'Flores', '蔡': 'Green',
    '蒋': 'Adams', '余': 'Nelson', '杜': 'Baker', '叶': 'Hall', '程': 'Rivera',
    '魏': 'Campbell', '吕': 'Mitchell', '丁': 'Carter', '任': 'Roberts',
}

FIRST_NAMES = [
    'James', 'Mary', 'John', 'Patricia', 'Robert', 'Jennifer', 'Michael', 'Linda',
    'William', 'Elizabeth', 'David', 'Barbara', 'Richard', 'Susan', 'Joseph', 'Jessica',
    'Thomas', 'Sarah', 'Charles', 'Karen', 'Christopher', 'Nancy', 'Daniel', 'Lisa',
]


# ==================== 工具函数 ====================

def safe_str(value):
    if pd.isna(value):
        return ''
    return str(value)


def anonymize_name(chinese_name, name_cache):
    if not chinese_name or chinese_name.strip() == '':
        return ''
    if chinese_name in name_cache:
        return name_cache[chinese_name]
    
    last_name = chinese_name[0] if chinese_name else None
    en_last = LAST_NAME_MAP.get(last_name, 'Smith') if last_name else 'Smith'
    en_first = random.choice(FIRST_NAMES)
    en_name = f"{en_first} {en_last}"
    
    name_cache[chinese_name] = en_name
    return en_name


def sanitize_text(text):
    if not text:
        return ''
    
    sensitive_words = {
        '飞猪': '旅行平台', '阿里': '旅行平台', '阿里巴巴': '旅行平台',
        '淘宝': '旅行平台', '千问': '旅行平台', '天猫': '旅行平台',
        '支付宝': '支付平台', '高德': '地图平台', '饿了么': '外卖平台',
    }
    
    result = text
    for sensitive, replacement in sensitive_words.items():
        result = result.replace(sensitive, replacement)
    return result


def extract_emotion_label(scenario):
    text_parts = []
    for field in ['痛点', '爽点', '用户具体场景', '任务', '底层需求']:
        value = scenario.get(field)
        if value:
            text_parts.append(safe_str(value))
    
    full_text = ' '.join(text_parts)
    
    for emotion, keywords in EMOTION_CATEGORIES.items():
        for keyword in keywords:
            if keyword in full_text:
                return emotion
    return '中性'


def generate_record_hash(scenario):
    key_fields = ['用户姓名和背景信息', '用户具体场景', '任务', '痛点', '底层需求']
    hash_content = '|'.join([safe_str(scenario.get(field, '')) for field in key_fields])
    return hashlib.md5(hash_content.encode('utf-8')).hexdigest()


def load_existing_library():
    """读取现有场景库"""
    data_file = OUTPUT_DIR / "scenario_library.json.enc"
    print(f"📂 读取现有场景库：{data_file}")
    
    manager = EncryptManager()
    with open(data_file, 'r', encoding='utf-8') as f:
        encrypted_data = f.read()
    
    decrypted = manager.decrypt_data(encrypted_data)
    scenarios = json.loads(decrypted)
    
    print(f"✅ 现有场景库：{len(scenarios):,} 条记录")
    return scenarios, manager


def process_file(file_path, name_cache, existing_hashes):
    """处理单个文件，返回新增的场景"""
    print(f"\n📄 处理文件：{file_path.name}")
    
    try:
        xl_file = pd.ExcelFile(file_path)
        sheet_name = xl_file.sheet_names[0]
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        scenarios = df.to_dict('records')
        
        new_scenarios = []
        duplicate_count = 0
        
        for scenario in scenarios:
            # 标准化字段
            processed = {
                '序号': safe_str(scenario.get('序号', '')),
                '用户姓名和背景信息': safe_str(scenario.get('用户姓名和背景信息', '')),
                '内容范围': safe_str(scenario.get('内容范围', '')),
                '是否出境游': safe_str(scenario.get('是否出境游', '')),
                '用户具体场景': safe_str(scenario.get('用户具体场景', '')),
                '任务': safe_str(scenario.get('任务', '')),
                '期待效果': safe_str(scenario.get('期待效果', '')),
                '当前方案': safe_str(scenario.get('当前方案', '')),
                '爽点': safe_str(scenario.get('爽点', '')),
                '痛点': safe_str(scenario.get('痛点', '')),
                '改进方向': safe_str(scenario.get('改进方向', '')),
                '底层需求': safe_str(scenario.get('底层需求', '')),
                '场景总分': safe_str(scenario.get('场景总分', '')),
                '质量分明细': safe_str(scenario.get('质量分明细', '')),
            }
            
            # 脱敏：公司名
            for field in ['用户姓名和背景信息', '用户具体场景', '任务', '当前方案', '改进方向']:
                if processed.get(field):
                    processed[field] = sanitize_text(processed[field])
            
            # 脱敏：姓名
            if processed.get('用户姓名和背景信息'):
                name_match = re.search(r'姓名\[([^\]]+)\]', processed['用户姓名和背景信息'])
                if name_match:
                    chinese_name = name_match.group(1)
                    en_name = anonymize_name(chinese_name, name_cache)
                    processed['用户姓名和背景信息'] = processed['用户姓名和背景信息'].replace(
                        f'姓名[{chinese_name}]', f'姓名[{en_name}]'
                    )
            
            # 情绪标签
            processed['情绪标签'] = extract_emotion_label(scenario)
            
            # 去重检查
            record_hash = generate_record_hash(processed)
            if record_hash in existing_hashes:
                duplicate_count += 1
                continue
            
            existing_hashes.add(record_hash)
            new_scenarios.append(processed)
        
        print(f"   ✅ 读取 {len(scenarios)} 条，新增 {len(new_scenarios)} 条，重复 {duplicate_count} 条")
        return new_scenarios
        
    except Exception as e:
        print(f"   ❌ 处理失败：{e}")
        return []


def compute_new_embeddings(new_scenarios, model):
    """计算新增场景的向量"""
    if not new_scenarios:
        return None
    
    texts = []
    for scenario in new_scenarios:
        text_parts = []
        if scenario.get('用户具体场景'):
            text_parts.append(f"场景：{scenario['用户具体场景']}")
        if scenario.get('任务'):
            text_parts.append(f"任务：{scenario['任务']}")
        if scenario.get('痛点'):
            text_parts.append(f"痛点：{scenario['痛点']}")
        if scenario.get('底层需求'):
            text_parts.append(f"需求：{scenario['底层需求']}")
        texts.append(" | ".join(text_parts))
    
    embeddings = model.encode(texts, show_progress_bar=True, batch_size=32)
    return embeddings


def save_updated_library(all_scenarios, manager):
    """保存更新后的场景库"""
    print("\n🔒 保存加密场景库...")
    
    json_data = json.dumps(all_scenarios, ensure_ascii=False, indent=2)
    encrypted = manager.encrypt_data(json_data.encode('utf-8'))
    
    output_file = OUTPUT_DIR / "scenario_library.json.enc"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(encrypted)
    
    print(f"✅ 已保存：{output_file} ({len(all_scenarios):,} 条)")


def main():
    print("\n" + "=" * 60)
    print("🚀 场景库增量合并脚本")
    print("=" * 60)
    print(f"开始时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 1. 读取现有场景库
    existing_scenarios, manager = load_existing_library()
    existing_hashes = set(generate_record_hash(s) for s in existing_scenarios)
    
    # 2. 加载向量化模型
    print(f"\n🤖 加载向量化模型：{MODEL_NAME}")
    model = SentenceTransformer(MODEL_NAME)
    
    # 3. 获取所有 Excel 文件
    excel_files = [f for f in DOWNLOADS_DIR.iterdir() 
                   if f.suffix == '.xlsx' and not f.name.startswith('.')]
    excel_files = [f for f in excel_files if f.name not in EXCLUDE_FILES]
    
    # 如果指定了文件名，只处理该文件
    if len(sys.argv) > 1:
        target_name = sys.argv[1]
        excel_files = [f for f in excel_files if target_name in f.name]
        print(f"🎯 只处理包含 '{target_name}' 的文件：{len(excel_files)} 个")
    
    print(f"\n📁 待处理文件：{len(excel_files)} 个")
    
    # 4. 逐个处理文件
    name_cache = {}
    all_new_scenarios = []
    
    for i, file_path in enumerate(sorted(excel_files), 1):
        print(f"\n[{i}/{len(excel_files)}]", end='')
        new_scenarios = process_file(file_path, name_cache, existing_hashes)
        all_new_scenarios.extend(new_scenarios)
    
    # 5. 合并所有场景
    print("\n\n" + "=" * 60)
    print("📊 合并统计")
    print("=" * 60)
    print(f"原有场景：{len(existing_scenarios):,} 条")
    print(f"新增场景：{len(all_new_scenarios):,} 条")
    print(f"合并后：{len(existing_scenarios) + len(all_new_scenarios):,} 条")
    
    # 6. 保存更新后的场景库
    all_scenarios = existing_scenarios + all_new_scenarios
    save_updated_library(all_scenarios, manager)
    
    # 7. 计算并保存所有向量（合并后重新计算）
    print("\n📐 重新计算所有场景的向量...")
    texts = []
    for scenario in all_scenarios:
        text_parts = []
        if scenario.get('用户具体场景'):
            text_parts.append(f"场景：{scenario['用户具体场景']}")
        if scenario.get('任务'):
            text_parts.append(f"任务：{scenario['任务']}")
        if scenario.get('痛点'):
            text_parts.append(f"痛点：{scenario['痛点']}")
        if scenario.get('底层需求'):
            text_parts.append(f"需求：{scenario['底层需求']}")
        texts.append(" | ".join(text_parts))
    
    embeddings = model.encode(texts, show_progress_bar=True, batch_size=32)
    
    embeddings_file = OUTPUT_DIR / "scenario_embeddings.npy"
    np.save(str(embeddings_file), embeddings)
    print(f"✅ 已保存向量：{embeddings_file} ({embeddings.shape})")
    
    # 8. 统计情绪标签
    emotion_stats = {}
    for scenario in all_scenarios:
        emotion = scenario.get('情绪标签', '中性')
        emotion_stats[emotion] = emotion_stats.get(emotion, 0) + 1
    
    print("\n😊 情绪标签分布：")
    for emotion in sorted(emotion_stats.keys(), key=lambda x: emotion_stats[x], reverse=True):
        count = emotion_stats[emotion]
        ratio = count / len(all_scenarios) * 100
        print(f"  {emotion}: {count:,} ({ratio:.2f}%)")
    
    print("\n" + "=" * 60)
    print("✅ 增量合并完成！")
    print("=" * 60)
    print(f"结束时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    random.seed(42)
    main()
