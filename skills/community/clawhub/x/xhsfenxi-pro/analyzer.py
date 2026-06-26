"""
analyzer.py — 小红书博主分析引擎
整合 xhsfenxi 三型博主分类体系 + 五层账号模型
可与 XhsClient 采集结果直接对接

用法:
    from xhscosmoskill import XhsClient
    from xhscosmoskill.analyzer import analyze_account

    with XhsClient() as xhs:
        notes = xhs.get_user_notes("user_id", limit=50)

    report = analyze_account(notes, creator_name="B 治愈系代表")
    print(report)
"""

from __future__ import annotations
from typing import List, Dict, Any
import re
from collections import Counter


# ── 三型博主分类系统 ──────────────────────────────────────────

ARCHETYPE_SIGNALS = {
    "A": {
        "name": "荒诞美学型",
        "desc": "用荒诞幽默包裹哲学内核，高质感视觉，品牌符号统一",
        "title_signals": ["（劲爆）", "劲爆", "＊", "*", "·"],
        "content_signals": ["哲", "美学", "荒诞", "飞", "高山", "宇宙", "奖励", "永恒"],
        "commercial": "高端生活方式、旅行、摄影、轻奢品牌",
        "difficulty": "高 — 依赖长期审美积累",
    },
    "B": {
        "name": "共鸣命名型",
        "desc": "把私人经历转化为普世命题，给模糊情绪命名",
        "title_signals": ["*", "为什么", "是什么", "原来", "才知道", "命题", "灯塔", "解药"],
        "content_signals": ["成长", "情绪", "留学", "记录", "年末", "不确定", "命题", "感受", "理解", "接纳"],
        "commercial": "成长/教育/创意平台、中端生活方式",
        "difficulty": "中 — 方法可学，需要真实观察力",
    },
    "C": {
        "name": "现实策略型",
        "desc": "打破职场/人际/金钱潜规则，提供可执行的向上策略",
        "title_signals": ["骗子", "不要脸", "装", "穷", "规则", "策略", "大法"],
        "content_signals": ["策略", "规则", "执行", "调整", "快速", "现实", "向上", "方法"],
        "commercial": "大众消费、职场、电商、实用工具",
        "difficulty": "中 — 框架可学，切忌复制表面攻击性",
    },
}


def classify_archetype(notes: List[Any]) -> Dict[str, Any]:
    """
    基于笔记标题关键词，初步判断博主类型。
    返回: { "type": "B", "name": "共鸣命名型", "scores": {...}, "rationale": [...] }
    """
    scores = {"A": 0, "B": 0, "C": 0}
    evidence = {"A": [], "B": [], "C": []}

    for note in notes:
        title = note.title or "" if hasattr(note, "title") else note.get("title", "")
        content = note.content or "" if hasattr(note, "content") else note.get("content", "")
        text = title + " " + content

        for typ, cfg in ARCHETYPE_SIGNALS.items():
            for sig in cfg["title_signals"]:
                if sig in title:
                    scores[typ] += 2
                    evidence[typ].append(f"标题含「{sig}」: {title[:30]}")
            for sig in cfg["content_signals"]:
                if sig in text:
                    scores[typ] += 1

    # 归一化
    total = sum(scores.values()) or 1
    pct = {k: round(v / total * 100) for k, v in scores.items()}

    best = max(scores, key=scores.get)
    second = sorted(scores, key=scores.get, reverse=True)[1]

    # 混合判断
    is_mixed = scores[second] >= scores[best] * 0.6
    if is_mixed:
        archetype_type = f"{best}+{second}"
        archetype_name = f"{ARCHETYPE_SIGNALS[best]['name']} × {ARCHETYPE_SIGNALS[second]['name']}"
    else:
        archetype_type = best
        archetype_name = ARCHETYPE_SIGNALS[best]["name"]

    rationale = evidence[best][:3] + (evidence[second][:2] if is_mixed else [])

    return {
        "type": archetype_type,
        "name": archetype_name,
        "desc": ARCHETYPE_SIGNALS[best]["desc"],
        "scores": scores,
        "pct": pct,
        "rationale": rationale,
        "commercial": ARCHETYPE_SIGNALS[best]["commercial"],
        "difficulty": ARCHETYPE_SIGNALS[best]["difficulty"],
        "is_mixed": is_mixed,
    }


# ── 数据工具 ──────────────────────────────────────────────────

def _parse_likes(v) -> int:
    if not v:
        return 0
    s = str(v).replace(",", "").strip()
    if "万" in s:
        return int(float(s.replace("万", "")) * 10000)
    try:
        return int(s)
    except ValueError:
        return 0


def _engagement_tier(likes: int) -> str:
    if likes >= 50000:
        return "爆款 🔥"
    if likes >= 10000:
        return "高量 ⭐"
    if likes >= 5000:
        return "中高量"
    if likes >= 1000:
        return "稳定量"
    return "普通"


# ── 五层账号模型 ──────────────────────────────────────────────

def build_five_layers(notes: List[Any], archetype: Dict) -> Dict[str, Any]:
    """
    提取五层账号模型:
    1. Identity    — 博主是谁（人设定位）
    2. Contract    — 用户为什么关注（情感契约）
    3. Topic       — 反复覆盖的问题/欲望（选题体系）
    4. Expression  — 标题/开头公式、品牌符号
    5. Transfer    — 可学习点 vs 不能硬抄
    """
    titles = []
    likes_list = []
    for n in notes:
        t = n.title if hasattr(n, "title") else n.get("title", "")
        lk = _parse_likes(n.likes if hasattr(n, "likes") else n.get("likes"))
        if t:
            titles.append((t, lk))
            likes_list.append(lk)

    # 选题体系：基于标题词频聚类
    topic_keywords = {
        "自然/户外": ["山", "自然", "户外", "攀岩", "跑", "溪", "飞", "森林", "海"],
        "留学/海外": ["留学", "巴黎", "欧洲", "外国", "服装生", "独居", "课后"],
        "情绪/成长": ["情绪", "成长", "失败", "不确定", "淤青", "消极", "烦恼", "困境"],
        "旅行/探索": ["旅行", "solotrip", "solo", "gap", "世界", "探索"],
        "生活哲学": ["生活", "命题", "本质", "人生", "记录", "计划", "感受", "存在", "宇宙"],
        "创作/记录": ["记录", "vlog", "日记", "分享", "创造力"],
    }

    topic_dist: Dict[str, List] = {k: [] for k in topic_keywords}
    for title, lk in titles:
        for topic, kws in topic_keywords.items():
            if any(kw in title for kw in kws):
                topic_dist[topic].append((title, lk))

    best_topic = max(topic_dist, key=lambda k: sum(x[1] for x in topic_dist[k]) / max(len(topic_dist[k]), 1))

    # 标题模式分析
    has_asterisk = sum(1 for t, _ in titles if "*" in t or "＊" in t)
    has_question = sum(1 for t, _ in titles if "为什么" in t or "如何" in t or "？" in t)
    has_contrast = sum(1 for t, _ in titles if "但" in t or "，" in t)
    has_emotion_label = sum(1 for t, _ in titles if any(w in t for w in ["模糊", "流动", "感受", "治愈", "珍贵"]))

    # 爆款标题
    top_titles = sorted(titles, key=lambda x: -x[1])[:5]

    return {
        "identity": _infer_identity(titles, archetype),
        "contract": _infer_contract(archetype),
        "topic_system": {k: len(v) for k, v in topic_dist.items() if v},
        "best_topic": best_topic,
        "best_topic_avg": round(
            sum(x[1] for x in topic_dist[best_topic]) / max(len(topic_dist[best_topic]), 1)
        ),
        "expression": {
            "asterisk_ratio": f"{has_asterisk}/{len(titles)}",
            "question_titles": has_question,
            "contrast_titles": has_contrast,
            "emotion_labels": has_emotion_label,
            "top_titles": top_titles,
        },
        "transfer": _infer_transfer(archetype),
    }


def _infer_identity(titles, archetype) -> str:
    typ = archetype["type"][0]
    if typ == "A":
        return "用荒诞美学构建独特视角的创作者，以品牌符号建立强识别度"
    if typ == "B":
        return "把私人经历转化为公共命题、擅长给模糊情绪命名的思考者"
    return "洞察现实规则、提供可执行策略的实用派创作者"


def _infer_contract(archetype) -> str:
    typ = archetype["type"][0]
    if typ == "A":
        return "看了就愉快 + 被美学震撼 + 看到了另一种看待生活的方式"
    if typ == "B":
        return "被理解 + 获得命名 + 对自己的状态有了新的视角"
    return "被验证 + 被激活 + 获得可执行的向上移动路径"


def _infer_transfer(archetype) -> Dict[str, List[str]]:
    typ = archetype["type"][0]
    if typ == "A":
        return {
            "可学": ["建立自己的品牌符号", "练习反差命名而非描述地点", "荒诞框架选题"],
            "不能硬抄": ["视觉审美需长期积累", "语气独特性不可复制"],
        }
    if typ == "B":
        return {
            "可学": ["命题化思维：私人经历→公共命题", "建立个人概念词汇库", "五步公式：经历→命题→命名→判断→共鸣"],
            "不能硬抄": ["真实性是基础，无法凭空虚构", "语气温度需与真实人设一致"],
        }
    return {
        "可学": ["找到自己的现实母题", "冲突词标题练习", "公式：困境→说破→规则→策略→爽感"],
        "不能硬抄": ["表面攻击性语气", "特定人设的羞耻感先夺法"],
    }


# ── 数据统计 ──────────────────────────────────────────────────

def compute_stats(notes: List[Any]) -> Dict[str, Any]:
    likes = [_parse_likes(n.likes if hasattr(n, "likes") else n.get("likes")) for n in notes]
    types = Counter(
        (n.type if hasattr(n, "type") else n.get("type", "unknown")) for n in notes
    )

    brackets = {"1万+": 0, "5000-9999": 0, "1000-4999": 0, "500-999": 0, "<500": 0}
    for lk in likes:
        if lk >= 10000:
            brackets["1万+"] += 1
        elif lk >= 5000:
            brackets["5000-9999"] += 1
        elif lk >= 1000:
            brackets["1000-4999"] += 1
        elif lk >= 500:
            brackets["500-999"] += 1
        else:
            brackets["<500"] += 1

    top = sorted(
        [(n.title if hasattr(n, "title") else n.get("title", ""), _parse_likes(n.likes if hasattr(n, "likes") else n.get("likes"))) for n in notes],
        key=lambda x: -x[1],
    )[:10]

    return {
        "total": len(notes),
        "video_count": types.get("video", 0),
        "normal_count": types.get("normal", 0),
        "total_likes": sum(likes),
        "avg_likes": round(sum(likes) / len(likes)) if likes else 0,
        "max_likes": max(likes) if likes else 0,
        "brackets": brackets,
        "top10": top,
    }


# ── 主入口 ────────────────────────────────────────────────────

def analyze_account(
    notes: List[Any],
    creator_name: str = "未知博主",
    mode: str = "full",
) -> str:
    """
    对采集到的笔记列表做完整分析，返回 Markdown 报告。

    参数:
        notes       — XhsClient.get_user_notes() 的返回值
        creator_name — 博主名称
        mode        — 'full' 完整报告 | 'formula' 只输出选题公式 | 'snapshot' 快速摘要

    ⭐ v2.1：full 模式自动调用 reverse_engineer 模块附加数据驱动逆向工程数据
    """
    stats = compute_stats(notes)
    archetype = classify_archetype(notes)
    five = build_five_layers(notes, archetype)

    if mode == "snapshot":
        return _render_snapshot(creator_name, stats, archetype)
    if mode == "formula":
        return _render_formula(creator_name, stats, archetype, five)
    return _render_full_report(creator_name, stats, archetype, five)


def analyze_with_reverse_engineering(notes: List[Any], creator_name: str = "未知博主") -> Dict[str, Any]:
    """
    ⭐ v2.1 新增：返回完整结构化数据（含 reverse_engineering 数据驱动洞察）

    返回字典包含：
    - stats: 基础统计
    - archetype: 三型分类
    - five_layers: 五层模型
    - reverse_engineering: 主题矩阵 / Top10vsBottom10 / 反常识 / 温度 / 内容结构
    - route: 公式生成器路线决策（B_HEALING / BA_IRONY / A / C）
    """
    from .reverse_engineer import full_reverse_engineering
    from .formula import detect_route

    stats = compute_stats(notes)
    archetype = classify_archetype(notes)
    five = build_five_layers(notes, archetype)
    reverse = full_reverse_engineering(notes)
    route = detect_route(archetype, reverse["temperature"]["primary"])

    return {
        "creator_name": creator_name,
        "stats": stats,
        "archetype": archetype,
        "five_layers": five,
        "reverse_engineering": reverse,
        "route": route,
        "_meta": {"version": "v2.1", "engine": "xhsfenxi-pro"},
    }


# ── 渲染函数 ──────────────────────────────────────────────────

def _render_snapshot(name, stats, archetype) -> str:
    return f"""# {name} — 快速摘要

| 指标 | 数值 |
|------|------|
| 分析笔记 | {stats['total']} 篇 |
| 视频占比 | {stats['video_count']}/{stats['total']} |
| 平均点赞 | {stats['avg_likes']:,} |
| 最高单篇 | {stats['max_likes']:,} |
| 博主类型 | **{archetype['name']}** ({archetype['type']}) |
| 商业适配 | {archetype['commercial']} |
"""


def _render_formula(name, stats, archetype, five) -> str:
    top_topic = five["best_topic"]
    top_avg = five["best_topic_avg"]
    transfer = five["transfer"]

    top_titles_md = "\n".join(
        f"- 👍{lk:,} {t[:50]}" for t, lk in five["expression"]["top_titles"]
    )
    can_learn = "\n".join(f"- ✅ {x}" for x in transfer["可学"])
    cant_copy = "\n".join(f"- ❌ {x}" for x in transfer["不能硬抄"])

    return f"""# {name} — 爆款选题公式

> 类型：{archetype['name']} | 平均点赞：{stats['avg_likes']:,} | 最高：{stats['max_likes']:,}

## 一、为什么能做出爆款？

博主类型：**{archetype['name']}**
{archetype['desc']}

核心公式：{_get_core_formula(archetype['type'][0])}

## 二、最强选题方向

最高互动主题：**{top_topic}**（均赞 {top_avg:,}）

## 三、爆款标题参考

{top_titles_md}

## 四、标题模式

- 含 * 符号：{five['expression']['asterisk_ratio']}（情感标记）
- 疑问句式：{five['expression']['question_titles']} 篇
- 情绪词命名：{five['expression']['emotion_labels']} 篇

## 五、可学 / 不能硬抄

{can_learn}

{cant_copy}
"""


def _render_full_report(name, stats, archetype, five) -> str:
    topic_table = "\n".join(
        f"| {t} | {c}篇 |"
        for t, c in sorted(five["topic_system"].items(), key=lambda x: -x[1])
    )

    brackets_md = "\n".join(
        f"| {k} | {'█' * v} {v}篇 |"
        for k, v in stats["brackets"].items()
    )

    top10_md = "\n".join(
        f"| {i+1} | 👍{lk:,} | {_engagement_tier(lk)} | {t[:45]} |"
        for i, (t, lk) in enumerate(stats["top10"])
    )

    rationale_md = "\n".join(f"- {r}" for r in archetype["rationale"]) or "- 基于内容风格综合判断"
    can_learn = "\n".join(f"- ✅ {x}" for x in five["transfer"]["可学"])
    cant_copy = "\n".join(f"- ❌ {x}" for x in five["transfer"]["不能硬抄"])

    return f"""# {name} — 结构化分析报告

> 数据来源：小红书公开主页，样本量 {stats['total']} 篇

---

## 一、账号快照

| 指标 | 数值 |
|------|------|
| 分析样本 | {stats['total']} 篇 |
| 视频/图文 | {stats['video_count']} / {stats['normal_count']} |
| 总点赞 | {stats['total_likes']:,} |
| 平均点赞 | {stats['avg_likes']:,} |
| 最高单篇 | {stats['max_likes']:,} |
| 爆款（1万+） | {stats['brackets']['1万+']} 篇 |

---

## 二、账号类型判断

**类型：** {archetype['name']} ({archetype['type']})
**核心内核：** {archetype['desc']}
**判断依据：**
{rationale_md}

---

## 三、人设定位（Identity）

{five['identity']}

---

## 四、用户情感契约（Audience Contract）

用户关注这个博主，是为了：
{five['contract']}

---

## 五、选题体系（Topic System）

| 主题方向 | 篇数 |
|----------|------|
{topic_table}

**最强方向：** {five['best_topic']}（均赞 {five['best_topic_avg']:,}）

---

## 六、表达体系（Expression System）

| 维度 | 数据 |
|------|------|
| 含 * 情感符号 | {five['expression']['asterisk_ratio']} 篇 |
| 疑问句标题 | {five['expression']['question_titles']} 篇 |
| 情绪词命名 | {five['expression']['emotion_labels']} 篇 |

**核心公式：** {_get_core_formula(archetype['type'][0])}

---

## 七、高互动内容 Top 10

| # | 点赞 | 量级 | 标题 |
|---|------|------|------|
{top10_md}

---

## 八、点赞分布

| 段位 | 分布 |
|------|------|
{brackets_md}

---

## 九、商业化判断

- **适合方向：** {archetype['commercial']}
- **复制难度：** {archetype['difficulty']}

---

## 十、可学 / 不能硬抄

**可以学习：**
{can_learn}

**不能硬抄：**
{cant_copy}

---

## 十一、后续建议

- 路径 A：深入拆解 3-5 篇高互动笔记的正文结构
- 路径 B：制作专项爆款选题公式（`mode='formula'`）
- 路径 C：引入对标账号做多账号综合对比
"""


def _get_core_formula(typ: str) -> str:
    formulas = {
        "A": "荒诞场景 × 品牌符号 × 哲思轻量化 → 审美共鸣",
        "B": "私人经历 → 命题化 → 给模糊状态命名 → 普世共鸣",
        "C": "困境 → 说破规则 → 提供策略 → 爽感执行",
    }
    return formulas.get(typ, "内容积累 → 风格稳定 → 用户粘性")
