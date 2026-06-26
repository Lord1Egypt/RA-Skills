from __future__ import annotations

import json
import re
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml
from skill_runtime.writing_core import OPENING_TYPES, STRUCTURE_TYPES, build_angle_pack


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def slugify(text: str) -> str:
    cleaned = re.sub(r"[^\w\u4e00-\u9fff-]+", "-", text.strip().lower())
    cleaned = re.sub(r"-{2,}", "-", cleaned).strip("-")
    return cleaned or datetime.now().strftime("%Y%m%d-%H%M%S")


def clean_text(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def truncate_text(value: Any, limit: int) -> str:
    cleaned = clean_text(value)
    if len(cleaned) <= limit:
        return cleaned
    return cleaned[: max(limit - 1, 0)].rstrip() + "…"


def parse_frontmatter(path: Path) -> tuple[dict[str, Any], str]:
    text = read_text(path)
    if not text.startswith("---"):
        return {}, text.strip()

    match = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", text, flags=re.DOTALL)
    if not match:
        return {}, text.strip()

    frontmatter = yaml.safe_load(match.group(1)) or {}
    if not isinstance(frontmatter, dict):
        raise ValueError(f"Frontmatter must be a mapping: {path}")
    return frontmatter, match.group(2).strip()


def normalize_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [clean_text(item) for item in value if clean_text(item)]
    return [part.strip() for part in str(value).split(",") if part.strip()]


def parse_json_output(stdout: str) -> Any:
    stripped = stdout.strip()
    if not stripped:
        return {}

    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        for start_char, end_char in (("{", "}"), ("[", "]")):
            start = stripped.find(start_char)
            end = stripped.rfind(end_char)
            if start != -1 and end != -1 and end > start:
                return json.loads(stripped[start : end + 1])
    raise ValueError("Tavily CLI did not return valid JSON.")


def resolve_source_file(path_value: str, workspace_root: Path) -> Path:
    candidate = Path(path_value)
    return candidate if candidate.is_absolute() else workspace_root / candidate


def resolve_request(path: Path, *, workspace_root: Path) -> dict[str, Any]:
    frontmatter, notes = parse_frontmatter(path)

    topic = clean_text(frontmatter.get("topic"))
    question = clean_text(frontmatter.get("question"))
    if not topic:
        raise ValueError("`topic` is required for topic-research.")
    if not question:
        raise ValueError("`question` is required for topic-research.")

    model = clean_text(frontmatter.get("model") or "pro").lower()
    if model not in {"mini", "pro", "auto"}:
        raise ValueError("`model` must be one of: mini, pro, auto.")

    source_file = clean_text(frontmatter.get("source_file"))
    resolved_source: Path | None = None
    source_excerpt = ""
    if source_file:
        resolved_source = resolve_source_file(source_file, workspace_root)
        if not resolved_source.exists():
            raise FileNotFoundError(f"source_file not found: {resolved_source}")
        source_excerpt = truncate_text(read_text(resolved_source), 1200)

    seed_urls = normalize_list(frontmatter.get("seed_urls"))
    slug = slugify(topic)
    today = datetime.now()

    return {
        "topic": topic,
        "question": question,
        "model": model,
        "source_file": resolved_source,
        "source_excerpt": source_excerpt,
        "seed_urls": seed_urls,
        "notes": notes,
        "slug": slug,
        "date": today.strftime("%Y%m%d"),
        "raw_date": today.strftime("%Y-%m-%d"),
    }


def require_tvly() -> str:
    tvly_path = shutil.which("tvly")
    if not tvly_path:
        raise RuntimeError("未找到 `tvly` CLI。请先安装并登录 Tavily，然后再运行 `topic-research`。")
    return tvly_path


def build_query(request: dict[str, Any]) -> str:
    parts = [
        f"研究主题：{request['topic']}",
        f"研究问题：{request['question']}",
        "请输出适合中文内容团队做选题判断的结构化研究，重点关注最新事实、分歧点、行业信号和可写角度。",
    ]
    if request["seed_urls"]:
        parts.append("优先参考这些链接：\n" + "\n".join(f"- {url}" for url in request["seed_urls"]))
    if request["source_excerpt"]:
        parts.append("首轮扫描上下文：\n" + request["source_excerpt"])
    if request["notes"]:
        parts.append("补充要求：\n" + request["notes"])
    return "\n\n".join(parts)


def collect_source_entries(node: Any) -> list[dict[str, str]]:
    found: list[dict[str, str]] = []

    def visit(value: Any) -> None:
        if isinstance(value, dict):
            url = clean_text(value.get("url") or value.get("link") or value.get("href"))
            title = clean_text(value.get("title") or value.get("name") or value.get("source"))
            snippet = clean_text(
                value.get("snippet")
                or value.get("summary")
                or value.get("excerpt")
                or value.get("content")
                or value.get("text")
            )
            if url:
                found.append({"title": title or url, "url": url, "snippet": truncate_text(snippet, 180)})
            for child in value.values():
                visit(child)
            return
        if isinstance(value, list):
            for item in value:
                visit(item)

    visit(node)

    deduped: list[dict[str, str]] = []
    seen_urls: set[str] = set()
    for item in found:
        if item["url"] in seen_urls:
            continue
        deduped.append(item)
        seen_urls.add(item["url"])
    return deduped


def collect_text_blocks(node: Any) -> list[str]:
    keys = {"report", "summary", "answer", "analysis", "content", "text", "final_report", "conclusion"}
    blocks: list[str] = []

    def visit(value: Any) -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                if key in keys and isinstance(child, str) and clean_text(child):
                    blocks.append(clean_text(child))
                else:
                    visit(child)
            return
        if isinstance(value, list):
            for item in value:
                visit(item)

    visit(node)
    return blocks


def build_conclusion_lines(text_blocks: list[str], source_entries: list[dict[str, str]]) -> list[str]:
    if text_blocks:
        return [f"- {truncate_text(block, 220)}" for block in text_blocks[:3]]
    if source_entries:
        return [f"- 目前主要线索集中在 {len(source_entries)} 个外部来源，建议优先回看引用最多的几条来源。"]
    return ["- Tavily 返回了结构化结果，但未识别到可直接抽取的结论文本。"]


def build_evidence_lines(source_entries: list[dict[str, str]]) -> list[str]:
    if not source_entries:
        return ["- 未识别到可枚举的引用来源，请直接查看 raw JSON。"]

    lines = []
    for index, entry in enumerate(source_entries[:6], start=1):
        lines.append(f"{index}. [{entry['title']}]({entry['url']})")
        if entry["snippet"]:
            lines.append(f"- 线索：{entry['snippet']}")
    return lines


def build_angle_lines(request: dict[str, Any], source_entries: list[dict[str, str]]) -> list[str]:
    base = [
        f"1. 围绕“{request['topic']}”写一篇判断文：先交代最新事实，再解释为什么现在值得关注。",
        f"2. 直接回答“{request['question']}”，拆成现状、分歧、机会与风险四段。",
    ]
    if source_entries:
        base.append(f"3. 选用引用最密集的 2 到 3 个来源，做一篇带来源脉络的深度综述。")
    else:
        base.append("3. 基于 raw JSON 再人工挑 2 到 3 个核心来源，补完素材后进入写作。")
    return base


def build_reference_lines(source_entries: list[dict[str, str]]) -> list[str]:
    if not source_entries:
        return ["- 暂无可枚举来源，请查看 raw JSON。"]
    return [f"- [{entry['title']}]({entry['url']})" for entry in source_entries[:10]]


def build_report(
    *,
    request: dict[str, Any],
    raw_path: Path,
    request_path: Path,
    source_entries: list[dict[str, str]],
    text_blocks: list[str],
    writing_decision: dict[str, Any],
) -> str:
    lines = [
        f"# 深度研究报告：{request['topic']}",
        "",
        "## 基础信息",
        "",
        f"- `date`：{request['date']}",
        f"- `slug`：{request['slug']}",
        f"- `topic`：{request['topic']}",
        f"- `model`：{request['model']}",
        f"- `request_path`：{request_path}",
    ]
    if request["source_file"] is not None:
        lines.append(f"- `source_file`：{request['source_file']}")
    if request["seed_urls"]:
        lines.append(f"- `seed_urls`：{', '.join(request['seed_urls'])}")

    lines.extend(
        [
            "",
            "## 研究问题",
            "",
            request["question"],
            "",
            "## 核心结论",
            "",
            *build_conclusion_lines(text_blocks, source_entries),
            "",
            "## 关键证据",
            "",
            *build_evidence_lines(source_entries),
            "",
            "## 候选写作角度",
            "",
            *build_angle_lines(request, source_entries),
            "",
            "## 选题是否值得写",
            "",
            f"- `writeworthiness_score`：{writing_decision.get('writeworthiness_score', 'N/A')}",
            f"- `recommendation`：{writing_decision.get('topic_score', {}).get('recommendation', 'unknown')}",
            "",
            "## 推荐读者与主痛点",
            "",
            f"- `reader_profile`：{writing_decision.get('primary_reader', '未识别')}",
            f"- `pain_point`：{writing_decision.get('primary_pain_point', '未识别')}",
            "",
            "## 推荐框架与论证顺序",
            "",
            f"- `recommended_structure`：{STRUCTURE_TYPES.get(writing_decision.get('recommended_structure', ''), writing_decision.get('recommended_structure', 'unknown'))}",
            f"- `recommended_opening_type`：{OPENING_TYPES.get(writing_decision.get('recommended_opening_type', ''), writing_decision.get('recommended_opening_label', 'unknown'))}",
            "- `论证顺序`：先交代事实与背景，再拆分分歧与机会，最后给出对读者的行动判断。",
            "",
            "## 开头钩子",
            "",
            f"- 建议先从“{OPENING_TYPES.get(writing_decision.get('recommended_opening_type', ''), '摘要切入')}”切入，再快速交代这件事为什么和读者有关。",
            "",
            "## 标题方向",
            "",
            *[f"- {item}" for item in (writing_decision.get("title_angles") or ["当前未生成标题方向"])],
            "",
            "## 风险与证据提醒",
            "",
            f"- `evidence_gap`：{writing_decision.get('evidence_gap', '未识别')}",
            f"- `risk_note`：{writing_decision.get('risk_note', '未识别')}",
            "",
            "## 参考来源",
            "",
            *build_reference_lines(source_entries),
            "",
            "## 原始数据位置",
            "",
            f"- Raw JSON：{raw_path}",
        ]
    )
    return "\n".join(lines) + "\n"


def run_topic_research(input_path: Path, *, workspace_root: Path, vendor_root: Path) -> dict[str, Any]:
    require_tvly()
    request = resolve_request(input_path, workspace_root=workspace_root)
    query = build_query(request)

    command = ["tvly", "research", query, "--json", "--model", request["model"]]
    completed = subprocess.run(
        command,
        cwd=vendor_root,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if completed.returncode != 0:
        raise RuntimeError(
            "Tavily research 执行失败："
            + (clean_text(completed.stderr) or clean_text(completed.stdout) or "未知错误")
        )

    payload = parse_json_output(completed.stdout)
    source_entries = collect_source_entries(payload)
    text_blocks = collect_text_blocks(payload)
    summary_seed = text_blocks[0] if text_blocks else request["question"]
    writing_decision = build_angle_pack(
        topic=request["topic"],
        summary=summary_seed,
        reader_hint="希望把研究结果转成公众号长文的中文读者",
        source_hint=request["question"],
        evidence_gap="需要优先回看一手来源，避免只根据自动研究摘要下结论。",
    )

    inbox_dir = workspace_root / "content-production" / "inbox"
    raw_path = inbox_dir / "raw" / "research" / request["raw_date"] / f"{request['slug']}.json"
    report_path = inbox_dir / f"{request['date']}-{request['slug']}-research.md"

    write_text(
        raw_path,
        json.dumps(
            {
                "generated_at": datetime.now().isoformat(timespec="seconds"),
                "request": {
                    "topic": request["topic"],
                    "question": request["question"],
                    "model": request["model"],
                    "source_file": str(request["source_file"]) if request["source_file"] is not None else "",
                    "seed_urls": request["seed_urls"],
                    "request_path": str(input_path),
                },
                "vendor_skill_path": str(vendor_root),
                "command": command,
                "stderr": completed.stderr,
                "payload": payload,
                "writing_decision": writing_decision,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
    )
    write_text(
        report_path,
        build_report(
            request=request,
            raw_path=raw_path,
            request_path=input_path,
            source_entries=source_entries,
            text_blocks=text_blocks,
            writing_decision=writing_decision,
        ),
    )

    return {
        "slug": request["slug"],
        "topic": request["topic"],
        "model": request["model"],
        "raw_path": raw_path,
        "report_path": report_path,
        "source_count": len(source_entries),
        "writeworthiness_score": writing_decision["writeworthiness_score"],
    }
