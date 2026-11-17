#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""分院帽 Skill 执行脚本。

职责边界（严格四件事）：解析 -> 计分 -> 查表 -> 渲染。
所有面向用户的文案来自 data/houses.json（或 --config 指定的替代配置），
本脚本内不含任何可直接展示给用户的判词、评语或祝福语。

关于「卷」：
  data/questions.json 是**题库**（33 道岔路），data/papers.json 是**试卷库**（33 张卷）。
  每张卷从题库里抽 11 道不重复的题，题目顺序与选项顺序都已打乱并固化在 papers.json 里。
  运行期不做任何随机——同一份答案 + 同一张卷，永远得到同一张卡、同一个编号。
  卷号因此必须跟着卡片走：它是复现的唯一钥匙。
"""

import argparse
import io
import json
import os
import random
import re
import sys
import unicodedata
import zlib

EXIT_OK = 0
EXIT_CONFIG = 1
EXIT_PARSE = 2
EXIT_USAGE = 3

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA_DIR = os.path.join(ROOT, "data")

DEFAULT_HOUSES = os.path.join(DATA_DIR, "houses.json")
DEFAULT_QUESTIONS = os.path.join(DATA_DIR, "questions.json")
DEFAULT_PAPERS = os.path.join(DATA_DIR, "papers.json")
DEFAULT_GLOSSARY = os.path.join(DATA_DIR, "glossary.json")
ALT_HOUSES = os.path.join(DATA_DIR, "houses.alt.json")
ALT_GLOSSARY = os.path.join(DATA_DIR, "glossary.alt.json")

HOUSE_ORDER = ["gryffindor", "slytherin", "ravenclaw", "hufflepuff"]

# 仅用于"解析"的别名表：让用户写学院名、写 A/B/C/D、写简称都能被认出来。
# 别名属于解析容错逻辑，不属于面向用户的文案。
HOUSE_ALIASES = {
    "gryffindor": ["格兰芬多", "格兰芬", "狮院", "焰炉堂", "焰炉"],
    "slytherin": ["斯莱特林", "斯莱特", "蛇院", "深流堂", "深流"],
    "ravenclaw": ["拉文克劳", "拉文克", "鹰院", "高风堂", "高风"],
    "hufflepuff": ["赫奇帕奇", "赫奇", "獾院", "沃土堂", "沃土"],
}

ABSTAIN_WORDS = ["随便", "你定", "都行", "都可以", "听你的", "随意", "看你", "不知道", "无所谓",
                 "帮我分", "你来定", "你决定", "你看着办", "你说了算", "随你", "依你"]

FULLWIDTH_MAP = str.maketrans(
    "ＡＢＣＤａｂｃｄ０１２３４５６７８９．，、　",
    "ABCDabcd0123456789.,, ",
)

PAPER_PREFIX = re.compile(r"^[#＃]\s*(\d{1,3})\b[\s:：,，、·-]*")


def out(text):
    sys.stdout.write(text if text.endswith("\n") else text + "\n")


def err(text):
    sys.stderr.write(text if text.endswith("\n") else text + "\n")


def setup_stdout():
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def dwidth(text):
    """返回终端显示宽度（CJK 全角按 2 计）。"""
    width = 0
    for ch in text:
        if unicodedata.combining(ch):
            continue
        width += 2 if unicodedata.east_asian_width(ch) in ("W", "F") else 1
    return width


def pad(text, width, align="left"):
    gap = max(0, width - dwidth(text))
    if align == "right":
        return " " * gap + text
    if align == "center":
        left = gap // 2
        return " " * left + text + " " * (gap - left)
    return text + " " * gap


def wrap(text, limit):
    """按显示宽度折行，中文按字断行。"""
    lines, cur = [], ""
    for ch in text:
        if dwidth(cur + ch) > limit and cur:
            lines.append(cur)
            cur = ch
        else:
            cur += ch
    if cur:
        lines.append(cur)
    return lines


def load_json(path, what="配置"):
    if not os.path.exists(path):
        err("[配置缺失] 找不到%s文件：%s" % (what, path))
        sys.exit(EXIT_CONFIG)
    try:
        with io.open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except ValueError as exc:
        err("[配置损坏] %s 不是合法 JSON：%s" % (path, exc))
        sys.exit(EXIT_CONFIG)


def resolve_papers_path(args):
    if args.papers_file:
        return args.papers_file
    meta_guess = None
    try:
        meta_guess = load_json(args.questions_file)["meta"].get("papers_file")
    except SystemExit:
        raise
    except Exception:
        meta_guess = None
    if meta_guess:
        return os.path.join(os.path.dirname(os.path.abspath(args.questions_file)), meta_guess)
    return DEFAULT_PAPERS


def resolve_glossary_path(args):
    """词典是可选的：找不到就不标注，不因为缺词典让整条链路挂掉。"""
    explicit = getattr(args, "glossary", None)
    if explicit:
        return explicit if os.path.exists(explicit) else None
    if args.config == "alt":
        return ALT_GLOSSARY if os.path.exists(ALT_GLOSSARY) else None
    return DEFAULT_GLOSSARY if os.path.exists(DEFAULT_GLOSSARY) else None


def load_configs(args):
    houses_path = args.houses
    if args.config == "alt":
        houses_path = ALT_HOUSES
    elif args.config and args.config not in ("canon", "main"):
        houses_path = args.config
    houses = load_json(houses_path, "house")
    questions = load_json(args.questions_file, "题库")
    papers = load_json(resolve_papers_path(args), "试卷")
    glossary_path = resolve_glossary_path(args)
    glossary = load_json(glossary_path, "词典") if glossary_path else None
    return houses, questions, papers, houses_path, glossary


def normalize_input(raw):
    text = raw.translate(FULLWIDTH_MAP)
    text = text.replace("（", " ").replace("）", " ")
    return text.strip()


def detect_house(text):
    """从一段文本里找出用户点名的学院；返回 house key 或 None。"""
    for house, names in HOUSE_ALIASES.items():
        for name in names:
            if name in text:
                return house
    return None


def detect_abstain(text):
    return any(word in text for word in ABSTAIN_WORDS)


def split_paper_prefix(raw):
    """从答案串里剥掉可选的卷号前缀（#7 / ＃7 / #7:），返回 (pid 或 None, 剩余文本)。"""
    if raw is None:
        return None, raw
    match = PAPER_PREFIX.match(raw.strip())
    if not match:
        return None, raw
    return int(match.group(1)), raw.strip()[match.end():]


def parse_answers(raw, questions):
    """宽容解析答案串。

    支持：1A 2B 3C / 1a2b3c / 1.A 2.B / A B C / ABCABC / A,B,C
    返回 (answers, tokens, error)。answers 为长度等于题数的字母列表，缺项为 None。
    """
    text = normalize_input(raw)
    if not text:
        return None, 0, "我什么也没听见。回我一串答案，比如 1A 2B 3C。"

    option_counts = {q["id"]: len(q["options"]) for q in questions}
    ids = [q["id"] for q in questions]

    numbered = {}
    spans = []
    pattern = re.compile(r"(\d{1,2})\s*[\.\,:：、\)\]]?\s*([A-Za-z])")
    for match in pattern.finditer(text):
        qid = int(match.group(1))
        letter = match.group(2).upper()
        spans.append(match.span())
        if qid in option_counts and qid not in numbered:
            numbered[qid] = letter

    rest_chars = list(text)
    for start, end in spans:
        for idx in range(start, end):
            rest_chars[idx] = " "
    rest = "".join(rest_chars)

    loose = [ch.upper() for ch in rest if ch.isalpha()]

    answers = [None] * len(ids)
    index = {qid: pos for pos, qid in enumerate(ids)}

    if numbered:
        for qid, letter in numbered.items():
            answers[index[qid]] = letter
        cursor = 0
        for pos in range(len(ids)):
            if answers[pos] is None and cursor < len(loose):
                answers[pos] = loose[cursor]
                cursor += 1
    else:
        for pos in range(len(ids)):
            if pos < len(loose):
                answers[pos] = loose[pos]

    used = [a for a in answers if a]
    if not used:
        return None, 0, "这串字符我认不出来。回我字母就行，比如 1A 2B 3C，或者 ABCABC。"

    for pos, letter in enumerate(answers):
        if letter is None:
            continue
        limit = option_counts[ids[pos]]
        if ord(letter) - ord("A") + 1 > limit:
            return None, len(used), "第 %d 题只有 A/B/C 三个选项，你给了我 %s。" % (ids[pos], letter)

    return answers, len(used), None


# 卷号缺失时用来「盲判」答案串的探针题库：题号 1~64、每题三选项。
# 真实题库里每题都是三选项，所以拿它做纯语法检查是安全的——
# 目的只是把「你压根没给我答案」和「你给了答案但没说哪张卷」分开报。
PROBE_QUESTIONS = [{"id": i + 1, "options": [{"key": k} for k in ("A", "B", "C")]}
                   for i in range(64)]


def probe_answers(raw):
    """不知道卷号时的语法盲判，返回 (识别出的选项数, 错误文案)。"""
    _, used, error = parse_answers(raw, PROBE_QUESTIONS)
    return used, error


# ---------------------------------------------------------------- 卷

def compile_paper(paper, questions_data):
    """把一张卷编译成「11 道题」的题目列表（结构与题库里的单题完全一致）。

    这是随机卷与原有计分/渲染之间**唯一**的接缝：编译出来的东西跟旧题库的题长得一样，
    于是 compute_caps / score_answers / render_card 一行都不用改。
    slot.order[0..2] 依次展示为 A/B/C，权重跟着选项一起搬运。
    """
    meta = questions_data["meta"]
    default_option = meta.get("default_option", "B")
    by_id = {q["id"]: q for q in questions_data["questions"]}
    letters = "ABCDEFGH"

    questions = []
    for slot_pos, slot in enumerate(paper["slots"]):
        src = by_id[slot["qid"]]
        by_key = {o["key"]: o for o in src["options"]}
        options = []
        for idx, src_key in enumerate(slot["order"]):
            opt = by_key[src_key]
            options.append({
                "key": letters[idx],
                "text": opt["text"],
                "weights": dict(opt["weights"]),
            })
        want = src.get("default", default_option)
        default_key = letters[slot["order"].index(want)] if want in slot["order"] else letters[0]
        questions.append({
            "id": slot_pos + 1,
            "scene": src["scene"],
            "stem": src["stem"],
            "default": default_key,
            "options": options,
        })
    return questions


def papers_index(papers_data):
    return {p["id"]: p for p in papers_data.get("papers", [])}


def paper_questions(papers_data, questions_data, pid):
    paper = papers_index(papers_data).get(pid)
    if paper is None:
        return None
    return compile_paper(paper, questions_data)


def pick_paper_id(args, papers_data, explicit=None):
    """决定用哪张卷：显式指定 > --paper > --seed 派生 > 随机。"""
    ids = [p["id"] for p in papers_data.get("papers", [])]
    if not ids:
        return None
    if explicit is not None:
        return explicit if explicit in ids else None
    if getattr(args, "paper", None) is not None:
        return args.paper if args.paper in ids else None
    if args.seed is not None:
        return ids[args.seed % len(ids)]
    return random.SystemRandom().choice(ids)


# ---------------------------------------------------------------- 计分

def compute_caps(questions, house_keys):
    """cap[house] = 各题中该院可获得的最高权重之和。"""
    caps = {h: 0 for h in house_keys}
    for q in questions:
        best = {h: 0 for h in house_keys}
        for opt in q["options"]:
            for h, w in opt["weights"].items():
                if h in best:
                    best[h] = max(best[h], w)
        for h in house_keys:
            caps[h] += best[h]
    return caps


def score_answers(answers, questions, house_keys, default_option):
    caps = compute_caps(questions, house_keys)
    raw = {h: 0 for h in house_keys}
    missing = []
    applied = []
    for pos, q in enumerate(questions):
        letter = answers[pos]
        if letter is None:
            letter = q.get("default", default_option)
            missing.append(q["id"])
        chosen = None
        for opt in q["options"]:
            if opt["key"] == letter:
                chosen = opt
                break
        if chosen is None:
            return None
        applied.append(letter)
        for h, w in chosen["weights"].items():
            if h in raw:
                raw[h] += w
    score = {h: (raw[h] / caps[h] if caps[h] else 0.0) for h in house_keys}
    return {"raw": raw, "cap": caps, "score": score, "missing": missing, "applied": applied}


def rank_houses(score, priority):
    prio = {h: i for i, h in enumerate(priority)}
    return sorted(score.keys(), key=lambda h: (-round(score[h], 6), prio.get(h, 99)))


def index_id(applied, profile, paper_id):
    seed_text = "".join(applied) + "|" + str(profile) + "|p" + str(paper_id)
    return "%08X" % (zlib.crc32(seed_text.encode("utf-8")) & 0xFFFFFFFF)


def analyze(answers, questions, meta, paper_id):
    house_keys = meta.get("houses", HOUSE_ORDER)
    result = score_answers(answers, questions, house_keys, meta.get("default_option", "B"))
    if result is None:
        return None
    order = rank_houses(result["score"], meta.get("tie_break_priority", house_keys))
    result["order"] = order
    result["top1"] = order[0]
    result["top2"] = order[1]
    result["gap"] = round(result["score"][order[0]] - result["score"][order[1]], 6)
    result["hesitate"] = result["gap"] <= float(meta.get("threshold", 0.12))
    result["paper_id"] = paper_id
    result["id"] = index_id(result["applied"], meta.get("houses"), paper_id)
    return result


# ---------------------------------------------------------------- 渲染

def paper_tag(card, paper_id):
    return "%s %02d" % (card["paper_label"], paper_id)


def render_questions(questions, card, paper_id, papers_data):
    lines = []
    width = card["width"]
    pts_meta = papers_data.get("meta", {})
    lines.append(card["song_intro"])
    lines.append("")
    lines.extend(card["song"])
    lines.append("")
    lines.append(card["paper_intro"].format(
        id="%02d" % paper_id,
        size=pts_meta.get("paper_size", len(questions)),
        pool=pts_meta.get("pool_size", "?"),
        total=pts_meta.get("count", "?"),
    ))
    lines.append("")
    lines.append(card["questions_intro"])
    lines.append("")
    for q in questions:
        lines.append("【%d】%s" % (q["id"], q["scene"]))
        lines.extend(["  " + seg for seg in wrap(q["stem"], width - 2)])
        for opt in q["options"]:
            head = "  %s " % opt["key"]
            body = wrap(opt["text"], width - 4)
            lines.append(head + body[0])
            for seg in body[1:]:
                lines.append("    " + seg)
        lines.append("")
    lines.append(card["questions_footer"])
    return "\n".join(lines)


def _section(label):
    return ["◆ " + label]


def render_card(result, houses_data, forced=None, abstain=False):
    card = houses_data["card"]
    lines_cfg = card["lines"]
    labels = card["labels"]
    arch = card["archive_labels"]
    sep = card["identity_separator"]
    width = card["width"]
    houses = houses_data["houses"]

    house_key = result["house"]
    house = houses[house_key]
    body = []

    body.append("═" * width)
    body.append(pad(card["title"], width, "center").rstrip())
    body.append("═" * width)
    body.append("%s%s%s %s" % (paper_tag(card, result["paper_id"]), sep,
                               card["index_label"], result["id"]))
    body.append("")

    body.extend(_section(labels["house"]))
    identity = house["name"] + sep + house["colors"]
    if forced == "user":
        identity += "　" + lines_cfg["yield_note"]
    body.append("  " + identity)
    body.append("")

    body.extend(_section(labels["verdict"]))
    body.extend(["  " + seg for seg in house["verdict"]])
    if abstain:
        body.extend(["  " + seg for seg in wrap(lines_cfg["abstain_tease"], width - 2)])
    body.append("")

    body.extend(_section(labels["founder"]))
    body.append("  " + house["founder"] + sep + house["relic"])
    body.append("")

    body.extend(_section(labels["archive"]))
    rows = [
        (arch["colors"], house["colors"]),
        (arch["animal"], house["animal"]),
        (arch["element"], house["element"]),
        (arch["ghost"], house["ghost"]),
        (arch["entry"], house["entry"]),
    ]
    label_w = max(dwidth(r[0]) for r in rows)
    for name, value in rows:
        body.append("  " + pad(name, label_w) + "  " + value)
    body.append("")

    body.extend(_section(labels["glow"]))
    for item in house["glow"]:
        segs = wrap(item, width - 4)
        body.append("  · " + segs[0])
        for seg in segs[1:]:
            body.append("    " + seg)
    body.append("")

    body.extend(_section(labels["roommate"]))
    for item in house["roommate"]:
        segs = wrap(item, width - 4)
        body.append("  · " + segs[0])
        for seg in segs[1:]:
            body.append("    " + seg)
    body.append("")

    pair_words = [p.strip() for p in labels["affinity"].split("/")]
    body.extend(_section(labels["affinity"]))
    for word, key in ((pair_words[0], "affinity"), (pair_words[-1], "clash")):
        item = house[key]
        other = houses[item["house"]]["name"]
        text = "%s：%s%s%s" % (word, other, sep, item["why"])
        segs = wrap(text, width - 2)
        body.append("  " + segs[0])
        for seg in segs[1:]:
            body.append("    " + seg)
    body.append("")

    body.extend(_section(labels["last_word"]))
    body.extend(["  " + seg for seg in wrap(house["last_word"], width - 2)])
    body.append("")

    if result["missing"]:
        note = lines_cfg["missing_note"].format(ids="、".join(str(i) for i in result["missing"]))
        body.extend(["  " + seg for seg in wrap(note, width - 2)])

    body.append("─" * width)
    body.append(lines_cfg["share"].format(house=house["name"]))
    body.append("")
    for item in lines_cfg["declaration"]:
        body.extend(wrap(item, width))
    return "\n".join(body)


def render_list(houses_data):
    houses = houses_data["houses"]
    lines = []
    for key in HOUSE_ORDER:
        if key not in houses:
            continue
        h = houses[key]
        lines.append("%s  |  %s  |  %s  |  %s" % (key, h["name"], h["colors"], h["animal"]))
        lines.append("  创始人/遗物：%s / %s" % (h["founder"], h["relic"]))
        lines.append("  元素：%s  幽灵：%s  入口：%s" % (h["element"], h["ghost"], h["entry"]))
        lines.append("")
    return "\n".join(lines).rstrip()


# ---------------------------------------------------------------- 自检

FORBIDDEN_QUALITY_WORDS = [
    "勇气", "勇敢", "野心", "智慧", "聪明才智", "忠诚", "博学",
    "善良", "包容", "勤奋", "公平", "机智", "正义",
]

REQUIRED_HOUSE_FIELDS = [
    "name", "colors", "animal", "element", "ghost", "founder", "relic",
    "entry", "verdict", "glow", "roommate", "affinity", "clash", "last_word",
]

REQUIRED_CARD_LINES = [
    "answer_hint", "hesitate_1", "hesitate_2", "abstain_tease", "yield_tease",
    "yield_note", "missing_note", "share", "declaration",
]

REQUIRED_CARD_FIELDS = ["title", "index_label", "paper_label", "paper_intro", "width"]


def iter_strings(node, path=""):
    if isinstance(node, dict):
        for key, value in node.items():
            for item in iter_strings(value, "%s.%s" % (path, key)):
                yield item
    elif isinstance(node, list):
        for idx, value in enumerate(node):
            for item in iter_strings(value, "%s[%d]" % (path, idx)):
                yield item
    elif isinstance(node, str):
        yield path, node


def check_pool(questions_data):
    """题库级硬约束。最关键的一条：每道题四院峰值都必须等于 max_weight。

    守住了这条，任何一张 11 题的卷 cap 都必然等于 11 × max_weight，四院天然配平，
    不需要、也不允许逐卷去配平。
    """
    problems = []
    meta = questions_data["meta"]
    house_keys = meta["houses"]
    max_weight = meta.get("max_weight", 3)
    seen_ids = set()
    for q in questions_data["questions"]:
        if q["id"] in seen_ids:
            problems.append("题库里第 %s 题的 id 重复" % q["id"])
        seen_ids.add(q["id"])
        keys = [o["key"] for o in q["options"]]
        if len(keys) < 3:
            problems.append("第 %s 题选项少于 3 个" % q["id"])
        if len(set(keys)) != len(keys):
            problems.append("第 %s 题选项字母重复" % q["id"])
        if q.get("default") not in keys:
            problems.append("第 %s 题 default 指向不存在的选项" % q["id"])
        for opt in q["options"]:
            if not opt.get("text", "").strip():
                problems.append("第 %s 题 %s 选项是空文案" % (q["id"], opt["key"]))
            weights = opt.get("weights", {})
            if not weights:
                problems.append("第 %s 题 %s 选项没有权重" % (q["id"], opt["key"]))
            for house, weight in weights.items():
                if house not in house_keys:
                    problems.append("第 %s 题 %s 引用了未知学院 %s" % (q["id"], opt["key"], house))
                if not isinstance(weight, int) or weight < 0 or weight > max_weight:
                    problems.append("第 %s 题 %s 权重越界：%s=%s" % (q["id"], opt["key"], house, weight))
        for house in house_keys:
            peak = max(o["weights"].get(house, 0) for o in q["options"])
            if peak != max_weight:
                problems.append("第 %s 题 %s 的峰值是 %d，必须等于 max_weight(%d)，否则各卷 cap 会失衡"
                                % (q["id"], house, peak, max_weight))
    return problems


def check_papers(papers_data, questions_data):
    """试卷级硬约束：结构、选项排列、逐卷 cap 配平、覆盖均衡、卷面互不相同。"""
    problems = []
    infos = []
    meta = questions_data["meta"]
    house_keys = meta["houses"]
    max_weight = meta.get("max_weight", 3)
    paper_size = int(meta.get("paper_size", 11))
    pool_ids = {q["id"] for q in questions_data["questions"]}
    keys_of = {q["id"]: [o["key"] for o in q["options"]] for q in questions_data["questions"]}
    papers = papers_data.get("papers", [])

    if not papers:
        return ["papers.json 里没有任何试卷"], infos

    sets = []
    for paper in papers:
        pid = paper.get("id")
        slots = paper.get("slots", [])
        if len(slots) != paper_size:
            problems.append("第 %s 卷题目数不是 %d：%d" % (pid, paper_size, len(slots)))
        qids = [s.get("qid") for s in slots]
        if len(set(qids)) != len(qids):
            problems.append("第 %s 卷抽到了重复的题" % pid)
        for qid in qids:
            if qid not in pool_ids:
                problems.append("第 %s 卷引用了题库里没有的第 %s 题" % (pid, qid))
        for slot in slots:
            if sorted(slot.get("order", [])) != sorted(keys_of.get(slot.get("qid"), [])):
                problems.append("第 %s 卷第 %s 题的选项排列不是全排列：%s"
                                % (pid, slot.get("qid"), slot.get("order")))
        compiled = compile_paper(paper, questions_data)
        totals = {house: 0 for house in house_keys}
        for q in compiled:
            for house in house_keys:
                peak = max(o["weights"].get(house, 0) for o in q["options"])
                if peak != max_weight:
                    problems.append("第 %s 卷第 %d 题 %s 的峰值是 %d，应为 %d"
                                    % (pid, q["id"], house, peak, max_weight))
                totals[house] += peak
        if len(set(totals.values())) != 1:
            problems.append("第 %s 卷 cap 未配平：%s" % (pid, totals))
        sets.append(frozenset(qids))

    if len(set(sets)) != len(sets):
        problems.append("存在两张卷抽到完全相同的题目集合")

    counts = {}
    for st in sets:
        for qid in st:
            counts[qid] = counts.get(qid, 0) + 1
    unused = sorted(pool_ids - set(counts))
    if unused:
        problems.append("题库里这些题在全部试卷中一次都没被抽到：%s" % unused)
    if counts and max(counts.values()) - min(counts.values()) > 1:
        problems.append("题池覆盖不均衡：单题最少被抽 %d 次，最多 %d 次"
                        % (min(counts.values()), max(counts.values())))

    worst = 0
    for i in range(len(sets)):
        for j in range(i + 1, len(sets)):
            worst = max(worst, len(sets[i] & sets[j]))
    infos.append("试卷 = %d 张，每张 %d 题，题库 %d 题" % (len(papers), paper_size, len(pool_ids)))
    if counts:
        span = ("每道题都被抽中 %d 次" % next(iter(counts.values()))
                if len(set(counts.values())) == 1
                else "单题被抽中 %d ~ %d 次" % (min(counts.values()), max(counts.values())))
        infos.append(span)
    infos.append("任意两张卷最多重合 %d 题" % worst)
    return problems, infos


def _combo_scores(questions, house_keys, meta, paper_id=0):
    """遍历 3^N 组合，返回 (reachable, first_normal, first_hesitate, hesitate_total)。"""
    keys_per_q = [[o["key"] for o in q["options"]] for q in questions]
    vectors = []
    for q in questions:
        vecs = []
        for opt in q["options"]:
            vecs.append(tuple(opt["weights"].get(h, 0) for h in house_keys))
        vectors.append(vecs)
    caps = compute_caps(questions, house_keys)
    cap_vec = tuple(caps[h] for h in house_keys)
    priority = meta.get("tie_break_priority", house_keys)
    prio = {h: i for i, h in enumerate(priority)}

    reachable = set()
    first_normal = None
    first_hesitate = None
    hesitate_total = 0
    n = len(questions)
    picks = [0] * n

    while True:
        raw = [0] * len(house_keys)
        for pos in range(n):
            vec = vectors[pos][picks[pos]]
            for hi in range(len(house_keys)):
                raw[hi] += vec[hi]
        score = [raw[hi] / cap_vec[hi] if cap_vec[hi] else 0.0 for hi in range(len(house_keys))]
        order = sorted(range(len(house_keys)), key=lambda hi: (-round(score[hi], 6), prio.get(house_keys[hi], 99)))
        gap = round(score[order[0]] - score[order[1]], 6)
        reachable.add(house_keys[order[0]])
        letters = "".join(keys_per_q[pos][picks[pos]] for pos in range(n))
        hesitate = gap <= float(meta.get("threshold", 0.12))
        if hesitate:
            hesitate_total += 1
            if first_hesitate is None:
                first_hesitate = (letters, house_keys[order[0]], house_keys[order[1]], gap)
        elif first_normal is None:
            first_normal = (letters, house_keys[order[0]], house_keys[order[1]], gap)

        pos = n - 1
        while pos >= 0:
            picks[pos] += 1
            if picks[pos] < len(keys_per_q[pos]):
                break
            picks[pos] = 0
            pos -= 1
        if pos < 0:
            break
    return reachable, first_normal, first_hesitate, hesitate_total


def check_glossary(glossary, questions_data, houses_data):
    """词典自检：字段完整、词条唯一、不留死词条（每个词条必须真的在文案里出现过）。

    语料 = 题库 + 学院文案 + 词典自己的标题与说明。
    把词典自己的说明也算进去，是因为「麻瓜」这类词只出现在说明里——
    没有这条，它会被误判成死词条。
    """
    problems = []
    infos = []
    if glossary is None:
        return problems, infos
    meta = glossary.get("meta", {})
    for field in ("title", "intro", "scope_note"):
        value = meta.get(field)
        if not isinstance(value, str) or not value.strip():
            problems.append("词典 meta.%s 为空文案" % field)

    terms = glossary.get("terms", [])
    if not terms:
        problems.append("词典一个词条都没有")

    blob_parts = [text for _, text in iter_strings(questions_data)]
    blob_parts += [text for _, text in iter_strings(houses_data)]
    blob_parts += [text for _, text in iter_strings(meta)]
    blob = "\n".join(blob_parts)

    seen = set()
    house_scoped = 0
    for item in terms:
        term = item.get("term", "")
        gloss = item.get("gloss", "")
        if not isinstance(term, str) or not term.strip():
            problems.append("词典里有空词条名")
            continue
        if term in seen:
            problems.append("词典词条重复：%s" % term)
        seen.add(term)
        if not isinstance(gloss, str) or not gloss.strip():
            problems.append("词典词条 %s 没有解释" % term)
            continue
        if term not in blob:
            problems.append("词典词条「%s」在题库、学院文案与词典说明里一次都没出现过" % term)
        if gloss.count("「") != gloss.count("」"):
            problems.append("词典 %s 的解释引号不配对" % term)
        if gloss.count("「") > 1:
            problems.append("词典 %s 的解释存在嵌套引号" % term)
        if item.get("house"):
            house_scoped += 1

    if terms:
        infos.append("词典 = %d 条（其中 %d 条带学院信息，只在封面与结果页标注）"
                     % (len(terms), house_scoped))
    return problems, infos


def audit(houses_data, questions_data, papers_data, label="canon", enumerate_papers=6, glossary=None):
    """自检。

    结构类约束（逐题峰值、逐卷 cap、试卷结构、字段、禁词）是**全量**检查，一张卷都不漏。
    3^11 组合枚举只是抽样观测（可达性与触发率都源于题库设计，不是靠枚举证明的），
    所以默认只均匀抽 enumerate_papers 张卷跑；enumerate_papers=0 表示全部跑（约 70 秒）。
    """
    problems = []
    infos = []
    house_keys = questions_data["meta"]["houses"]
    houses = houses_data["houses"]
    card = houses_data["card"]

    if len(house_keys) != 4:
        problems.append("四院数量不是 4：%s" % house_keys)

    for key in house_keys:
        if key not in houses:
            problems.append("配置缺少学院：%s" % key)
            continue
        house = houses[key]
        for field in REQUIRED_HOUSE_FIELDS:
            if field not in house:
                problems.append("%s 缺字段 %s" % (key, field))
        for field in ("name", "colors", "animal", "element", "ghost", "founder", "relic", "entry", "last_word"):
            value = house.get(field, "")
            if not isinstance(value, str) or not value.strip():
                problems.append("%s.%s 为空文案" % (key, field))
        for field in ("verdict", "glow", "roommate"):
            value = house.get(field, [])
            if not isinstance(value, list) or not value:
                problems.append("%s.%s 为空文案" % (key, field))
            else:
                for idx, item in enumerate(value):
                    if not isinstance(item, str) or not item.strip():
                        problems.append("%s.%s[%d] 为空文案" % (key, field, idx))
        for field in ("affinity", "clash"):
            item = house.get(field, {})
            if not isinstance(item, dict) or not item.get("house") or not item.get("why"):
                problems.append("%s.%s 字段不全" % (key, field))
                continue
            if item["house"] not in house_keys:
                problems.append("%s.%s 指向了未知学院 %s" % (key, field, item["house"]))
            if item["house"] == key:
                problems.append("%s.%s 指向了自己" % (key, field))
            pair_key = item.get("pair_key", "")
            parts = pair_key.split("-") if "-" in pair_key else []
            if len(parts) != 2 or any(p not in house_keys for p in parts):
                problems.append("%s.%s.pair_key 不是「学院-学院」形式：%s" % (key, field, pair_key))
            if set(parts) != {key, item["house"]}:
                problems.append("%s.%s.pair_key 与 house 字段不一致：%s" % (key, field, pair_key))

    for field in REQUIRED_CARD_FIELDS:
        if field not in card:
            problems.append("card 缺字段 %s" % field)
    for field in REQUIRED_CARD_LINES:
        value = card["lines"].get(field)
        if value is None or (isinstance(value, str) and not value.strip()) or (isinstance(value, list) and not value):
            problems.append("card.lines.%s 为空文案" % field)
    for field in ("labels", "archive_labels", "focus_comment"):
        if field not in card:
            problems.append("card 缺字段 %s" % field)
    for key in house_keys:
        if key not in card.get("focus_comment", {}):
            problems.append("card.focus_comment 缺少 %s" % key)
    if len(card.get("song", [])) < 6 or len(card.get("song", [])) > 10:
        problems.append("card.song 行数不在 6-10 行之间：%d" % len(card.get("song", [])))
    if card.get("paper_intro"):
        for token in ("{id}", "{size}", "{pool}"):
            if token not in card["paper_intro"]:
                problems.append("card.paper_intro 缺少占位符 %s" % token)
        try:
            card["paper_intro"].format(id="01", size=11, pool=33, total=33)
        except Exception as exc:
            problems.append("card.paper_intro 占位符无法填充：%s" % exc)

    problems.extend(check_pool(questions_data))
    paper_problems, paper_infos = check_papers(papers_data, questions_data)
    problems.extend(paper_problems)
    infos.extend(paper_infos)
    gloss_problems, gloss_infos = check_glossary(glossary, questions_data, houses_data)
    problems.extend(gloss_problems)
    infos.extend(gloss_infos)

    reachable_all = set()
    hesitate_rates = []
    examples = {}
    papers = papers_data.get("papers", [])
    for paper in papers:
        questions = compile_paper(paper, questions_data)
        caps = compute_caps(questions, house_keys)
        if len(set(caps.values())) != 1:
            problems.append("第 %s 卷 cap 未配平：%s" % (paper["id"], caps))

    # 均匀抽几张卷做组合枚举（第 1 张必跑，它的示例要喂给 --selftest）
    if enumerate_papers and enumerate_papers > 0 and len(papers) > enumerate_papers:
        step = len(papers) / float(enumerate_papers)
        picked = sorted({papers[0]["id"]} | {papers[min(int(i * step), len(papers) - 1)]["id"]
                                            for i in range(enumerate_papers)})
    else:
        picked = [p["id"] for p in papers]
    for pid in picked:
        questions = paper_questions(papers_data, questions_data, pid)
        reachable, normal, hesitate, total = _combo_scores(
            questions, house_keys, questions_data["meta"], pid)
        reachable_all |= reachable
        enum_total = 1
        for q in questions:
            enum_total *= len(q["options"])
        hesitate_rates.append(total / float(enum_total))
        if pid == papers[0]["id"]:
            examples = {"normal": normal, "hesitate": hesitate, "reachable": sorted(reachable)}

    for house in house_keys:
        if house not in reachable_all:
            problems.append("学院不可达（抽到的试卷里都当不上头名）：%s" % house)
    infos.append("可达学院 = %s（枚举 %d 张卷）"
                 % ("、".join(h for h in house_keys if h in reachable_all), len(picked)))
    if hesitate_rates:
        infos.append("第 3 轮触发率 = %.1f%% ~ %.1f%%（逐卷枚举 %d 张，随机作答基准）"
                     % (min(hesitate_rates) * 100, max(hesitate_rates) * 100, len(picked)))
    caps = compute_caps(compile_paper(papers[0], questions_data), house_keys) if papers else {}
    if caps:
        infos.insert(0, "单卷 cap = %s" % json.dumps(caps, ensure_ascii=False))

    forbidden = list(HOUSE_ALIASES.keys())
    for names in HOUSE_ALIASES.values():
        forbidden.extend(names)
    forbidden.extend([houses[h]["name"] for h in houses])
    forbidden.extend(FORBIDDEN_QUALITY_WORDS)
    for q in questions_data["questions"]:
        zone = [q.get("scene", ""), q.get("stem", "")] + [o.get("text", "") for o in q["options"]]
        for text in zone:
            for word in forbidden:
                if word and word in text:
                    problems.append("题库第 %s 题出现禁用词「%s」：%s" % (q["id"], word, text))

    for path, text in iter_strings(houses_data):
        if text.count("「") != text.count("」"):
            problems.append("引号不配对：%s -> %s" % (path, text))
        if text.count("「") > 1:
            problems.append("存在嵌套引号：%s -> %s" % (path, text))
        if re.match(r"^[A-Z]{2,8}$", text):
            problems.append("疑似连读枚举值（应用分隔符连接）：%s -> %s" % (path, text))

    ok = not problems
    return ok, problems, infos, examples


# ---------------------------------------------------------------- 第 3 轮意愿解析

def resolve_will(raw, houses_data, house_keys):
    text = normalize_input(raw)
    if not text:
        return "error", "帽子在等一句话：你想去哪？"
    house = detect_house(text)
    if house:
        return "house", house
    if detect_abstain(text):
        return "abstain", None
    letters = [ch.upper() for ch in text if ch.isalpha()]
    if len(letters) == 1:
        idx = ord(letters[0]) - ord("A")
        if 0 <= idx < len(house_keys):
            return "house", house_keys[idx]
        return "error", "字母只到 %s，超出的我不认。" % chr(ord("A") + len(house_keys) - 1)
    return "error", "没听清。回我学院名，或者回 A B C D 里对应的那个字母。"


def random_answers_letters(questions, seed):
    rng = random.Random(seed)
    return "".join(rng.choice([o["key"] for o in q["options"]]) for q in questions)


# ---------------------------------------------------------------- 主流程

PAPER_HELP = ("[认不出卷号] 你回了我一串答案，但没告诉我是哪张卷。\n"
              "  文本模式下帽子开头就会报「卷号 NN」，照抄给我：\n"
              "    python sorting_hat.py --card \"1A 2B 3C …\" --paper 7\n"
              "  也可以把卷号写在答案串前面：--card \"#7 1A 2B 3C …\"\n"
              "  想先看看有哪些卷：python sorting_hat.py --list-papers")


def report_missing_paper(body):
    """卷号缺失时报最贴切的那个错。

    先盲判这段文本到底是不是答案：连字母都认不出来 → 报「认不出答案」；
    字母认得出但越界（回了 D）→ 报选项越界；确实是一串像样的答案 → 才报缺卷号。
    否则用户回个「???」会被告知「你没告诉我哪张卷」，纯属误导。
    """
    used, probe_error = probe_answers(body)
    if used == 0:
        err("[认不出答案] " + (probe_error or "这串字符我认不出来。回我字母就行，比如 1A 2B 3C。"))
        err("示例：--card \"#7 1A 2B 3C …\"（卷号写在最前面）")
        return EXIT_PARSE
    if probe_error:
        err("[认不出答案] " + probe_error)
        err("示例：--card \"#7 1A 2B 3C …\"（卷号写在最前面）")
        return EXIT_PARSE
    err(PAPER_HELP)
    return EXIT_PARSE


def emit(houses, questions_data, papers_data, raw_answers, raw_will, paper_id=None):
    meta = questions_data["meta"]
    house_keys = meta["houses"]
    card = houses["card"]
    lines = card["lines"]

    prefix_pid, body = split_paper_prefix(raw_answers)
    if prefix_pid is not None:
        paper_id = prefix_pid

    if paper_id is None:
        return report_missing_paper(body)
    questions = paper_questions(papers_data, questions_data, paper_id)
    if questions is None:
        err("[认不出卷号] 没有第 %s 号卷。可用范围：1 ~ %d。"
            % (paper_id, len(papers_data.get("papers", []))))
        return EXIT_PARSE

    answers, used, error = parse_answers(body, questions)
    if error:
        err("[认不出答案] " + error)
        err("示例：--card \"1A 2B 3C …\" --paper 7 ／ --card \"#7 ABCABC…\"")
        return EXIT_PARSE

    result = analyze(answers, questions, meta, paper_id)
    if result is None:
        err("[计分失败] 配置与答案不匹配，请先跑 --audit 检查。")
        return EXIT_CONFIG

    out("\n".join(card["focus_comment"][result["top1"]]))
    out("")

    forced = None
    abstain = False
    if raw_will is None:
        if result["hesitate"]:
            out(lines["hesitate_1"])
            out(lines["hesitate_2"])
            out(lines["round3_hint"])
            for idx, key in enumerate(house_keys):
                out("  %s %s" % (chr(ord("A") + idx), houses["houses"][key]["name"]))
            return EXIT_OK
        result["house"] = result["top1"]
    else:
        kind, payload = resolve_will(raw_will, houses, house_keys)
        if kind == "error":
            err("[意愿没听清] " + payload)
            return EXIT_PARSE
        if kind == "abstain":
            result["house"] = result["order"][0]
            abstain = True
        else:
            result["house"] = payload
            if payload != result["top1"]:
                forced = "user"
                out(lines["yield_tease"])
                out("")

    out(render_card(result, houses, forced=forced, abstain=abstain))
    return EXIT_OK


def cmd_scores(houses, questions_data, papers_data, raw_answers, paper_id):
    meta = questions_data["meta"]
    prefix_pid, body = split_paper_prefix(raw_answers)
    if prefix_pid is not None:
        paper_id = prefix_pid
    if paper_id is None:
        return report_missing_paper(body)
    questions = paper_questions(papers_data, questions_data, paper_id)
    if questions is None:
        err("[认不出卷号] 没有第 %s 号卷。" % paper_id)
        return EXIT_PARSE
    answers, used, error = parse_answers(body, questions)
    if error:
        err("[认不出答案] " + error)
        return EXIT_PARSE
    result = analyze(answers, questions, meta, paper_id)
    out("卷号 %02d  编号 %s" % (paper_id, result["id"]))
    for pos, key in enumerate(result["order"]):
        out("%d. %-8s %s raw=%s cap=%s gap=%s" % (
            pos + 1, key, round(result["score"][key], 4),
            result["raw"][key], result["cap"][key],
            round(result["score"][result["order"][0]] - result["score"][key], 4)))
    out("threshold=%s hesitate=%s 未作答=%s" % (meta["threshold"], result["hesitate"], result["missing"]))
    return EXIT_OK


def cmd_list_papers(papers_data, questions_data, limit=0):
    meta = papers_data.get("meta", {})
    papers = papers_data.get("papers", [])
    out("试卷库：%d 张，每张 %d 题，题库 %d 题，种子 %s"
        % (len(papers), meta.get("paper_size", "?"), meta.get("pool_size", "?"), meta.get("seed", "?")))
    out("")
    by_id = {q["id"]: q for q in questions_data["questions"]}
    for paper in papers[:limit] if limit else papers:
        scenes = [by_id[s["qid"]]["scene"] for s in paper["slots"]]
        out("卷号 %02d：%s" % (paper["id"], " / ".join(scenes)))
    return EXIT_OK


def cmd_audit(houses, questions_data, papers_data, label, enumerate_papers=6, glossary=None):
    ok, problems, infos, examples = audit(houses, questions_data, papers_data, label,
                                          enumerate_papers=enumerate_papers, glossary=glossary)
    out("[自检] 配置 = %s" % label)
    for info in infos:
        out("  · " + info)
    if ok:
        out("[OK] 逐题四院峰值配平、逐卷 cap 配平、四院可达、试卷结构完整、字段完整、无空文案、题干无禁用词")
        return EXIT_OK
    for item in problems:
        out("[FAIL] " + item)
    out("[结果] 发现 %d 处问题" % len(problems))
    return EXIT_CONFIG


def selftest(args):
    houses, questions_data, papers_data, _, glossary = load_configs(args)
    alt = load_json(ALT_HOUSES, "house")
    alt_glossary = load_json(ALT_GLOSSARY, "词典") if os.path.exists(ALT_GLOSSARY) else None
    meta = questions_data["meta"]
    house_keys = meta["houses"]
    card = houses["card"]
    papers = papers_data["papers"]
    checks = []

    ok, problems, infos, examples = audit(houses, questions_data, papers_data, "canon", glossary=glossary)
    checks.append(("主配置自检通过", ok, problems))
    ok_alt, problems_alt, _, _ = audit(alt, questions_data, papers_data, "alt",
                                       enumerate_papers=1, glossary=alt_glossary)
    checks.append(("去 IP 化配置自检通过", ok_alt, problems_alt))
    checks.append(("四院均可达成头名", set(examples["reachable"]) == set(house_keys), []))

    pid = papers[0]["id"]
    questions = paper_questions(papers_data, questions_data, pid)
    n_letters, n_top, _, n_gap = examples["normal"]
    h_letters, h_top, _, h_gap = examples["hesitate"]
    r_normal = analyze(list(n_letters), questions, meta, pid)
    r_hes = analyze(list(h_letters), questions, meta, pid)

    checks.append(("结局1 正常判定（分差 %s > %s）" % (n_gap, meta["threshold"]),
                   (not r_normal["hesitate"]) and r_normal["top1"] == n_top, []))
    checks.append(("结局2 第 3 轮可触发（分差 %s <= %s）" % (h_gap, meta["threshold"]),
                   r_hes["hesitate"], []))

    c_normal = dict(r_normal)
    c_normal["house"] = r_normal["top1"]
    card1 = render_card(c_normal, houses)
    c_hes = dict(r_hes)
    c_hes["house"] = r_hes["top1"]
    card2 = render_card(c_hes, houses)
    c_yield = dict(r_hes)
    c_yield["house"] = r_hes["order"][-1]
    card3 = render_card(c_yield, houses, forced="user")
    c_abstain = dict(r_hes)
    c_abstain["house"] = r_hes["order"][0]
    card4 = render_card(c_abstain, houses, abstain=True)

    checks.append(("结局3 帽子让步并标注", card["lines"]["yield_note"].strip("（）") in card3, []))
    checks.append(("结局4 用户弃权并吐槽", card["lines"]["abstain_tease"] in card4, []))

    again = analyze(list(n_letters), questions, meta, pid)
    c_again = dict(again)
    c_again["house"] = again["top1"]
    checks.append(("同一卷同一答案跑两次结果完全一致", render_card(c_again, houses) == card1, []))

    # 卷号必须真的参与编号：换一张卷，同一串字母必须给出不同的编号
    other = papers[1]["id"]
    other_q = paper_questions(papers_data, questions_data, other)
    r_other = analyze(list(n_letters), other_q, meta, other)
    checks.append(("换卷后编号随之改变（同一答案不同卡）",
                   r_other["id"] != r_normal["id"] and r_other["paper_id"] == other, []))

    # 同一张卷必须可复现：显式 --paper 两次给出同一个编号
    r_repeat = analyze(list(n_letters), paper_questions(papers_data, questions_data, pid), meta, pid)
    checks.append(("--paper 可复现同一张卡", r_repeat["id"] == r_normal["id"], []))

    seed = args.seed if args.seed is not None else 20260911
    pid_seed = papers[seed % len(papers)]["id"]
    q_seed = paper_questions(papers_data, questions_data, pid_seed)
    l1 = random_answers_letters(q_seed, seed)
    l2 = random_answers_letters(q_seed, seed)
    checks.append(("--random --seed %d 两次输出一致（含卷号固定）" % seed,
                   l1 == l2 and l1 != "" and pid_seed == papers[seed % len(papers)]["id"], []))

    _, _, e_empty = parse_answers("", questions)
    _, _, e_junk = parse_answers("???", questions)
    _, _, e_over = parse_answers("1D 2D", questions)
    checks.append(("空输入/非法输入给出友好提示", all([e_empty, e_junk, e_over]),
                   [x for x in (e_empty, e_junk, e_over) if not x]))

    partial, _, e_partial = parse_answers("1A 2B", questions)
    r_partial = analyze(partial, questions, meta, pid)
    checks.append(("缺答按该题默认项补入并留注记",
                   e_partial is None and r_partial is not None
                   and len(r_partial["missing"]) == len(questions) - 2, []))

    # 默认项必须落在编译后的某个字母位上，且位置与卷数据一致
    default_ok = True
    for paper in papers:
        for pos, q in enumerate(compile_paper(paper, questions_data)):
            pool_q = {x["id"]: x for x in questions_data["questions"]}[paper["slots"][pos]["qid"]]
            want_pos = paper["slots"][pos]["order"].index(pool_q["default"])
            if q["default"] != "ABC"[want_pos]:
                default_ok = False
    checks.append(("每题默认项随选项顺序一起搬运", default_ok, []))

    formats = [
        "1A 2B 3C 4A 5B 6C 7A 8B 9C 10A 11B",
        "1a2b3c4a5b6c7a8b9c10a11b",
        "1.A 2.B 3.C 4.A 5.B 6.C 7.A 8.B 9.C 10.A 11.B",
        "A B C A B C A B C A B",
        "ABCABCABCAB",
        "A,B,C,A,B,C,A,B,C,A,B",
    ]
    parsed = []
    for item in formats:
        ans, _, err_ = parse_answers(item, questions)
        parsed.append(None if err_ else "".join(a for a in ans if a))
    checks.append(("六种答案格式解析结果一致", len(set(parsed)) == 1 and parsed[0] is not None, [repr(p) for p in parsed]))

    # 卷号前缀必须能从答案串里剥出来
    pid_from_text, rest = split_paper_prefix("#7 1A 2B 3C")
    checks.append(("答案串可自带卷号前缀 #N",
                   pid_from_text == 7 and rest.strip() == "1A 2B 3C", [repr(pid_from_text), repr(rest)]))

    # 缺卷号时，「不是答案」和「没说哪张卷」必须报不同的错
    junk_used, junk_err = probe_answers("???")
    ok_used, ok_err = probe_answers("1A 2B 3C")
    over_used, over_err = probe_answers("1D 2D")
    checks.append(("缺卷号时能区分「不是答案」「选项越界」「缺卷号」",
                   junk_used == 0 and junk_err
                   and ok_used == 3 and ok_err is None
                   and over_used > 0 and over_err is not None,
                   [repr(junk_used), repr(junk_err), repr(ok_used), repr(ok_err),
                    repr(over_used), repr(over_err)]))

    # 每题选项顺序确实被打乱过（不能整库原样搬运）
    shuffled = 0
    for paper in papers:
        for slot in paper["slots"]:
            if slot["order"] != sorted(slot["order"]):
                shuffled += 1
    checks.append(("选项顺序确实被打乱（%d/%d 个槽位非字母序）"
                   % (shuffled, sum(len(p["slots"]) for p in papers)),
                   shuffled > 0, []))

    width = card["width"]
    joined = "\n".join([card1, card2, card3, card4])
    over = [line for line in joined.split("\n") if dwidth(line) > width]
    checks.append(("卡片行宽不超过版心 %d" % width, not over, over[:3]))

    failed = 0
    for name, passed, detail in checks:
        if passed:
            out("[PASS] " + name)
        else:
            failed += 1
            out("[FAIL] " + name)
            for item in detail[:4]:
                out("        ↳ " + str(item))
    out("[汇总] %d/%d 项通过" % (len(checks) - failed, len(checks)))
    out("[示例] 卷号 %02d 正常判定答案串 = %s（分差 %s）" % (pid, n_letters, n_gap))
    out("[示例] 卷号 %02d 触发第 3 轮答案串 = %s（分差 %s，头名 %s）" % (pid, h_letters, h_gap, h_top))
    return EXIT_OK if failed == 0 else EXIT_CONFIG


def build_parser():
    parser = argparse.ArgumentParser(
        prog="sorting_hat.py",
        description="分院帽 Skill：解析 -> 计分 -> 查表 -> 渲染（题库随机抽卷）",
    )
    parser.add_argument("--card", metavar="ANSWERS", help="答案串，如 1A 2B 3C 或 ABCABC；可写 #7 前缀带卷号")
    parser.add_argument("--questions", action="store_true", help="第 1 轮：歌谣 + 报卷号 + 一屏题目")
    parser.add_argument("--paper", type=int, default=None, help="指定卷号（1 起）")
    parser.add_argument("--list", action="store_true", help="列出四院配置")
    parser.add_argument("--list-papers", action="store_true", help="列出试卷库（卷号 + 各卷场景）")
    parser.add_argument("--limit", type=int, default=0, help="--list-papers 只打印前 N 张（0 = 全部）")
    parser.add_argument("--audit", action="store_true", help="自检：题库峰值/逐卷 cap/试卷结构/字段/禁词")
    parser.add_argument("--audit-papers", type=int, default=6,
                        help="--audit 组合枚举抽几张卷（默认 6；0 = 全部跑，约 70 秒）")
    parser.add_argument("--selftest", action="store_true", help="回归自测：四种结局 + 确定性 + 解析容错")
    parser.add_argument("--random", action="store_true", help="按种子生成一份随机答案并出结果")
    parser.add_argument("--seed", type=int, default=None, help="随机种子（决定卷号与答案，可复现）")
    parser.add_argument("--will", default=None, help="第 3 轮意愿：学院名 / A-D 字母 / 随便")
    parser.add_argument("--scores", metavar="ANSWERS", help="调试：打印四院归一化得分")
    parser.add_argument("--config", default="canon", help="数据配置：canon | alt | 自定义路径")
    parser.add_argument("--houses", default=DEFAULT_HOUSES, help="指定 houses.json 路径")
    parser.add_argument("--questions-file", default=DEFAULT_QUESTIONS, help="指定题库 questions.json 路径")
    parser.add_argument("--papers-file", default=None, help="指定试卷库 papers.json 路径")
    parser.add_argument("--glossary", default=None, help="指定麻瓜词典路径（默认随 --config 自动选）")
    return parser


def main(argv=None):
    setup_stdout()
    args = build_parser().parse_args(argv)
    houses, questions_data, papers_data, houses_path, glossary = load_configs(args)

    if args.selftest:
        return selftest(args)
    if args.audit:
        return cmd_audit(houses, questions_data, papers_data,
                         args.config if args.config else houses_path,
                         enumerate_papers=args.audit_papers, glossary=glossary)
    if args.list_papers:
        return cmd_list_papers(papers_data, questions_data, args.limit)
    if args.questions:
        pid = pick_paper_id(args, papers_data)
        if pid is None:
            err("[配置缺失] 试卷库是空的，先跑 python scripts/make_papers.py 生成。")
            return EXIT_CONFIG
        questions = paper_questions(papers_data, questions_data, pid)
        out(render_questions(questions, houses["card"], pid, papers_data))
        return EXIT_OK
    if args.list:
        out(render_list(houses))
        return EXIT_OK
    if args.scores is not None:
        return cmd_scores(houses, questions_data, papers_data, args.scores, args.paper)
    if args.random:
        seed = args.seed if args.seed is not None else random.SystemRandom().randrange(1, 10 ** 9)
        pid = pick_paper_id(args, papers_data, explicit=None)
        questions = paper_questions(papers_data, questions_data, pid)
        letters = random_answers_letters(questions, seed)
        out("随机种子：%d（带同一 seed 重跑结果一致）" % seed)
        out("卷号：%02d" % pid)
        out("答案串：%s" % letters)
        out("")
        return emit(houses, questions_data, papers_data, letters, args.will, paper_id=pid)
    if args.card is not None:
        return emit(houses, questions_data, papers_data, args.card, args.will, paper_id=args.paper)

    err("需要指定一个动作：--questions | --card <答案串> [--paper N] | --list | --list-papers "
        "| --audit | --random | --selftest")
    err("示例：python sorting_hat.py --questions")
    return EXIT_USAGE


if __name__ == "__main__":
    sys.exit(main())
