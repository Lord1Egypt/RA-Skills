#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""分院帽 Skill 随机试卷生成器（构建期工具，运行期用不到）。

把 data/questions.json 的**题库**（pool）切成若干张**试卷**（paper）：
每张卷从题库里抽 paper_size 道**不重复**的题，题目顺序打乱、每题选项顺序也打乱，
并把 default 选项落在哪个位置记下来，最后写出 data/papers.json。

输出结构极简，只存「抽了哪几道、选项怎么排」：

    {"id": 7, "slots": [{"qid": 12, "order": ["C", "A", "B"]}, ... 共 paper_size 项]}

order 的含义：order[0] 展示成 A，order[1] 展示成 B，order[2] 展示成 C。
权重跟着选项一起搬运，所以任何一张卷的 cap 都仍是 paper_size × max_weight，四院天然配平
（前提是题库每题四院峰值都等于 max_weight，由 sorting_hat.py --audit 守）。

为什么把「打乱」放在构建期而不是运行期：
  页面里的 JS 和 sorting_hat.py 都要按同一份卷算分。随机数发生器一旦分两处实现，
  迟早悄悄分叉。这里把随机性一次性固化进 papers.json，运行期两边都只是**读同一份数据**。

发牌是**均衡**的：每道题在全部试卷里被抽中的次数完全相同。用的是
「多重集洗牌 + 换牌修复」，不是逐张独立抽样——独立抽样会让某些题罕见（实测最少只出现 5 次）。

用法：
    python scripts/make_papers.py                    # 默认种子生成 data/papers.json
    python scripts/make_papers.py --count 40 --seed 7
    python scripts/make_papers.py --check            # 只校验已存在的 papers.json
"""

import argparse
import io
import json
import os
import random
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA_DIR = os.path.join(ROOT, "data")

if HERE not in sys.path:
    sys.path.insert(0, HERE)
import sorting_hat as core  # noqa: E402  校验逻辑只此一份，避免两边分叉

DEFAULT_QUESTIONS = os.path.join(DATA_DIR, "questions.json")
DEFAULT_PAPERS = os.path.join(DATA_DIR, "papers.json")

EXIT_OK = 0
EXIT_CONFIG = 1

DEAL_ROUNDS = 200
REPAIR_ROUNDS = 4000


def setup_stdout():
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def deal_balanced(ids, count, paper_size, rng):
    """均衡发牌：把「每道题出现 count×paper_size/题数 次」的多重集洗牌后切成 count 份，
    再用换牌法修掉「同一份里出现同一道题」的冲突，保证每题被抽中的次数完全相同。
    """
    total = count * paper_size
    base, extra = divmod(total, len(ids))
    bag = []
    for i, qid in enumerate(ids):
        bag.extend([qid] * (base + (1 if i < extra else 0)))

    for _ in range(DEAL_ROUNDS):
        rng.shuffle(bag)
        chunks = [bag[i * paper_size:(i + 1) * paper_size] for i in range(count)]
        counts = [Counter(c) for c in chunks]
        if all(len(c) == paper_size for c in counts):
            return chunks

        # 换牌：把来源份里多出来的 x，跟目标份里多出来的 y 对调，两边都不会变差
        for _round in range(REPAIR_ROUNDS):
            moved = False
            for si, cnt in enumerate(counts):
                for x in [q for q, n in cnt.items() if n > 1]:
                    for ti, tcnt in enumerate(counts):
                        if ti == si or x in tcnt:
                            continue
                        spare = [q for q, n in tcnt.items() if n > 1]
                        if not spare:
                            continue
                        y = spare[0]
                        chunks[si][chunks[si].index(x)] = y
                        chunks[ti][chunks[ti].index(y)] = x
                        counts[si][x] -= 1
                        counts[si][y] += 1
                        counts[ti][y] -= 1
                        counts[ti][x] += 1
                        moved = True
                        break
                    if moved:
                        break
                if moved:
                    break
            if not moved:
                break
        if all(len(c) == paper_size for c in counts):
            return chunks

    raise RuntimeError("均衡发牌没能收敛，请调整 --count 或 --seed 后重试。")


def build_papers(questions_data, count, seed):
    meta = questions_data["meta"]
    questions = questions_data["questions"]
    paper_size = int(meta.get("paper_size", len(questions)))
    ids = [q["id"] for q in questions]
    keys_of = {q["id"]: [o["key"] for o in q["options"]] for q in questions}

    if len(ids) < paper_size:
        raise ValueError("题库只有 %d 道题，不够抽一张 %d 题的卷。" % (len(ids), paper_size))

    rng = random.Random(seed)
    deals = deal_balanced(ids, count, paper_size, rng)

    papers = []
    for pid, chosen in enumerate(deals, start=1):
        slots = []
        for qid in chosen:
            order = list(keys_of[qid])
            rng.shuffle(order)
            slots.append({"qid": qid, "order": order})
        papers.append({"id": pid, "slots": slots})

    return {
        "version": "1.0.0",
        "meta": {
            "paper_size": paper_size,
            "count": count,
            "seed": seed,
            "pool_size": len(ids),
            "notes": "每张卷从题库抽 paper_size 道不重复的题，题目顺序与选项顺序都已打乱并固化；"
                     "题库里每道题被抽中的次数完全相同（均衡发牌）。"
                     "order[0..2] 依次展示为 A/B/C。默认种子是 %d，改动题库后重跑 make_papers.py 即可。"
                     "运行期不做任何随机：sorting_hat.py 与页面 JS 都只读这份文件，"
                     "所以同一份答案 + 同一张卷永远得到同一张卡。" % seed,
        },
        "papers": papers,
    }


def main(argv=None):
    setup_stdout()
    parser = argparse.ArgumentParser(prog="make_papers.py",
                                     description="从题库生成随机试卷库 papers.json")
    parser.add_argument("--out", default=DEFAULT_PAPERS, help="输出路径（默认 data/papers.json）")
    parser.add_argument("--questions-file", default=DEFAULT_QUESTIONS, help="题库路径")
    parser.add_argument("--count", type=int, default=None, help="生成几张卷（默认＝题池题数）")
    parser.add_argument("--seed", type=int, default=20260915, help="随机种子，同种子输出完全一致")
    parser.add_argument("--check", action="store_true", help="只校验已存在的 papers.json，不重新生成")
    args = parser.parse_args(argv)

    questions = core.load_json(args.questions_file, "题库")

    if args.check:
        papers = core.load_json(args.out, "试卷")
    else:
        count = args.count if args.count is not None else len(questions["questions"])
        papers = build_papers(questions, count, args.seed)

    problems, infos = core.check_papers(papers, questions)
    for info in infos:
        print("  · " + info)
    if problems:
        for item in problems:
            print("[FAIL] " + item)
        print("[结果] 发现 %d 处问题" % len(problems))
        return EXIT_CONFIG
    print("[OK] 试卷结构、选项排列、逐卷 cap 配平、覆盖均衡、卷面互不相同")

    if args.check:
        return EXIT_OK

    out_path = os.path.abspath(args.out)
    parent = os.path.dirname(out_path)
    if parent and not os.path.isdir(parent):
        os.makedirs(parent)
    with io.open(out_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(papers, ensure_ascii=False, indent=1))
        fh.write("\n")

    print("[生成] %s" % out_path)
    print("  · 种子 = %d（同种子重跑输出一致）" % args.seed)
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
