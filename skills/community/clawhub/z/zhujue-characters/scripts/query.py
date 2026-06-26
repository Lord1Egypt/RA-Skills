# -*- coding: utf-8 -*-
"""
《主角》人物 → 相关章节 查询/导入工具。

依赖 data/characters.json、data/chapters.json（由 build_index.py 生成）。

用法：
  python3 query.py 忆秦娥 胡三元          # 解析人名 → 列出相关章节(交集优先) + 计数 + 建议
  python3 query.py 楚嘉禾                  # 单人 → 其全部出现章节
  python3 query.py 忆秦娥 --part 上部       # 仅某一部
  python3 query.py 忆秦娥 封潇潇 --all      # 仅二人「同时出现」的章节(交集)
  python3 query.py 忆秦娥 石怀玉 --any      # 任一人出现的章节(并集)
  python3 query.py 楚嘉禾 --text           # 直接输出相关章节纯文本(供导入为背景)
  python3 query.py 忆秦娥 --part 下部 --text --out /tmp/bg.txt   # 文本写入文件
  python3 query.py --list                  # 列出全部可检索人物及别名
  python3 query.py --resolve 青娥          # 仅做名字解析，看匹配到谁

退出码：0 正常；2 没解析到人物 / 没匹配章节。
"""
import re, os, sys, json, argparse

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
DATA = os.path.join(SKILL, "data")
BIG = 25  # 章节数超过此值视为"过大集合"，提示收窄

def resolve_txt_dir(stored=None):
    """优先环境变量；其次 skill 自带 txt/（自包含）；最后用索引里记录的路径。"""
    env = os.environ.get("ZHUJUE_TXT")
    if env:
        return env
    bundled = os.path.join(SKILL, "txt")
    if os.path.isdir(bundled):
        return bundled
    return stored or "/home/jjw/zj/txt"

def load():
    cj = os.path.join(DATA, "characters.json")
    pj = os.path.join(DATA, "chapters.json")
    if not (os.path.exists(cj) and os.path.exists(pj)):
        sys.exit("缺少索引文件，请先运行：python3 scripts/build_index.py")
    db = json.load(open(cj, encoding="utf-8"))
    return resolve_txt_dir(db.get("txt_dir")), db["characters"], json.load(open(pj, encoding="utf-8"))

# --------------------------------------------------------- 名字解析
def resolve(query, chars):
    """返回 (matched_records, note)。支持精确/别名/双向子串模糊匹配。"""
    q = query.strip()
    names = lambda c: [c["name"]] + c.get("aka", [])
    # 1) 精确（名或别名）
    exact = [c for c in chars if q in names(c)]
    if exact:
        return exact, "精确"
    # 2) 双向子串：查询是某名/别名的子串，或某名/别名是查询的子串
    fuzzy = [c for c in chars if any(q in n or n in q for n in names(c))]
    if fuzzy:
        return fuzzy, "模糊"
    return [], "无"

def part_ok(label, part):
    return part is None or label.startswith(part)

# --------------------------------------------------------- 文本清洗（按需）
def clean_html(path):
    t = open(path, encoding="utf-8").read()
    t = re.sub(r"(?is)<head.*?</head>", "", t)
    t = re.sub(r"(?is)<[^>]+>", "", t)
    t = (t.replace("&nbsp;", " ").replace("&amp;", "&")
           .replace("&lt;", "<").replace("&gt;", ">").replace("&#160;", " "))
    t = re.sub(r"[ \t]+", " ", t)
    t = re.sub(r"\n\s*\n+", "\n", t)
    return t.strip()

# --------------------------------------------------------- 主逻辑
def main():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("names", nargs="*", help="一个或多个人物名（可用别名/简称）")
    ap.add_argument("--all", action="store_true", help="多人时取交集（同时出现）")
    ap.add_argument("--any", action="store_true", help="多人时取并集（任一出现）")
    ap.add_argument("--part", choices=["上部", "中部", "下部", "后记"], help="限定某一部")
    ap.add_argument("--text", action="store_true", help="输出所选章节的纯文本")
    ap.add_argument("--out", help="把 --text 写入文件而非 stdout")
    ap.add_argument("--max", type=int, default=15, help="--text 最多导出章节数（默认 15）")
    ap.add_argument("--list", action="store_true", help="列出全部可检索人物")
    ap.add_argument("--resolve", metavar="名字", help="仅解析名字")
    args = ap.parse_args()

    txt_dir, chars, chapters = load()

    if args.list:
        for cat in ["主要人物", "次要人物", "戏曲角色"]:
            print(f"\n【{cat}】")
            for c in [x for x in chars if x["cat"] == cat]:
                aka = f"  (别名: {'、'.join(c['aka'])})" if c["aka"] else ""
                print(f"  {c['name']}（{c['chapter_count']}章）{aka}")
        return

    if args.resolve:
        recs, how = resolve(args.resolve, chars)
        if not recs:
            print(f"未匹配到人物：{args.resolve}"); sys.exit(2)
        print(f"'{args.resolve}' [{how}匹配] → " + "、".join(r["name"] for r in recs))
        return

    if not args.names:
        ap.print_help(); sys.exit(2)

    # 解析每个查询名
    resolved, unresolved = [], []
    for q in args.names:
        recs, how = resolve(q, chars)
        if recs:
            for r in recs:
                if r not in resolved:
                    resolved.append(r)
        else:
            unresolved.append(q)
    if unresolved:
        print("⚠ 未解析到：" + "、".join(unresolved))
    if not resolved:
        print("没有解析到任何人物。用 --list 查看可检索人物，或 --resolve <名字> 调试。"); sys.exit(2)

    print("解析到人物：" + "、".join(f"{r['name']}({r['chapter_count']}章)" for r in resolved))

    # 各人物章节集合（受 --part 过滤）
    def chset(rec):
        return {ch["file"] for ch in rec["chapters"] if part_ok(ch["label"], args.part)}
    sets = {r["name"]: chset(r) for r in resolved}
    union = set().union(*sets.values()) if sets else set()
    inter = set.intersection(*sets.values()) if len(sets) > 1 else union

    # 选定导入集合
    if len(resolved) == 1:
        chosen, mode = union, "单人全部章节"
    elif args.any:
        chosen, mode = union, "并集（任一出现）"
    elif args.all:
        chosen, mode = inter, "交集（同时出现）"
    else:  # 默认：交集非空用交集，否则退回并集
        if inter:
            chosen, mode = inter, "交集（同时出现，默认）"
        else:
            chosen, mode = union, "并集（无共同章节，退回任一出现）"

    label_of = {f: chapters[f]["label"] for f in chapters}
    def fmt(files):
        return sorted(files, key=lambda f: chapters[f]["idx"])

    if args.part:
        print(f"（已限定：{args.part}）")
    if len(resolved) > 1:
        print(f"并集 {len(union)} 章；交集 {len(inter)} 章。")
    print(f"\n采用【{mode}】，共 {len(chosen)} 章：")
    if not chosen:
        print("（无匹配章节）"); sys.exit(2)
    files = fmt(chosen)
    for f in files:
        print(f"  {label_of[f]:<8} {os.path.join(txt_dir, f)}")

    # 护栏：集合过大
    if not args.text and len(chosen) > BIG:
        print(f"\n⚠ 命中 {len(chosen)} 章，偏多。建议收窄后再导入正文：")
        print("   · 与另一人物共现：  query.py 忆秦娥 楚嘉禾 --all")
        print("   · 限定某一部：      query.py 忆秦娥 --part 上部")
        print("   · 直接按需读取上面列出的少数关键章节文件")

    # 文本导出
    if args.text:
        if len(files) > args.max:
            print(f"\n⚠ {len(files)} 章超过 --max {args.max}，仅导出前 {args.max} 章；"
                  f"如需全部加 --max {len(files)} 或先收窄。")
            files = files[:args.max]
        buf = []
        for f in files:
            buf.append(f"\n\n===== 《主角》{label_of[f]} （{f}）=====\n")
            buf.append(clean_html(os.path.join(txt_dir, f)))
        out = "".join(buf)
        if args.out:
            open(args.out, "w", encoding="utf-8").write(out)
            print(f"\n✓ 已写入 {args.out}（{len(files)} 章，约 {len(out)} 字）")
        else:
            sys.stdout.write(out)

if __name__ == "__main__":
    main()
