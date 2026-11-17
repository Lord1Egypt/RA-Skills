#!/usr/bin/env python3
"""
smoke_test.py —— 路由冒烟测试（golden snapshot）

@logfather: "include a routing-only smoke test that (1) runs a small set of
canonical prompts exercising every rule, (2) records only selected personas,
order, and loudness, and (3) diffs against a checked-in golden snapshot.
It's repo-friendly, cheap to run in CI, and catches accidental routing drift
without invoking the model."

这个脚本**只测路由**，不测台词、不调模型：

  · 每条规范语料跑一次 demo.choose()
  · 只记三样东西：**选了谁**、**什么顺序**、**多大声**
  · 和签进仓库的 tests/golden_routing.json 对比
  · 有漂移 → 打印逐条 diff，**退出码 1**

⚠️ **golden 文件带 profile_hash**：如果 profile 变了而 golden 没重新生成，
脚本**报「条件不同」而不是「漂移」** —— 因为那不是路由坏了，是**换了被测对象**。
这两件事混在一起，就会像上一轮那样造出一个「假分歧」去误导人。

用法:
    python3 smoke_test.py            # 对比，漂移则退出码 1
    python3 smoke_test.py --update   # 重新生成 golden（改了 profile 之后要显式做）
    python3 smoke_test.py --json     # 机器可读输出
"""
import argparse
import hashlib
import json
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
import demo as D  # noqa: E402

GOLDEN = os.path.join(ROOT, "tests", "golden_routing.json")

# 规范语料与 swap_test.py 共用同一份（CANONICAL_PROMPTS）。
# 从 swap_test 导入而不是复制 —— 复制就会漂，而漂了的语料会让 golden 失去意义。
try:
    from swap_test import CANONICAL_PROMPTS
except Exception:  # pragma: no cover
    CANONICAL_PROMPTS = [
        ("对伊朗动武，军事打击", "military"),
        ("战争迷雾：导弹与航母", "military"),
        ("关税谈判与贸易协议", "deal"),
        ("这笔交易合同能不能签，谈判破裂", "deal"),
        ("假新闻：媒体和记者的报道", "media"),
        ("电视台收视下滑，报纸不印了", "media"),
        ("我最强大，史上最伟大，政绩第一", "ego"),
        ("我是谁？我最棒，历史属于我", "ego"),
        ("边境移民非法驱逐，对手国家", "rival"),
        ("竞争对手在挖我的客户，敌人出现", "rival"),
        ("家族传承：父亲的儿子女儿与遗产", "family"),
        ("家族产业的继承问题，遗产分配", "family"),
        ("地产项目的利润与收入，品牌的商业价值", "money"),
        ("这笔生意赚了多少利润，商业地产", "money"),
        ("选举与政策法案，president 对 america", "policy"),
        ("总统选举，democrat 与 republican 的政策", "policy"),
        ("社交媒体与科技平台", "tech"),
        ("推特发文，社交媒体科技公司", "tech"),
        ("今天天气不错", None),
        ("随便聊聊", None),
        ("怎么办才好呢", None),
    ]


def load(name):
    with open(os.path.join(ROOT, "data", name), encoding="utf-8") as f:
        return json.load(f)


def profile_hash(profile):
    return hashlib.sha256(
        json.dumps(profile["tenGods"], ensure_ascii=False, sort_keys=True).encode()
    ).hexdigest()[:12]


def observe(profile, topic_memory):
    """跑一遍语料，只记：选了谁、什么顺序、多大声。"""
    gods = profile["tenGods"]
    rows = []
    for topic, expect in CANONICAL_PROMPTS:
        keys, reason = D.choose(topic, profile, topic_memory)
        ordered = sorted(keys, key=lambda k: -gods[k].get("score", 0))
        rows.append({
            "topic": topic,
            "expected_route": expect,
            "routed": "fallback" if "兜底" in reason else "rule",
            # **两个顺序都要记**：
            #   selected_raw = 路由**原样**返回的顺序（路由表里写的顺序就是决策的一部分）
            #   selected     = 按音量排完的顺序（发言顺序）
            # 我第一版只记了 selected（而且是排过序的），结果**路由表里换顺序完全测不出来** ——
            # 核对方把自己要看的东西先归一化掉了，这就是上一轮那条教训的复刻：
            # **核对方不能用自己的默认值去核对别人的记录。**
            "selected_raw": list(keys),
            "selected": list(ordered),
            "names": [gods[k]["name"] for k in ordered],
            "loudness": [D.level_of(gods[k].get("score", 0)) for k in ordered],
        })
    return rows


def main():
    ap = argparse.ArgumentParser(description="路由冒烟测试（golden snapshot）")
    ap.add_argument("--update", action="store_true", help="重新生成 golden")
    ap.add_argument("--json", action="store_true", help="机器可读输出")
    args = ap.parse_args()

    profile = load("trump-profile.json")
    topic_memory = load("topic-memory.json")
    ph = profile_hash(profile)
    rows = observe(profile, topic_memory)

    if args.update or not os.path.exists(GOLDEN):
        os.makedirs(os.path.dirname(GOLDEN), exist_ok=True)
        golden = {
            "note": "路由 golden snapshot —— 只记选了谁/什么顺序/多大声。",
            "profile_hash": ph,
            "fixture": "canonical-v1",
            "rows": rows,
        }
        with open(GOLDEN, "w", encoding="utf-8") as f:
            json.dump(golden, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print(f"[UPDATE] golden 已写入 {os.path.relpath(GOLDEN, ROOT)} "
              f"(profile_hash={ph}, {len(rows)} 条)")
        return 0

    with open(GOLDEN, encoding="utf-8") as f:
        golden = json.load(f)

    # ---- 条件不同 ≠ 漂移 ----
    if golden.get("profile_hash") != ph:
        print("[COND] golden 是在**另一个 profile** 下生成的：")
        print(f"       golden profile_hash = {golden.get('profile_hash')}")
        print(f"       当前  profile_hash = {ph}")
        print("       这**不是**路由漂移，是换了被测对象。")
        print("       如果这是有意改动，跑：python3 smoke_test.py --update")
        return 2

    old = {r["topic"]: r for r in golden.get("rows", [])}
    diffs = []
    for r in rows:
        o = old.get(r["topic"])
        if o is None:
            diffs.append((r["topic"], "新增语料（golden 里没有）", None, r))
            continue
        if o.get("selected_raw") != r["selected_raw"]:
            diffs.append((r["topic"], "路由返回的顺序变了（原始顺序）",
                          o.get("selected_raw"), r["selected_raw"]))
        elif o["selected"] != r["selected"]:
            diffs.append((r["topic"], "选中的人/发言顺序变了",
                          o["selected"], r["selected"]))
        elif o["loudness"] != r["loudness"]:
            diffs.append((r["topic"], "音量档位变了", o["loudness"], r["loudness"]))
        elif o["routed"] != r["routed"]:
            diffs.append((r["topic"], "路由方式变了（规则 <-> 兜底）",
                          o["routed"], r["routed"]))

    if args.json:
        print(json.dumps({"profile_hash": ph, "n": len(rows),
                          "drift": len(diffs),
                          "diffs": [{"topic": t, "what": w, "was": a, "now": b}
                                    for t, w, a, b in diffs]},
                         ensure_ascii=False, indent=2))
        return 1 if diffs else 0

    print(f"[SMOKE] profile_hash={ph}  fixture={golden.get('fixture')}  "
          f"语料 {len(rows)} 条")
    if not diffs:
        print("[SMOKE] ✅ 无路由漂移（选了谁 / 什么顺序 / 多大声 全对）")
        return 0
    print(f"[SMOKE] ❌ 发现 {len(diffs)} 处漂移：")
    for t, w, a, b in diffs:
        print(f"  · {t}")
        print(f"      {w}: {a} -> {b}")
    print("      如果这是有意改动，跑：python3 smoke_test.py --update")
    return 1


if __name__ == "__main__":
    sys.exit(main())
