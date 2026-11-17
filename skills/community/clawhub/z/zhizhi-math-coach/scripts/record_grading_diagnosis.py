#!/usr/bin/env python3
"""Write grading diagnosis artifacts from one compact JSON payload."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from run_log import Timer, append_run_log, new_run_id  # noqa: E402
from validate_diagnosis_payload import validate_payload  # noqa: E402
from grading_followup import normalize_payload, plan_followup  # noqa: E402
from knowledge_assessment import assess_knowledge, render_knowledge  # noqa: E402
from workspace_transaction import inside, record_once  # noqa: E402


def text(value: Any, default: str = "") -> str:
    if value is None:
        return default
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value).strip()


def text_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        items = value
    else:
        items = [value]
    result = []
    for item in items:
        item_text = text(item)
        if item_text:
            result.append(item_text)
    return result


def slugify(value: Any, fallback: str = "diagnosis") -> str:
    original = text(value)
    raw = original.lower()
    slug = re.sub(r"[^a-z0-9._-]+", "-", raw)
    slug = re.sub(r"-{2,}", "-", slug).strip("-._")
    if slug:
        return slug
    if original:
        digest = hashlib.sha1(original.encode("utf-8")).hexdigest()[:8]
        prefix = fallback or "item"
        return f"{prefix}-{digest}"
    return fallback


def table_cell(value: Any) -> str:
    value_text = text(value, "unknown")
    return value_text.replace("\n", "<br>").replace("|", r"\|")


def bullet_lines(values: Any) -> list[str]:
    return [f"- {item}" for item in text_list(values)]


def ensure_workspace_dirs(workspace: Path) -> None:
    for rel in ["records", "mistakes", "weak-points", "memory"]:
        (workspace / rel).mkdir(parents=True, exist_ok=True)


def unique_path(path: Path) -> Path:
    if not path.exists():
        return path
    stem = path.stem
    suffix = path.suffix
    for index in range(2, 100):
        candidate = path.with_name(f"{stem}-{index}{suffix}")
        if not candidate.exists():
            return candidate
    raise RuntimeError(f"too many existing diagnosis files for {path.name}")


def read_json(path: str) -> dict[str, Any]:
    if path == "-":
        return json.load(sys.stdin)
    with Path(path).open("r", encoding="utf-8") as f:
        return json.load(f)


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def append_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    prefix = ""
    if path.exists() and path.read_text(encoding="utf-8").strip():
        prefix = "\n\n"
    with path.open("a", encoding="utf-8") as f:
        f.write(prefix + content.rstrip() + "\n")


def append_line(path: Path, line: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        existing = path.read_text(encoding="utf-8")
        separator = "" if existing.endswith("\n") else "\n"
    else:
        separator = ""
    with path.open("a", encoding="utf-8") as f:
        f.write(separator + line.rstrip() + "\n")


def source_book(payload: dict[str, Any]) -> Path:
    explicit = slugify(payload.get("mistake_book") or payload.get("source_type"), "")
    if explicit in {
        "system",
        "generated",
        "worksheet",
        "system-mistakes",
        "system-mistakes.md",
        "system-worksheet",
        "generated-worksheet",
        "system-worksheet-mistakes",
    }:
        return Path("mistakes/system-mistakes.md")
    return Path("mistakes/school-mistakes.md")


def summary_rows(values: Any) -> list[str]:
    if not isinstance(values, list):
        return text_list(values)
    rows = []
    for value in values:
        if isinstance(value, dict):
            cause = text(value.get("cause") or value.get("title") or value.get("name"), "未命名归因")
            count = text(value.get("count"), "")
            judgment = text(value.get("judgment") or value.get("finding") or value.get("note"), "")
            parts = [cause]
            if count:
                parts.append(f"{count}题")
            if judgment:
                parts.append(judgment)
            rows.append(": ".join([parts[0], " / ".join(parts[1:])]) if len(parts) > 1 else parts[0])
        else:
            value_text = text(value)
            if value_text:
                rows.append(value_text)
    return rows


def render_diagnosis(payload: dict[str, Any], diagnosis_slug: str) -> str:
    mistakes = payload.get("mistakes") or []
    if not isinstance(mistakes, list):
        raise ValueError("mistakes must be a list")

    lines = [
        f"# 批改诊断：{text(payload.get('source') or diagnosis_slug, diagnosis_slug)}",
        "",
        f"- 日期：{text(payload.get('date'))}",
        f"- 学年：{text(payload.get('school_year'), 'unknown')}",
        f"- 年级：{text(payload.get('grade'), 'unknown')}",
        f"- 学期：{text(payload.get('semester'), 'unknown')}",
        f"- 学期时间段：{text(payload.get('semester_range'), 'unknown')}",
        f"- 学期阶段：{text(payload.get('term_phase'), 'unknown')}",
        f"- 来源：{text(payload.get('source'), 'unknown')}",
        f"- 范围：{text(payload.get('scope'), 'unknown')}",
        f"- 总题数：{text(payload.get('total_items'), 'unknown')}",
        f"- 正确数：{text(payload.get('correct_items'), 'unknown')}",
        f"- 总体判断：{text(payload.get('overall'), '待补充')}",
        "",
        *render_paper_evidence(payload),
        "## 错题与待确认项",
        "",
        "| 题号 | 题目 | 孩子答案 | 正确答案 | 结果 | 错题类型 | 可能原因 | 历史状态 | 复发判断 | 证据 | 置信度 | 补救动作 |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in mistakes:
        if not isinstance(item, dict):
            continue
        lines.append(
            "| "
            + " | ".join(
                [
                    table_cell(item.get("item_no")),
                    table_cell(item.get("question")),
                    table_cell(item.get("student_answer")),
                    table_cell(item.get("correct_answer")),
                    table_cell(item.get("result")),
                    table_cell(item.get("error_type")),
                    table_cell(item.get("cause")),
                    table_cell(item.get("historical_status")),
                    table_cell(item.get("relapse_judgment")),
                    table_cell(item.get("evidence")),
                    table_cell(item.get("confidence")),
                    table_cell(item.get("remediation")),
                ]
            )
            + " |"
        )

    lines.extend(["", "## 归因汇总", ""])
    cause_rows = summary_rows(payload.get("cause_summary"))
    lines.extend(bullet_lines(cause_rows) or ["- 待补充"])

    lines.extend(["", "## 讲解与验证练习", ""])
    teaching_blocks = payload.get("teaching_and_practice") or []
    if isinstance(teaching_blocks, list) and teaching_blocks:
        for block in teaching_blocks:
            if not isinstance(block, dict):
                continue
            title = text(block.get("title") or block.get("cause"), "重点问题")
            lines.extend([f"### {title}", "", f"讲解：{text(block.get('explanation'), '待补充')}", "", "验证题："])
            questions = text_list(block.get("validation_questions"))
            lines.extend([f"{idx}. {question}" for idx, question in enumerate(questions, start=1)] or ["待补充"])
            lines.append("")
    else:
        lines.append("待补充")

    next_steps = payload.get("next_steps") or {}
    if not isinstance(next_steps, dict):
        next_steps = {"下次练习": text(next_steps)}
    lines.extend(
        [
            "## 下一步",
            "",
            f"- 更新薄弱项：{text(next_steps.get('weak_points'), '按证据追加')}",
            f"- 更新错题集：{text(next_steps.get('mistake_book'), '已记录错题或待确认题')}",
            f"- 下次练习：{text(next_steps.get('practice'), '待安排')}",
            f"- 复测标准：{text(next_steps.get('recheck_standard'), '待补充')}",
            f"- 是否复发：{text(next_steps.get('relapse'), '待判断')}",
        ]
    )
    return "\n".join(lines)


def render_paper_evidence(payload: dict[str, Any]) -> list[str]:
    lines = ["## 原始试卷", ""]
    for index, path in enumerate(payload.get("archived_images", []), 1):
        lines.extend([f"![原图第{index}页]({path})", ""])
    if not payload.get("archived_images"):
        lines.extend(["未提供原图；仅保存本次提供的文本证据。", ""])
    items = payload.get("items")
    if items is None:
        return lines + ["本次为旧版错题记录，未提供完整试卷题目。", ""]
    labels = {"correct": "正确", "wrong": "错误", "unanswered": "未作答", "need-confirmation": "待确认"}
    lines.extend(["## 全卷逐题档案", "", f"- 覆盖范围：{payload.get('coverage', 'complete')}（partial 表示图片或题目不完整）", ""])
    for item in items:
        points = "、".join(point["title"] for point in item.get("knowledge_points", [])) or "待识别"
        lines.extend([
            f"### 题 {text(item.get('item_no'))} · {labels.get(item.get('result'), '待确认')}", "",
            f"- 原图页码：{text(item.get('page'), '未标注')}",
            f"- 题目：{text(item.get('question'), '待确认')}",
            f"- 图形信息：{text(item.get('diagram_description'), '无/未提供')}",
            f"- 孩子作答：{text(item.get('student_answer'), '未作答/未识别')}",
            f"- 正确答案：{text(item.get('correct_answer'), '待确认')}",
            f"- 作答步骤：{text(item.get('student_work'), '未提供')}",
            f"- 知识点：{points}",
            f"- 识别置信度：{text(item.get('recognition_confidence'), 'low')}",
            f"- 是否借助提示：{text(item.get('assisted', False))}",
            f"- 解析：{text(item.get('explanation'), '待补充')}", "",
        ])
    return lines


def render_mistake_entry(payload: dict[str, Any], item: dict[str, Any]) -> str:
    source = text(payload.get("source"), "unknown")
    title = f"### {text(payload.get('date'))} - {source} - 题{table_cell(item.get('item_no'))}"
    fields = [
        ("学期", payload.get("semester")),
        ("学期时间段", payload.get("semester_range")),
        ("来源类型", payload.get("source_type") or payload.get("mistake_book")),
        ("来源文件", payload.get("source_file") or payload.get("source_image") or source),
        ("题目", item.get("question")),
        ("孩子答案", item.get("student_answer")),
        ("正确答案", item.get("correct_answer")),
        ("错题类型", item.get("error_type")),
        ("可能原因", item.get("cause")),
        ("对应薄弱项", item.get("weak_point_slug") or item.get("weak_point_title")),
        ("复发判断", item.get("relapse_judgment")),
        ("复练状态", item.get("repractice_status") or item.get("status")),
        ("后续处理", item.get("remediation")),
    ]
    lines = [title, ""]
    lines.extend(f"- {label}：{text(value, 'unknown')}" for label, value in fields)
    return "\n".join(lines)


def append_mistakes(workspace: Path, payload: dict[str, Any]) -> Path | None:
    mistakes = payload.get("mistakes") or []
    if not mistakes:
        return None
    path = workspace / source_book(payload)
    if not path.exists():
        write_text(path, f"# {path.stem.replace('-', ' ').title()}\n\n## Entries")
    entries = [render_mistake_entry(payload, item) for item in mistakes if isinstance(item, dict)]
    if entries:
        append_text(path, "\n\n".join(entries))
    return path


def progress_payload(payload: dict[str, Any]) -> dict[str, Any]:
    progress = payload.get("progress") or {}
    if not isinstance(progress, dict):
        progress = {}
    return progress


def append_progress(workspace: Path, payload: dict[str, Any]) -> Path:
    path = workspace / "records/learning-progress.md"
    if not path.exists():
        write_text(
            path,
            "# Learning Progress\n\n## Current Overview\n\n| Weak Point | Status | Latest Evidence Date | Relapse Count | Recent Evidence | Next Step |\n| --- | --- | --- | --- | --- | --- |\n\n## Dated Records\n\n| Date | Type | Source/Topic | Result | Finding | Next Step |\n| --- | --- | --- | --- | --- | --- |",
        )
    progress = progress_payload(payload)
    next_steps = payload.get("next_steps") if isinstance(payload.get("next_steps"), dict) else {}
    next_step = progress.get("next_step") or next_steps.get("practice") or ""
    row = "| {date} | {type} | {source} | {result} | {finding} | {next_step} |".format(
        date=table_cell(payload.get("date")),
        type=table_cell(progress.get("type") or payload.get("source_type") or "grading"),
        source=table_cell(progress.get("source_topic") or payload.get("source") or payload.get("scope")),
        result=table_cell(progress.get("result") or f"{text(payload.get('correct_items'), 'unknown')}/{text(payload.get('total_items'), 'unknown')}"),
        finding=table_cell(progress.get("finding") or payload.get("overall")),
        next_step=table_cell(next_step),
    )
    append_line(path, row)
    return path


def weak_point_payloads(payload: dict[str, Any]) -> list[dict[str, Any]]:
    weak_points = payload.get("weak_points")
    if isinstance(weak_points, list):
        return [item for item in weak_points if isinstance(item, dict)]
    return []


def create_weak_point_content(payload: dict[str, Any], wp: dict[str, Any]) -> str:
    title = text(wp.get("title") or wp.get("slug"), "未命名薄弱项")
    date = text(payload.get("date"))
    likely_causes = bullet_lines(wp.get("likely_causes") or wp.get("causes"))
    teaching = bullet_lines(wp.get("teaching_strategy"))
    validation = bullet_lines(wp.get("validation_strategy"))
    history = text(wp.get("history_note") or payload.get("overall"), "新增诊断证据")
    return "\n".join(
        [
            f"# Weak Point: {title}",
            "",
            f"- 当前状态：{text(wp.get('status'), '观察中')}",
            f"- 首次发现日期：{date}",
            f"- 最近证据日期：{date}",
            f"- 复发次数：{text(wp.get('relapse_count'), '0')}",
            f"- 对应知识点：{text(wp.get('knowledge_point'), '待补充')}",
            f"- 下次复练日期：{text(wp.get('next_review_date'), '待安排')}",
            f"- 复练优先级：{text(wp.get('priority'), 'normal')}",
            "",
            "## 典型表现",
            "",
            *(bullet_lines(wp.get("typical_behavior")) or ["- 待补充"]),
            "",
            "## 可能原因",
            "",
            *(likely_causes or ["- 待补充"]),
            "",
            "## 讲解策略",
            "",
            *(teaching or ["- 待补充"]),
            "",
            "## 验证练习策略",
            "",
            *(validation or ["- 待补充"]),
            "",
            "## 复发处理策略",
            "",
            f"- {text(wp.get('relapse_strategy'), '如再次出现同因错误，按复发或迁移失败处理。')}",
            "",
            "## 历史记录",
            "",
            f"- {date}: {history}",
            "",
            "## 下次动作",
            "",
            f"- {text(wp.get('next_action'), '安排短练并复测。')}",
        ]
    )


def append_weak_points(workspace: Path, payload: dict[str, Any]) -> list[Path]:
    paths = []
    for wp in weak_point_payloads(payload):
        slug = slugify(wp.get("slug") or wp.get("title"), "")
        if not slug:
            continue
        path = workspace / "weak-points" / f"{slug}.md"
        if path.exists():
            content = path.read_text(encoding="utf-8")
            for key, label in [("status", "当前状态"), ("next_review_date", "下次复练日期"), ("priority", "复练优先级")]:
                if wp.get(key):
                    content = re.sub(rf"^- {label}：.*$", lambda _: f"- {label}：{text(wp[key])}", content, flags=re.MULTILINE)
            content = re.sub(r"^- 最近证据日期：.*$", lambda _: f"- 最近证据日期：{text(payload.get('date'))}", content, flags=re.MULTILINE)
            write_text(path, content)
            update = "\n".join(
                [
                    f"## 证据更新：{text(payload.get('date'))}",
                    "",
                    f"- 状态：{text(wp.get('status'), '观察中')}",
                    f"- 证据：{text(wp.get('history_note') or payload.get('overall'), '新增诊断证据')}",
                    f"- 复发判断：{text(wp.get('relapse_judgment') or payload.get('relapse_judgment'), '待判断')}",
                    f"- 下次动作：{text(wp.get('next_action'), '安排短练并复测。')}",
                ]
            )
            append_text(path, update)
        else:
            write_text(path, create_weak_point_content(payload, wp))
        paths.append(path)
    return paths


def append_memory_notes(workspace: Path, payload: dict[str, Any]) -> list[Path]:
    paths = []
    date = text(payload.get("date"))
    for key, rel_path, title in [
        ("short_term_notes", "memory/short-term.md", "## Update"),
        ("long_term_notes", "memory/long-term.md", "## Evidence-Backed Update"),
    ]:
        notes = text_list(payload.get(key))
        if not notes:
            continue
        path = workspace / rel_path
        if not path.exists():
            write_text(path, f"# {Path(rel_path).stem.replace('-', ' ').title()}")
        append_text(path, "\n".join([f"{title}: {date}", "", *[f"- {note}" for note in notes]]))
        paths.append(path)
    return paths


def write_active_context(workspace: Path, payload: dict[str, Any]) -> Path | None:
    content = text(payload.get("active_context_md"))
    if not content:
        return None
    path = workspace / "memory/active-context.md"
    write_text(path, content)
    return path


def write_diagnosis(workspace: Path, payload: dict[str, Any]) -> Path:
    date = text(payload.get("date")) or dt.date.today().isoformat()
    payload["date"] = date
    diagnosis_slug = slugify(payload.get("source_slug") or payload.get("source") or payload.get("scope"), "grading")
    path = unique_path(workspace / "records" / f"{date}-{diagnosis_slug}-diagnosis.md")
    write_text(path, render_diagnosis(payload, diagnosis_slug))
    return path


def prepare_recording(workspace: Path, payload: dict, mode: str, warnings: list[str]) -> tuple[dict, dict]:
    payload, decision = plan_followup(workspace, payload, mode)
    slug = slugify(payload.get("source_slug") or payload["source"], "grading")
    diagnosis = unique_path(inside(workspace, f"records/{payload['date']}-{slug}-diagnosis.md"))
    diagnosis_rel = diagnosis.relative_to(workspace).as_posix()
    stem = Path(diagnosis_rel).stem.removesuffix("-diagnosis")
    targets = ["records/learning-progress.md", "records/next-practice.json", "records/knowledge-state.json",
               "records/knowledge-mastery.md", source_book(payload).as_posix(),
               "memory/short-term.md", "memory/long-term.md", "memory/active-context.md"]
    targets.extend(f"weak-points/{slugify(wp.get('slug') or wp.get('title'), '')}.md" for wp in weak_point_payloads(payload))
    with tempfile.TemporaryDirectory() as tmp:
        staging = Path(tmp)
        for rel in set(targets):
            original = inside(workspace, rel)
            if original.is_file():
                target = inside(staging, rel)
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(original, target)
        archived = []
        image_paths = []
        for index, source in enumerate(payload.get("source_images", []), 1):
            original = Path(source)
            if not original.is_absolute():
                original = workspace / original
            if original.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp", ".heic"} or not original.is_file():
                raise ValueError(f"source image is missing or unsupported: {source}")
            rel = f"records/{stem}-assets/page-{index}{original.suffix.lower()}"
            target = inside(staging, rel)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(original, target)
            archived.append(Path(rel).relative_to("records").as_posix())
            image_paths.append(target)
        payload["archived_images"] = archived
        payload["decision"] = decision
        diagnosis_path = staging / diagnosis_rel
        write_text(diagnosis_path, render_diagnosis(payload, slug))
        evidence_path = diagnosis_path.with_suffix(".json")
        write_text(evidence_path, json.dumps(payload, ensure_ascii=False, indent=2))
        written = [diagnosis_path, evidence_path, *image_paths, append_progress(staging, payload)]
        mistake_result = append_mistakes(staging, payload)
        if mistake_result:
            written.append(mistake_result)
        written.extend(append_weak_points(staging, payload))
        written.extend(append_memory_notes(staging, payload))
        active = write_active_context(staging, payload)
        if active:
            written.append(active)
        plan_path = staging / "records/next-practice.json"
        previous = json.loads(plan_path.read_text(encoding="utf-8")) if plan_path.exists() else {}
        reviews = {review["slug"]: review for review in previous.get("reviews", [])}
        for review in decision["reviews"]:
            old = reviews.get(review["slug"], {})
            if old.get("evidence_date", "") <= review["evidence_date"]:
                reviews[review["slug"]] = review
        write_text(plan_path, json.dumps({"updated": max(previous.get("updated", ""), payload["date"]),
                                        "reviews": list(reviews.values())}, ensure_ascii=False, indent=2))
        written.append(plan_path)
        knowledge_summary = []
        if payload.get("items"):
            state_path = staging / "records/knowledge-state.json"
            previous_state = json.loads(state_path.read_text(encoding="utf-8")) if state_path.exists() else {}
            state = assess_knowledge(previous_state, payload, diagnosis_rel)
            write_text(state_path, json.dumps(state, ensure_ascii=False, indent=2))
            dashboard = staging / "records/knowledge-mastery.md"
            write_text(dashboard, render_knowledge(state))
            written.extend([state_path, dashboard])
            paper_ids = list(dict.fromkeys(point["id"] for item in payload["items"] for point in item.get("knowledge_points", [])))
            knowledge_summary = [{"id": key, **{k: v for k, v in state["concepts"][key].items() if k != "recent_evidence"}}
                                 for key in paper_ids]
            for point in knowledge_summary:
                key = "knowledge:" + point["id"]
                reviews[key] = {"slug": key, "topic": point["title"], "evidence_date": point["latest_date"],
                                "due_date": point["next_review_date"], "status": point["status"],
                                "strategy": "diagnostic_probe" if point["status"] in {"待确认", "待观察"} else "spaced_review",
                                "action": "按知识点安排3道独立作答的变式题，记录步骤和是否需要提示。"}
            write_text(plan_path, json.dumps({"updated": state["updated"], "reviews": list(reviews.values())}, ensure_ascii=False, indent=2))
        files = {path.relative_to(staging).as_posix(): path.read_bytes() for path in written}
    return files, {"ok": True, "written": list(files), "warnings": warnings,
                   "decision": decision, "knowledge_assessment": knowledge_summary}


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Record a zhizhi-math-coach grading diagnosis from JSON.")
    parser.add_argument("--workspace", type=Path, default=Path("."), help="Personal learning repository root.")
    parser.add_argument("--input", default="-", help="JSON payload path, or '-' for stdin.")
    parser.add_argument("--mode", choices=["auto", "fast_grade_light_record", "full_archive"], default="auto")
    parser.add_argument("--dry-run", action="store_true", help="Validate and print planned output paths without writing.")
    parser.add_argument("--run-id", default="", help="Optional run id for .zhizhi-math-coach/run-log.jsonl.")
    parser.add_argument("--no-log", action="store_true", help="Do not append run-log.jsonl.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    timer = Timer()
    workspace = args.workspace.resolve()
    run_id = args.run_id or new_run_id()
    ok = False
    validation_errors: list[str] = []
    validation_warnings: list[str] = []
    written_rel: list[str] = []
    dry_run = bool(args.dry_run)
    try:
        payload = read_json(args.input)
        if not isinstance(payload, dict):
            raise ValueError("input JSON must be an object")

        payload = normalize_payload(payload)
        errors, warnings = validate_payload(payload, mode=args.mode)
        validation_errors = errors
        validation_warnings = warnings
        if errors:
            print(json.dumps({"ok": False, "errors": errors, "warnings": warnings}, ensure_ascii=False, indent=2))
            return 1

        if args.dry_run:
            enriched, decision = plan_followup(workspace, payload, args.mode)
            ok = True
            print(json.dumps({"ok": True, "dry_run": True, "decision": decision,
                              "warnings": warnings}, ensure_ascii=False, indent=2))
            return 0

        result = record_once(workspace, payload, lambda: prepare_recording(workspace, payload, args.mode, warnings))
        written_rel = result["written"]
        ok = True
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    finally:
        if not args.no_log and not args.dry_run:
            append_run_log(
                workspace,
                {
                    "run_id": run_id,
                    "script": "record_grading_diagnosis.py",
                    "mode": args.mode,
                    "ok": ok,
                    "dry_run": dry_run,
                    "duration_ms": timer.elapsed_ms(),
                    "written": written_rel,
                    "validation_errors": validation_errors,
                    "validation_warnings": validation_warnings,
                },
            )


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
