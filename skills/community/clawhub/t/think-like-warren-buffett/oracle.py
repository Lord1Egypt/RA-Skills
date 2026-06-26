#!/usr/bin/env python3
"""
Buffett Oracle — Repo Helper

Usage:
  python3 oracle.py                 # 显示项目状态
  python3 oracle.py status          # 显示项目状态
  python3 oracle.py validate        # 校验 company_cards / README / backtest 一致性
  python3 oracle.py backtest        # 重新汇总并输出当前回测结果
  python3 oracle.py site            # 生成可静态部署的网站到 docs/
  python3 oracle.py serve-site      # 本地预览网页版本
  python3 oracle.py marketplace-bundle  # 生成 Claw Mart / marketplace 销售包
  python3 oracle.py cards           # 列出已缓存 company cards
  python3 oracle.py pending         # 列出待分析案例
  python3 oracle.py methodology     # 审计方法论质量与高胜率成因
  python3 oracle.py gate-review     # 审计 7 个 hard gates 在回测中的误伤与有效性
  python3 oracle.py show <query>    # 查看某张 company card
  python3 oracle.py brain           # 查看大脑内容
  python3 oracle.py corpus          # 浏览可用语料
  python3 oracle.py learn <file>    # 从语料文件提炼新知识（生成提示词）
  python3 oracle.py evolve          # 手动添加一条新原则
"""

from __future__ import annotations

import argparse
import datetime
import functools
import http.server
import json
import os
import re
import shutil
import socketserver
import sys
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent
BRAIN_FILE = BASE_DIR / "buffett_brain.md"
BACKTEST_FILE = BASE_DIR / "backtest_results.md"
README_FILE = BASE_DIR / "README.md"
ANALYSIS_INDEX_FILE = BASE_DIR / "analysis_index.json"
EXPANSION_FILE = BASE_DIR / "universe_expansion.md"
EXPANSION_INDEX_FILE = BASE_DIR / "universe_expansion_index.json"
GATE_REVIEW_FILE = BASE_DIR / "gate_review.md"
CARDS_DIR = BASE_DIR / "company_cards"
SITE_SRC_DIR = BASE_DIR / "site"
SITE_OUTPUT_DIR = BASE_DIR / "docs"
DIST_DIR = BASE_DIR / "dist"
MARKETPLACE_OUTPUT_DIR = DIST_DIR / "clawmart"
CORPUS_DIR = Path(os.environ.get("BUFFETT_CORPUS_DIR", Path.home() / "Documents/warren-buffet"))
SITE_TEMPLATE_SUFFIXES = {".html", ".txt", ".xml", ".svg", ".webmanifest"}
MARKETPLACE_PACKAGE_SLUG = "buffett-oracle"
MARKETPLACE_HOMEPAGE = "https://github.com/yixiao1032-publish/buffet-oracle"
MARKETPLACE_REPOSITORY = f"{MARKETPLACE_HOMEPAGE}.git"
MARKETPLACE_AUTHOR_NAME = "Buffett Oracle"
MARKETPLACE_PLUGIN_CATALOG_NAME = "buffett-oracle-catalog"
MARKETPLACE_PLUGIN_CATEGORY = "Finance / Research"
MARKETPLACE_PLUGIN_CAPABILITIES = ("Read", "Write")
MARKETPLACE_INCLUDED_PATHS = (
    "SKILL.md",
    "agents",
    "assets",
    "buffett-oracle.md",
    "CLAUDE.md",
    "README.md",
    "buffett_brain.md",
    "backtest_results.md",
    "coverage_scope.md",
    "methodology_audit.md",
    "gate_review.md",
    "analysis_index.json",
    "universe_expansion.md",
    "universe_expansion_index.json",
    "oracle.py",
    "company_cards",
)
MARKETPLACE_PREVIEW_ASSETS = ("docs/social-card.svg", "docs/favicon.svg")
MARKETPLACE_WORKS_WITH = ("Codex Plugins", "OpenClaw", "Raw Files", "Claude Projects", "Custom GPTs", "Cursor")

TOP_LEVEL_REQUIRED_KEYS = {
    "ticker",
    "company",
    "analysis_year",
    "data_source",
    "analyzed_date",
    "hard_gates",
    "control_groups",
    "conclusion",
    "buffett_action",
    "actual_result",
    "verdict",
    "key_insight",
}

HARD_GATE_KEYS = {
    "g1_roe_roic",
    "g2_fcf_to_ni",
    "g3_leverage",
    "g4_revenue_trend",
    "g5_gross_margin_trend",
    "g6_earnings_yield",
    "g7_moat",
}

ALLOWED_SPECIAL_CHANNELS = {
    None,
    "CRISIS_PREFERRED",
    "INFRA_EXEMPTION",
    "GROWTH_EXCEPTION",
}

ALLOWED_MANAGEMENT_VETO_STATUSES = {"clear", "watch", "fail"}

ALLOWED_BUY_FAILURES = {
    "CRISIS_PREFERRED": {"g1_roe_roic", "g2_fcf_to_ni", "g3_leverage", "g6_earnings_yield"},
    "INFRA_EXEMPTION": {"g6_earnings_yield"},
    "GROWTH_EXCEPTION": {"g1_roe_roic", "g2_fcf_to_ni"},
}

BACKTEST_CORRECT_SYMBOLS = {"✅", "⭐"}
BACKTEST_SCORED_SYMBOLS = {"✅", "⭐", "❌"}

GATE_METADATA = [
    {
        "key": "g1_roe_roic",
        "label": "Gate 1",
        "title": "Normalized ROE / ROIC",
        "rule": "3-year average must be at least 12%, excluding one-time items.",
    },
    {
        "key": "g2_fcf_to_ni",
        "label": "Gate 2",
        "title": "FCF / Net Income",
        "rule": "Cash conversion must be at least 0.8x.",
    },
    {
        "key": "g3_leverage",
        "label": "Gate 3",
        "title": "Leverage",
        "rule": "Net Debt / EBITDA must be at most 4x. Banks use Tier 1 capital instead.",
    },
    {
        "key": "g4_revenue_trend",
        "label": "Gate 4",
        "title": "Structural Revenue Trend",
        "rule": "Cyclical weakness is allowed; structural decline is not.",
    },
    {
        "key": "g5_gross_margin_trend",
        "label": "Gate 5",
        "title": "Gross Margin Trend",
        "rule": "Two or more consecutive years of decline fail the gate.",
    },
    {
        "key": "g6_earnings_yield",
        "label": "Gate 6",
        "title": "Earnings Yield",
        "rule": "Net Income / Enterprise Value must be at least 6%, unless a named exception applies.",
    },
    {
        "key": "g7_moat",
        "label": "Gate 7",
        "title": "Moat Test",
        "rule": "You must be able to explain why competitors cannot replicate the business in 10 years.",
    },
]


@dataclass
class ValidationResult:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


@dataclass
class CardRecord:
    path: Path
    payload: dict[str, Any]
    validation: ValidationResult

    @property
    def ticker(self) -> str:
        return str(self.payload.get("ticker", self.path.stem.split("_")[0]))

    @property
    def company(self) -> str:
        return str(self.payload.get("company", self.path.stem))

    @property
    def analysis_year(self) -> Any:
        return self.payload.get("analysis_year")

    @property
    def conclusion(self) -> str:
        return str(self.payload.get("conclusion", "UNKNOWN"))

    @property
    def special_channel(self) -> Any:
        return self.payload.get("special_channel")

    @property
    def failed_gates(self) -> list[str]:
        hard_gates = self.payload.get("hard_gates", {})
        if not isinstance(hard_gates, dict):
            return []
        failed = []
        for gate_key, gate_value in hard_gates.items():
            if isinstance(gate_value, dict) and gate_value.get("pass") is False:
                failed.append(gate_key)
        return sorted(failed)


def is_live_analysis_card(record: CardRecord) -> bool:
    scope = record.payload.get("analysis_scope")
    return record.path.name.startswith("LIVE_") or scope == "live"


@dataclass
class BacktestRow:
    index: int
    target: str
    decision_year: str
    framework_conclusion: str
    buffett_action: str
    actual_result: str
    verdict: str


@dataclass
class ReadmeProgress:
    completed: int
    total: int
    version: str
    accuracy: str


@dataclass
class BrainMetadata:
    version: str
    line_count: int
    patch_count: int


@dataclass
class AnalysisIndexRow:
    id: int
    target: str
    decision_year: int
    status: str
    cards: list[str]
    card_required: bool
    notes: str = ""


@dataclass
class AuditReport:
    brain: BrainMetadata
    cards: list[CardRecord]
    backtest_rows: list[BacktestRow]
    analysis_index_rows: list[AnalysisIndexRow]
    detailed_sections: set[int]
    pending_rows: list[BacktestRow]
    expansion_rows: list[BacktestRow]
    expansion_index_rows: list[AnalysisIndexRow]
    expansion_detailed_sections: set[int]
    readme_progress: ReadmeProgress | None
    errors: list[str]
    warnings: list[str]

    @property
    def total_cases(self) -> int:
        return len(self.backtest_rows)

    @property
    def completed_cases(self) -> int:
        return sum(1 for row in self.backtest_rows if row.verdict in BACKTEST_SCORED_SYMBOLS)

    @property
    def correct_cases(self) -> int:
        return sum(1 for row in self.backtest_rows if row.verdict in BACKTEST_CORRECT_SYMBOLS)

    @property
    def accuracy(self) -> str:
        scored = self.completed_cases
        if scored == 0:
            return "0/0"
        return f"{self.correct_cases}/{scored}"

    @property
    def expansion_total_cases(self) -> int:
        return len(self.expansion_rows)

    @property
    def expansion_completed_cases(self) -> int:
        return sum(1 for row in self.expansion_rows if row.verdict in BACKTEST_SCORED_SYMBOLS)

    @property
    def expansion_correct_cases(self) -> int:
        return sum(1 for row in self.expansion_rows if row.verdict in BACKTEST_CORRECT_SYMBOLS)

    @property
    def expansion_accuracy(self) -> str:
        scored = self.expansion_completed_cases
        if scored == 0:
            return "0/0"
        return f"{self.expansion_correct_cases}/{scored}"


@dataclass
class MethodologyReport:
    completed_rows: list[BacktestRow]
    ambiguous_rows: list[BacktestRow]
    exit_rows: list[BacktestRow]
    exception_rows: list[BacktestRow]
    core_binary_rows: list[BacktestRow]
    cards_with_control_group_issues: list[CardRecord]
    buy_cards_with_control_group_issues: list[CardRecord]
    cards_with_scope_drift: list[CardRecord]
    retrospective_consistency: str


@dataclass
class GateReviewEntry:
    key: str
    label: str
    title: str
    rule: str
    total_failures: int
    wrong_case_failures: int
    wrong_case_files: list[str]
    assessment: str
    note: str


@dataclass
class GateReviewReport:
    archived_case_count: int
    wrong_case_count: int
    wrong_case_files: list[str]
    entries: list[GateReviewEntry]


@dataclass
class MarketplaceBundle:
    output_dir: Path
    package_dir: Path
    skill_dir: Path
    preview_dir: Path
    plugin_catalog_dir: Path
    plugin_dir: Path
    plugin_manifest_path: Path
    plugin_catalog_path: Path
    manifest_path: Path
    listing_copy_path: Path
    publish_checklist_path: Path
    zip_path: Path | None
    skill_zip_path: Path | None
    plugin_zip_path: Path | None


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def load_brain() -> str:
    return load_text(BRAIN_FILE)


def parse_brain_metadata(text: str) -> BrainMetadata:
    versions = re.findall(r"\|\s*(v\d+\.\d+)\s*\|", text)
    version = versions[-1] if versions else "v1.0"
    return BrainMetadata(
        version=version,
        line_count=text.count("\n") + (1 if text else 0),
        patch_count=text.count("## 进化补丁"),
    )


def framework_version_to_semver(version: str) -> str:
    match = re.search(r"v?(\d+)\.(\d+)(?:\.(\d+))?", version.strip())
    if not match:
        return "1.0.0"
    major, minor, patch = match.groups()
    return f"{major}.{minor}.{patch or '0'}"


def parse_markdown_table_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def parse_backtest_rows(text: str) -> list[BacktestRow]:
    rows: list[BacktestRow] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = parse_markdown_table_row(stripped)
        if len(cells) != 7 or not cells[0].isdigit():
            continue
        rows.append(
            BacktestRow(
                index=int(cells[0]),
                target=cells[1],
                decision_year=cells[2],
                framework_conclusion=cells[3],
                buffett_action=cells[4],
                actual_result=cells[5],
                verdict=cells[6],
            )
        )
    return rows


def parse_detailed_sections(text: str) -> set[int]:
    return {int(match.group(1)) for match in re.finditer(r"^### #(\d+)\b", text, flags=re.MULTILINE)}


def parse_readme_progress(text: str) -> ReadmeProgress | None:
    for line in text.splitlines():
        cells = parse_markdown_table_row(line) if line.strip().startswith("|") else []
        if len(cells) != 3:
            continue
        match = re.fullmatch(r"(\d+)\s*/\s*(\d+)\s+(?:benchmark\s+)?cases", cells[0])
        if not match:
            continue
        return ReadmeProgress(
            completed=int(match.group(1)),
            total=int(match.group(2)),
            version=cells[1],
            accuracy=cells[2],
        )
    return None


def classify_framework_conclusion(label: str) -> str:
    normalized = label.strip()
    if "/" in normalized or "可投" in normalized or "谨慎" in normalized:
        return "AMBIGUOUS"
    if "卖" in normalized:
        return "SELL"
    if "买" in normalized:
        return "BUY"
    if "不投" in normalized or normalized.upper() == "PASS":
        return "PASS"
    return "UNKNOWN"


def load_analysis_index(index_path: Path) -> tuple[list[AnalysisIndexRow], ValidationResult]:
    result = ValidationResult()
    if not index_path.exists() or not index_path.is_file():
        result.errors.append(f"{index_path.name} is missing")
        return [], result

    try:
        payload = json.loads(index_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        result.errors.append(f"{index_path.name}: invalid JSON ({exc})")
        return [], result

    raw_rows = payload.get("rows")
    if not isinstance(raw_rows, list):
        result.errors.append(f"{index_path.name}: top-level 'rows' must be a list")
        return [], result

    rows: list[AnalysisIndexRow] = []
    for raw in raw_rows:
        if not isinstance(raw, dict):
            result.errors.append(f"{index_path.name}: each row must be an object")
            continue
        raw_cards = raw.get("cards", [])
        if not isinstance(raw_cards, list):
            result.errors.append(f"{index_path.name}: row #{raw.get('id', '?')} cards must be a list")
            continue
        try:
            row = AnalysisIndexRow(
                id=int(raw["id"]),
                target=str(raw["target"]),
                decision_year=int(raw["decision_year"]),
                status=str(raw["status"]),
                cards=[str(card_name) for card_name in raw_cards],
                card_required=bool(raw.get("card_required", True)),
                notes=str(raw.get("notes", "")),
            )
        except (KeyError, TypeError, ValueError) as exc:
            result.errors.append(f"{index_path.name}: invalid row payload ({exc})")
            continue

        if row.status not in {"completed", "pending"}:
            result.errors.append(f"{index_path.name}: row #{row.id} has invalid status {row.status!r}")
        rows.append(row)

    return rows, result


def validate_analysis_index(
    index_rows: list[AnalysisIndexRow],
    backtest_rows: list[BacktestRow],
    cards: list[CardRecord],
    *,
    index_label: str = "analysis_index.json",
) -> ValidationResult:
    result = ValidationResult()
    backtest_by_id = {row.index: row for row in backtest_rows}
    archived_cards = [card for card in cards if not is_live_analysis_card(card)]
    card_names = {card.path.name for card in archived_cards}

    index_ids = [row.id for row in index_rows]
    duplicate_ids = sorted({row_id for row_id in index_ids if index_ids.count(row_id) > 1})
    if duplicate_ids:
        result.errors.append(
            f"{index_label} has duplicate row ids: " + ", ".join(f"#{row_id}" for row_id in duplicate_ids)
        )

    missing_ids = sorted(set(backtest_by_id) - set(index_ids))
    extra_ids = sorted(set(index_ids) - set(backtest_by_id))
    if missing_ids:
        result.errors.append(
            f"{index_label} is missing backtest rows: " + ", ".join(f"#{row_id}" for row_id in missing_ids)
        )
    if extra_ids:
        result.errors.append(
            f"{index_label} references unknown backtest rows: " + ", ".join(f"#{row_id}" for row_id in extra_ids)
        )

    referenced_cards: list[str] = []
    for index_row in index_rows:
        backtest_row = backtest_by_id.get(index_row.id)
        if backtest_row is None:
            continue

        if index_row.target != backtest_row.target:
            result.errors.append(
                f"{index_label} row #{index_row.id} target mismatch: {index_row.target!r} != {backtest_row.target!r}"
            )
        if str(index_row.decision_year) != backtest_row.decision_year:
            result.errors.append(
                f"{index_label} row #{index_row.id} year mismatch: {index_row.decision_year} != {backtest_row.decision_year}"
            )

        expected_status = "completed" if backtest_row.verdict in BACKTEST_SCORED_SYMBOLS else "pending"
        if index_row.status != expected_status:
            result.errors.append(
                f"{index_label} row #{index_row.id} status mismatch: {index_row.status} != {expected_status}"
            )

        for card_name in index_row.cards:
            referenced_cards.append(card_name)
            if card_name not in card_names:
                result.errors.append(
                    f"{index_label} row #{index_row.id} references missing card {card_name}"
                )

        if index_row.status == "completed" and index_row.card_required and not index_row.cards:
            result.errors.append(
                f"{index_label} row #{index_row.id} is completed but has no linked card"
            )
        if index_row.status == "pending" and index_row.cards:
            result.warnings.append(
                f"{index_label} row #{index_row.id} is still pending but already has linked cards"
            )

    duplicate_cards = sorted({card_name for card_name in referenced_cards if referenced_cards.count(card_name) > 1})
    if duplicate_cards:
        result.warnings.append(
            f"{index_label} reuses card links across rows: " + ", ".join(duplicate_cards)
        )

    return result


def validate_card_index_coverage(
    cards: list[CardRecord],
    index_groups: list[list[AnalysisIndexRow]],
) -> ValidationResult:
    result = ValidationResult()
    archived_cards = [card for card in cards if not is_live_analysis_card(card)]
    card_names = {card.path.name for card in archived_cards}
    referenced_cards = [card_name for index_rows in index_groups for row in index_rows for card_name in row.cards]

    duplicate_cards = sorted({card_name for card_name in referenced_cards if referenced_cards.count(card_name) > 1})
    if duplicate_cards:
        result.warnings.append(
            "analysis indexes reuse card links across tracks: " + ", ".join(duplicate_cards)
        )

    unreferenced_cards = sorted(card_names - set(referenced_cards))
    if unreferenced_cards:
        result.errors.append(
            "company_cards contains files not linked from any analysis index: "
            + ", ".join(unreferenced_cards)
        )

    return result


def card_matches_query(record: CardRecord, query: str) -> bool:
    query_upper = query.upper()
    haystacks = {
        record.path.stem.upper(),
        record.ticker.upper(),
        record.company.upper(),
    }
    return any(query_upper in haystack for haystack in haystacks)


def load_company_cards(cards_dir: Path = CARDS_DIR) -> list[CardRecord]:
    records: list[CardRecord] = []
    if not cards_dir.exists():
        return records

    for path in sorted(cards_dir.glob("*.json")):
        if path.name == "_schema.json":
            continue
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            records.append(
                CardRecord(
                    path=path,
                    payload={},
                    validation=ValidationResult(errors=[f"{path.name}: invalid JSON ({exc})"]),
                )
            )
            continue
        records.append(CardRecord(path=path, payload=payload, validation=validate_card_payload(path.name, payload)))
    return records


def validate_card_payload(filename: str, payload: dict[str, Any]) -> ValidationResult:
    result = ValidationResult()

    missing_keys = sorted(TOP_LEVEL_REQUIRED_KEYS - payload.keys())
    if missing_keys:
        result.errors.append(f"{filename}: missing top-level keys: {', '.join(missing_keys)}")

    hard_gates = payload.get("hard_gates")
    if not isinstance(hard_gates, dict):
        result.errors.append(f"{filename}: hard_gates must be an object")
        return result

    missing_gates = sorted(HARD_GATE_KEYS - hard_gates.keys())
    if missing_gates:
        result.errors.append(f"{filename}: missing hard gates: {', '.join(missing_gates)}")

    conclusion = payload.get("conclusion")
    if conclusion not in {"BUY", "PASS"}:
        result.errors.append(f"{filename}: conclusion must be BUY or PASS")

    special_channel = payload.get("special_channel")
    if special_channel not in ALLOWED_SPECIAL_CHANNELS:
        result.errors.append(f"{filename}: invalid special_channel {special_channel!r}")

    control_groups = payload.get("control_groups")
    if not isinstance(control_groups, list) or len(control_groups) < 2:
        result.errors.append(f"{filename}: control_groups must contain at least 2 entries")

    review_notes = payload.get("review_notes", {})
    if review_notes is None:
        review_notes = {}
    if not isinstance(review_notes, dict):
        result.errors.append(f"{filename}: review_notes must be an object when present")
        review_notes = {}

    g6 = hard_gates.get("g6_earnings_yield", {})
    if isinstance(g6, dict):
        exemption = g6.get("exemption")
        if exemption is not None and exemption != special_channel:
            result.errors.append(
                f"{filename}: g6_earnings_yield.exemption ({exemption}) must match special_channel ({special_channel})"
            )

    failed_gates = [
        gate_key
        for gate_key, gate_value in hard_gates.items()
        if isinstance(gate_value, dict) and gate_value.get("pass") is False
    ]

    if conclusion == "PASS" and not failed_gates:
        result.warnings.append(f"{filename}: PASS card has no failed hard gate; verify quick rejection rationale")

    if conclusion == "BUY" and failed_gates:
        if special_channel is None:
            result.errors.append(
                f"{filename}: BUY card has failed gates without a named exemption ({', '.join(sorted(failed_gates))})"
            )
        else:
            allowed_failures = ALLOWED_BUY_FAILURES.get(special_channel, set())
            unexpected = sorted(set(failed_gates) - allowed_failures)
            if unexpected:
                result.errors.append(
                    f"{filename}: {special_channel} does not allow failed gates: {', '.join(unexpected)}"
                )

    if special_channel == "GROWTH_EXCEPTION":
        g6_pass = isinstance(g6, dict) and g6.get("pass") is True
        if not g6_pass:
            result.errors.append(f"{filename}: GROWTH_EXCEPTION requires g6_earnings_yield.pass = true")

    if special_channel == "INFRA_EXEMPTION":
        moat = hard_gates.get("g7_moat", {})
        moat_type = moat.get("moat_type") if isinstance(moat, dict) else None
        if moat_type not in {"monopoly", "cost_advantage"}:
            result.warnings.append(
                f"{filename}: INFRA_EXEMPTION is usually paired with monopoly/cost_advantage moat"
            )

    g2 = hard_gates.get("g2_fcf_to_ni", {})
    g7 = hard_gates.get("g7_moat", {})
    moat_pass = isinstance(g7, dict) and g7.get("pass") is True
    requires_owner_earnings_note = isinstance(g2, dict) and g2.get("pass") is False and moat_pass
    requires_quality_multiple_note = isinstance(g6, dict) and g6.get("pass") is False and moat_pass

    owner_note = review_notes.get("owner_earnings_note")
    quality_note = review_notes.get("quality_multiple_note")
    management_veto = review_notes.get("management_veto")

    if requires_owner_earnings_note:
        if not isinstance(owner_note, dict):
            result.errors.append(f"{filename}: g2 fail with passing moat requires review_notes.owner_earnings_note")
        else:
            missing_owner_fields = [
                field_name
                for field_name in ("summary", "maintenance_vs_growth_view", "decision_impact")
                if not str(owner_note.get(field_name, "")).strip()
            ]
            if missing_owner_fields:
                result.errors.append(
                    f"{filename}: owner_earnings_note is missing fields: {', '.join(missing_owner_fields)}"
                )

    if requires_quality_multiple_note:
        if not isinstance(quality_note, dict):
            result.errors.append(f"{filename}: g6 fail with passing moat requires review_notes.quality_multiple_note")
        else:
            missing_quality_fields = [
                field_name
                for field_name in ("summary", "reason_for_low_yield", "decision_impact")
                if not str(quality_note.get(field_name, "")).strip()
            ]
            if missing_quality_fields:
                result.errors.append(
                    f"{filename}: quality_multiple_note is missing fields: {', '.join(missing_quality_fields)}"
                )

    if any((requires_owner_earnings_note, requires_quality_multiple_note, bool(review_notes))):
        if not isinstance(management_veto, dict):
            result.errors.append(f"{filename}: review_notes.management_veto is required when review_notes are used")
        else:
            status = management_veto.get("status")
            if status not in ALLOWED_MANAGEMENT_VETO_STATUSES:
                result.errors.append(
                    f"{filename}: management_veto.status must be one of {sorted(ALLOWED_MANAGEMENT_VETO_STATUSES)}"
                )
            if not str(management_veto.get("summary", "")).strip():
                result.errors.append(f"{filename}: management_veto.summary must be non-empty")
            if status == "fail" and conclusion == "BUY":
                result.errors.append(f"{filename}: management_veto=fail cannot coexist with conclusion=BUY")

    analyzed_date = payload.get("analyzed_date")
    if analyzed_date:
        try:
            datetime.date.fromisoformat(str(analyzed_date))
        except ValueError:
            result.errors.append(f"{filename}: analyzed_date must be ISO format YYYY-MM-DD")

    return result


def build_audit_report(base_dir: Path = BASE_DIR) -> AuditReport:
    brain_text = load_text(base_dir / "buffett_brain.md")
    backtest_text = load_text(base_dir / "backtest_results.md")
    expansion_text = load_text(base_dir / "universe_expansion.md")
    readme_text = load_text(base_dir / "README.md")

    brain = parse_brain_metadata(brain_text)
    cards = load_company_cards(base_dir / "company_cards")
    analysis_index_rows, index_load_result = load_analysis_index(base_dir / "analysis_index.json")
    backtest_rows = parse_backtest_rows(backtest_text)
    detailed_sections = parse_detailed_sections(backtest_text)
    pending_rows = [row for row in backtest_rows if row.verdict == "—"]
    expansion_rows: list[BacktestRow] = []
    expansion_detailed_sections: set[int] = set()
    expansion_index_rows: list[AnalysisIndexRow] = []
    expansion_index_load_result = ValidationResult()
    expansion_file = base_dir / "universe_expansion.md"
    expansion_index_file = base_dir / "universe_expansion_index.json"
    if expansion_file.exists() or expansion_index_file.exists():
        expansion_rows = parse_backtest_rows(expansion_text)
        expansion_detailed_sections = parse_detailed_sections(expansion_text)
        expansion_index_rows, expansion_index_load_result = load_analysis_index(expansion_index_file)
    readme_progress = parse_readme_progress(readme_text)

    errors: list[str] = list(index_load_result.errors)
    warnings: list[str] = list(index_load_result.warnings)
    errors.extend(expansion_index_load_result.errors)
    warnings.extend(expansion_index_load_result.warnings)

    for card in cards:
        errors.extend(card.validation.errors)
        warnings.extend(card.validation.warnings)

    index_validation = validate_analysis_index(
        analysis_index_rows,
        backtest_rows,
        cards,
        index_label="analysis_index.json",
    )
    errors.extend(index_validation.errors)
    warnings.extend(index_validation.warnings)
    if expansion_file.exists() or expansion_index_file.exists():
        expansion_validation = validate_analysis_index(
            expansion_index_rows,
            expansion_rows,
            cards,
            index_label="universe_expansion_index.json",
        )
        errors.extend(expansion_validation.errors)
        warnings.extend(expansion_validation.warnings)

    coverage_validation = validate_card_index_coverage(cards, [analysis_index_rows, expansion_index_rows])
    errors.extend(coverage_validation.errors)
    warnings.extend(coverage_validation.warnings)

    completed_indices = {row.index for row in backtest_rows if row.verdict in BACKTEST_SCORED_SYMBOLS}
    missing_sections = sorted(completed_indices - detailed_sections)
    extra_sections = sorted(detailed_sections - completed_indices)
    if missing_sections:
        warnings.append(
            "backtest_results.md is missing detailed sections for completed cases: "
            + ", ".join(f"#{index}" for index in missing_sections)
        )
    if extra_sections:
        warnings.append(
            "backtest_results.md has detailed sections without scored summary rows: "
            + ", ".join(f"#{index}" for index in extra_sections)
        )

    completed_expansion_indices = {row.index for row in expansion_rows if row.verdict in BACKTEST_SCORED_SYMBOLS}
    missing_expansion_sections = sorted(completed_expansion_indices - expansion_detailed_sections)
    extra_expansion_sections = sorted(expansion_detailed_sections - completed_expansion_indices)
    if missing_expansion_sections:
        warnings.append(
            "universe_expansion.md is missing detailed sections for completed cases: "
            + ", ".join(f"#{index}" for index in missing_expansion_sections)
        )
    if extra_expansion_sections:
        warnings.append(
            "universe_expansion.md has detailed sections without scored summary rows: "
            + ", ".join(f"#{index}" for index in extra_expansion_sections)
        )

    report = AuditReport(
        brain=brain,
        cards=cards,
        backtest_rows=backtest_rows,
        analysis_index_rows=analysis_index_rows,
        detailed_sections=detailed_sections,
        pending_rows=pending_rows,
        expansion_rows=expansion_rows,
        expansion_index_rows=expansion_index_rows,
        expansion_detailed_sections=expansion_detailed_sections,
        readme_progress=readme_progress,
        errors=errors,
        warnings=warnings,
    )

    if readme_progress is None:
        report.errors.append("README.md is missing the Current Progress summary row")
    else:
        if readme_progress.completed != report.completed_cases:
            report.warnings.append(
                f"README.md completed cases says {readme_progress.completed}, but backtest_results.md shows {report.completed_cases}"
            )
        if readme_progress.total != report.total_cases:
            report.warnings.append(
                f"README.md total cases says {readme_progress.total}, but backtest_results.md shows {report.total_cases}"
            )
        if readme_progress.version != report.brain.version:
            report.warnings.append(
                f"README.md framework version says {readme_progress.version}, but buffett_brain.md is {report.brain.version}"
            )
        if not readme_progress.accuracy.startswith(report.accuracy):
            report.warnings.append(
                f"README.md accuracy says {readme_progress.accuracy}, but backtest_results.md computes to {report.accuracy}"
            )

    return report


def card_has_control_group_issue(card: CardRecord) -> bool:
    control_groups = card.payload.get("control_groups", [])
    if not isinstance(control_groups, list):
        return False
    for control_group in control_groups:
        conclusion = str(control_group.get("conclusion", ""))
        failed_gates = control_group.get("gates_failed", [])
        if "BUY" in conclusion or failed_gates == []:
            return True
    return False


def build_methodology_report(base_dir: Path = BASE_DIR) -> MethodologyReport:
    audit_report = build_audit_report(base_dir)
    index_by_id = {row.id: row for row in audit_report.analysis_index_rows}
    benchmark_card_names = {card_name for row in audit_report.analysis_index_rows for card_name in row.cards}
    benchmark_cards = [card for card in audit_report.cards if card.path.name in benchmark_card_names]
    cards_by_name = {card.path.name: card for card in benchmark_cards}

    completed_rows = [row for row in audit_report.backtest_rows if row.verdict in BACKTEST_SCORED_SYMBOLS]
    ambiguous_rows: list[BacktestRow] = []
    exit_rows: list[BacktestRow] = []
    exception_rows: list[BacktestRow] = []
    core_binary_rows: list[BacktestRow] = []

    for row in completed_rows:
        decision_class = classify_framework_conclusion(row.framework_conclusion)
        index_row = index_by_id.get(row.index)
        linked_cards = [cards_by_name[card_name] for card_name in index_row.cards if card_name in cards_by_name] if index_row else []
        is_exception = any(card.special_channel for card in linked_cards) or any(
            token in row.framework_conclusion for token in ("优先股", "成长例外")
        )

        if decision_class == "AMBIGUOUS":
            ambiguous_rows.append(row)
        if decision_class == "SELL":
            exit_rows.append(row)
        if is_exception:
            exception_rows.append(row)
        if decision_class in {"BUY", "PASS"} and decision_class != "AMBIGUOUS" and not is_exception:
            core_binary_rows.append(row)

    cards_with_control_group_issues = [card for card in benchmark_cards if card_has_control_group_issue(card)]
    buy_cards_with_control_group_issues = [
        card for card in cards_with_control_group_issues if card.conclusion == "BUY"
    ]
    cards_with_scope_drift = [
        card
        for card in audit_report.cards
        if "not classic Buffett" in str(card.payload.get("key_insight", ""))
        or "Munger" in str(card.payload.get("key_insight", ""))
    ]

    return MethodologyReport(
        completed_rows=completed_rows,
        ambiguous_rows=ambiguous_rows,
        exit_rows=exit_rows,
        exception_rows=exception_rows,
        core_binary_rows=core_binary_rows,
        cards_with_control_group_issues=cards_with_control_group_issues,
        buy_cards_with_control_group_issues=buy_cards_with_control_group_issues,
        cards_with_scope_drift=cards_with_scope_drift,
        retrospective_consistency=audit_report.accuracy,
    )


def build_gate_review_report(base_dir: Path = BASE_DIR) -> GateReviewReport:
    audit_report = build_audit_report(base_dir)
    archived_card_names = {
        card_name
        for row in [*audit_report.analysis_index_rows, *audit_report.expansion_index_rows]
        for card_name in row.cards
    }
    archived_cards = [card for card in audit_report.cards if card.path.name in archived_card_names]
    wrong_cards = [card for card in archived_cards if card.payload.get("verdict") == "❌ framework_wrong"]

    gate_notes = {
        "g1_roe_roic": "So far there is no evidence that the 12% normalized return hurdle is the source of false negatives. Keep it strict.",
        "g2_fcf_to_ni": "Raw FCF / NI is catching real capital intensity, but it also punishes reinvestment-heavy compounders. Future memos should separate maintenance capex from expansion capex before treating this fail as decisive.",
        "g3_leverage": "Leverage has not yet produced false negatives in the archived set. Keep the balance-sheet discipline hard.",
        "g4_revenue_trend": "Structural-decline screening is still behaving sensibly. No archived false negatives are driven by this gate yet.",
        "g5_gross_margin_trend": "This gate is low-signal but not obviously broken. Keep it as a deterioration check, not as a primary stock picker.",
        "g6_earnings_yield": "A flat 6% earnings-yield floor is missing some elite asset-light or brand-heavy compounders. Future memos should add a quality-multiple note before treating this fail as decisive.",
        "g7_moat": "Moat remains the strongest qualitative filter in the current archive. It rejects weak businesses and has not yet shown up as a source of false negatives.",
    }

    entries: list[GateReviewEntry] = []
    for gate in GATE_METADATA:
        wrong_case_files = [card.path.name for card in wrong_cards if gate["key"] in card.failed_gates]
        total_failures = sum(1 for card in archived_cards if gate["key"] in card.failed_gates)
        wrong_case_failures = len(wrong_case_files)

        if wrong_case_failures == 0 and total_failures == 0:
            assessment = "low-signal"
        elif wrong_case_failures == 0:
            assessment = "holding-up"
        elif gate["key"] in {"g2_fcf_to_ni", "g6_earnings_yield"}:
            assessment = "under-review"
        else:
            assessment = "review"

        entries.append(
            GateReviewEntry(
                key=gate["key"],
                label=gate["label"],
                title=gate["title"],
                rule=gate["rule"],
                total_failures=total_failures,
                wrong_case_failures=wrong_case_failures,
                wrong_case_files=wrong_case_files,
                assessment=assessment,
                note=gate_notes[gate["key"]],
            )
        )

    return GateReviewReport(
        archived_case_count=len(archived_cards),
        wrong_case_count=len(wrong_cards),
        wrong_case_files=[card.path.name for card in wrong_cards],
        entries=entries,
    )


def serialize_card(record: CardRecord) -> dict[str, Any]:
    hard_gates = record.payload.get("hard_gates", {})
    gate_summary = []
    if isinstance(hard_gates, dict):
        for gate in GATE_METADATA:
            gate_payload = hard_gates.get(gate["key"], {})
            if isinstance(gate_payload, dict):
                gate_summary.append(
                    {
                        "key": gate["key"],
                        "label": gate["label"],
                        "title": gate["title"],
                        "pass": gate_payload.get("pass"),
                        "details": gate_payload,
                    }
                )

    return {
        "file": record.path.name,
        "ticker": record.ticker,
        "company": record.company,
        "analysis_year": record.analysis_year,
        "conclusion": record.conclusion,
        "special_channel": record.special_channel,
        "failed_gates": record.failed_gates,
        "validation": {
            "errors": record.validation.errors,
            "warnings": record.validation.warnings,
        },
        "payload": record.payload,
        "gate_summary": gate_summary,
    }


def serialize_backtest_row(row: BacktestRow) -> dict[str, Any]:
    return {
        "index": row.index,
        "target": row.target,
        "decision_year": row.decision_year,
        "framework_conclusion": row.framework_conclusion,
        "framework_class": classify_framework_conclusion(row.framework_conclusion),
        "buffett_action": row.buffett_action,
        "actual_result": row.actual_result,
        "verdict": row.verdict,
    }


def build_site_payload(base_dir: Path = BASE_DIR) -> dict[str, Any]:
    audit_report = build_audit_report(base_dir)
    methodology_report = build_methodology_report(base_dir)
    cards_by_name = {card.path.name: card for card in audit_report.cards}

    linked_rows = []
    for index_row in audit_report.analysis_index_rows:
        linked_cards = [serialize_card(cards_by_name[name]) for name in index_row.cards if name in cards_by_name]
        linked_rows.append(
            {
                "id": index_row.id,
                "track": "benchmark",
                "site_key": f"benchmark-{index_row.id}",
                "target": index_row.target,
                "decision_year": index_row.decision_year,
                "status": index_row.status,
                "card_required": index_row.card_required,
                "notes": index_row.notes,
                "cards": linked_cards,
                "backtest": serialize_backtest_row(
                    next(row for row in audit_report.backtest_rows if row.index == index_row.id)
                ),
            }
        )

    expansion_linked_rows = []
    for index_row in audit_report.expansion_index_rows:
        linked_cards = [serialize_card(cards_by_name[name]) for name in index_row.cards if name in cards_by_name]
        expansion_linked_rows.append(
            {
                "id": index_row.id,
                "track": "expansion",
                "site_key": f"expansion-{index_row.id}",
                "target": index_row.target,
                "decision_year": index_row.decision_year,
                "status": index_row.status,
                "card_required": index_row.card_required,
                "notes": index_row.notes,
                "cards": linked_cards,
                "backtest": serialize_backtest_row(
                    next(row for row in audit_report.expansion_rows if row.index == index_row.id)
                ),
            }
        )

    return {
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "project": {
            "name": "Buffett Oracle",
            "scope_label": "Curated benchmark set",
            "scope_note": "The 29 indexed rows are a selected benchmark set, not the full Buffett/Berkshire investment universe.",
            "framework_version": audit_report.brain.version,
            "framework_size": audit_report.brain.line_count,
            "completed_cases": audit_report.completed_cases,
            "total_cases": audit_report.total_cases,
            "expansion_completed_cases": audit_report.expansion_completed_cases,
            "expansion_total_cases": audit_report.expansion_total_cases,
            "retrospective_consistency": audit_report.accuracy,
            "expansion_consistency": audit_report.expansion_accuracy,
            "cached_cards": len(audit_report.cards),
        },
        "rules": {
            "point_in_time": "Use only information publicly available on or before the decision date.",
            "named_exceptions": sorted(channel for channel in ALLOWED_SPECIAL_CHANNELS if channel),
            "gates": GATE_METADATA,
        },
        "methodology": {
            "retrospective_consistency": methodology_report.retrospective_consistency,
            "ambiguous_case_ids": [row.index for row in methodology_report.ambiguous_rows],
            "exception_case_ids": [row.index for row in methodology_report.exception_rows],
            "exit_case_ids": [row.index for row in methodology_report.exit_rows],
            "core_case_ids": [row.index for row in methodology_report.core_binary_rows],
            "buy_control_issue_files": [card.path.name for card in methodology_report.buy_cards_with_control_group_issues],
            "scope_drift_files": [card.path.name for card in methodology_report.cards_with_scope_drift],
        },
        "documents": {
            "brain_markdown": load_text(base_dir / "buffett_brain.md"),
            "methodology_markdown": load_text(base_dir / "methodology_audit.md"),
            "readme_markdown": load_text(base_dir / "README.md"),
            "expansion_markdown": load_text(base_dir / "universe_expansion.md"),
        },
        "rows": linked_rows,
        "expansion_rows": expansion_linked_rows,
        "cards": [serialize_card(card) for card in audit_report.cards],
    }


def normalize_site_url(site_url: str | None) -> str:
    if not site_url:
        return ""
    normalized = site_url.strip()
    if not normalized:
        return ""
    return normalized.rstrip("/")


def render_site_template(template: str, context: dict[str, str]) -> str:
    rendered = template
    for key, value in context.items():
        rendered = rendered.replace(f"{{{{{key}}}}}", value)
    return rendered


def build_site_template_context(site_url: str) -> dict[str, str]:
    canonical_url = f"{site_url}/" if site_url else "./"
    og_image_url = f"{site_url}/social-card.svg" if site_url else "./social-card.svg"

    return {
        "SITE_URL": site_url,
        "CANONICAL_URL": canonical_url,
        "OG_IMAGE_URL": og_image_url,
        "SITE_NAME": "Buffett Oracle",
        "SITE_DESCRIPTION": (
            "A public Buffett-style decision engine: framework, backtests, methodology audit, "
            "and a live 7-gate decision lab."
        ),
        "THEME_COLOR": "#f6f1e7",
        "GENERATED_DATE": datetime.date.today().isoformat(),
    }


def build_static_site(
    output_dir: Path = SITE_OUTPUT_DIR,
    base_dir: Path = BASE_DIR,
    site_url: str | None = None,
) -> Path:
    if not SITE_SRC_DIR.exists():
        raise FileNotFoundError(f"Missing site source directory: {SITE_SRC_DIR}")

    assets_dir = output_dir / "assets"
    normalized_site_url = normalize_site_url(site_url)
    template_context = build_site_template_context(normalized_site_url)
    output_dir.mkdir(parents=True, exist_ok=True)
    assets_dir.mkdir(parents=True, exist_ok=True)

    for source_path in SITE_SRC_DIR.rglob("*"):
        relative_path = source_path.relative_to(SITE_SRC_DIR)
        target_path = output_dir / relative_path

        if source_path.is_dir():
            target_path.mkdir(parents=True, exist_ok=True)
            continue

        target_path.parent.mkdir(parents=True, exist_ok=True)
        if source_path.suffix in SITE_TEMPLATE_SUFFIXES:
            rendered = render_site_template(source_path.read_text(encoding="utf-8"), template_context)
            target_path.write_text(rendered, encoding="utf-8")
        else:
            shutil.copy2(source_path, target_path)

    payload = build_site_payload(base_dir)
    (assets_dir / "site-data.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    (output_dir / ".nojekyll").write_text("", encoding="utf-8")
    return output_dir


def copy_path(source_path: Path, target_path: Path) -> None:
    if source_path.is_dir():
        shutil.copytree(source_path, target_path, dirs_exist_ok=True)
        return

    target_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_path, target_path)


def copy_marketplace_payload(target_dir: Path, base_dir: Path) -> None:
    for relative_path in MARKETPLACE_INCLUDED_PATHS:
        source_path = base_dir / relative_path
        if not source_path.exists():
            continue
        copy_path(source_path, target_dir / relative_path)


def build_zip_archive(source_dir: Path, archive_base: Path, zip_path: Path) -> Path:
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(source_dir.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(archive_base))
    return zip_path


def build_marketplace_manifest(
    audit_report: AuditReport,
    methodology_report: MethodologyReport,
) -> dict[str, Any]:
    return {
        "product_name": "Buffett Oracle",
        "slug": MARKETPLACE_PACKAGE_SLUG,
        "type": "skill",
        "suggested_category": "Finance / Research",
        "version": audit_report.brain.version,
        "generated_date": datetime.date.today().isoformat(),
        "works_with": list(MARKETPLACE_WORKS_WITH),
        "delivery_formats": ["raw_files", "standalone_skill", "codex_plugin"],
        "scope_note": (
            "The benchmark archive covers a curated 29-case set, not Buffett or Berkshire's full investment history."
        ),
        "stats": {
            "benchmark_cases_completed": audit_report.completed_cases,
            "benchmark_cases_total": audit_report.total_cases,
            "benchmark_consistency": audit_report.accuracy,
            "expansion_cases_completed": audit_report.expansion_completed_cases,
            "expansion_cases_total": audit_report.expansion_total_cases,
            "cached_company_cards": len(audit_report.cards),
            "buy_cards": sum(1 for card in audit_report.cards if card.conclusion == "BUY"),
            "pass_cards": sum(1 for card in audit_report.cards if card.conclusion == "PASS"),
            "ambiguous_cases": len(methodology_report.ambiguous_rows),
            "exception_cases": len(methodology_report.exception_rows),
            "buy_control_misses": len(methodology_report.buy_cards_with_control_group_issues),
        },
        "bundle_contents": list(MARKETPLACE_INCLUDED_PATHS),
    }


def build_plugin_manifest(manifest: dict[str, Any]) -> dict[str, Any]:
    stats = manifest["stats"]
    return {
        "name": MARKETPLACE_PACKAGE_SLUG,
        "version": framework_version_to_semver(str(manifest["version"])),
        "description": "Buffett-style point-in-time investment analysis with BUY/PASS verdicts and cached company cards.",
        "author": {
            "name": MARKETPLACE_AUTHOR_NAME,
            "url": MARKETPLACE_HOMEPAGE,
        },
        "homepage": MARKETPLACE_HOMEPAGE,
        "repository": MARKETPLACE_REPOSITORY,
        "license": "MIT",
        "keywords": ["buffett", "investing", "valuation", "research", "finance"],
        "skills": "./skills/",
        "interface": {
            "displayName": "Buffett Oracle",
            "shortDescription": "Point-in-time Buffett investment skill",
            "longDescription": (
                "Buffett Oracle packages a strict Buffett + Graham research workflow with "
                f"{stats['benchmark_cases_completed']}/{stats['benchmark_cases_total']} benchmark cases, "
                f"{stats['expansion_cases_completed']}/{stats['expansion_cases_total']} expansion cases, and "
                f"{stats['cached_company_cards']} cached company cards."
            ),
            "developerName": MARKETPLACE_AUTHOR_NAME,
            "category": MARKETPLACE_PLUGIN_CATEGORY,
            "capabilities": list(MARKETPLACE_PLUGIN_CAPABILITIES),
            "websiteURL": MARKETPLACE_HOMEPAGE,
            "privacyPolicyURL": MARKETPLACE_HOMEPAGE,
            "termsOfServiceURL": MARKETPLACE_HOMEPAGE,
            "defaultPrompt": [
                "Analyze Apple 2016 with Buffett Oracle.",
                "Run Buffett Oracle on Tencent 2023.",
                "Explain whether Mastercard 2020 is BUY or PASS.",
            ],
            "brandColor": "#8B5E3C",
            "composerIcon": "./assets/icon.svg",
            "logo": "./assets/logo.svg",
        },
    }


def build_plugin_marketplace_catalog() -> dict[str, Any]:
    return {
        "name": MARKETPLACE_PLUGIN_CATALOG_NAME,
        "interface": {
            "displayName": "Buffett Oracle Catalog",
        },
        "plugins": [
            {
                "name": MARKETPLACE_PACKAGE_SLUG,
                "source": {
                    "source": "local",
                    "path": f"./plugins/{MARKETPLACE_PACKAGE_SLUG}",
                },
                "policy": {
                    "installation": "AVAILABLE",
                    "authentication": "ON_INSTALL",
                },
                "category": MARKETPLACE_PLUGIN_CATEGORY,
            }
        ],
    }


def build_marketplace_start_here(manifest: dict[str, Any]) -> str:
    stats = manifest["stats"]
    return f"""# Buffett Oracle — Start Here

Buffett Oracle is a point-in-time investing framework and research archive. It is not personalized investment advice.

## What you received

- `SKILL.md`: skill/package entry point for OpenClaw and other instruction-friendly tools
- `agents/openai.yaml`: optional UI metadata so the package behaves like a polished skill instead of plain raw files
- `buffett-oracle.md`: portable persona/system prompt for Claude Projects and Custom GPTs
- `buffett_brain.md`: the full Buffett + Graham framework, including the 7 hard gates
- `backtest_results.md`, `coverage_scope.md`, `methodology_audit.md`, `gate_review.md`: evidence, scope boundaries, and caveats
- `company_cards/`: {stats['cached_company_cards']} cached cards so repeated analyses do not require re-fetching source filings
- `oracle.py`: helper CLI for validation, listing cards, and static-site generation
- Seller-kit siblings: the build output also includes a standalone skill zip and a Codex plugin catalog zip

## Quick install

### Standalone skill / raw files

1. Use `buffett-oracle.md` as the base system prompt.
2. Keep `SKILL.md`, `agents/openai.yaml`, and the supporting research files in the same folder.
3. Ask for a company analysis with a year, for example: `Apple 2016` or `Tencent 2023`.

### OpenClaw / Cursor

1. Upload or open this entire folder.
2. Keep `SKILL.md` and `agents/openai.yaml` in the package root.
3. Point the assistant at the repo files and ask it to analyze a company using the Buffett Oracle framework.

### Codex plugin

1. Use the seller kit's `*-codex-plugin-*.zip` artifact instead of this raw folder.
2. Install the included `plugins/buffett-oracle/` plus `.agents/plugins/marketplace.json` into your Codex plugin catalog.
3. Invoke the plugin and start with prompts like `Analyze Coca-Cola 1988`.

### Codex / Claude Code

1. Open this folder as a workspace.
2. Run `python3 oracle.py status` and `python3 oracle.py validate`.
3. Ask the assistant to analyze a company while following `CLAUDE.md`.

## Guardrails you should preserve

- Use only information available on or before the decision date.
- Keep the benchmark-scope caveat visible: this repo audits a curated 29-case benchmark, not the full Berkshire universe.
- Do not market the framework as guaranteed predictive accuracy. The methodology caveats are part of the product.
"""


def build_marketplace_listing_copy(manifest: dict[str, Any]) -> str:
    stats = manifest["stats"]
    works_with = ", ".join(manifest["works_with"])
    return f"""# Buffett Oracle — Listing Copy

## Suggested Listing Setup

- Name: Buffett Oracle
- Type: Skill
- Category: Finance / Research
- Works With: {works_with}
- Delivery formats: raw files, standalone skill folder, Codex plugin catalog
- Suggested launch price: $29
- Suggested standard price after first reviews: $49

## Short Description

Buffett-style investment decision engine with a documented 7-gate framework, audited backtests, control groups, cached company cards, and explicit methodology caveats.

## Long Description

Buffett Oracle turns Warren Buffett's investment logic into a usable, inspectable operating system for stock research.

This package gives buyers:

- A full Buffett + Graham framework with 7 hard gates, moat analysis, named exemptions, and lock-the-conclusion discipline
- A public evidence archive with {stats['benchmark_cases_completed']}/{stats['benchmark_cases_total']} completed benchmark cases and a separate {stats['expansion_cases_completed']}/{stats['expansion_cases_total']} expansion track
- {stats['cached_company_cards']} cached company cards so repeated analyses reuse existing work instead of re-reading filings every time
- A portable prompt file for Claude Projects / Custom GPTs plus a skill file for OpenClaw-style tools
- A Codex plugin wrapper so teams can install the same research system through a plugin catalog instead of raw files
- Methodology audit files that show ambiguity, exceptions, and where the framework can still mislead you

## Core Capabilities

- Classify a thesis as INVESTMENT, SPECULATION, or TOO_HARD before doing the work
- Run 7 hard gates and auto-reject fragile businesses
- Force BUY vs PASS conclusions instead of vague hedging
- Require two control-group comparisons for every BUY
- Keep point-in-time discipline so later facts do not leak into the decision
- Reuse archived company cards instead of re-fetching known cases

## Proof Points You Can Safely Claim

- Framework version: {manifest['version']}
- Benchmark archive: {stats['benchmark_cases_completed']}/{stats['benchmark_cases_total']} completed
- Expansion archive: {stats['expansion_cases_completed']}/{stats['expansion_cases_total']} completed
- Cached company cards: {stats['cached_company_cards']}
- Methodology flags currently tracked: {stats['ambiguous_cases']} ambiguous, {stats['exception_cases']} exception-assisted, {stats['buy_control_misses']} BUY-control misses

## Scope Note

Use this exact caveat in the listing:

> The benchmark archive is a curated 29-case set. It is not Buffett or Berkshire's full investment history.

## Positioning Notes

- Best sold as a premium research skill or persona bundle, not as a trading bot
- The Codex plugin wrapper is best framed as a packaging convenience, not a new analytic engine
- Strongest buyer promise: disciplined decision process, evidence archive, and reusable research memory
- Weakest promise: "beats the market" or "predicts Buffett perfectly" - do not sell it that way
"""


def build_marketplace_publish_checklist(manifest: dict[str, Any], bundle: MarketplaceBundle) -> str:
    raw_zip_name = bundle.zip_path.name if bundle.zip_path else f"{manifest['slug']}.zip"
    skill_zip_name = bundle.skill_zip_path.name if bundle.skill_zip_path else f"{manifest['slug']}-skill.zip"
    plugin_zip_name = (
        bundle.plugin_zip_path.name if bundle.plugin_zip_path else f"{manifest['slug']}-codex-plugin.zip"
    )
    return f"""# Publish Checklist

1. Use `preview/social-card.svg` as your initial listing art.
2. Upload `{raw_zip_name}` to raw-files storefronts.
3. Upload `{skill_zip_name}` when a storefront wants a pure skill folder.
4. Upload `{plugin_zip_name}` when distributing through a Codex plugin catalog.
5. Paste the copy from `listing-copy.md` into the marketplace listing.
6. Set the product type to `Skill`.
7. Set works-with tags to: {", ".join(manifest['works_with'])}.
8. Keep the benchmark-scope caveat in the public description.
9. Keep the non-advice disclaimer in the package and listing.
10. After publishing, test one fresh install in both a raw-files flow and a plugin-catalog flow.
"""


def build_marketplace_bundle(
    output_dir: Path = MARKETPLACE_OUTPUT_DIR,
    base_dir: Path = BASE_DIR,
    create_zip: bool = True,
) -> MarketplaceBundle:
    audit_report = build_audit_report(base_dir)
    methodology_report = build_methodology_report(base_dir)

    output_dir.mkdir(parents=True, exist_ok=True)
    package_dir = output_dir / "package" / MARKETPLACE_PACKAGE_SLUG
    skill_dir = output_dir / "skill" / MARKETPLACE_PACKAGE_SLUG
    preview_dir = output_dir / "preview"
    plugin_catalog_dir = output_dir / "plugin-catalog"
    plugin_dir = plugin_catalog_dir / "plugins" / MARKETPLACE_PACKAGE_SLUG
    plugin_manifest_path = plugin_dir / ".codex-plugin" / "plugin.json"
    plugin_catalog_path = plugin_catalog_dir / ".agents" / "plugins" / "marketplace.json"
    package_dir.mkdir(parents=True, exist_ok=True)
    skill_dir.mkdir(parents=True, exist_ok=True)
    preview_dir.mkdir(parents=True, exist_ok=True)
    plugin_manifest_path.parent.mkdir(parents=True, exist_ok=True)
    plugin_catalog_path.parent.mkdir(parents=True, exist_ok=True)

    copy_marketplace_payload(package_dir, base_dir)
    copy_marketplace_payload(skill_dir, base_dir)

    manifest = build_marketplace_manifest(audit_report, methodology_report)
    manifest_path = package_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    (package_dir / "START_HERE.md").write_text(build_marketplace_start_here(manifest), encoding="utf-8")

    listing_copy_path = output_dir / "listing-copy.md"
    listing_copy_path.write_text(build_marketplace_listing_copy(manifest), encoding="utf-8")

    bundle = MarketplaceBundle(
        output_dir=output_dir,
        package_dir=package_dir,
        skill_dir=skill_dir,
        preview_dir=preview_dir,
        plugin_catalog_dir=plugin_catalog_dir,
        plugin_dir=plugin_dir,
        plugin_manifest_path=plugin_manifest_path,
        plugin_catalog_path=plugin_catalog_path,
        manifest_path=manifest_path,
        listing_copy_path=listing_copy_path,
        publish_checklist_path=output_dir / "publish-checklist.md",
        zip_path=None,
        skill_zip_path=None,
        plugin_zip_path=None,
    )

    for relative_path in MARKETPLACE_PREVIEW_ASSETS:
        source_path = base_dir / relative_path
        if source_path.exists():
            copy_path(source_path, preview_dir / source_path.name)

    for asset_name in ("icon.svg", "logo.svg"):
        source_path = base_dir / "assets" / asset_name
        if source_path.exists():
            copy_path(source_path, plugin_dir / "assets" / asset_name)

    copy_path(skill_dir, plugin_dir / "skills" / MARKETPLACE_PACKAGE_SLUG)
    plugin_manifest_path.write_text(
        json.dumps(build_plugin_manifest(manifest), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    plugin_catalog_path.write_text(
        json.dumps(build_plugin_marketplace_catalog(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    bundle.publish_checklist_path.write_text(build_marketplace_publish_checklist(manifest, bundle), encoding="utf-8")

    if create_zip:
        zip_path = output_dir / f"{MARKETPLACE_PACKAGE_SLUG}-clawmart-{manifest['version'].lower()}.zip"
        build_zip_archive(package_dir, package_dir.parent, zip_path)
        bundle.zip_path = zip_path

        skill_zip_path = output_dir / f"{MARKETPLACE_PACKAGE_SLUG}-skill-{manifest['version'].lower()}.zip"
        build_zip_archive(skill_dir, skill_dir.parent, skill_zip_path)
        bundle.skill_zip_path = skill_zip_path

        plugin_zip_path = output_dir / f"{MARKETPLACE_PACKAGE_SLUG}-codex-plugin-{manifest['version'].lower()}.zip"
        build_zip_archive(plugin_catalog_dir, plugin_catalog_dir, plugin_zip_path)
        bundle.plugin_zip_path = plugin_zip_path
        bundle.publish_checklist_path.write_text(build_marketplace_publish_checklist(manifest, bundle), encoding="utf-8")

    return bundle


def format_card_line(record: CardRecord) -> str:
    failed = ", ".join(record.failed_gates) if record.failed_gates else "none"
    channel = record.special_channel or "-"
    return (
        f"{record.path.name:<16} "
        f"{str(record.analysis_year):<4} "
        f"{record.conclusion:<4} "
        f"channel={channel:<17} "
        f"failed={failed}"
    )


def print_validation_messages(report: AuditReport) -> None:
    if report.errors:
        print("Errors:")
        for error in report.errors:
            print(f"  - {error}")

    if report.warnings:
        print("Warnings:")
        for warning in report.warnings:
            print(f"  - {warning}")


def cmd_status(_: argparse.Namespace) -> int:
    report = build_audit_report()
    methodology_report = build_methodology_report()
    pending_preview = ", ".join(f"#{row.index} {row.target}" for row in report.pending_rows[:5]) or "none"
    if len(report.pending_rows) > 5:
        pending_preview += ", ..."

    buy_count = sum(1 for card in report.cards if card.conclusion == "BUY")
    pass_count = sum(1 for card in report.cards if card.conclusion == "PASS")

    print(
        f"""
Buffett Oracle — Repo Status
─────────────────────────────────
Framework version : {report.brain.version}
Framework size    : {report.brain.line_count} lines
Evolution patches : {report.brain.patch_count}

Benchmark set     : {report.completed_cases}/{report.total_cases} completed
Consistency       : {report.accuracy}
Detailed writeups : {len(report.detailed_sections)}
Pending           : {len(report.pending_rows)}
Indexed rows      : {len(report.analysis_index_rows)}
Expansion track   : {report.expansion_completed_cases}/{report.expansion_total_cases} completed
Expansion index   : {len(report.expansion_index_rows)}

Company cards     : {len(report.cards)} cached
BUY / PASS        : {buy_count} / {pass_count}
Method flags      : {len(methodology_report.ambiguous_rows)} ambiguous, {len(methodology_report.exception_rows)} exceptions, {len(methodology_report.buy_cards_with_control_group_issues)} BUY-control misses
Next pending      : {pending_preview}
Coverage scope    : benchmark set + separate universe expansion track
""".strip()
    )

    if report.errors or report.warnings:
        print()
        print_validation_messages(report)
    else:
        print()
        print("Validation: clean")

    return 1 if report.errors else 0


def cmd_validate(args: argparse.Namespace) -> int:
    report = build_audit_report()
    if report.errors or report.warnings:
        print_validation_messages(report)
    else:
        print("Validation passed: repository state is internally consistent.")

    if report.errors:
        return 1
    if args.strict and report.warnings:
        return 1
    return 0


def cmd_site(args: argparse.Namespace) -> int:
    output_dir = build_static_site(Path(args.output).resolve(), site_url=args.site_url)
    print(f"Static site built at: {output_dir}")
    print(f"Open: {output_dir / 'index.html'}")
    if args.site_url:
        print(f"Canonical URL: {normalize_site_url(args.site_url)}/")
    return 0


def cmd_marketplace_bundle(args: argparse.Namespace) -> int:
    bundle = build_marketplace_bundle(Path(args.output).resolve(), create_zip=not args.no_zip)
    manifest = json.loads(bundle.manifest_path.read_text(encoding="utf-8"))
    print(f"Marketplace seller kit built at: {bundle.output_dir}")
    print(f"Package folder: {bundle.package_dir}")
    print(f"Standalone skill: {bundle.skill_dir}")
    print(f"Codex plugin catalog: {bundle.plugin_catalog_dir}")
    print(f"Plugin manifest: {bundle.plugin_manifest_path}")
    print(f"Listing copy: {bundle.listing_copy_path}")
    print(f"Publish checklist: {bundle.publish_checklist_path}")
    print(f"Preview assets: {bundle.preview_dir}")
    if bundle.zip_path:
        print(f"Raw-files zip: {bundle.zip_path}")
    if bundle.skill_zip_path:
        print(f"Skill zip: {bundle.skill_zip_path}")
    if bundle.plugin_zip_path:
        print(f"Plugin zip: {bundle.plugin_zip_path}")
    print(f"Suggested type/category: {manifest['type']} / {manifest['suggested_category']}")
    print("Suggested launch price: $29")
    return 0


def cmd_serve_site(args: argparse.Namespace) -> int:
    output_dir = build_static_site(Path(args.output).resolve(), site_url=args.site_url)
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(output_dir))

    class ThreadingTCPServer(socketserver.ThreadingTCPServer):
        allow_reuse_address = True

    with ThreadingTCPServer(("", args.port), handler) as httpd:
        print(f"Serving Buffett Oracle site at http://127.0.0.1:{args.port}")
        print(f"Root: {output_dir}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopped.")
    return 0


def cmd_backtest(_: argparse.Namespace) -> int:
    audit_report = build_audit_report()
    methodology_report = build_methodology_report()

    def bucket_consistency(rows: list[BacktestRow]) -> str:
        if not rows:
            return "0/0"
        correct = sum(1 for row in rows if row.verdict in BACKTEST_CORRECT_SYMBOLS)
        return f"{correct}/{len(rows)}"

    def row_list(rows: list[BacktestRow]) -> str:
        return ", ".join(f"#{row.index} {row.target}" for row in rows) or "none"

    print(
        f"""
Buffett Oracle — Backtest Rerun
─────────────────────────────────
Completed benchmark cases       : {audit_report.completed_cases}/{audit_report.total_cases}
Headline retrospective consistency : {audit_report.accuracy}
Expansion track completed       : {audit_report.expansion_completed_cases}/{audit_report.expansion_total_cases}
Expansion consistency           : {audit_report.expansion_accuracy}

Core binary non-exception set   : {bucket_consistency(methodology_report.core_binary_rows)}
Ambiguous scored cases          : {bucket_consistency(methodology_report.ambiguous_rows)}
Exception-assisted cases        : {bucket_consistency(methodology_report.exception_rows)}
Exit / non-binary cases         : {bucket_consistency(methodology_report.exit_rows)}

Current bucket members:
  Core       : {row_list(methodology_report.core_binary_rows)}
  Ambiguous  : {row_list(methodology_report.ambiguous_rows)}
  Exceptions : {row_list(methodology_report.exception_rows)}
  Exit       : {row_list(methodology_report.exit_rows)}

Selection quality checks:
  BUY cards with BUY controls   : {len(methodology_report.buy_cards_with_control_group_issues)}
  Scope-drift cards             : {len(methodology_report.cards_with_scope_drift)}

Point-in-time rule:
  Decision logic must use only information available on or before the decision date.
Coverage note:
  Methodology buckets cover the curated benchmark set only.
  Universe expansion is tracked separately and does not change the benchmark hit-rate math.
""".strip()
    )
    return 0


def cmd_methodology(_: argparse.Namespace) -> int:
    report = build_methodology_report()

    def row_list(rows: list[BacktestRow]) -> str:
        return ", ".join(f"#{row.index} {row.target}" for row in rows) or "none"

    buy_control_issue_list = ", ".join(card.path.name for card in report.buy_cards_with_control_group_issues) or "none"
    scope_drift_list = ", ".join(card.path.name for card in report.cards_with_scope_drift) or "none"

    print(
        f"""
Buffett Oracle — Methodology Audit
─────────────────────────────────
Completed benchmark cases     : {len(report.completed_rows)}
Retrospective consistency     : {report.retrospective_consistency}
Ambiguous scored cases        : {len(report.ambiguous_rows)} ({row_list(report.ambiguous_rows)})
Exception-assisted cases      : {len(report.exception_rows)} ({row_list(report.exception_rows)})
Exit / non-binary cases       : {len(report.exit_rows)} ({row_list(report.exit_rows)})
Core binary non-exception set : {len(report.core_binary_rows)} ({row_list(report.core_binary_rows)})
BUY cards with BUY controls   : {len(report.buy_cards_with_control_group_issues)} ({buy_control_issue_list})
Scope-drift cards             : {len(report.cards_with_scope_drift)} ({scope_drift_list})

Notes:
  - This audit covers the curated benchmark set, not the full Buffett/Berkshire investment universe.
  - "Retrospective consistency" is not predictive accuracy.
  - Ambiguous conclusions, exception channels, and non-failing control groups all make the headline win rate look cleaner than it really is.
  - Decision memos must stay point-in-time; later facts belong only in the reveal.
  - oracle.py evolve now requires affected-case metadata, but it still does not automatically verify reruns.
""".strip()
    )
    return 0


def cmd_gate_review(_: argparse.Namespace) -> int:
    report = build_gate_review_report()
    wrong_case_list = ", ".join(report.wrong_case_files) or "none"
    flagged_entries = [entry for entry in report.entries if entry.wrong_case_failures]

    print(
        f"""
Buffett Oracle — Gate Review
─────────────────────────────────
Archived scored cases          : {report.archived_case_count}
Framework-wrong cases          : {report.wrong_case_count} ({wrong_case_list})

False-negative gate triggers:
""".strip()
    )

    if flagged_entries:
        for entry in flagged_entries:
            files = ", ".join(entry.wrong_case_files)
            print(f"  {entry.label} {entry.title}: {entry.wrong_case_failures} wrong-case hits ({files})")
    else:
        print("  none")

    print("\nGate-by-gate assessment:")
    for entry in report.entries:
        files = ", ".join(entry.wrong_case_files) or "none"
        print(
            f"  {entry.label} {entry.title}\n"
            f"    Rule            : {entry.rule}\n"
            f"    Total fails     : {entry.total_failures}\n"
            f"    Wrong-case fails: {entry.wrong_case_failures} ({files})\n"
            f"    Assessment      : {entry.assessment}\n"
            f"    Note            : {entry.note}"
        )

    print(
        "\nCurrent implication:\n"
        "  Keep the 7 gates intact for benchmark comparability, but require an owner-earnings note for Gate 2 failures\n"
        "  and a quality-multiple note for Gate 6 failures in new live or expansion memos."
    )
    return 0


def cmd_cards(_: argparse.Namespace) -> int:
    cards = load_company_cards()
    if not cards:
        print("No company cards found.")
        return 0

    print("Cached company cards:")
    for card in cards:
        print(f"  {format_card_line(card)}")
    return 0


def cmd_pending(_: argparse.Namespace) -> int:
    rows = parse_backtest_rows(load_text(BACKTEST_FILE))
    pending = [row for row in rows if row.verdict == "—"]
    if not pending:
        expansion_rows = parse_backtest_rows(load_text(EXPANSION_FILE))
        if expansion_rows:
            print(
                "No pending benchmark cases. "
                f"Universe expansion currently tracks {len(expansion_rows)} additional completed cases."
            )
        else:
            print("No pending benchmark cases. Broader Buffett/Berkshire universe expansion remains open.")
        return 0

    print("Pending backtest cases:")
    for row in pending:
        print(f"  #{row.index:<2} {row.target} ({row.decision_year})")
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    matches = [card for card in load_company_cards() if card_matches_query(card, args.query)]
    if not matches:
        print(f"No company card matched: {args.query}")
        return 1

    for index, record in enumerate(matches, start=1):
        if len(matches) > 1:
            print(f"[{index}] {record.path.name}")
        print(json.dumps(record.payload, ensure_ascii=False, indent=2))
    return 0


def cmd_brain(_: argparse.Namespace) -> int:
    brain = load_brain()
    if not brain:
        print("大脑文件不存在：", BRAIN_FILE)
        return 1
    print(brain)
    return 0


def cmd_corpus(_: argparse.Namespace) -> int:
    print("\n📚 可用语料：\n")
    qa_dir = CORPUS_DIR / "2019/巴菲特股东大会1994-2025"
    if qa_dir.exists():
        print(f"[股东大会 Q&A] — {qa_dir}")
        for item in sorted(qa_dir.iterdir()):
            if item.is_dir():
                files = list(item.glob("*.txt"))
                print(f"  {item.name}/  ({len(files)} 个文件)")
            else:
                print(f"  {item.name}")
        print()

    letter_dir = CORPUS_DIR / "2019/巴菲特致股东信1957-2025/中文翻译"
    if letter_dir.exists():
        files = sorted(letter_dir.glob("*.docx"))
        if files:
            print(f"[股东信中文翻译] — {letter_dir}")
            print(f"  共 {len(files)} 封，从 {files[0].stem} 到 {files[-1].stem}")
            print()

    en_dir = CORPUS_DIR / "2019/巴菲特致股东信1957-2025/英文原文"
    if en_dir.exists():
        files = sorted(en_dir.glob("*.pdf"))
        if files:
            print(f"[股东信英文原文] — {en_dir}")
            print(f"  共 {len(files)} 封 PDF")
    return 0


def cmd_learn(args: argparse.Namespace) -> int:
    path = Path(args.filepath)
    if not path.exists():
        print(f"文件不存在：{path}")
        return 1

    content = path.read_text(encoding="utf-8", errors="ignore")
    if len(content) > 15000:
        content = content[:15000] + "\n...[截断，仅取前15000字]"

    prompt = f"""你现在扮演「巴菲特神谕」的大脑进化模块。

当前大脑内容（buffett_brain.md）已在你脑中。

以下是新的语料（来源：{path.name}）：

---
{content}
---

请：
1. 提炼这段语料中有价值的新投资原则、判断逻辑、或具体案例
2. 指出与现有大脑内容的关联或补充（不要重复已有内容）
3. 给出一段可以直接追加到 buffett_brain.md 的 Markdown 内容

格式要求：
- 用 ## 进化补丁 — {datetime.date.today()} (来源: {path.name}) 作为标题
- 内容简洁，只写真正有增量价值的部分
- 附一行版本更新日志，格式：版本升级建议：v1.x"""

    print("\n" + "=" * 60)
    print("📋 已生成语料提炼提示词，请复制以下内容粘贴到 Claude Code：")
    print("=" * 60 + "\n")
    print(prompt)
    print("\n" + "=" * 60)
    print("📌 Claude Code 回复后，用以下命令把内容追加到大脑：")
    print("   python3 oracle.py evolve")
    print("=" * 60)

    try:
        import subprocess

        subprocess.run("pbcopy", input=prompt.encode(), check=True)
        print("\n✅ 已自动复制到剪贴板，直接 Cmd+V 粘贴即可。")
    except Exception:
        pass
    return 0


def cmd_evolve(_: argparse.Namespace) -> int:
    print("\n先记录这次方法学修改影响哪些案例。")
    affected_cases = input("受影响案例编号（例如 #7,#9,#13）：").strip()
    if not affected_cases:
        print("必须提供受影响案例编号，退出。")
        return 1

    rerun_summary = input("重跑/回归摘要：").strip()
    if not rerun_summary:
        print("必须提供重跑/回归摘要，退出。")
        return 1

    print("\n输入要添加到 buffett_brain.md 的内容（Markdown 格式）。")
    print("输入完成后，单独一行输入 END 结束：\n")
    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line.strip() == "END":
            break
        lines.append(line)

    if not lines:
        print("没有输入内容，退出。")
        return 1

    new_content = "\n".join(lines)
    brain_content = load_brain()
    today = datetime.date.today().isoformat()

    versions = re.findall(r"\|\s*v(\d+)\.(\d+)\s*\|", brain_content)
    if versions:
        major, minor = versions[-1]
        next_version = f"v{major}.{int(minor) + 1}"
    else:
        next_version = "v1.1"

    version_row = f"| {next_version} | {today} | 手动进化 | evolve 命令；影响案例 {affected_cases} |"
    if "## 原始语料索引" in brain_content:
        brain_content = brain_content.replace("## 原始语料索引", f"{version_row}\n\n## 原始语料索引", 1)
    else:
        brain_content += f"\n\n## 自我进化记录\n\n| 版本 | 日期 | 更新内容 | 触发原因 |\n|---|---|---|---|\n{version_row}\n"

    metadata_block = f"> 影响案例：{affected_cases}\n> 回归摘要：{rerun_summary}"
    brain_content += f"\n\n---\n\n{metadata_block}\n\n{new_content}\n"
    BRAIN_FILE.write_text(brain_content, encoding="utf-8")
    print(f"\n✅ 大脑已更新至 {next_version}。")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Buffett Oracle repository helper")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("status", help="Show repository status")

    validate_parser = subparsers.add_parser("validate", help="Validate cards, README, and backtest consistency")
    validate_parser.add_argument("--strict", action="store_true", help="Exit non-zero on warnings too")

    subparsers.add_parser("backtest", help="Re-run current backtest summary with methodology buckets")
    site_parser = subparsers.add_parser("site", help="Build the static website into docs/")
    site_parser.add_argument("--output", default=str(SITE_OUTPUT_DIR), help="Output directory for the built site")
    site_parser.add_argument("--site-url", default="", help="Public site URL for canonical and social metadata")

    bundle_parser = subparsers.add_parser(
        "marketplace-bundle",
        help="Build seller-kit outputs for raw files, standalone skill installs, and Codex plugins",
    )
    bundle_parser.add_argument("--output", default=str(MARKETPLACE_OUTPUT_DIR), help="Output directory for bundle files")
    bundle_parser.add_argument("--no-zip", action="store_true", help="Skip generating the buyer .zip archive")

    serve_parser = subparsers.add_parser("serve-site", help="Build and preview the static website locally")
    serve_parser.add_argument("--output", default=str(SITE_OUTPUT_DIR), help="Output directory for the built site")
    serve_parser.add_argument("--site-url", default="", help="Public site URL for canonical and social metadata")
    serve_parser.add_argument("--port", type=int, default=8000, help="Port to bind the local preview server")

    subparsers.add_parser("cards", help="List cached company cards")
    subparsers.add_parser("pending", help="List pending backtest cases")
    subparsers.add_parser("methodology", help="Audit methodology quality beyond repo consistency")
    subparsers.add_parser("gate-review", help="Audit which hard gates are causing false negatives")

    show_parser = subparsers.add_parser("show", help="Display a company card by ticker/company/file query")
    show_parser.add_argument("query")

    subparsers.add_parser("brain", help="Print buffett_brain.md")
    subparsers.add_parser("corpus", help="Browse local Buffett corpus")

    learn_parser = subparsers.add_parser("learn", help="Generate a learning prompt from a local file")
    learn_parser.add_argument("filepath")

    subparsers.add_parser("evolve", help="Append an evolution patch to buffett_brain.md")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    command = args.command or "status"
    handlers = {
        "status": cmd_status,
        "validate": cmd_validate,
        "backtest": cmd_backtest,
        "site": cmd_site,
        "marketplace-bundle": cmd_marketplace_bundle,
        "serve-site": cmd_serve_site,
        "cards": cmd_cards,
        "pending": cmd_pending,
        "methodology": cmd_methodology,
        "gate-review": cmd_gate_review,
        "show": cmd_show,
        "brain": cmd_brain,
        "corpus": cmd_corpus,
        "learn": cmd_learn,
        "evolve": cmd_evolve,
    }
    return handlers[command](args)


if __name__ == "__main__":
    sys.exit(main())
