#!/usr/bin/env python3
"""
论文格式差异对比器 v2 — 基于 reader v2 classify_and_dump
输出属性级差异表，含 source_trace 诊断

用法:
  python3 differ.py 目标.docx --template 学校模板.docx -o 差异表.md
  python3 differ.py 目标.docx --template 学校模板.docx --json -o 差异表.json
"""
import sys, os, json, argparse
from pathlib import Path

BASE = Path(__file__).parent
sys.path.insert(0, str(BASE))
from reader import classify_and_dump


def diff(pap_rules, ref_rules, fix_types=None):
    """比对两套规则，返回属性级差异"""
    pap_by = {r['type']: r for r in pap_rules}
    ref_by = {r['type']: r for r in ref_rules}

    pPr = ['alignment', 'spacing_beforeLines', 'spacing_afterLines',
           'spacing_line', 'spacing_lineRule',
           'indent_firstLine', 'indent_firstLineChars',
           'indent_left', 'indent_right', 'indent_hanging']
    rPr = ['font_eastAsia', 'font_ascii', 'font_hAnsi', 'font_size', 'bold']

    diffs = []
    for ptype, ref in sorted(ref_by.items()):
        if fix_types and ptype not in fix_types:
            continue
        pap = pap_by.get(ptype)
        if not pap:
            continue

        items = {}
        for k in pPr:
            e = ref['final_pPr'].get(k, '')
            a = pap['final_pPr'].get(k, '')
            if e and a and e != a:
                items[k] = {'expected': e, 'actual': a,
                            'ref_src': ref.get('source_trace', {}).get(k, '?'),
                            'pap_src': pap.get('source_trace', {}).get(k, '?')}
        for k in rPr:
            e = ref['final_rPr'].get(k, '')
            a = pap['final_rPr'].get(k, '')
            if e and a and e != a:
                items[k] = {'expected': e, 'actual': a,
                            'ref_src': ref.get('source_trace', {}).get(k, '?'),
                            'pap_src': pap.get('source_trace', {}).get(k, '?')}

        if items:
            diffs.append({
                'type': ptype,
                'label': ref.get('label', ptype),
                'ref_count': ref.get('count', 0),
                'pap_count': pap.get('count', 0),
                'ref_readable': ref.get('readable', ''),
                'pap_readable': pap.get('readable', ''),
                'diffs': items
            })

    return diffs


def format_markdown(diffs, template_name='', paper_name=''):
    lines = [
        f'# 论文格式差异对照表',
        f'',
        f'- **模板**: {template_name}',
        f'- **论文**: {paper_name}',
        f'- **差异项**: {len(diffs)}',
        f'',
        f'| 类型 | 标签 | 属性 | 模板值 | 论文值 | 模板来源 | 论文来源 |',
        f'|------|------|------|--------|--------|----------|----------|',
    ]
    for d in diffs:
        for attr, dv in sorted(d['diffs'].items()):
            lines.append(
                f'| {d["type"]} | {d["label"]} | `{attr}` | `{dv["expected"]}` | `{dv["actual"]}` | {dv.get("ref_src", "?")} | {dv.get("pap_src", "?")} |'
            )
    lines.append('')
    lines.append('> source_trace: `ref_src` = 模板中该属性的来源层, `pap_src` = 论文中该属性的来源层')
    return '\n'.join(lines)


def main():
    p = argparse.ArgumentParser(description='论文格式差异对比器 v2')
    p.add_argument('paper', help='目标论文 .docx')
    p.add_argument('--template', '-t', required=True, help='学校模板 .docx')
    p.add_argument('--output', '-o', help='输出文件 (.md 或 .json)')
    p.add_argument('--json', action='store_true', help='输出 JSON 格式')
    p.add_argument('--types', help='仅比对指定类型(逗号分隔)')
    args = p.parse_args()

    paper = Path(args.paper)
    template = Path(args.template)
    for fp, label in [(paper, '论文'), (template, '模板')]:
        if not fp.exists():
            print(f'❌ {label}不存在: {fp}')
            sys.exit(1)

    print(f'📐 解析模板: {template.name}')
    ref_rules, ref_meta = classify_and_dump(str(template))
    print(f'📄 解析论文: {paper.name}')
    pap_rules, pap_meta = classify_and_dump(str(paper))

    fix_types = set(args.types.split(',')) if args.types else None
    diffs = diff(pap_rules, ref_rules, fix_types)

    if args.json:
        output_data = {'diffs': diffs, 'template': str(template), 'paper': str(paper)}
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, ensure_ascii=False, indent=2)
            print(f'📄 JSON → {args.output}')
        else:
            print(json.dumps(output_data, ensure_ascii=False, indent=2))
    else:
        md = format_markdown(diffs, template.name, paper.name)
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(md)
            print(f'📄 MD → {args.output}')
        else:
            print(md)


if __name__ == '__main__':
    main()
