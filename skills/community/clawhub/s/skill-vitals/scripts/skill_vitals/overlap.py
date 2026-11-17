"""Lexical overlap candidate analysis and rendering."""

import json
import re
from pathlib import Path

# ── overlap：字面相似度筛选（PRODUCT §5.4）─────────────────
#
# 这一块是**筛选器，不是判决**。语义竞争完全可能发生在用词毫无交集的两个
# skill 之间，Jaccard 查不到；反过来，两个都在讲「文件」的 skill 也未必真
# 争抢。所以输出里必须带 [Lexical，待判定]，并给出下一步怎么拿到真判断。
#
# 判断为什么不放进这个脚本：它不是正则问题（同 SKILL.md 的 2.3）。
# 脚本负责测量，模型负责判断 —— 这条分界是整个设计的支点。

# `overlap` 与 `doctor` 的 SV401 必须用**同一个**阈值，否则 doctor 说有 3 对、
# overlap 列出 5 对，两条命令在同一份数据上给出两个答案。
DEFAULT_OVERLAP_MIN = 0.25

# 停用词只挡真正没有区分度的功能词。**宁可少挡**：挡多了会把两个本来
# 就该被看见的 skill 的共享词全滤掉，只剩一个孤零零的 Jaccard 数字。
_STOP_EN = {
    "a", "an", "the", "and", "or", "of", "to", "for", "in", "on", "at", "by",
    "with", "from", "this", "that", "these", "those", "is", "are", "be", "was",
    "were", "it", "its", "you", "your", "as", "if", "when", "then", "than",
    "can", "will", "should", "would", "may", "must", "not", "no", "any", "all",
    "use", "uses", "used", "using", "skill", "skills", "user", "users", "via",
}
_STOP_ZH = set("的了和与或在是为对把被就都也还很更最之及其等这那有个上下前后中")


def _cjk_runs(text):
    """按标点切成若干串中文字符。bigram 与展示短语都基于它。

    二元组**不跨串**：跨过标点把「导出。图片」拼成一个词是凭空造词。

    **不在这里删停用字。**删了之后「在线文档」会变成「线文档」，展示时
    打出来的是一个原文里根本没有的说法 —— 而这条输出的全部用处就是让人
    自己判断两个 skill 是不是在讲同一件事。噪声改在 bigram 那层挡：
    只丢弃**两个字都是虚词**的组合，「在线」这种一实一虚的照常保留。
    """
    return re.findall(r"[一-鿿]+", text)


def _tokenize(text):
    """英文按词、中文按字二元组。

    中文不做分词：**引入词典就引入了一个必须随语料更新的依赖**，而这里
    只需要「有没有共同的说法」这个粗粒度信号。二元组在这个用途上够用，
    且两个实现能逐字节对齐 —— 分词器做不到这一点。
    """
    tokens = set()
    for m in re.finditer(r"[A-Za-z][A-Za-z0-9_-]*", text):
        w = m.group(0).lower()
        if len(w) > 1 and w not in _STOP_EN:
            tokens.add(w)
    for run in _cjk_runs(text):
        for i in range(len(run) - 1):
            a, b = run[i], run[i + 1]
            if a in _STOP_ZH and b in _STOP_ZH:
                continue
            tokens.add(a + b)
    return tokens


def _shared_display(a_text, b_text, inter, df):
    """把交集整理成**能读的**共享词。

    二元组适合算相似度，不适合给人看：直接打印会得到
    `云文 · 件夹 · 件管` 这样的半个词，读者无法据此判断这两个 skill
    是不是真的在讲同一件事 —— 而那正是这条输出唯一的用处。

    所以展示时把连续命中的二元组接回长串，并且**要求接出来的串在两边
    的原文里都真的出现过**。否则「云文」+「文档」能接出一个谁都没写过的
    词，那就是凭空造证据。
    """
    en = {t for t in inter if t.isascii()}
    b_runs = _cjk_runs(b_text)
    phrases = set()
    for run in _cjk_runs(a_text):
        i = 0
        while i < len(run) - 1:
            if run[i] + run[i + 1] in inter:
                j = i + 1
                while j < len(run) - 1 and run[j] + run[j + 1] in inter:
                    j += 1
                phrase = run[i:j + 1]
                if any(phrase in r for r in b_runs):
                    phrases.add(phrase)
                i = j + 1
            else:
                i += 1

    def rank(t):
        # 罕见的排前面。短语的 df 取组成它的二元组里最小的那个：
        # 一个短语不可能比它最罕见的组成部分更常见。
        if t.isascii():
            d = df.get(t, 0)
        else:
            d = min(df.get(t[k] + t[k + 1], 0) for k in range(len(t) - 1))
        return (d, -len(t), t)

    return sorted(en | phrases, key=rank)


def overlap_pairs(out, min_jaccard, top=None):
    """两两比较描述的字面相似度。

    只比**同一 conflict_domain 内、且真的进了上下文**的那批：不同宿主是
    互不相干的运行时，未加载的副本压根不在选择器里 —— 把它们算进来会报出
    一堆用户无法验证也无需处理的「重叠」。这与预算、冲突用的是同一条口径。

    去重键与冲突判定一致 `(conflict_domain, namespace, name)`：同一个 skill
    的多份副本不该跟自己重叠。
    """
    seen, items = set(), []
    for s in out["skills"]:
        if not s.get("loaded"):
            continue
        key = (s.get("conflict_domain"), s.get("namespace") or "", s["name"])
        if key in seen:
            continue
        seen.add(key)
        label = ("%s:%s" % (s["namespace"], s["name"])) if s.get("namespace") else s["name"]
        text = "%s %s" % (s["name"], s.get("description") or "")
        items.append({
            "name": label,
            "domain": s.get("conflict_domain"),
            "text": text,
            "tokens": _tokenize(text),
        })
    # 罕见词优先展示：两个 skill 都提到「文件」说明不了什么，
    # 都提到「webhook」才是线索。df 在**本次比较范围内**统计。
    df = {}
    for it in items:
        for t in it["tokens"]:
            df[t] = df.get(t, 0) + 1

    items.sort(key=lambda x: x["name"])
    pairs = []
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            a, b = items[i], items[j]
            if a["domain"] != b["domain"]:
                continue
            inter = a["tokens"] & b["tokens"]
            union = a["tokens"] | b["tokens"]
            if not union:
                continue
            jac = len(inter) / len(union)
            if jac < min_jaccard:
                continue
            shared = _shared_display(a["text"], b["text"], inter, df)
            pairs.append({"a": a["name"], "b": b["name"], "domain": a["domain"],
                          "jaccard": round(jac, 2), "shared": shared[:6],
                          "shared_total": len(inter)})
    pairs.sort(key=lambda p: (-p["jaccard"], p["a"], p["b"]))
    return pairs[:top] if top else pairs


def render_overlap(out, args):
    scope = sum(1 for s in out["skills"] if s.get("loaded"))
    pairs = overlap_pairs(out, args.min, args.top)

    if args.json:
        Path(args.json).write_text(
            json.dumps(pairs, ensure_ascii=False, indent=2), encoding="utf-8")
        print("Wrote %s: %d pairs" % (args.json, len(pairs)))
        return

    print("Overlap candidates                          [Lexical, review required]")
    print()
    if not pairs:
        print("  No pair among %d loaded skills has lexical similarity >= %.2f." % (scope, args.min))
        print()
        print("  This does not mean there is no semantic competition. Skills with")
        print("  completely different wording can still compete; see the next step below.")
    else:
        for p in pairs:
            print("  %s  ↔  %s" % (p["a"], p["b"]))
            # 展示的是接回长串后的说法，条数与 Jaccard 的分子不是一回事，
            # 所以后缀写「字面交集共 N 项」而不是「等 N 个」—— 后者会被
            # 读成「共享词还有 N-6 个没列出来」。
            print("    Shared terms  %s%s" % (
                " · ".join(p["shared"]) or "(no complete shared phrase; bigram similarity only)",
                "" if p["shared_total"] <= len(p["shared"])
                else "   (%d lexical intersections total)" % p["shared_total"]))
            print("    Jaccard       %.2f" % p["jaccard"])
            print()
        print("  This is a lexical filter, not a verdict. Semantic competition can")
        print("  occur between skills with completely different wording.")
    print()
    print("  To obtain a decision you can act on:")
    print("    · Run /skill-vitals in Claude Code (free; no API key required).")
    print("      Let the model judge the description fields; this is not a regex problem.")
    print("    · overlap --judge (external model) is not implemented yet; see PRODUCT §5.4.")
    print()
    print("  Scope: %d loaded skills, grouped by host; threshold --min %.2f" % (scope, args.min))
