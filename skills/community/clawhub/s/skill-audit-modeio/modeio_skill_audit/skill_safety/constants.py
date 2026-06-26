from __future__ import annotations

import re
from typing import Sequence, Tuple

TOOL_NAME = "skill-audit"
SCAN_VERSION = "skill-safety-assessment-v2"
ENGINE_VERSION = "ssa-engine-2.0.0"
POLICY_VERSION = "ssa-policy-2026.03"

LAYER_STATIC = "L1_STATIC_AST"
LAYER_SECRET = "L2_SECRET_EGRESS"
LAYER_CAPABILITY = "L3_CAPABILITY_CONTRACT"
LAYER_PROMPT = "L4_PROMPT_SEMANTICS"
LAYER_SUPPLY = "L5_SUPPLY_CHAIN"
LAYER_EVASION = "L7_EVASION"

REQUIRED_LAYERS = (
    LAYER_STATIC,
    LAYER_SECRET,
    LAYER_CAPABILITY,
    LAYER_PROMPT,
    LAYER_SUPPLY,
)

DECISION_VALUES = {"reject", "caution", "approve"}
SEVERITY_VALUES = {"low", "medium", "high", "critical"}
CONFIDENCE_VALUES = {"low", "medium", "high"}
CATEGORY_VALUES = {"A", "B", "C", "D", "E"}

SEVERITY_RANK = {
    "critical": 4,
    "high": 3,
    "medium": 2,
    "low": 1,
}

CONFIDENCE_RANK = {
    "high": 3,
    "medium": 2,
    "low": 1,
}

SEVERITY_BASE = {
    "low": 6.0,
    "medium": 12.0,
    "high": 20.0,
    "critical": 30.0,
}

CONFIDENCE_MULT = {
    "low": 0.70,
    "medium": 0.85,
    "high": 1.00,
}

LAYER_MULT = {
    LAYER_STATIC: 1.00,
    LAYER_SECRET: 0.95,
    LAYER_CAPABILITY: 1.00,
    LAYER_PROMPT: 0.75,
    LAYER_SUPPLY: 0.90,
    LAYER_EVASION: 1.05,
}

SKIP_DIR_NAMES = {
    ".git",
    ".hg",
    ".svn",
    ".idea",
    ".vscode",
    "node_modules",
    "dist",
    "build",
    "coverage",
    "__pycache__",
    ".venv",
    "venv",
    ".next",
    ".open-next",
    ".wrangler",
}

TEXT_EXTENSIONS = {
    ".py",
    ".js",
    ".ts",
    ".tsx",
    ".mjs",
    ".cjs",
    ".sh",
    ".bash",
    ".zsh",
    ".ps1",
    ".yml",
    ".yaml",
    ".json",
    ".md",
    ".txt",
    ".html",
    ".htm",
    ".toml",
    ".ini",
    ".cfg",
    ".conf",
    ".env",
    ".lock",
}

EXECUTABLE_EXTENSIONS = {
    ".py",
    ".js",
    ".ts",
    ".tsx",
    ".mjs",
    ".cjs",
    ".sh",
    ".bash",
    ".zsh",
    ".ps1",
}

HIGH_PRIORITY_FILES = {
    "SKILL.md",
    "README.md",
    "AGENTS.md",
    "CLAUDE.md",
    "Makefile",
    "Dockerfile",
    "package.json",
    "pyproject.toml",
    "requirements.txt",
}

PROMPT_SURFACE_FILENAMES = {
    "SKILL.md",
    "README.md",
    "AGENTS.md",
    "CLAUDE.md",
}

PROMPT_SURFACE_HINTS = (
    "prompt",
    "instruction",
    "policy",
    "guardrail",
    "safety",
)

TEST_PATH_PARTS = {
    "tests",
    "test",
    "__tests__",
    "spec",
    "specs",
    "fixtures",
}

MAX_FILE_BYTES = 600_000

PROMPT_OVERRIDE_RULES: Sequence[Tuple[re.Pattern[str], str, str, str, str, str]] = [
    (
        re.compile(r"\bignore\s+(all\s+)?(previous|prior|system)\s+(instructions|prompts?)\b", re.IGNORECASE),
        "A_IGNORE_PREVIOUS_INSTRUCTIONS",
        "high",
        "high",
        "Prompt contains instruction-override language.",
        "Remove override phrase and enforce explicit instruction hierarchy.",
    ),
    (
        re.compile(r"\boverride\s+(system|developer)\s+instructions\b", re.IGNORECASE),
        "A_OVERRIDE_SYSTEM_INSTRUCTIONS",
        "high",
        "high",
        "Prompt attempts to override higher-priority instructions.",
        "Disallow hierarchy inversion and keep system/developer precedence immutable.",
    ),
    (
        re.compile(r"\bbypass\s+(all\s+)?(safety|guardrails?)\b", re.IGNORECASE),
        "A_BYPASS_SAFETY",
        "high",
        "high",
        "Prompt contains explicit safety bypass wording.",
        "Replace with refusal-preserving wording and explicit safe fallback.",
    ),
    (
        re.compile(r"\breveal\s+(your\s+)?(system|developer)\s+prompt\b", re.IGNORECASE),
        "A_PROMPT_EXTRACTION",
        "medium",
        "high",
        "Prompt includes system/developer prompt extraction request.",
        "Remove extraction instructions and add explicit no-disclosure policy.",
    ),
    (
        re.compile(r"\b(user|retrieved)\s+instructions\s+take\s+priority\s+over\s+(system|developer)\b", re.IGNORECASE),
        "A_HIERARCHY_INVERSION",
        "critical",
        "high",
        "Prompt contract inverts instruction precedence.",
        "Restore hierarchy: system > developer > user > external content.",
    ),
    (
        re.compile(r"\bign\w{1,4}e\b.{0,40}\bpre\w{1,6}\b.{0,40}\binstr\w+", re.IGNORECASE),
        "A_TYPOGLYCEMIA_OVERRIDE",
        "medium",
        "medium",
        "Prompt contains obfuscated instruction-override pattern.",
        "Normalize and reject typoglycemia variants of override directives.",
    ),
    (
        re.compile(r"(必须|务必|即刻|立即).{0,32}(执行|调用).{0,48}(run_shell_command|bash|命令)", re.IGNORECASE),
        "A_FORCED_TOOL_EXECUTION_ZH",
        "high",
        "high",
        "Prompt forces immediate tool/command execution.",
        "Replace coercive execution directive with policy-aware, user-confirmed flow.",
    ),
    (
        re.compile(r"(唯一动作|只能|不得回复|禁止闲聊).{0,48}(run_shell_command|执行|调用)", re.IGNORECASE),
        "A_FORCED_TOOL_EXECUTION_ZH",
        "high",
        "medium",
        "Prompt constrains agent to forced command execution behavior.",
        "Allow safe dialogue and explicit policy checks before running commands.",
    ),
    (
        re.compile(
            r"\b(must|immediately|only)\b.{0,24}\b(execute|invoke|call)\b.{0,64}\b(run_shell_command|shell\s+command|bash)\b",
            re.IGNORECASE,
        ),
        "A_FORCED_TOOL_EXECUTION_EN",
        "high",
        "high",
        "Prompt forces immediate command/tool invocation.",
        "Remove forced invocation and add policy gating for command execution.",
    ),
]

EXEC_RULES: Sequence[Tuple[re.Pattern[str], str, str, str, str, str, str]] = [
    (
        re.compile(r"\bsubprocess\.(run|Popen|call|check_call|check_output)\s*\([^\n]*shell\s*=\s*True", re.IGNORECASE),
        LAYER_STATIC,
        "C_SUBPROCESS_SHELL_TRUE",
        "high",
        "high",
        "Shell execution with shell=True increases command injection risk.",
        "Avoid shell=True and pass command arguments as explicit arrays.",
    ),
    (
        re.compile(r"\bos\.system\s*\(", re.IGNORECASE),
        LAYER_STATIC,
        "C_OS_SYSTEM_CALL",
        "medium",
        "medium",
        "Direct shell invocation via os.system is difficult to constrain safely.",
        "Use subprocess with fixed argument vectors and input validation.",
    ),
    (
        re.compile(r"\bchild_process\.(exec|execSync)\s*\(", re.IGNORECASE),
        LAYER_STATIC,
        "C_NODE_EXEC_CALL",
        "high",
        "medium",
        "Node command execution API detected.",
        "Prefer safer process APIs and strict command allowlists.",
    ),
]

DESTRUCTIVE_RULES: Sequence[Tuple[re.Pattern[str], str, str, str, str]] = [
    (
        re.compile(r"\brm\s+-rf\s+--no-preserve-root\b", re.IGNORECASE),
        "C_RM_NO_PRESERVE_ROOT",
        "critical",
        "high",
        "Explicit no-preserve-root recursive deletion command detected.",
    ),
    (
        re.compile(r"\brm\s+-rf\s+/\b", re.IGNORECASE),
        "C_RM_ROOT_RECURSIVE",
        "critical",
        "high",
        "Recursive deletion against filesystem root detected.",
    ),
    (
        re.compile(r"\bmkfs\.[a-z0-9]+\b", re.IGNORECASE),
        "C_FILESYSTEM_FORMAT",
        "critical",
        "high",
        "Filesystem format command detected.",
    ),
    (
        re.compile(r"\bdd\s+if=.*\sof=/dev/", re.IGNORECASE),
        "C_RAW_DEVICE_WRITE",
        "critical",
        "medium",
        "Raw write to block device detected.",
    ),
    (
        re.compile(r"\bchmod\s+777\s+/(etc|bin|usr|var|root)\b", re.IGNORECASE),
        "C_WORLD_WRITABLE_SYSTEM_PATH",
        "high",
        "high",
        "World-writable permission change on sensitive system path.",
    ),
]

DOWNLOAD_EXEC_PATTERN = re.compile(r"\b(curl|wget)\b[^\n]*\|\s*(bash|sh|zsh|pwsh|powershell)\b", re.IGNORECASE)
BASE64_PIPE_PATTERN = re.compile(r"\bbase64\s+(-d|--decode)\b[^\n]*\|\s*(bash|sh|zsh|pwsh|powershell)\b", re.IGNORECASE)
POWERSHELL_ENCODED_PATTERN = re.compile(r"\bpowershell(\.exe)?\b[^\n]*\s-(enc|encodedcommand)\b", re.IGNORECASE)
PY_DYNAMIC_EXEC_PATTERN = re.compile(r"\bexec\s*\(\s*base64\.b64decode\s*\(", re.IGNORECASE)
JS_DYNAMIC_EVAL_PATTERN = re.compile(r"\b(eval|Function)\s*\(.*Buffer\.from\s*\(.*base64", re.IGNORECASE)
UNICODE_TAG_BUILD_PATTERN = re.compile(
    r"(chr\s*\(\s*0xE0000\s*\+|fromCodePoint\s*\(\s*0xE0000)",
    re.IGNORECASE,
)
UNICODE_TAG_RANGE_PATTERN = re.compile(r"(U\+E0{3}[0-9A-F]{1,2}|0xE0{3}[0-9A-F]{1,2}|\\uE0{3}[0-9A-F]{1,2})", re.IGNORECASE)
PROMPT_STEGO_PATTERN = re.compile(r"\b(embed|extract|hide)_?prompt\b", re.IGNORECASE)
STEGO_TECHNIQUE_PATTERN = re.compile(
    r"(least\s+significant\s+bits|steganograph|zero-width|hidden\s+prompt)",
    re.IGNORECASE,
)

ENV_SOURCE_PATTERNS = [
    re.compile(r"\bos\.environ\b(?!\s*(\.get|\[))", re.IGNORECASE),
    re.compile(r"\bprocess\.env\b(?!\s*(\.|\[))", re.IGNORECASE),
    re.compile(r"\bdict\s*\(\s*os\.environ\s*\)", re.IGNORECASE),
    re.compile(r"\bObject\.entries\s*\(\s*process\.env\s*\)", re.IGNORECASE),
    re.compile(r"\bprintenv\b", re.IGNORECASE),
]

NETWORK_SINK_PATTERNS = [
    re.compile(r"\brequests\.(post|get|put|patch|request)\s*\(", re.IGNORECASE),
    re.compile(r"\bhttpx\.(post|get|put|patch|request)\s*\(", re.IGNORECASE),
    re.compile(r"\burllib\.request\b", re.IGNORECASE),
    re.compile(r"\burlopen\s*\(", re.IGNORECASE),
    re.compile(r"\bfetch\s*\(", re.IGNORECASE),
    re.compile(r"\baxios\.(post|get|put|patch|request)\s*\(", re.IGNORECASE),
    re.compile(r"\bInvoke-WebRequest\b", re.IGNORECASE),
    re.compile(r"\bcurl\b[^\n]*https?://", re.IGNORECASE),
    re.compile(r"\bwget\b[^\n]*https?://", re.IGNORECASE),
    re.compile(r"\bsocket\.connect\s*\(", re.IGNORECASE),
    re.compile(r"\b[a-zA-Z_][a-zA-Z0-9_]*\.connect\s*\(", re.IGNORECASE),
    re.compile(r"\b[a-zA-Z_][a-zA-Z0-9_]*\.send(all)?\s*\(", re.IGNORECASE),
    re.compile(r"\bhttp\.request\s*\(", re.IGNORECASE),
]

SYSTEM_ENUM_PATTERNS = [
    re.compile(r"\bos\.userInfo\s*\(", re.IGNORECASE),
    re.compile(r"\bos\.hostname\s*\(", re.IGNORECASE),
    re.compile(r"\bos\.platform\s*\(", re.IGNORECASE),
    re.compile(r"\bprocess\.version\b", re.IGNORECASE),
    re.compile(r"\bos\.release\s*\(", re.IGNORECASE),
    re.compile(r"\bos\.arch\s*\(", re.IGNORECASE),
]

SUSPICIOUS_EGRESS_PATTERNS = [
    re.compile(r"discord(?:app)?\.com/api/webhooks", re.IGNORECASE),
    re.compile(r"pastebin", re.IGNORECASE),
    re.compile(r"requestbin", re.IGNORECASE),
    re.compile(r"ngrok", re.IGNORECASE),
    re.compile(r"telegram", re.IGNORECASE),
    re.compile(r"webhook", re.IGNORECASE),
]

EXTERNAL_URL_PATTERN = re.compile(r"https?://(?!localhost\b|127\.0\.0\.1\b|0\.0\.0\.0\b)[^\s\"'`]+", re.IGNORECASE)

INSTALL_HOOK_NAMES = {
    "preinstall",
    "install",
    "postinstall",
    "prepare",
    "prepublish",
    "prepack",
    "postpack",
}

HOOK_RISK_PATTERNS = [
    DOWNLOAD_EXEC_PATTERN,
    re.compile(r"\b(node|python|ruby|perl)\s+-e\b", re.IGNORECASE),
    re.compile(r"\brm\s+-rf\b", re.IGNORECASE),
    re.compile(r"\bchmod\s+777\b", re.IGNORECASE),
]

INSTALL_HOOK_LOCAL_SCRIPT_PATTERN = re.compile(
    r"^\s*(node|python3?|bash|sh|pwsh|powershell)\s+[\"']?([A-Za-z0-9_./\\-]+(?:\.[A-Za-z0-9_]+)?)",
    re.IGNORECASE,
)

HOOK_TARGET_SPLIT_PATTERN = re.compile(r"\s*(?:&&|\|\||;)\s*")
HOOK_TARGET_SKIP_PREFIXES = ("npm", "pnpm", "yarn", "bun")

HOOK_TARGET_EXEC_PATTERNS = [
    re.compile(r"\bspawn\s*\(", re.IGNORECASE),
    re.compile(r"\bspawnSync\s*\(", re.IGNORECASE),
    re.compile(r"\bexecSync\s*\(", re.IGNORECASE),
    re.compile(r"\bexec\s*\(", re.IGNORECASE),
    re.compile(r"\bsubprocess\.(run|Popen|call|check_call|check_output)\s*\(", re.IGNORECASE),
    re.compile(r"\bos\.system\s*\(", re.IGNORECASE),
]

HOOK_TARGET_WRITE_PATTERNS = [
    re.compile(r"\bwriteFileSync\s*\(", re.IGNORECASE),
    re.compile(r"\bcopyFileSync\s*\(", re.IGNORECASE),
    re.compile(r"\bchmodSync\s*\(", re.IGNORECASE),
    re.compile(r"\bsymlinkSync\s*\(", re.IGNORECASE),
    re.compile(r"\bwrite_text\s*\(", re.IGNORECASE),
    re.compile(r"\bchmod\s+\d{3,4}\b", re.IGNORECASE),
]

PY_SETUP_INSTALL_HOOK_PATTERNS = [
    re.compile(r"\bsetuptools\.command\.install\s+import\s+install\b", re.IGNORECASE),
    re.compile(r"class\s+\w+\s*\(\s*install\s*\)", re.IGNORECASE),
    re.compile(r"cmdclass\s*=\s*\{[^}]*['\"]install['\"]", re.IGNORECASE | re.DOTALL),
]

PY_SUBPROCESS_EXEC_PATTERN = re.compile(r"\bsubprocess\.(run|Popen|call|check_call|check_output)\s*\(", re.IGNORECASE)
PY_OS_SYSTEM_PATTERN = re.compile(r"\bos\.system\s*\(", re.IGNORECASE)

TRUSTED_BOOTSTRAP_DOMAINS = {
    "astral.sh",
    "bun.sh",
    "deno.land",
    "get.docker.com",
}

DOCS_COMMAND_RISK_PATTERNS = [
    re.compile(r"\b(curl|wget)\b[^\n]*\|\s*(bash|sh|zsh|pwsh|powershell)\b", re.IGNORECASE),
    re.compile(r"\bbash\s+<\(\s*(curl|wget)\b", re.IGNORECASE),
    re.compile(r"\b(iwr|invoke-webrequest)\b[^\n]*\|\s*iex\b", re.IGNORECASE),
]

PROMPT_EXFIL_RULES: Sequence[Tuple[re.Pattern[str], str, str, str, str, str]] = [
    (
        re.compile(r"\b(cat|type)\s+\.env\b.{0,160}\b(curl|wget|invoke-webrequest|iwr)\b", re.IGNORECASE),
        "B_PROMPT_ENV_EXFIL_DIRECTIVE",
        "critical",
        "high",
        "Prompt directive instructs reading .env and transmitting it over the network.",
        "Remove data-exfiltration directives and prohibit secret-bearing outbound commands.",
    ),
    (
        re.compile(r"\b(curl|wget|invoke-webrequest|iwr)\b[^\n]*\$\(\s*(cat|type)\s+\.env\b", re.IGNORECASE),
        "B_PROMPT_ENV_EXFIL_DIRECTIVE",
        "critical",
        "high",
        "Prompt directive instructs reading .env and transmitting it over the network.",
        "Remove data-exfiltration directives and prohibit secret-bearing outbound commands.",
    ),
    (
        re.compile(r"\b(cat|type)\s+.*\.aws[/\\]credentials\b.{0,200}\b(curl|wget|invoke-webrequest|iwr)\b", re.IGNORECASE),
        "B_PROMPT_CREDENTIAL_EXFIL_DIRECTIVE",
        "critical",
        "high",
        "Prompt directive instructs credential file exfiltration.",
        "Remove credential-exfiltration instructions and block credential file access in prompts.",
    ),
    (
        re.compile(
            r"\b(curl|wget|invoke-webrequest|iwr)\b[^\n]*(/exfil|/steal|webhook|requestbin|ngrok|localhost:8888)",
            re.IGNORECASE,
        ),
        "B_PROMPT_NETWORK_EXFIL_ENDPOINT",
        "high",
        "medium",
        "Prompt content references a known exfiltration-style endpoint pattern.",
        "Use vetted non-sensitive test payloads and avoid hidden endpoint instructions.",
    ),
]

ATTACK_CONTENT_DECLARATION_RULES: Sequence[Tuple[re.Pattern[str], str, str, str, str, str]] = [
    (
        re.compile(
            r"\b(prompt\s+injection)\b.{0,80}\b(demo|attack|exploit|payload|poc)\b|\b(demo|attack|exploit|payload|poc)\b.{0,80}\b(prompt\s+injection)\b",
            re.IGNORECASE,
        ),
        "A_PROMPT_INJECTION_ATTACK_CONTENT",
        "high",
        "medium",
        "Repository content declares prompt-injection attack/demo payload behavior.",
        "Treat repository as hostile training/demo content and do not execute embedded instructions.",
    ),
    (
        re.compile(
            r"\b(supply\s+chain\s+attack|malicious\s+package)\b.{0,80}\b(demo|lab|proof[- ]?of[- ]?concept|poc)\b",
            re.IGNORECASE,
        ),
        "E_SUPPLY_CHAIN_ATTACK_DEMO_CONTENT",
        "high",
        "medium",
        "Repository content declares supply-chain attack demo behavior.",
        "Treat package/install scripts as hostile and avoid execution in trusted environments.",
    ),
]

PRIVILEGED_OPERATION_RULES: Sequence[Tuple[re.Pattern[str], str, str]] = [
    (
        re.compile(
            r"\bsudo\s+(?:-[a-zA-Z-]+\s+)*(mount|umount|losetup|debugfs|fsck(\.[a-z0-9_]+)?)\b\s+",
            re.IGNORECASE,
        ),
        "C_PRIVILEGED_FILESYSTEM_OPERATION",
        "Privileged filesystem administration command detected.",
    ),
    (
        re.compile(r"(^|\s)(mount|umount|losetup|debugfs|fsck(\.[a-z0-9_]+)?)\b\s+", re.IGNORECASE),
        "C_PRIVILEGED_FILESYSTEM_OPERATION",
        "Filesystem administration command detected and may require elevated privilege.",
    ),
    (
        re.compile(r"\bsudo\s+(?:-[a-zA-Z-]+\s+)*(chroot|modprobe|insmod)\b\s+", re.IGNORECASE),
        "C_PRIVILEGED_SYSTEM_OPERATION",
        "Privileged host/system command detected.",
    ),
]

NODE_LITERAL_SAFE_COMMAND_PATTERNS = [
    re.compile(r"^git\s+rev-parse\s+head$", re.IGNORECASE),
    re.compile(r"^git\s+describe(\s+--[a-z-]+)*$", re.IGNORECASE),
    re.compile(r"^git\s+log\s+--oneline(\s+-n\s*\d+)?$", re.IGNORECASE),
    re.compile(r"^node\s+--version$", re.IGNORECASE),
    re.compile(r"^python\d*\s+--version$", re.IGNORECASE),
]

HYGIENE_RULE_IDS = {
    "E_WORKFLOW_ACTION_MUTABLE_REF",
    "E_WORKFLOW_ACTION_UNPINNED",
    "E_PY_REQUIREMENT_UNPINNED",
    "E_NODE_LOCKFILE_MISSING",
    "E_INSTALL_HOOK_SCRIPT_EXECUTION",
    "C_NODE_EXEC_LITERAL_SAFE",
    "C_NODE_EXEC_ALIAS_LITERAL_SAFE",
}

ATTACK_SURFACE_RULE_IDS = {
    "A_IGNORE_PREVIOUS_INSTRUCTIONS",
    "A_OVERRIDE_SYSTEM_INSTRUCTIONS",
    "A_BYPASS_SAFETY",
    "A_PROMPT_EXTRACTION",
    "A_HIERARCHY_INVERSION",
    "A_TYPOGLYCEMIA_OVERRIDE",
    "A_FORCED_TOOL_EXECUTION_ZH",
    "A_FORCED_TOOL_EXECUTION_EN",
    "E_DOCS_DOWNLOAD_EXEC_COMMAND",
    "B_PROMPT_ENV_EXFIL_DIRECTIVE",
    "B_PROMPT_CREDENTIAL_EXFIL_DIRECTIVE",
    "B_PROMPT_NETWORK_EXFIL_ENDPOINT",
    "A_PROMPT_INJECTION_ATTACK_CONTENT",
    "E_SUPPLY_CHAIN_ATTACK_DEMO_CONTENT",
    "E_GITHUB_OSINT_HIGH_RISK_SIGNAL",
    "D_PROMPT_STEGANOGRAPHY_CONTENT",
}

WORKFLOW_USES_PATTERN = re.compile(r"^\s*uses:\s*([^\s#]+)")
