#!/usr/bin/env python3
"""
Lease Contract Analysis Script
Usage: python analyze-contract.py <input-json> <output-path>

Input JSON format:
{
  "lease_type": "住宅" | "店面/商用" | "車位",
  "tenant": "承租人姓名 (optional)",
  "landlord": "出租人姓名 (optional)",
  "property": "地址 (optional)",
  "clauses": [
    { "clause": "第X條 禁止報稅", "risk": "違法條款"|"高風險"|"低風險"|"標準條款", "note": "說明" }
  ],
  "missing_items": ["審閱期條款", "修繕責任條款"],
  "suggestions": ["建議增加審閱期條款"]
}
"""

import json
import sys
import os
from datetime import datetime

RISK_EMOJI = {
    '違法條款': '🔴',
    '高風險': '🟡',
    '低風險': '🟢',
    '標準條款': '✅',
}

def count_risks(clauses):
    counts = {'違法條款': 0, '高風險': 0, '低風險': 0, '標準條款': 0}
    for c in clauses:
        r = c.get('risk', '')
        if r in counts:
            counts[r] += 1
    return counts

def generate_report(data, output_path):
    lease_type = data.get('lease_type', '住宅')
    clauses = data.get('clauses', [])
    missing = data.get('missing_items', [])
    suggestions = data.get('suggestions', [])
    risk_counts = count_risks(clauses)
    total = sum(risk_counts.values())

    # Build clause list
    clause_lines = []
    for i, c in enumerate(clauses, 1):
        emoji = RISK_EMOJI.get(c.get('risk', ''), '•')
        note = c.get('note', '') or ''
        note_str = f' — {note}' if note else ''
        clause_lines.append(f'{i}. {emoji} **{c["clause"]}**{note_str}')

    # Build missing items
    missing_text = '\n'.join(f'- ❌ {item}' for item in missing) if missing else '- 無缺失項目（所有應記載事項均已包含）'
    
    # Build suggestions
    suggestion_text = '\n'.join(f'- 💡 {s}' for s in suggestions) if suggestions else '- 無待修改事項'

    # Conclusion
    illegal_count = risk_counts.get('違法條款', 0)
    high_count = risk_counts.get('高風險', 0)
    if illegal_count > 0:
        conclusion = '⚠️ 本契約存在違法條款，依法無效，強烈建議修改後再行簽約。'
    elif high_count > 0:
        conclusion = '📋 本契約存在高風險條款，建議協商修改以保障權益。'
    elif missing:
        conclusion = '📋 本契約有缺失事項，建議補齊以符合法規。'
    else:
        conclusion = '✅ 本契約條款大體符合法規，可安心簽約。'

    report = f"""# 📄 租約審查報告

## 基本資訊

| 項目 | 內容 |
|------|------|
| 租約類型 | {lease_type} |
| 承租人 | {data.get('tenant', '—')} |
| 出租人 | {data.get('landlord', '—')} |
| 租賃標的 | {data.get('property', '—')} |
| 審查日期 | {datetime.now().strftime('%Y-%m-%d')} |

## 風險統計

- 🔴 違法條款：{risk_counts.get('違法條款', 0)} 條
- 🟡 高風險條款：{risk_counts.get('高風險', 0)} 條
- 🟢 低風險條款：{risk_counts.get('低風險', 0)} 條
- ✅ 標準條款：{risk_counts.get('標準條款', 0)} 條
- **合計：{total} 條**

## 條款審查明細

{chr(10).join(clause_lines)}

## 缺失事項（應有而無）

{missing_text}

## 修改建議

{suggestion_text}

## 綜合結論

{conclusion}

---
*報告由 Lease Review Skill 自動產生*
*產出時間：{datetime.now().strftime('%Y-%m-%d %H:%M')}*
"""

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f'✅ 審查報告已產出：{output_path}')
    print(f'   共分析 {total} 條條款（違法 {illegal_count} 條，高風險 {high_count} 條）')

def main():
    if len(sys.argv) < 3:
        print('Usage: python analyze-contract.py <input-json> <output-path>')
        print('  input-json: Path to contract clauses JSON')
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
