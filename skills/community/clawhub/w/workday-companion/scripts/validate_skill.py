#!/usr/bin/env python3
"""Run the compact Workday Companion v1 release gates with stdlib only."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import struct
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {".md", ".json", ".py", ".yaml", ".yml", ".html", ".css", ".svg"}
TOP_LEVEL = {"SKILL.md", "agents", "assets", "references", "schemas", "scripts", "templates", "adapters"}
REQUIRED_FILES = {
    "SKILL.md",
    "agents/openai.yaml",
    "references/module-contracts.md",
    "references/lunch-oracle-category-library.md",
    "references/product-pattern-library.md",
    "references/audience-coverage.md",
    "references/clawhub-discovery-playbook.md",
    "references/smoke-cases.json",
    "references/golden-judgments.json",
    "references/public-listing-pack.json",
    "templates/baseline-intake.md",
    "templates/image-card-prompts.md",
    "adapters/image-model.md",
    "schemas/judgment.schema.json",
    "schemas/card.schema.json",
    "scripts/validate_skill.py",
    "scripts/validate_card.py",
    "scripts/judgment_to_card.py",
    "scripts/render_card.py",
    "scripts/validate_rendered_cards.py",
    "scripts/package_release.py",
    "assets/card-template.html",
    "assets/card-template.css",
}
PRIVATE_MARKERS = (
    "/" + "Users/",
    "/var/" + "folders/",
    "zheng" + "mingyi",
)
STALE_MARKERS = (
    "v1" + ".1",
    "V1" + ".1",
    "v1" + ".2",
    "V1" + ".2",
    "2026" + "0709",
    "2026" + "0712",
)
MODULES = {"今日工作签", "午饭判官", "精神天气台", "下班放行单"}
PUBLIC_STEMS = {"work-sign-low-energy", "lunch-hot-meal", "mood-low-battery", "afterwork-direct-home"}


class GateFailure(RuntimeError):
    pass


def load_json(relative: str) -> Any:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def load_module(relative: str, name: str):
    path = ROOT / relative
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise GateFailure(f"cannot load {relative}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def require(condition: bool, message: str) -> None:
    if not condition:
        raise GateFailure(message)


def iter_package_files() -> list[Path]:
    return sorted(path for path in ROOT.rglob("*") if path.is_file() and "__pycache__" not in path.parts)


def gate_structure() -> str:
    names = {path.name for path in ROOT.iterdir() if not path.name.startswith(".")}
    require(names <= TOP_LEVEL, f"unexpected top-level entries: {sorted(names - TOP_LEVEL)}")
    missing = sorted(relative for relative in REQUIRED_FILES if not (ROOT / relative).is_file())
    require(not missing, f"missing required files: {missing}")
    require(not (ROOT / "README.md").exists(), "README.md does not belong inside the skill")
    return f"files={len(iter_package_files())}"


def parse_frontmatter(text: str) -> dict[str, str]:
    require(text.startswith("---\n"), "SKILL.md frontmatter missing")
    end = text.find("\n---\n", 4)
    require(end > 0, "SKILL.md frontmatter not closed")
    values: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip('"')
    return values


def gate_skill_entry() -> str:
    text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    meta = parse_frontmatter(text)
    require(meta.get("name") == "workday-companion", "skill name drifted")
    description = meta.get("description", "")
    for marker in (
        "工作伴侣",
        "四件小事判官",
        "午饭",
        "精神天气",
        "下班",
        "来张图",
        "Daily Decision Helper",
        "decision fatigue",
        "what should I eat",
        "mood check-in",
        "after-work planner",
    ):
        require(marker in description, f"description missing trigger: {marker}")
    require(len(text.splitlines()) <= 180, "SKILL.md exceeds 180 lines")
    require("# 工作伴侣｜四件小事判官" in text, "Chinese differentiated title missing")
    require("先给一个临时判断" in text, "result-first rule missing")
    require("只补问一个" in text, "single-question rule missing")
    require("探测当前环境" in text, "image capability probe missing")
    return f"lines={len(text.splitlines())}"


def gate_user_surface() -> str:
    text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    marker = "## Agent 执行说明"
    require(marker in text, "Agent execution boundary missing")
    public, agent = text.split(marker, 1)
    public_lines = len(public.splitlines())
    agent_lines = len(agent.splitlines())
    require(public_lines > agent_lines, "SKILL.md must remain primarily user-facing")
    for heading in ("## 咱们不一样", "## 适合谁", "## 立即试用", "## 你会拿到什么", "## 为什么用起来轻", "## 看一眼效果：四张演示图", "## 图卡", "## 使用边界"):
        require(heading in public, f"public landing section missing: {heading}")
    for marker_text in ("今天先这么过。", "咱们的工作伴侣不一样", "今天全套，快点", "先给判断", "现实优先", "最多追问一个字段"):
        require(marker_text in public, f"public value copy missing: {marker_text}")
    for blocked in ("references/", "scripts/", "schemas/", "baseline", "release gate", "JSON"):
        require(blocked not in public, f"internal term leaked into public surface: {blocked}")
    cjk_count = len(re.findall(r"[\u4e00-\u9fff]", public))
    require(cjk_count >= 500, "public surface needs more Chinese user-facing copy")
    for stem in sorted(PUBLIC_STEMS):
        url = (
            "/api/v1/skills/workday-companion/file"
            f"?path=assets%2Fpublic-cards%2F{stem}.svg&tag=latest"
        )
        require(url in public, f"public SVG demo URL missing: {stem}")
    return f"public_lines={public_lines} agent_lines={agent_lines} cjk={cjk_count}"


def gate_links() -> str:
    text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    pattern = r"(?:references|templates|adapters|scripts|schemas|assets)/[A-Za-z0-9_.*/-]+"
    links = sorted(set(re.findall(pattern, text)))
    missing: list[str] = []
    for link in links:
        clean = link.rstrip(".,;:)")
        if "*" in clean:
            continue
        if not (ROOT / clean).exists():
            missing.append(clean)
    require(not missing, f"SKILL.md has missing local links: {missing}")
    return f"links={len(links)}"


def gate_agents_metadata() -> str:
    text = (ROOT / "agents/openai.yaml").read_text(encoding="utf-8")
    require('display_name: "工作伴侣｜四件小事判官"' in text, "display_name lost differentiated Chinese name")
    require("开工、午饭、低电量、下班" in text, "short description lost four-decision promise")
    require("先拍板" in text and "最多补问一个字段" in text, "default prompt contract drifted")
    require("请使用 $workday-companion" in text and "Use $workday-companion" not in text, "default prompt must stay Chinese-first")
    return "display=工作伴侣｜四件小事判官"


def gate_json_and_schemas() -> str:
    json_files = sorted(ROOT.rglob("*.json"))
    for path in json_files:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise GateFailure(f"invalid JSON {path.relative_to(ROOT)}:{exc.lineno}") from exc
    card_schema = load_json("schemas/card.schema.json")
    required = set(card_schema.get("required", []))
    require({"alt_text", "share_safe"} <= required, "card schema must require alt_text and share_safe")
    judgment_schema = load_json("schemas/judgment.schema.json")
    require(set(judgment_schema.get("required", [])) >= {"module", "reason", "action", "share_safe"}, "judgment schema incomplete")
    return f"json={len(json_files)}"


def gate_runtime_contracts() -> str:
    module_text = (ROOT / "references/module-contracts.md").read_text(encoding="utf-8")
    for marker in MODULES | {"固定 6 项", "饭后短反馈", "台风预警", "候选分级", "今日全套"}:
        require(marker in module_text, f"module contracts missing: {marker}")
    baseline = (ROOT / "templates/baseline-intake.md").read_text(encoding="utf-8")
    for marker in ("饭前 30 秒", "3-8 个候选", "饭后回票", "回家方向", "拒填降级"):
        require(marker in baseline, f"baseline template missing: {marker}")
    lunch = (ROOT / "references/lunch-oracle-category-library.md").read_text(encoding="utf-8")
    for marker in ("快稳热饭", "轻负担碗", "汤面回血", "蛋白补给", "校区预算餐", "远程快手餐", "Candidate Verdict Matrix"):
        require(marker in lunch, f"lunch library missing: {marker}")
    return "modules=4 lunch_categories=covered"


def gate_pattern_and_audience() -> str:
    patterns = (ROOT / "references/product-pattern-library.md").read_text(encoding="utf-8")
    for marker in ("Daylio", "Finch", "I Am", "Beli", "Google Maps", "Foursquare", "Eventbrite"):
        require(marker in patterns, f"product pattern missing: {marker}")
    audience = (ROOT / "references/audience-coverage.md").read_text(encoding="utf-8")
    for marker in ("办公室", "通勤", "学生", "实习", "自由职业", "远程"):
        require(marker in audience, f"audience coverage missing: {marker}")
    return "patterns=7 audience=4+"


def gate_clawhub_discovery() -> str:
    text = (ROOT / "references/clawhub-discovery-playbook.md").read_text(encoding="utf-8")
    for marker in (
        "双语搜索",
        "详情核验",
        "安全审计",
        "下载量只作补充信号",
        "咱们的工作伴侣不一样",
        "openclaw skills install @killsnake01/workday-companion",
    ):
        require(marker in text, f"ClawHub discovery playbook missing: {marker}")
    for query in (
        "workday companion",
        "daily decision helper",
        "decision fatigue",
        "what should I eat",
        "mood check-in",
        "work buddy",
        "after-work planner",
    ):
        require(query in text, f"ClawHub search intent missing: {query}")
    return "bilingual_queries=7 comparison=ready"


def gate_images() -> str:
    adapter = (ROOT / "adapters/image-model.md").read_text(encoding="utf-8")
    prompts = (ROOT / "templates/image-card-prompts.md").read_text(encoding="utf-8")
    for marker in ("能力探测", "可调用", "未知或不可用", "alt_text", "隐私门禁"):
        require(marker in adapter, f"image adapter missing: {marker}")
    for marker in MODULES | {"No readable text", "Overlay", "能力降级"}:
        require(marker in prompts, f"image prompt missing: {marker}")
    return "stages=4 fallback=ready"


def gate_cards() -> str:
    validate_card = load_module("scripts/validate_card.py", "validate_card_module")
    converter = load_module("scripts/judgment_to_card.py", "judgment_to_card_module")
    cards = sorted((ROOT / "assets/golden-cards").glob("*.json"))
    require(len(cards) == 8, f"expected 8 golden cards, got {len(cards)}")
    for path in cards:
        errors = validate_card.validate_card(json.loads(path.read_text(encoding="utf-8")))
        require(not errors, f"invalid card {path.name}: {errors}")
    judgments = load_json("references/golden-judgments.json")
    if isinstance(judgments, dict) and isinstance(judgments.get("cases"), list):
        items = [case.get("judgment") for case in judgments["cases"]]
    else:
        items = judgments.get("judgments", judgments) if isinstance(judgments, dict) else judgments
    require(isinstance(items, list) and len(items) >= 4, "golden judgments must cover four modules")
    converted_modules: set[str] = set()
    for item in items:
        require(isinstance(item, dict), "golden judgment entry must be an object")
        card = converter.convert_judgment(item)
        errors = validate_card.validate_card(card)
        require(not errors, f"judgment bridge produced invalid card: {errors}")
        converted_modules.add(card["module"])
    require(converted_modules == MODULES, f"judgment bridge coverage drifted: {converted_modules}")
    return f"golden_cards={len(cards)} judgments={len(items)}"


def gate_smoke_cases() -> str:
    payload = load_json("references/smoke-cases.json")
    cases = payload.get("cases", [])
    require(len(cases) >= 9, "smoke suite must keep at least 9 cases")
    ids: set[str] = set()
    for case in cases:
        case_id = case.get("id")
        require(isinstance(case_id, str) and case_id not in ids, f"duplicate or invalid smoke id: {case_id}")
        ids.add(case_id)
        output = case.get("output", "")
        require(isinstance(output, str) and output.strip(), f"{case_id} output missing")
        for marker in case.get("must_contain", []):
            require(marker in output, f"{case_id} missing required marker: {marker}")
        for marker in case.get("must_not_contain", []):
            require(marker not in output, f"{case_id} contains blocked marker: {marker}")
        require(len(output.splitlines()) <= int(case.get("max_lines", 999)), f"{case_id} exceeds line limit")
    expected = {
        "lunch_no_candidate_magic",
        "lunch_five_candidates_verdict",
        "work_charm_empty_task",
        "mood_low_battery",
        "afterwork_missing_route",
        "daily_pack_zero_candidate_table",
        "staged_image_user_model_unknown",
        "negative_feedback_short_repair",
        "clawhub_compare_install",
    }
    require(expected <= ids, f"core smoke cases missing: {sorted(expected - ids)}")
    return f"cases={len(cases)}"


def png_dimensions(path: Path) -> tuple[int, int]:
    header = path.read_bytes()[:24]
    require(len(header) == 24 and header[:8] == b"\x89PNG\r\n\x1a\n" and header[12:16] == b"IHDR", f"invalid PNG: {path.name}")
    return struct.unpack(">II", header[16:24])


def gate_public_listing() -> str:
    listing = load_json("references/public-listing-pack.json")
    identity = listing.get("identity", {})
    require(identity.get("display_name") == "工作伴侣｜四件小事判官", "public listing differentiated name drifted")
    require(identity.get("product_action") == "每天替你判四件小事", "public product action drifted")
    discovery = listing.get("discoverability", {})
    require("咱们的工作伴侣不一样" in discovery.get("difference_line", ""), "public difference line missing")
    require(len(discovery.get("search_intents", [])) >= 7, "public search intents incomplete")
    agents_text = (ROOT / "agents/openai.yaml").read_text(encoding="utf-8")
    prompt_match = re.search(r'^\s*default_prompt:\s*"([^"]+)"\s*$', agents_text, flags=re.MULTILINE)
    require(prompt_match is not None, "agents default prompt missing")
    require(listing.get("default_prompt") == prompt_match.group(1), "public listing prompt drifted from agents metadata")
    require(len(listing.get("public_entries", [])) == 2, "public listing must keep two entry groups")
    modules = {item.get("module") for item in listing.get("module_cards", [])}
    require(modules == MODULES, f"public module cards drifted: {modules}")
    public_cards = listing.get("media_assets", {}).get("public_cards", [])
    require(len(public_cards) == 4, "public listing must link four rendered cards")
    stems: set[str] = set()
    for item in public_cards:
        png = ROOT / item["png"]
        svg = ROOT / item["svg"]
        require(png.is_file() and svg.is_file(), f"public card missing: {item}")
        require(png_dimensions(png) == (900, 1600), f"public PNG dimensions drifted: {png.name}")
        svg_text = svg.read_text(encoding="utf-8")
        require("<desc>" in svg_text, f"public SVG alt description missing: {svg.name}")
        stems.add(png.stem)
    require(stems == PUBLIC_STEMS, f"public card set drifted: {stems}")
    return "entries=2 public_cards=4"


def gate_privacy_and_staleness() -> str:
    scanned = 0
    for path in iter_package_files():
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        text = path.read_text(encoding="utf-8")
        scanned += 1
        for marker in PRIVATE_MARKERS:
            require(marker not in text, f"private marker {marker!r} in {path.relative_to(ROOT)}")
        for marker in STALE_MARKERS:
            require(marker not in text, f"stale marker {marker!r} in {path.relative_to(ROOT)}")
    return f"text_files={scanned}"


GATES = (
    ("structure", gate_structure),
    ("skill-entry", gate_skill_entry),
    ("user-surface", gate_user_surface),
    ("local-links", gate_links),
    ("agents-metadata", gate_agents_metadata),
    ("json-schemas", gate_json_and_schemas),
    ("runtime-contracts", gate_runtime_contracts),
    ("patterns-audience", gate_pattern_and_audience),
    ("clawhub-discovery", gate_clawhub_discovery),
    ("image-flow", gate_images),
    ("card-data", gate_cards),
    ("smoke-cases", gate_smoke_cases),
    ("public-listing", gate_public_listing),
    ("privacy-staleness", gate_privacy_and_staleness),
)


def validate_all(quiet: bool = False) -> dict[str, str]:
    results: dict[str, str] = {}
    for name, gate in GATES:
        detail = gate()
        results[name] = detail
        if not quiet:
            print(f"OK {name} {detail}")
    if not quiet:
        digest = hashlib.sha256(json.dumps(results, sort_keys=True).encode()).hexdigest()[:12]
        print(f"OK workday-companion v1 gates={len(results)} digest={digest}")
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate the compact Workday Companion v1 skill.")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()
    try:
        validate_all(quiet=args.quiet)
    except (GateFailure, OSError, ValueError, KeyError, TypeError) as exc:
        print(f"FAIL {exc}")
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
