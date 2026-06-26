#!/usr/bin/env python3
"""
Safe-Skill - Programmatic Security Scanner for AI Agent Skills
Zero external dependencies. Python 3.8+ stdlib only.

Usage:
    python3 scan.py <skill_directory> [--json] [--verbose]
    python3 scan.py <skill_directory> --output report.json
    python3 scan.py <single_file.md>
"""

import ast
import argparse
import hashlib
import json
import math
import os
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import stat
import subprocess as _subprocess


# ============================================================
# 0. IOC Threat Intelligence Loaders (lazy, cached)
# ============================================================

_IOC_DIR = Path(__file__).parent.parent / "ioc"

_ioc_cache: Dict[str, object] = {}


def _load_ioc_file(filename: str, key_index: int = 0) -> set:
    """Load an IOC file and return a set of the key column (case-folded).

    Lines starting with '#' are skipped.  Fields are '|'-separated.
    Returns an empty set if the file does not exist.
    """
    cache_key = f"{filename}:{key_index}"
    if cache_key in _ioc_cache:
        return _ioc_cache[cache_key]

    result: set = set()
    fpath = _IOC_DIR / filename
    if not fpath.exists():
        _ioc_cache[cache_key] = result
        return result
    try:
        for line in fpath.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split("|")
            if len(parts) > key_index:
                result.add(parts[key_index].strip().lower())
    except Exception:
        pass
    _ioc_cache[cache_key] = result
    return result


def load_c2_ips() -> set:
    """Return set of known C2 IP addresses (lowercase strings)."""
    return _load_ioc_file("c2-ips.txt", 0)


def load_malicious_domains() -> set:
    """Return set of known malicious domains (lowercase)."""
    return _load_ioc_file("malicious-domains.txt", 0)


def load_malicious_publishers() -> set:
    """Return set of known malicious publisher usernames (lowercase)."""
    return _load_ioc_file("malicious-publishers.txt", 0)


def load_malicious_hashes() -> set:
    """Return set of known malicious file hashes (lowercase sha256)."""
    hashes = _load_ioc_file("malicious-hashes.txt", 0)
    hashes |= _load_ioc_file("file-hashes.txt", 0)
    return hashes


def load_malicious_skill_patterns() -> List[re.Pattern]:
    """Return list of compiled regex patterns for malicious skill names."""
    cache_key = "skill_patterns_compiled"
    if cache_key in _ioc_cache:
        return _ioc_cache[cache_key]

    patterns: List[re.Pattern] = []
    fpath = _IOC_DIR / "malicious-skill-patterns.txt"
    if not fpath.exists():
        _ioc_cache[cache_key] = patterns
        return patterns
    try:
        for line in fpath.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split("|")
            if parts:
                try:
                    patterns.append(re.compile(parts[0].strip(), re.IGNORECASE))
                except re.error:
                    pass
    except Exception:
        pass
    _ioc_cache[cache_key] = patterns
    return patterns


# ============================================================
# 1. Pattern Definitions — the detection ruleset
# ============================================================

@dataclass
class PatternRule:
    id: str
    category: str       # rce, exfil, credential, obfuscation, escalation, agent_identity, persistence, ioc
    severity: str        # critical, high, medium, low, info
    pattern: str         # regex pattern
    description: str
    context: str = ""    # what makes this dangerous
    false_positive_hint: str = ""


RULES: List[PatternRule] = [
    # --- Remote Code Execution ---
    PatternRule("RCE-001", "rce", "critical",
        r'curl\s+[^|]*\|\s*(ba)?sh', 
        "Pipe from curl to shell",
        "Downloads and executes arbitrary remote code",
        "Legitimate if URL is pinned and trusted"),
    PatternRule("RCE-002", "rce", "critical",
        r'wget\s+[^|]*\|\s*(ba)?sh',
        "Pipe from wget to shell",
        "Downloads and executes arbitrary remote code"),
    PatternRule("RCE-003", "rce", "critical",
        r'wget\s+.*-O\s*-\s*\|\s*(ba)?sh',
        "wget stdout to shell",
        "Downloads and executes arbitrary remote code"),
    PatternRule("RCE-004", "rce", "critical",
        r'eval\s*["\(]\s*\$\(',
        "eval with command substitution",
        "Executes dynamically constructed commands"),
    PatternRule("RCE-005", "rce", "high",
        r'eval\s*\(',
        "eval() call",
        "Arbitrary code execution",
        "Check if input is user-controlled"),
    PatternRule("RCE-006", "rce", "high",
        r'exec\s*\(',
        "exec() call",
        "Arbitrary code execution",
        "Check if input is user-controlled"),
    PatternRule("RCE-007", "rce", "high",
        r'subprocess\.(?:call|run|Popen|check_output)\s*\(',
        "subprocess invocation",
        "Spawns external process",
        "Check if arguments are hardcoded or user-controlled"),
    PatternRule("RCE-008", "rce", "high",
        r'os\.system\s*\(',
        "os.system() call",
        "Executes shell command"),
    PatternRule("RCE-009", "rce", "medium",
        r'os\.popen\s*\(',
        "os.popen() call",
        "Executes shell command and captures output"),
    PatternRule("RCE-010", "rce", "high",
        r'__import__\s*\(',
        "Dynamic import",
        "Loads modules at runtime, can bypass static analysis"),
    PatternRule("RCE-011", "rce", "high",
        r'compile\s*\(.*["\']exec["\']',
        "compile() with exec mode",
        "Compiles code for execution"),
    PatternRule("RCE-012", "rce", "medium",
        r'importlib\.import_module\s*\(',
        "Dynamic module import via importlib",
        "Loads modules at runtime"),
    PatternRule("RCE-013", "rce", "high",
        r'getattr\s*\([^,]+,\s*[^"\'\s][^)]*\)',
        "Dynamic getattr() call",
        "Resolves function names at runtime to evade detection"),

    # --- Data Exfiltration ---
    PatternRule("EXFIL-001", "exfil", "critical",
        r'requests\.(?:post|put|patch)\s*\(',
        "HTTP POST/PUT/PATCH request",
        "Sends data to external server",
        "Check if target URL is legitimate"),
    PatternRule("EXFIL-002", "exfil", "high",
        r'urllib\.request\.(?:urlopen|Request)\s*\(',
        "urllib outbound request",
        "Sends data to external server"),
    PatternRule("EXFIL-003", "exfil", "high",
        r'http\.client\.HTTP',
        "Direct HTTP client usage",
        "Low-level HTTP connection"),
    PatternRule("EXFIL-004", "exfil", "high",
        r'socket\.\s*(?:socket|create_connection)',
        "Raw socket creation",
        "Low-level network access, can bypass proxies"),
    PatternRule("EXFIL-005", "exfil", "medium",
        r'smtplib\.',
        "SMTP library usage",
        "Can send data via email"),
    PatternRule("EXFIL-006", "exfil", "high",
        r'curl\s+.*-(?:d|X\s*POST|F)\s',
        "curl with data/POST",
        "Sends data to external server via curl"),
    PatternRule("EXFIL-007", "exfil", "medium",
        r'fetch\s*\(\s*["\']https?://',
        "JavaScript fetch to external URL",
        "Sends data to external server from JS context"),

    # --- Credential Access ---
    PatternRule("CRED-001", "credential", "critical",
        r'~/\.ssh',
        "SSH directory access",
        "Reads SSH private keys"),
    PatternRule("CRED-002", "credential", "critical",
        r'~/\.aws',
        "AWS credentials access",
        "Reads AWS access keys"),
    PatternRule("CRED-003", "credential", "critical",
        r'~/\.config/gcloud',
        "GCloud credentials access",
        "Reads Google Cloud credentials"),
    PatternRule("CRED-004", "credential", "high",
        r'~/\.(?:kube|docker)/config',
        "Kubernetes/Docker config access",
        "Reads cluster credentials"),
    PatternRule("CRED-005", "credential", "high",
        r'~/\.(?:netrc|pgpass|my\.cnf)',
        "Database/service credential files",
        "Reads stored passwords"),
    PatternRule("CRED-006", "credential", "high",
        r'(?:API_KEY|SECRET|TOKEN|PASSWORD|CREDENTIALS?)\s*[=:]\s*["\'][^"\']{8,}',
        "Hardcoded credential pattern",
        "Embeds secrets directly in code"),
    PatternRule("CRED-007", "credential", "high",
        r'os\.environ\.get\s*\(\s*["\'](?:.*(?:KEY|SECRET|TOKEN|PASS|CRED))',
        "Reading secret environment variables",
        "Accesses credentials from environment",
        "Normal for API integrations, check what it does with the value"),
    PatternRule("CRED-008", "credential", "critical",
        r'keyring\.|keychain|credential.?store',
        "System keyring/keychain access",
        "Accesses OS-level credential storage"),
    PatternRule("CRED-009", "credential", "high",
        r'~/\.(?:env|env\.local)',
        "Dotenv file access",
        "Reads environment configuration with potential secrets"),
    PatternRule("CRED-010", "credential", "high",
        r'(?:browser|https?|steal|access|get|read|extract|dump|export|send|document)[\s._\[\]"\x27-]*(?:cookie|session)s?\b',
        "Browser cookie/session access",
        "Can steal authenticated sessions"),
    PatternRule("CRED-011", "credential", "high",
        r'\b(?:cookie|session)s?[\s._-]*(?:access|theft|steal|exfil|extract|send|dump|read|hijack|grab)',
        "Cookie/session theft pattern",
        "Attempts to steal or exfiltrate session data"),

    # --- Obfuscation ---
    PatternRule("OBFS-001", "obfuscation", "high",
        r'base64\.(?:b64decode|decodebytes)\s*\(',
        "Base64 decoding",
        "Decodes hidden payload",
        "Check what is being decoded"),
    PatternRule("OBFS-002", "obfuscation", "high",
        r'codecs\.decode\s*\(.*["\']rot',
        "ROT cipher decoding",
        "Obfuscated string"),
    PatternRule("OBFS-003", "obfuscation", "medium",
        r'\\x[0-9a-fA-F]{2}(?:\\x[0-9a-fA-F]{2}){5,}',
        "Hex-encoded byte sequence (6+ bytes)",
        "Potentially obfuscated payload"),
    PatternRule("OBFS-004", "obfuscation", "medium",
        r'\\u[0-9a-fA-F]{4}(?:\\u[0-9a-fA-F]{4}){5,}',
        "Unicode escape sequence (6+ chars)",
        "Potentially obfuscated strings"),
    PatternRule("OBFS-005", "obfuscation", "high",
        r'zlib\.decompress\s*\(',
        "Zlib decompression",
        "Unpacking compressed payload"),
    PatternRule("OBFS-006", "obfuscation", "medium",
        r'chr\s*\(\s*\d+\s*\)(?:\s*\+\s*chr\s*\(\s*\d+\s*\)){3,}',
        "String built from chr() calls (4+ chars)",
        "Character-by-character string construction to evade detection"),
    PatternRule("OBFS-007", "obfuscation", "high",
        r'marshal\.loads\s*\(',
        "marshal.loads() - bytecode deserialization",
        "Loads pre-compiled Python bytecode, can hide anything"),
    PatternRule("OBFS-008", "obfuscation", "high",
        r'pickle\.loads?\s*\(',
        "pickle deserialization",
        "Arbitrary code execution via deserialization"),

    # --- Privilege Escalation ---
    PatternRule("ESC-001", "escalation", "critical",
        r'sudo\s+|["\']sudo["\']',
        "sudo usage",
        "Requests elevated privileges"),
    PatternRule("ESC-002", "escalation", "high",
        r'chmod\s+[0-7]*[2367][0-7]*\s',
        "chmod with write/execute for group/others",
        "Loosens file permissions"),
    PatternRule("ESC-003", "escalation", "high",
        r'chown\s+',
        "chown - change file ownership",
        "Changes file ownership"),
    PatternRule("ESC-004", "escalation", "critical",
        r'/etc/(?:passwd|shadow|sudoers)',
        "System authentication file access",
        "Reads/modifies system auth files"),
    PatternRule("ESC-005", "escalation", "high",
        r'setuid|setgid|cap_|chmod\s+[ugo]*\+s\b',
        "SUID/SGID/capability manipulation",
        "Modifies execution privileges"),

    # --- Agent Identity / OpenClaw Specific ---
    PatternRule("AGENT-001", "agent_identity", "critical",
        r'(?:MEMORY|SOUL|IDENTITY|USER|PERSONA)\.md',
        "Agent identity file access",
        "Reads/modifies agent memory, personality, or user profile"),
    PatternRule("AGENT-002", "agent_identity", "high",
        r'~/\.claude(?:/|$)',
        "Claude config directory access",
        "Reads agent configuration and stored skills"),
    PatternRule("AGENT-003", "agent_identity", "high",
        r'CLAUDE\.md|\.clauderc|claude_config',
        "Claude configuration files",
        "Reads/modifies agent behavior settings"),
    PatternRule("AGENT-004", "agent_identity", "high",
        r'(?:system_prompt|system_message|instructions)\s*[=:]',
        "System prompt manipulation",
        "Attempts to read or modify agent instructions"),
    PatternRule("AGENT-005", "agent_identity", "medium",
        r'(?:conversation|chat)_?(?:history|log|memory)',
        "Conversation history access",
        "Reads past agent interactions"),

    # --- Persistence / Backdoor ---
    PatternRule("PERSIST-001", "persistence", "critical",
        r'cron(?:tab)?\s+',
        "Crontab manipulation",
        "Installs persistent scheduled tasks"),
    PatternRule("PERSIST-002", "persistence", "high",
        r'~/.(?:bashrc|bash_profile|zshrc|profile)',
        "Shell profile modification",
        "Persists across shell sessions"),
    PatternRule("PERSIST-003", "persistence", "high",
        r'systemctl\s+(?:enable|start)',
        "Systemd service manipulation",
        "Installs persistent service"),
    PatternRule("PERSIST-004", "persistence", "high",
        r'launchctl\s+(?:load|submit)',
        "macOS LaunchAgent/Daemon",
        "Installs persistent agent on macOS"),
    PatternRule("PERSIST-005", "persistence", "medium",
        r'(?:git\s+)?(?:config|hook).*(?:pre-|post-)',
        "Git hook manipulation",
        "Installs code that runs on git operations",
        "May be legitimate for git workflow skills"),

    # --- Suspicious Network ---
    PatternRule("NET-001", "network", "high",
        r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',
        "Hardcoded IP address (non-localhost)",
        "Connects to IP instead of domain, harder to audit"),
    PatternRule("NET-002", "network", "medium",
        r'ngrok|localtunnel|serveo\.net|bore\.pub',
        "Tunnel service reference",
        "Creates public tunnel to local services"),
    PatternRule("NET-003", "network", "medium",
        r'(?:pastebin|hastebin|ix\.io|dpaste|ghostbin)',
        "Paste service reference",
        "Reads from or writes to paste services"),
    PatternRule("NET-004", "network", "high",
        r'\.onion\b',
        "Tor hidden service reference",
        "References dark web service"),

    # --- File System ---
    PatternRule("FS-001", "filesystem", "medium",
        r'shutil\.rmtree\s*\(',
        "Recursive directory deletion",
        "Deletes entire directory trees"),
    PatternRule("FS-002", "filesystem", "medium",
        r'os\.(?:remove|unlink|rmdir)\s*\(',
        "File/directory deletion",
        "Deletes files or directories"),
    PatternRule("FS-003", "filesystem", "high",
        r'(?:open|Path)\s*\(.*(?:/etc/|/var/|/usr/|/opt/|/root/)',
        "System directory access",
        "Reads/writes outside workspace"),
    PatternRule("FS-004", "filesystem", "medium",
        r'glob\.glob\s*\(\s*["\'](?:\*\*|/)',
        "Recursive/root file globbing",
        "Enumerates files broadly"),

    # --- Package Installation ---
    PatternRule("PKG-001", "package", "medium",
        r'pip\s+install\s+(?!-r\b)',
        "pip install (ad-hoc)",
        "Installs Python packages at runtime",
        "Check if packages are listed in requirements"),
    PatternRule("PKG-002", "package", "medium",
        r'npm\s+install\s+(?!--save-dev)',
        "npm install",
        "Installs Node.js packages at runtime"),
    PatternRule("PKG-003", "package", "high",
        r'pip\s+install\s+.*--index-url\s+(?!https://pypi\.org)',
        "pip install from custom index",
        "Installs from non-official package repository"),
    PatternRule("PKG-004", "package", "high",
        r'pip\s+install\s+git\+https?://',
        "pip install from git URL",
        "Installs directly from git, version unpinned"),

    # --- IOC-based rules (matched via IOC data, patterns here are placeholders) ---
    PatternRule("IOC-001", "ioc", "critical",
        r'(?!x)x',  # never matches — IOC matching done programmatically
        "Known C2 IP address detected",
        "IP address found in threat intelligence C2 feed"),
    PatternRule("IOC-002", "ioc", "critical",
        r'(?!x)x',
        "Known malicious domain detected",
        "Domain found in threat intelligence malicious domain list"),
    PatternRule("IOC-003", "ioc", "critical",
        r'(?!x)x',
        "Known malicious publisher",
        "Publisher matches known malicious actor in threat intelligence"),
    PatternRule("IOC-004", "ioc", "critical",
        r'(?!x)x',
        "Known malicious file hash",
        "File hash matches known malware in threat intelligence"),
    PatternRule("IOC-005", "ioc", "high",
        r'(?!x)x',
        "Skill name matches known attack pattern",
        "Skill name matches known malicious skill naming pattern"),

    # --- Prompt Injection ---
    PatternRule("INJECT-001", "agent_identity", "critical",
        r'ignore\s+previous\s+instructions|ignore\s+all\s+previous|disregard.*previous|override.*instruction|new\s+system\s+prompt|forget.*previous|you\s+are\s+now|pretend\s+to\s+be|from\s+now\s+on.*ignore',
        "Prompt injection pattern",
        "Attempts to override agent instructions"),
    PatternRule("INJECT-002", "exfil", "critical",
        r'forward\s+to|send\s+to|exfiltrat|leak\s+(the\s+)?(secret|token|credential|key)|reveal\s+(the\s+)?(system\s+prompt|secret|token|credential)',
        "Data exfiltration instruction",
        "Instructions to leak secrets or credentials"),

    # --- Malware Markers ---
    PatternRule("MALWARE-001", "rce", "critical",
        r'authtool|atomic[.\s_]stealer|AMOS|NovaStealer|nova[.\s_]stealer|osascript.*password|osascript.*dialog|osascript.*keychain|Security\.framework.*Auth|openclaw-agent\.exe|openclaw-agent\.zip|openclawcli\.zip|AuthTool|Installer-Package',
        "AMOS/stealer marker",
        "Known malware distribution pattern"),
]

# Compile all patterns once
COMPILED_RULES = [(rule, re.compile(rule.pattern, re.IGNORECASE | re.MULTILINE)) for rule in RULES]


# ============================================================
# 1b. Whitelist Configuration (.vetterrc)
# ============================================================

@dataclass
class WhitelistConfig:
    """Rules/patterns to suppress in a specific skill context."""
    # Rule IDs to ignore completely, e.g. ["RCE-005", "CRED-007"]
    ignore_rules: List[str] = field(default_factory=list)
    # Categories to ignore, e.g. ["package"]
    ignore_categories: List[str] = field(default_factory=list)
    # URL domains considered safe for this skill
    trusted_domains: List[str] = field(default_factory=list)
    # Specific line+rule combos to suppress: [{"file": "helper.py", "line": 42, "rule": "RCE-005"}]
    inline_suppressions: List[Dict] = field(default_factory=list)
    # Max severity to auto-accept ("info", "low", "medium")
    accept_severity: str = ""


_VETTERRC_NAMES = [".vetterrc", ".vetterrc.json", ".vetterrc.yaml", ".vetterrc.yml"]


def load_whitelist(skill_path: str) -> Tuple[WhitelistConfig, bool]:
    """Load .vetterrc from a skill directory (if present).

    Returns:
        A tuple of (WhitelistConfig, skill_bundled) where *skill_bundled*
        is True when the whitelist was auto-detected inside the skill
        directory (as opposed to being supplied via an explicit ``-w`` flag).
    """
    path = Path(skill_path)
    if path.is_file():
        path = path.parent

    for name in _VETTERRC_NAMES:
        rc_file = path / name
        if rc_file.exists():
            try:
                raw = rc_file.read_text(encoding='utf-8')
                # Try JSON first
                if name.endswith('.json') or raw.strip().startswith('{'):
                    data = json.loads(raw)
                else:
                    # Minimal YAML-like parsing for simple key: [values] format
                    data = _parse_simple_yaml(raw)
                return WhitelistConfig(
                    ignore_rules=data.get("ignore_rules", []),
                    ignore_categories=data.get("ignore_categories", []),
                    trusted_domains=data.get("trusted_domains", []),
                    inline_suppressions=data.get("inline_suppressions", []),
                    accept_severity=data.get("accept_severity", ""),
                ), True  # skill-bundled
            except Exception as e:
                print(f"Warning: Failed to parse {rc_file}: {e}", file=sys.stderr)
    return WhitelistConfig(), False


def _parse_simple_yaml(text: str) -> Dict:
    """Minimal parser for simple YAML (key: value or key: [list] format)."""
    result = {}
    current_key = None
    current_list = None

    for line in text.split('\n'):
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            continue

        # key: value or key:
        kv_match = re.match(r'^(\w+)\s*:\s*(.*)', stripped)
        if kv_match:
            key = kv_match.group(1)
            val = kv_match.group(2).strip()
            if val.startswith('[') and val.endswith(']'):
                # Inline list: key: [a, b, c]
                items = [x.strip().strip('"').strip("'") for x in val[1:-1].split(',') if x.strip()]
                result[key] = items
                current_key = None
                current_list = None
            elif val == '' or val == '[]':
                current_key = key
                current_list = []
                result[key] = current_list
            else:
                result[key] = val.strip('"').strip("'")
                current_key = None
                current_list = None
            continue

        # List item: - value
        list_match = re.match(r'^-\s+(.*)', stripped)
        if list_match and current_list is not None:
            current_list.append(list_match.group(1).strip().strip('"').strip("'"))
            continue

    return result


def apply_whitelist(findings: List[Dict], whitelist: WhitelistConfig, filepath: str = "") -> List[Dict]:
    """Filter findings through whitelist. Returns filtered list."""
    if not (whitelist.ignore_rules or whitelist.ignore_categories
            or whitelist.inline_suppressions or whitelist.accept_severity):
        return findings

    severity_order = {"info": 0, "low": 1, "medium": 2, "high": 3, "critical": 4}
    accept_threshold = severity_order.get(whitelist.accept_severity, -1)

    filtered = []
    for f in findings:
        # Rule ID suppression
        if f.get("rule_id", "") in whitelist.ignore_rules:
            continue
        # Category suppression
        if f.get("category", "") in whitelist.ignore_categories:
            continue
        # Severity auto-accept
        if accept_threshold >= 0 and severity_order.get(f.get("severity", ""), 99) <= accept_threshold:
            continue
        # Inline suppression
        fname = Path(filepath).name if filepath else ""
        suppressed = False
        for sup in whitelist.inline_suppressions:
            if (sup.get("file", "") == fname
                    and sup.get("line", -1) == f.get("line", -2)
                    and sup.get("rule", "") == f.get("rule_id", "")):
                suppressed = True
                break
        if suppressed:
            continue

        filtered.append(f)
    return filtered


def _apply_whitelist_downgrade(findings: List[Dict], whitelist: WhitelistConfig, filepath: str = "") -> List[Dict]:
    """Apply a skill-bundled whitelist by *downgrading* matches to info severity
    instead of fully suppressing them.

    This prevents a malicious skill from silencing the scanner by shipping
    its own permissive ``.vetterrc``.  Matched findings are kept in the
    report with ``severity`` set to ``"info"`` and a ``[SUPPRESSED]`` tag
    prepended to their description.
    """
    if not (whitelist.ignore_rules or whitelist.ignore_categories
            or whitelist.inline_suppressions or whitelist.accept_severity):
        return findings

    severity_order = {"info": 0, "low": 1, "medium": 2, "high": 3, "critical": 4}
    accept_threshold = severity_order.get(whitelist.accept_severity, -1)

    result = []
    for f in findings:
        should_downgrade = False

        # Rule ID suppression
        if f.get("rule_id", "") in whitelist.ignore_rules:
            should_downgrade = True
        # Category suppression
        elif f.get("category", "") in whitelist.ignore_categories:
            should_downgrade = True
        # Severity auto-accept
        elif accept_threshold >= 0 and severity_order.get(f.get("severity", ""), 99) <= accept_threshold:
            should_downgrade = True
        else:
            # Inline suppression
            fname = Path(filepath).name if filepath else ""
            for sup in whitelist.inline_suppressions:
                if (sup.get("file", "") == fname
                        and sup.get("line", -1) == f.get("line", -2)
                        and sup.get("rule", "") == f.get("rule_id", "")):
                    should_downgrade = True
                    break

        if should_downgrade:
            f = dict(f)  # shallow copy to avoid mutating the original
            f["severity"] = "info"
            if not f.get("description", "").startswith("[SUPPRESSED]"):
                f["description"] = "[SUPPRESSED] " + f.get("description", "")

        result.append(f)
    return result


# ============================================================
# 2. Entropy Analysis
# ============================================================

def shannon_entropy(data: str) -> float:
    """Calculate Shannon entropy of a string."""
    if not data:
        return 0.0
    counter = Counter(data)
    length = len(data)
    return -sum(
        (count / length) * math.log2(count / length)
        for count in counter.values()
    )


def detect_high_entropy_strings(content: str, min_length: int = 40, threshold: float = 4.5,
                                filepath: str = "") -> List[Dict]:
    """Find high-entropy strings that may be encoded/obfuscated payloads."""
    # Skip lock files entirely — they contain hundreds of integrity hashes
    # that are benign (sha512- checksums, npm/yarn integrity fields).
    _basename = os.path.basename(filepath).lower() if filepath else ""
    if _basename in _ENTROPY_SKIP_FILES:
        return []

    findings = []
    # Match long alphanumeric strings (potential base64, hex, etc.)
    pattern = re.compile(r'[A-Za-z0-9+/=_-]{' + str(min_length) + r',}')
    for match in pattern.finditer(content):
        s = match.group()
        # Skip known safe patterns
        if _is_safe_entropy_string(s):
            continue
        ent = shannon_entropy(s)
        if ent >= threshold:
            line_num = content[:match.start()].count('\n') + 1
            findings.append({
                "line": line_num,
                "length": len(s),
                "entropy": round(ent, 3),
                "preview": s[:60] + ("..." if len(s) > 60 else ""),
                "type": _classify_encoding(s),
            })
    return findings


# Files that are always full of legitimate high-entropy hashes
_ENTROPY_SKIP_FILES = {
    "package-lock.json", "yarn.lock", "pnpm-lock.yaml",
    "poetry.lock", "pipfile.lock", "composer.lock",
    "gemfile.lock", "cargo.lock", "go.sum",
}

# Regex patterns for known-safe high-entropy strings
_SAFE_ENTROPY_PREFIXES = (
    "sha512-", "sha256-", "sha384-", "sha1-",       # integrity hashes
    "AAAA",                                            # SSH public key prefix
)

_SAFE_ENTROPY_RE = re.compile(
    r'^(?:'
    r'[0-9a-fA-F]{40}$'       # SHA-1 git hashes (exactly 40 hex chars)
    r'|[0-9a-fA-F]{64}$'      # SHA-256 hashes (exactly 64 hex chars)
    r'|[0-9a-fA-F]{128}$'     # SHA-512 hashes (exactly 128 hex chars)
    r'|0x[0-9a-fA-F]{40,}$'   # Ethereum/Solidity addresses and hashes
    r')'
)


def _is_safe_entropy_string(s: str) -> bool:
    """Check if a high-entropy string is a known-safe pattern."""
    # Integrity hash prefixes
    if any(s.startswith(p) for p in _SAFE_ENTROPY_PREFIXES):
        return True
    # Exact-length cryptographic hashes (hex)
    if _SAFE_ENTROPY_RE.match(s):
        return True
    # Solana/crypto base58 addresses (32-44 chars, alphanumeric only)
    if 32 <= len(s) <= 44 and re.match(r'^[1-9A-HJ-NP-Za-km-z]+$', s):
        return True
    return False


def _classify_encoding(s: str) -> str:
    """Heuristic guess of encoding type."""
    if re.match(r'^[A-Za-z0-9+/]+=*$', s):
        return "likely_base64"
    if re.match(r'^[0-9a-fA-F]+$', s):
        return "likely_hex"
    if re.match(r'^[A-Za-z0-9_-]+$', s):
        return "likely_base64url"
    return "unknown_encoding"


# ============================================================
# 2b. Markdown Context Analyzer — reduces false positives
# ============================================================

@dataclass
class MarkdownContext:
    """Parsed markdown structure for context-aware scanning."""
    # Maps line number → context type
    line_contexts: Dict[int, str] = field(default_factory=dict)
    # code_block, documentation_list, heading, prose, frontmatter

    # Ranges of fenced code blocks: [(start_line, end_line, lang), ...]
    code_blocks: List[Tuple[int, int, str]] = field(default_factory=list)

    # Lines that are part of a "danger/warning checklist" (bullet points listing patterns)
    checklist_lines: set = field(default_factory=set)


# Headings/phrases that indicate a section is DESCRIBING dangers, not executing them
_DOCUMENTATION_HEADINGS = re.compile(
    r'(?:red\s*flag|check\s*(?:for|list)|reject|warning|danger|'
    r'do\s*not|never|avoid|suspicious|malicious|vetting|review|'
    r'safe\s*pattern|what\s*(?:it|to)\s*(?:detect|scan|check|look)|'
    r'detect(?:ion|s|ed)|limitation|example\s*(?:of|:)|'
    r'owasp|vulnerabilit|common\s*(?:attack|threat|issue)|'
    r'security\s*(?:guide|best|tip|practice|overview))',
    re.IGNORECASE
)

# Bullet points that are describing patterns to look for
_CHECKLIST_BULLET = re.compile(
    r'^\s*[-•*]\s+.*(?:curl|wget|eval|exec|sudo|ssh|aws|credential|token|'
    r'base64|obfuscat|cookie|session|\.onion|crontab|chmod)',
    re.IGNORECASE
)


def parse_markdown_context(content: str) -> MarkdownContext:
    """Parse a markdown file to understand structural context of each line."""
    ctx = MarkdownContext()
    lines = content.split('\n')
    in_code_block = False
    code_block_start = 0
    code_lang = ""
    in_frontmatter = False
    frontmatter_started = False

    # Track documentation section scoping by heading depth
    doc_section_active = False
    doc_section_depth = 99  # heading depth that started the doc section

    for i, line in enumerate(lines):
        line_num = i + 1

        # YAML frontmatter
        if line.strip() == '---':
            if not frontmatter_started and i == 0:
                frontmatter_started = True
                in_frontmatter = True
                ctx.line_contexts[line_num] = "frontmatter"
                continue
            elif in_frontmatter:
                in_frontmatter = False
                ctx.line_contexts[line_num] = "frontmatter"
                continue
        if in_frontmatter:
            ctx.line_contexts[line_num] = "frontmatter"
            continue

        # Fenced code blocks
        if line.strip().startswith('```'):
            if not in_code_block:
                in_code_block = True
                code_block_start = line_num
                code_lang = line.strip()[3:].strip().split()[0] if len(line.strip()) > 3 else ""
            else:
                in_code_block = False
                ctx.code_blocks.append((code_block_start, line_num, code_lang))
                code_lang = ""
            ctx.line_contexts[line_num] = "code_fence"
            continue
        if in_code_block:
            # If we're inside a doc section, this code block is documentation too
            if doc_section_active:
                ctx.line_contexts[line_num] = "documentation_list"
                ctx.checklist_lines.add(line_num)
            else:
                ctx.line_contexts[line_num] = "code_block"
            continue

        # Headings — check if the heading suggests documentation of dangers
        heading_match = re.match(r'^(#{1,6})\s+(.*)', line)
        if heading_match:
            depth = len(heading_match.group(1))
            heading_text = heading_match.group(2)
            if _DOCUMENTATION_HEADINGS.search(heading_text):
                doc_section_active = True
                doc_section_depth = depth
            elif depth <= doc_section_depth:
                # A same-or-higher-level heading ends the doc section
                doc_section_active = False
                doc_section_depth = 99
            ctx.line_contexts[line_num] = "heading"
            continue

        # Content under documentation headings
        if doc_section_active:
            ctx.checklist_lines.add(line_num)
            ctx.line_contexts[line_num] = "documentation_list"
            continue

        ctx.line_contexts[line_num] = "prose"

    return ctx


def is_documentation_context(md_ctx: MarkdownContext, line_num: int) -> bool:
    """Check if a given line is in a documentation/descriptive context."""
    ctx_type = md_ctx.line_contexts.get(line_num, "prose")

    if ctx_type == "frontmatter":
        return True
    if ctx_type == "documentation_list":
        return True
    if line_num in md_ctx.checklist_lines:
        return True

    return False


def adjust_finding_for_context(finding: dict, md_ctx: MarkdownContext) -> dict:
    """Adjust a finding's severity if it's in a documentation context."""
    line = finding.get("line", 0)
    if is_documentation_context(md_ctx, line):
        finding = dict(finding)  # copy
        original_severity = finding["severity"]
        finding["severity"] = "info"
        finding["context"] = (
            f"[DOCUMENTATION CONTEXT — downgraded from {original_severity}] "
            + finding.get("context", "")
        )
        finding["in_documentation"] = True
    else:
        finding["in_documentation"] = False
    return finding


# ============================================================
# 3. Python AST Analysis
# ============================================================

@dataclass
class ASTFinding:
    line: int
    severity: str
    category: str
    description: str


def analyze_python_ast(filepath: str, content: str) -> List[ASTFinding]:
    """Deep analysis of Python files using AST."""
    findings = []
    try:
        tree = ast.parse(content, filename=filepath)
    except SyntaxError:
        return [ASTFinding(0, "info", "parse_error", f"SyntaxError: cannot parse {filepath}")]

    for node in ast.walk(tree):
        # Detect exec/eval with non-literal arguments
        if isinstance(node, ast.Call):
            func_name = _get_call_name(node)
            if func_name in ("eval", "exec"):
                if node.args and not isinstance(node.args[0], (ast.Constant, ast.Str)):
                    findings.append(ASTFinding(
                        node.lineno, "critical", "rce",
                        f"{func_name}() called with dynamic argument"
                    ))
            elif func_name == "__import__":
                if node.args and not isinstance(node.args[0], (ast.Constant, ast.Str)):
                    findings.append(ASTFinding(
                        node.lineno, "high", "rce",
                        "__import__() with dynamic module name"
                    ))
                elif node.args and isinstance(node.args[0], (ast.Constant, ast.Str)):
                    mod = node.args[0].s if isinstance(node.args[0], ast.Str) else node.args[0].value
                    if mod in ("subprocess", "os", "socket", "ctypes", "marshal"):
                        findings.append(ASTFinding(
                            node.lineno, "high", "rce",
                            f"Dynamic import of sensitive module: {mod}"
                        ))
            elif func_name in ("pickle.loads", "pickle.load", "marshal.loads"):
                findings.append(ASTFinding(
                    node.lineno, "critical", "obfuscation",
                    f"Deserialization via {func_name}() — arbitrary code execution"
                ))
            elif func_name == "compile" and len(node.args) >= 3:
                # compile(source, filename, 'exec')
                if isinstance(node.args[2], (ast.Constant, ast.Str)):
                    mode = node.args[2].s if isinstance(node.args[2], ast.Str) else node.args[2].value
                    if mode == "exec":
                        findings.append(ASTFinding(
                            node.lineno, "high", "rce",
                            "compile() in exec mode"
                        ))
            elif func_name == "getattr" and len(node.args) >= 2:
                _DANGEROUS_ATTR_NAMES = {
                    "system", "exec", "eval", "popen", "run", "call",
                    "check_output", "check_call", "Popen", "loads", "load",
                }
                attr_arg = node.args[1]
                if isinstance(attr_arg, (ast.Constant, ast.Str)):
                    attr_name = attr_arg.s if isinstance(attr_arg, ast.Str) else attr_arg.value
                    if isinstance(attr_name, str) and attr_name in _DANGEROUS_ATTR_NAMES:
                        findings.append(ASTFinding(
                            node.lineno, "high", "rce",
                            f"[AST-getattr-dangerous] getattr() resolving dangerous function: {attr_name} (line {node.lineno})"
                        ))
                elif not isinstance(attr_arg, (ast.Constant, ast.Str)):
                    findings.append(ASTFinding(
                        node.lineno, "critical", "obfuscation",
                        f"[AST-getattr-dynamic] Dynamic getattr() — attribute name constructed at runtime (line {node.lineno})"
                    ))

        # Detect try/except that silently catches everything
        if isinstance(node, ast.ExceptHandler):
            if node.type is None and _is_pass_body(node.body):
                findings.append(ASTFinding(
                    node.lineno, "low", "evasion",
                    "Bare except with pass — silently swallows all errors (can hide failures)"
                ))

        # Detect suspicious string concatenation patterns (anti-detection)
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
            depth = _string_concat_depth(node)
            if depth >= 6:
                findings.append(ASTFinding(
                    node.lineno, "medium", "obfuscation",
                    f"Deep string concatenation ({depth} levels) — may be building commands dynamically"
                ))

    return findings


def _get_call_name(node: ast.Call) -> str:
    """Extract function name from a Call node."""
    if isinstance(node.func, ast.Name):
        return node.func.id
    elif isinstance(node.func, ast.Attribute):
        parts = []
        current = node.func
        while isinstance(current, ast.Attribute):
            parts.append(current.attr)
            current = current.value
        if isinstance(current, ast.Name):
            parts.append(current.id)
        return ".".join(reversed(parts))
    return ""


def _is_pass_body(body) -> bool:
    return len(body) == 1 and isinstance(body[0], ast.Pass)


def _string_concat_depth(node, depth=0) -> int:
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        left = _string_concat_depth(node.left, depth + 1)
        right = _string_concat_depth(node.right, depth + 1)
        return max(left, right)
    return depth


# ============================================================
# 4. URL / IP Extraction
# ============================================================

def extract_urls(content: str) -> List[Dict]:
    """Extract all URLs from content."""
    url_pattern = re.compile(
        r'https?://[^\s"\'<>\)\]\}\\]{4,}',
        re.IGNORECASE
    )
    results = []
    seen = set()
    for match in url_pattern.finditer(content):
        url = match.group().rstrip('.,;:')
        if url not in seen:
            seen.add(url)
            line_num = content[:match.start()].count('\n') + 1
            results.append({
                "url": url,
                "line": line_num,
                "risk": _classify_url_risk(url),
            })
    return results


def _classify_url_risk(url: str) -> str:
    """Heuristic risk classification of a URL."""
    low_risk_domains = {
        "github.com", "raw.githubusercontent.com", "api.github.com",
        "pypi.org", "npmjs.com", "registry.npmjs.org",
        "docs.python.org", "stackoverflow.com",
        "cdn.jsdelivr.net", "cdnjs.cloudflare.com",
        "unpkg.com",
    }
    url_lower = url.lower()
    from urllib.parse import urlparse
    try:
        parsed = urlparse(url)
        domain = parsed.hostname or ""
    except Exception:
        return "unparseable"

    if domain in low_risk_domains:
        return "low"
    if re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', domain):
        return "high"  # IP-based URL
    if domain.endswith('.onion'):
        return "critical"
    if any(x in domain for x in ['ngrok', 'localtunnel', 'serveo', 'bore.pub']):
        return "high"
    return "medium"  # Unknown domain, needs review


def extract_ips(content: str) -> List[Dict]:
    """Extract hardcoded IPs."""
    ip_pattern = re.compile(r'\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\b')
    safe_ips = {'127.0.0.1', '0.0.0.0', '255.255.255.255', '255.255.255.0'}
    results = []
    seen = set()
    for match in ip_pattern.finditer(content):
        ip = match.group()
        if ip not in seen and ip not in safe_ips:
            seen.add(ip)
            line_num = content[:match.start()].count('\n') + 1
            results.append({"ip": ip, "line": line_num})
    return results


# ============================================================
# 5. Permission Scope Inference
# ============================================================

def infer_permissions(content: str, all_findings: list) -> Dict:
    """Infer what permissions this skill requires based on content analysis."""
    perms = {
        "file_read": [],
        "file_write": [],
        "network": [],
        "commands": [],
        "env_vars": [],
        "packages": [],
    }

    # File read patterns — require path-like argument
    for m in re.finditer(r'(?:^|\s)(?:open|read_text|read_bytes|Path)\s*\(\s*["\']([~/\w][^"\']*)', content, re.MULTILINE):
        path_arg = m.group(1)
        if '/' in path_arg or '~' in path_arg or path_arg.endswith(('.md', '.txt', '.json', '.yaml', '.yml', '.py', '.sh', '.env', '.cfg', '.conf', '.toml')):
            perms["file_read"].append(path_arg)
    for m in re.finditer(r'(?:^|\s)cat\s+((?:/|~|\.\.?/)\S+)', content, re.MULTILINE):
        perms["file_read"].append(m.group(1))

    # File write patterns — require path-like argument with explicit write mode
    for m in re.finditer(r'open\s*\(\s*["\']([~/\w][^"\']*)["\'].*["\'][wa]', content):
        perms["file_write"].append(m.group(1))
    # Shell redirects — only match when preceded by a command-like context
    for m in re.finditer(r'(?:^|\|)\s*\S+[^-]\s*(?:>>?)\s*((?:/|~|\.\.?/)\S+)', content, re.MULTILINE):
        perms["file_write"].append(m.group(1))

    # Network
    urls = extract_urls(content)
    perms["network"] = list(set(u["url"] for u in urls))

    # Commands
    for m in re.finditer(r'(?:subprocess\.(?:run|call|Popen|check_output))\s*\(\s*\[?\s*["\']([^"\']+)', content):
        perms["commands"].append(m.group(1))
    for m in re.finditer(r'os\.system\s*\(\s*["\']([^"\']+)', content):
        perms["commands"].append(m.group(1))

    # Environment variables
    for m in re.finditer(r'os\.environ(?:\.get)?\s*\[?\s*\(?\s*["\']([^"\']+)', content):
        perms["env_vars"].append(m.group(1))

    # Packages — match actual install commands, not references in docs
    for m in re.finditer(r'(?:^|\s|&&|\|\|)(?:pip3?|python3?\s+-m\s+pip)\s+install\s+(?!-r\b)([a-zA-Z][\w.-]+)', content, re.MULTILINE):
        perms["packages"].append(m.group(1))
    for m in re.finditer(r'(?:^|\s|&&|\|\|)npm\s+install\s+(?!--save-dev)([a-zA-Z@][\w./@-]+)', content, re.MULTILINE):
        perms["packages"].append(m.group(1))

    # Deduplicate
    for k in perms:
        perms[k] = sorted(set(perms[k]))

    return perms


# ============================================================
# 6. Risk Scoring
# ============================================================

SEVERITY_SCORES = {
    "critical": 25,
    "high": 15,
    "medium": 8,
    "low": 3,
    "info": 1,
}

def compute_risk_score(pattern_findings: list, ast_findings: list, entropy_findings: list) -> Tuple[int, str]:
    """
    Compute a quantitative risk score (0-100+).
    Returns (score, risk_level).
    """
    score = 0

    for f in pattern_findings:
        score += SEVERITY_SCORES.get(f["severity"], 0)

    for f in ast_findings:
        score += SEVERITY_SCORES.get(f.severity, 0)

    for f in entropy_findings:
        if f["entropy"] > 5.5:
            score += 10
        elif f["entropy"] > 5.0:
            score += 5
        else:
            score += 2

    if score == 0:
        return 0, "CLEAN"
    elif score <= 15:
        return score, "LOW"
    elif score <= 40:
        return score, "MEDIUM"
    elif score <= 80:
        return score, "HIGH"
    else:
        return score, "EXTREME"


# ============================================================
# 7. File Scanner
# ============================================================

BINARY_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.ico', '.woff', '.woff2',
                     '.ttf', '.eot', '.mp3', '.mp4', '.zip', '.tar', '.gz', '.bz2',
                     '.pyc', '.pyo', '.so', '.dylib', '.dll', '.exe'}

SCANNABLE_EXTENSIONS = {'.md', '.py', '.sh', '.bash', '.js', '.ts', '.json', '.yaml',
                        '.yml', '.toml', '.cfg', '.ini', '.txt', '.html', '.css',
                        '.env', '.conf', '.xml', '.rb', '.go', '.rs', '.lua', ''}


@dataclass
class FileReport:
    path: str
    size: int
    sha256: str
    pattern_findings: List[Dict] = field(default_factory=list)
    ast_findings: List[ASTFinding] = field(default_factory=list)
    entropy_findings: List[Dict] = field(default_factory=list)
    urls: List[Dict] = field(default_factory=list)
    ips: List[Dict] = field(default_factory=list)


@dataclass
class ScanReport:
    skill_name: str
    scan_time: str
    scanner_version: str
    skill_path: str
    total_files: int
    files_scanned: int
    files_skipped: List[str]
    file_reports: List[FileReport]
    permissions: Dict
    risk_score: int
    risk_level: str
    verdict: str
    summary: Dict


def scan_file(filepath: str) -> Optional[FileReport]:
    """Scan a single file."""
    path = Path(filepath)

    if path.suffix.lower() in BINARY_EXTENSIONS:
        return None

    if path.suffix.lower() not in SCANNABLE_EXTENSIONS and path.suffix != '':
        return None

    try:
        content = path.read_text(encoding='utf-8', errors='replace')
    except Exception:
        return None

    file_hash = hashlib.sha256(content.encode()).hexdigest()

    report = FileReport(
        path=str(path),
        size=len(content),
        sha256=file_hash,
    )

    # Parse markdown context for .md files (false positive reduction)
    md_ctx = None
    if path.suffix.lower() == '.md':
        md_ctx = parse_markdown_context(content)

    # Safe IPs to exclude from NET-001
    _SAFE_IPS = {'127.0.0.1', '0.0.0.0', '255.255.255.255', '255.255.255.0',
                 '10.0.0.0', '172.16.0.0', '192.168.0.0'}
    _SAFE_IP_PREFIXES = ('127.', '0.0.0.', '255.255.')

    # Pattern matching
    for rule, compiled in COMPILED_RULES:
        for match in compiled.finditer(content):
            matched_text = match.group()

            # Post-filter: skip safe IPs for NET-001
            if rule.id == "NET-001":
                ip = matched_text.strip()
                if ip in _SAFE_IPS or any(ip.startswith(p) for p in _SAFE_IP_PREFIXES):
                    continue

            line_num = content[:match.start()].count('\n') + 1
            finding = {
                "rule_id": rule.id,
                "category": rule.category,
                "severity": rule.severity,
                "line": line_num,
                "match": matched_text[:100],
                "description": rule.description,
                "context": rule.context,
                "false_positive_hint": rule.false_positive_hint,
                "in_documentation": False,
            }
            # Apply markdown context adjustment
            if md_ctx is not None:
                finding = adjust_finding_for_context(finding, md_ctx)
            report.pattern_findings.append(finding)

    # Deduplicate: same rule + same line + same match = keep only first
    seen = set()
    deduped = []
    for f in report.pattern_findings:
        key = (f["rule_id"], f["line"], f["match"])
        if key not in seen:
            seen.add(key)
            deduped.append(f)
    report.pattern_findings = deduped

    # AST analysis for Python files
    if path.suffix == '.py':
        report.ast_findings = analyze_python_ast(str(path), content)

    # Entropy analysis
    report.entropy_findings = detect_high_entropy_strings(content, filepath=filepath)

    # URL and IP extraction
    report.urls = extract_urls(content)
    report.ips = extract_ips(content)

    return report


def scan_skill(skill_path: str, whitelist: Optional[WhitelistConfig] = None,
               _whitelist_explicit: bool = False) -> ScanReport:
    """Scan an entire skill directory or a single file.

    Parameters
    ----------
    skill_path : str
        Path to the skill directory or a single file.
    whitelist : WhitelistConfig or None
        Pre-loaded whitelist.  When *None*, one is auto-detected from the
        skill directory.
    _whitelist_explicit : bool
        If *True* the whitelist was provided via the ``-w`` CLI flag and
        is therefore trusted (full suppression).  When *False* **and** the
        whitelist was found inside the skill directory itself, findings are
        only downgraded to ``info`` (not removed) to prevent a malicious
        skill from silencing the scanner.
    """
    path = Path(skill_path)
    scanner_version = "1.2.0"
    scan_time = datetime.now().astimezone().isoformat()

    # Determine skill name
    if path.is_file():
        skill_name = path.stem
        files_to_scan = [path]
    else:
        skill_name = path.name
        files_to_scan = sorted(path.rglob('*'))

    # Track whether whitelist came from inside the skill
    skill_bundled_whitelist = False

    # Load whitelist config if not provided
    if whitelist is None:
        whitelist, skill_bundled_whitelist = load_whitelist(str(path))
    elif not _whitelist_explicit:
        # Caller passed a whitelist but didn't mark it explicit — treat as
        # skill-bundled for safety.
        skill_bundled_whitelist = True

    file_reports = []
    files_skipped = []
    all_content = ""
    whitelist_suppressed = 0

    for f in files_to_scan:
        if not f.is_file():
            continue
        report = scan_file(str(f))
        if report:
            # Apply whitelist to pattern findings
            original_count = len(report.pattern_findings)
            if skill_bundled_whitelist:
                # Skill-bundled whitelist: downgrade to info instead of removing
                report.pattern_findings = _apply_whitelist_downgrade(
                    report.pattern_findings, whitelist, filepath=str(f)
                )
                whitelist_suppressed += original_count - len(report.pattern_findings)
            else:
                report.pattern_findings = apply_whitelist(
                    report.pattern_findings, whitelist, filepath=str(f)
                )
                whitelist_suppressed += original_count - len(report.pattern_findings)

            # Apply whitelist to URL findings (trusted domains)
            if whitelist.trusted_domains:
                report.urls = [
                    u for u in report.urls
                    if not any(d in u.get("url", "") for d in whitelist.trusted_domains)
                ]

            file_reports.append(report)
            try:
                all_content += f.read_text(encoding='utf-8', errors='replace') + "\n"
            except:
                pass
        else:
            files_skipped.append(str(f))

    # Aggregate findings
    all_pattern = []
    all_ast = []
    all_entropy = []
    for fr in file_reports:
        all_pattern.extend(fr.pattern_findings)
        all_ast.extend(fr.ast_findings)
        all_entropy.extend(fr.entropy_findings)

    # ----- IOC threat intelligence matching -----
    ioc_match_count = 0

    # Collect all extracted IPs and URLs across files
    all_ips_extracted = set()
    all_urls_extracted: List[Dict] = []
    all_file_hashes: Dict[str, str] = {}  # hash -> filepath
    for fr in file_reports:
        for ip_info in fr.ips:
            all_ips_extracted.add(ip_info["ip"])
        all_urls_extracted.extend(fr.urls)
        all_file_hashes[fr.sha256.lower()] = fr.path

    # IOC-001: Check extracted IPs against C2 list
    c2_ips = load_c2_ips()
    for fr in file_reports:
        for ip_info in fr.ips:
            if ip_info["ip"].lower() in c2_ips:
                finding = {
                    "rule_id": "IOC-001",
                    "category": "ioc",
                    "severity": "critical",
                    "description": "Known C2 IP address detected",
                    "context": f"IP {ip_info['ip']} matches threat intelligence C2 feed",
                    "file": fr.path,
                    "line": ip_info.get("line", 0),
                    "matched_text": ip_info["ip"],
                    "in_documentation": False,
                }
                all_pattern.append(finding)
                ioc_match_count += 1

    # IOC-002: Check extracted URLs against malicious domains
    mal_domains = load_malicious_domains()
    if mal_domains:
        from urllib.parse import urlparse as _urlparse
        for fr in file_reports:
            for url_info in fr.urls:
                try:
                    parsed = _urlparse(url_info["url"])
                    host = (parsed.hostname or "").lower()
                    # Check full host and also path-prefixed form for github etc
                    url_lower = url_info["url"].lower()
                    matched_domain = None
                    for md in mal_domains:
                        if md in url_lower or host == md:
                            matched_domain = md
                            break
                    if matched_domain:
                        finding = {
                            "rule_id": "IOC-002",
                            "category": "ioc",
                            "severity": "critical",
                            "description": "Known malicious domain detected",
                            "context": f"URL contains malicious domain: {matched_domain}",
                            "file": fr.path,
                            "line": url_info.get("line", 0),
                            "matched_text": url_info["url"][:100],
                            "in_documentation": False,
                        }
                        all_pattern.append(finding)
                        ioc_match_count += 1
                except Exception:
                    pass

    # IOC-003: Check skill name against malicious publishers
    mal_publishers = load_malicious_publishers()
    if skill_name.lower() in mal_publishers:
        finding = {
            "rule_id": "IOC-003",
            "category": "ioc",
            "severity": "critical",
            "description": "Known malicious publisher",
            "context": f"Skill name '{skill_name}' matches known malicious publisher",
            "file": str(path),
            "line": 0,
            "matched_text": skill_name,
            "in_documentation": False,
        }
        all_pattern.append(finding)
        ioc_match_count += 1

    # IOC-004: Check file hashes against malicious hash list
    mal_hashes = load_malicious_hashes()
    for fhash, fpath_str in all_file_hashes.items():
        if fhash in mal_hashes:
            finding = {
                "rule_id": "IOC-004",
                "category": "ioc",
                "severity": "critical",
                "description": "Known malicious file hash",
                "context": f"File hash {fhash[:16]}... matches known malware",
                "file": fpath_str,
                "line": 0,
                "matched_text": fhash,
                "in_documentation": False,
            }
            all_pattern.append(finding)
            ioc_match_count += 1

    # IOC-005: Check skill name against malicious skill name patterns
    skill_patterns = load_malicious_skill_patterns()
    for pat in skill_patterns:
        if pat.search(skill_name):
            finding = {
                "rule_id": "IOC-005",
                "category": "ioc",
                "severity": "high",
                "description": "Skill name matches known attack pattern",
                "context": f"Skill name '{skill_name}' matches pattern: {pat.pattern}",
                "file": str(path),
                "line": 0,
                "matched_text": skill_name,
                "in_documentation": False,
            }
            all_pattern.append(finding)
            ioc_match_count += 1
            break  # one match is enough

    # META-001: Warn if the skill ships its own whitelist
    if skill_bundled_whitelist:
        meta_finding = {
            "rule_id": "META-001",
            "category": "meta",
            "severity": "high",
            "description": "Skill ships its own .vetterrc whitelist \u2014 findings may be suppressed",
            "context": "A malicious skill can silence the scanner by bundling a permissive whitelist",
            "file": str(path),
            "line": 0,
            "matched_text": ".vetterrc",
            "in_documentation": False,
        }
        all_pattern.append(meta_finding)

    # Compute risk
    risk_score, risk_level = compute_risk_score(all_pattern, all_ast, all_entropy)

    # Infer permissions
    permissions = infer_permissions(all_content, all_pattern)

    # Verdict
    if risk_level == "CLEAN":
        verdict = "SAFE_TO_INSTALL"
    elif risk_level == "LOW":
        verdict = "SAFE_TO_INSTALL"
    elif risk_level == "MEDIUM":
        verdict = "INSTALL_WITH_CAUTION"
    elif risk_level == "HIGH":
        verdict = "HUMAN_REVIEW_REQUIRED"
    else:
        verdict = "DO_NOT_INSTALL"

    # Summary stats
    severity_counts = Counter(f["severity"] for f in all_pattern)
    severity_counts.update(Counter(f.severity for f in all_ast))
    category_counts = Counter(f["category"] for f in all_pattern)
    category_counts.update(Counter(f.category for f in all_ast))

    doc_downgraded = sum(1 for f in all_pattern if f.get("in_documentation"))

    summary = {
        "findings_by_severity": dict(severity_counts),
        "findings_by_category": dict(category_counts),
        "total_findings": len(all_pattern) + len(all_ast),
        "doc_downgraded": doc_downgraded,
        "whitelist_suppressed": whitelist_suppressed,
        "high_entropy_strings": len(all_entropy),
        "external_urls": len(set(u["url"] for fr in file_reports for u in fr.urls)),
        "hardcoded_ips": len(set(ip["ip"] for fr in file_reports for ip in fr.ips)),
        "ioc_matches": ioc_match_count,
    }

    return ScanReport(
        skill_name=skill_name,
        scan_time=scan_time,
        scanner_version=scanner_version,
        skill_path=str(path),
        total_files=len(files_to_scan) if path.is_dir() else 1,
        files_scanned=len(file_reports),
        files_skipped=files_skipped,
        file_reports=file_reports,
        permissions=permissions,
        risk_score=risk_score,
        risk_level=risk_level,
        verdict=verdict,
        summary=summary,
    )


# ============================================================
# 8. Output Formatters
# ============================================================

RISK_ICONS = {
    "CLEAN": "🟢",
    "LOW": "🟢",
    "MEDIUM": "🟡",
    "HIGH": "🔴",
    "EXTREME": "⛔",
}

VERDICT_ICONS = {
    "SAFE_TO_INSTALL": "✅",
    "INSTALL_WITH_CAUTION": "⚠️",
    "HUMAN_REVIEW_REQUIRED": "🔴",
    "DO_NOT_INSTALL": "❌",
}


def format_text_report(report: ScanReport, verbose: bool = False) -> str:
    """Format scan report as human-readable text."""
    lines = []
    ri = RISK_ICONS.get(report.risk_level, "?")
    vi = VERDICT_ICONS.get(report.verdict, "?")

    lines.append("╔═══════════════════════════════════════════════════════╗")
    lines.append("║          SAFE-SKILL — SECURITY SCAN REPORT           ║")
    lines.append("╚═══════════════════════════════════════════════════════╝")
    lines.append("")
    lines.append(f"  Skill:     {report.skill_name}")
    lines.append(f"  Path:      {report.skill_path}")
    lines.append(f"  Scanned:   {report.scan_time}")
    lines.append(f"  Scanner:   v{report.scanner_version}")
    lines.append(f"  Files:     {report.files_scanned} scanned / {report.total_files} total")
    lines.append("")
    lines.append("───────────────────────────────────────────────────────")
    lines.append(f"  RISK SCORE:  {report.risk_score}/100+    {ri} {report.risk_level}")
    lines.append(f"  VERDICT:     {vi} {report.verdict.replace('_', ' ')}")
    lines.append("───────────────────────────────────────────────────────")

    # Summary
    if report.summary["total_findings"] > 0:
        lines.append("")
        lines.append("  FINDINGS SUMMARY")
        lines.append("  ─────────────────")
        for sev in ["critical", "high", "medium", "low", "info"]:
            count = report.summary["findings_by_severity"].get(sev, 0)
            if count > 0:
                icon = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🔵", "info": "⚪"}.get(sev, "")
                lines.append(f"    {icon} {sev.upper():10s}  {count}")
        lines.append("")
        lines.append("  By Category:")
        for cat, count in sorted(report.summary["findings_by_category"].items(), key=lambda x: -x[1]):
            lines.append(f"    • {cat:20s}  {count}")

    if report.summary["high_entropy_strings"] > 0:
        lines.append(f"\n  ⚠  High-entropy strings detected: {report.summary['high_entropy_strings']}")
    if report.summary.get("doc_downgraded", 0) > 0:
        lines.append(f"  📝 Documentation context (downgraded): {report.summary['doc_downgraded']}")
    if report.summary.get("whitelist_suppressed", 0) > 0:
        lines.append(f"  🔕 Whitelist suppressed: {report.summary['whitelist_suppressed']}")
    if report.summary["external_urls"] > 0:
        lines.append(f"  🌐 External URLs found: {report.summary['external_urls']}")
    if report.summary["hardcoded_ips"] > 0:
        lines.append(f"  📡 Hardcoded IPs found: {report.summary['hardcoded_ips']}")
    if report.summary.get("ioc_matches", 0) > 0:
        lines.append(f"  🛡  IOC threat intel matches: {report.summary['ioc_matches']}")

    # Detailed findings
    lines.append("")
    lines.append("═══════════════════════════════════════════════════════")
    lines.append("  DETAILED FINDINGS")
    lines.append("═══════════════════════════════════════════════════════")

    for fr in report.file_reports:
        has_findings = fr.pattern_findings or fr.ast_findings or fr.entropy_findings
        if not has_findings and not verbose:
            continue

        rel_path = fr.path
        lines.append(f"\n  📄 {rel_path}  ({fr.size} bytes, sha256:{fr.sha256[:16]}...)")

        if not has_findings:
            lines.append("     ✅ Clean")
            continue

        # Pattern findings
        for f in sorted(fr.pattern_findings, key=lambda x: SEVERITY_SCORES.get(x["severity"], 0), reverse=True):
            sev_icon = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🔵", "info": "⚪"}.get(f["severity"], "⚪")
            doc_tag = " [DOC]" if f.get("in_documentation") else ""
            lines.append(f"     {sev_icon} [{f['rule_id']}] L{f['line']}: {f['description']}{doc_tag}")
            lines.append(f"        Match: {f['match'][:80]}")
            if f.get("context"):
                lines.append(f"        Why:   {f['context']}")
            if verbose and f.get("false_positive_hint"):
                lines.append(f"        Note:  {f['false_positive_hint']}")

        # AST findings
        for f in fr.ast_findings:
            sev_icon = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🔵"}.get(f.severity, "⚪")
            lines.append(f"     {sev_icon} [AST] L{f.line}: {f.description}")

        # Entropy findings
        for f in fr.entropy_findings:
            lines.append(f"     ⚠  [ENTROPY] L{f['line']}: {f['type']} (entropy={f['entropy']}, len={f['length']})")
            lines.append(f"        Preview: {f['preview']}")

    # Permissions
    lines.append("")
    lines.append("═══════════════════════════════════════════════════════")
    lines.append("  INFERRED PERMISSIONS")
    lines.append("═══════════════════════════════════════════════════════")
    for perm_type, values in report.permissions.items():
        if values:
            lines.append(f"\n  {perm_type}:")
            for v in values[:20]:
                lines.append(f"    • {v}")
            if len(values) > 20:
                lines.append(f"    ... and {len(values) - 20} more")

    has_any_perms = any(v for v in report.permissions.values())
    if not has_any_perms:
        lines.append("\n  None detected — skill appears to be prompt-only.")

    # URLs
    all_urls = []
    for fr in report.file_reports:
        all_urls.extend(fr.urls)
    if all_urls:
        lines.append("")
        lines.append("═══════════════════════════════════════════════════════")
        lines.append("  EXTERNAL URLS")
        lines.append("═══════════════════════════════════════════════════════")
        for u in sorted(all_urls, key=lambda x: {"critical": 0, "high": 1, "medium": 2, "low": 3}.get(x["risk"], 4)):
            risk_icon = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}.get(u["risk"], "⚪")
            lines.append(f"  {risk_icon} [{u['risk'].upper():8s}] L{u['line']}: {u['url'][:80]}")

    # Footer
    lines.append("")
    lines.append("═══════════════════════════════════════════════════════")
    lines.append(f"  {ri} FINAL: Risk={report.risk_score} Level={report.risk_level} → {vi} {report.verdict.replace('_', ' ')}")
    lines.append("═══════════════════════════════════════════════════════")
    lines.append("")

    return "\n".join(lines)


def to_json(report: ScanReport) -> str:
    """Convert report to JSON."""
    def _serialize(obj):
        if isinstance(obj, ASTFinding):
            return {"line": obj.line, "severity": obj.severity, "category": obj.category, "description": obj.description}
        if isinstance(obj, FileReport):
            return {
                "path": obj.path, "size": obj.size, "sha256": obj.sha256,
                "pattern_findings": obj.pattern_findings,
                "ast_findings": [_serialize(f) for f in obj.ast_findings],
                "entropy_findings": obj.entropy_findings,
                "urls": obj.urls, "ips": obj.ips,
            }
        if isinstance(obj, ScanReport):
            return {
                "skill_name": obj.skill_name, "scan_time": obj.scan_time,
                "scanner_version": obj.scanner_version, "skill_path": obj.skill_path,
                "total_files": obj.total_files, "files_scanned": obj.files_scanned,
                "files_skipped": obj.files_skipped,
                "file_reports": [_serialize(fr) for fr in obj.file_reports],
                "permissions": obj.permissions,
                "risk_score": obj.risk_score, "risk_level": obj.risk_level,
                "verdict": obj.verdict, "summary": obj.summary,
            }
        return str(obj)

    return json.dumps(_serialize(report), indent=2, ensure_ascii=False)


# ============================================================
# 9. Environment Security Check
# ============================================================

_PROMPT_INJECTION_RE = re.compile(
    r'ignore\s+previous\s+instructions|ignore\s+all\s+previous|disregard.*previous|'
    r'override.*instruction|new\s+system\s+prompt|forget.*previous|you\s+are\s+now|'
    r'pretend\s+to\s+be|from\s+now\s+on.*ignore',
    re.IGNORECASE,
)

_API_KEY_RE = re.compile(
    r'(?:sk-ant-[A-Za-z0-9_-]{10,}|sk-proj-[A-Za-z0-9_-]{10,}|'
    r'sk-[A-Za-z0-9_-]{20,}|xoxb-[A-Za-z0-9_-]{10,}|xoxp-[A-Za-z0-9_-]{10,})',
)

_REVERSE_SHELL_RE = re.compile(
    r'(?:bash\s+-i\s+>&|/dev/tcp/|nc\s+-e|ncat\s+-e|mkfifo|'
    r'python[23]?\s+-c\s+["\']import\s+socket|'
    r'perl\s+-e\s+["\']use\s+Socket|'
    r'ruby\s+-rsocket|'
    r'socket\.connect\s*\()',
    re.IGNORECASE,
)

_SUSPICIOUS_CRON_RE = re.compile(
    r'openclaw|clawdbot',
    re.IGNORECASE,
)

_PLANTED_EXECUTABLES = {"node", "python3", "python", "bash", "curl", "git"}


def env_check(openclaw_home: Optional[str] = None, json_output: bool = False) -> dict:
    """Perform OpenClaw environment security checks.

    Returns a dict with check results suitable for JSON serialization or text display.
    """
    if openclaw_home is None:
        openclaw_home = str(Path.home() / ".openclaw")
    oc_path = Path(openclaw_home)

    checks: List[Dict] = []
    scan_time = datetime.now().astimezone().isoformat()

    def _add(check_name: str, severity: str, status: str, detail: str, file: str = ""):
        checks.append({
            "check": check_name,
            "severity": severity,
            "status": status,
            "detail": detail,
            "file": file,
        })

    # ── 1. Credential file permissions ───────────────────────
    check_name = "credential_permissions"
    if oc_path.exists():
        _check_dir_perms(oc_path, check_name, checks, _add)
        for name in ["openclaw.json", "device.json"]:
            fp = oc_path / name
            if fp.exists():
                _check_file_perms(fp, check_name, _add)
        cred_dir = oc_path / "credentials"
        if cred_dir.exists():
            _check_dir_perms(cred_dir, check_name, checks, _add)
            for fp in cred_dir.iterdir():
                if fp.is_file():
                    _check_file_perms(fp, check_name, _add)
        if not any(c["check"] == check_name and c["status"] == "FAIL" for c in checks):
            _add(check_name, "info", "PASS", "Credential file permissions are secure")
    else:
        _add(check_name, "info", "SKIP", f"OpenClaw home not found: {oc_path}")

    # ── 2. Memory file poisoning ─────────────────────────────
    check_name = "memory_poisoning"
    memory_files = ["SOUL.md", "MEMORY.md", "IDENTITY.md"]
    poisoned_found = False
    for mf_name in memory_files:
        mf = oc_path / mf_name
        if not mf.exists():
            continue
        try:
            content = mf.read_text(encoding="utf-8", errors="replace")
            for m in _PROMPT_INJECTION_RE.finditer(content):
                line_num = content[:m.start()].count("\n") + 1
                _add(check_name, "critical", "FAIL",
                     f"Prompt injection at L{line_num}: {m.group()[:80]}",
                     file=str(mf))
                poisoned_found = True
        except Exception:
            pass
    if not poisoned_found:
        _add(check_name, "info", "PASS", "No prompt injection found in memory files")

    # ── 3. API key leakage ───────────────────────────────────
    check_name = "api_key_leakage"
    leaked = False
    if oc_path.exists():
        for ext in ("*.md", "*.json"):
            for fp in oc_path.rglob(ext):
                if not fp.is_file():
                    continue
                try:
                    content = fp.read_text(encoding="utf-8", errors="replace")
                    for m in _API_KEY_RE.finditer(content):
                        line_num = content[:m.start()].count("\n") + 1
                        _add(check_name, "critical", "FAIL",
                             f"Exposed API key at L{line_num}: {m.group()[:20]}...",
                             file=str(fp))
                        leaked = True
                except Exception:
                    pass
    if not leaked:
        _add(check_name, "info", "PASS", "No exposed API keys found")

    # ── 4. Installed skill C2/malware scan ───────────────────
    check_name = "installed_skill_scan"
    skills_dir = oc_path / "workspace" / "skills"
    skill_threats = 0
    if skills_dir.exists():
        c2_ips = load_c2_ips()
        mal_domains = load_malicious_domains()
        for skill_dir in skills_dir.iterdir():
            if not skill_dir.is_dir():
                continue
            for fp in skill_dir.rglob("*"):
                if not fp.is_file() or fp.suffix.lower() in BINARY_EXTENSIONS:
                    continue
                try:
                    content = fp.read_text(encoding="utf-8", errors="replace")
                except Exception:
                    continue
                # C2 IPs
                for ip_m in re.finditer(r'\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\b', content):
                    if ip_m.group().lower() in c2_ips:
                        ln = content[:ip_m.start()].count("\n") + 1
                        _add(check_name, "critical", "FAIL",
                             f"C2 IP {ip_m.group()} at L{ln}",
                             file=str(fp))
                        skill_threats += 1
                # Malicious domains
                content_lower = content.lower()
                for md in mal_domains:
                    if md in content_lower:
                        _add(check_name, "critical", "FAIL",
                             f"Malicious domain '{md}' found",
                             file=str(fp))
                        skill_threats += 1
                        break
                # Reverse shells
                for rs_m in _REVERSE_SHELL_RE.finditer(content):
                    ln = content[:rs_m.start()].count("\n") + 1
                    _add(check_name, "high", "FAIL",
                         f"Reverse shell pattern at L{ln}: {rs_m.group()[:60]}",
                         file=str(fp))
                    skill_threats += 1
        if skill_threats == 0:
            _add(check_name, "info", "PASS", "No threats found in installed skills")
    else:
        _add(check_name, "info", "SKIP", f"Skills directory not found: {skills_dir}")

    # ── 5. Persistence mechanism detection ───────────────────
    check_name = "persistence_detection"
    persist_found = False
    # Crontab
    try:
        result = _subprocess.run(
            ["crontab", "-l"], capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0 and result.stdout:
            for i, line in enumerate(result.stdout.splitlines(), 1):
                if _SUSPICIOUS_CRON_RE.search(line):
                    _add(check_name, "high", "FAIL",
                         f"Suspicious crontab entry L{i}: {line.strip()[:80]}",
                         file="crontab")
                    persist_found = True
    except Exception:
        pass

    # LaunchAgents (macOS)
    for la_dir in [Path.home() / "Library" / "LaunchAgents",
                   Path("/Library/LaunchAgents"),
                   Path("/Library/LaunchDaemons")]:
        if la_dir.exists():
            for fp in la_dir.iterdir():
                if fp.is_file():
                    try:
                        content = fp.read_text(encoding="utf-8", errors="replace")
                        if _SUSPICIOUS_CRON_RE.search(content):
                            _add(check_name, "high", "FAIL",
                                 f"Suspicious LaunchAgent: {fp.name}",
                                 file=str(fp))
                            persist_found = True
                    except Exception:
                        pass

    # systemd user units
    systemd_dir = Path.home() / ".config" / "systemd" / "user"
    if systemd_dir.exists():
        for fp in systemd_dir.rglob("*.service"):
            try:
                content = fp.read_text(encoding="utf-8", errors="replace")
                if _SUSPICIOUS_CRON_RE.search(content):
                    _add(check_name, "high", "FAIL",
                         f"Suspicious systemd service: {fp.name}",
                         file=str(fp))
                    persist_found = True
            except Exception:
                pass

    if not persist_found:
        _add(check_name, "info", "PASS", "No suspicious persistence mechanisms found")

    # ── 6. PATH hijacking ────────────────────────────────────
    check_name = "path_hijacking"
    hijack_found = False
    path_dirs = os.environ.get("PATH", "").split(os.pathsep)
    for d in path_dirs:
        dp = Path(d)
        if not dp.exists():
            continue
        # Check if directory is writable
        if not os.access(str(dp), os.W_OK):
            continue
        for exe_name in _PLANTED_EXECUTABLES:
            exe_path = dp / exe_name
            if exe_path.exists() and exe_path.is_file():
                # Check if it's a symlink to somewhere unexpected or a small script
                try:
                    real = exe_path.resolve()
                    # Suspicious if it's in a temp dir, home dir writable location, etc.
                    real_str = str(real).lower()
                    if any(x in real_str for x in ["/tmp/", "/.local/bin/", "/home/", "/users/"]):
                        # Only flag if the writable dir is unusual (not standard system paths)
                        if not str(dp).startswith(("/usr/bin", "/usr/local/bin", "/bin", "/sbin")):
                            _add(check_name, "high", "FAIL",
                                 f"Potentially planted '{exe_name}' in writable PATH dir",
                                 file=str(exe_path))
                            hijack_found = True
                except Exception:
                    pass
    if not hijack_found:
        _add(check_name, "info", "PASS", "No PATH hijacking detected")

    # ── Build result ─────────────────────────────────────────
    fail_count = sum(1 for c in checks if c["status"] == "FAIL")
    critical_count = sum(1 for c in checks if c["status"] == "FAIL" and c["severity"] == "critical")

    result = {
        "scan_type": "env_check",
        "scan_time": scan_time,
        "openclaw_home": str(oc_path),
        "checks": checks,
        "summary": {
            "total_checks": len(checks),
            "passed": sum(1 for c in checks if c["status"] == "PASS"),
            "failed": fail_count,
            "skipped": sum(1 for c in checks if c["status"] == "SKIP"),
            "critical_issues": critical_count,
        },
        "risk_level": "EXTREME" if critical_count > 0 else ("HIGH" if fail_count > 2 else ("MEDIUM" if fail_count > 0 else "CLEAN")),
    }
    return result


def _check_dir_perms(dirpath: Path, check_name: str, checks: list, add_fn):
    """Check that a directory has 700 permissions."""
    try:
        st = dirpath.stat()
        mode = stat.S_IMODE(st.st_mode)
        if mode & 0o077:  # group/other have any access
            add_fn(check_name, "high", "FAIL",
                   f"Directory {dirpath} has insecure permissions: {oct(mode)} (should be 0o700)",
                   file=str(dirpath))
    except Exception:
        pass


def _check_file_perms(filepath: Path, check_name: str, add_fn):
    """Check that a file has 600 permissions."""
    try:
        st = filepath.stat()
        mode = stat.S_IMODE(st.st_mode)
        if mode & 0o077:
            add_fn(check_name, "high", "FAIL",
                   f"File {filepath} has insecure permissions: {oct(mode)} (should be 0o600)",
                   file=str(filepath))
    except Exception:
        pass


def format_env_check_text(result: dict) -> str:
    """Format env_check result as human-readable text."""
    lines = []
    lines.append("╔═══════════════════════════════════════════════════════╗")
    lines.append("║     SAFE-SKILL — ENVIRONMENT SECURITY CHECK          ║")
    lines.append("╚═══════════════════════════════════════════════════════╝")
    lines.append("")
    lines.append(f"  OpenClaw Home: {result['openclaw_home']}")
    lines.append(f"  Scanned:       {result['scan_time']}")
    lines.append("")

    s = result["summary"]
    rl = result["risk_level"]
    ri = RISK_ICONS.get(rl, "?")
    lines.append("───────────────────────────────────────────────────────")
    lines.append(f"  RISK LEVEL:  {ri} {rl}")
    lines.append(f"  Checks:  {s['passed']} passed, {s['failed']} failed, {s['skipped']} skipped")
    if s["critical_issues"] > 0:
        lines.append(f"  🔴 CRITICAL ISSUES: {s['critical_issues']}")
    lines.append("───────────────────────────────────────────────────────")

    # Group by check name
    from collections import OrderedDict
    grouped: Dict[str, List[Dict]] = OrderedDict()
    for c in result["checks"]:
        grouped.setdefault(c["check"], []).append(c)

    for check_name, items in grouped.items():
        lines.append(f"\n  [{check_name.upper().replace('_', ' ')}]")
        for c in items:
            status_icon = {"PASS": "✅", "FAIL": "❌", "SKIP": "⏭"}.get(c["status"], "?")
            sev_icon = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🔵", "info": "⚪"}.get(c["severity"], "")
            file_str = f"  ({c['file']})" if c.get("file") else ""
            lines.append(f"    {status_icon} {sev_icon} {c['detail']}{file_str}")

    lines.append("")
    lines.append("═══════════════════════════════════════════════════════")
    lines.append(f"  {ri} RESULT: {rl} — {s['failed']} issue(s) found")
    lines.append("═══════════════════════════════════════════════════════")
    lines.append("")
    return "\n".join(lines)


# ============================================================
# 10. CLI Entry Point
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="Safe-Skill — Programmatic Security Scanner for AI Agent Skills"
    )
    parser.add_argument("target", nargs="?", default=None, help="Skill directory or single file to scan")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--output", "-o", help="Write report to file")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show all files including clean ones")
    parser.add_argument("--whitelist", "-w", help="Path to .vetterrc whitelist config (auto-detected in skill dir if not specified)")
    parser.add_argument("--env-check", action="store_true", help="Run environment security check instead of skill scan")
    args = parser.parse_args()

    # ── Environment check mode ───────────────────────────────
    if args.env_check:
        target_dir = args.target if args.target else str(Path.home() / ".openclaw")
        result = env_check(openclaw_home=target_dir, json_output=args.json)

        if args.json:
            output = json.dumps(result, indent=2, ensure_ascii=False)
        else:
            output = format_env_check_text(result)

        if args.output:
            Path(args.output).write_text(output, encoding="utf-8")
            print(f"Report written to {args.output}")
        else:
            print(output)

        rl = result.get("risk_level", "CLEAN")
        if rl in ("HIGH", "EXTREME"):
            sys.exit(2)
        elif rl == "MEDIUM":
            sys.exit(1)
        sys.exit(0)

    # ── Normal skill scan mode ───────────────────────────────
    if args.target is None:
        parser.error("target is required when not using --env-check")

    target = Path(args.target)
    if not target.exists():
        print(f"Error: {target} does not exist", file=sys.stderr)
        sys.exit(1)

    # Load whitelist
    wl = None
    if args.whitelist:
        wl_path = Path(args.whitelist)
        if wl_path.exists():
            try:
                raw = wl_path.read_text(encoding='utf-8')
                data = json.loads(raw) if raw.strip().startswith('{') else _parse_simple_yaml(raw)
                wl = WhitelistConfig(
                    ignore_rules=data.get("ignore_rules", []),
                    ignore_categories=data.get("ignore_categories", []),
                    trusted_domains=data.get("trusted_domains", []),
                    inline_suppressions=data.get("inline_suppressions", []),
                    accept_severity=data.get("accept_severity", ""),
                )
            except Exception as e:
                print(f"Warning: Failed to parse whitelist {wl_path}: {e}", file=sys.stderr)

    report = scan_skill(str(target), whitelist=wl,
                        _whitelist_explicit=bool(args.whitelist))

    if args.json:
        output = to_json(report)
    else:
        output = format_text_report(report, verbose=args.verbose)

    if args.output:
        Path(args.output).write_text(output, encoding='utf-8')
        print(f"Report written to {args.output}")
    else:
        print(output)

    # Exit code reflects risk
    if report.risk_level in ("HIGH", "EXTREME"):
        sys.exit(2)
    elif report.risk_level == "MEDIUM":
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
