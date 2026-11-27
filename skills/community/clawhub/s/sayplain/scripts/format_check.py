#!/usr/bin/env python3
# 格式扫描：按「风格手册.md」扫一篇稿子的格式/口径问题，报命中位置与条数，不下合格判定。
# 它只读取文件、不修改任何东西；对应 SKILL.md 的第零道「格式统一」。
#
# 可机器扫描的部分：术语大小写变体、标题层级异常（跳级/超三级/标题内包裹）、
# 引号/符号混用、疑似整段加粗、单路径独占围栏、围栏语言标签混用、行尾多余空格。
# 代码块内的内容一律跳过（保护边界）；真实引语、产品专名脚本无法识别，
# 命中时先人工排除再判定。错别字语义判断、编号跳号的人工复核对照风格手册做。
# 判据只有一条：当前写法是否匹配风格手册。命中是信号，不是违规。
#
# 用法（工作区根目录执行）：
#   python <skill_dir>/scripts/format_check.py <目标稿件.md>

import re
import sys

# 术语变体：统一写法在前，变体为正则
TERMS = [
    ('Skill 概念大写', r'(?<![A-Za-z/])[sS][kK][iI][lL][lL](?![A-Za-z])', ['Skill', 'SKILL.md', 'skill.md']),
    ('MCP 全大写', r'(?<![A-Za-z/])(?:Mcp|mcp)(?![A-Za-z])', ['MCP']),
    ('prompt 小写', r'(?<![A-Za-z/])Prompt(?![A-Za-z])', ['prompt', '提示词']),
    ('Spec 概念大写', r'(?<![A-Za-z/])spec(?!\.[a-zA-Z])(?![A-Za-z])', ['Spec', 'spec.md']),
    ('Agent 首字母大写', r'(?<![A-Za-z/])agent(?![A-Za-z])', ['Agent']),
    ('AGENTS.md 文件名', r'(?<![A-Za-z/])(?:Agent\.md|agent\.md)(?![A-Za-z])', ['AGENTS.md']),
    ('Subagent 连写', r'Sub\s+Agent', ['Subagent']),
    ('术语书名号', r'《\s*(?:skill|Skill|SKILL|mcp|MCP|spec|Spec)\s*》', ['Skill', 'MCP', 'Spec']),
]

HEAD_EMPTY = re.compile(r'^#{1,6}\s*$')
HEAD_DOUBLE = re.compile(r'^##\s+##\s')
CODE_FENCE = re.compile(r'^\s*```')


def paint(s, code):
    return '\033[{}m{}\033[0m'.format(code, s) if sys.stdout.isatty() else s


def code_block_mask(lines):
    """返回与 lines 等长的布尔列表，True 表示该行在代码块内（保护边界，跳过）。"""
    mask = [False] * len(lines)
    in_code = False
    for i, ln in enumerate(lines):
        if CODE_FENCE.match(ln):
            in_code = not in_code
            mask[i] = True  # 围栏行本身跳过
        elif in_code:
            mask[i] = True
    return mask


def main():
    if len(sys.argv) != 2:
        print('Usage: python format_check.py <target.md>', file=sys.stderr)
        return 2
    target = sys.argv[1]
    with open(target, encoding='utf-8', newline='') as f:
        lines = f.read().split('\n')
    mask = code_block_mask(lines)

    print()
    print(paint('格式扫描：{}（{} 行，其中代码块 {} 行已跳过）'.format(
        target, len(lines), sum(mask)), 36))
    print(paint('命中是信号，不是违规。真实引语、产品专名请人工排除后再判定。', 90))
    print()

    total = 0

    # ---- 标题层级的文件级检查（只看非代码块行）----
    head_lines = [(i + 1, ln) for i, ln in enumerate(lines)
                  if not mask[i] and re.match(r'^#{1,6}\s', ln)]
    if head_lines:
        first_lv = len(head_lines[0][1]) - len(head_lines[0][1].lstrip('#'))
        if first_lv > 1:
            total += 1
            print(paint('[标题] 首个标题不是一级标题 #（当前是第 {} 级）：第 {} 行  {}'.format(
                first_lv, head_lines[0][0], head_lines[0][1].strip()), 33))
        tops = [(i, ln) for i, ln in head_lines if len(ln) - len(ln.lstrip('#')) == 1]
        if len(tops) > 1:
            total += 1
            print(paint('[标题] 出现 {} 个一级标题 #（应每篇一个）：行 {}'.format(
                len(tops), [i for i, _ in tops]), 33))

    for i, ln in enumerate(lines, 1):
        if mask[i - 1]:
            continue
        if HEAD_DOUBLE.search(ln):
            total += 1
            print(paint('[标题] 双井号 "## ##"：第 {} 行  {}'.format(i, ln.strip()[:58]), 33))
        if HEAD_EMPTY.match(ln):
            total += 1
            print(paint('[标题] 空标题：第 {} 行  {}'.format(i, ln.strip()), 33))

    # ---- 术语变体 ----
    for name, pattern, preferred in TERMS:
        regex = re.compile(pattern)
        hits = [i for i, ln in enumerate(lines, 1)
                if not mask[i - 1] and regex.search(ln)]
        if hits:
            total += len(hits)
            print('{:<22} 命中 {} 行（建议统一为 {}）'.format(name, len(hits), ' / '.join(preferred)))
            for i in hits[:8]:
                snippet = lines[i - 1].strip()
                if len(snippet) > 64:
                    snippet = snippet[:64] + '…'
                print(paint('    第 {} 行  {}'.format(i, snippet), 33))

    # ---- 引号 / 符号 ----
    quote_checks = [
        ('直角引号「」', r'[「」]', '“”'),
        ('直角引号『』', r'[『』]', '“”'),
        ('中文里的半角双引号 "', r'[^A-Za-z0-9]"', '“”'),
    ]
    for name, pattern, preferred in quote_checks:
        regex = re.compile(pattern)
        hits = [i for i, ln in enumerate(lines, 1)
                if not mask[i - 1] and regex.search(ln)]
        if hits:
            total += len(hits)
            print('{:<22} 命中 {} 行（建议统一为 {}）'.format(name, len(hits), preferred))
            for i in hits[:8]:
                snippet = lines[i - 1].strip()
                if len(snippet) > 64:
                    snippet = snippet[:64] + '…'
                print(paint('    第 {} 行  {}'.format(i, snippet), 33))

    # ---- 标题层级：跳级 / 超三级 / 标题内包裹符号 ----
    prev_lv = None
    for i, ln in head_lines:
        lv = len(ln) - len(ln.lstrip('#'))
        if lv > 3:
            total += 1
            print(paint('[标题] 层级超过三级（{} 级）：第 {} 行  {}'.format(lv, i, ln.strip()[:56]), 33))
        if prev_lv is not None and lv > prev_lv + 1:
            total += 1
            print(paint('[标题] 层级跳级（{} → {}）：第 {} 行  {}'.format(
                prev_lv, lv, i, ln.strip()[:56]), 33))
        prev_lv = lv
        if '**' in ln or '`' in ln:
            total += 1
            print(paint('[标题] 标题内含加粗或反引号（标题内应裸写）：第 {} 行  {}'.format(
                i, ln.strip()[:56]), 33))

    # ---- 整行加粗且 3 句以上（疑似整段加粗）----
    for i, ln in enumerate(lines, 1):
        if mask[i - 1]:
            continue
        s = ln.strip()
        if re.match(r'^\*\*[^*]+\*\*$', s) and s.count('。') >= 3:
            total += 1
            print(paint('[加粗] 整行加粗且含 {} 个句号（疑似整段加粗）：第 {} 行  {}'.format(
                s.count('。'), i, s[:56]), 33))

    # ---- 行尾多余空格（多于 2 个；2 个是硬换行，保留）----
    for i, ln in enumerate(lines, 1):
        if mask[i - 1]:
            continue
        trail = len(ln) - len(ln.rstrip(' '))
        if trail > 2:
            total += 1
            print(paint('[空白] 行尾多余空格（{} 个）：第 {} 行'.format(trail, i), 33))

    # ---- 单个路径/文件名独占围栏块（建议改行内代码）----
    j = 0
    while j < len(lines):
        if CODE_FENCE.match(lines[j]):
            k = j + 1
            body = []
            while k < len(lines) and not CODE_FENCE.match(lines[k]):
                if lines[k].strip():
                    body.append(lines[k].strip())
                k += 1
            if len(body) == 1 and re.fullmatch(r'[\w./\\<>:\-]+', body[0]) \
                    and ('.' in body[0] or '/' in body[0] or '\\' in body[0]):
                total += 1
                print(paint('[围栏] 单个路径/文件名独占围栏块（建议改行内代码）：第 {} 行  {}'.format(
                    j + 1, body[0][:56]), 33))
            j = k + 1
        else:
            j += 1

    # ---- 同文件围栏语言标签混用 ----
    langs = set()
    for ln in lines:
        m = re.match(r'^\s*```([A-Za-z]+)\s*$', ln)
        if m:
            langs.add(m.group(1).lower())
    if 'md' in langs and 'markdown' in langs:
        total += 1
        print(paint('[围栏] 围栏语言标签混用：md / markdown（同文件应统一）', 33))

    print()
    print('合计命中 {} 处'.format(total))
    print('提示：编号跳号（方法五→六、小节1→4）与错别字请对照 references/风格手册.md 人工复核。')
    print()
    return 0


if __name__ == '__main__':
    sys.exit(main())
