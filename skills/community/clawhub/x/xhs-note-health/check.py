#!/usr/bin/env python3
"""
xhs-note-health v1.1.0 — 小红书笔记限流状态检测
通过创作者后台 API 获取所有笔记的 level 字段，判断限流等级。

用法:
    python3 check.py [--cookies PATH] [--throttled-only] [--json] [--output PATH]

更新日志 (v1.1.0):
- 增加限流笔记编辑链接
- 报告增加互动数据 (点赞/评论/收藏/分享)
- 限流原因说明优化（去掉冗余 "level低于1"）
- 新增 --sort 参数 (level/likes/comments)
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

try:
    import requests
except ImportError:
    print("ERROR: 需要 requests 库。运行: pip3 install requests", file=sys.stderr)
    sys.exit(1)

# ── 常量 ──────────────────────────────────────────────────────────

DEFAULT_COOKIES = os.path.expanduser("~/tools/xiaohongshu-mcp/xiaohongshu_cookies.json")

API_URL = "https://creator.xiaohongshu.com/api/galaxy/v2/creator/note/user/posted"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://creator.xiaohongshu.com/new/note-manager",
    "Accept": "application/json, text/plain, */*",
    "Origin": "https://creator.xiaohongshu.com",
}

LEVEL_META = {
    4:    ("🟢 正常推荐", "笔记正常分发"),
    2:    ("🟡 基本正常", "轻微受限"),
    1:    ("⚪ 新帖初始", "刚发布，等待审核"),
    -1:   ("🔴 轻度限流", "推荐量明显下降"),
    -5:   ("🔴🔴 中度限流", "几乎无推荐"),
    -102: ("⛔ 严重限流", "不可逆，需删除重发"),
}

SENSITIVE_WORDS = [
    # AI / 自动化
    "AI生成", "AI自动", "AI创作", "自动化", "自动发布", "自动工作流",
    "全自动", "批量", "内容工厂", "矩阵号",
    # 极限词 / 绝对化
    "最好", "最佳", "最强", "最便宜", "最低价", "全网最低",
    "第一", "NO.1", "TOP1", "唯一", "顶级", "极致", "巅峰",
    "独一无二", "全国第一", "世界级", "国家级",
    # 虚假承诺
    "包过", "稳赚不赔", "零风险", "永久", "万能", "100%",
    # 医疗功效夸大
    "根治", "特效", "一次见效", "立竿见影", "秒变",
    "一洗白", "一抹就瘦", "防脱发", "改善睡眠",
    # 站外引流
    "微信", "加V", "+V", "VX", "wx",
    # 诱导互动
    "互粉", "互关", "求关注", "求点赞", "求收藏", "一键三连",
    # 营销限时
    "秒杀", "抢疯了", "再不抢就没了", "随时涨价",
    # 迷信
    "招财进宝", "旺夫",
]

# ── 工具函数 ──────────────────────────────────────────────────────

def get_level_label(level: int) -> tuple:
    """返回 (标签, 说明)"""
    if level in LEVEL_META:
        return LEVEL_META[level]
    if level >= 4:
        return ("🟢 正常推荐", "笔记正常分发")
    if level >= 2:
        return (f"🟡 L{level}", "基本正常")
    if level <= -102:
        return ("⛔ 严重限流", "不可逆，需删除重发")
    if level <= -5:
        return (f"🔴🔴 L{level}", "中度限流")
    if level < 0:
        return (f"🔴 L{level}", "限流")
    return (f"L{level}", "未知状态")


def detect_sensitive(title: str) -> list:
    """检测标题中的敏感词"""
    return [w for w in SENSITIVE_WORDS if w in (title or "")]


def load_cookies(path: str) -> str:
    """从 JSON 文件加载 cookies，返回 Cookie header 字符串"""
    with open(path, "r") as f:
        raw = json.load(f)

    if isinstance(raw, list):
        # [{name, value}, ...] 格式
        return "; ".join(
            f"{c['name']}={c['value']}"
            for c in raw
            if c.get("name") and c.get("value")
        )
    elif isinstance(raw, dict):
        # {name: value, ...} 格式
        return "; ".join(f"{k}={v}" for k, v in raw.items() if v)
    else:
        raise ValueError(f"不支持的 cookies 格式: {type(raw)}")


def count_tags(note: dict) -> int:
    """统计笔记标签数量"""
    for key in ("tag_list", "tags", "topic_list", "topics", "hash_tag_list", "hashtag_list"):
        val = note.get(key)
        if isinstance(val, list):
            return len(val)
    for key in ("tag_count", "topic_count", "hashtag_count"):
        val = note.get(key)
        if isinstance(val, int):
            return val
    return 0


# ── 核心逻辑 ──────────────────────────────────────────────────────

def fetch_all_notes(cookie_str: str) -> list:
    """分页获取所有笔记"""
    all_notes = []
    page = 1
    page_size = 30

    while True:
        headers = {**HEADERS, "Cookie": cookie_str}
        params = {"page": page, "page_size": page_size}

        try:
            resp = requests.get(API_URL, headers=headers, params=params, timeout=20)
        except requests.RequestException as e:
            print(f"ERROR: 请求失败: {e}", file=sys.stderr)
            break

        if resp.status_code == 401:
            print("ERROR: Cookies 已过期 (401)，请重新从浏览器导出 cookies。", file=sys.stderr)
            sys.exit(2)

        try:
            data = resp.json()
        except json.JSONDecodeError:
            print(f"ERROR: 响应不是 JSON: {resp.text[:200]}", file=sys.stderr)
            break

        if not data.get("success"):
            code = data.get("code", "?")
            msg = data.get("msg", "未知错误")
            if code == 903:
                print(f"ERROR: {msg} (code={code})，请重新导出 cookies。", file=sys.stderr)
                sys.exit(2)
            print(f"ERROR: API 返回失败: {msg} (code={code})", file=sys.stderr)
            break

        notes = []
        if data.get("data"):
            for key in ("notes", "note_list", "items", "list"):
                val = data["data"].get(key)
                if isinstance(val, list):
                    notes = val
                    break

        if not notes:
            break

        for note in notes:
            note_id = str(note.get("note_id") or note.get("noteId") or note.get("id") or "")
            title = str(note.get("display_title") or note.get("title") or note.get("note_title") or "").strip()
            level_raw = note.get("level_", note.get("level", note.get("distribution_level")))
            try:
                level = int(level_raw) if level_raw is not None else 1
            except (ValueError, TypeError):
                level = 1

            tag_count = count_tags(note)
            sensitive_hits = detect_sensitive(title)
            label, desc = get_level_label(level)

            all_notes.append({
                "note_id": note_id,
                "title": title,
                "level": level,
                "level_label": label,
                "level_desc": desc,
                "tag_count": tag_count,
                "tag_warning": tag_count > 5,
                "sensitive_hits": sensitive_hits,
                "cover": note.get("cover", {}).get("url", ""),
                "likes": note.get("liked_count", 0),
                "comments": note.get("comment_count", 0),
                "collects": note.get("collected_count", 0),
                "shares": note.get("shared_count", 0),
                "type": note.get("type", ""),
            })

        # 检查是否还有下一页
        has_more = data.get("data", {}).get("has_more", False)
        total = data.get("data", {}).get("total", 0)
        if not has_more and len(all_notes) >= total and total > 0:
            break
        if len(notes) < page_size:
            break

        page += 1
        time.sleep(0.5)  # 避免请求过快

    return all_notes


def generate_report(notes: list) -> str:
    """生成 Markdown 报告"""
    if not notes:
        return "## 小红书笔记健康报告\n\n⚠️ 未获取到任何笔记。\n"

    # 统计
    level_counts = {}
    throttled = []
    sensitive_notes = []
    tag_warning_notes = []

    for n in notes:
        lv = n["level"]
        level_counts[lv] = level_counts.get(lv, 0) + 1
        if lv < 0:
            throttled.append(n)
        if n["sensitive_hits"]:
            sensitive_notes.append(n)
        if n["tag_warning"]:
            tag_warning_notes.append(n)

    lines = []
    lines.append("## 📊 小红书笔记健康报告\n")
    lines.append(f"**总笔记数**: {len(notes)}")
    lines.append(f"**检测时间**: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Level 分布
    lines.append("### Level 分布\n")
    for lv in sorted(level_counts.keys(), reverse=True):
        label, _ = get_level_label(lv)
        lines.append(f"- **L{lv}** {label}: {level_counts[lv]} 篇")

    # 限流笔记
    if throttled:
        lines.append(f"\n### ⚠️ 限流笔记 ({len(throttled)} 篇)\n")
        for n in sorted(throttled, key=lambda x: x["level"]):
            lines.append(f"- **{n['level_label']}** | {n['title'][:50]}")
            edit_url = f"https://creator.xiaohongshu.com/publish/publish?noteId={n['note_id']}"
            lines.append(f"  - {n['level_desc']} | [✏️ 编辑]({edit_url})")
            lines.append(f"  - 👍 {n['likes']} 💬 {n['comments']} ⭐ {n['collects']} 🔄 {n['shares']}")
            reasons = []
            if n["sensitive_hits"]:
                reasons.append(f"敏感词: {', '.join(n['sensitive_hits'])}")
            if n["tag_warning"]:
                reasons.append(f"标签过多: {n['tag_count']} 个")
            if reasons:
                lines.append(f"  - ⚠️ {' | '.join(reasons)}")
    else:
        lines.append("\n### ✅ 无限流笔记\n")

    # 敏感词命中
    if sensitive_notes:
        lines.append(f"\n### ⚠️ 敏感词命中 ({len(sensitive_notes)} 篇)\n")
        for n in sensitive_notes:
            lines.append(f"- **{n['title'][:50]}** → {', '.join(n['sensitive_hits'])}")

    # 标签过多
    if tag_warning_notes:
        lines.append(f"\n### 📛 标签过多 ({len(tag_warning_notes)} 篇)\n")
        for n in tag_warning_notes:
            lines.append(f"- **{n['title'][:50]}** — {n['tag_count']} 个标签")

    # 正常笔记概览
    normal = [n for n in notes if n["level"] >= 0]
    if normal:
        lines.append(f"\n### 📋 正常笔记 ({len(normal)} 篇)\n")
        for n in sorted(normal, key=lambda x: -x["level"]):
            lines.append(f"- {n['level_label']} | {n['title'][:50]} | 👍{n['likes']} 💬{n['comments']} ⭐{n['collects']}")

    return "\n".join(lines)


# ── CLI 入口 ──────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="小红书笔记限流状态检测")
    parser.add_argument("--cookies", default=DEFAULT_COOKIES,
                        help=f"Cookies JSON 文件路径 (默认: {DEFAULT_COOKIES})")
    parser.add_argument("--throttled-only", action="store_true",
                        help="只显示限流笔记")
    parser.add_argument("--json", action="store_true",
                        help="JSON 格式输出")
    parser.add_argument("--output", "-o", type=str, default=None,
                        help="保存报告到文件")
    parser.add_argument("--sort", choices=["level", "likes", "comments", "collects"],
                        default="level", help="排序方式 (默认: level)")

    args = parser.parse_args()

    # 加载 cookies
    cookies_path = os.path.expanduser(args.cookies)
    if not os.path.exists(cookies_path):
        print(f"ERROR: Cookies 文件不存在: {cookies_path}", file=sys.stderr)
        print("请从浏览器导出小红书创作者后台的 cookies 到该路径。", file=sys.stderr)
        sys.exit(1)

    cookie_str = load_cookies(cookies_path)

    # 获取笔记
    print("正在获取笔记列表...", file=sys.stderr)
    notes = fetch_all_notes(cookie_str)
    print(f"获取到 {len(notes)} 篇笔记。", file=sys.stderr)

    if args.throttled_only:
        notes = [n for n in notes if n["level"] < 0]

    # 排序
    sort_keys = {
        "level": lambda x: x["level"],
        "likes": lambda x: -x["likes"],
        "comments": lambda x: -x["comments"],
        "collects": lambda x: -x["collects"],
    }
    if args.sort in sort_keys:
        notes.sort(key=sort_keys[args.sort])

    # 输出
    if args.json:
        result = {
            "total": len(notes),
            "checked_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "notes": notes,
            "summary": {},
        }
        level_counts = {}
        for n in notes:
            lv = n["level"]
            level_counts[lv] = level_counts.get(lv, 0) + 1
        result["summary"] = {
            "level_distribution": level_counts,
            "throttled_count": sum(1 for n in notes if n["level"] < 0),
            "sensitive_count": sum(1 for n in notes if n["sensitive_hits"]),
            "tag_warning_count": sum(1 for n in notes if n["tag_warning"]),
        }
        output = json.dumps(result, ensure_ascii=False, indent=2)
    else:
        output = generate_report(notes)

    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        print(f"报告已保存到: {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
