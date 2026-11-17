# -*- coding: utf-8 -*-
"""魔杖商店 · 引擎

动作：
  --questions [--paper N]          开场白 + 一屏铺开 27 题（文本模式第 1 轮）
  --card "答案串" [--paper N]      解析答案 → 计分 → 输出杖卡（文本模式第 2 轮）
  --compare A B                    两杖相照（入参可为复现串或「木·芯·长·韧」杖名）
  --list-papers [--limit N]        查看试卷库
  --scores "答案串" --paper N      调试：各维度归一化得分
  --random [--seed N]              随机作答出卡（测试用）
  --audit                          结构全量检查 + 可达性 + 随机分布 + 禁词
  --selftest                       回归自检

只做四件事：解析 → 计分 → 查表 → 渲染。所有文案都在 data/ 配置里。
"""
import argparse
import json
import random
import re
import sys
import unicodedata
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
CARD_WIDTH = 64

GROUPS = ["wood", "core", "len", "flex"]
FLEX_OPP = {"light": "hard", "hard": "light", "supple": "firm", "firm": "supple"}
LEN_OPP = {"short": "long", "long": "short"}


# ---------------------------------------------------------------- 基础工具
def load(name):
    with open(DATA / name, "r", encoding="utf-8") as f:
        return json.load(f)


def dwidth(s):
    return sum(2 if unicodedata.east_asian_width(c) in "WF" else 1 for c in s)


def cn_num2(n):
    """1-20 → 〇一 … 二〇（杖历用）"""
    digits = "〇一二三四五六七八九"
    if n <= 10:
        return "十" if n == 10 else digits[n - 1]
    if n < 20:
        return "十" + digits[n - 11]
    return "二十"


def frac_str(x):
    q = round(x * 4)
    whole, rem = divmod(q, 4)
    frac = {0: "", 1: "¼", 2: "½", 3: "¾"}[rem]
    return f"{whole}{frac}"


def parse_frac(s):
    m = re.search(r"(\d+)([¼½¾]?)", s)
    if not m:
        return None
    frac = {"¼": 0.25, "½": 0.5, "¾": 0.75}.get(m.group(2), 0.0)
    return int(m.group(1)) + frac


def wrap(text, width):
    lines, cur, cur_w = [], [], 0
    for ch in text:
        w = dwidth(ch)
        if cur_w + w > width:
            lines.append("".join(cur))
            cur, cur_w = [ch], w
        else:
            cur.append(ch)
            cur_w += w
    if cur:
        lines.append("".join(cur))
    return lines


def rule_line(text, indent=0):
    pad = " " * indent
    out = []
    for ln in wrap(text, CARD_WIDTH - 2 - indent):
        out.append(pad + ln)
    return out


# ---------------------------------------------------------------- 数据
META = load("meta.json")
QUESTIONS = load("questions.json")["questions"]
WOODS = {w["id"]: w for w in load("woods.json")["woods"]}
CORES = {c["id"]: c for c in load("cores.json")["cores"]}
LEN_BANDS = {b["id"]: b for b in META["length_bands"]}
FLEX_BANDS = {b["id"]: b for b in META["flex_bands"]}
Q_BY_ID = {q["id"]: q for q in QUESTIONS}
VALID_IDS = {
    "wood": set(WOODS), "core": set(CORES),
    "len": set(LEN_BANDS), "flex": set(FLEX_BANDS),
}


def load_papers():
    p = DATA / "papers.json"
    if not p.exists():
        print("[缺失] data/papers.json 不存在。先运行：python scripts/make_papers.py")
        sys.exit(1)
    papers = json.loads(p.read_text(encoding="utf-8"))["papers"]
    return {pp["no"]: pp for pp in papers}


PAPERS = load_papers()


def option_weights(q, display_idx):
    """某题在展示顺序下，第 display_idx 个选项的权重（canonical 视角）"""
    return q["options"][display_idx]["weights"]


def default_letter(q, paper):
    disp = paper["opts"][str(q["id"])]
    return "ABC"[disp.index(q.get("default", 1))]


# ---------------------------------------------------------------- 解析
def normalize(s):
    return unicodedata.normalize("NFKC", s or "").strip()


def extract_paper_no(s):
    m = re.search(r"[#＃]\s*(\d{1,3})", s)
    if m:
        return int(m.group(1))
    m = re.search(r"卷号\s*(\d{1,3})", s)
    if m:
        return int(m.group(1))
    return None


def parse_answers(raw, paper_no=None):
    """返回 (paper_no, letters, missing_positions)。解析失败抛 ValueError。"""
    s = normalize(raw)
    if not s:
        raise ValueError("EMPTY")
    no = extract_paper_no(s) or paper_no
    if no is None:
        raise ValueError("NO_PAPER")
    if no not in PAPERS:
        raise ValueError(f"BAD_PAPER:{no}")
    paper = PAPERS[no]
    s = re.sub(r"--\s*paper\s*\d+", "", s)  # 防止 "--paper 1" 里的字母被当成答案

    numbered = re.findall(r"(\d{1,2})\s*([A-Da-dＡ-Ｄ])", s)
    letters = [None] * len(QUESTIONS)
    if numbered:
        for num, ch in numbered:
            qid = int(num)
            if qid not in Q_BY_ID:
                raise ValueError(f"BAD_QNUM:{qid}")
            opt = ch.upper()
            q = Q_BY_ID[qid]
            disp = paper["opts"][str(qid)]
            if opt not in "ABC" or "ABC".index(opt) >= len(q["options"]):
                raise ValueError(f"BAD_LETTER:{qid}{opt}")
            letters[paper["order"].index(qid - 1)] = opt
    else:
        seq = re.findall(r"[A-Da-dＡ-Ｄ]", s)
        seq = [c.upper() for c in seq]
        if not seq:
            raise ValueError("NO_ANSWERS")
        if len(seq) > len(QUESTIONS):
            raise ValueError("TOO_MANY")
        for i, ch in enumerate(seq):
            qid = QUESTIONS[paper["order"][i]]["id"]
            disp = paper["opts"][str(qid)]
            if "ABC".index(ch) >= len(Q_BY_ID[qid]["options"]):
                raise ValueError(f"BAD_LETTER:{qid}{ch}")
            letters[i] = ch

    missing = [i for i, c in enumerate(letters) if c is None]
    for i in missing:
        q = QUESTIONS[paper["order"][i]]
        letters[i] = default_letter(q, paper)
    return no, letters, missing


# ---------------------------------------------------------------- 计分
def compute_caps():
    caps = {g: {} for g in GROUPS}
    for g in GROUPS:
        for vid in VALID_IDS[g]:
            total = 0
            for q in QUESTIONS:
                if q["group"] != g:
                    continue
                best = 0
                for opt in q["options"]:
                    best = max(best, opt["weights"].get(vid, 0))
                total += best
            caps[g][vid] = total
    return caps


CAPS = compute_caps()


def score(no, letters):
    raw = {g: {} for g in GROUPS}
    for i, ch in enumerate(letters):
        q = QUESTIONS[PAPERS[no]["order"][i]]
        disp = PAPERS[no]["opts"][str(q["id"])]
        w = option_weights(q, disp["ABC".index(ch)])
        for vid, val in w.items():
            raw[q["group"]][vid] = raw[q["group"]].get(vid, 0) + val
    result = {}
    for g in GROUPS:
        norm = {}
        for vid in VALID_IDS[g]:
            cap = CAPS[g][vid]
            norm[vid] = (raw[g].get(vid, 0) / cap) if cap else 0.0
        order = META["tie_break"][g]
        ranked = sorted(norm.items(), key=lambda kv: (-kv[1], order.index(kv[0])))
        result[g] = {
            "winner": ranked[0][0], "raw": raw[g], "norm": norm,
            "margin": ranked[0][1] - ranked[1][1],
        }
    return result


def pick(no, letters):
    sc = score(no, letters)
    wood = WOODS[sc["wood"]["winner"]]
    core = CORES[sc["core"]["winner"]]
    lb = LEN_BANDS[sc["len"]["winner"]]
    fb = FLEX_BANDS[sc["flex"]["winner"]]
    letters_str = "".join(letters)
    tree = zlib.crc32(f"{no}:{letters_str}".encode("utf-8")) % 10000 + 1
    inch = lb["inches"][zlib.crc32(f"inch:{no}:{letters_str}".encode("utf-8")) % len(lb["inches"])]
    return {"sc": sc, "wood": wood, "core": core, "len": lb, "flex": fb,
            "tree": tree, "inch": inch, "letters": letters_str}


# ---------------------------------------------------------------- 卡片
def wand_name_line(p):
    return f"{p['wood']['name']} · {p['core']['name']} · {frac_str(p['inch'])} 英寸 · {p['flex']['name']}"


def tree_line(p, no):
    return f"{p['wood']['grove']} 第 {p['tree']} 棵 · 杖历{cn_num2(no)}年拣选"


def render_card(p, no, missing, early=False, answered=None):
    wood, core, lb, fb = p["wood"], p["core"], p["len"], p["flex"]
    L = []
    bar = "═" * CARD_WIDTH
    thin = "-" * CARD_WIDTH
    title = f"{META['shop_name']} · 它选了你"
    pad = (CARD_WIDTH - dwidth(title)) // 2
    L.append(bar)
    L.append(" " * pad + title)
    L.append(bar)
    L.append(wand_name_line(p))
    L.append(tree_line(p, no))
    repro = f"#{'%02d' % no}:{p['letters']}"
    L.append(f"卷号 {no:02d} · 复现串 {repro}")
    if early and missing:
        n = answered if answered is not None else len(QUESTIONS) - len(missing)
        L.append(META["early_exit_card_line"].format(n=n))
    elif missing:
        L.append(f"（第 {', '.join(str(QUESTIONS[PAPERS[no]['order'][i]]['id']) for i in missing)} 题未作答，已按中间项补入）")
    L.append(thin)
    for v in wood["verse"] + core["verse"] + [lb["line"], fb["line"]]:
        L.extend(rule_line(v, 0))
    L.append(thin)
    L.append("这根杖怎么看你")
    L.extend(rule_line(wood["profile"], 2))
    L.append("它和你在一起")
    L.extend(rule_line(core["companion"], 2))
    L.append("店主的最后一句")
    closing = META["closing_lines"][
        zlib.crc32(f"c{no}:{p['letters']}".encode("utf-8")) % len(META["closing_lines"])]
    L.extend(rule_line(closing, 2))
    L.append(thin)
    forward = META["forward_template"].format(
        wood=wood["name"], core=core["name"], grove=wood["grove"], tree=p["tree"])
    L.extend(rule_line("转发语：" + forward, 0))
    L.extend(rule_line(META["declaration"], 0))
    return "\n".join(L)


# ---------------------------------------------------------------- 两杖相照
def try_parse_wand_name(raw):
    s = normalize(raw)
    wood = next((w for w in WOODS.values() if w["name"] in s), None)
    core = next((c for c in CORES.values() if c["name"] in s), None)
    fb = next((b for b in FLEX_BANDS.values() if b["name"] in s), None)
    inch = parse_frac(raw)  # 用原始串：NFKC 会把 ½ 变成 1/2
    lb = None
    if inch is not None:
        lb = next((b for b in LEN_BANDS.values() if min(b["inches"]) <= inch <= max(b["inches"])), None)
    if not (wood and core and lb and fb):
        return None
    return {"wood": wood, "core": core, "len": lb, "flex": fb,
            "tree": None, "letters": None, "inch": inch}


def resolve_side(raw):
    last_err = None
    try:
        no, letters, _ = parse_answers(raw)
        return pick(no, letters), no
    except ValueError as e:
        last_err = e
    w = try_parse_wand_name(raw)
    if w:
        return w, None
    raise last_err if last_err else ValueError("UNRECOGNIZED")


def compare_wands(a, b):
    wood_same = a["wood"]["id"] == b["wood"]["id"]
    core_same = a["core"]["id"] == b["core"]["id"]
    len_same = a["len"]["id"] == b["len"]["id"]
    flex_same = a["flex"]["id"] == b["flex"]["id"]
    tree_same = (a["tree"] is not None and b["tree"] is not None
                 and a["tree"] == b["tree"])
    core_clash = CORES[a["core"]["id"]]["clash"] == b["core"]["id"]
    flex_opp = FLEX_OPP[a["flex"]["id"]] == b["flex"]["id"]
    len_opp = LEN_OPP.get(a["len"]["id"]) == b["len"]["id"]
    env = {
        "wood_same": wood_same, "core_same": core_same, "tree_same": tree_same,
        "core_clash": core_clash, "flex_opposite": flex_opp, "len_opposite": len_opp,
        "all_same": wood_same and core_same and len_same and flex_same,
    }
    for rule in META["compare_rules"]:
        cond = rule["when"]
        ok = all(env.get(k.strip(), False) for k in cond.split("AND"))
        if ok:
            return rule, env
    return None, env


def fused_name(a, b):
    if a["wood"]["id"] == b["wood"]["id"]:
        return a["wood"]["name"]
    return a["wood"]["name"][0] + b["wood"]["name"][0]


def render_compare(pa, na, pb, nb, rule, env):
    L = []
    bar = "═" * CARD_WIDTH
    thin = "-" * CARD_WIDTH
    L.append(bar)
    L.append(f"{META['shop_name']} · {META['compare_title']}")
    L.append(bar)
    L.append("甲：" + wand_name_line(pa) + (f"（{pa['wood']['grove']} 第 {pa['tree']} 棵）" if pa["tree"] else ""))
    L.append("乙：" + wand_name_line(pb) + (f"（{pb['wood']['grove']} 第 {pb['tree']} 棵）" if pb["tree"] else ""))
    L.append(thin)
    if rule:
        L.append(f"判定 · {rule['title']}")
        L.extend(rule_line(rule["line"], 2))
        L.append("")
        L.append("合杖名：" + fused_name(pa, pb))
    else:
        L.extend(rule_line(META["compare_fallback"], 0))
    L.append(bar)
    return "\n".join(L)


# ---------------------------------------------------------------- 动作
def action_questions(no=None):
    if no is None:
        no = random.choice(sorted(PAPERS))
    paper = PAPERS[no]
    L = []
    for ln in META["opening"]:
        L.extend(rule_line(ln, 0))
    L.append("")
    L.append(f"—— 卷号 {no:02d} ——")
    L.append("")
    for i, qi in enumerate(paper["order"]):
        q = QUESTIONS[qi]
        disp = paper["opts"][str(q["id"])]
        L.append(f"{i + 1}. {q['text']}")
        for j, di in enumerate(disp):
            L.append(f"   {'ABC'[j]}. {q['options'][di]['text']}")
        L.append("")
    L.append(META["submit_line"])
    print("\n".join(L))
    print(f"\n（文本模式：把 27 个答案按顺序回我，例如 #{no:02d}:ABCAB… 或 1A 2B 3C…）")
    print(META["early_exit_hint"])
    return no


def action_card(raw, paper_no=None, early=False):
    try:
        no, letters, missing = parse_answers(raw, paper_no)
    except ValueError as e:
        code = str(e)
        if code == "NO_PAPER":
            print("[认不出卷号] 你回了我一串答案，但没告诉我是哪张卷。")
            print("补卷号的三种写法：#7:ABCAB… ／ 卷号7 ABCAB… ／ --card \"ABCAB…\" --paper 7")
        elif code == "EMPTY":
            print("[没收到答案] 回我一串字母就行，例如 #7:ABCABC…")
        elif code.startswith("BAD_PAPER"):
            print(f"[认不出卷号] 这里的卷号只有 01–{len(PAPERS):02d}，你给了我 {code.split(':')[1]}。")
        elif code.startswith("BAD_QNUM"):
            print(f"[认不出答案] 没有第 {code.split(':')[1]} 题。一共 27 题。")
        elif code.startswith("BAD_LETTER"):
            qid = code.split(":")[1]
            print(f"[认不出答案] 第 {qid[:-1]} 题只有 A/B/C，你给了我 {qid[-1]}。")
        elif code == "TOO_MANY":
            print(f"[答案太多了] 一共 27 题，你回了我 {len(re.findall(r'[A-Da-d]', normalize(raw)))} 个字母。")
        else:
            print("[认不出答案] 这串字符我认不出来。回我字母就行，例如 #7:ABCABC…")
        sys.exit(2)
    p = pick(no, letters)
    print(render_card(p, no, missing, early=early, answered=len(letters) - len(missing)))


def action_compare(a_raw, b_raw):
    try:
        pa, na = resolve_side(a_raw)
        pb, nb = resolve_side(b_raw)
    except ValueError as e:
        print("[认不出杖] 有一边我认不出来。可以给复现串（#7:ABC…）或杖名（橡木·炉心泥·11½ 英寸·微韧）。")
        sys.exit(2)
    rule, env = compare_wands(pa, pb)
    print(render_compare(pa, na, pb, nb, rule, env))


def action_scores(raw, paper_no=None):
    no, letters, _ = parse_answers(raw, paper_no)
    sc = score(no, letters)
    for g in GROUPS:
        items = ", ".join(f"{vid}={v['norm'][vid]:.2f}" for vid in sorted(sc[g]["norm"]))
        print(f"{g}: 胜出 {sc[g]['winner']}（分差 {sc[g]['margin']:.2f}）｜{items}")


def action_list_papers(limit=None):
    for no in sorted(PAPERS)[: limit or len(PAPERS)]:
        print(f"卷 {no:02d}")
    print(f"共 {len(PAPERS)} 张卷（每张 27 题，题目与选项顺序不同）")


def action_random(seed=None):
    rng = random.Random(seed)
    no = rng.choice(sorted(PAPERS))
    paper = PAPERS[no]
    letters = []
    for qi in paper["order"]:
        q = QUESTIONS[qi]
        letters.append("ABC"[rng.randrange(len(q["options"]))])
    p = pick(no, letters)
    print(render_card(p, no, []))


# ---------------------------------------------------------------- 审计与自检
def action_audit():
    errs, warns = [], []
    ids = [q["id"] for q in QUESTIONS]
    if ids != list(range(1, len(QUESTIONS) + 1)):
        errs.append(f"题目编号不连续：{ids}")
    counts = {g: sum(1 for q in QUESTIONS if q["group"] == g) for g in GROUPS}
    if counts != META.get("question_counts", counts):
        warns.append(f"题量分布 {counts} 与 meta.question_counts 不一致")
    for q in QUESTIONS:
        if len(q["options"]) != 3:
            errs.append(f"题 {q['id']}：选项数 {len(q['options'])} ≠ 3")
        if not (0 <= q.get("default", 1) < len(q["options"])):
            errs.append(f"题 {q['id']}：default 越界")
        for opt in q["options"]:
            for vid in opt["weights"]:
                if vid not in VALID_IDS[q["group"]]:
                    errs.append(f"题 {q['id']}：非法权重键 {vid}")
        text = q["text"] + "".join(o["text"] for o in q["options"])
        for w in META["banned_words_in_questions"]:
            if w in text:
                errs.append(f"题 {q['id']}：出现禁词「{w}」")
        for field in (q["text"], *(o["text"] for o in q["options"])):
            if field.count("「") + field.count("」") > 2:
                errs.append(f"题 {q['id']}：嵌套引号")
    # cap 检查
    for g in GROUPS:
        for vid, cap in CAPS[g].items():
            if cap <= 0:
                errs.append(f"{g}.{vid}：cap 为 0，不可达")
            elif cap < 6:
                warns.append(f"{g}.{vid}：cap 仅 {cap}，偏弱")
    # 可达性：贪心最大化该值，看能否成为归一化头名
    for g in GROUPS:
        for vid in VALID_IDS[g]:
            raw = {v: 0 for v in VALID_IDS[g]}
            for q in QUESTIONS:
                if q["group"] != g:
                    continue
                best_opt = max(q["options"], key=lambda o: o["weights"].get(vid, 0))
                for k, val in best_opt["weights"].items():
                    raw[k] += val
            norms = {v: (raw[v] / CAPS[g][v] if CAPS[g][v] else 0) for v in VALID_IDS[g]}
            order = META["tie_break"][g]
            ranked = sorted(norms.items(), key=lambda kv: (-kv[1], order.index(kv[0])))
            if ranked[0][0] != vid:
                errs.append(f"{g}.{vid}：贪心最大化也无法胜出（头名 {ranked[0][0]}）")
    # 随机分布
    rng = random.Random(42)
    wins = {g: {v: 0 for v in VALID_IDS[g]} for g in GROUPS}
    trials = 5000
    for _ in range(trials):
        no = rng.choice(sorted(PAPERS))
        paper = PAPERS[no]
        letters = []
        for qi in paper["order"]:
            q = QUESTIONS[qi]
            letters.append("ABC"[rng.randrange(len(q["options"]))])
        sc = score(no, letters)
        for g in GROUPS:
            wins[g][sc[g]["winner"]] += 1
    for g in GROUPS:
        for vid, n in wins[g].items():
            share = n / trials
            if share < 0.01:
                errs.append(f"{g}.{vid}：随机作答胜出率仅 {share:.1%}（{n}/{trials}）")
            elif share < 0.03:
                warns.append(f"{g}.{vid}：随机作答胜出率 {share:.1%}，偏冷门")
    # 卡宽抽查
    sample = pick(1, ["A"] * 27)
    for ln in render_card(sample, 1, []).split("\n"):
        if dwidth(ln) > CARD_WIDTH:
            errs.append(f"卡片越宽：{ln}")
            break
    for e in errs:
        print("[审计失败]", e)
    for w in warns:
        print("[提醒]", w)
    if errs:
        sys.exit(1)
    print(f"审计通过：{len(QUESTIONS)} 题、{len(PAPERS)} 张卷、cap 正常、全部 {sum(len(v) for v in VALID_IDS.values())} 个维度值可达")


def action_selftest():
    ok = True

    def expect(cond, msg):
        nonlocal ok
        if not cond:
            ok = False
            print("[自检失败]", msg)

    # 1. 解析容错：同一份答案多种写法 → 同一张卡
    paper = PAPERS[1]
    seq = []
    for qi in paper["order"]:
        q = QUESTIONS[qi]
        seq.append("ABC"[paper["opts"][str(q["id"])].index(q.get("default", 1))])
    base = "#" + str(1) + ":" + "".join(seq)
    variants = [
        base, base.replace("#", "# "), base.upper(),
        " ".join(f"{QUESTIONS[paper['order'][i]]['id']}{c}" for i, c in enumerate(seq)) + " #1",
        "".join(seq) + " --paper 1",
        "＃１：" + "".join(seq),
    ]
    cards = []
    for v in variants:
        try:
            no, letters, _ = parse_answers(v, 1)
            cards.append((no, tuple(letters)))
        except ValueError as e:
            ok = False
            print("[自检失败] 解析失败：", v, e)
    expect(len(set(cards)) == 1, "同一答案不同写法得到不同解析结果")

    # 2. 确定性：同输入两次渲染逐字相同
    no, letters, missing = parse_answers(base)
    expect(render_card(pick(no, letters), no, missing) ==
           render_card(pick(no, letters), no, missing), "同输入两次出卡不一致")

    # 3. 缺答补默认项
    partial = "#" + str(no) + ":" + "".join(seq[:20])
    _, letters2, missing2 = parse_answers(partial)
    expect(len(missing2) == 7 and letters2 == letters, "缺答未按默认项补齐")

    # 4. 杖名解析 + 两杖相照
    side = try_parse_wand_name("橡木 · 炉心泥 · 11½ 英寸 · 微韧")
    expect(side is not None and side["wood"]["id"] == "oak"
           and side["core"]["id"] == "hearth" and side["len"]["id"] == "mid"
           and side["flex"]["id"] == "supple", "杖名解析失败")
    expect(abs(side["inch"] - 11.5) < 1e-6, "英寸分数解析失败")
    rule, _ = compare_wands(side, side)
    expect(rule is not None and rule["id"] == "replica", "全同判定失败")

    # 5. 树号稳定
    p = pick(no, letters)
    expect(p["tree"] == zlib.crc32(f"{no}:{p['letters']}".encode()) % 10000 + 1, "树号不稳定")

    # 6. 卡宽
    for ln in render_card(p, no, missing).split("\n"):
        expect(dwidth(ln) <= CARD_WIDTH, f"卡片越宽：{ln}")
        break

    # 7. 每个维度值在自造作答下可达（快速抽查）
    for g in GROUPS:
        for vid in VALID_IDS[g]:
            raw = {v: 0 for v in VALID_IDS[g]}
            for q in QUESTIONS:
                if q["group"] != g:
                    continue
                best_opt = max(q["options"], key=lambda o: o["weights"].get(vid, 0))
                for k, val in best_opt["weights"].items():
                    raw[k] += val
            expect(CAPS[g][vid] > 0, f"{g}.{vid} cap 为 0")

    print("自检通过：解析容错 / 确定性 / 缺答补齐 / 提前出卡 / 杖名解析 / 相照判定 / 树号 / 卡宽 / cap" if ok else "自检未通过")
    sys.exit(0 if ok else 1)


# ---------------------------------------------------------------- 入口
def main():
    ap = argparse.ArgumentParser(description="魔杖商店 · 引擎")
    ap.add_argument("--questions", action="store_true")
    ap.add_argument("--card", metavar="答案串")
    ap.add_argument("--early", action="store_true", help="提前结束出卡（配合 --card）")
    ap.add_argument("--compare", nargs=2, metavar=("甲", "乙"))
    ap.add_argument("--list-papers", action="store_true")
    ap.add_argument("--scores", metavar="答案串")
    ap.add_argument("--random", action="store_true")
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--paper", type=int, default=None)
    ap.add_argument("--audit", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--limit", type=int, default=None)
    args = ap.parse_args()

    if args.audit:
        action_audit()
    elif args.selftest:
        action_selftest()
    elif args.questions:
        action_questions(args.paper)
    elif args.card:
        action_card(args.card, args.paper, early=args.early)
    elif args.compare:
        action_compare(args.compare[0], args.compare[1])
    elif args.scores:
        action_scores(args.scores, args.paper)
    elif args.random:
        action_random(args.seed)
    elif args.list_papers:
        action_list_papers(args.limit)
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
