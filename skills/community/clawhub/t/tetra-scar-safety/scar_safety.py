#!/usr/bin/env python3
"""scar_safety.py -- Agent safety that learns from incidents.

Reflex arc blocks repeat threats without LLM calls.
Single-file, zero external dependencies, Python 3.9+ stdlib only.

Two-layer safety:
  1. Built-in threat detection (regex/heuristic)
  2. Scar-based reflex arc (pattern-match against past incidents)

Severity levels:
  CRITICAL -- auto-block
  HIGH     -- warn + confirm
  MEDIUM   -- warn
  LOW      -- log

License: MIT-0
Author: B Button Corp (Tetra Genesis)
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

# ============================================================================
# Configuration
# ============================================================================

SCAR_FILENAME = "safety_scars.jsonl"
SEVERITIES = ("CRITICAL", "HIGH", "MEDIUM", "LOW")

# ============================================================================
# Built-in Threat Patterns
# ============================================================================

# Secret patterns: (regex, description)
_SECRET_PATTERNS: list[tuple[str, str]] = [
    # Generic API keys / tokens
    (r'(?i)(api[_-]?key|api[_-]?secret|access[_-]?token|auth[_-]?token'
     r'|secret[_-]?key|private[_-]?key)\s*[=:]\s*["\']?[A-Za-z0-9+/=_\-]{16,}',
     "API key or token assignment"),
    # AWS keys
    (r'AKIA[0-9A-Z]{16}', "AWS access key"),
    # GitHub tokens
    (r'gh[pousr]_[A-Za-z0-9_]{36,}', "GitHub token"),
    # Generic long hex/base64 secrets after common env var names
    (r'(?i)(DATABASE_URL|DB_PASSWORD|REDIS_URL|SECRET_KEY|JWT_SECRET'
     r'|PRIVATE_KEY|ENCRYPTION_KEY)\s*[=:]\s*\S{8,}',
     "sensitive environment variable"),
    # Private key blocks
    (r'-----BEGIN\s+(RSA\s+)?PRIVATE\s+KEY-----', "private key"),
    # Password in connection strings
    (r'(?i)password\s*[=:]\s*["\']?[^\s"\']{6,}', "password assignment"),
    # Bearer tokens
    (r'(?i)bearer\s+[A-Za-z0-9\-._~+/]+=*', "bearer token"),
]

# Dangerous commands: (pattern, description, severity)
_DANGEROUS_COMMANDS: list[tuple[str, str, str]] = [
    (r'\brm\s+(-[a-zA-Z]*f[a-zA-Z]*\s+|--force\s+)*-[a-zA-Z]*r[a-zA-Z]*',
     "dangerous command: rm -rf", "CRITICAL"),
    (r'\brm\s+(-[a-zA-Z]*r[a-zA-Z]*\s+|--recursive\s+)*-[a-zA-Z]*f',
     "dangerous command: rm -rf", "CRITICAL"),
    (r'(?i)\bdrop\s+(table|database|schema|index)\b',
     "dangerous SQL: DROP", "CRITICAL"),
    (r'(?i)\btruncate\s+table\b',
     "dangerous SQL: TRUNCATE TABLE", "CRITICAL"),
    (r'(?i)\bdelete\s+from\s+\S+\s*(;|$)',
     "dangerous SQL: DELETE FROM without WHERE", "HIGH"),
    (r'\bgit\s+push\s+.*--force\b',
     "force push", "HIGH"),
    (r'\bgit\s+push\s+-f\b',
     "force push", "HIGH"),
    (r'\bgit\s+reset\s+--hard\b',
     "git reset --hard", "HIGH"),
    (r'\bchmod\s+777\b',
     "chmod 777: world-writable", "HIGH"),
    (r'\bchmod\s+[0-7]*s',
     "chmod with setuid/setgid", "HIGH"),
    (r'\bmkfs\b',
     "filesystem format command", "CRITICAL"),
    (r'\bdd\s+if=',
     "dd raw disk write", "HIGH"),
    (r'>\s*/dev/sd[a-z]',
     "raw write to block device", "CRITICAL"),
    (r'(?i)\bformat\s+[a-zA-Z]:\s',
     "disk format command", "CRITICAL"),
]

# Injection patterns: (pattern, description, severity)
_INJECTION_PATTERNS: list[tuple[str, str, str]] = [
    (r'\beval\s*\(',
     "eval() call", "HIGH"),
    (r'\bexec\s*\(',
     "exec() call", "HIGH"),
    (r'\bos\.system\s*\(',
     "os.system() call", "MEDIUM"),
    (r'\bsubprocess\.(call|run|Popen)\s*\(\s*[^)\[]*\+',
     "subprocess with string concatenation", "HIGH"),
    (r'\bos\.popen\s*\(',
     "os.popen() call", "MEDIUM"),
    (r'(?i)\b__import__\s*\(',
     "dynamic import", "MEDIUM"),
    (r'\bcompile\s*\(.*\bexec\b',
     "compile+exec", "HIGH"),
]

# Data exfiltration patterns: (pattern, description, severity)
_EXFIL_PATTERNS: list[tuple[str, str, str]] = [
    (r'(?i)\bcurl\b.*\|\s*bash',
     "curl pipe to bash", "CRITICAL"),
    (r'(?i)\bwget\b.*\|\s*sh',
     "wget pipe to shell", "CRITICAL"),
    (r'(?i)\bcurl\s+.*(-d|--data)\s+.*(\$\(|`)',
     "curl POST with command substitution", "HIGH"),
    (r'(?i)\bbase64\b.*\b(key|secret|token|password|private)\b',
     "base64 encoding of secrets", "HIGH"),
    (r'(?i)\b(key|secret|token|password|private)\b.*\bbase64\b',
     "base64 encoding of secrets", "HIGH"),
    (r'(?i)\bcurl\s+(-X\s+POST\s+)?https?://[^/\s]*\.(ru|cn|tk|ml|ga|cf)\b',
     "data sent to suspicious TLD", "HIGH"),
]

# Privilege escalation patterns: (pattern, description, severity)
_PRIVESC_PATTERNS: list[tuple[str, str, str]] = [
    (r'\bsudo\s+',
     "sudo usage", "MEDIUM"),
    (r'\bchmod\s+[ugo]*\+s\b',
     "setuid/setgid bit", "HIGH"),
    (r'(?i)\b(docker|podman)\s+run\s+.*--privileged',
     "privileged container", "CRITICAL"),
    (r'(?i)\b(docker|podman)\s+run\s+.*--pid\s*=\s*host',
     "container with host PID namespace", "CRITICAL"),
    (r'(?i)\b(docker|podman)\s+run\s+.*--net\s*=\s*host',
     "container with host network", "HIGH"),
    (r'/etc/passwd',
     "/etc/passwd access", "MEDIUM"),
    (r'/etc/shadow',
     "/etc/shadow access", "HIGH"),
    (r'(?i)\bnsenter\b',
     "nsenter (namespace escape)", "HIGH"),
    (r'(?i)capsh\s+--print',
     "capability inspection", "MEDIUM"),
]


def _compile_patterns(
    patterns: list[tuple[str, str, str]],
) -> list[tuple[re.Pattern[str], str, str]]:
    """Compile regex patterns for efficiency."""
    return [(re.compile(p), desc, sev) for p, desc, sev in patterns]


_COMPILED_DANGEROUS = _compile_patterns(_DANGEROUS_COMMANDS)
_COMPILED_INJECTION = _compile_patterns(_INJECTION_PATTERNS)
_COMPILED_EXFIL = _compile_patterns(_EXFIL_PATTERNS)
_COMPILED_PRIVESC = _compile_patterns(_PRIVESC_PATTERNS)
_COMPILED_SECRETS = [(re.compile(p), desc) for p, desc in _SECRET_PATTERNS]


# ============================================================================
# JSONL helpers
# ============================================================================

def _read_jsonl(filepath: Path) -> list[dict]:
    """Read a JSONL file, skipping malformed lines."""
    if not filepath.exists():
        return []
    entries: list[dict] = []
    with open(filepath, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return entries


# ============================================================================
# Scar Memory -- Immutable. Append-only.
# ============================================================================

def load_safety_scars(scar_file: Optional[str] = None) -> list[dict]:
    """Load all safety scars from the JSONL file.

    Args:
        scar_file: Path to the scar file. Defaults to ./safety_scars.jsonl.

    Returns:
        List of scar dicts with keys: id, what_happened, never_allow,
        severity, created_at.
    """
    path = Path(scar_file) if scar_file else Path.cwd() / SCAR_FILENAME
    return _read_jsonl(path)


def record_incident(
    what_happened: str,
    never_allow: str,
    severity: str = "HIGH",
    scar_file: Optional[str] = None,
) -> dict:
    """Record a security incident as an immutable scar.

    Args:
        what_happened: Description of what went wrong.
        never_allow: The constraint to prevent recurrence.
        severity: One of CRITICAL, HIGH, MEDIUM, LOW.
        scar_file: Path to scar file. Defaults to ./safety_scars.jsonl.

    Returns:
        The recorded scar entry.
    """
    severity = severity.upper()
    if severity not in SEVERITIES:
        severity = "HIGH"

    path = Path(scar_file) if scar_file else Path.cwd() / SCAR_FILENAME
    path.parent.mkdir(parents=True, exist_ok=True)

    entry = {
        "id": f"scar_{int(time.time() * 1000)}",
        "what_happened": what_happened,
        "never_allow": never_allow,
        "severity": severity,
        "created_at": datetime.now().isoformat(),
    }
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry


# ============================================================================
# Reflex Arc -- Spinal reflex. No LLM. Pure pattern matching.
# ============================================================================

def _extract_keywords(text: str) -> list[str]:
    """Extract meaningful keywords from text (3+ char English words)."""
    words = re.findall(r'[a-zA-Z_]{3,}', text.lower())
    # Filter out very common stop words
    stop = frozenset([
        "the", "and", "for", "are", "but", "not", "you", "all",
        "can", "had", "her", "was", "one", "our", "out", "has",
        "that", "this", "with", "from", "have", "been", "will",
        "they", "then", "than", "them", "into", "also", "just",
        "never", "should", "would", "could", "about", "which",
        "when", "what", "there", "their", "allow", "without",
    ])
    return [w for w in words if w not in stop]


def reflex_block(
    action: str,
    scars: list[dict],
    threshold_ratio: float = 0.4,
    min_matches: int = 2,
) -> Optional[dict]:
    """Check if an action collides with any scar. No LLM needed.

    Uses keyword overlap between the action description and scar
    never_allow fields. Same algorithm as tetra_scar.py reflex_check.

    Args:
        action: The action description to check.
        scars: List of scar dicts from load_safety_scars().
        threshold_ratio: Fraction of keywords that must match.
        min_matches: Minimum number of keyword matches.

    Returns:
        Blocking scar dict with added 'matched_keywords' key if blocked,
        None if safe.
    """
    if not action or not scars:
        return None

    action_lower = action.lower()

    for scar in scars:
        never = scar.get("never_allow", "")
        if not never:
            continue

        keywords = _extract_keywords(never)
        if len(keywords) < 2:
            continue

        matches = [kw for kw in keywords if kw in action_lower]
        threshold = max(min_matches, int(len(keywords) * threshold_ratio))
        if len(matches) >= threshold:
            result = dict(scar)
            result["matched_keywords"] = matches
            return result

    return None


# ============================================================================
# Built-in Threat Detection
# ============================================================================

def _check_secrets(text: str) -> Optional[dict]:
    """Check for exposed secrets in text."""
    for pat, desc in _COMPILED_SECRETS:
        if pat.search(text):
            return {"severity": "CRITICAL", "reason": f"secret exposure: {desc}", "source": "builtin"}
    return None


def _check_patterns(
    text: str,
    compiled: list[tuple[re.Pattern[str], str, str]],
) -> Optional[dict]:
    """Check text against a list of compiled patterns."""
    for pat, desc, sev in compiled:
        if pat.search(text):
            return {"severity": sev, "reason": desc, "source": "builtin"}
    return None


def _severity_rank(sev: str) -> int:
    """Higher number = more severe."""
    return {"CRITICAL": 4, "HIGH": 3, "MEDIUM": 2, "LOW": 1}.get(sev, 0)


# ============================================================================
# Main Safety Check
# ============================================================================

def safety_check(
    action_description: str,
    scars: Optional[list[dict]] = None,
    scar_file: Optional[str] = None,
) -> dict:
    """Check if an action is safe based on built-in rules + scars.

    Args:
        action_description: Description of the action to check.
        scars: Pre-loaded scars. If None, loads from scar_file.
        scar_file: Path to scar file (used if scars is None).

    Returns:
        Dict with keys:
          safe: bool -- True if action is considered safe
          severity: str -- highest severity found (or "NONE")
          reason: str -- explanation
          source: str -- "builtin", "scar", or "none"
          details: list[dict] -- all findings
    """
    if not action_description or not action_description.strip():
        return {
            "safe": True,
            "severity": "NONE",
            "reason": "empty action",
            "source": "none",
            "details": [],
        }

    findings: list[dict] = []

    # Layer 1: Built-in threat detection
    secret_hit = _check_secrets(action_description)
    if secret_hit:
        findings.append(secret_hit)

    for compiled_list in (_COMPILED_DANGEROUS, _COMPILED_INJECTION,
                          _COMPILED_EXFIL, _COMPILED_PRIVESC):
        hit = _check_patterns(action_description, compiled_list)
        if hit:
            findings.append(hit)

    # Layer 2: Scar reflex arc
    if scars is None:
        scars = load_safety_scars(scar_file)

    blocked_scar = reflex_block(action_description, scars)
    if blocked_scar:
        findings.append({
            "severity": blocked_scar.get("severity", "HIGH"),
            "reason": (
                f"scar reflex: '{blocked_scar.get('never_allow', '')[:80]}' "
                f"(matched: {', '.join(blocked_scar.get('matched_keywords', [])[:5])})"
            ),
            "source": "scar",
            "scar_id": blocked_scar.get("id", ""),
        })

    if not findings:
        return {
            "safe": True,
            "severity": "NONE",
            "reason": "no threats detected",
            "source": "none",
            "details": [],
        }

    # Return worst severity
    findings.sort(key=lambda f: _severity_rank(f.get("severity", "LOW")), reverse=True)
    worst = findings[0]
    is_safe = worst["severity"] not in ("CRITICAL", "HIGH")

    return {
        "safe": is_safe,
        "severity": worst["severity"],
        "reason": worst["reason"],
        "source": worst["source"],
        "details": findings,
    }


# ============================================================================
# Directory Audit
# ============================================================================

# File extensions to scan
_AUDIT_EXTENSIONS = frozenset([
    ".py", ".js", ".ts", ".jsx", ".tsx", ".rb", ".go", ".rs",
    ".java", ".sh", ".bash", ".zsh", ".yml", ".yaml", ".toml",
    ".json", ".env", ".cfg", ".conf", ".ini", ".sql", ".tf",
    ".hcl", ".dockerfile", ".php", ".pl", ".r", ".swift",
    ".kt", ".scala", ".c", ".cpp", ".h", ".hpp", ".cs",
])

# Filename patterns that are inherently risky
_RISKY_FILENAMES = [
    (re.compile(r'(?i)\.env(\.|$)'), "dotenv file may contain secrets", "HIGH"),
    (re.compile(r'(?i)(credentials|secrets|passwords)\.(json|yaml|yml|toml|ini|cfg)$'),
     "credentials file", "CRITICAL"),
    (re.compile(r'(?i)id_rsa$|id_ed25519$|id_ecdsa$'), "private SSH key", "CRITICAL"),
    (re.compile(r'(?i)\.pem$'), "PEM file (may contain private key)", "HIGH"),
    (re.compile(r'(?i)\.p12$|\.pfx$'), "PKCS12 certificate bundle", "HIGH"),
    (re.compile(r'(?i)\.key$'), "key file", "HIGH"),
]


def audit(
    directory: str,
    scars: Optional[list[dict]] = None,
    scar_file: Optional[str] = None,
    max_file_size: int = 1_000_000,
) -> list[dict]:
    """Scan a directory for security issues.

    Checks for:
      - Secrets in file contents
      - Dangerous patterns in code
      - Risky filenames
      - Scar-matched patterns

    Args:
        directory: Path to directory to audit.
        scars: Pre-loaded scars. If None, loads from scar_file.
        scar_file: Path to scar file.
        max_file_size: Skip files larger than this (bytes).

    Returns:
        List of issue dicts with keys: file, line, severity, reason, source.
    """
    dirpath = Path(directory)
    if not dirpath.is_dir():
        return [{"file": str(directory), "line": 0, "severity": "HIGH",
                 "reason": "not a directory", "source": "audit"}]

    if scars is None:
        scars = load_safety_scars(scar_file)

    issues: list[dict] = []

    for root, _dirs, files in os.walk(dirpath):
        # Skip hidden directories and common non-code dirs
        root_path = Path(root)
        parts = root_path.parts
        if any(p.startswith(".") and p not in (".", "..") for p in parts):
            if not any(p == ".env" for p in parts):
                continue
        if any(p in ("node_modules", "__pycache__", ".git", "venv", ".venv")
               for p in parts):
            continue

        for fname in files:
            filepath = root_path / fname

            # Check risky filenames
            for pat, desc, sev in _RISKY_FILENAMES:
                if pat.search(fname):
                    issues.append({
                        "file": str(filepath),
                        "line": 0,
                        "severity": sev,
                        "reason": desc,
                        "source": "filename",
                    })

            # Check file contents
            suffix = filepath.suffix.lower()
            if suffix not in _AUDIT_EXTENSIONS:
                continue

            try:
                size = filepath.stat().st_size
            except OSError:
                continue

            if size > max_file_size or size == 0:
                continue

            try:
                content = filepath.read_text(encoding="utf-8", errors="replace")
            except (OSError, UnicodeDecodeError):
                continue

            for line_num, line in enumerate(content.splitlines(), 1):
                if not line.strip():
                    continue

                # Secret check
                for pat, desc in _COMPILED_SECRETS:
                    if pat.search(line):
                        issues.append({
                            "file": str(filepath),
                            "line": line_num,
                            "severity": "CRITICAL",
                            "reason": f"secret exposure: {desc}",
                            "source": "builtin",
                        })
                        break  # One finding per line is enough

                # Scar reflex on each line
                if scars:
                    blocked = reflex_block(line, scars)
                    if blocked:
                        issues.append({
                            "file": str(filepath),
                            "line": line_num,
                            "severity": blocked.get("severity", "HIGH"),
                            "reason": (
                                f"scar match: {blocked.get('never_allow', '')[:60]}"
                            ),
                            "source": "scar",
                        })

    # Sort by severity
    issues.sort(key=lambda i: _severity_rank(i.get("severity", "LOW")), reverse=True)
    return issues


# ============================================================================
# CLI Interface
# ============================================================================

def _cli_check(args: list[str]) -> int:
    """CLI: check an action."""
    if not args:
        print("Usage: scar_safety.py check <action description>", file=sys.stderr)
        return 1

    action = " ".join(args)
    result = safety_check(action)

    if result["safe"]:
        print(f"SAFE -- {result['reason']}")
        return 0
    else:
        print(f"BLOCKED [{result['severity']}] -- {result['reason']}")
        for d in result.get("details", [])[1:]:
            print(f"  also: [{d['severity']}] {d['reason']}")
        return 1


def _cli_record_incident(args: list[str]) -> int:
    """CLI: record a security incident."""
    what = ""
    never = ""
    severity = "HIGH"

    i = 0
    while i < len(args):
        if args[i] == "--what" and i + 1 < len(args):
            what = args[i + 1]
            i += 2
        elif args[i] == "--never" and i + 1 < len(args):
            never = args[i + 1]
            i += 2
        elif args[i] == "--severity" and i + 1 < len(args):
            severity = args[i + 1]
            i += 2
        else:
            i += 1

    if not what or not never:
        print("Usage: scar_safety.py record-incident --what <desc> --never <constraint> [--severity CRITICAL|HIGH|MEDIUM|LOW]",
              file=sys.stderr)
        return 1

    entry = record_incident(what, never, severity)
    print(f"SCAR RECORDED: {entry['id']}")
    print(f"  what:     {entry['what_happened']}")
    print(f"  never:    {entry['never_allow']}")
    print(f"  severity: {entry['severity']}")
    return 0


def _cli_audit(args: list[str]) -> int:
    """CLI: audit a directory."""
    if not args:
        print("Usage: scar_safety.py audit <directory>", file=sys.stderr)
        return 1

    directory = args[0]
    issues = audit(directory)

    if not issues:
        print(f"CLEAN -- no issues found in {directory}")
        return 0

    print(f"Found {len(issues)} issue(s) in {directory}:\n")
    for issue in issues:
        loc = f"{issue['file']}"
        if issue.get("line"):
            loc += f":{issue['line']}"
        print(f"  [{issue['severity']}] {loc}")
        print(f"    {issue['reason']}")
    return 1


def _cli_list_scars(args: list[str]) -> int:
    """CLI: list recorded scars."""
    scars = load_safety_scars()
    if not scars:
        print("No safety scars recorded yet.")
        return 0

    for s in scars:
        print(f"[{s.get('created_at', '?')}] {s.get('id', '?')} ({s.get('severity', '?')})")
        print(f"  what: {s.get('what_happened', '')[:80]}")
        print(f"  never: {s.get('never_allow', '')[:80]}")
        print()
    return 0


def main() -> int:
    """CLI entry point."""
    args = sys.argv[1:]

    if not args or args[0] in ("-h", "--help", "help"):
        print("scar-safety: Agent safety that learns from incidents.\n")
        print("Usage:")
        print("  scar_safety.py check <action>              Check if action is safe")
        print("  scar_safety.py record-incident --what <d> --never <c> [--severity S]")
        print("  scar_safety.py audit <directory>            Scan for security issues")
        print("  scar_safety.py list-scars                   List recorded scars")
        return 0

    command = args[0]
    rest = args[1:]

    if command == "check":
        return _cli_check(rest)
    elif command == "record-incident":
        return _cli_record_incident(rest)
    elif command == "audit":
        return _cli_audit(rest)
    elif command == "list-scars":
        return _cli_list_scars(rest)
    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
