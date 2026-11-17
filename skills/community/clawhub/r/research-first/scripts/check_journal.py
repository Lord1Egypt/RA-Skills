#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
研究纪要判据机检器 —— research-first skill 配套
用法: python check_journal.py <纪要.md>

机检 S1 / S2 / S4，并对 S5（量化必须有出处）做辅助扫描。S3 需人工判定。

退出码:
  0 = 全部通过
  1 = 存在红项
  2 = 解析失败（0 条结论）—— 空过防护，见下方 VACUOUS_GUARD
"""
import sys
import re

# ⛔ VACUOUS_GUARD
# 开源社区踩过的坑：校验器支持多 schema 时，遇到没见过的结构会"静默解析零字段"，
# 结果判据永远为绿 —— 叫 vacuous pass（空过）。commit 证据：
# Weizhena/Deep-Research-skills@6ce38f6 "fixing the vacuous-pass bug"
# ⇒ 本脚本解析不到任何结论行时，必须 exit 2 报错，绝不允许"没读到 = 通过"。

URL_RE = re.compile(r'https?://([^\s\)\|\]`，。、]+)')
HAS_DIGIT = re.compile(r'\d')
SEP_ROW = re.compile(r'^\s*\|[\s:\-|]+\|\s*$')
NONE_MARKS = {'—', '-', '–', '无', 'n/a', 'N/A', ''}
NEGATIVE = ('未做', '没做', '未搜', '没搜', '未检索', '没有查', '没查', '未触顶',
            '❌', '跳过', '略', '待补')


def die(msg, code=2):
    print(f'⛔ {msg}')
    sys.exit(code)


def split_row(line):
    return [c.strip() for c in line.strip().strip('|').split('|')]


def strip_fences(lines):
    """剔除 ``` 代码块，返回 [(原行号, 文本)]。
    ⛔ 必须剔：模板代码块里也有'结论/出处'表头和'反面样本…未做'字样，
    不剔会把模板当真实内容读（2026-10-18 实测踩到）。"""
    out, fence = [], False
    for i, ln in enumerate(lines, 1):
        if ln.lstrip().startswith('```'):
            fence = not fence
            continue
        if not fence:
            out.append((i, ln))
    return out


def is_header(cells):
    """严格列名匹配：⛔ 不可用 '结论' in line 子串匹配 ——
    正文里 '| S2 | 每条结论都能指到出处 | … |' 会被误当表头（2026-10-18 实测踩到）。"""
    norm = [c.replace('**', '').replace('*', '').replace('`', '').strip() for c in cells]
    return '结论' in norm and '出处' in norm


def find_conclusion_table(lines):
    """返回 [(原文件行号, cells)]；找不到或无数据行返回 []"""
    for idx, (lineno, ln) in enumerate(lines):
        if not ln.lstrip().startswith('|'):
            continue
        cells = split_row(ln)
        if len(cells) < 3 or not is_header(cells):
            continue
        j = idx + 1
        if j < len(lines) and SEP_ROW.match(lines[j][1]):
            j += 1
        rows = []
        while j < len(lines) and lines[j][1].lstrip().startswith('|'):
            c2 = split_row(lines[j][1])
            if len(c2) >= 5 and not SEP_ROW.match(lines[j][1]):
                rows.append((lines[j][0], c2))
            j += 1
        if rows:
            return rows
    return []


def find_section(lines, keywords):
    """抓取含任一关键词的小节正文（跳过代码块），返回文本。

    ⛔⛔ 这个函数踩了四轮才对，连踩记录（2026-10-18，别删）：
      v1 len(strip('#'))<=2 当边界 ⇒ `###` 被吞进本节
      v2 误判为「井号数量 vs 标题文字」⇒ 没修到点
      v3 改成「任何标题即边界」⇒ 边界对了，但仍抓错小节
      v4 ⭐ 真根因：`strip_fences()` 返回的是 (原文件行号, 文本)，
         而 v1–v3 都写成 `for i,ln in lines: range(i+1, len(lines))`，
         ⛔ 把**原文件行号当成列表索引**切片 ⇒ 剔除代码块后列表变短 ⇒ 索引整体偏移
         ⇒ 抓到了 20 多行之外的小节 ⇒ 把「明确写了未做」判成有内容（假阴性）。
      正解：必须用 `enumerate` 拿**列表索引**，原文件行号只用于报错定位。
    ⚠️ 假阴性比假阳性严重：假阳性只是费时间，假阴性是骗自己。
    ⚠️ 教训：判据连修三次不对时，⛔ 不要继续读代码猜 —— 打印中间值。
    """
    for idx, (lineno, ln) in enumerate(lines):
        if ln.startswith('#') and any(k in ln for k in keywords):
            buf = []
            for k in range(idx + 1, len(lines)):
                t = lines[k][1]
                if t.lstrip().startswith('#'):
                    break
                buf.append(t)
            return '\n'.join(buf).strip()
    return None


def main(path):
    try:
        with open(path, encoding='utf-8') as f:
            lines = strip_fences(f.read().splitlines())
    except OSError as e:
        die(f'读不了文件: {e}')

    rows = find_conclusion_table(lines)
    if not rows:
        die('解析到 0 条结论 —— 判据空过（vacuous pass）。\n'
            '   纪要里必须有表头含「结论」与「出处」的表格，列名照 references/纪要模板.md。')

    domains, named, no_src, unverif, unsourced_nums = set(), 0, [], [], []
    for lineno, c in rows:
        concl, val, src, strength = c[1], c[2], c[3], (c[4] if len(c) > 4 else '')
        urls = URL_RE.findall(src)
        for d in urls:
            domains.add(d.lower().split('/')[0].lstrip('www.').strip())
        marked_unverif = ('未验证' in strength) or ('未验证' in src)
        src_blank = src in NONE_MARKS
        if not urls:
            if src and not src_blank:
                named += 1
            if not marked_unverif:
                no_src.append((lineno, concl[:28]))
        if HAS_DIGIT.search(concl) and not urls and not marked_unverif:
            unsourced_nums.append((lineno, concl[:28]))

    # ---------- S1 ----------
    if len(domains) >= 3:
        s1 = ('PASS', f'独立域名 {len(domains)} 个: ' + ', '.join(sorted(domains)))
    elif len(domains) + named >= 3:
        s1 = ('WARN', f'可辨来源 {len(domains) + named} 个，但只有 {len(domains)} 个带 URL '
                      f'⇒ 复核者无法回溯原始页面。补 URL')
    else:
        s1 = ('FAIL', f'独立来源不足：域名 {len(domains)} + 具名 {named} < 3'
                      f'（⛔ 转载/摘要不算独立来源）')

    # ---------- S2 ----------
    if no_src:
        s2 = ('FAIL', f'{len(no_src)} 条结论既无 URL 也未标「未验证」，行号: '
                      + ', '.join(str(n) for n, _ in no_src))
    elif named:
        s2 = ('WARN', f'{named} 条只有来源名没有 URL（可追溯但不可回溯），建议补 URL')
    else:
        s2 = ('PASS', f'{len(rows)} 条结论全部带 URL 出处')

    # ---------- S4 ----------
    # ⛔⛔ 2026-10-18 修正：原判据是「含否定词 ⇒ 判没做」。
    # 实测假阳性：我把「未做」改写成真内容后，句尾仍带一句「本节仍未做：…」，
    # 判据照样报红 —— **"含否定词"不等于"没做"，判据问错了问题**。
    # 正解：剔除否定句后看**净内容量**（净字数下限 40）。
    sec = find_section(lines, ['反面样本', '失败案例', '反面'])
    if sec is None:
        s4 = ('FAIL', '找不到「反面样本 / 失败案例」小节 —— S4 要求必须搜过失败模式')
    else:
        keep = [l.strip() for l in sec.splitlines()
                if l.strip() and not any(n in l for n in NEGATIVE)]
        net = re.sub(r'[\s|*#`\-—·]', '', ''.join(keep))
        has_neg = any(n in sec for n in NEGATIVE)
        if len(net) < 40:
            s4 = ('FAIL', f'反面样本小节**净内容只有 {len(net)} 字**（剔掉否定句后）'
                          f' ⇒ 实质等于没做（只搜正确做法 = 没 research）')
        elif has_neg:
            s4 = ('WARN', f'有实质内容（净 {len(net)} 字），但仍含未完成项 —— '
                          f'需在「未决」里跟进（⛔ 不算红项）')
        else:
            s4 = ('PASS', f'反面样本小节有实质内容（净 {len(net)} 字）')

    # ---------- S5 辅助 ----------
    if unsourced_nums:
        s5 = ('WARN', f'{len(unsourced_nums)} 条含数字的结论无出处（数字最像证据，最容易掩盖没查），'
                      f'行号: ' + ', '.join(str(n) for n, _ in unsourced_nums))
    else:
        s5 = ('PASS', '无「有数字但无出处」的结论')

    # ---------- S3 边际收敛（2026-10-18 补机检） ----------
    # 判据：边际收敛记录表里是否存在**连续两行**「新增事实数 = 0」
    sec3 = find_section(lines, ['边际收敛'])
    if sec3 is None:
        s3 = ('FAIL', '找不到「边际收敛记录」小节 —— S3 要求记录每轮新增事实数')
    else:
        zeros, rows3 = 0, []
        for ln in sec3.splitlines():
            ln = ln.strip()
            if not ln.startswith('|') or SEP_ROW.match(ln):
                continue
            cells = split_row(ln)
            if len(cells) < 2:
                continue
            tail = cells[-1].strip()
            # ⛔ 2026-10-18 修正：原正则 ^(\d+)\+?$ 要求纯数字，
            # 但人习惯写「6+（on twos/threes…）」⇒ 明明有数据却判"不可解析"。
            # 放宽为**取前缀数字**：6、6+、6+（说明…）、0、0+ 都能解析。
            m = re.match(r'^(\d+)', tail)
            if m and cells[0].strip().rstrip('.').isdigit():
                rows3.append(int(m.group(1)))
                if int(m.group(1)) == 0:
                    zeros += 1
        if not rows3:
            s3 = ('FAIL', '边际收敛表里没有可解析的「新增事实数」列（要写成纯数字，可带 +）')
        elif zeros >= 2:
            s3 = ('PASS', f'{len(rows3)} 轮记录，出现连续 ≥2 次零新增 ⇒ 已触顶')
        else:
            s3 = ('WARN', f'{len(rows3)} 轮记录，但零新增只出现 {zeros} 次 '
                          f'⇒ 尚未触顶（S3 是收敛制：没触顶不等于错，但别把它当"已查完"）')

    # ---------- S6 探索产出率（2026-10-18 11:50 补机检） ----------
    # 一句话判据：说不出一个「我之前不知道它存在」的东西，这轮 research 就是白做的。
    # 计数器：U = 探索条目数（红线 <3）／ C = 类别含"能力"的条数（红线 <1）
    sec6 = find_section(lines, ['探索产出', '不知道 → 已知', '不知道→已知'])
    if sec6 is None:
        s6 = ('FAIL', '找不到「探索产出」小节 —— ⛔ 不填就默认是防守型 research。'
                        '每轮必须回答：我新发现了什么**存在**的东西？')
    else:
        U, C = 0, 0
        for ln in sec6.splitlines():
            ln = ln.strip()
            if not ln.startswith('|') or SEP_ROW.match(ln):
                continue
            cells = split_row(ln)
            if len(cells) < 4:
                continue
            first = cells[0].strip()
            if not re.match(r'^\*{0,2}\d+\*{0,2}$', first):
                continue          # 表头 / 合计行不算
            if not cells[1].strip():       # 「我原本以为」为空 ⇒ 没填
                continue
            U += 1
            if '能力' in cells[3]:
                C += 1
        bad = []
        if U < 3:
            bad.append(f'U={U} < 3')
        if C < 1:
            bad.append(f'C={C} < 1')
        if bad:
            s6 = ('FAIL', f'{", ".join(bad)} —— 这轮没（或没有）拓宽能力边界。'
                         f'⛔ 「把 A 理解反了」不算，要的是「发现了原本不知道存在的东西」')
        else:
            s6 = ('PASS', f'U={U}（红线 3）｜C={C}（红线 1）—— 找到 {U} 个原本不知道存在的东西，'
                         f'其中 {C} 个拓宽了能力边界')

    print(f'\n研究纪要判据机检 —— {path}')
    print(f'解析到 {len(rows)} 条结论\n' + '-' * 62)
    fails = 0
    for name, res in (('S1 独立来源', s1), ('S2 出处完整', s2),
                      ('S3 边际收敛', s3), ('S4 反面样本', s4),
                      ('S5 量化有据', s5), ('S6 探索产出', s6)):
        icon = {'PASS': '✅', 'WARN': '⚠️ ', 'FAIL': '⛔', 'TODO': '🔵'}[res[0]]
        print(f'{icon} {name}: {res[1]}')
        if res[0] == 'FAIL':
            fails += 1
    print('-' * 62)
    print(f'结论：{fails} 项红项 —— ' + ('❌ 未达标，不许据此宣称 research 完成' if fails
                                        else '⚠️ 无红项（WARN 仍需人工处理）'))
    sys.exit(1 if fails else 0)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('用法: python check_journal.py <纪要.md>')
        sys.exit(2)
    main(sys.argv[1])
