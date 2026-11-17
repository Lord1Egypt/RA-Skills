#!/usr/bin/env python3
"""Bounded, read-only project fingerprint and recommendation scanner."""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # 优雅降级：缺少 PyYAML 时主入口输出 unavailable 并以退出码 2 退出
    yaml = None


ROOT = Path(__file__).resolve().parent.parent
IGNORE_DIRS = {
    ".git", "node_modules", ".venv", "__pycache__", "dist", "build", ".next", "target", "vendor",
    "fixture-data", "fixtures", ".audit-snapshots", ".tmp", "tmp", "backups", "archives",
    "archived_sessions", "sessions", "worktrees", ".archived", "memories", "snapshots",
    ".codegraph", "browser_data", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".cache", ".webassets-cache",
}
IGNORE_FILES = {"tech-fingerprints.yaml", "project-types.yaml"}


def iter_files(project: Path, max_files: int, max_depth: int) -> tuple[list[Path], bool]:
    found: list[Path] = []
    if not project.exists():
        return found, False
    depth_truncated = False
    for current, directories, files in os.walk(project, topdown=True, followlinks=False):
        base = Path(current)
        depth = len(base.relative_to(project).parts)
        eligible = [name for name in directories if name not in IGNORE_DIRS and not (base / name).is_symlink()]
        depth_truncated = depth_truncated or (depth >= max_depth and bool(eligible))
        directories[:] = eligible if depth < max_depth else []
        for name in files:
            path = base / name
            # SQLite indexes and browser stores are runtime/cache evidence, not project technology evidence.
            if path.is_file() and name not in IGNORE_FILES and path.suffix.lower() not in {".db", ".sqlite", ".sqlite3"}:
                found.append(path)
                if len(found) >= max_files:
                    return found, True
    return found, depth_truncated


def load_yaml(path: Path):
    with path.open("r", encoding="utf-8-sig") as handle:
        return yaml.safe_load(handle)


def matching_files(files: list[Path], project: Path, patterns: list[str]) -> list[Path]:
    return [path for path in files if any(path.relative_to(project).match(pattern) for pattern in patterns)]


def package_version(project: Path, tech: dict, package_files: list[Path] | None = None) -> str | None:
    probe = tech.get("version_probe") or {}
    if probe.get("file") != "package.json":
        return None
    dependency = str(probe.get("jsonpath", "")).split(".")[-1]
    candidates = list(package_files or [])
    if not candidates:
        candidates = [project / "package.json"]
    # Prefer the root manifest while still supporting independently versioned nested packages.
    candidates.sort(key=lambda path: (path != project / "package.json", len(path.parts)))
    for package in candidates:
        if not package.exists():
            continue
        try:
            data = json.loads(package.read_text(encoding="utf-8-sig"))
        except (OSError, json.JSONDecodeError):
            continue
        version = (data.get("dependencies") or {}).get(dependency) or (data.get("devDependencies") or {}).get(dependency)
        if version:
            return version
    return None


def package_records(files: list[Path], project: Path) -> list[tuple[Path, dict, set[str]]]:
    records: list[tuple[Path, dict, set[str]]] = []
    for path in files:
        if path.name != "package.json":
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8-sig"))
        except (OSError, json.JSONDecodeError):
            continue
        dependencies = set((data.get("dependencies") or {})) | set((data.get("devDependencies") or {}))
        records.append((path, data, dependencies))
    return records


def candidate_skills(skills: list[dict]) -> list[dict]:
    """Keep compatibility fields while preventing unverified effect claims from being facts."""
    result = []
    for skill in skills:
        if not isinstance(skill, dict):
            continue
        item = dict(skill)
        item["priority"] = "candidate"
        item["why"] = "项目特征命中内置候选规则；仍需核验具体需求、来源和已安装替代项。"
        item["fact_status"] = "inferred"
        item["availability"] = "unavailable"
        if "effect" in item:
            item["effect"] = "效果未验证（需结合项目实际评估）"
        result.append(item)
    return result


def detect(project: Path, max_files: int = 2000, max_depth: int = 10) -> dict:
    files, truncated = iter_files(project, max_files, max_depth)
    database = load_yaml(ROOT / "references" / "tech-fingerprints.yaml")
    detected: list[dict] = []
    fingerprint_errors: list[dict] = []
    for category, entries in database.items():
        if not isinstance(entries, list):
            continue
        for tech in entries:
            if not isinstance(tech, dict):
                continue
            evidence: list[dict] = []
            for fingerprint in tech.get("fingerprints", []) or []:
                candidates = matching_files(files, project, fingerprint.get("files", []) or [])
                pattern = fingerprint.get("contents")
                if pattern:
                    pattern = str(pattern).replace("\\\\", "\\")
                    try:
                        compiled = re.compile(pattern)
                    except re.error as exc:
                        fingerprint_errors.append({"technology": tech.get("id"), "pattern": pattern, "error": str(exc)})
                        candidates = []
                    else:
                        candidates = [path for path in candidates if compiled.search(path.read_text(encoding="utf-8", errors="ignore"))]
                for path in candidates[:8]:
                    evidence.append({"path": str(path.relative_to(project)), "confidence": fingerprint.get("confidence", "low")})
            if evidence:
                rank = {"high": 3, "medium": 2, "low": 1}
                confidence = max(evidence, key=lambda item: rank.get(item["confidence"], 0))["confidence"]
                package_evidence = [project / item["path"] for item in evidence if item["path"].endswith("package.json")]
                version = package_version(project, tech, package_evidence)
                detected.append({"id": tech.get("id"), "name": tech.get("name"), "category": tech.get("category", category), "confidence": confidence, "version": version, "version_status": "declared_range" if version else "unavailable", "evidence": evidence, "tags": tech.get("tags", [])})
    ids = {item["id"] for item in detected}
    types: list[dict] = []
    for rule in (database.get("matching_rules", {}).get("project_type_inference", []) or []):
        matched = [tech_id for tech_id in rule.get("when_any", []) if tech_id in ids]
        if matched:
            types.append({"type": rule.get("then_type"), "confidence": rule.get("confidence"), "based_on": matched})

    project_types = load_yaml(ROOT / "references" / "project-types.yaml") or []
    recommendations: list[dict] = []
    packages = package_records(files, project)
    matched_recommendations = 0
    for entry in project_types:
        pattern = entry.get("pattern", {}) if isinstance(entry, dict) else {}
        if pattern.get("fallback"):
            continue
        checks: list[bool] = []
        evidence: list[str] = []
        file_patterns = pattern.get("files", []) or []
        if file_patterns:
            matched = matching_files(files, project, file_patterns)
            checks.append(bool(matched))
            evidence.extend(str(path.relative_to(project)) for path in matched[:8])
        contained_patterns = pattern.get("contains_files", []) or []
        if contained_patterns:
            matched = matching_files(files, project, contained_patterns)
            minimum = int(pattern.get("count_min", 1))
            checks.append(len(matched) >= minimum)
            evidence.extend(str(path.relative_to(project)) for path in matched[:8])
        contained_dirs = pattern.get("contains_dirs", []) or []
        if contained_dirs:
            found_dirs = [name for name in contained_dirs if (project / name).is_dir()]
            checks.append(len(found_dirs) == len(contained_dirs))
            evidence.extend(found_dirs)
        required = set(pattern.get("contains_deps", []) or [])
        if required:
            scope = [record for record in packages if not file_patterns or record[0] in matching_files(files, project, file_patterns)]
            matching_packages = [record for record in scope if required <= record[2]]
            checks.append(bool(matching_packages))
            for path, _, _ in matching_packages[:8]:
                evidence.append(f"{path.relative_to(project)} dependencies: " + ", ".join(sorted(required)))
        if checks and all(checks):
            recommendations.append({"project_type": entry.get("type"), "description": entry.get("description"), "skills": candidate_skills(entry.get("skills", [])), "evidence": list(dict.fromkeys(evidence)), "status": "rule_based_candidate", "fact_status": "inferred", "availability": "installable_unverified", "market_status": "not_verified"})
            matched_recommendations += 1

    if not matched_recommendations:
        fallback = next((entry for entry in project_types if isinstance(entry, dict) and (entry.get("pattern") or {}).get("fallback")), None)
        if fallback:
            recommendations.append({"project_type": fallback.get("type"), "description": fallback.get("description"), "skills": candidate_skills(fallback.get("skills", [])), "evidence": ["未命中更具体的 project-types 规则"], "status": "rule_based_candidate", "fact_status": "inferred", "availability": "installable_unverified", "market_status": "not_verified"})
    merged_recommendations: dict[str, dict] = {}
    for recommendation in recommendations:
        project_type = str(recommendation.get("project_type"))
        existing = merged_recommendations.get(project_type)
        if existing is None:
            merged_recommendations[project_type] = recommendation
            continue
        existing["evidence"] = list(dict.fromkeys([*existing.get("evidence", []), *recommendation.get("evidence", [])]))
        existing_skills = {str(skill.get("name")): skill for skill in existing.get("skills", []) if isinstance(skill, dict)}
        for skill in recommendation.get("skills", []):
            if isinstance(skill, dict):
                existing_skills.setdefault(str(skill.get("name")), skill)
        existing["skills"] = list(existing_skills.values())
    recommendations = list(merged_recommendations.values())
    return {"schema_version": 1, "mode": "read_only", "project": str(project.resolve()), "limits": {"max_files": max_files, "max_depth": max_depth, "files_scanned": len(files), "truncated": truncated}, "detected_technologies": detected, "inferred_project_types": types, "recommendations": recommendations, "fingerprint_errors": fingerprint_errors, "fact_status": "observed"}


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    parser = argparse.ArgumentParser(description="Scan project technology fingerprints without writing files.")
    parser.add_argument("project", type=Path)
    parser.add_argument("--max-files", type=int, default=2000)
    parser.add_argument("--max-depth", type=int, default=10)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    if yaml is None:
        if args.as_json:
            print(json.dumps({"status": "unavailable", "reason": "PyYAML not installed", "remediation": "pip install pyyaml"}, ensure_ascii=False, indent=2))
        else:
            print("错误：缺少 PyYAML 依赖，无法加载 YAML 技术指纹文件。请运行 pip install -r requirements.txt 后重试。", file=sys.stderr)
        return 2
    report = detect(args.project, args.max_files, args.max_depth)
    if args.as_json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"项目画像：{report['project']}；扫描 {report['limits']['files_scanned']} 个文件，识别 {len(report['detected_technologies'])} 项技术")
        for tech in report["detected_technologies"]:
            print(f"- {tech['name']} [{tech['confidence']}] version={tech['version'] or 'unavailable'}")
        for recommendation in report["recommendations"]:
            print(f"规则候选组（未验证安装/市场）：{recommendation['project_type']} ({len(recommendation['skills'])} 项)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
