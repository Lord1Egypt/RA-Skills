#!/usr/bin/env python3
import json
import re
from pathlib import Path


PACKAGE_DIR = Path("<research-root>/example-web-capture-evaluation-20260616/workspace/outputs/web-capture-evaluation")
OUT_PATH = Path("<research-root>/example-web-capture-evaluation-20260616/workspace/analysis/verify-package-report.json")

REQUIRED_FILES = [
    "README.md",
    "prompt.md",
    "research-plan.md",
    "sources.md",
    "final-report.md",
]

PRIVATE_PATTERNS = {
    "home_path": re.compile(r"<absolute-home-path>/|<tmp-research-root>"),
    "private_user": re.compile(r"<user>|<personal-name>|<personal-name>|<personal-name>|личн|персональн", re.I),
    "messaging_ids": re.compile(r"chat_id|thread_id|topic_id|chat-system|chat-system|chat-system", re.I),
    "local_only_tool": re.compile(r"OpenClaw|research_mode\.py|pinchtab|claw-helper", re.I),
    "secret_literal": re.compile(r"(api[_-]?key|password|bearer\s+[a-z0-9._-]+|(?<![a-z0-9])sk-[a-z0-9]{8,})", re.I),
    "cyrillic_text": re.compile(r"[\u0400-\u04ff]"),
}

COVERAGE_TERMS = {
    "risks_permission_politeness": ["robots", "politeness", "authorization"],
    "risks_request_safety": ["safe read-only HTTP methods", "redirect", "timeout", "byte"],
    "risks_url_network": ["scheme", "host", "internal", "private", "redirect"],
    "risks_conversion_markdown": ["Markdown conversion is not sanitization", "untrusted text"],
    "risks_prompt_injection": ["embedded instructions", "reveal secrets", "tool"],
    "workflow_intake": ["Intake"],
    "workflow_preflight": ["Preflight"],
    "workflow_fetch": ["Fetch"],
    "workflow_convert": ["Convert"],
    "workflow_analyze": ["Analyze"],
    "workflow_synthesize": ["Synthesize"],
    "workflow_verify": ["Verify"],
    "artifacts_source_log": ["Source log"],
    "artifacts_fetch_metadata": ["Fetch metadata"],
    "artifacts_converted_markdown": ["Converted Markdown"],
    "artifacts_analysis_notes": ["Analysis notes"],
    "artifacts_final_report": ["Final report"],
    "provider_neutral": ["provider-neutral", "converter-neutral"],
}

SOURCE_URLS = [
    "https://datatracker.ietf.org/doc/html/rfc9309",
    "https://datatracker.ietf.org/doc/html/rfc9110",
    "https://docs.python.org/3/library/urllib.parse.html",
    "https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html",
    "https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html",
    "https://spec.commonmark.org/0.31.2/",
    "https://github.com/microsoft/markitdown",
]


def main() -> None:
    files = {}
    missing = []
    for name in REQUIRED_FILES:
        path = PACKAGE_DIR / name
        if not path.exists():
            missing.append(name)
            continue
        files[name] = path.read_text(encoding="utf-8")

    combined = "\n\n".join(files.values())
    privacy_issues = []
    for name, text in files.items():
        for pattern_name, pattern in PRIVATE_PATTERNS.items():
            for match in pattern.finditer(text):
                privacy_issues.append(
                    {
                        "file": name,
                        "pattern": pattern_name,
                        "match": match.group(0)[:80],
                    }
                )

    coverage = {}
    for requirement, terms in COVERAGE_TERMS.items():
        coverage[requirement] = {
            "passed": all(term.lower() in combined.lower() for term in terms),
            "terms": terms,
        }

    source_text = files.get("sources.md", "")
    source_coverage = {
        "expected_count": len(SOURCE_URLS),
        "present": [url for url in SOURCE_URLS if url in source_text],
        "missing": [url for url in SOURCE_URLS if url not in source_text],
    }

    report = {
        "package_dir": str(PACKAGE_DIR),
        "required_files": REQUIRED_FILES,
        "missing_files": missing,
        "privacy_issues": privacy_issues,
        "coverage": coverage,
        "source_coverage": source_coverage,
        "passed": (
            not missing
            and not privacy_issues
            and all(item["passed"] for item in coverage.values())
            and not source_coverage["missing"]
        ),
    }
    OUT_PATH.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
