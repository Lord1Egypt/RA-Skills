"""
ClawGuard Risk Pattern Definitions
Defines regex patterns and AST checks for dangerous code patterns.
"""

import re
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Pattern:
    """Risk pattern definition"""
    name: str
    category: str
    severity: str  # HIGH, MEDIUM, LOW
    weight: int  # Score weight
    regex: str
    description: str

# Network exfiltration patterns (Weight: 25)
NETWORK_PATTERNS = [
    Pattern(
        name="external_http_post",
        category="network",
        severity="HIGH",
        weight=25,
        regex=r"(fetch|axios|request|curl|wget).*(POST|post).*http[s]?://",
        description="HTTP POST to external URL (potential data exfiltration)"
    ),
    Pattern(
        name="fetch_call",
        category="network",
        severity="MEDIUM",
        weight=15,
        regex=r"\b(fetch|axios|requests\.post|requests\.get|urllib\.request)\s*\(",
        description="Network request detected"
    ),
    Pattern(
        name="curl_command",
        category="network",
        severity="MEDIUM",
        weight=15,
        regex=r"\bcurl\s+(-[A-Za-z]+\s+)*http[s]?://",
        description="curl command to external URL"
    ),
    Pattern(
        name="wget_command",
        category="network",
        severity="MEDIUM",
        weight=15,
        regex=r"\bwget\s+(-[A-Za-z]+\s+)*http[s]?://",
        description="wget command to external URL"
    ),
]

# Credential access patterns (Weight: 20)
CREDENTIAL_PATTERNS = [
    Pattern(
        name="env_token_access",
        category="credential",
        severity="HIGH",
        weight=20,
        regex=r"(process\.env|os\.getenv|ENV)\[?['\"][\w_]*(TOKEN|KEY|SECRET|PASSWORD|API_KEY)['\"]?\]?",
        description="Accesses credential from environment variables"
    ),
    Pattern(
        name="credential_file_read",
        category="credential",
        severity="HIGH",
        weight=20,
        regex=r"(readFile|open|cat|read).*(/\.ssh|/\.aws|/\.config|credentials|\.env)",
        description="Reads credential files"
    ),
    Pattern(
        name="password_in_code",
        category="credential",
        severity="MEDIUM",
        weight=15,
        regex=r"(password|passwd|pwd)\s*[=:]\s*['\"][^'\"]{3,}['\"]",
        description="Hardcoded password detected"
    ),
]

# Shell execution patterns (Weight: 15)
SHELL_PATTERNS = [
    Pattern(
        name="shell_exec",
        category="shell",
        severity="HIGH",
        weight=15,
        regex=r"\b(exec|execSync|spawn|spawnSync|system|popen|subprocess\.run|subprocess\.call)\s*\(",
        description="Shell command execution"
    ),
    Pattern(
        name="shell_injection_risk",
        category="shell",
        severity="HIGH",
        weight=15,
        regex=r"(exec|system|popen)\s*\([^)]*\+[^)]*\)",
        description="Shell command with string concatenation (injection risk)"
    ),
    Pattern(
        name="bash_command",
        category="shell",
        severity="MEDIUM",
        weight=10,
        regex=r"\b(bash|sh|zsh)\s+-c\s+",
        description="Direct bash command execution"
    ),
]

# File destruction patterns (Weight: 15)
FILE_DESTRUCTION_PATTERNS = [
    Pattern(
        name="rm_rf",
        category="file_destruction",
        severity="HIGH",
        weight=15,
        regex=r"\brm\s+-[rfRF]*\s+",
        description="Recursive file deletion (rm -rf)"
    ),
    Pattern(
        name="unlink_call",
        category="file_destruction",
        severity="MEDIUM",
        weight=10,
        regex=r"\b(unlink|unlinkSync|rmdir|rmdirSync|fs\.rm)\s*\(",
        description="File/directory deletion"
    ),
    Pattern(
        name="shutil_rmtree",
        category="file_destruction",
        severity="HIGH",
        weight=15,
        regex=r"\bshutil\.rmtree\s*\(",
        description="Recursive directory deletion (Python)"
    ),
]

# Obfuscation patterns (Weight: 15)
OBFUSCATION_PATTERNS = [
    Pattern(
        name="eval_call",
        category="obfuscation",
        severity="HIGH",
        weight=15,
        regex=r"\beval\s*\(",
        description="Dynamic code execution (eval) - code injection risk"
    ),
    Pattern(
        name="function_constructor",
        category="obfuscation",
        severity="HIGH",
        weight=15,
        regex=r"\bFunction\s*\(",
        description="Dynamic function creation - code injection risk"
    ),
    Pattern(
        name="base64_decode",
        category="obfuscation",
        severity="MEDIUM",
        weight=10,
        regex=r"\b(atob|Buffer\.from|base64\.b64decode)\s*\(",
        description="Base64 decoding (possible obfuscated payload)"
    ),
    Pattern(
        name="hex_decode",
        category="obfuscation",
        severity="MEDIUM",
        weight=10,
        regex=r"(\\x[0-9a-fA-F]{2}){10,}",
        description="Hex-encoded string (possible obfuscation)"
    ),
]

# Hidden file patterns (Weight: 10)
HIDDEN_FILE_PATTERNS = [
    Pattern(
        name="dotfile",
        category="hidden_file",
        severity="LOW",
        weight=10,
        regex=r"^\.",
        description="Hidden file (dotfile) detected"
    ),
    Pattern(
        name="hidden_dir_access",
        category="hidden_file",
        severity="LOW",
        weight=5,
        regex=r"/\.[a-zA-Z0-9_-]+/",
        description="Accesses hidden directory"
    ),
]

# All patterns combined
ALL_PATTERNS: List[Pattern] = (
    NETWORK_PATTERNS
    + CREDENTIAL_PATTERNS
    + SHELL_PATTERNS
    + FILE_DESTRUCTION_PATTERNS
    + OBFUSCATION_PATTERNS
    + HIDDEN_FILE_PATTERNS
)

# URL extraction pattern
URL_PATTERN = re.compile(r'https?://[^\s\'"<>]+')

# Known safe domains (whitelist)
SAFE_DOMAINS = [
    "api.openai.com",
    "api.anthropic.com",
    "api.cohere.ai",
    "api.github.com",
    "registry.npmjs.org",
    "pypi.org",
    "clawhub.com",
    "localhost",
    "127.0.0.1",
]

def extract_urls(content: str) -> List[str]:
    """Extract all URLs from content"""
    return list(set(URL_PATTERN.findall(content)))

def is_safe_domain(url: str) -> bool:
    """Check if URL domain is in whitelist"""
    from urllib.parse import urlparse
    try:
        domain = urlparse(url).netloc
        return any(safe in domain for safe in SAFE_DOMAINS)
    except:
        return False

# Severity weights for scoring
SEVERITY_WEIGHTS = {
    "HIGH": 1.0,
    "MEDIUM": 0.6,
    "LOW": 0.3,
}
