#!/usr/bin/env python3

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from urllib.parse import urlparse


MARKDOWN_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
BARE_URL_RE = re.compile(r"https?://[^\s)>]+")
HEADING_RE = re.compile(r"^\s{0,3}#\s+(.+?)\s*$")


@dataclass(frozen=True)
class SourceItem:
    title: str
    locator: str
    source_type: str
    classification: str
    origin: str
    statement: str
    relevance: str
    limitations: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Build a markdown evidence ledger draft from local markdown/text files. "
            "The script extracts markdown links, bare URLs, and the input files themselves "
            "as candidate evidence items."
        )
    )
    parser.add_argument(
        "inputs",
        nargs="+",
        help="Markdown or text files to scan for evidence sources.",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Write the ledger to this file instead of stdout.",
    )
    parser.add_argument(
        "--id-prefix",
        default="E",
        help="Prefix for evidence ids. Default: E",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_paths = [Path(value).expanduser().resolve() for value in args.inputs]
    missing = [str(path) for path in input_paths if not path.exists()]
    if missing:
        for item in missing:
            print(f"Missing input: {item}", file=sys.stderr)
        return 1

    sources = collect_sources(input_paths)
    output = render_ledger(sources, args.id_prefix)

    if args.output:
        output_path = Path(args.output).expanduser().resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output, encoding="utf-8")
    else:
        sys.stdout.write(output)

    return 0


def collect_sources(paths: Iterable[Path]) -> list[SourceItem]:
    items_by_key: dict[str, SourceItem] = {}
    local_result_sources: list[SourceItem] = []

    for path in paths:
        if path.is_file():
            local_source = build_local_source(path)
            add_source(items_by_key, local_source)
            if local_source.source_type == "local_result":
                local_result_sources.append(local_source)

            if path.suffix.lower() not in {".md", ".txt"}:
                continue

            text = path.read_text(encoding="utf-8")
            for title, locator in extract_markdown_links(text):
                add_source(items_by_key, build_external_source(title, locator, path.name))
            for locator in extract_bare_urls(text):
                add_source(
                    items_by_key,
                    build_external_source(guess_title_from_url(locator), locator, path.name),
                )

    if len(local_result_sources) >= 2:
        add_source(items_by_key, build_aggregate_result_source(local_result_sources))

    return list(items_by_key.values())


def add_source(items_by_key: dict[str, SourceItem], source: SourceItem) -> None:
    key = canonical_source_key(source.locator)
    existing = items_by_key.get(key)
    if existing is None or source_priority(source) > source_priority(existing):
        items_by_key[key] = source


def build_local_source(path: Path) -> SourceItem:
    title = extract_local_title(path)
    source_type = guess_local_source_type(path)
    structured = parse_local_artifact(path, source_type)
    classification = guess_local_classification(path, source_type, structured)
    return SourceItem(
        title=structured.get("title", title),
        locator=str(path),
        source_type=source_type,
        classification=classification,
        origin=path.name,
        statement=build_local_statement(path, title, source_type, structured),
        relevance=build_local_relevance(path, source_type, structured),
        limitations=build_local_limitations(source_type, structured),
    )


def build_external_source(title: str, locator: str, origin: str) -> SourceItem:
    source_type = guess_external_source_type(locator)
    return SourceItem(
        title=title,
        locator=locator,
        source_type=source_type,
        classification="unverified",
        origin=origin,
        statement=f"TODO: review the exact claim or observation from {title}.",
        relevance=f"TODO: explain why {title} matters for this evidence pack. Found in {origin}.",
        limitations="TODO: state scope limits, comparability risks, or verification gaps.",
    )


def extract_local_title(path: Path) -> str:
    if path.suffix.lower() in {".md", ".txt"}:
        for line in path.read_text(encoding="utf-8").splitlines():
            match = HEADING_RE.match(line)
            if match:
                return match.group(1).strip()
    return path.stem.replace("-", " ").replace("_", " ").strip() or path.name


def parse_structured_markdown(path: Path) -> dict[str, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    fields: dict[str, list[str]] = {}
    current_heading = ""

    for raw_line in lines:
        heading = HEADING_RE.match(raw_line)
        if heading:
            current_heading = heading.group(1).strip().lower()
            continue
        stripped = raw_line.strip()
        if not stripped.startswith("- ") or ":" not in stripped:
            continue
        key, value = stripped[2:].split(":", 1)
        normalized_key = key.strip().lower()
        full_key = normalized_key if not current_heading else f"{current_heading}:{normalized_key}"
        fields.setdefault(full_key, []).append(value.strip())
        fields.setdefault(normalized_key, []).append(value.strip())

    flattened: dict[str, str] = {}
    for key, values in fields.items():
        cleaned = [value for value in values if value]
        if cleaned:
            flattened[key] = "; ".join(cleaned)
    return flattened


def parse_local_artifact(path: Path, source_type: str) -> dict[str, str]:
    suffix = path.suffix.lower()
    if suffix in {".md", ".txt"}:
        return parse_structured_markdown(path)
    if source_type == "local_result" and suffix in {".csv", ".tsv"}:
        return parse_tabular_result_artifact(path, delimiter="\t" if suffix == ".tsv" else ",")
    if source_type == "local_result" and suffix == ".json":
        return parse_json_result_artifact(path)
    return {}


def parse_tabular_result_artifact(path: Path, delimiter: str) -> dict[str, str]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter=delimiter)
        fieldnames = reader.fieldnames or []
        rows = list(reader)

    lowered = {name.lower(): name for name in fieldnames}
    metrics = normalize_values(collect_column_values(rows, lowered, ["metric", "metrics"]), kind="metric")
    if not metrics:
        metrics = normalize_values(infer_metric_columns(fieldnames), kind="metric")
    baselines = normalize_values(
        collect_column_values(rows, lowered, ["baseline", "baselines", "model", "method", "system"]),
        kind="baseline",
    )
    benchmarks = normalize_values(
        collect_column_values(rows, lowered, ["benchmark", "dataset", "task", "suite", "split"]),
        kind="scope",
    )
    run_ids = collect_column_values(rows, lowered, ["run_id", "run ids", "run", "trial"])

    structured: dict[str, str] = {
        "title": path.stem.replace("-", " ").replace("_", " "),
        "artifact type": "tabular result artifact",
        "path": str(path),
        "metric": ", ".join(metrics[:4]) if metrics else infer_metric_from_headers(fieldnames),
        "scope": ", ".join(benchmarks[:3]) if benchmarks else infer_scope_from_filename(path),
        "provenance": f"parsed from {path.name}",
    }
    if benchmarks:
        structured["benchmark"] = ", ".join(benchmarks[:3])
    if baselines:
        structured["baseline set"] = ", ".join(baselines[:4])
    if run_ids:
        structured["run ids"] = ", ".join(run_ids[:5])
    return structured


def parse_json_result_artifact(path: Path) -> dict[str, str]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    rows: list[dict[str, object]]
    if isinstance(payload, list):
        rows = [item for item in payload if isinstance(item, dict)]
    elif isinstance(payload, dict):
        if isinstance(payload.get("results"), list):
            rows = [item for item in payload["results"] if isinstance(item, dict)]
        else:
            rows = [payload]
    else:
        rows = []

    keys = sorted({str(key) for row in rows for key in row.keys()})
    lowered = {name.lower(): name for name in keys}
    metrics = normalize_values(collect_object_values(rows, lowered, ["metric", "metrics"]), kind="metric")
    if not metrics:
        metrics = normalize_values(infer_metric_columns(keys), kind="metric")
    baselines = normalize_values(
        collect_object_values(rows, lowered, ["baseline", "baselines", "model", "method", "system"]),
        kind="baseline",
    )
    benchmarks = normalize_values(
        collect_object_values(rows, lowered, ["benchmark", "dataset", "task", "suite", "split"]),
        kind="scope",
    )
    run_ids = collect_object_values(rows, lowered, ["run_id", "run ids", "run", "trial"])

    structured: dict[str, str] = {
        "title": path.stem.replace("-", " ").replace("_", " "),
        "artifact type": "json result artifact",
        "path": str(path),
        "metric": ", ".join(metrics[:4]) if metrics else infer_metric_from_headers(keys),
        "scope": ", ".join(benchmarks[:3]) if benchmarks else infer_scope_from_filename(path),
        "provenance": f"parsed from {path.name}",
    }
    if benchmarks:
        structured["benchmark"] = ", ".join(benchmarks[:3])
    if baselines:
        structured["baseline set"] = ", ".join(baselines[:4])
    if run_ids:
        structured["run ids"] = ", ".join(run_ids[:5])
    return structured


def collect_column_values(
    rows: list[dict[str, str]],
    lowered_map: dict[str, str],
    candidates: list[str],
) -> list[str]:
    values: list[str] = []
    seen: set[str] = set()
    for candidate in candidates:
        column = lowered_map.get(candidate)
        if not column:
            continue
        for row in rows[:50]:
            value = clean_table_value(row.get(column, ""))
            if value and value.lower() not in seen:
                seen.add(value.lower())
                values.append(value)
    return values


def collect_object_values(
    rows: list[dict[str, object]],
    lowered_map: dict[str, str],
    candidates: list[str],
) -> list[str]:
    values: list[str] = []
    seen: set[str] = set()
    for candidate in candidates:
        column = lowered_map.get(candidate)
        if not column:
            continue
        for row in rows[:50]:
            value = clean_table_value(str(row.get(column, "")))
            if value and value.lower() not in seen:
                seen.add(value.lower())
                values.append(value)
    return values


def infer_metric_columns(fieldnames: list[str]) -> list[str]:
    metrics: list[str] = []
    for name in fieldnames:
        lowered = name.lower()
        if any(token in lowered for token in ["success", "accuracy", "precision", "recall", "f1", "pass@", "score", "metric"]):
            metrics.append(name)
    return metrics[:4]


def infer_metric_from_headers(fieldnames: list[str]) -> str:
    inferred = infer_metric_columns(fieldnames)
    if inferred:
        return ", ".join(inferred[:4])
    return "an internal metric"


def infer_scope_from_filename(path: Path) -> str:
    label = path.stem.replace("-", " ").replace("_", " ")
    return label or "the current evaluation scope"


def clean_table_value(value: str) -> str:
    value = re.sub(r"\s+", " ", str(value)).strip()
    if value in {"", "nan", "null", "none", "None"}:
        return ""
    return value


def normalize_values(values: list[str], *, kind: str) -> list[str]:
    normalized: list[str] = []
    seen: set[str] = set()
    for value in values:
        item = normalize_value(value, kind=kind)
        if item and item.lower() not in seen:
            seen.add(item.lower())
            normalized.append(item)
    return normalized


def normalize_value(value: str, *, kind: str) -> str:
    text = clean_table_value(value).replace("_", " ").replace("-", " ")
    collapsed = re.sub(r"\s+", " ", text).strip()
    lowered = collapsed.lower()
    if not lowered:
        return ""
    if kind == "metric":
        aliases = {
            "success rate": "success rate",
            "success_rate": "success rate",
            "accuracy": "accuracy",
            "precision": "precision",
            "recall": "recall",
            "f1": "F1",
            "pass@k": "pass@k",
            "pass k": "pass@k",
            "score": "score",
        }
        return aliases.get(lowered, collapsed)
    return collapsed


def build_aggregate_result_source(sources: list[SourceItem]) -> SourceItem:
    metrics = collect_field_fragments(sources, marker="Candidate metric fact: This artifact defines or reports ")
    baselines = collect_field_fragments(sources, marker="Candidate baseline fact: This artifact compares against ")
    scopes = collect_scope_fragments(sources)
    metric_text = ", ".join(metrics[:4]) if metrics else "internal metrics"
    scope_text = ", ".join(scopes[:4]) if scopes else "current evaluation scopes"
    baseline_text = ", ".join(baselines[:5]) if baselines else "task-aligned baselines"
    statement = (
        f"Aggregated result artifacts cover {metric_text} across {scope_text}. "
        f"Candidate baseline fact: Combined artifacts compare against {baseline_text}."
    )
    return SourceItem(
        title="Aggregated Result Artifacts",
        locator=f"aggregate://local-results/{len(sources)}",
        source_type="local_result",
        classification="project_evidence",
        origin="aggregated-local-results",
        statement=statement,
        relevance=f"This aggregate project evidence summarizes {len(sources)} local result artifacts across {scope_text}.",
        limitations="Aggregate result evidence still requires manual checks for metric alignment, split compatibility, and fair baseline matching.",
    )


def collect_field_fragments(sources: list[SourceItem], *, marker: str) -> list[str]:
    values: list[str] = []
    seen: set[str] = set()
    for source in sources:
        for sentence in source.statement.split("."):
            cleaned = sentence.strip()
            if marker.lower() in cleaned.lower():
                raw_value = cleaned.split(marker, 1)[-1].strip().rstrip(".")
                for part in [piece.strip() for piece in raw_value.split(",") if piece.strip()]:
                    value = normalize_value(part, kind="metric" if "metric" in marker.lower() else "baseline")
                    if value and value.lower() not in seen:
                        seen.add(value.lower())
                        values.append(value)
    return values


def collect_scope_fragments(sources: list[SourceItem]) -> list[str]:
    values: list[str] = []
    seen: set[str] = set()
    pattern = re.compile(r"tracks .*? for (.+?)(?: against|$)", re.IGNORECASE)
    for source in sources:
        match = pattern.search(source.statement)
        if not match:
            continue
        raw_value = match.group(1).strip()
        for part in [piece.strip() for piece in raw_value.split(",") if piece.strip()]:
            value = normalize_value(part, kind="scope")
            if value and value.lower() not in seen:
                seen.add(value.lower())
                values.append(value)
    return values


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    results: list[tuple[str, str]] = []
    for title, locator in MARKDOWN_LINK_RE.findall(text):
        if locator.startswith("#"):
            continue
        results.append((title.strip() or guess_title_from_url(locator), locator.strip()))
    return results


def extract_bare_urls(text: str) -> list[str]:
    linked_urls = {locator for _, locator in extract_markdown_links(text)}
    urls = []
    for match in BARE_URL_RE.findall(text):
        if match not in linked_urls:
            urls.append(match)
    return urls


def guess_external_source_type(locator: str) -> str:
    parsed = urlparse(locator)
    host = parsed.netloc.lower()
    path = parsed.path.lower()

    if "arxiv.org" in host or "doi.org" in host:
        return "paper"
    if "github.com" in host or "gitlab.com" in host:
        return "repo"
    if any(token in host for token in ["paperswithcode.com", "huggingface.co"]):
        return "benchmark"
    if any(token in path for token in ["/dataset", "/datasets"]):
        return "dataset"
    return "official_doc" if host else "other"


def guess_local_source_type(path: Path) -> str:
    suffix = path.suffix.lower()
    lowered_name = path.name.lower()
    if suffix in {".md", ".txt"}:
        if looks_like_result_artifact(path):
            return "local_result"
        return "note"
    if suffix in {".json", ".yaml", ".yml", ".toml"}:
        if any(token in lowered_name for token in ["result", "metric", "benchmark", "ablation"]):
            return "local_result"
        return "local_code"
    if suffix in {".csv", ".tsv"}:
        return "local_result"
    return "local_code"


def guess_local_classification(path: Path, source_type: str, structured: dict[str, str]) -> str:
    verification = (
        structured.get("source:verification status")
        or structured.get("verification status")
        or structured.get("verification")
        or ""
    ).lower()
    if source_type == "local_result":
        return "project_evidence"
    if source_type == "note" and verification in {"verified", "verified-page-metadata", "reviewed-primary"}:
        return "verified_fact"
    return "unverified"


def looks_like_result_artifact(path: Path) -> bool:
    lowered_name = path.name.lower()
    if any(token in lowered_name for token in ["result", "ablation", "artifact"]) and path.suffix.lower() not in {".md", ".txt"}:
        return True
    if path.suffix.lower() not in {".md", ".txt"} and any(token in lowered_name for token in ["metric", "benchmark"]):
        return True
    if path.suffix.lower() not in {".md", ".txt"}:
        return False
    text = path.read_text(encoding="utf-8")
    markers = [
        "## artifact",
        "artifact type:",
        "provenance:",
        "run ids:",
        "baseline set:",
    ]
    lowered = text.lower()
    return any(marker in lowered for marker in markers)


def guess_title_from_url(locator: str) -> str:
    parsed = urlparse(locator)
    if parsed.netloc:
        tail = parsed.path.rstrip("/").split("/")[-1]
        if tail:
            return tail.replace("-", " ").replace("_", " ")
        return parsed.netloc
    return locator


def canonical_source_key(locator: str) -> str:
    if locator.startswith("http://") or locator.startswith("https://"):
        parsed = urlparse(locator)
        path = parsed.path.rstrip("/")
        return f"{parsed.netloc.lower()}{path}"
    return str(Path(locator).expanduser().resolve())


def source_priority(source: SourceItem) -> tuple[int, int, int]:
    local_bonus = 1 if not source.locator.startswith(("http://", "https://")) else 0
    quality = 2 if source.classification == "project_evidence" else 1 if source.statement and not source.statement.lower().startswith("todo:") else 0
    richness = sum(1 for item in [source.statement, source.relevance, source.limitations] if item and not item.lower().startswith("todo:"))
    return (local_bonus, quality, richness)


def build_local_statement(path: Path, title: str, source_type: str, structured: dict[str, str]) -> str:
    if source_type == "local_result":
        metric = structured.get("metric", "an internal metric")
        scope = structured.get("scope", "the current evaluation scope")
        baseline_set = structured.get("baseline set")
        baseline_suffix = f" against {baseline_set}" if baseline_set else ""
        metric_fact = f" Candidate metric fact: This artifact defines or reports {metric}."
        baseline_fact = (
            f" Candidate baseline fact: This artifact compares against {baseline_set}."
            if baseline_set
            else ""
        )
        return (
            f"Internal result artifact tracks {metric} for {scope}{baseline_suffix}."
            f"{metric_fact}{baseline_fact}"
        )

    reviewed_summary = structured.get("reviewed summary:reviewed summary") or structured.get("reviewed summary")
    if reviewed_summary:
        return reviewed_summary.rstrip(".") + "."

    key_facts = structured.get("key facts:fact") or structured.get("fact")
    if key_facts:
        parts = [item.strip() for item in key_facts.split(";") if item.strip()]
        benchmark_fact = next(
            (item for item in parts if item.lower().startswith("candidate benchmark/task fact:")),
            None,
        )
        evaluation_fact = next(
            (item for item in parts if item.lower().startswith("candidate evaluation fact:")),
            None,
        )
        metric_fact = next(
            (item for item in parts if item.lower().startswith("candidate metric fact:")),
            None,
        )
        baseline_fact = next(
            (item for item in parts if item.lower().startswith("candidate baseline fact:")),
            None,
        )
        selected = [item for item in [benchmark_fact, evaluation_fact, metric_fact, baseline_fact] if item]
        if selected:
            return " ".join(item.rstrip(".") + "." for item in selected[:3])
        return parts[0].rstrip(".") + "."

    task = structured.get("task")
    metrics = structured.get("metrics")
    if task and metrics:
        return f"{title} covers {task} and highlights {metrics}."
    if task:
        return f"{title} covers {task}."
    return f"TODO: review the exact claim or observation from {title}."


def build_local_relevance(path: Path, source_type: str, structured: dict[str, str]) -> str:
    if source_type == "local_result":
        benchmark = structured.get("benchmark", "the current evaluation setting")
        return f"This project artifact provides direct internal evidence for {benchmark}."

    relevance = structured.get("why it matters:relevance to our paper") or structured.get("relevance to our paper")
    comparable = structured.get("why it matters:comparable to us") or structured.get("comparable to us")
    if relevance and comparable:
        return f"{relevance} Comparable scope: {comparable}."
    if relevance:
        return relevance.rstrip(".") + "."
    return f"TODO: explain why {extract_local_title(path)} matters for this evidence pack."


def build_local_limitations(source_type: str, structured: dict[str, str]) -> str:
    caveat = structured.get("caveats:caveat") or structured.get("limits:limit") or structured.get("limit")
    if caveat:
        return caveat.rstrip(".") + "."
    if source_type == "local_result":
        return "TODO: state remaining comparability risks, missing baselines, or evaluation limits."
    return "TODO: state scope limits, comparability risks, or verification gaps."


def render_ledger(sources: list[SourceItem], id_prefix: str) -> str:
    lines = [
        "# Evidence Ledger Draft",
        "",
        "This draft was generated automatically. Review every item before using it in downstream research work.",
        "",
    ]

    for index, source in enumerate(sources, start=1):
        lines.extend(
            [
                f"- id: {id_prefix}{index:02d}",
                f"  statement: \"{escape_quotes(source.statement)}\"",
                f"  classification: {source.classification}",
                f"  source_type: {source.source_type}",
                f"  source_title: \"{escape_quotes(source.title)}\"",
                f"  source_locator: \"{escape_quotes(source.locator)}\"",
                "  date: \"unknown\"",
                f"  relevance: \"{escape_quotes(source.relevance)}\"",
                f"  limitations: \"{escape_quotes(source.limitations)}\"",
                "",
            ]
        )

    if not sources:
        lines.extend(
            [
                "No sources were extracted.",
                "",
                "Check that the input files contain markdown links, URLs, or useful local artifacts.",
                "",
            ]
        )

    return "\n".join(lines)


def escape_quotes(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


if __name__ == "__main__":
    raise SystemExit(main())
