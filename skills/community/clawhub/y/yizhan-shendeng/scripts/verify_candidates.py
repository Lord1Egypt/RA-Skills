# -*- coding: utf-8 -*-
"""五路候选跨批全量校验器（一盏神灯流水线通用）

用法：python verify_candidates.py <工作区路径>
例：  python verify_candidates.py /path/to/workdir

做四件事：
1. 五个候选文件（框架/原则/案例/反例/术语）每条「原文摘录」回块逐字比对
   —— 两侧同口径归一化（去 [第N页] + 去全部空白）；只归一化一侧会双向出错
   —— 严格匹配失败时对「跨页摘录」给二次机会：按行剥离 OCR 页眉噪声行
      （页标记行、纯 1-3 位页码行、行首 N.M 小节式页眉行）后重试；
      全半角/字形差异不走这条通道（仍属真差异，修摘录）
2. 摘录三级回退提取：代码围栏 → > 引用块 → 同行（剥外层中文引号）
3. 「原文位置」兼容「第 N 块」「块 N」「第 N-M 块」多种写法
4. 空摘录一律判失败——空串是任何文本的子串，漏判会让整路假全绿

输出每路 ok/bad 计数与失败明细；TOTAL BAD: 0 为全过。
目录兼容：blocks/ 或 原文/；cand/ 或 候选/。
"""
import io
import os
import re
import sys
import glob

BASE = sys.argv[1] if len(sys.argv) > 1 else '.'
BLOCKS_DIR = next((d for d in (os.path.join(BASE, 'blocks'), os.path.join(BASE, '原文'))
                   if os.path.isdir(d)), os.path.join(BASE, 'blocks'))
CAND_DIR = next((d for d in (os.path.join(BASE, 'cand'), os.path.join(BASE, '候选'))
                 if os.path.isdir(d)), os.path.join(BASE, 'cand'))


def norm(s):
    return re.sub(r'\s+', '', re.sub(r'\[第\s*\d+\s*页\]', '', s))


def clean_block(t):
    """按行剥离 OCR 页眉噪声行（页标记行、纯 1-3 位页码行、行首 N.M 小节式页眉行），
    供跨页摘录的二次匹配——严格匹配失败后才使用，全半角/字形差异不走这条通道。"""
    out = []
    for ln in t.split('\n'):
        s = ln.strip()
        if re.match(r'^\[第\s*\d+\s*页\]$', s):
            continue
        if re.match(r'^\d{1,3}$', s):
            continue
        if re.match(r'^\d+\.\d+\S', s):
            continue
        out.append(ln)
    return '\n'.join(out)


blocks = {}
for p in sorted(glob.glob(os.path.join(BLOCKS_DIR, 'block*.txt'))):
    m = re.search(r'block(\d+)', os.path.basename(p))
    if m:
        blocks[int(m.group(1))] = io.open(p, encoding='utf-8').read().replace('\r\n', '\n')
print('blocks loaded:', len(blocks))
blocks_clean = {k: clean_block(v) for k, v in blocks.items()}


def extract_excerpt(p):
    """三级回退提取摘录；返回 None 或字符串（可能为空串，调用方须判空）"""
    m = re.search(r'- 原文摘录[^：]*：\n```(?:text)?\n(.*?)\n```', p, re.S)
    if m:
        return m.group(1)
    m = re.search(r'- 原文摘录[^：]*：\n\s*((?:[ \t]*>.*\n?)+)', p)
    if m:
        lines = [ln.strip().lstrip('>').strip() for ln in m.group(1).strip().split('\n')]
        return '\n'.join(l for l in lines if l)
    m = re.search(r'- 原文摘录[^：]*：(.*)', p)
    if m:
        s = m.group(1).strip()
        if len(s) >= 2 and s[0] in '“"「《' and s[-1] in '”"」》':
            s = s[1:-1]
        return s
    return None


def check(name, title_pat):
    path = os.path.join(CAND_DIR, name + '.md')
    if not os.path.exists(path):
        print('[%s] 文件不存在，跳过' % name)
        return 0
    t = io.open(path, encoding='utf-8').read()
    parts = re.split(r'(?m)^(?=%s)' % title_pat, t)
    ok = bad = 0
    fails = []
    for p in parts[1:]:
        title = p.split('\n')[0].strip()
        if '回执' in title or '候选（' in title:
            continue
        ex = extract_excerpt(p)
        m_loc = re.search(r'- 原文位置：(.+)', p)
        if ex is None or not ex.strip() or not m_loc:
            bad += 1
            fails.append((title[:45], '摘录为空/未识别或位置缺失'))
            continue
        ex = ex.strip()
        if '[第' in ex:
            bad += 1
            fails.append((title[:45], 'PAGE-MARK: ' + ex[:40]))
            continue
        decl = []
        loc = m_loc.group(1)
        for a, b in re.findall(r'第\s*(\d+)(?:[-–](\d+))?\s*块', loc):
            decl.append(int(a))
            if b:
                decl.append(int(b))
        for a in re.findall(r'块\s*(\d+)', loc):
            decl.append(int(a))
        hit = any(
            bn in blocks and (norm(ex) in norm(blocks[bn])
                              or norm(ex) in norm(blocks_clean[bn]))
            for bn in decl)
        if hit:
            ok += 1
        else:
            bad += 1
            fails.append((title[:45], ex[:55]))
    print('[%s] ok=%d bad=%d' % (name, ok, bad))
    for t_, e_ in fails[:10]:
        print('   FAIL:', t_, '|', repr(e_))
    return bad


total = 0
total += check('框架', r'## \d+\. ')
total += check('原则', r'## 原则：')
total += check('案例', r'## 案例：')
total += check('反例', r'## 反例 \d+：')
total += check('术语', r'## 术语：')
print('TOTAL BAD:', total)
sys.exit(1 if total else 0)
