# -*- coding: utf-8 -*-
"""
HTML 章节草稿预扫描脚本 — 在 assemble.py 运行前检测三类 <code> 标签问题
=============================================================================
生产教训：子代理生成的 HTML 中 <code> 标签经常出现结构性错误，导致：
  1. <code> 开启/闭合数量不匹配 → 后续内容全部变成等宽字体
  2. 块级标签 (<p>/<table>/<h3> 等) 被错误嵌套在 <code> 内 → font-family: monospace 泄漏到正文
  3. 闭合标签与 </strong> 混用（如 </code> 错写成 </strong>）

用法：python scripts/scan_html.py              （扫描工作区所有 _draft_*.html）
      python scripts/scan_html.py --fix           （交互式修复，输出到 _draft_*_fixed.html）

检查项：
  A. <code>/</code> 开闭数量是否匹配
  B. <code>...</code> 内是否包含块级标签
  C. 闭合标签是否含中文字符（如 </strong文>）
"""

import re, os, sys, glob, argparse
from collections import defaultdict

# Windows 控制台默认 cp936 编码，emoji 输出会 UnicodeEncodeError
# 设置 stdout 为 utf-8，解决 "⚠️✅" 等字符在 Windows 上崩溃的问题
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BLOCK_TAGS = {'p', 'table', 'div', 'h2', 'h3', 'h4', 'h5', 'h6',
              'blockquote', 'ul', 'ol', 'li', 'section', 'article'}

# ─── 检查 A：<code> 开闭数量 ──────────────────────────────────────────
def check_code_balance(html, filepath):
    opens = len(re.findall(r'<\s*code[^>]*>', html, re.I))
    closes = len(re.findall(r'</\s*code\s*>', html, re.I))
    if opens != closes:
        return [(filepath, 'A.code_balance',
                 f'<code> 开启 {opens} 个，闭合 {closes} 个，差额 {opens - closes} '
                 f'（正数=缺闭合，负数=多余闭合）')]
    return []

# ─── 检查 B：块级标签嵌套在 <code> 内 ────────────────────────────────
def check_block_in_code(html, filepath):
    issues = []
    # 用简单方式：找每个 <code>...</code> 区间
    pattern = re.compile(r'<\s*code[^>]*>(.*?)</\s*code\s*>', re.S | re.I)
    for match in pattern.finditer(html):
        inner = match.group(1)
        for tag in BLOCK_TAGS:
            if re.search(rf'<\s*{tag}[\s>]', inner, re.I):
                ctx = inner[:120].replace('\n', ' ').strip()
                issues.append((filepath, 'B.block_in_code',
                               f'<code> 内包含块级标签 <{tag}>，'
                               f'导致 font-family: monospace 泄漏到正文。上下文: {ctx}'))
                break  # 同个 <code> 内只报第一个块级标签
    return issues

# ─── 检查 C：含中文的异常闭合标签 ────────────────────────────────────
def check_suspicious_close(html, filepath):
    issues = []
    # 匹配 </ 开头、> 结尾、中间含中文
    suspicious = re.findall(r'</\s*([^>]*[\u4e00-\u9fff][^>]*)>', html)
    seen = set()
    for s in suspicious:
        if s not in seen:
            seen.add(s)
            issues.append((filepath, 'C.suspicious_close',
                           f'疑似异常闭合标签: </{s}> '
                           f'（可能意欲写作 </code> 或 </strong> 但被中文字符污染）'))
    return issues

# ─── 检查 D：<code> 与 <strong> 交叉混用 ──────────────────────────────
def check_code_strong_cross(html, filepath):
    issues = []
    # <code><strong>...</code></strong> 或 <strong><code>...</strong></code> 交叉
    if re.search(r'<\s*code[^>]*>\s*<\s*strong[^>]*>.*?</\s*code\s*>.*?</\s*strong\s*>', html, re.S | re.I):
        issues.append((filepath, 'D.cross_nest',
                       '检测到 <code> 与 <strong> 交叉嵌套，可能导致字体异常'))
    return issues

# ─── 主流程 ──────────────────────────────────────────────────────────
def scan(drafts, verbose=True):
    all_issues = []
    stats = {'scanned': 0, 'clean': 0}
    for fp in drafts:
        if not os.path.exists(fp):
            continue
        stats['scanned'] += 1
        html = open(fp, encoding='utf-8', errors='ignore').read()
        issues = (
            check_code_balance(html, fp) +
            check_block_in_code(html, fp) +
            check_suspicious_close(html, fp) +
            check_code_strong_cross(html, fp)
        )
        all_issues.extend(issues)
        if not issues:
            stats['clean'] += 1

    if verbose:
        if not all_issues:
            print(f"✅ 扫描 {stats['scanned']} 个文件，全部通过")
        else:
            # 按类别分组打印
            by_cat = defaultdict(list)
            for _, cat, detail in all_issues:
                by_cat[cat].append(detail)
            print(f"⚠️ 扫描 {stats['scanned']} 个文件，发现 {len(all_issues)} 个问题 "
                  f"({stats['scanned'] - stats['clean']} 个文件):\n")
            for cat, details in sorted(by_cat.items()):
                print(f"  [{cat}] ({len(details)} 处)")
                for d in details:
                    print(f"    → {d}")
                print()

    return all_issues, stats

def main():
    parser = argparse.ArgumentParser(description='HTML 章节草稿 <code> 标签预扫描')
    parser.add_argument('--fix', action='store_true', help='交互式修复 (TODO)')
    parser.add_argument('--files', nargs='*', help='指定文件，默认扫描所有 _draft_*.html')
    args = parser.parse_args()

    drafts = args.files if args.files else (
        glob.glob('./other/_draft_*.html') + glob.glob('./other/_draft_ch_*.html') +
        glob.glob('_draft_*.html') + glob.glob('_draft_ch_*.html')  # fallback: root
    )
    drafts = sorted(set(drafts))

    if not drafts:
        print("[提示] 未找到 _draft_*.html 文件，跳过扫描")
        return 0

    if args.fix:
        print("[TODO] 自动修复模式尚未实现，请手工修复上述问题后重新运行")
        return 1

    issues, _ = scan(drafts, verbose=True)

    if issues:
        print("💡 建议：修复以上问题后运行 python ./other/assemble.py")
        return 1
    return 0

if __name__ == '__main__':
    sys.exit(main())
