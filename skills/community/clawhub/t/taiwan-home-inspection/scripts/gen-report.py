#!/usr/bin/env python3
"""
Home Inspection Report Generator
Usage: python gen-report.py <input-json> <output-path>

Input JSON format:
{
  "property": {
    "address": "台北市...",
    "area": 35.0,
    "age": 15,
    "type": "電梯大樓",
    "floor": "8F/14F"
  },
  "findings": [
    { "zone": "結構", "item": "樑", "defect": "45度裂縫", "grade": "大缺失", "note": "..." }
  ],
  "inspector": "驗屋人員姓名",
  "date": "2026-06-14"
}
"""

import json
import sys
import os
from datetime import datetime

def load_template(path):
    """Load the report markdown template."""
    template_path = path or os.path.join(os.path.dirname(__file__), '..', 'assets', 'report-template.md')
    with open(template_path, 'r', encoding='utf-8') as f:
        return f.read()

def grade_emoji(grade):
    mapping = {
        '大缺失': '🔴',
        '中缺失': '🟡',
        '小缺失': '🟢',
        '注意事項': 'ℹ️',
    }
    return mapping.get(grade, '•')

def count_by_grade(findings):
    counts = {'大缺失': 0, '中缺失': 0, '小缺失': 0, '注意事項': 0}
    for f in findings:
        g = f.get('grade', '')
        if g in counts:
            counts[g] += 1
    return counts

def generate_report(data, output_path):
    p = data.get('property', {})
    findings = data.get('findings', [])
    grade_counts = count_by_grade(findings)

    # Build findings table
    items_lines = []
    for i, f in enumerate(findings, 1):
        emoji = grade_emoji(f.get('grade', ''))
        note = f.get('note', '') or ''
        note_str = f' — {note}' if note else ''
        items_lines.append(f'{i}. {emoji} **{f.get("zone")}** → {f.get("item")}：{f.get("defect")}{note_str}')

    items_text = '\n'.join(items_lines) if items_lines else '本次檢查無異常。'

    # Summary
    total = sum(grade_counts.values())
    summary_lines = [f'- 🔴 大缺失：{grade_counts["大缺失"]} 項', f'- 🟡 中缺失：{grade_counts["中缺失"]} 項', f'- 🟢 小缺失：{grade_counts["小缺失"]} 項', f'- ℹ️ 注意事項：{grade_counts["注意事項"]} 項', f'- **合計：{total} 項**']

    # Has major defects?
    major_defects = [f for f in findings if f.get('grade') == '大缺失']
    conclusion = ''
    if major_defects:
        conclusion = '⚠️ 本案存在大缺失，建議修復完成後再進行交屋程序。'
    elif total == 0:
        conclusion = '✅ 本案檢查結果良好，無異常發現。'
    else:
        conclusion = '📋 本案有以上缺失，建議與賣方協商修復或折價。'

    report = f"""# 🏠 驗屋檢查報告

## 物件基本資料

| 項目 | 內容 |
|------|------|
| 地址 | {p.get('address', '—')} |
| 坪數 | {p.get('area', '—')} 坪 |
| 屋齡 | {p.get('age', '—')} 年 |
| 類型 | {p.get('type', '—')} |
| 樓層 | {p.get('floor', '—')} |
| 檢查日期 | {data.get('date', '—')} |
| 檢查人員 | {data.get('inspector', '—')} |

## 缺失統計

{'  '.join(summary_lines)}

## 檢查明細

{items_text}

## 綜合結論

{conclusion}

---
*報告由 Home Inspection Skill 自動產生*
*產出時間：{datetime.now().strftime('%Y-%m-%d %H:%M')}*
"""

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f'✅ 報告已產出：{output_path}')
    print(f'   共 {total} 項缺失（大缺失 {grade_counts["大缺失"]} 項）')

def main():
    if len(sys.argv) < 3:
        print('Usage: python gen-report.py <input-json> <output-path>')
        print('  input-json: Path to findings JSON file')
        print('  output-path: Output file path (.md)')
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    if not os.path.exists(input_path):
        print(f'❌ 找不到輸入檔案：{input_path}')
        sys.exit(1)

    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    generate_report(data, output_path)

if __name__ == '__main__':
    main()
