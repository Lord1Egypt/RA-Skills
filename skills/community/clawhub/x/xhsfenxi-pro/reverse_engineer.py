"""
reverse_engineer.py — 数据驱动逆向工程引擎（v2.1 新增）

把B+A 反讽系 v3.5 实战中手写的 Step 4 数据驱动逆向工程代码固化为可复用模块。

核心输出（与 PROMPT 模板 v1.1 第六节"数据驱动模块必查清单"对齐）：
1. 主题表现矩阵（按均赞排）
2. Top10 vs Bottom10 标题特征对比
3. 反常识发现（视频/图文倍数 / "我"字 / 引号 / ptN 系列 / 隐藏金矿）
4. 标题数据画像（字数 / emoji / 数字 / 群体主语 / 流行符号）
5. 温度判断（治愈系 vs 反讽系 vs 锋利系）

用法:
    from xhscosmoskill.reverse_engineer import full_reverse_engineering
    result = full_reverse_engineering(notes)
    print(result["findings"])
"""
from __future__ import annotations
from typing import List, Any, Dict
import re
from collections import defaultdict


# ── 工具 ────────────────────────────────────────────────────────

def _parse_likes(v) -> int:
    if not v:
        return 0
    s = str(v).replace(",", "").strip()
    if "万" in s:
        return int(float(s.replace("万", "").replace("+", "")) * 10000)
    if "亿" in s:
        return int(float(s.replace("亿", "")) * 100000000)
    try:
        return int(s)
    except ValueError:
        return 0


def _get(note, attr, default=""):
    if hasattr(note, attr):
        return getattr(note, attr) or default
    return note.get(attr, default) if hasattr(note, "get") else default


# ── 主题分类（更精细，支持自定义）──────────────────────────────

DEFAULT_THEME_KEYWORDS = {
    "城市/异乡": ["纽约", "巴黎", "伦敦", "东京", "上海", "北京", "海外", "异乡", "留学", "城市", "街头"],
    "美食/感官": ["饿", "吃", "汉堡", "美食", "豆汁", "餐", "饭", "口", "味", "食堂"],
    "身份/群体": ["留子", "打工人", "学生", "同学", "朋友们", "新人", "i人", "infj", "普通人"],
    "解构金句": ["塌房", "审判", "破碎", "装", "放屁", "驾照", "学历", "特点", "抽象", "具象"],
    "情绪/感悟": ["失败", "成功", "走了", "幻想", "突然", "远离", "宅家", "接纳", "理解"],
    "文化/审美": ["音乐剧", "电影", "动漫", "维密", "时尚", "走秀", "Ken", "MJ", "zima", "主持", "百老汇"],
    "自然/户外": ["山", "海", "森林", "户外", "徒步", "草原", "雪", "高原"],
    "创作/记录": ["记录", "vlog", "日记", "写作", "创造"],
    "成长/人生": ["年终", "汇报", "二十", "成长", "毕业", "gap", "回望"],
    "系列编号": ["pt1", "pt2", "pt3", "pt4", "pt5", "第一期", "第二期", "vol1", "vol2"],
}


def categorize_theme(title: str, keyword_map: Dict[str, List[str]] = None) -> str:
    """根据标题判断主题类别。优先级按 keyword_map 顺序。"""
    keyword_map = keyword_map or DEFAULT_THEME_KEYWORDS
    t = title or ""
    for theme, kws in keyword_map.items():
        if any(kw.lower() in t.lower() for kw in kws):
            return theme
    return "其他"


def theme_matrix(notes: List[Any], keyword_map: Dict = None) -> List[Dict]:
    """生成主题表现矩阵，按均赞排序。"""
    theme_data = defaultdict(list)
    for n in notes:
        title = _get(n, "title")
        likes = _parse_likes(_get(n, "likes"))
        cat = categorize_theme(title, keyword_map)
        theme_data[cat].append({"title": title, "likes": likes})

    result = []
    for theme, items in theme_data.items():
        likes_list = [x["likes"] for x in items]
        avg = sum(likes_list) / len(likes_list) if likes_list else 0
        rep = max(items, key=lambda x: x["likes"])
        result.append({
            "theme": theme,
            "count": len(items),
            "avg": int(avg),
            "max": max(likes_list),
            "min": min(likes_list),
            "representative": rep["title"][:40],
        })
    return sorted(result, key=lambda x: -x["avg"])


# ── Top10 vs Bottom10 对比 ──────────────────────────────────────

def title_features(notes_list: List[Any]) -> Dict[str, Any]:
    """提取一组笔记的标题特征。"""
    feats = {
        "uses_我": 0, "uses_quotes": 0, "uses_数字": 0,
        "uses_emoji_or_decoration": 0,
        "len_avg": 0,
        "is_video": 0,
        "starts_with_action": 0,
        "starts_with_place": 0,
        "uses_question": 0,
        "uses_pt系列": 0,
        "starts_with_group": 0,  # 群体主语开头
        "uses_pop_symbol": 0,    # 流行符号
    }
    lens = []
    pop_symbols = ["Ken", "老友记", "钱德勒", "zima", "MJ", "哈利", "蝙蝠侠", "哥谭", "甄嬛"]
    group_subjects = ["留子", "打工人", "i人", "infj", "学生", "同学", "朋友们", "新人", "普通人", "我们"]

    for n in notes_list:
        t = _get(n, "title")
        if "我" in t:
            feats["uses_我"] += 1
        if any(c in t for c in ['"', '"', '"']):
            feats["uses_quotes"] += 1
        if re.search(r'\d', t):
            feats["uses_数字"] += 1
        if any(c in t for c in ['！', '？', '!', '?', '✨', '🌅', '🥹']):
            feats["uses_emoji_or_decoration"] += 1
        if t.startswith(('来', '走', '去', '看')):
            feats["starts_with_action"] += 1
        if t.startswith(('纽约', '巴黎', '芝加哥', '北海道', '帕米尔', '上海', '北京')):
            feats["starts_with_place"] += 1
        if t.endswith(('?', '？')) or '吗' in t:
            feats["uses_question"] += 1
        if 'pt' in t.lower() or '第一期' in t or '第二期' in t:
            feats["uses_pt系列"] += 1
        if any(t.startswith(g) for g in group_subjects):
            feats["starts_with_group"] += 1
        if any(s in t for s in pop_symbols):
            feats["uses_pop_symbol"] += 1
        if (_get(n, "type") or "") == 'video':
            feats["is_video"] += 1
        lens.append(len(t))
    feats['len_avg'] = round(sum(lens) / len(lens), 1) if lens else 0
    return feats


def top_vs_bottom(notes: List[Any], n: int = 10) -> Dict[str, Any]:
    """Top n vs Bottom n 标题特征对比。"""
    sorted_notes = sorted(notes, key=lambda x: -_parse_likes(_get(x, "likes")))
    top = sorted_notes[:n]
    bot = sorted_notes[-n:]

    top_feats = title_features(top)
    bot_feats = title_features(bot)

    diff = {k: top_feats[k] - bot_feats[k] for k in top_feats if isinstance(top_feats[k], (int, float))}

    return {
        "top": top_feats,
        "bottom": bot_feats,
        "diff": diff,
        "top_titles": [(_get(t, "title")[:50], _parse_likes(_get(t, "likes"))) for t in top],
        "bottom_titles": [(_get(t, "title")[:50], _parse_likes(_get(t, "likes"))) for t in bot],
    }


# ── 反常识发现（findings）──────────────────────────────────────

def detect_findings(notes: List[Any], top_bot: Dict, theme_data: List[Dict]) -> List[Dict]:
    """生成反常识发现列表。每项含 type / message / severity / data。"""
    findings = []

    # 1. 视频/图文倍数
    video_notes = [n for n in notes if (_get(n, "type") or "") == "video"]
    normal_notes = [n for n in notes if (_get(n, "type") or "") == "normal"]
    if video_notes and normal_notes:
        v_avg = sum(_parse_likes(_get(n, "likes")) for n in video_notes) / len(video_notes)
        n_avg = sum(_parse_likes(_get(n, "likes")) for n in normal_notes) / len(normal_notes)
        if n_avg > 0:
            ratio = v_avg / n_avg
            if ratio > 1.5:
                findings.append({
                    "type": "media_engine",
                    "severity": "high",
                    "message": f"视频是 {ratio:.2f}x 引擎（视频均赞 {int(v_avg):,} vs 图文 {int(n_avg):,}）",
                    "action": "降低图文比例，重要选题首选视频",
                })
            elif ratio < 0.7:
                findings.append({
                    "type": "media_engine",
                    "severity": "high",
                    "message": f"图文反向胜出（图文均赞 {int(n_avg):,} vs 视频 {int(v_avg):,}）",
                    "action": "图文叙事感是该博主优势，不必强行视频化",
                })

    # 2. "我"字检查
    top_我 = top_bot["top"]["uses_我"]
    bot_我 = top_bot["bottom"]["uses_我"]
    if top_我 == 0 and bot_我 >= 1:
        findings.append({
            "type": "去我化",
            "severity": "critical",
            "message": f"Top10 中 0 篇用「我」字，Bottom10 中 {bot_我} 篇用「我」",
            "action": "标题去『我』化是该博主铁证。改群体主语扩大传播半径",
        })
    elif top_我 < bot_我:
        findings.append({
            "type": "去我化",
            "severity": "medium",
            "message": f"Top10「我」字 {top_我} 篇 vs Bottom10 {bot_我} 篇",
            "action": "倾向去『我』化，但非铁证",
        })

    # 3. ptN 系列化检查
    pt_notes = [n for n in notes if "pt" in _get(n, "title").lower()]
    if pt_notes:
        pt_avg = sum(_parse_likes(_get(n, "likes")) for n in pt_notes) / len(pt_notes)
        all_avg = sum(_parse_likes(_get(n, "likes")) for n in notes) / len(notes)
        if pt_avg < all_avg * 0.7:
            findings.append({
                "type": "系列化失败",
                "severity": "high",
                "message": f"ptN 系列 {len(pt_notes)} 篇均赞 {int(pt_avg):,}（远低全样本 {int(all_avg):,}）",
                "action": "用户为单点惊喜买单，不为系列化打卡买单。停止 ptN 模式",
            })

    # 4. 隐藏金矿主题（篇数<5 但均赞高）
    sorted_themes = sorted(theme_data, key=lambda x: -x["avg"])
    for t in sorted_themes[:3]:
        all_avg = sum(_parse_likes(_get(n, "likes")) for n in notes) / max(len(notes), 1)
        if t["count"] < 5 and t["avg"] > all_avg * 1.3:
            findings.append({
                "type": "隐藏金矿",
                "severity": "high",
                "message": f"主题「{t['theme']}」仅 {t['count']} 篇但均赞 {t['avg']:,}（vs 全样本 {int(all_avg):,}）",
                "action": f"严重供不应求 — 加码该方向是最快增长杠杆",
            })

    # 5. 群体主语正向相关
    top_group = top_bot["top"]["starts_with_group"]
    bot_group = top_bot["bottom"]["starts_with_group"]
    if top_group >= 3 and top_group > bot_group:
        findings.append({
            "type": "群体主语优势",
            "severity": "medium",
            "message": f"Top10 群体主语开头 {top_group} 篇 vs Bottom10 {bot_group} 篇",
            "action": "群体主语（留子/打工人/同学们）是有效公式",
        })

    # 6. 标题字数分布
    top_len = top_bot["top"]["len_avg"]
    bot_len = top_bot["bottom"]["len_avg"]
    if abs(top_len - bot_len) > 5:
        findings.append({
            "type": "标题长度偏好",
            "severity": "low",
            "message": f"Top10 平均字数 {top_len} vs Bottom10 {bot_len}",
            "action": "短/长 标题风格" + ("偏短" if top_len < bot_len else "偏长") + "更受欢迎",
        })

    # 7. 流行符号挪用
    pop_count = sum(top_bot["top"]["uses_pop_symbol"] + top_bot["bottom"]["uses_pop_symbol"] for _ in [None])
    if top_bot["top"]["uses_pop_symbol"] >= 2:
        findings.append({
            "type": "A 型流行符号挪用",
            "severity": "medium",
            "message": f"Top10 中 {top_bot['top']['uses_pop_symbol']} 篇挪用流行符号（Ken/老友记类）",
            "action": "流行符号挪用是 A 型放大器，可继续投资该型选题",
        })

    return findings


# ── 温度判断（治愈系 vs 反讽系 vs 锋利系）──────────────────────

TEMPERATURE_SIGNALS = {
    "治愈": {
        "title_kw": ["接纳", "理解", "陪伴", "温柔", "可爱", "想念", "思念", "如灯塔", "温暖", "暖到了"],
        "punctuation": ["*", "～", "✨"],
    },
    "反讽": {
        "title_kw": ["塌房", "审判", "破碎", "装", "放屁", "驾照", "学历", "代餐", "开机慢", "不耐受", "其实是装的"],
        "punctuation": [":", "："],
    },
    "锋利": {
        "title_kw": ["骗子", "不要脸", "现实", "规则", "策略", "拿回", "向上", "潜规则", "穷"],
        "punctuation": ["！", "?", "？"],
    },
}


def detect_temperature(notes: List[Any]) -> Dict[str, Any]:
    """检测博主底色温度（治愈/反讽/锋利）。"""
    scores = {"治愈": 0, "反讽": 0, "锋利": 0}
    evidence = {"治愈": [], "反讽": [], "锋利": []}

    for n in notes:
        t = _get(n, "title")
        for temp, sig in TEMPERATURE_SIGNALS.items():
            for kw in sig["title_kw"]:
                if kw in t:
                    scores[temp] += 2
                    if len(evidence[temp]) < 3:
                        evidence[temp].append(t[:40])
            for p in sig["punctuation"]:
                if p in t:
                    scores[temp] += 0.3

    total = sum(scores.values()) or 1
    pct = {k: round(v / total * 100) for k, v in scores.items()}
    primary = max(scores, key=scores.get)

    return {
        "primary": primary,
        "scores": {k: round(v, 1) for k, v in scores.items()},
        "pct": pct,
        "evidence": evidence,
        "is_hybrid": scores[sorted(scores, key=scores.get, reverse=True)[1]] >= scores[primary] * 0.6,
    }


# ── 内容结构推断（3 种）─────────────────────────────────────────

def infer_content_structures(notes: List[Any], top_bot: Dict) -> List[str]:
    """根据 Top10 标题特征推断该博主主导的内容结构（A/B/C）。"""
    top_titles = [_get(n, "title") for n in
                  sorted(notes, key=lambda x: -_parse_likes(_get(x, "likes")))[:10]]

    structures = []
    # 结构 A：反预期开场型
    if any(any(kw in t for kw in ["没想过", "没想到", "原来", "才发现"]) for t in top_titles):
        structures.append({
            "type": "A 反预期开场型",
            "适用": "B 型 / 命题驱动",
            "节奏": "标题反预期 → 视频铺陈 → 揭示共同处境 → 短判断收束",
        })
    # 结构 B：类比观点型
    if any(any(kw in t for kw in ["像", "其实是", "不是", "更像"]) for t in top_titles):
        structures.append({
            "type": "B 类比观点型",
            "适用": "A 像 B 类比博主",
            "节奏": "抛 A=B 类比 → 举例证明 → 保留最锋利判断",
        })
    # 结构 C：城市奇观型
    if any(any(kw in t for kw in ["凌晨", "看见", "遇到", "撞见", "奇观", "神奇"]) for t in top_titles):
        structures.append({
            "type": "C 城市奇观型",
            "适用": "A 型 / 荒诞白描博主",
            "节奏": "抛具体时空 → 展示荒诞画面 → 冷静旁白合法化",
        })

    if not structures:
        structures.append({
            "type": "通用型",
            "适用": "未识别明显结构",
            "节奏": "建议人工拆视频后补充",
        })
    return structures


# ── 主入口 ──────────────────────────────────────────────────────

def full_reverse_engineering(notes: List[Any], theme_keywords: Dict = None) -> Dict[str, Any]:
    """
    一站式数据驱动逆向工程。
    返回完整的分析数据，可直接喂给报告生成器。
    """
    tm = theme_matrix(notes, theme_keywords)
    tb = top_vs_bottom(notes)
    findings = detect_findings(notes, tb, tm)
    temp = detect_temperature(notes)
    structures = infer_content_structures(notes, tb)

    return {
        "theme_matrix": tm,
        "top_vs_bottom": tb,
        "findings": findings,
        "temperature": temp,
        "content_structures": structures,
        "_meta": {
            "version": "v2.1",
            "engine": "xhsfenxi-pro reverse_engineer",
        },
    }


def format_findings_md(findings: List[Dict]) -> str:
    """把 findings 列表格式化成 markdown 段落。"""
    if not findings:
        return "_暂无显著反常识发现_"
    lines = []
    severity_emoji = {"critical": "🚨", "high": "🔥", "medium": "💡", "low": "📌"}
    for f in findings:
        emoji = severity_emoji.get(f["severity"], "•")
        lines.append(f"- {emoji} **{f['type']}**: {f['message']}")
        lines.append(f"  → 建议：{f['action']}")
    return "\n".join(lines)


# ── CLI 入口（调试用）───────────────────────────────────────────

if __name__ == "__main__":
    import sys, json
    if len(sys.argv) < 2:
        print("用法: python3 reverse_engineer.py <notes.json>")
        sys.exit(1)

    with open(sys.argv[1]) as f:
        notes = json.load(f)

    result = full_reverse_engineering(notes)
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
