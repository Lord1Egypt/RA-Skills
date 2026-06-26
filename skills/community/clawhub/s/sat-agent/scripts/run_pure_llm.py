#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Sequence, Tuple


SKIP_DIRS = {
    ".git",
    ".idea",
    ".venv",
    "venv",
    "target",
    "build",
    "dist",
    "node_modules",
    "__pycache__",
}

NOISE_PATH_MARKERS = {
    "/.git/",
    "/node_modules/",
    "/target/",
    "/build/",
    "/dist/",
    "/.idea/",
}

PERMISSION_ANNOTATION_RE = re.compile(r"@(RequiresPermissions|RequiresRoles|PreAuthorize|SaCheckPermission)\b")
MAPPING_ANNOTATION_RE = re.compile(r"@(RequestMapping|GetMapping|PostMapping|PutMapping|DeleteMapping)\b")


PROFILE_LIBRARY: Dict[str, Dict[str, object]] = {
    "java-web": {
        "suffixes": {".java", ".xml", ".properties", ".yml", ".yaml", ".jsp", ".jspx"},
        "sources": [
            ("spring_mapping", "Spring MVC mapping annotations", r"@(RequestMapping|GetMapping|PostMapping|PutMapping|DeleteMapping)\b"),
            ("request_binding", "Request-bound parameters/body in controller methods", r"@(RequestParam|PathVariable|RequestBody|RequestHeader|CookieValue)\b"),
            ("servlet_request", "Direct servlet request access", r"\b(HttpServletRequest|getParameter\s*\(|getHeader\s*\(|getQueryString\s*\()"),
            ("multipart_upload", "Multipart/file upload input points", r"\b(MultipartFile|Part\s+|getPart\s*\(|getParts\s*\()"),
        ],
        "sinks": [
            ("jdbc_execution", "Dynamic SQL execution APIs", r"\b(createStatement\s*\(|prepareStatement\s*\(|JdbcTemplate\.(query|update|execute)\s*\()"),
            ("mybatis_dollar", "MyBatis `${}` string interpolation", r"\$\{[^}]+\}"),
            ("command_exec", "OS command execution APIs", r"\b(Runtime\.getRuntime\(\)\.exec|ProcessBuilder\s*\()"),
            ("file_access", "Filesystem APIs used as sensitive sinks", r"\b(new\s+File\s*\(|Paths\.get\s*\(|Files\.(read|write|copy|move|delete))"),
            ("ssrf_network", "Outbound HTTP/network APIs", r"\b(new\s+URL\s*\(|RestTemplate|WebClient|HttpClient|OkHttpClient)"),
            ("unsafe_deser", "Java deserialization APIs", r"\b(ObjectInputStream|readObject\s*\()"),
            ("template_eval", "Template/EL expression evaluation", r"\b(ExpressionParser|SpelExpressionParser|TemplateEngine|parseExpression\s*\()"),
        ],
        "sanitizers": [
            ("bean_validation", "Bean validation annotations", r"@(Valid|Validated|NotNull|NotBlank|Size|Pattern|Email|Min|Max)\b"),
            ("prepared_stmt_usage", "PreparedStatement parameter binding", r"\bPreparedStatement\b|\.\s*set(Int|Long|String|Object|Boolean)\s*\("),
            ("path_canonicalization", "Path canonicalization checks", r"\b(getCanonicalPath\s*\(|normalize\s*\(|toRealPath\s*\()"),
            ("escaping_utils", "Escaping utility methods", r"\b(StringEscapeUtils|HtmlUtils\.htmlEscape|Encode\.forHtml|ESAPI)"),
            ("allowlist_checks", "Allowlist/whitelist style checks", r"\b(allowlist|whitelist|isAllowed|isSafeInput)\b"),
        ],
    },
    "python-web": {
        "suffixes": {".py", ".jinja", ".jinja2", ".html", ".yaml", ".yml", ".toml"},
        "sources": [
            ("flask_request", "Flask request data sources", r"\b(request\.(args|form|values|json|data|headers|cookies)|get_json\s*\()"),
            ("django_request", "Django request data sources", r"\b(request\.(GET|POST|body|META|FILES)|QueryDict\b)"),
            ("fastapi_params", "FastAPI request parameter sources", r"\b(Query|Body|Path|Header|Cookie|Form|File)\s*\("),
            ("url_params", "Route/path parameter extraction", r"\b(kwargs\.get\s*\(|path_params|request\.path_params|request\.query_params)"),
        ],
        "sinks": [
            ("sql_execution", "Raw SQL execution APIs", r"\b(cursor\.execute|cursor\.executemany|raw\s*\(|extra\s*\(|text\s*\()"),
            ("command_exec", "OS command execution APIs", r"\b(os\.system|subprocess\.(run|Popen|call|check_output|check_call))"),
            ("file_access", "Filesystem APIs used as sensitive sinks", r"\b(open\s*\(|Path\s*\(|send_file\s*\(|FileResponse\s*\(|shutil\.(copy|move|rmtree))"),
            ("ssrf_network", "Outbound HTTP/network APIs", r"\b(requests\.(get|post|put|delete|request)|httpx\.(get|post|put|delete|request)|urllib\.request\.urlopen)"),
            ("unsafe_deser", "Unsafe deserialization APIs", r"\b(pickle\.loads|yaml\.load\s*\()"),
            ("template_eval", "Template rendering / code eval sinks", r"\b(render_template_string|jinja2\.Template|mark_safe|eval\s*\(|exec\s*\()"),
        ],
        "sanitizers": [
            ("pydantic_validation", "Pydantic model validation", r"\b(BaseModel|Field\s*\(|model_validate\s*\()"),
            ("django_forms_validation", "Django form/serializer validation", r"\b(is_valid\s*\(|cleaned_data|Serializer\b|validate_[a-zA-Z0-9_]+\s*\()"),
            ("parameterized_sql", "Parameterized SQL execution patterns", r"\bexecute\s*\(\s*[^,\n]+,\s*[^)\n]+\)"),
            ("escaping_utils", "Escaping/filtering utility methods", r"\b(bleach\.clean|markupsafe\.escape|django\.utils\.html\.escape)"),
            ("path_canonicalization", "Path canonicalization checks", r"\b(resolve\s*\(|os\.path\.realpath\s*\(|normpath\s*\()"),
        ],
    },
}


def find_project_root(start: Path) -> Path:
    for candidate in [start, *start.parents]:
        if (candidate / "qlcoder" / "cli.py").exists():
            return candidate
    raise SystemExit(f"Could not find a qlcoder project root from {start}")


def run(cmd: list[str], cwd: Path) -> str:
    proc = subprocess.run(cmd, cwd=str(cwd), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if proc.returncode != 0:
        raise SystemExit(proc.stderr or proc.stdout)
    return proc.stdout.strip()


def write_json(path: Path, payload: Dict[str, object]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def should_skip(path: Path) -> bool:
    return any(part in SKIP_DIRS for part in path.parts)


def normalize_rel(path: str) -> str:
    return path.replace("\\", "/")


def contains_noise_path(rel_path: str) -> bool:
    lower = normalize_rel(rel_path).lower()
    return any(marker in lower for marker in NOISE_PATH_MARKERS)


def should_record_hit(profile_name: str, kind: str, rule_id: str, rel_path: str, line_text: str) -> bool:
    rel_lower = normalize_rel(rel_path).lower()
    if contains_noise_path(rel_lower):
        return False

    if profile_name == "java-web" and kind == "sinks" and rule_id == "mybatis_dollar":
        # Keep `${...}` only in MyBatis mapper SQL context; drop pom/logback/property placeholders.
        if not rel_lower.endswith(".xml"):
            return False
        if "/mapper/" not in rel_lower:
            return False
        if rel_lower.endswith("/pom.xml") or rel_lower.endswith("/logback.xml"):
            return False
        if "<version>" in line_text.lower():
            return False

    return True


def detect_profiles(repo_path: Path, app_profile: str) -> Tuple[List[str], Dict[str, int]]:
    if app_profile != "auto":
        return [app_profile], {"java_files": 0, "python_files": 0}

    java_files = 0
    python_files = 0
    for path in repo_path.rglob("*"):
        if not path.is_file() or should_skip(path):
            continue
        suffix = path.suffix.lower()
        if suffix == ".java":
            java_files += 1
        elif suffix == ".py":
            python_files += 1
        if java_files + python_files >= 2000:
            break

    if java_files and python_files:
        profiles = ["java-web", "python-web"]
    elif python_files:
        profiles = ["python-web"]
    else:
        profiles = ["java-web"]
    return profiles, {"java_files": java_files, "python_files": python_files}


def compile_rules(rule_specs: Sequence[Tuple[str, str, str]]) -> List[Tuple[str, str, re.Pattern[str]]]:
    return [(rule_id, desc, re.compile(pattern, re.IGNORECASE)) for rule_id, desc, pattern in rule_specs]


def scan_profile(repo_path: Path, profile_name: str) -> Dict[str, object]:
    profile = PROFILE_LIBRARY[profile_name]
    suffixes = set(profile["suffixes"])
    compiled_rules = {
        "sources": compile_rules(profile["sources"]),
        "sinks": compile_rules(profile["sinks"]),
        "sanitizers": compile_rules(profile["sanitizers"]),
    }
    hits_by_kind: Dict[str, List[Dict[str, object]]] = defaultdict(list)
    file_count = 0

    for path in repo_path.rglob("*"):
        if not path.is_file() or should_skip(path):
            continue
        if path.suffix.lower() not in suffixes:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        rel = str(path.relative_to(repo_path))
        file_count += 1
        lines = text.splitlines()
        for idx, line in enumerate(lines, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            for kind, rules in compiled_rules.items():
                for rule_id, desc, pattern in rules:
                    if pattern.search(stripped):
                        if not should_record_hit(profile_name, kind, rule_id, rel, stripped):
                            continue
                        hits_by_kind[kind].append(
                            {
                                "rule_id": rule_id,
                                "rule_description": desc,
                                "file": rel,
                                "line": idx,
                                "code": stripped[:300],
                            }
                        )

    def aggregate(kind: str) -> List[Dict[str, object]]:
        bucket: Dict[str, Dict[str, object]] = {}
        for rule_id, desc, _ in compiled_rules[kind]:
            bucket[rule_id] = {
                "type": rule_id,
                "description": desc,
                "count": 0,
                "evidence": [],
            }
        for hit in hits_by_kind[kind]:
            item = bucket[hit["rule_id"]]
            item["count"] += 1
            if len(item["evidence"]) < 8:
                item["evidence"].append(
                    {
                        "file": hit["file"],
                        "line": hit["line"],
                        "code": hit["code"],
                    }
                )
        return [item for item in sorted(bucket.values(), key=lambda x: x["count"], reverse=True) if item["count"] > 0]

    return {
        "profile": profile_name,
        "files_scanned": file_count,
        "source_types": aggregate("sources"),
        "sink_types": aggregate("sinks"),
        "sanitizer_types": aggregate("sanitizers"),
    }


def build_taint_profile_report(repo_path: Path, app_profile: str) -> Dict[str, object]:
    profiles, detector_stats = detect_profiles(repo_path, app_profile)
    profile_reports = [scan_profile(repo_path, profile) for profile in profiles]

    source_count = sum(sum(item["count"] for item in report["source_types"]) for report in profile_reports)
    sink_count = sum(sum(item["count"] for item in report["sink_types"]) for report in profile_reports)
    sanitizer_count = sum(sum(item["count"] for item in report["sanitizer_types"]) for report in profile_reports)
    return {
        "mode": "pure-llm-taint-profile",
        "target_repo_path": str(repo_path),
        "selected_profiles": profiles,
        "auto_detection": detector_stats,
        "summary": {
            "source_hits": source_count,
            "sink_hits": sink_count,
            "sanitizer_hits": sanitizer_count,
        },
        "profile_reports": profile_reports,
        "limitations": [
            "This report is pattern-based static scanning, not full dataflow proof.",
            "Counts indicate candidates and should be validated with manual trace or deeper tooling.",
        ],
    }


def report_to_markdown(payload: Dict[str, object]) -> str:
    lines = [
        "# Multi-Profile Taint Flow Report",
        "",
        f"Target: {payload['target_repo_path']}",
        f"Profiles: {', '.join(payload['selected_profiles'])}",
        "",
        "## Summary",
        f"- Source hits: {payload['summary']['source_hits']}",
        f"- Sink hits: {payload['summary']['sink_hits']}",
        f"- Sanitizer hits: {payload['summary']['sanitizer_hits']}",
        "",
    ]

    for report in payload["profile_reports"]:
        lines.append(f"## Profile: {report['profile']}")
        lines.append(f"- Files scanned: {report['files_scanned']}")
        lines.append("")
        lines.append("### Source Types")
        if report["source_types"]:
            for item in report["source_types"]:
                lines.append(f"- `{item['type']}` ({item['count']}): {item['description']}")
                for evidence in item["evidence"][:3]:
                    lines.append(f"  - {evidence['file']}:{evidence['line']} {evidence['code']}")
        else:
            lines.append("- No source hits.")
        lines.append("")
        lines.append("### Sink Types")
        if report["sink_types"]:
            for item in report["sink_types"]:
                lines.append(f"- `{item['type']}` ({item['count']}): {item['description']}")
                for evidence in item["evidence"][:3]:
                    lines.append(f"  - {evidence['file']}:{evidence['line']} {evidence['code']}")
        else:
            lines.append("- No sink hits.")
        lines.append("")
        lines.append("### Sanitizer Types")
        if report["sanitizer_types"]:
            for item in report["sanitizer_types"]:
                lines.append(f"- `{item['type']}` ({item['count']}): {item['description']}")
                for evidence in item["evidence"][:3]:
                    lines.append(f"  - {evidence['file']}:{evidence['line']} {evidence['code']}")
        else:
            lines.append("- No sanitizer hits.")
        lines.append("")

    lines.append("## Limitations")
    for limitation in payload["limitations"]:
        lines.append(f"- {limitation}")
    lines.append("")
    return "\n".join(lines)


def write_taint_profile_artifacts(repo_path: Path, run_root: Path, app_profile: str) -> Tuple[Path, Path, Dict[str, object]]:
    payload = build_taint_profile_report(repo_path, app_profile)
    json_path = run_root / "taint_profile.analysis.json"
    md_path = run_root / "taint_profile.analysis.md"
    write_json(json_path, payload)
    md_path.write_text(report_to_markdown(payload), encoding="utf-8")
    return json_path, md_path, payload


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def first_line_no(path: Path, needle: str) -> int | None:
    text = read_text(path)
    if not text:
        return None
    for idx, line in enumerate(text.splitlines(), start=1):
        if needle in line:
            return idx
    return None


def collect_line_hits(path: Path, regex: re.Pattern[str], rel_path: str, limit: int = 6) -> List[Dict[str, object]]:
    hits: List[Dict[str, object]] = []
    text = read_text(path)
    if not text:
        return hits
    for idx, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if not stripped:
            continue
        if regex.search(stripped):
            hits.append({"file": rel_path, "line": idx, "code": stripped[:300]})
            if len(hits) >= limit:
                break
    return hits


def collect_pattern_hits(
    repo_path: Path,
    suffixes: set[str],
    pattern: re.Pattern[str],
    include_paths: Sequence[str] | None = None,
    exclude_paths: Sequence[str] | None = None,
    limit: int = 20,
) -> List[Dict[str, object]]:
    include_paths = include_paths or []
    exclude_paths = exclude_paths or []
    hits: List[Dict[str, object]] = []
    for path in repo_path.rglob("*"):
        if not path.is_file() or should_skip(path):
            continue
        if path.suffix.lower() not in suffixes:
            continue
        rel = normalize_rel(str(path.relative_to(repo_path)))
        rel_lower = rel.lower()
        if include_paths and not any(token in rel_lower for token in include_paths):
            continue
        if any(token in rel_lower for token in exclude_paths):
            continue
        if contains_noise_path(rel):
            continue
        for hit in collect_line_hits(path, pattern, rel_path=rel, limit=max(1, limit - len(hits))):
            hits.append(hit)
            if len(hits) >= limit:
                return hits
    return hits


def detect_xss_finding(repo_path: Path) -> Dict[str, object] | None:
    notice_view = repo_path / "ruoyi-admin" / "src" / "main" / "resources" / "templates" / "system" / "notice" / "view.html"
    if not notice_view.exists():
        return None
    rel_notice = normalize_rel(str(notice_view.relative_to(repo_path)))
    notice_hits = collect_line_hits(notice_view, re.compile(r"th:utext\s*="), rel_notice, limit=4)
    if not notice_hits:
        return None

    app_yml = repo_path / "ruoyi-admin" / "src" / "main" / "resources" / "application.yml"
    app_text = read_text(app_yml)
    has_notice_exclude = "/system/notice/*" in app_text
    has_xss_enabled = bool(re.search(r"(?ms)^xss:\s*\n(?:[ \t].*\n)*?[ \t]+enabled:\s*true\b", app_text))

    evidence = list(notice_hits)
    if app_yml.exists():
        rel_yml = normalize_rel(str(app_yml.relative_to(repo_path)))
        line = first_line_no(app_yml, "excludes:")
        if line is not None:
            evidence.append({"file": rel_yml, "line": line, "code": "xss excludes configuration"})

    notice_controller = repo_path / "ruoyi-admin" / "src" / "main" / "java" / "com" / "ruoyi" / "web" / "controller" / "system" / "SysNoticeController.java"
    if notice_controller.exists():
        rel_ctrl = normalize_rel(str(notice_controller.relative_to(repo_path)))
        for needle in ('@PostMapping("/add")', '@PostMapping("/edit")'):
            line = first_line_no(notice_controller, needle)
            if line is not None:
                evidence.append({"file": rel_ctrl, "line": line, "code": needle})

    severity = "high" if has_notice_exclude and has_xss_enabled else "medium"
    confidence = "high" if has_notice_exclude else "medium"
    summary = (
        "noticeContent is rendered via th:utext; request-side XSS filtering is weakened by current notice exclude policy."
        if has_notice_exclude
        else "noticeContent is rendered via th:utext and may allow stored XSS if upstream sanitization is bypassed."
    )
    return {
        "id": "xss-notice-content",
        "category": "xss",
        "severity": severity,
        "confidence": confidence,
        "title": "Potential stored XSS in notice content rendering",
        "summary": summary,
        "evidence": evidence[:10],
        "recommendations": [
            "Prefer escaped rendering (th:text) or strict HTML allowlist sanitization before persistence.",
            "Re-evaluate xss.excludes for /system/notice/* and avoid broad exclusions for rich-text endpoints.",
        ],
    }


def detect_broken_access_control_finding(repo_path: Path) -> Dict[str, object] | None:
    controller_root = repo_path / "ruoyi-admin" / "src" / "main" / "java" / "com" / "ruoyi" / "web" / "controller"
    if not controller_root.exists():
        return None

    exposures: List[Dict[str, object]] = []
    for path in controller_root.rglob("*.java"):
        rel = normalize_rel(str(path.relative_to(repo_path)))
        rel_lower = rel.lower()
        text = read_text(path)
        if not text:
            continue
        if not MAPPING_ANNOTATION_RE.search(text):
            continue
        if PERMISSION_ANNOTATION_RE.search(text):
            continue
        if "/demo/" not in rel_lower and not rel_lower.endswith("/testcontroller.java"):
            continue
        line = first_line_no(path, "@RequestMapping(") or first_line_no(path, "@GetMapping(") or 1
        exposures.append({"file": rel, "line": line, "code": "controller endpoint without explicit permission annotation"})
        if len(exposures) >= 12:
            break

    if not exposures:
        return None

    shiro_config = repo_path / "ruoyi-framework" / "src" / "main" / "java" / "com" / "ruoyi" / "framework" / "config" / "ShiroConfig.java"
    if shiro_config.exists():
        line = first_line_no(shiro_config, 'filterChainDefinitionMap.put("/**", "user')
        if line is not None:
            exposures.append(
                {
                    "file": normalize_rel(str(shiro_config.relative_to(repo_path))),
                    "line": line,
                    "code": 'global auth chain requires only authenticated user on "/**"',
                }
            )

    return {
        "id": "bac-demo-test-endpoints",
        "category": "broken-access-control",
        "severity": "medium",
        "confidence": "medium",
        "title": "Demo/Test controllers expose endpoints without fine-grained permission checks",
        "summary": "Several demo/test controllers define mapped endpoints without @RequiresPermissions/@RequiresRoles guards.",
        "evidence": exposures,
        "recommendations": [
            "Disable demo/test controllers in production profiles.",
            "Apply explicit permission annotations to mutable or sensitive demo/test endpoints.",
        ],
    }


def detect_sqli_findings(repo_path: Path) -> List[Dict[str, object]]:
    findings: List[Dict[str, object]] = []

    dynamic_sql_hits = collect_pattern_hits(
        repo_path,
        suffixes={".xml"},
        pattern=re.compile(r"\$\{sql\}", re.IGNORECASE),
        include_paths=["/mapper/"],
        limit=6,
    )
    if dynamic_sql_hits:
        gen_controller = repo_path / "ruoyi-generator" / "src" / "main" / "java" / "com" / "ruoyi" / "generator" / "controller" / "GenController.java"
        controller_rel = normalize_rel(str(gen_controller.relative_to(repo_path))) if gen_controller.exists() else ""
        role_line = first_line_no(gen_controller, '@RequiresRoles("admin")') if gen_controller.exists() else None
        filter_line = first_line_no(gen_controller, "SqlUtil.filterKeyword(sql)") if gen_controller.exists() else None

        evidence = list(dynamic_sql_hits)
        if role_line is not None:
            evidence.append({"file": controller_rel, "line": role_line, "code": '@RequiresRoles("admin")'})
        if filter_line is not None:
            evidence.append({"file": controller_rel, "line": filter_line, "code": "SqlUtil.filterKeyword(sql)"})

        guarded = role_line is not None and filter_line is not None
        findings.append(
            {
                "id": "sqli-dynamic-sql-generator",
                "category": "sql-injection",
                "severity": "low" if guarded else "high",
                "confidence": "medium",
                "title": "Dynamic SQL sink `${sql}` in generator mapper",
                "summary": "Raw `${sql}` execution exists; current path appears partially guarded but remains a sensitive sink.",
                "evidence": evidence[:10],
                "recommendations": [
                    "Replace `${sql}` execution with structured DDL builders where possible.",
                    "Keep strict parser/allowlist checks around CREATE TABLE flow.",
                ],
            }
        )

    data_scope_hits = collect_pattern_hits(
        repo_path,
        suffixes={".xml"},
        pattern=re.compile(r"\$\{params\.dataScope\}", re.IGNORECASE),
        include_paths=["/mapper/"],
        limit=8,
    )
    if data_scope_hits:
        aspect_path = repo_path / "ruoyi-framework" / "src" / "main" / "java" / "com" / "ruoyi" / "framework" / "aspectj" / "DataScopeAspect.java"
        aspect_rel = normalize_rel(str(aspect_path.relative_to(repo_path))) if aspect_path.exists() else ""
        clear_line = first_line_no(aspect_path, 'baseEntity.getParams().put(DATA_SCOPE, "")') if aspect_path.exists() else None
        build_line = first_line_no(aspect_path, 'baseEntity.getParams().put(DATA_SCOPE, " AND (') if aspect_path.exists() else None
        evidence = list(data_scope_hits)
        if clear_line is not None:
            evidence.append({"file": aspect_rel, "line": clear_line, "code": 'params.dataScope is cleared before rebuild'})
        if build_line is not None:
            evidence.append({"file": aspect_rel, "line": build_line, "code": "params.dataScope is rebuilt from role scope"})

        findings.append(
            {
                "id": "sqli-datascope-fragment",
                "category": "sql-injection",
                "severity": "low",
                "confidence": "medium",
                "title": "`${params.dataScope}` sink requires policy-aware review",
                "summary": "Mapper uses `${params.dataScope}` but repository includes explicit clear-and-rebuild guard in DataScopeAspect.",
                "evidence": evidence[:10],
                "recommendations": [
                    "Preserve clearDataScope + controlled rebuild pattern in DataScopeAspect.",
                    "Avoid introducing request-controlled params.dataScope assignment outside aspect flow.",
                ],
            }
        )

    return findings


def build_security_findings(repo_path: Path, taint_payload: Dict[str, object]) -> Dict[str, object]:
    findings: List[Dict[str, object]] = []
    xss_finding = detect_xss_finding(repo_path)
    if xss_finding:
        findings.append(xss_finding)
    bac_finding = detect_broken_access_control_finding(repo_path)
    if bac_finding:
        findings.append(bac_finding)
    findings.extend(detect_sqli_findings(repo_path))

    severity_order = {"high": 0, "medium": 1, "low": 2}
    findings.sort(key=lambda item: severity_order.get(str(item.get("severity", "low")).lower(), 99))
    summary = {
        "finding_count": len(findings),
        "high": sum(1 for item in findings if item.get("severity") == "high"),
        "medium": sum(1 for item in findings if item.get("severity") == "medium"),
        "low": sum(1 for item in findings if item.get("severity") == "low"),
    }
    return {
        "mode": "pure-llm-taint-findings",
        "target_repo_path": str(repo_path),
        "selected_profiles": taint_payload.get("selected_profiles", []),
        "taint_summary": taint_payload.get("summary", {}),
        "summary": summary,
        "findings": findings,
        "limitations": [
            "This is static triage output; exploitation still requires environment-specific verification.",
            "Severity/confidence are heuristic and should be validated by reviewer and test cases.",
        ],
    }


def findings_to_markdown(payload: Dict[str, object]) -> str:
    lines = [
        "# Taintflow Security Findings",
        "",
        f"Target: {payload['target_repo_path']}",
        f"Profiles: {', '.join(payload.get('selected_profiles', [])) or 'unknown'}",
        "",
        "## Summary",
        f"- Findings: {payload['summary']['finding_count']}",
        f"- High: {payload['summary']['high']}",
        f"- Medium: {payload['summary']['medium']}",
        f"- Low: {payload['summary']['low']}",
        "",
    ]

    for finding in payload.get("findings", []):
        lines.append(f"## {finding['title']}")
        lines.append(f"- ID: {finding['id']}")
        lines.append(f"- Category: {finding['category']}")
        lines.append(f"- Severity: {finding['severity']}")
        lines.append(f"- Confidence: {finding['confidence']}")
        lines.append(f"- Summary: {finding['summary']}")
        lines.append("- Evidence:")
        for ev in finding.get("evidence", [])[:8]:
            lines.append(f"  - {ev['file']}:{ev['line']} {ev['code']}")
        lines.append("- Recommendations:")
        for rec in finding.get("recommendations", []):
            lines.append(f"  - {rec}")
        lines.append("")

    lines.append("## Limitations")
    for limitation in payload.get("limitations", []):
        lines.append(f"- {limitation}")
    lines.append("")
    return "\n".join(lines)


def write_security_findings_artifacts(
    repo_path: Path, run_root: Path, taint_payload: Dict[str, object]
) -> Tuple[Path, Path]:
    payload = build_security_findings(repo_path, taint_payload)
    json_path = run_root / "taint_findings.analysis.json"
    md_path = run_root / "taint_findings.analysis.md"
    write_json(json_path, payload)
    md_path.write_text(findings_to_markdown(payload), encoding="utf-8")
    return json_path, md_path


def run_local_repo_mode(project_root: Path, repo_path: Path, analysis_name: str | None, app_profile: str) -> None:
    cmd = [
        sys.executable,
        "-m",
        "qlcoder.cli",
        "run-local-pure-llm",
        "--repo-path",
        str(repo_path),
    ]
    if analysis_name:
        cmd += ["--analysis-name", analysis_name]

    output = run(cmd, cwd=project_root)
    print(output)

    lines = [line.strip() for line in output.splitlines() if line.strip()]
    if not lines:
        return

    analysis_json_path = Path(lines[0])
    if not analysis_json_path.is_absolute():
        analysis_json_path = (project_root / analysis_json_path).resolve()
    run_root = analysis_json_path.parent
    taint_json_path, taint_md_path, taint_payload = write_taint_profile_artifacts(repo_path.resolve(), run_root, app_profile)
    findings_json_path, findings_md_path = write_security_findings_artifacts(repo_path.resolve(), run_root, taint_payload)
    print(str(taint_json_path))
    print(str(taint_md_path))
    print(str(findings_json_path))
    print(str(findings_md_path))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", type=Path, default=Path.cwd())
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--project-slug")
    parser.add_argument("--build-base-manifest", action="store_true")
    parser.add_argument("--batch-limit", type=int)
    parser.add_argument("--repo-path", type=Path, help="Run local Web App pure-LLM analysis on this repository path.")
    parser.add_argument("--analysis-name", help="Optional custom run name for local repo mode.")
    parser.add_argument(
        "--app-profile",
        choices=["auto", "java-web", "python-web"],
        default="auto",
        help="Taint profile for local repo source/sink/sanitizer typing.",
    )
    args = parser.parse_args()

    project_root = find_project_root(args.workspace.resolve())
    if args.repo_path:
        run_local_repo_mode(project_root, args.repo_path.resolve(), args.analysis_name, args.app_profile)
        return

    manifest = args.manifest or project_root / "datasets" / "manifests" / "qlcoder_base_111.csv"
    if args.build_base_manifest or not manifest.exists():
        manifest = Path(
            run(
                [
                    sys.executable,
                    "-m",
                    "qlcoder.cli",
                    "build-manifest",
                    "--base-only",
                    "--allow-manual-override",
                    "--manual-base-ref",
                    "master",
                ],
                cwd=project_root,
            ).splitlines()[-1]
        )

    if args.batch_limit:
        output = run(
            [
                sys.executable,
                "-m",
                "qlcoder.cli",
                "run-manifest-pure-llm",
                "--manifest",
                str(manifest),
                "--limit",
                str(args.batch_limit),
            ],
            cwd=project_root,
        )
        print(output)
        return

    project_slug = args.project_slug
    if not project_slug:
        project_slug = run(
            [
                sys.executable,
                "-m",
                "qlcoder.cli",
                "choose-seed",
                "--manifest",
                str(manifest),
            ],
            cwd=project_root,
        ).splitlines()[-1]

    output = run(
        [
            sys.executable,
            "-m",
            "qlcoder.cli",
            "run-one-pure-llm",
            "--project-slug",
            project_slug,
            "--manifest",
            str(manifest),
        ],
        cwd=project_root,
    )
    print(output)


if __name__ == "__main__":
    main()
