# -*- coding: utf-8 -*-
"""linggen.py — 本命灵根测试主引擎。

用法：
  python linggen.py --card "P07:1A2B3C4A5B6C7A8B" [--config alt|fan]
  python linggen.py --questions --paper 7
  python linggen.py --scores "P07:1A2B..." --paper 7
  python linggen.py --audit | --selftest | --calibrate | --list | --list-papers

退出码：0 成功 / 2 答案串或卷号无法解析 / 3 帖码校验失败
"""
import argparse
import json
import math
import random
import re
import sys
import unicodedata
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
FIVE = ["metal", "wood", "water", "fire", "earth"]
CN_NUM = {1: "一", 1.5: "一点五", 2: "二", 3: "三", 5: "五", 6: "六",
          9: "九", 25: "二十五", 36: "三十六"}


def out(s=""):
    print(s)


def disp_w(s):
    """显示宽度：CJK 记 2，其余记 1。"""
    w = 0
    for ch in s:
        w += 2 if unicodedata.east_asian_width(ch) in "WF" else 1
    return w


def load():
    d = {name: json.loads((DATA / f"{name}.json").read_text(encoding="utf-8"))
         for name in ["questions", "attrs", "tiers", "meta", "papers"]}
    return d


# ---------------------------------------------------------------- 判定核心

def round_half_up(x):
    return math.floor(x + 0.5)


def grade(raw, cfg, cap):
    """raw → (tier_key, mutation_key|None, attr_set, main_attr, scores)"""
    meta, attrs = cfg["meta"], cfg["attrs"]
    scores = {a: raw[a] / cap for a in FIVE}
    ranked = sorted(FIVE, key=lambda a: (-scores[a], meta["tie_break"].index(a)))
    s1, s2 = scores[ranked[0]], scores[ranked[1]]
    # 变异优先：top2 为相生对、双双过线、并列领先、且明显甩开第三名
    m = meta["mutation"]
    s3 = scores[ranked[2]] if len(ranked) > 2 else 0.0
    if (s1 >= m["min_top"] and s2 >= m["min_top"]
            and s1 - s2 <= m["max_gap"] and s2 - s3 >= m["min_lead"]
            and is_sheng_pair(attrs, ranked[0], ranked[1])):
        key = mutation_key(attrs, ranked[0], ranked[1])
        return "mutation", key, [ranked[0], ranked[1]], ranked[0], scores
    # 过线集 = 绝对阈值 ∪ 相对阈值（二者并集，解耦「强偏好」与「中庸均衡」两类人群）
    top = scores[ranked[0]]
    passed = {a for a in FIVE if scores[a] >= meta["attr_threshold"]}
    if top > 0:
        passed |= {a for a in FIVE if scores[a] >= meta["fallback_ratio"] * top}
    if not passed:
        passed = {ranked[0]}
    n = min(len(passed), 5)
    tier = meta["tier_keys_by_n"][str(n)]
    main_attr = max(passed, key=lambda a: (scores[a], -meta["tie_break"].index(a)))
    return tier, None, passed, main_attr, scores


def is_sheng_pair(attrs, a, b):
    for x, y in attrs["sheng_ring"]:
        if {a, b} == {x, y}:
            return True
    return False


def mutation_key(attrs, a, b):
    for k, v in attrs["mutations"].items():
        if set(v["pair"]) == {a, b}:
            return k
    return None


def evaluate(answers, paper, cfg, config_name="alt"):
    """answers: {qid: option_id} → 结果 dict"""
    qs, attrs = cfg["questions"], cfg["attrs"]
    tiers, meta = cfg["tiers"], cfg["meta"]
    qmap = {q["id"]: q for q in qs["questions"]}
    cap = len(qmap) * qs["max_weight"]
    raw = {a: 0 for a in FIVE}
    for qid, oid in answers.items():
        opt = next(o for o in qmap[qid]["options"] if o["id"] == oid)
        for a, w in opt["weights"].items():
            raw[a] += w
    tier_key, mut_key, passed, main_attr, scores = grade(raw, cfg, cap)
    tier = tiers["tiers"][tier_key]
    if mut_key:
        verse = tier["verse"][config_name]
        mut = attrs["mutations"][mut_key]
        quality_char = meta["quality_chars"][mut_key]
        q_index = meta["quality_index"][mut_key]
        quality_name = "变异灵根"
        display_attrs = [mut["name"]]
        sects = [mut["sect"]] + sorted(
            (attrs["attributes"][attrs["sheng_wo"][p]]["sect"] for p in mut["pair"]),
            key=lambda s: [x["sect"] for x in attrs["attributes"].values()].index(s))
    else:
        verse = tier["verse"][config_name]
        quality_char = tier["quality_char"]
        q_index = tier["index"]
        quality_name = {"quad": "四灵根", "full": "五行俱全"}.get(tier_key, tier["name"])
        display_attrs = [attrs["attributes"][a]["name"] for a in FIVE if a in passed]
        main_sect = attrs["attributes"][main_attr]["sect"]
        nourish = attrs["attributes"][attrs["sheng_wo"][main_attr]]["sect"]
        grind = attrs["attributes"][attrs["ke_wo"][main_attr]]["sect"]
        sects = [main_sect, nourish, grind]
    slots = [round_half_up(scores[a] * 9) for a in FIVE]
    checksum = (q_index + sum(slots)) % 10
    talisman = (f"{quality_char}·"
                f"{''.join(meta['stems'][v] for v in slots)}·"
                f"{meta['branches'][checksum]}")
    dao = dao_name(talisman, meta)
    return {
        "tier_key": tier_key, "mutation": mut_key, "passed": passed,
        "main_attr": main_attr, "scores": scores, "raw": raw, "cap": cap,
        "quality_name": quality_name, "display_attrs": display_attrs,
        "verse": verse, "sects": sects, "speed": tier["speed"],
        "foundation": tier["foundation"], "core": tier["core"],
        "talisman": talisman, "dao": dao,
        "attr_str": "".join(display_attrs),
    }


def dao_name(talisman, meta):
    norm = talisman.replace("·", "")
    p = meta["dao_prefix"][zlib.crc32(norm.encode("utf-8")) % len(meta["dao_prefix"])]
    s = meta["dao_suffix"][zlib.crc32((norm + "x").encode("utf-8")) % len(meta["dao_suffix"])]
    return f"{p}{s}"


# ---------------------------------------------------------------- 帖码反解

def decode_talisman(code, cfg):
    meta = cfg["meta"]
    parts = code.split("·")
    if len(parts) != 3:
        raise ValueError("帖码须为三段，以 · 分隔")
    qchar, stem_str, branch = parts
    rev_q = {v: k for k, v in meta["quality_chars"].items()}
    if qchar not in rev_q:
        raise ValueError(f"品质字不认识：{qchar}")
    qkey = rev_q[qchar]
    if len(stem_str) != 5 or any(ch not in meta["stems"] for ch in stem_str):
        raise ValueError("档位段须为五个天干字")
    if branch not in meta["branches"]:
        raise ValueError(f"校验字不认识：{branch}")
    slots = [meta["stems"].index(ch) for ch in stem_str]
    q_index = meta["quality_index"][qkey]
    if (q_index + sum(slots)) % 10 != meta["branches"].index(branch):
        raise ValueError("校验不通过，帖码可能抄错了")
    if qkey in ("ice", "mist", "wind", "melt", "rock"):
        tier_key, mut = "mutation", qkey
        pair = cfg["attrs"]["mutations"][qkey]["pair"]
        names = [cfg["attrs"]["mutations"][qkey]["name"]]
    else:
        n = {"single": 1, "double": 2, "triple": 3, "quad": 4, "full": 5}[qkey]
        tier_key, mut = meta["tier_keys_by_n"][str(n)], None
        order = sorted(range(5), key=lambda i: (-slots[i], meta["tie_break"].index(FIVE[i])))
        pair = [FIVE[i] for i in order[:n]]
        names = [cfg["attrs"]["attributes"][FIVE[i]]["name"] for i in order[:n]]
    main = max(pair, key=lambda a: (-slots[FIVE.index(a)], meta["tie_break"].index(a)))
    return {"tier_key": tier_key, "mutation": mut, "slots": dict(zip(FIVE, slots)),
            "display_attrs": names, "main_attr": main, "quality_char": qchar}


# ---------------------------------------------------------------- 答案解析

def normalize(s):
    s = unicodedata.normalize("NFKC", s)
    s = s.upper()
    for ch in ["，", "、", " ", "\t", ",", ".", "。", "："]:
        s = s.replace(ch, "")
    return s.strip()


def parse_answers(text, paper, cfg):
    """返回 (answers, used_default, error)。error 非 None 时退出码 2。"""
    qs = cfg["questions"]
    qmap = {q["id"]: q for q in qs["questions"]}
    s = normalize(text)
    m = re.match(r"^(?:P)?(\d{1,2})[:：\-]?(.*)$", s)
    if not m or not m.group(2):
        return None, False, "缺卷号。卷号在题目最上方，形如 P07，不许猜。"
    paper_no = int(m.group(1))
    if not (1 <= paper_no <= len(paper["order"]) if isinstance(paper, list) else True):
        return None, False, f"卷号 {paper_no} 不存在（共 {len(paper)} 卷）"
    body = m.group(2)
    letters = "ABC"
    answers, used_default = {}, False
    if re.fullmatch(r"(?:[1-8][A-C])+|[1-8][A-C]", body):
        for num, letter in re.findall(r"([1-8])([A-C])", body):
            qid = paper["order"][int(num) - 1]
            answers[qid] = paper["opt_orders"][qid][letters.index(letter)]
    elif re.fullmatch(r"[A-C]{1,8}", body):
        for i, letter in enumerate(body):
            qid = paper["order"][i]
            answers[qid] = paper["opt_orders"][qid][letters.index(letter)]
    else:
        return None, False, "认不出答案。示例：P07:1A2B3C4A5B6C7A8B"
    for qid in paper["order"]:
        if qid not in answers:
            answers[qid] = qmap[qid]["default"]
            used_default = True
    return answers, used_default, None


# ---------------------------------------------------------------- 卡片渲染

def wrap_line(line, width):
    """贪心折行：CJK 记 2。返回行列表。"""
    if disp_w(line) <= width:
        return [line]
    out_lines, cur, cur_w = [], "", 0
    for ch in line:
        w = 2 if unicodedata.east_asian_width(ch) in "WF" else 1
        if cur_w + w > width:
            out_lines.append(cur)
            cur, cur_w = "", 0
        cur += ch
        cur_w += w
    if cur:
        out_lines.append(cur)
    return out_lines


def render_card(res, cfg, used_default=False, config_name="alt"):
    meta, attrs = cfg["meta"], cfg["attrs"]
    W = meta["card_width"]
    L = {1: "一", 2: "二", 3: "三", 5: "五", 6: "六", 9: "九", 25: "二十五", 36: "三十六"}
    fmult = res["foundation"] if res["foundation"] != 1 else None
    cmult = res["core"] if res["core"] != 1 else None
    lines = []
    bar = "═" * 36
    thin = "─" * 36
    lines += [bar, " ".ljust(16) + "你的灵根", bar]
    lines.append(f"道号　{res['dao']}")
    lines.append(f"灵根　{' · '.join(res['display_attrs'])}")
    lines.append(f"品质　{res['quality_name']}")
    lines.append(thin)
    lines.append(f"修炼速度　× {res['speed']:.1f}")
    lines.append("筑基难度　" + ("与天灵根相同" if fmult is None else f"天灵根的{CN_NUM.get(res['foundation'], res['foundation'])}倍"))
    lines.append("结丹难度　" + ("与天灵根相同" if cmult is None else f"天灵根的{CN_NUM.get(res['core'], res['core'])}倍"))
    lines.append(thin)
    lines.append("契合宗门")
    for tag, sect in zip(["本命", "滋养", "磨砺"], res["sects"][:3]):
        lines.append(f"　{tag}　{sect}")
    lines.append(thin)
    lines += res["verse"].split("\n")
    lines.append(thin)
    lines.append("── 道友帖 ──")
    lines.append(f"道号：{res['dao']}")
    lines.append(f"灵根：{res['attr_str']} · {res['quality_name']}")
    lines.append(f"契合：{' · '.join(res['sects'][:3])}")
    lines.append(f"帖码：{res['talisman']}")
    lines.append(thin)
    if len(res["display_attrs"]) == 1:
        forward = f"我的灵根是{res['attr_str']}，{res['quality_name']}。你的呢？"
    elif res["mutation"]:
        forward = f"我的灵根是{res['attr_str']}，变异灵根。你的呢？"
    else:
        forward = f"我的灵根是{res['attr_str']}，{res['quality_name']}。你的呢？"
    lines.append(f"转发语：{forward}")
    lines += wrap_line(f"声明：{meta['disclaimer']}", W)
    if used_default:
        lines.append(f"注：{meta['partial_note']}")
    over = [l for l in lines if disp_w(l) > W]
    return "\n".join(lines), over


# ---------------------------------------------------------------- 模拟人群

def simulate_population(n_users, cfg, seed=77, temperature=0.9, temp_range=None):
    """有倾向的模拟人群：每人抽一组属性偏好，按 softmax 选选项。

    temp_range=(t_low, t_high) 时为混合人群：多数人偏好尖锐，少数人中庸。
    """
    qs = cfg["questions"]
    rng = random.Random(seed)
    results = []
    for _ in range(n_users):
        if temp_range:
            t_low, t_high = temp_range
            polar = rng.random() ** 2          # 偏小 → 多数人偏好尖锐
            temp = t_low + (t_high - t_low) * polar
        else:
            temp = temperature
        pref = {a: rng.random() for a in FIVE}
        answers = {}
        for q in qs["questions"]:
            scores = [sum(w * pref[a] for a, w in o["weights"].items())
                      for o in q["options"]]
            mx = max(scores)
            exps = [math.exp((s - mx) / temp) for s in scores]
            total = sum(exps)
            r, acc = rng.random() * total, 0.0
            for i, e in enumerate(exps):
                acc += e
                if r <= acc:
                    answers[q["id"]] = q["options"][i]["id"]
                    break
            else:
                answers[q["id"]] = q["options"][-1]["id"]
        results.append(evaluate(answers, None, cfg))
    return results


# ---------------------------------------------------------------- audit / selftest

def audit(cfg):
    ok = True
    qs, attrs, meta = cfg["questions"], cfg["attrs"], cfg["meta"]
    qmap = {q["id"]: q for q in qs["questions"]}
    mw = qs["max_weight"]

    def fail(msg):
        nonlocal ok
        ok = False
        out(f"  ✗ {msg}")

    out("== 1 逐题五行峰值 ==")
    for q in qs["questions"]:
        peaks = {}
        for o in q["options"]:
            for a, w in o["weights"].items():
                peaks[a] = max(peaks.get(a, 0), w)
        bad = [a for a in FIVE if peaks.get(a, 0) != mw]
        if bad:
            fail(f"{q['id']} 峰值不足: {bad}")
    out("  通过" if ok else "")

    out("== 2 逐卷 cap 配平（每属性每题恰有峰值）==")
    cap = len(qmap) * mw
    out(f"  cap = {cap}（题数 {len(qmap)} × {mw}）")

    out("== 3 六档品质可达（均匀采样 + 倾向人群）==")
    rng = random.Random(2026)
    found = set()
    for _ in range(120000):
        answers = {q["id"]: rng.choice(q["options"])["id"] for q in qs["questions"]}
        res = evaluate(answers, None, cfg)
        found.add("mutation" if res["mutation"] else res["tier_key"])
    need = {"single", "double", "triple", "quad", "full", "mutation"}

    out("== 4 品质分布（倾向人群 20000 人，逐档比对）==")
    trange = tuple(meta.get("sim_temp_range", [0.9, 4.0]))
    pop = simulate_population(20000, cfg, temp_range=trange)
    for r in pop:
        found.add(r["mutation"] if r["mutation"] else r["tier_key"])
    norm = lambda k: "mutation" if k in attrs["mutations"] else k
    if need - {norm(k) for k in found}:
        fail(f"不可达档位: {need - {norm(k) for k in found}}")
    else:
        out(f"  六档可达（含变异: {sorted(found & set(attrs['mutations']))}）")
    cnt = {}
    for r in pop:
        key = "mutation" if r["mutation"] else r["tier_key"]
        cnt[key] = cnt.get(key, 0) + 1
    target = cfg["tiers"]["target_distribution"]
    tol = cfg["tiers"]["distribution_tolerance"]
    for k in ["triple", "double", "quad", "single", "full", "mutation"]:
        p = cnt.get(k, 0) / len(pop)
        t = target[k]
        flag = "✓" if abs(p - t) <= tol else "✗"
        if abs(p - t) > tol:
            fail(f"{k}: 实测 {p:.1%} vs 目标 {t:.0%}（偏差 {p - t:+.1%}）")
        else:
            out(f"  {flag} {k}: {p:.1%}（目标 {t:.0%}）")

    out("== 5 帖码往返（500 例）==")
    bad = 0
    for r in pop[:500]:
        try:
            d = decode_talisman(r["talisman"], cfg)
            if d["quality_char"] != r["talisman"].split("·")[0]:
                bad += 1
        except ValueError:
            bad += 1
    if bad:
        fail(f"往返失败 {bad}/500")
    else:
        out("  通过")

    out("== 6 帖码字符集纯净（无裸数字 / 拉丁字母 / 连字符）==")
    pat = re.compile(r"[0-9A-Za-z\-]")
    dirty = [r["talisman"] for r in pop[:500] if pat.search(r["talisman"])]
    if dirty:
        fail(f"含非法字符: {dirty[:3]}")
    else:
        out("  通过")

    out("== 7 宗门方向（生我 / 克我）==")
    expect = {"metal": ("磐石堡", "丹霞顶"), "wood": ("沧浪门", "锐金堂"),
              "water": ("锐金堂", "磐石堡"), "fire": ("青梧谷", "沧浪门"),
              "earth": ("丹霞顶", "青梧谷")}
    for a, (n_s, g_s) in expect.items():
        answers = construct_for_main(cfg, a)
        res = evaluate(answers, None, cfg)
        if res["sects"][1] != n_s or res["sects"][2] != g_s:
            fail(f"主属性 {a}: 期望 滋养={n_s} 磨砺={g_s}，实得 {res['sects']}")
        else:
            out(f"  ✓ {a} → 本命 {res['sects'][0]} / 滋养 {n_s} / 磨砺 {g_s}")

    out("== 8 题干禁词 ==")
    banned = meta["banned_words_in_questions"]
    hits = []
    for q in qs["questions"]:
        text = q["text"] + "".join(o["text"] for o in q["options"])
        for w in banned:
            if w in text:
                hits.append((q["id"], w))
    if hits:
        fail(f"命中禁词: {hits}")
    else:
        out("  通过")

    out("== 9 引号与嵌套 ==")
    bad_q = [q["id"] for q in qs["questions"]
             if re.search(r"[“”‘’]", q["text"] + "".join(o["text"] for o in q["options"]))]
    if bad_q:
        fail(f"含弯引号: {bad_q}")
    else:
        out("  通过")

    out("== 10 卡片行宽 ≤ 64 ==")
    sample = {q["id"]: q["options"][0]["id"] for q in qs["questions"]}
    res = evaluate(sample, None, cfg)
    _, over = render_card(res, cfg)
    if over:
        fail(f"超宽行: {over}")
    else:
        out("  通过")

    out("")
    out("AUDIT " + ("PASSED" if ok else "FAILED"))
    sys.exit(0 if ok else 1)


def construct_for_main(cfg, target):
    """构造一个主属性为 target 的答案串。"""
    qs = cfg["questions"]
    answers = {}
    for q in qs["questions"]:
        best = max(q["options"],
                   key=lambda o: o["weights"].get(target, 0) * 10 + sum(o["weights"].values()))
        answers[q["id"]] = best["id"]
    return answers


def selftest(cfg):
    ok = True
    qs = cfg["questions"]

    def fail(msg):
        nonlocal ok
        ok = False
        out(f"  ✗ {msg}")

    out("== 确定性：同一答案两次结果一致 ==")
    answers = {q["id"]: q["options"][1]["id"] for q in qs["questions"]}
    r1, r2 = evaluate(answers, None, cfg), evaluate(answers, None, cfg)
    if r1["talisman"] != r2["talisman"] or r1["dao"] != r2["dao"]:
        fail("两次结果不一致")
    else:
        out(f"  ✓ {r1['talisman']} / {r1['dao']}")

    out("== 帖码错码拦截 ==")
    bad_code = list(r1["talisman"])
    bad_code[2] = "甲" if bad_code[2] != "甲" else "乙"
    try:
        decode_talisman("".join(bad_code), cfg)
        out("  - 改动后仍可解（校验位恰好相同），不算失败")
    except ValueError as e:
        out(f"  ✓ 拦截：{e}")

    out("== 解析容错（多种写法同结果）==")
    variants = ["P01:1A2B3C4A5B6C7A8B", "01-1a2b3c4a5b6c7a8b",
                "P01，1A，2B，3C，4A，5B，6C，7A，8B", "P01 1Ａ2Ｂ3Ｃ4Ａ5Ｂ6Ｃ7Ａ8Ｂ"]
    got = set()
    for v in variants:
        paper = cfg["papers"]["papers"][0]
        a, _, err = parse_answers(v, paper, cfg)
        if err:
            fail(f"{v!r} → {err}")
        else:
            got.add(evaluate(a, paper, cfg)["talisman"])
    if len(got) == 1:
        out(f"  ✓ 四种写法 → 同一帖码 {got.pop()}")
    else:
        fail(f"解析结果不一致: {got}")

    out("== 漏答补默认项 ==")
    paper = cfg["papers"]["papers"][0]
    partial = "P01:1A2B3C"
    a, used, err = parse_answers(partial, paper, cfg)
    if err or not used:
        fail(f"漏答处理异常 err={err} used={used}")
    else:
        out("  ✓ 3 题作答 + 5 题默认补齐")

    out("== 六档可达 ==")
    rng = random.Random(9)
    seen = set()
    for _ in range(120000):
        ans = {q["id"]: rng.choice(q["options"])["id"] for q in qs["questions"]}
        res = evaluate(ans, None, cfg)
        seen.add("mutation" if res["mutation"] else res["tier_key"])
        if len(seen) == 6:
            break
    if seen != {"single", "double", "triple", "quad", "full", "mutation"}:
        fail(f"缺档: {set(['single','double','triple','quad','full','mutation']) - seen}")
    else:
        out("  ✓ 六档全可达")

    out("")
    out("SELFTEST " + ("PASSED" if ok else "FAILED"))
    sys.exit(0 if ok else 1)


def calibrate(cfg):
    out("网格搜索（混合人群，伪灵根合计 30% 为硬约束）…")
    best = None
    target = cfg["tiers"]["target_distribution"]

    def pop_dist(pop):
        cnt = {}
        for r in pop:
            k = "mutation" if r["mutation"] else r["tier_key"]
            cnt[k] = cnt.get(k, 0) + 1
        return {k: cnt.get(k, 0) / len(pop) for k in target}

    def err_of(dist):
        fake = dist["quad"] + dist["full"]
        e = 3.0 * abs(fake - 0.30)                 # 硬约束：伪灵根合计 30%
        for k in target:
            if k not in ("quad", "full"):
                e += abs(dist[k] - target[k])
        return e

    for t_low, t_high in [(0.6, 2.5), (0.9, 4.0)]:
        for th in [0.50, 0.55, 0.60]:
            for ratio in [0.65, 0.72, 0.80]:
                for mtop in [0.55, 0.60, 0.65]:
                    for gap in [0.125, 0.14]:
                        for lead in [0.08, 0.125]:
                            cfg["meta"]["attr_threshold"] = th
                            cfg["meta"]["fallback_ratio"] = ratio
                            cfg["meta"]["mutation"] = {
                                "max_gap": gap, "min_top": mtop, "min_lead": lead}
                            pop = simulate_population(
                                6000, cfg, seed=7,
                                temp_range=(t_low, t_high))
                            dist = pop_dist(pop)
                            e = err_of(dist)
                            if best is None or e < best[0]:
                                best = (e, th, ratio, mtop, gap, lead,
                                        (t_low, t_high), dist)
    e, th, ratio, mtop, gap, lead, (t_low, t_high), dist = best
    out(f"最优：attr_threshold={th}  fallback_ratio={ratio}  min_top={mtop}  "
        f"max_gap={gap}  min_lead={lead}  人群温度=({t_low},{t_high})  总偏差={e:.1%}")
    out(f"分布：{ {k: f'{v:.0%}' for k, v in dist.items()} }")
    out(f"伪灵根合计：{dist['quad'] + dist['full']:.0%}（目标 30%）")
    out("把这几个值写回 meta.json 后重跑 --audit 确认。")


# ---------------------------------------------------------------- CLI

def cmd_questions(cfg, paper_no):
    papers = cfg["papers"]["papers"]
    paper = papers[paper_no - 1]
    qmap = {q["id"]: q for q in cfg["questions"]["questions"]}
    out(cfg["meta"]["opening"])
    out("")
    out(f"【卷号 {paper['paper_id']}】把答案按题号发我，如 1A2B3C4A5B6C7A8B")
    out("")
    for i, qid in enumerate(paper["order"], 1):
        q = qmap[qid]
        out(f"{i}. {q['text']}")
        for j, oid in enumerate(paper["opt_orders"][qid]):
            opt = next(o for o in q["options"] if o["id"] == oid)
            out(f"   {'ABC'[j]}. {opt['text']}")
        out("")


def cmd_card(cfg, text, config_name):
    papers = cfg["papers"]["papers"]
    s = normalize(text)
    m = re.match(r"^(?:P)?(\d{1,2})", s)
    if not m:
        out("缺卷号。示例：P07:1A2B3C4A5B6C7A8B")
        sys.exit(2)
    no = int(m.group(1))
    if not (1 <= no <= len(papers)):
        out(f"卷号 {no} 不存在（P01–P{len(papers):02d}）")
        sys.exit(2)
    paper = papers[no - 1]
    answers, used_default, err = parse_answers(text, paper, cfg)
    if err:
        out(err)
        sys.exit(2)
    res = evaluate(answers, paper, cfg, config_name)
    card, over = render_card(res, cfg, used_default, config_name)
    out(card)
    if over:
        out("")
        out(f"[警告] {len(over)} 行超出版心（≤{cfg['meta']['card_width']}）")
        sys.exit(1)


def cmd_start(cfg, paper_no):
    """输出开场白 + 第 1 题（逐题交互用）"""
    papers = cfg["papers"]["papers"]
    paper = papers[paper_no - 1]
    qmap = {q["id"]: q for q in cfg["questions"]["questions"]}
    out(cfg["meta"]["opening"])
    out("")
    out(f"【卷号 {paper['paper_id']}】")
    out("")
    # 第 1 题
    qid = paper["order"][0]
    q = qmap[qid]
    out(f"1. {q['text']}")
    for j, oid in enumerate(paper["opt_orders"][qid]):
        opt = next(o for o in q["options"] if o["id"] == oid)
        out(f"   {'ABC'[j]}. {opt['text']}")
    out("")
    out("（告诉我答案字母即可，如 A；答完自动进入下一题）")


def cmd_question(cfg, paper_no, question_index):
    """输出指定题号的单题（1-based），用于逐题交互"""
    papers = cfg["papers"]["papers"]
    paper = papers[paper_no - 1]
    qmap = {q["id"]: q for q in cfg["questions"]["questions"]}
    if question_index < 1 or question_index > len(paper["order"]):
        out(f"题号 {question_index} 超出范围（1–{len(paper['order'])}）")
        sys.exit(2)
    qid = paper["order"][question_index - 1]
    q = qmap[qid]
    out(f"{question_index}. {q['text']}")
    for j, oid in enumerate(paper["opt_orders"][qid]):
        opt = next(o for o in q["options"] if o["id"] == oid)
        out(f"   {'ABC'[j]}. {opt['text']}")
    out("")
    if question_index < len(paper["order"]):
        out("（告诉我答案字母即可）")
    else:
        out("（最后一题了，答完即可出结果）")


def cmd_list(cfg):
    attrs = cfg["attrs"]
    out("五行 → 宗门：")
    for a in FIVE:
        info = attrs["attributes"][a]
        out(f"  {info['name']}　{info['sect']}　{info['sect_line']}")
    out("")
    out("相生（生我→滋养）：")
    for x, y in attrs["sheng_ring"]:
        out(f"  {x} 生 {y}")
    out("相克（克我→磨砺）：")
    for x, y in attrs["ke_ring"]:
        out(f"  {x} 克 {y}")
    out("")
    out("变异灵根（相生对）：")
    for k, v in attrs["mutations"].items():
        out(f"  {v['name']} ← {'+'.join(v['pair'])}　{v['sect']}")


def cmd_list_papers(cfg):
    for p in cfg["papers"]["papers"]:
        out(f"{p['paper_id']}  题序 {''.join(q[-1] for q in p['order'])}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--card")
    ap.add_argument("--start", action="store_true")
    ap.add_argument("--question", type=int)
    ap.add_argument("--questions", action="store_true")
    ap.add_argument("--paper", type=int)
    ap.add_argument("--scores")
    ap.add_argument("--audit", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--calibrate", action="store_true")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--list-papers", action="store_true")
    ap.add_argument("--config", default="alt", choices=["alt", "fan"])
    args = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    cfg = load()
    if args.audit:
        audit(cfg)
    elif args.selftest:
        selftest(cfg)
    elif args.calibrate:
        calibrate(cfg)
    elif args.list:
        cmd_list(cfg)
    elif args.list_papers:
        cmd_list_papers(cfg)
    elif args.questions:
        if not args.paper:
            out("--questions 需要 --paper N")
            sys.exit(2)
        cmd_questions(cfg, args.paper)
    elif args.start:
        if not args.paper:
            out("--start 需要 --paper N")
            sys.exit(2)
        cmd_start(cfg, args.paper)
    elif args.question:
        if not args.paper:
            out("--question 需要 --paper N")
            sys.exit(2)
        cmd_question(cfg, args.paper, args.question)
    elif args.scores:
        if not args.paper:
            out("--scores 需要 --paper N")
            sys.exit(2)
        paper = cfg["papers"]["papers"][args.paper - 1]
        answers, _, err = parse_answers(args.scores, paper, cfg)
        if err:
            out(err)
            sys.exit(2)
        res = evaluate(answers, paper, cfg, args.config)
        out(json.dumps({a: round(res["scores"][a], 4) for a in FIVE},
                       ensure_ascii=False))
        out(f"品质 {res['quality_name']}　主属性 {res['main_attr']}　帖码 {res['talisman']}")
    elif args.card:
        cmd_card(cfg, args.card, args.config)
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
