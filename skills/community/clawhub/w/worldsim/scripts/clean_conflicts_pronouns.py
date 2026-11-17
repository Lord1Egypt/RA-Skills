#!/usr/bin/env python3
# 简单清洗 snaps 存档 conflicts.yaml：全局上帝视角代词→人名
# 策略：引号内（「」""）不碰；「他的/她的/他/她」仅在 CT 内性别候选唯一时替换；
#       排除「他们/她们/他人/其他/他日/他乡」等组合；「我/你」不处理（存档简单清洗）。
import re, glob, os, sys

# I/O 纪律（硬性）：本脚本读写一律 UTF-8——Windows 缺省 locale（GBK）读中文 yaml 必炸、
# emoji 写 GBK stdout 必炸；所有 open/read_text/write_text 已显式 encoding，此处兜底 stdout/stderr
for _s in (sys.stdout, sys.stderr):
    try:
        if _s and _s.encoding and _s.encoding.lower().replace("-", "") != "utf8":
            _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

FEMALE = {"Clementine", "Dolores", "Maeve", "Armistice", "Elsie", "Theresa"}
MALE = {"Guest", "Hector", "Teddy", "Peter", "Rebus", "Walter", "Sheriff",
        "Ford", "Bernard", "Arnold", "Felix", "Sylvester", "William",
        "MiB", "The Man in Black", "Ashley", "Stubbs"}
NAMES = FEMALE | MALE

def extract_chars(block):
    chars = set()
    for n in NAMES:
        if n in block:
            chars.add(n)
    return chars

def replace_outside_quotes(text, fn):
    parts = re.split(r'([「」""])', text)
    out, in_q = [], False
    for p in parts:
        if p in ('「', '」', '"', '"'):
            in_q = not in_q
            out.append(p)
        else:
            out.append(fn(p) if not in_q else p)
    return ''.join(out)

def clean_block(text, chars):
    male_cands = sorted(c for c in chars if c in MALE)
    female_cands = sorted(c for c in chars if c in FEMALE)

    def fn(seg):
        if len(male_cands) == 1 and '他的' in seg:
            seg = seg.replace('他的', male_cands[0] + '的')
        if len(female_cands) == 1 and '她的' in seg:
            seg = seg.replace('她的', female_cands[0] + '的')
        if len(male_cands) == 1:
            seg = re.sub(r'(?<!其)他(?!们|人|日|乡|处|方|国|地|位)', male_cands[0], seg)
        if len(female_cands) == 1:
            seg = re.sub(r'她(?!们|人)', female_cands[0], seg)
        return seg
    return replace_outside_quotes(text, fn)

def process(path):
    with open(path, encoding='utf-8') as f:
        text = f.read()
    lines = text.split('\n')
    blocks = []
    start = None
    for i, ln in enumerate(lines):
        if re.match(r'^CT-\d+:', ln):
            if start is not None:
                blocks.append((start, i))
            start = i
    if start is not None:
        blocks.append((start, len(lines)))

    replaced, skipped = 0, 0
    new_lines = list(lines)
    for s, e in blocks:
        block = '\n'.join(lines[s:e])
        chars = extract_chars(block)
        male_cands = sorted(c for c in chars if c in MALE)
        female_cands = sorted(c for c in chars if c in FEMALE)
        # 统计
        for ln in lines[s:e]:
            for m in re.finditer(r'他的|她的|他|她', replace_outside_quotes(ln, lambda x: x)):
                tok = m.group(0)
                if tok == '他的' or tok == '他':
                    if len(male_cands) == 1:
                        replaced += 1
                    else:
                        skipped += 1
                else:
                    if len(female_cands) == 1:
                        replaced += 1
                    else:
                        skipped += 1
        new_block = clean_block(block, chars)
        new_lines[s:e] = new_block.split('\n')
    new_text = '\n'.join(new_lines)
    if new_text != text:
        with open(path, 'w', encoding='utf-8', newline='') as f:
            f.write(new_text)
    return replaced, skipped

if __name__ == '__main__':
    # 世界目录经 _paths 单一事实源收敛（名称校验/链接拦截/越界拒绝）——禁止任意路径参数
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from _paths import resolve_world
    if len(sys.argv) != 2:
        print("用法: clean_conflicts_pronouns.py <世界名>（清洗 {世界}/snaps/*/conflicts.yaml）", file=sys.stderr)
        sys.exit(2)
    snaps = resolve_world(sys.argv[1]) / 'snaps'
    total_r = total_s = 0
    for p in sorted(glob.glob(os.path.join(snaps, '*', 'conflicts.yaml'))):
        r, s = process(p)
        total_r += r; total_s += s
        print(f"{p}: 替换 {r} 处, 跳过 {s} 处")
    print(f"合计: 替换 {total_r}, 跳过 {total_s}")
