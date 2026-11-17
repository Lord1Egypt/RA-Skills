#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sz-ink - audit_semantic.py 锚点核查器 (v0.1)
用法: python audit_semantic.py <改前.txt> <改后.txt> [--anchors anchors.json]
S6 还原审核第一查的脚本部分——只查机械可判项：
  ①数字保全：改前所有数字必须仍在改后
  ②专名保全：书名号/引号内容、英文专名必须仍在
  ③否定词守恒：否定词数量不许净减（立场翻转信号）
  ④锚点串保全：anchors.json 列出的关键句片段必须仍在
语义级复核（逻辑关系/立场）仍需独立盲审，本工具只兜底机械项。
输出: 漂移报告 JSON（stdout 或 --out）
"""
import sys, json, re, argparse
from pathlib import Path

NEG_WORDS = ['不', '没', '未', '无', '别', '莫', '勿', '非', '难以', '无法', '不能']
CN_WORD = r'[\u4e00-\u9fff]'


def extract_numbers(text):
    return re.findall(r'\d+(?:\.\d+)?(?:%|万|亿|千|百|元|年|月|日|号|个|次|倍)?', text)


def extract_proper(text):
    props = set()
    props.update(re.findall(r'《([^》]{1,30})》', text))          # 书名号
    props.update(re.findall(r'[""「]([^""」]{2,20})[""」]', text))  # 引号短语
    props.update(re.findall(r'([A-Za-z][A-Za-z0-9 .\-]{1,29})', text))  # 英文专名
    return props


def count_neg(text):
    return sum(text.count(w) for w in NEG_WORDS)


def audit(before, after, anchors):
    drifts = []
    # ① 数字
    bn, an = extract_numbers(before), extract_numbers(after)
    an_pool = list(an)
    for n in bn:
        if n in an_pool:
            an_pool.remove(n)
        else:
            drifts.append({'type': '数字丢失', 'value': n, 'severity': 'high'})
    # ② 专名
    bp, ap = extract_proper(before), extract_proper(after)
    for p in bp - ap:
        if p.strip():  # 排除纯空白
            drifts.append({'type': '专名丢失', 'value': p.strip(), 'severity': 'high'})
    # ③ 否定词
    nb, na = count_neg(before), count_neg(after)
    if na < nb - 1:  # 允许±1容差（表达重排可合并否定）
        drifts.append({'type': '否定词净减', 'before': nb, 'after': na,
                       'severity': 'medium', 'note': '立场翻转信号，需人工复核'})
    # ④ 锚点串
    for a in anchors or []:
        if a and a not in after:
            drifts.append({'type': '锚点丢失', 'value': a[:40], 'severity': 'high'})

    return {
        'numbers_before': len(bn), 'numbers_after': len(an),
        'proper_nouns_before': len(bp), 'proper_nouns_after': len(ap),
        'negation_before': nb, 'negation_after': na,
        'drift_count': len(drifts),
        'drifts': drifts,
        'verdict': 'PASS' if not drifts else ('REVIEW' if all(d['severity'] == 'medium' for d in drifts) else 'FAIL'),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('before', help='改前文本文件')
    ap.add_argument('after', help='改后文本文件')
    ap.add_argument('--anchors', default=None, help='锚点JSON文件（字符串数组）')
    ap.add_argument('--out', default=None, help='漂移报告输出路径')
    a = ap.parse_args()

    before = Path(a.before).read_text(encoding='utf-8')
    after = Path(a.after).read_text(encoding='utf-8')
    anchors = json.loads(Path(a.anchors).read_text(encoding='utf-8')) if a.anchors else []

    report = audit(before, after, anchors)
    out = json.dumps(report, ensure_ascii=False, indent=2)
    if a.out:
        Path(a.out).write_text(out, encoding='utf-8')
        print(f'漂移报告已写入: {a.out}')
    print(out)
    sys.exit(0 if report['verdict'] == 'PASS' else 1)


if __name__ == '__main__':
    main()
