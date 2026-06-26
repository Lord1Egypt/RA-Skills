# -*- coding: utf-8 -*-
"""
合并 LLM 检查点结果到 CSV
将 llm_checkpoint.json 中的 LLM 分类结果合并回 articles_final.csv

用法：
    python merge_llm_results.py [--input CSV] [--checkpoint JSON] [--output CSV]
"""

import csv, json, argparse, os
from collections import Counter

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_INPUT = os.path.join(SCRIPT_DIR, "..", "exported_favorites", "articles_final.csv")
DEFAULT_OUTPUT = os.path.join(SCRIPT_DIR, "..", "exported_favorites", "articles_final_llm.csv")
DEFAULT_CHECKPOINT = os.path.join(SCRIPT_DIR, "..", "exported_favorites", "llm_checkpoint.json")


def parse_args():
    parser = argparse.ArgumentParser(description="合并 LLM 检查点结果到 CSV")
    parser.add_argument("--input", default=DEFAULT_INPUT, help="输入 CSV")
    parser.add_argument("--output", default=DEFAULT_OUTPUT, help="输出 CSV")
    parser.add_argument("--checkpoint", default=DEFAULT_CHECKPOINT, help="检查点文件")
    parser.add_argument("--min-confidence", type=float, default=0.5,
                        help="LLM 结果最低置信度（低于此值保留原分类）")
    return parser.parse_args()


def main():
    args = parse_args()

    if not os.path.exists(args.checkpoint):
        print(f"[ERROR] 检查点文件不存在: {args.checkpoint}")
        return 1

    # 加载检查点
    with open(args.checkpoint, 'r', encoding='utf-8') as f:
        cp = json.load(f)

    llm_results = {}
    for r in cp.get('results', []):
        lid = r.get('local_id', '')
        if lid:
            llm_results[lid] = r

    print(f"Loaded {len(llm_results)} LLM results from checkpoint")

    # 读取 CSV
    with open(args.input, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames)
        rows = list(reader)

    print(f"Loaded {len(rows)} rows from CSV")

    # 修复 BOM
    if '\ufefflocal_id' in fieldnames:
        idx = fieldnames.index('\ufefflocal_id')
        fieldnames[idx] = 'local_id'

    # 合并
    tag_counter = Counter()
    updated = 0
    still_other = 0

    for row in rows:
        lid = row.get('local_id', '')
        if lid in llm_results:
            result = llm_results[lid]
            new_tags = result.get('tags', [])
            confidence = result.get('confidence', 0)

            if new_tags and confidence >= args.min_confidence:
                # 取第一个标签作为主分类
                row['category'] = new_tags[0]
                row['_llm_tags'] = '|'.join(new_tags)
                row['_llm_confidence'] = str(confidence)
                row['_llm_reason'] = result.get('reason', '')
                tag_counter[new_tags[0]] += 1
                updated += 1
            else:
                still_other += 1
        elif row.get('category', '') == 'other':
            still_other += 1

    # 添加新字段
    for f in ['_llm_tags', '_llm_confidence', '_llm_reason']:
        if f not in fieldnames:
            fieldnames.append(f)

    # 写输出
    with open(args.output, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nUpdated: {updated}")
    print(f"Still other (low confidence): {still_other}")
    print(f"\nTag distribution:")
    for tag, count in tag_counter.most_common():
        print(f"  {tag}: {count}")
    print(f"\nOutput: {args.output}")
    return 0


if __name__ == "__main__":
    exit(main())
