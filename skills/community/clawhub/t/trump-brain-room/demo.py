#!/usr/bin/env python3
"""
demo.py — 不装 Claude Code 也能看到「谁来发言」。

这个脚本只做**确定性**的那一半：读 data/trump-profile.json（谁、声音多大）
和 data/topic-memory.json（最近在聊什么），把一个话题路由到 3-5 个十神，
并打印出面板结构。

它**不生成台词** —— 台词是模型的事。台词部分见 README 的真实输出示例，
或者直接装插件跑 /trump:ask。

用法:
    python3 demo.py "对伊朗动武"
    python3 demo.py "the trade deal" --en
    python3 demo.py --roster

零依赖：只用 Python 3 标准库。
"""

import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "data")

# ---------------------------------------------------------------------------
# ⚠️ **这个文件是一份政策，不是一份数据。**
#
# @David_: "A routing table embedded as a lookup table, rather than as a named policy,
# is maintained as data — subject to copy drift, staleness, incremental inconsistency —
# while its effects are policy-level. Nobody reviews a data file for governance
# implications."
#
# **它规定的是「哪些对话配得上被讨论」** —— 这是一项政策判断，不是配置。
# → 改它需要**政策审查**，不是数据审查。
# → 「数据所有者复制粘贴就改；政策所有者要给出理由。」
#
# ⚠️ **它和 data/trump-profile.json 的名册是两份会漂移的副本。**
#    名册删掉一个人，这张表还点着他 → **悬空引用**。
#    → `policy_consistency()` 专门查这个；PROBE 16 每次跑都查。
#    → 没有这条检查，漂移只能靠肉眼发现，而漂移的后果是**静默的**。
# ---------------------------------------------------------------------------
STATIC_ROUTING = {
    "military": (["qisha", "zhengguan", "jiecai"], "军事/安全/战争"),
    "deal": (["shishen", "zhengcai", "piancai"], "交易/谈判/贸易"),
    "media": (["shangguan", "bijian", "pianyin"], "媒体攻击/假新闻"),
    "ego": (["bijian", "pianyin", "jiecai"], "自我吹嘘/竞选"),
    "rival": (["jiecai", "qisha", "shangguan"], "竞争对手/敌人"),
    "family": (["zhengyin", "bijian", "pianyin"], "家族/传承/个人"),
    "money": (["piancai", "zhengcai", "shishen"], "经济/商业/地产"),
    "policy": (["zhengguan", "bijian", "pianyin"], "选举/政策/法案"),
    "tech": (["pianyin", "shishen", "shangguan"], "科技/社交媒体"),
}

FALLBACK_KEYWORDS = {
    "military": ["military", "iran", "dominance", "hormuz", "nuclear", "warrior",
                 "lethal", "airman", "war", "strike", "army", "nuke",
                 "伊朗", "军事", "动武", "战争", "袭击", "导弹", "核", "军队",
                 "轰炸", "开战", "士兵", "航母"],
    "deal": ["tariff", "tariffs", "jobs", "deal", "billions", "trade", "deals",
             "deficit", "negotiat", "contract",
             "关税", "贸易", "交易", "谈判", "协议", "合同", "出口", "进口", "经济"],
    "media": ["fake news", "new york times", "cnn", "media", "failing", "circulation",
              "假新闻", "媒体", "记者", "电视台", "报纸", "收视"],
    "ego": ["me ", "my", "i am", "me,", "history", "greatest", "best", "approval",
            "我", "最强", "最棒", "历史", "伟大", "政绩"],
    "rival": ["illegal", "border", "migrant", "migrants", "alien", "deport",
              "immigration", "enemy", "competitor", "rival",
              "边境", "移民", "非法", "敌人", "对手", "竞争", "驱逐"],
    "family": ["family", "fred", "dynasty", "inherit",
               "家族", "父亲", "儿子", "女儿", "传承", "遗产"],
    "money": ["real estate", "property", "tower", "brand", "profit", "revenue",
              "地产", "房产", "利润", "收入", "品牌", "生意", "商业"],
    "policy": ["president", "america", "democrat", "election", "republican",
               "vote", "white house", "administration", "bill", "law",
               "总统", "选举", "政策", "法案", "民主", "白宫", "政府"],
    "tech": ["tiktok", "ai", "chip", "semiconductor", "app", "social media",
             "instagram", "tesla", "tech",
             "科技", "芯片", "人工智能", "社交", "禁令", "应用"],
}

LEVEL_RULE = [
    (4.0, "旺", "声音洪亮自信，长发言（2-3 句），像在集会演讲"),
    (2.0, "中", "正常发言（1-2 句）"),
    (0.5, "弱", "声音小，在角落嘀咕，简短（1 句）"),
    (-1.0, "几乎听不见", "极简短，像远处传来的耳语"),
]


# --- 可达性哨兵（reachability sentinels） ---------------------------------
# @solanize: "the number does not carry its own validity" —— 一个 0.0% 可能是
# "扰动没动"，也可能是"根本没走到那一层"。这两句话在输出里必须不是同一个格子。
# 做法：每一层在**真的被进入**的时候自己加一个计数；探针把这个计数和读数一起报。
# 于是"零观测"和"零变化"不再共享一个格子。
REACH = {}


def _reach(key, n=1):
    REACH[key] = REACH.get(key, 0) + n
    return REACH[key]


def reach_reset():
    REACH.clear()


def reach_snapshot():
    return dict(REACH)


def render_persona_line(key, profile):
    """生成一个人格台词行。**探针从不调用它** —— 所以 persona_text_entered 恒为 0，
    而这正是探针自己该说出口的话：这一层从未被观测。"""
    _reach("persona_text_entered")
    g = profile["tenGods"][key]
    return f"{g['name']}·{g['persona']}·{level_of(g.get('score', 0))}"


def load(name):
    path = os.path.join(DATA, name)
    if not os.path.exists(path):
        sys.exit(f"缺少数据文件：{path}")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def level_of(score):
    for threshold, label, _ in LEVEL_RULE:
        if score >= threshold:
            return label
    return "几乎听不见"


def strip_marker(text):
    """'七杀（主）' -> '七杀'"""
    out = []
    for ch in text:
        if ch in "（(【[":
            break
        out.append(ch)
    return "".join(out).strip()


def name_to_key(profile, cn_name):
    for key, g in profile["tenGods"].items():
        if g["name"] == cn_name:
            return key
    return None


def score_topic(topic, topic_memory):
    """返回 (命中条数, [topic dict...])，按命中数降序。"""
    low = topic.lower()
    hits = []
    for t in topic_memory.get("topics", []):
        n = sum(1 for kw in t.get("matched_keywords", []) if kw.lower() in low)
        if n:
            hits.append((n, t))
    hits.sort(key=lambda x: -x[0])
    return hits


def score_static(topic):
    low = topic.lower()
    hits = []
    for cat, (gods, label) in STATIC_ROUTING.items():
        n = sum(1 for kw in FALLBACK_KEYWORDS[cat] if kw in low)
        if n:
            hits.append((n, cat, label, gods))
    hits.sort(key=lambda x: -x[0])
    return hits


def choose(topic, profile, topic_memory):
    """路由决策：返回 (选中的 key 列表, 决策来源说明)。"""
    _reach("routing_entered")
    dyn = score_topic(topic, topic_memory)
    if dyn and dyn[0][0] >= 2:
        n, t = dyn[0]
        keys = []
        for cn in t.get("ten_gods", []):
            k = name_to_key(profile, strip_marker(cn))
            if k:
                keys.append(k)
        _reach("dynamic_corpus_hit")
        return keys, f"动态语料 topic-memory.json → {t['slug']}（命中 {n} 个关键词）"

    # 动态语料只覆盖英文语料；中文话题走静态表（中英双关键词）

    stat = score_static(topic)
    if stat and stat[0][0] >= 2:
        n, cat, label, gods = stat[0]
        _reach("static_route_hit")
        # **名册是唯一真相**：路由表里可能有**已经不在名册里的人**
        # （路由表是一份独立的手抄拷贝，见 PROBE 16）。
        # → 先按名册过滤掉，再按名册补位。
        # → 补位规则：同一条路由规则里剩下的，按**名册里还没被叫到的人**里
        #   力量最高的补（并列按 roster_rank）。补不满就少几个人上场——
        #   **宁可台上有空位，也不要台上有幽灵。**
        _roster = profile.get("tenGods", {})
        _picked = [g for g in (gods or []) if g in _roster]
        if len(_picked) < 3 and _roster:
            _called = set(_picked)
            _pool = [k for k in _roster if k not in _called]
            _pool.sort(key=lambda k: (-_roster[k].get("score", 0),
                                      _roster[k].get("roster_rank", 999)))
            for k in _pool:
                if len(_picked) >= 3:
                    break
                _picked.append(k)
        if _picked:
            _note = ""
            _dropped = [g for g in (gods or []) if g not in _roster]
            if _dropped:
                _note = ("（路由表点名的 %s 已不在名册，已剔除并按名册补位）"
                         % "/".join(_dropped))
            return _picked, f"静态路由表 → {label}（命中 {n} 个关键词）" + _note

    # 都没有：按旺/中各取，最强的人先开口
    # 决胜规则必须是**显式值**，不能是「谁先敲字」。
    # @morrowfield: with tied weights, permuting JSON keys must not change the
    # chosen set unless insertion order is explicitly declared as policy.
    # → roster_rank 是一个**值**，所以 JSON 键序怎么排都改不了结果。
    order = sorted(profile["tenGods"].items(),
                   key=lambda kv: (-kv[1].get("score", 0),
                                   kv[1].get("roster_rank", 999)))
    _reach("fallback")
    keys = [k for k, v in order[:3]]
    # 并列必须**说出来**：谁被选中是策略，谁被并列是事实，两者要分开记。
    # @spiritofthefleet: "do you log the intent (this was a tie) separately from
    # the outcome (this one won)?" —— 之前只记了结果。
    tie_note = ""
    if len(order) > 3:
        cut = order[2][1].get("score", 0)
        tied = [k for k, v in order if v.get("score", 0) == cut]
        if len(tied) > 1:
            tie_note = ("（并列 %.1f 分：%s → 按 roster_rank 显式名册位次决出）"
                        % (cut, "/".join(tied)))
    return keys, "无明确命中 → 取力量最高的 3 个十神（兜底）" + tie_note


def main():
    ap = argparse.ArgumentParser(description="trump-skill 零依赖演示")
    ap.add_argument("topic", nargs="?", help="一个话题，例如：对伊朗动武")
    ap.add_argument("--en", action="store_true", help="英文面板标题")
    ap.add_argument("--roster", action="store_true", help="只打印十神名册")
    args = ap.parse_args()

    profile = load("trump-profile.json")
    topic_memory = load("topic-memory.json")
    gods = profile["tenGods"]

    if args.roster:
        print("\n十神名册（按力量排序）\n")
        for key, g in sorted(gods.items(), key=lambda kv: -kv[1].get("score", 0)):
            sc = g.get("score", 0)
            print(f"  {g['emoji']} {g['name']}·{g['persona']}  [{level_of(sc)} {sc}]")
            print(f"      {g['description']}")
        print(f"\n当前大运：{profile['currentDayun']['meaning']}")
        print(f"当前流年：{profile['currentLiunian']['meaning']}\n")
        return

    if not args.topic:
        ap.print_help()
        return

    topic = args.topic
    keys, reason = choose(topic, profile, topic_memory)

    # 力量决定谁先说、谁更大声
    keys = sorted(keys, key=lambda k: -gods[k].get("score", 0))

    title = "Trump Brain Panel" if args.en else "特朗普脑内会议室"
    print()
    print(f"────── 🧠 {title} ──────")
    print(f"【话题】{topic}")
    print(f"【路由】{reason}")
    print()
    for k in keys:
        g = gods[k]
        sc = g.get("score", 0)
        print(f"【{g['name']}·{g['persona']}·{level_of(sc)}】{g['description']}")
        for threshold, label, rule in LEVEL_RULE:
            if label == level_of(sc):
                print(f"    （{rule}）")
                break
    print()
    print("> 台词由模型生成 —— 装上插件跑 /trump:ask，或看 README 的真实输出示例。")
    print("> 这一步只决定【谁发言、多大声、什么顺序】，这一步是确定性的。")
    print()


if __name__ == "__main__":
    main()
