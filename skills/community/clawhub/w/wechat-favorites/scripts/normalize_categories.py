# -*- coding: utf-8 -*-
"""
分类标签标准化脚本 v1.2.0
将各种格式的分类值标准化为 8 个标准分类（英文 key）+ 二级标签 + 跨领域标签

用法：
    python normalize_categories.py [--input CSV] [--output CSV]
"""

import csv, argparse, os, re
from collections import Counter, defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_INPUT = os.path.join(SCRIPT_DIR, "..", "exported_favorites", "articles_final_llm.csv")
DEFAULT_OUTPUT = os.path.join(SCRIPT_DIR, "..", "exported_favorites", "articles_final_normalized.csv")

# 标准 8 分类
CATEGORY_MAP = {
    'biomed': '生物医药',
    'ai': 'AI科技',
    'invest': '投资金融',
    'science': '科学研究',
    'business': '商业财经',
    'lifestyle': '生活方式',
    'media': '媒体资讯',
    'politics': '政治国际',
    'tech': 'AI科技',  # tech 合并到 AI科技
}

# 中文标签 → 标准 key
CN_TO_KEY = {v: k for k, v in CATEGORY_MAP.items() if k != 'tech'}

# 标准二级分类 key（中文）
SUBCATEGORY_KEYS = {
    'biomed': ['临床', '神经', '创新药', '肿瘤', '抗体', '基因治疗', 'CAR-T', 'ADC', '靶点', 'mRNA', 'PD-1/PD-L1', '罕见病', 'GLP-1', '中药'],
    'ai': ['AI应用', '大模型/LLM', 'AI医疗', '芯片/算力', '机器人', 'Agent', 'AIGC', '多模态', 'RAG'],
    'invest': ['VC/PE', '二级市场', 'IPO/上市', '并购', '宏观', '估值'],
    'science': ['神经科学', '生物', '物理', '化学', '材料', '天文'],
    'business': ['宏观经济', '行业分析', '企业战略', '互联网', '监管政策'],
    'lifestyle': ['读书', '健康', '音乐', '影视', '旅行', '运动', '美食'],
    'media': [],
    'politics': [],
}

# 跨领域标签标准 key
CROSS_DOMAIN_KEYS = ['生物医药+投资', 'AI+医疗', 'AI+投资', '生物医药+AI', '科学+政策', '商业+政治']

# 二级标签别名映射（LLM 可能输出不同的写法）
SUBCATEGORY_ALIASES = {
    '大模型/LLM': ['大模型', 'LLM', 'LLM/GPT', 'LLM/大模型'],
    'AI应用': ['AI+应用', 'AI应用场景', 'AI落地'],
    'AI医疗': ['AI+医疗', 'AI制药', '数字医疗'],
    '芯片/算力': ['芯片', '算力', 'GPU', '半导体'],
    'VC/PE': ['VC', 'PE', '风险投资', '私募股权'],
    'IPO/上市': ['IPO', '上市'],
    '二级市场': ['股票', 'A股', '证券'],
    '宏观经济': ['宏观', '经济'],
    '企业战略': ['战略', '企业管理'],
    '行业分析': ['行业', '产业'],
    '监管政策': ['监管', '政策', '合规'],
    '神经科学': ['神经', '脑科学'],
    'PD-1/PD-L1': ['PD-1', 'PD-L1', '免疫检查点'],
}

# 跨领域标签别名
CROSS_DOMAIN_ALIASES = {
    '生物医药+投资': ['biomed+invest', '生物医药+金融', '医药投资'],
    'AI+医疗': ['ai+medical', 'AI+医药', '人工智能+医疗'],
    'AI+投资': ['ai+invest', 'AI+金融', '人工智能+投资'],
    '生物医药+AI': ['biomed+ai', '医药+AI', '医药AI'],
}


def normalize_category(raw):
    """将原始分类值标准化为 8 个标准分类之一"""
    if not raw or raw == 'other' or raw == '未分类':
        return 'other'

    if raw in CN_TO_KEY:
        return CN_TO_KEY[raw]
    if raw in CATEGORY_MAP:
        return 'ai' if raw == 'tech' else raw

    for sep in ['+', '|', ',', '，']:
        if sep in raw:
            parts = raw.split(sep)
            for p in parts:
                p = p.strip()
                if p in CN_TO_KEY:
                    return CN_TO_KEY[p]
                if p in CATEGORY_MAP:
                    return 'ai' if p == 'tech' else p
            return 'other'

    return 'other'


def normalize_subcategory(raw, primary_cat):
    """标准化二级分类标签"""
    if not raw or not primary_cat:
        return ''

    valid_keys = SUBCATEGORY_KEYS.get(primary_cat, [])
    if not valid_keys:
        return ''

    # 构建别名反查表
    alias_to_key = {}
    for key in valid_keys:
        alias_to_key[key] = key
        for alias in SUBCATEGORY_ALIASES.get(key, []):
            alias_to_key[alias.lower()] = key
            alias_to_key[alias] = key

    parts = re.split(r'[|+,，]', raw)
    normalized = []
    for p in parts:
        p = p.strip()
        if p in alias_to_key:
            normalized.append(alias_to_key[p])
        elif p.lower() in alias_to_key:
            normalized.append(alias_to_key[p.lower()])
        # 模糊匹配：检查是否是某个 key 的子串
        else:
            for key in valid_keys:
                if p in key or key in p:
                    normalized.append(key)
                    break

    # 去重
    seen = set()
    result = []
    for n in normalized:
        if n not in seen:
            seen.add(n)
            result.append(n)

    return '|'.join(result)


def normalize_cross_domain(raw):
    """标准化跨领域标签"""
    if not raw:
        return ''

    # 构建别名反查表
    alias_to_key = {}
    for key in CROSS_DOMAIN_KEYS:
        alias_to_key[key] = key
        alias_to_key[key.lower()] = key
        for alias in CROSS_DOMAIN_ALIASES.get(key, []):
            alias_to_key[alias] = key
            alias_to_key[alias.lower()] = key

    parts = re.split(r'[|+,，]', raw)
    normalized = []
    for p in parts:
        p = p.strip()
        if p in alias_to_key:
            normalized.append(alias_to_key[p])
        elif p.lower() in alias_to_key:
            normalized.append(alias_to_key[p.lower()])

    seen = set()
    result = []
    for n in normalized:
        if n not in seen:
            seen.add(n)
            result.append(n)

    return '|'.join(result)


def parse_args():
    parser = argparse.ArgumentParser(description="分类标签标准化")
    parser.add_argument("--input", default=DEFAULT_INPUT, help="输入 CSV")
    parser.add_argument("--output", default=DEFAULT_OUTPUT, help="输出 CSV")
    return parser.parse_args()


def main():
    args = parse_args()

    with open(args.input, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames)
        rows = list(reader)

    print(f"Total rows: {len(rows)}")

    cat_counter = Counter()
    updated = 0

    for row in rows:
        # 标准化一级分类
        old = row.get('category', '')
        new = normalize_category(old)
        if old != new:
            row['category'] = new
            updated += 1
        cat_counter[new] += 1

        # 标准化二级分类
        if 'subcategory' in row:
            row['subcategory'] = normalize_subcategory(row.get('subcategory', ''), new)

        # 标准化跨领域标签
        if 'cross_domain' in row:
            row['cross_domain'] = normalize_cross_domain(row.get('cross_domain', ''))

    print(f"Updated: {updated}")
    print(f"\nFinal distribution:")
    for cat, count in cat_counter.most_common():
        cn = CATEGORY_MAP.get(cat, cat)
        print(f"  {cat} ({cn}): {count}")

    with open(args.output, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nOutput: {args.output}")
    return 0


if __name__ == "__main__":
    exit(main())
