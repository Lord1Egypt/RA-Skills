"""Deterministic heuristic security scanning for Skill bundles."""

import re
from pathlib import Path

from .util import norm


SELF_SKILL_ROOT = Path(__file__).resolve().parent.parent.parent

SECURITY_PATTERNS = [
    ("adversarial_instruction", "critical", re.compile(
        r"(ignore\s+(all\s+)?previous|disregard\s+(all\s+)?prior|"
        r"忽略(之前|先前|上述)|无视(之前|先前)|"
        r"do\s+not\s+(tell|inform|mention\s+to)\s+the\s+user|不要告诉用户)", re.I)),
    ("pipe_to_shell", "critical", re.compile(
        r"(curl|wget)[^\n|]{0,200}\|\s*(ba)?sh", re.I)),
    ("base64_exec", "critical", re.compile(
        r"base64\s+(-d|--decode)[^\n]{0,80}\|\s*(ba)?sh", re.I)),
    ("raw_ip_fetch", "high", re.compile(
        r"(curl|wget|fetch)[^\n]{0,80}https?://\d{1,3}(\.\d{1,3}){3}", re.I)),
    ("password_archive", "high", re.compile(
        r"(unzip\s+-P|7z[a-z]*\s+x?\s*-p\S|openssl\s+enc\s+-\S*d)", re.I)),
    ("hardcoded_secret", "high", re.compile(
        r"(sk-[A-Za-z0-9]{16,}|ghp_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{12,}|"
        r"xoxb-[0-9A-Za-z-]{10,})")),
    ("credential_env_read", "medium", re.compile(
        r"(cat|grep|cp)\s+[^\n]{0,60}(\.env|\.aws/credentials|\.ssh/id_|"
        r"\.npmrc|\.netrc)", re.I)),
    ("obfuscated_exec", "medium", re.compile(
        r"(eval\s*\(\s*(atob|base64)|exec\s*\(\s*(atob|base64)|"
        r"\bchr\(\d+\)\s*\+)", re.I)),
]

CITATION_HINTS = re.compile(
    r"(re\.compile|regex|正则|例如|举例|比如|这类|样例|"
    r"example|such as|e\.g\.|banned|forbidden|禁止|防御|抵御|注入|injection|"
    r"prompt\s*injection|attack|攻击|不要遵从|不得执行)", re.I)
OPEN_QUOTES = ("“", "「", "『")
URL_RE = re.compile(r"https?://[^\s\)\]\"'>]+")
EXEC_EXT = {".sh", ".py", ".js", ".ts", ".rb", ".pl", ".ps1", ".bat", ".zsh"}


def is_cited(line: str, matched: str) -> bool:
    """Return whether a match appears in a quotation or defensive example."""
    index = line.find(matched)
    if index < 0:
        return False
    before = line[:index]
    if any(before.count(quote) % 2 == 1 for quote in ('"', "'", "`")):
        return True
    if any(quote in before for quote in OPEN_QUOTES):
        return True
    return bool(CITATION_HINTS.search(line))


def security_scan(skill_dir: Path, skill_raw: str):
    """Scan SKILL.md and executable source files for review-worthy patterns."""
    findings, scanned_files = [], []

    try:
        if skill_dir.resolve() == SELF_SKILL_ROOT:
            return {
                "findings": [], "max_severity": "none",
                "max_severity_uncited": "none", "cited_count": 0,
                "all_findings_cited": False, "exec_scripts": [],
                "external_urls": [], "external_url_count": 0,
                "scanned_script_count": 0, "self_excluded": True,
            }
    except OSError:
        pass

    def check(text: str, where: str):
        lines = text.splitlines()
        for name, severity, pattern in SECURITY_PATTERNS:
            match = pattern.search(text)
            if not match:
                continue
            snippet = match.group(0)[:80].replace("\n", " ")
            line_no = text[:match.start()].count("\n") + 1
            line = lines[line_no - 1] if line_no <= len(lines) else ""
            findings.append({
                "rule": name,
                "severity": severity,
                "cited": is_cited(line, match.group(0)),
                "where": where,
                "line": line_no,
                "match": snippet,
            })

    check(skill_raw, "SKILL.md")

    exec_scripts = []
    for path in sorted(skill_dir.rglob("*"), key=norm):
        if not path.is_file() or path.name == "SKILL.md":
            continue
        if path.suffix.lower() in EXEC_EXT:
            relative = norm(path.relative_to(skill_dir))
            try:
                mode = path.stat().st_mode
            except OSError:
                mode = 0
            exec_scripts.append({"path": relative, "executable": bool(mode & 0o111)})
            try:
                check(path.read_text(encoding="utf-8", errors="replace"), relative)
                scanned_files.append(relative)
            except OSError:
                pass

    urls = sorted(set(URL_RE.findall(skill_raw)))
    external = [url for url in urls
                if not any(domain in url for domain in
                           ("localhost", "127.0.0.1", "example.com"))]

    seen, unique = set(), []
    for finding in findings:
        key = (finding["rule"], finding["where"])
        if key not in seen:
            seen.add(key)
            unique.append(finding)

    def worst(items):
        for level in ("critical", "high", "medium"):
            if any(item["severity"] == level for item in items):
                return level
        return "none"

    uncited = [finding for finding in unique if not finding["cited"]]
    return {
        "findings": unique,
        "max_severity": worst(unique),
        "max_severity_uncited": worst(uncited),
        "cited_count": len(unique) - len(uncited),
        "all_findings_cited": bool(unique) and not uncited,
        "exec_scripts": exec_scripts,
        "external_urls": external[:10],
        "external_url_count": len(external),
        "scanned_script_count": len(scanned_files),
    }
