#!/usr/bin/env python3
import argparse
import json
import re
import urllib.parse
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Tuple

E_TAG_RE = re.compile(r'<e\s+[^>]*title="([^"]*)"[^>]*/?>')
ANY_TAG_RE = re.compile(r"<[^>]+>")
PARTIAL_TAG_TAIL_RE = re.compile(r"<[^\n]*$")
TIME_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})T(\d{2}:\d{2})")
DATE_ONLY_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})")
URL_LINE_RE = re.compile(r"^https?://\S+$")
HASHTAG_RE = re.compile(r"#[^#\n]+#")
LEADING_ENUM_RE = re.compile(r"^(?:旧闻\s*)?(?:\d+[\.、]\s*|\d+\s+)")
TRAILING_SOURCE_TAIL_RE = re.compile(r"(?:[_|｜][^_|｜\s]{1,12}){2,}$")
TRAILING_SOURCE_NAME_RE = re.compile(r"[-_｜|](新华网|凤凰网|新浪新闻|网易新闻|网易|腾讯新闻|财新网|观察者网|澎湃新闻)$")
TRAILING_ELLIPSIS_RE = re.compile(r"(\.\.\.|…|……)+$")
SOURCE_NOISE = {"百度安全验证", "华尔街见闻", "本球消息"}
QUESTION_HINTS = ("？", "?", "是否", "能否", "可行性", "怎么", "如何", "有没有", "意见", "建议", "问题", "请教")
PRIVATE_AUTHOR_ALLOWLISTS = {
    "睡前消息的编辑们": {"豆农", "马督工", "小白", "子不语", "聿人", "曾勃", "月亮池塘", "弗朗茨波拿巴"}
}


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_payload(path: Path) -> Tuple[List[dict], dict]:
    data = load_json(path)
    meta = {}
    if isinstance(data, dict):
        meta = {k: v for k, v in data.items() if k != "items"}
        data = data.get("items", [])
    if not isinstance(data, list):
        raise ValueError("Input JSON must be a list or an object with an 'items' array")
    return [item for item in data if isinstance(item, dict)], meta


def replace_e_tag(match: re.Match) -> str:
    title = match.group(1) or ""
    title = urllib.parse.unquote(title)
    return title.strip()


def clean_text(value: Any) -> str:
    if value is None:
        return ""
    text = str(value).replace("\r\n", "\n").replace("\r", "\n")
    text = E_TAG_RE.sub(replace_e_tag, text)
    text = ANY_TAG_RE.sub("", text)
    text = PARTIAL_TAG_TAIL_RE.sub("", text)
    text = urllib.parse.unquote(text)
    text = HASHTAG_RE.sub("", text)
    text = text.replace("&nbsp;", " ").replace("&amp;", "&")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def normalize_lines(text: str) -> List[str]:
    lines = []
    seen = set()
    for raw_line in clean_text(text).splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line in SOURCE_NOISE:
            continue
        if URL_LINE_RE.match(line):
            continue
        key = line.lower()
        if key in seen:
            continue
        seen.add(key)
        lines.append(line)
    return lines


def is_noise_author(text: str) -> bool:
    text = clean_text(text)
    if not text:
        return True
    if text in SOURCE_NOISE:
        return True
    if text.isdigit():
        return True
    if len(text) > 20:
        return True
    return False


def normalize_title_text(text: str) -> str:
    text = clean_text(text)
    text = TRAILING_ELLIPSIS_RE.sub("", text).strip()
    return text


def format_time(value: Any) -> str:
    text = clean_text(value)
    if not text:
        return ""
    match = TIME_RE.match(text)
    if match:
        return f"{match.group(1)} {match.group(2)}"
    return text[:16] if len(text) >= 16 else text


def extract_date(value: Any) -> str:
    text = clean_text(value)
    match = DATE_ONLY_RE.match(text)
    return match.group(1) if match else ""


def circle_date_span(items: List[dict]) -> str:
    dates = [extract_date(item.get("published_at")) for item in items]
    dates = [d for d in dates if d]
    if not dates:
        return ""
    return dates[0] if min(dates) == max(dates) else f"{min(dates)} ~ {max(dates)}"


def circle_authors(items: List[dict], private_mode: bool = False) -> str:
    authors = []
    seen = set()
    candidates = items
    circle_name = clean_text(items[0].get("circle_name")) if items else ""

    if private_mode:
        allowlist = PRIVATE_AUTHOR_ALLOWLISTS.get(circle_name)
        if allowlist:
            filtered = [item for item in items if clean_text(item.get("author")) in allowlist]
            if filtered:
                candidates = filtered
        else:
            filtered = [item for item in items if not item.get("is_question")]
            if filtered:
                candidates = filtered

    for item in candidates:
        author = clean_text(item.get("author"))
        if is_noise_author(author) or author in seen:
            continue
        seen.add(author)
        authors.append(author)
    return "、".join(authors)


def coerce_int(value: Any) -> int:
    if value in (None, "", False):
        return 0
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    digits = ""
    for ch in str(value):
        if ch.isdigit() or (ch == "-" and not digits):
            digits += ch
        elif digits:
            break
    try:
        return int(digits) if digits else 0
    except Exception:
        return 0


def sort_key(item: dict):
    return (
        item.get("summary_mode") != "full",
        -coerce_int(item.get("stream_score")),
        str(item.get("published_at") or ""),
        str(item.get("title_or_hook") or ""),
    )


def infer_display_title(item: dict) -> str:
    raw_title = normalize_title_text(item.get("title_or_hook") or item.get("title") or "")
    lines = normalize_lines(item.get("detail_excerpt") or item.get("content_preview") or "")
    first_line = normalize_title_text(lines[0]) if lines else ""

    if raw_title and raw_title not in SOURCE_NOISE and not raw_title.isdigit():
        if (raw_title.endswith("...") or raw_title.endswith("…") or len(raw_title) < 8) and first_line and len(first_line) >= len(raw_title):
            return first_line
        if first_line and raw_title in first_line and len(first_line) > len(raw_title):
            return first_line
        return raw_title

    if first_line:
        return first_line
    return raw_title or "（无标题）"


def compact_sentence(text: str, max_chars: int) -> str:
    text = re.sub(r"\s+", " ", clean_text(text)).strip()
    if not text:
        return "（无预览）"
    if len(text) <= max_chars:
        return text
    candidate = text[:max_chars].rstrip()
    split_at = max(candidate.rfind("。"), candidate.rfind("！"), candidate.rfind("？"), candidate.rfind("；"), candidate.rfind("，"))
    if split_at >= max_chars // 2:
        candidate = candidate[: split_at + 1].rstrip()
    return candidate + "…"


def candidate_content_lines(item: dict) -> List[str]:
    title = infer_display_title(item)
    base = item.get("detail_excerpt_raw") or item.get("detail_excerpt") or item.get("content_preview") or "（无预览）"
    lines = normalize_lines(base)
    kept = []
    for line in lines:
        line = clean_text(line)
        if not line:
            continue
        if line == title:
            continue
        if title and line.startswith(title) and len(line) <= len(title) + 3:
            continue
        if line.startswith("#"):
            continue
        if line in SOURCE_NOISE:
            continue
        kept.append(line)
    return kept or lines


def looks_like_news_list(item: dict) -> bool:
    if item.get("is_answer"):
        return False
    lines = candidate_content_lines(item)
    if len(lines) < 3:
        return False

    short_headlines = 0
    source_style = 0
    geopolitical_terms = 0
    for line in lines[:12]:
        line = clean_text(line)
        if not line:
            continue
        if len(line) <= 42:
            short_headlines += 1
        if "_" in line or "|" in line:
            source_style += 1
        if any(word in line for word in ("伊朗", "美国", "特朗普", "军舰", "雷达", "出口", "核电", "OpenAI", "ChatGPT", "凤凰网", "网易", "新华网")):
            geopolitical_terms += 1

    title = infer_display_title(item)
    title_is_headline = len(title) <= 42 and not title.endswith("？") and not title.endswith("吗")
    base_match = (
        source_style >= 2
        or short_headlines >= 4
        or (len(lines) >= 4 and short_headlines >= 3 and title_is_headline)
        or (len(lines) >= 4 and geopolitical_terms >= 3)
    )
    if not base_match:
        return False

    if item.get("is_question"):
        return source_style >= 2 or (geopolitical_terms >= 4 and short_headlines >= 3)
    return True


def infer_news_theme(line: str) -> str:
    text = clean_text(line)
    mapping = [
        ("平台内容治理", ["网盘", "影视剧", "盗版", "浏览器", "短剧", "分账"]),
        ("AI与科技", ["OpenAI", "ChatGPT", "AI", "医生", "算力", "模型"]),
        ("中东局势", ["伊朗", "霍尔木兹", "导弹", "军舰", "美军基地", "特朗普攻击伊朗"]),
        ("能源与产业", ["核电", "反应堆", "藏红花", "股市", "出口"]),
        ("外交人事", ["耿爽", "履新", "副会长", "联合国", "外交学会"]),
        ("国际冲突", ["袭击", "轰炸", "绑架", "战争", "动武"]),
        ("社会与劳动", ["就业", "劳动", "工人", "灵活就业", "平台用工"]),
    ]
    for theme, keywords in mapping:
        if any(keyword in text for keyword in keywords):
            return theme
    if "|" in text or "_" in text:
        return "外部新闻"
    return ""


def clean_news_line(line: str) -> str:
    line = normalize_title_text(line)
    line = LEADING_ENUM_RE.sub("", line).strip()
    line = TRAILING_SOURCE_NAME_RE.sub("", line).strip()
    line = TRAILING_SOURCE_TAIL_RE.sub("", line).strip("-_｜| ")
    return line


def summarize_private_news_list(item: dict, max_chars: int) -> str:
    lines = []
    seen = set()
    for raw in candidate_content_lines(item):
        line = clean_news_line(raw)
        if not line or line.startswith("#"):
            continue
        if line in SOURCE_NOISE:
            continue
        if URL_LINE_RE.match(line):
            continue
        key = line.lower()
        if key in seen:
            continue
        seen.add(key)
        lines.append(line)
    if not lines:
        return "一组新闻线索更新。"

    picks = []
    total_len = 0
    truncated = False
    for line in lines:
        if len(line) < 6:
            continue
        next_len = total_len + (1 if picks else 0) + len(line)
        if picks and next_len > max_chars:
            truncated = True
            break
        picks.append(line)
        total_len = next_len
        if len(picks) >= 5:
            truncated = len(lines) > len(picks)
            break

    if not picks:
        picks = lines[:2]
        truncated = len(lines) > len(picks)

    if truncated and picks:
        last = picks[-1].rstrip("。；，…")
        picks[-1] = last + "…"

    return "\n".join(picks)


def split_sentences(text: str) -> List[str]:
    return [part.strip() for part in re.split(r"(?<=[。！？；])\s*", text) if part.strip()]


def is_intro_sentence(sentence: str) -> bool:
    sentence = clean_text(sentence)
    intro_prefixes = (
        "豆农你好",
        "督工你好",
        "陈司你好",
        "我是睡前消息的老观众",
        "第一次提问",
        "突发奇想了一下",
        "最近赶上我朋友喜当爹",
    )
    return any(sentence.startswith(prefix) for prefix in intro_prefixes)


def topic_label_for_question(text: str) -> str:
    mapping = [
        ("生育与自动化社会分工", ["生育师", "自动化", "基础产业链", "生育率", "AI必然会替代"]),
        ("育儿与社会化抚养", ["育儿", "母乳", "奶粉", "抚养", "宝妈", "新生儿", "父亲", "月嫂", "育儿中心"]),
        ("劳动法实践与劳动维权", ["劳动法", "劳动仲裁", "维权", "违法解除", "补偿标准", "律师"]),
        ("金钱观与消费取舍", ["金钱观", "最值得的钱", "最后悔没花的钱", "收入尚有富余"]),
    ]
    for label, keywords in mapping:
        if any(word in text for word in keywords):
            return label
    return ""


def rewrite_question_core(text: str) -> str:
    text = clean_text(text)
    replacements = [
        ("豆农有什么意见", "对此有哪些建议"),
        ("也问问知识星球里的其他朋友，", ""),
        ("有多大的可行性呢", "可行性有多高"),
        ("碰到过哪些问题", "常见问题有哪些"),
        ("补偿标准的计算亦或是违法解除的举证", "补偿计算和违法解除举证该怎么处理"),
        ("这个时候了，", ""),
        ("现在的初步想法是", "是否适合"),
    ]
    for old, new in replacements:
        text = text.replace(old, new)
    text = re.sub(r"[（(][^）)]{0,30}[）)]", "", text)
    text = re.sub(r"想了解\s*想了解", "想了解", text)
    text = re.sub(r"\s+", " ", text).strip("，。； ")
    return text


def is_operational_notice(text: str) -> bool:
    text = clean_text(text)
    notice_markers = ("后台提问", "提问时间线", "筛选", "清理", "敬请谅解", "忽略掉", "忽略", "不会浪费")
    strong_question_hints = ("？", "?", "请教", "能否", "如何", "怎么", "有没有", "可行性")
    return any(marker in text for marker in notice_markers) and not any(hint in text for hint in strong_question_hints)


def summarize_operational_notice(item: dict, max_chars: int) -> str:
    text = re.sub(r"\s+", " ", " ".join(candidate_content_lines(item))).strip()
    pieces = []
    if any(marker in text for marker in ("不会浪费", "筛选", "清理")):
        pieces.append("说明后台提问会按价值逐步筛选清理")
    if any(marker in text for marker in ("忽略", "敬请谅解")):
        pieces.append("近期部分问题会暂时忽略")
    if not pieces:
        pieces.append("这是一条后台处理说明")
    summary = "，".join(pieces)
    if not summary.endswith("。"):
        summary += "。"
    return compact_sentence(summary, max_chars)


def summarize_question_item(item: dict, max_chars: int) -> str:
    lines = candidate_content_lines(item)
    text = re.sub(r"\s+", " ", " ".join(lines)).strip()
    sentences = [s for s in split_sentences(text) if not is_intro_sentence(s)]
    question_sentences = [s for s in sentences if any(hint in s for hint in QUESTION_HINTS)]
    label = topic_label_for_question(text)

    chosen = []
    source_sentences = question_sentences or sentences
    for sentence in source_sentences:
        sentence = rewrite_question_core(sentence)
        if not sentence:
            continue
        chosen.append(sentence)
        if len(chosen) >= 2:
            break

    if chosen and (label or len(chosen[0]) >= 42):
        core = chosen[0]
    else:
        core = " ".join(chosen).strip() if chosen else rewrite_question_core(text)

    if label:
        summary = f"围绕{label}提问，想了解{core}"
    else:
        summary = core
    summary = summary.replace("？？", "？").replace("。。", "。")
    return compact_sentence(summary, max_chars)


def summarize_text(item: dict, max_chars: int, private_news_list_mode: bool = False) -> str:
    if private_news_list_mode and looks_like_news_list(item):
        return summarize_private_news_list(item, max_chars)

    base_text = " ".join(candidate_content_lines(item))
    if is_operational_notice(base_text):
        return summarize_operational_notice(item, max_chars)

    if item.get("is_question") and item.get("summary_mode") != "full":
        return summarize_question_item(item, max_chars)

    text = base_text
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        text = infer_display_title(item)

    sentence_parts = split_sentences(text)
    if sentence_parts:
        summary = sentence_parts[0]
        idx = 1
        while len(summary) < min(60, max_chars // 2) and idx < len(sentence_parts):
            nxt = sentence_parts[idx]
            if len(summary) + 1 + len(nxt) > max_chars:
                break
            summary = f"{summary} {nxt}".strip()
            idx += 1
    else:
        summary = text

    return compact_sentence(summary, max_chars)


def append_summary(out: List[str], summary: str):
    if "\n" not in summary:
        out.append(f"- 摘要：{summary}")
        return
    out.append("- 摘要：")
    for line in summary.splitlines():
        line = clean_text(line)
        if not line:
            continue
        out.append(f"  - {line}")


def write_output(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Render a stream-style markdown digest from enriched ZSXQ JSON")
    parser.add_argument("input", help="Path to enriched stream JSON")
    parser.add_argument("--output", help="Optional output markdown path")
    parser.add_argument("--title", default="知识星球信息流摘要")
    parser.add_argument("--compact-max-items", type=int, default=8, help="Per-circle compact item limit")
    parser.add_argument("--compact-max-chars", type=int, default=220)
    parser.add_argument("--full-max-chars", type=int, default=320)
    parser.add_argument("--scope-label", default="", help="Accepted for pipeline compatibility; hidden by default")
    parser.add_argument("--private-news-list-mode", action="store_true", help="Optional private enhancement for news-list style updates")
    args = parser.parse_args()

    items, _meta = load_payload(Path(args.input))

    grouped: Dict[str, List[dict]] = defaultdict(list)
    for item in items:
        grouped[item.get("circle_name") or "未分类星球"].append(item)

    out: List[str] = []
    out.append(f"# {args.title}")

    for circle_name in sorted(grouped):
        circle_items = sorted(grouped[circle_name], key=sort_key)
        full_items = [item for item in circle_items if item.get("summary_mode") == "full"]
        compact_items = [item for item in circle_items if item.get("summary_mode") != "full"]
        if args.compact_max_items and args.compact_max_items > 0:
            compact_items = compact_items[: args.compact_max_items]

        out.append(f"## {circle_name}")
        date_span = circle_date_span(circle_items)
        authors = circle_authors(circle_items, private_mode=args.private_news_list_mode)
        if date_span:
            out.append(f"- 摘要时间跨度：{date_span}")
        if authors:
            out.append(f"- 作者：{authors}")
        out.append("")

        if full_items:
            out.append("### 重点展开")
            for idx, item in enumerate(full_items, start=1):
                title = infer_display_title(item)
                out.append(f"#### {idx}. {title}")
                summary = summarize_text(item, max_chars=args.full_max_chars, private_news_list_mode=args.private_news_list_mode)
                append_summary(out, summary)
                url = clean_text(item.get("url"))
                if url:
                    out.append(f"- 原文：{url}")
                out.append("")

        if compact_items:
            out.append("### 其余更新")
            for item in compact_items:
                summary = summarize_text(item, max_chars=args.compact_max_chars, private_news_list_mode=args.private_news_list_mode)
                append_summary(out, summary)
                url = clean_text(item.get("url"))
                if url:
                    out.append(f"  - 原文：{url}")
            out.append("")

    text = "\n".join(out).rstrip() + "\n"
    if args.output:
        write_output(Path(args.output), text)
    print(text)


if __name__ == "__main__":
    main()
