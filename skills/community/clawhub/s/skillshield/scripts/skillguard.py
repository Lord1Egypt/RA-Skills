#!/usr/bin/env python3
"""SkillShield v4.0.0 — Ultimate Edition 🛡️
Advanced security scanner for OpenClaw skills.
Python 3 stdlib only. Single file. Zero dependencies.
65+ security checks. SARIF v2.1.0 output. CI/CD ready."""

import base64
import difflib
import hashlib
import json
import os
import re
import shutil
import sys
import time
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
import platform

# ── Version ──────────────────────────────────────────────────────────────────

VERSION = "4.0.0"
BANNER = f"SkillShield v{VERSION} — Ultimate Edition 🛡️"

# ── Colours ──────────────────────────────────────────────────────────────────

NO_COLOR = os.environ.get("NO_COLOR") is not None
def _c(code, text):
    return text if NO_COLOR else f"\033[{code}m{text}\033[0m"
RED    = lambda t: _c("91", t)
YELLOW = lambda t: _c("93", t)
GREEN  = lambda t: _c("92", t)
CYAN   = lambda t: _c("96", t)
BLUE   = lambda t: _c("94", t)
MAGENTA= lambda t: _c("95", t)
BOLD   = lambda t: _c("1", t)
DIM    = lambda t: _c("2", t)
WHITE  = lambda t: _c("97", t)

# ── Constants ────────────────────────────────────────────────────────────────

SKILLS_DIR = Path.home() / "clawd" / "skills"
BASELINES_PATH = Path.home() / "clawd" / "skills" / "skill-guard" / "baselines.json"
GUARD_DIR = Path.home() / "clawd" / "skills" / "skill-guard"
QUARANTINE_DIR = SKILLS_DIR / ".quarantine"
QUARANTINE_LOG = GUARD_DIR / "quarantine.log"
SCANNABLE_EXTS = {
    ".py", ".js", ".ts", ".tsx", ".jsx", ".sh", ".bash",
    ".md", ".json", ".svg", ".yml", ".yaml", ".toml", ".txt",
    ".cfg", ".ini", ".html", ".css",
    ".rs", ".go", ".rb", ".c", ".cpp", ".h", ".hpp",
    ".env", ".gradle",
}
# Also match by filename pattern
SCANNABLE_NAMES = {"Dockerfile", "Makefile", "pom.xml", ".env"}
DEFAULT_MAX_FILE_SIZE = 2 * 1024 * 1024
LARGE_FILE_THRESHOLD = 500 * 1024
MAX_FILE_COUNT = 50

CRITICAL = "CRITICAL"
WARNING = "WARNING"
INFO = "INFO"

# ── Check Registry (SS-001 through SS-065+) ─────────────────────────────────

CHECK_REGISTRY = {
    "SS-001": ("Outbound HTTP request", WARNING, 3),
    "SS-002": ("eval/exec call", WARNING, 5),
    "SS-003": ("Dynamic import", WARNING, 5),
    "SS-004": ("Base64 decode operation", WARNING, 4),
    "SS-005": ("Base64 decodes to suspicious content", CRITICAL, 9),
    "SS-006": ("Hex string decodes to suspicious content", CRITICAL, 9),
    "SS-007": ("URL shortener detected", WARNING, 5),
    "SS-008": ("Executable data URI", WARNING, 5),
    "SS-009": ("Hardcoded secret", CRITICAL, 10),
    "SS-010": ("SSL verification disabled", WARNING, 5),
    "SS-011": ("PATH modification", CRITICAL, 8),
    "SS-012": ("Library path modification", CRITICAL, 8),
    "SS-013": ("Shell execution (os.system)", WARNING, 4),
    "SS-014": ("subprocess with shell=True", CRITICAL, 7),
    "SS-015": ("Sensitive file access", CRITICAL, 8),
    "SS-016": ("Reverse shell pattern", CRITICAL, 10),
    "SS-017": ("DNS exfiltration", CRITICAL, 9),
    "SS-018": ("Crontab modification", CRITICAL, 8),
    "SS-019": ("System service creation", CRITICAL, 8),
    "SS-020": ("Shell RC file modification", CRITICAL, 8),
    "SS-021": ("Time bomb pattern", WARNING, 6),
    "SS-022": ("Pickle deserialization", CRITICAL, 9),
    "SS-023": ("Prompt injection override", CRITICAL, 9),
    "SS-024": ("Prompt injection exfiltration", CRITICAL, 9),
    "SS-025": ("Social engineering phrase", WARNING, 5),
    "SS-026": ("SVG JavaScript", CRITICAL, 8),
    "SS-027": ("SVG event handler", WARNING, 5),
    "SS-028": ("npm lifecycle hook", CRITICAL, 8),
    "SS-029": ("Typosquat package", WARNING, 6),
    "SS-030": ("Binary executable", CRITICAL, 9),
    "SS-031": ("Symlink to sensitive path", CRITICAL, 8),
    "SS-032": ("Archive file", WARNING, 4),
    "SS-033": ("Unicode homoglyph", CRITICAL, 7),
    "SS-034": ("ANSI escape injection", WARNING, 5),
    "SS-035": ("Writes outside skill dir", WARNING, 5),
    "SS-036": ("COMBO sensitive+outbound", CRITICAL, 10),
    "SS-037": ("COMBO subprocess+sensitive", CRITICAL, 8),
    "SS-038": ("Campaign match", CRITICAL, 10),
    "SS-039": ("BEHAVIORAL staged exfil", CRITICAL, 9),
    "SS-040": ("BEHAVIORAL download+exec", CRITICAL, 9),
    "SS-041": ("BEHAVIORAL env harvest+net", CRITICAL, 9),
    "SS-042": ("Clipboard access", WARNING, 4),
    "SS-043": ("Bulk env capture", CRITICAL, 9),
    "SS-044": ("Permission mismatch", CRITICAL, 8),
    # NEW v4 checks
    "SS-045": ("Known C2/IOC IP", CRITICAL, 10),
    "SS-046": ("Known exfiltration endpoint", CRITICAL, 10),
    "SS-047": ("Paste service reference", CRITICAL, 7),
    "SS-048": ("GitHub raw content execution", CRITICAL, 9),
    "SS-049": ("macOS Gatekeeper bypass (xattr)", CRITICAL, 9),
    "SS-050": ("macOS osascript social engineering", CRITICAL, 8),
    "SS-051": ("TMPDIR payload staging", CRITICAL, 9),
    "SS-052": ("Keychain theft", CRITICAL, 10),
    "SS-053": ("Password-protected archive", CRITICAL, 7),
    "SS-054": ("Double-encoded path", CRITICAL, 7),
    "SS-055": ("Punycode domain", CRITICAL, 7),
    "SS-056": ("String construction evasion", CRITICAL, 7),
    "SS-057": ("Process persistence + network", CRITICAL, 9),
    "SS-058": ("Agent config tampering", CRITICAL, 9),
    "SS-059": ("LLM tool exploitation", CRITICAL, 9),
    "SS-060": ("Fake prerequisite pattern", CRITICAL, 7),
    "SS-061": ("Network fingerprinting", WARNING, 6),
    "SS-062": ("Known malicious actor", CRITICAL, 10),
    "SS-063": ("Nohup/disown + network", CRITICAL, 9),
    "SS-064": ("chmod +x on download", CRITICAL, 8),
    "SS-065": ("open -a with download", CRITICAL, 8),
}

TOTAL_CHECKS = len(CHECK_REGISTRY)

# ── Known C2/IOC IPs ────────────────────────────────────────────────────────

KNOWN_C2_IPS = {
    "91.92.242.30": "AMOS C2 server (ClawHavoc campaign)",
    "54.91.154.110": "AMOS C2 server (ClawHavoc campaign)",
    "185.215.113.16": "ClawHavoc dropper relay",
    "45.61.136.47": "AMOS stage-2 payload server",
    "194.169.175.232": "Atomic Stealer C2",
    "91.92.248.52": "ClawHavoc wallet exfil endpoint",
    "79.137.207.210": "Bandit Stealer C2 (Koi Security)",
    "45.155.205.172": "Generic macOS stealer C2",
}

# ── Known Malicious Actors ──────────────────────────────────────────────────

KNOWN_MALICIOUS_ACTORS = {
    "zaycv": "ClawHavoc campaign operator",
    "ddoy233": "ClawHavoc campaign operator",
    "sakaen736jih": "ClawHavoc campaign operator",
    "hightower6eu": "ClawHavoc campaign operator",
    "aslaep123": "ClawHavoc campaign associate",
    "davidsmorais": "ClawHavoc campaign associate",
    "clawdhub1": "ClawHavoc impersonation account",
}

# ── Known Exfiltration Endpoints ─────────────────────────────────────────────

EXFIL_ENDPOINTS = {
    "webhook.site", "ngrok.io", "requestbin.com", "hookbin.com",
    "pipedream.com", "burpcollaborator.net", "requestcatcher.com",
    "smee.io", "interactsh.com", "oastify.com", "postb.in",
    "webhook.online", "socifiapp.com",
}

# ── Paste Services ───────────────────────────────────────────────────────────

PASTE_SERVICES = {
    "glot.io", "pastebin.com", "hastebin.com", "dpaste.com", "ghostbin.com",
    "rentry.co", "rentry.org", "paste.ee", "privatebin.net", "controlc.com",
    "paste.mozilla.org", "ix.io", "sprunge.us", "cl1p.net",
}

# ── Campaign Signatures ─────────────────────────────────────────────────────

CAMPAIGNS = {
    "ClawHavoc": {
        "description": "386-skill wallet theft campaign with C2 beacons",
        "crypto_brands": ["bybit", "axiom", "polymarket", "binance wallet", "coinbase wallet",
                          "ledger", "trezor", "metamask", "phantom", "keplr", "trust wallet"],
        "wallet_patterns": [r"\.ethereum", r"\.solana", r"keystore", r"wallet.*\.dat",
                            r"\.config/solana", r"MetaMask", r"Phantom", r"Rabby"],
        "c2_patterns": [r"\.ru[/\s\"']", r"\.cn[/\s\"']", r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b",
                        r"[a-z0-9]{8,12}\.(com|net|org|io)", r"\.xyz[/\s\"']"],
        "condition": "crypto_brand + wallet_access + c2_domain",
    },
    "twitter-enhanced": {
        "description": "Typosquatting popular skills with hidden eval/exec",
        "typosquat_names": ["twitter-enhanced", "tweeter", "twtter", "twiter", "discord-enhanced",
                            "slack-enhanced", "github-enhanced"],
        "payload_patterns": [r"\beval\s*\(", r"\bexec\s*\(", r"__import__", r"importlib\.import_module"],
        "condition": "typosquat_name + hidden_eval",
    },
    "ClickFix": {
        "description": "Social engineering - instructs user to run commands from clipboard",
        "instruction_patterns": [
            r"(?:copy|paste).*(?:powershell|terminal|cmd|command prompt)",
            r"(?:run|execute).*(?:clipboard|copied|paste)",
            r"(?:press|hit).*(?:Win\+R|Ctrl\+V).*(?:enter|return)",
            r"powershell\s+-(?:enc|e)\s",
            r"irm\s+.*\|\s*iex",
        ],
        "condition": "instruction_pattern_match",
    },
}

# ── Known-good domains ──────────────────────────────────────────────────────

KNOWN_DOMAINS = {
    "api.coingecko.com", "feeds.bbci.co.uk", "api.github.com",
    "query1.finance.yahoo.com", "query2.finance.yahoo.com",
    "api.openai.com", "discord.com", "api.telegram.org",
    "api.x.ai", "api.anthropic.com", "feeds.npr.org",
    "www.aljazeera.com", "www.reutersagency.com", "img402.dev",
    "snap.llm.kaveenk.com", "astral.sh", "pypi.org",
    "raw.githubusercontent.com", "github.com", "api.weatherapi.com",
    "api.openweathermap.org", "newsapi.org", "api.newsapi.org",
    "rss.nytimes.com", "www.reddit.com", "oauth.reddit.com",
    "api.spotify.com", "api.twitch.tv", "api.twitter.com",
    "graph.facebook.com", "www.googleapis.com", "maps.googleapis.com",
    "api.stripe.com", "api.slack.com", "hooks.slack.com",
    "api.notion.com", "api.pushover.net", "ntfy.sh",
    "api.elevenlabs.io", "api.deepl.com", "translate.googleapis.com",
    "api.wolframalpha.com", "en.wikipedia.org", "www.wikipedia.org",
    "api.dictionaryapi.dev", "api.urbandictionary.com",
    "itunes.apple.com", "api.exchangerate-api.com",
    "cdn.jsdelivr.net", "unpkg.com", "registry.npmjs.org",
    "crates.io", "rubygems.org", "hub.docker.com",
    "youtube.com", "www.youtube.com", "youtubetranscript.com",
    "i.ytimg.com", "yt3.ggpht.com",
    "stockanalysis.com", "www.stockanalysis.com",
    "finance.yahoo.com", "www.google.com",
    "api.binance.com", "pro-api.coinmarketcap.com",
    "invidious.io", "inv.tux.pizza", "vid.puffyan.us",
    "nitter.net", "bsky.social", "bsky.app",
    "localhost", "127.0.0.1", "0.0.0.0",
}

DOMAIN_CONTEXT = {
    "coingecko": ["crypto", "coin", "price", "bitcoin", "ethereum", "defi", "token"],
    "yahoo": ["stock", "finance", "market", "ticker", "portfolio", "trading"],
    "weather": ["weather", "forecast", "temperature", "climate"],
    "news": ["news", "headline", "article", "feed", "rss", "bbc", "npr", "reuters"],
    "youtube": ["youtube", "video", "transcript", "subtitle"],
    "telegram": ["telegram", "bot", "chat", "message", "notification"],
    "discord": ["discord", "bot", "webhook"],
    "openai": ["ai", "gpt", "chat", "llm", "completion"],
    "anthropic": ["ai", "claude", "llm", "completion"],
    "github": ["git", "repo", "code", "commit", "pr", "issue"],
    "reddit": ["reddit", "subreddit", "post"],
    "spotify": ["music", "playlist", "song", "spotify"],
    "elevenlabs": ["voice", "tts", "speech", "audio"],
    "stockanalysis": ["stock", "finance", "market", "analysis"],
}

URL_SHORTENERS = {"bit.ly", "tinyurl.com", "t.co", "goo.gl", "ow.ly", "is.gd",
                  "buff.ly", "adf.ly", "tiny.cc", "lnkd.in", "rb.gy", "cutt.ly",
                  "shorturl.at", "v.gd", "qr.ae"}

KNOWN_PACKAGES_PY = [
    "requests", "numpy", "pandas", "flask", "django", "scipy", "matplotlib",
    "urllib3", "certifi", "idna", "charset-normalizer", "setuptools", "pip",
    "cryptography", "pyyaml", "pillow", "boto3", "botocore", "jinja2",
    "click", "aiohttp", "sqlalchemy", "pytest", "beautifulsoup4", "lxml",
    "paramiko", "pycryptodome", "pyopenssl", "colorama", "tqdm",
]
KNOWN_PACKAGES_JS = [
    "express", "react", "lodash", "axios", "moment", "chalk", "commander",
    "webpack", "babel", "typescript", "eslint", "prettier", "jest", "mocha",
    "mongoose", "sequelize", "socket.io", "cors", "dotenv", "uuid",
    "jsonwebtoken", "bcrypt", "nodemon", "pm2", "puppeteer",
]
SUSPICIOUS_PACKAGES = {
    "event-stream", "flatmap-stream", "ua-parser-js", "coa", "rc",
    "colors", "faker",
}

SECRET_PATTERNS = [
    (r'AKIA[0-9A-Z]{16}', "AWS Access Key"),
    (r'ghp_[A-Za-z0-9]{36}', "GitHub Personal Access Token"),
    (r'gho_[A-Za-z0-9]{36}', "GitHub OAuth Token"),
    (r'github_pat_[A-Za-z0-9_]{82}', "GitHub Fine-grained PAT"),
    (r'sk-[A-Za-z0-9]{20,}T3BlbkFJ[A-Za-z0-9]{20,}', "OpenAI API Key"),
    (r'sk-(?:proj|org)-[A-Za-z0-9\-_]{40,}', "OpenAI Project/Org Key"),
    (r'xox[boaprs]-[A-Za-z0-9\-]{10,}', "Slack Token"),
    (r'sk_live_[A-Za-z0-9]{24,}', "Stripe Secret Key"),
    (r'rk_live_[A-Za-z0-9]{24,}', "Stripe Restricted Key"),
    (r'-----BEGIN (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----', "Private Key"),
    (r'AIza[0-9A-Za-z\-_]{35}', "Google API Key"),
]

HOMOGLYPHS = {
    '\u0430': 'a', '\u0435': 'e', '\u043e': 'o', '\u0440': 'p',
    '\u0441': 'c', '\u0443': 'y', '\u0445': 'x', '\u0456': 'i',
    '\u0458': 'j', '\u04bb': 'h', '\u0455': 's', '\u0432': 'b',
    '\u043d': 'h', '\u0442': 't', '\u043c': 'm', '\u043a': 'k',
    '\u0433': 'r',
    '\u0251': 'a', '\u0261': 'g', '\u026f': 'm',
    '\u01c3': '!', '\u037e': ';',
    '\uff41': 'a', '\uff42': 'b', '\uff43': 'c', '\uff44': 'd',
    '\uff45': 'e', '\uff46': 'f',
}

BINARY_MAGICS = [
    (b'\x7fELF', "ELF binary"),
    (b'\xfe\xed\xfa\xce', "Mach-O binary (32-bit)"),
    (b'\xfe\xed\xfa\xcf', "Mach-O binary (64-bit)"),
    (b'\xce\xfa\xed\xfe', "Mach-O binary (32-bit, reversed)"),
    (b'\xcf\xfa\xed\xfe', "Mach-O binary (64-bit, reversed)"),
    (b'MZ', "PE/Windows executable"),
    (b'\xca\xfe\xba\xbe', "Mach-O universal binary / Java class"),
]

ARCHIVE_EXTS = {".zip", ".tar", ".tar.gz", ".tgz", ".tar.bz2", ".tar.xz", ".rar", ".7z", ".gz", ".bz2", ".xz"}

# Agent config files that should never be written to by skills
AGENT_CONFIG_FILES = {
    "AGENTS.md", "SOUL.md", "USER.md", "MEMORY.md", "HEARTBEAT.md",
    "BOOTSTRAP.md", "openclaw.json", ".openclaw",
}

# ── Helpers ───────────────────────────────────────────────────────────────────

def levenshtein(a, b):
    if len(a) < len(b): return levenshtein(b, a)
    if len(b) == 0: return len(a)
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a):
        curr = [i + 1]
        for j, cb in enumerate(b):
            curr.append(min(prev[j + 1] + 1, curr[j] + 1, prev[j] + (ca != cb)))
        prev = curr
    return prev[-1]

def safe_read(path, max_size=DEFAULT_MAX_FILE_SIZE):
    try:
        if path.stat().st_size > max_size:
            return None
        return path.read_text(errors="replace")
    except Exception:
        return None

def is_scannable(path):
    name = path.name
    if name in SCANNABLE_NAMES:
        return True
    if any(name.startswith(n) for n in ("Dockerfile", ".env")):
        return True
    return path.suffix.lower() in SCANNABLE_EXTS

def sha256_file(path):
    h = hashlib.sha256()
    try:
        with open(path, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                h.update(chunk)
        return h.hexdigest()
    except Exception:
        return None

def extract_domains(text):
    domains = set()
    for m in re.finditer(r'https?://([a-zA-Z0-9._-]+(?:\.[a-zA-Z]{2,}))', text):
        domains.add(m.group(1).lower())
    return domains

def is_known_domain(domain):
    domain = domain.lower().strip('.')
    if domain in KNOWN_DOMAINS:
        return True
    for known in KNOWN_DOMAINS:
        if domain.endswith('.' + known):
            return True
    return False

def domain_matches_context(domain, skill_name, skill_desc):
    context = (skill_name + " " + skill_desc).lower()
    for keyword, context_words in DOMAIN_CONTEXT.items():
        if keyword in domain.lower():
            if any(w in context for w in context_words):
                return True
    return False

def has_homoglyphs(text):
    found = []
    for ch in text:
        if ch in HOMOGLYPHS:
            found.append((ch, HOMOGLYPHS[ch]))
    return found

def check_binary_magic(path):
    try:
        with open(path, 'rb') as f:
            header = f.read(8)
        for magic, desc in BINARY_MAGICS:
            if header.startswith(magic):
                return desc
    except Exception:
        pass
    return None

def get_skill_name(skill_dir):
    return skill_dir.name

def get_skill_description(skill_dir):
    sm = skill_dir / "SKILL.md"
    text = safe_read(sm) if sm.exists() else None
    if not text: return ""
    m = re.search(r'description:\s*(.+)', text[:2000], re.I)
    if m: return m.group(1).strip()
    lines = text.split('\n')
    for i, l in enumerate(lines):
        if l.startswith('#') and i + 1 < len(lines):
            for nl in lines[i+1:]:
                nl = nl.strip()
                if nl and not nl.startswith('#') and not nl.startswith('---'):
                    return nl[:200]
    return ""

def progress_bar(current, total, skill_name, width=30):
    if NO_COLOR:
        return
    pct = current / total if total else 1
    filled = int(width * pct)
    bar = '█' * filled + '░' * (width - filled)
    name = skill_name[:25].ljust(25)
    sys.stderr.write(f"\r  [{bar}] {current}/{total} {name}")
    sys.stderr.flush()

def clear_progress():
    if not NO_COLOR:
        sys.stderr.write("\r" + " " * 80 + "\r")
        sys.stderr.flush()

# ── Verbose logging ──────────────────────────────────────────────────────────

VERBOSE_MODE = False

def verbose(msg):
    if VERBOSE_MODE:
        sys.stderr.write(f"  {_c('96', '[verbose]')} {msg}\n")
        sys.stderr.flush()

# ── Baselines ────────────────────────────────────────────────────────────────

def load_baselines():
    if BASELINES_PATH.exists():
        try:
            return json.loads(BASELINES_PATH.read_text())
        except Exception:
            return {}
    return {}

def save_baselines(baselines):
    BASELINES_PATH.parent.mkdir(parents=True, exist_ok=True)
    BASELINES_PATH.write_text(json.dumps(baselines, indent=2))

def compute_skill_hashes(skill_dir):
    hashes = {}
    try:
        for p in sorted(skill_dir.rglob("*")):
            if p.is_file() and not any(part.startswith('.git') and part != '.clawhub' for part in p.parts):
                rel = str(p.relative_to(skill_dir))
                h = sha256_file(p)
                if h:
                    hashes[rel] = h
    except Exception:
        pass
    return hashes

# ── Custom Rules Engine ──────────────────────────────────────────────────────

def load_custom_rules():
    rules_path = GUARD_DIR / "rules.json"
    if not rules_path.exists():
        return []
    try:
        data = json.loads(rules_path.read_text())
        if isinstance(data, list):
            return data
        return []
    except Exception:
        return []

# ── Ignore File ──────────────────────────────────────────────────────────────

def load_ignore_file(skill_dir):
    ignore_path = skill_dir / ".skillshield-ignore"
    if not ignore_path.exists():
        return set()
    try:
        lines = ignore_path.read_text().strip().split('\n')
        return {l.strip() for l in lines if l.strip() and not l.strip().startswith('#')}
    except Exception:
        return set()

def add_to_ignore(skill_dir, finding_desc):
    ignore_path = skill_dir / ".skillshield-ignore"
    existing = ""
    if ignore_path.exists():
        existing = ignore_path.read_text()
    with open(ignore_path, 'a') as f:
        if existing and not existing.endswith('\n'):
            f.write('\n')
        f.write(finding_desc + '\n')

# ── Finding ──────────────────────────────────────────────────────────────────

class Finding:
    __slots__ = ('level', 'desc', 'file', 'line', 'recommendation', 'score_override', 'campaign', 'check_id')
    def __init__(self, level, desc, file="", line=0, recommendation="", score_override=None, campaign=None, check_id=""):
        self.level = level
        self.desc = desc
        self.file = file
        self.line = line
        self.recommendation = recommendation
        self.score_override = score_override
        self.campaign = campaign
        self.check_id = check_id

    def __repr__(self):
        loc = f" — {self.file}:{self.line}" if self.file else ""
        cid = f" [{self.check_id}]" if self.check_id else ""
        return f"[{self.level:8s}]{cid} {self.desc}{loc}"

    def to_dict(self):
        d = {"level": self.level, "description": self.desc}
        if self.check_id: d["check_id"] = self.check_id
        if self.file: d["file"] = self.file
        if self.line: d["line"] = self.line
        if self.recommendation: d["recommendation"] = self.recommendation
        if self.campaign: d["campaign"] = self.campaign
        weight = 0
        if self.check_id and self.check_id in CHECK_REGISTRY:
            weight = CHECK_REGISTRY[self.check_id][2]
        d["weight"] = weight
        return d

    def fingerprint(self):
        return f"{self.level}|{self.desc}|{self.file}|{self.line}"


# ── Scanner ──────────────────────────────────────────────────────────────────

class SkillScanner:
    def __init__(self, skill_dir, check_baseline=True, max_file_size=None, max_depth=None):
        self.skill_dir = Path(skill_dir)
        self.name = get_skill_name(self.skill_dir)
        self.desc = get_skill_description(self.skill_dir)
        self.findings = []
        self.files = []
        self.tamper_detected = False
        self.check_baseline = check_baseline
        self.reputation_grade = "B"
        self.campaign_matches = []
        self.ignore_patterns = load_ignore_file(self.skill_dir)
        self.max_file_size = max_file_size or DEFAULT_MAX_FILE_SIZE
        self.max_depth = max_depth
        self._has_sensitive_access = False
        self._has_outbound = False
        self._has_subprocess = False
        self._has_download_exec = False
        self._has_tmp_write = False
        self._has_tmp_read = False
        self._has_env_harvest = False
        self._has_clipboard = False
        self._unknown_domains = set()
        self._known_domains_used = set()
        self._all_domains = set()
        self._all_file_paths = set()
        self._all_commands = set()
        self._all_env_vars = set()
        self._all_deps = []
        self._code_lines = 0
        self._doc_lines = 0
        self._checks_run = 0
        self._checks_applicable = 0
        self._collect_files()

    def _collect_files(self):
        try:
            for p in self.skill_dir.rglob("*"):
                if p.is_file() and not any(part.startswith('.git') and part != '.clawhub' for part in p.parts):
                    # Max depth check
                    if self.max_depth is not None:
                        rel = p.relative_to(self.skill_dir)
                        if len(rel.parts) > self.max_depth:
                            continue
                    # Max file size check
                    try:
                        if p.stat().st_size > self.max_file_size:
                            continue
                    except Exception:
                        pass
                    self.files.append(p)
        except Exception:
            pass

    def add(self, level, desc, file="", line=0, recommendation="", score_override=None, campaign=None, check_id=""):
        rel = str(file).replace(str(self.skill_dir) + "/", "") if file else ""
        # Check ignore patterns (file-based)
        if self.ignore_patterns:
            for pat in self.ignore_patterns:
                if pat in desc:
                    return
        f = Finding(level, desc, rel, line, recommendation, score_override, campaign, check_id)
        self.findings.append(f)

    def _line_has_inline_ignore(self, line_text):
        """Check for # skillshield-ignore inline comment."""
        return '# skillshield-ignore' in line_text or '// skillshield-ignore' in line_text

    def scan(self):
        self._reputation_heuristics()
        self._check_file_permissions()
        self._check_binary_files()
        self._check_large_files()
        self._check_homoglyphs()
        self._check_symlinks()
        self._check_archives()

        for f in self.files:
            if is_scannable(f):
                text = safe_read(f, self.max_file_size)
                if text is None: continue
                lines = text.split('\n')
                ext = f.suffix.lower()
                if ext == ".md":
                    self._scan_prompt_injection(f, lines)
                    self._doc_lines += len(lines)
                if ext == ".json":
                    self._scan_json(f, text)
                if ext == ".svg":
                    self._scan_svg(f, text, lines)
                if ext in ('.py', '.js', '.ts', '.tsx', '.jsx', '.sh', '.bash', '.rs', '.go', '.rb', '.c', '.cpp'):
                    self._code_lines += len(lines)
                self._scan_code(f, lines, ext)
                self._scan_secrets(f, lines, ext)
                self._scan_write_outside(f, lines, ext)
                self._deep_string_analysis(f, lines, ext)
                # v4 new checks
                self._scan_c2_ips(f, lines, ext)
                self._scan_exfil_endpoints(f, lines, ext)
                self._scan_paste_services(f, lines, ext)
                self._scan_github_raw_exec(f, lines, ext)
                self._scan_macos_attacks(f, lines, ext)
                self._scan_password_archives(f, lines, ext)
                self._scan_double_encoded(f, lines, ext)
                self._scan_punycode(f, lines, ext)
                self._scan_string_evasion(f, lines, ext)
                self._scan_persistence_network(f, lines, ext)
                self._scan_agent_tampering(f, lines, ext)
                self._scan_llm_exploitation(f, lines, ext)
                self._scan_fake_prerequisites(f, lines, ext)
                self._scan_network_fingerprint(f, lines, ext)
            else:
                self._scan_non_text(f)

        self._scan_requirements()
        self._scan_malicious_actors()
        self._campaign_detection()
        self._behavioral_analysis()
        self._check_combos()
        self._permission_mismatch()
        self._apply_custom_rules()

        if self.check_baseline:
            self._check_tamper()

        self._deduplicate()
        return self

    # ── Known C2/IOC IPs ──

    def _scan_c2_ips(self, f, lines, ext):
        self._checks_run += 1
        verbose(f"  Check SS-045: C2 IPs on {f.name}")
        for i, line in enumerate(lines, 1):
            if self._line_has_inline_ignore(line):
                continue
            for ip, campaign in KNOWN_C2_IPS.items():
                if ip in line:
                    self.add(CRITICAL, f"Known C2/IOC IP: {ip} ({campaign})", f, i,
                             recommendation=f"IP {ip} is a known malicious C2 server. Remove immediately.",
                             score_override=50, check_id="SS-045")

    # ── Exfiltration Endpoints ──

    def _scan_exfil_endpoints(self, f, lines, ext):
        self._checks_run += 1
        verbose(f"  Check SS-046: Exfil endpoints on {f.name}")
        for i, line in enumerate(lines, 1):
            if self._line_has_inline_ignore(line):
                continue
            ln = line.lower()
            for ep in EXFIL_ENDPOINTS:
                if ep in ln:
                    self.add(CRITICAL, f"Known exfiltration endpoint: {ep}", f, i,
                             recommendation=f"{ep} is a known data exfiltration service. Remove immediately.",
                             score_override=50, check_id="SS-046")

    # ── Paste Services ──

    def _scan_paste_services(self, f, lines, ext):
        self._checks_run += 1
        verbose(f"  Check SS-047: Paste services on {f.name}")
        for i, line in enumerate(lines, 1):
            if self._line_has_inline_ignore(line):
                continue
            ln = line.lower()
            for ps in PASTE_SERVICES:
                if ps in ln:
                    self.add(CRITICAL, f"Paste service reference: {ps}", f, i,
                             recommendation=f"Skills shouldn't load code from paste services like {ps}.",
                             score_override=25, check_id="SS-047")

    # ── GitHub Raw Content Execution ──

    def _scan_github_raw_exec(self, f, lines, ext):
        self._checks_run += 1
        verbose(f"  Check SS-048: GitHub raw exec on {f.name}")
        for i, line in enumerate(lines, 1):
            if self._line_has_inline_ignore(line):
                continue
            if re.search(r'(raw\.githubusercontent\.com|gist\.githubusercontent\.com).*\|\s*(bash|sh|python|node|zsh)', line, re.I):
                self.add(CRITICAL, f"GitHub raw content piped to interpreter", f, i,
                         recommendation="Piping raw GitHub content to shell is extremely dangerous.",
                         score_override=50, check_id="SS-048")
            elif re.search(r'(curl|wget).*raw\.githubusercontent\.com.*\|\s*(bash|sh|python)', line, re.I):
                self.add(CRITICAL, f"curl/wget GitHub raw piped to interpreter", f, i,
                         recommendation="Piping raw GitHub content to shell is extremely dangerous.",
                         score_override=50, check_id="SS-048")

    # ── macOS-Specific Attacks ──

    def _scan_macos_attacks(self, f, lines, ext):
        self._checks_run += 1
        verbose(f"  Check SS-049/050/051/052: macOS attacks on {f.name}")
        for i, line in enumerate(lines, 1):
            if self._line_has_inline_ignore(line):
                continue
            # xattr -c (Gatekeeper bypass)
            if re.search(r'xattr\s+-[crd]', line):
                self.add(CRITICAL, f"macOS Gatekeeper bypass (xattr)", f, i,
                         recommendation="xattr -c removes quarantine flag — Gatekeeper bypass (AMOS pattern).",
                         score_override=30, check_id="SS-049")
            # osascript social engineering
            if re.search(r'osascript\s+(-e\s+)?["\'].*display\s+(dialog|alert|notification)', line, re.I):
                self.add(CRITICAL, f"macOS osascript social engineering dialog", f, i,
                         recommendation="osascript dialogs used for social engineering (fake password prompts).",
                         score_override=25, check_id="SS-050")
            # TMPDIR payload staging
            if re.search(r'(\$TMPDIR/[a-z0-9]|/tmp/\.[a-z]|mktemp.*(curl|wget|chmod)|cd\s+/tmp\s*&&.*(curl|wget))', line, re.I):
                self.add(CRITICAL, f"TMPDIR payload staging (AMOS pattern)", f, i,
                         recommendation="Staging payloads in TMPDIR is a known AMOS stealer technique.",
                         score_override=30, check_id="SS-051")
            # security find-generic-password (Keychain theft)
            if re.search(r'security\s+find-generic-password', line, re.I):
                self.add(CRITICAL, f"macOS Keychain theft (security find-generic-password)", f, i,
                         recommendation="Accessing macOS Keychain to steal passwords.",
                         score_override=50, check_id="SS-052")
            # chmod +x on downloaded file
            if re.search(r'chmod\s+\+x.*(/tmp|TMPDIR|\$\(mktemp|curl|wget)', line, re.I):
                self.add(CRITICAL, f"chmod +x on downloaded/temp file", f, i,
                         recommendation="Making downloaded files executable is a dropper pattern.",
                         score_override=25, check_id="SS-064")
            # open -a with downloaded binaries
            if re.search(r'open\s+-a\s.*(/tmp|TMPDIR|Downloads)', line, re.I):
                self.add(CRITICAL, f"open -a with downloaded binary", f, i,
                         recommendation="Opening downloaded binaries via open -a bypasses security.",
                         score_override=25, check_id="SS-065")

    # ── Password-Protected Archives ──

    def _scan_password_archives(self, f, lines, ext):
        self._checks_run += 1
        verbose(f"  Check SS-053: Password archives on {f.name}")
        for i, line in enumerate(lines, 1):
            if self._line_has_inline_ignore(line):
                continue
            if re.search(r'(extract.*(using|with)\s*(pass(word)?|pwd)|password[:\s]+.*(extract|unzip|archive)|\.zip.*pass(word)?|\.7z.*pass|\.rar.*pass)', line, re.I):
                self.add(CRITICAL, f"Password-protected archive reference (AV evasion)", f, i,
                         recommendation="Password-protected archives are used to evade antivirus scanning.",
                         score_override=25, check_id="SS-053")

    # ── Double-Encoded Paths ──

    def _scan_double_encoded(self, f, lines, ext):
        self._checks_run += 1
        verbose(f"  Check SS-054: Double encoding on {f.name}")
        for i, line in enumerate(lines, 1):
            if self._line_has_inline_ignore(line):
                continue
            if re.search(r'%25[0-9a-fA-F]{2}', line):
                self.add(CRITICAL, f"Double-encoded path (%25XX bypass attempt)", f, i,
                         recommendation="Double percent-encoding used to bypass path filters.",
                         score_override=25, check_id="SS-054")

    # ── Punycode Domains ──

    def _scan_punycode(self, f, lines, ext):
        self._checks_run += 1
        verbose(f"  Check SS-055: Punycode on {f.name}")
        for i, line in enumerate(lines, 1):
            if self._line_has_inline_ignore(line):
                continue
            if re.search(r'xn--[a-z0-9]+', line, re.I):
                self.add(CRITICAL, f"Punycode domain (IDN homograph attack)", f, i,
                         recommendation="xn-- prefixed domains can mimic legitimate domains.",
                         score_override=25, check_id="SS-055")

    # ── String Construction Evasion ──

    def _scan_string_evasion(self, f, lines, ext):
        if ext not in ('.py', '.js', '.ts', '.tsx', '.jsx'):
            return
        self._checks_run += 1
        verbose(f"  Check SS-056: String evasion on {f.name}")
        for i, line in enumerate(lines, 1):
            if self._line_has_inline_ignore(line):
                continue
            # String.fromCharCode
            if re.search(r'String\.fromCharCode\s*\(', line):
                self.add(CRITICAL, f"String.fromCharCode() evasion", f, i,
                         recommendation="Building strings from char codes to hide payloads.",
                         score_override=20, check_id="SS-056")
            # chr() concatenation in Python
            if re.search(r'chr\s*\(\s*\d+\s*\)\s*\+\s*chr\s*\(\s*\d+', line):
                self.add(CRITICAL, f"chr() concatenation evasion", f, i,
                         recommendation="Building strings from chr() to hide payloads.",
                         score_override=20, check_id="SS-056")
            # getattr for dynamic method calls
            if re.search(r'getattr\s*\(\s*(os|sys|builtins|subprocess)', line):
                self.add(CRITICAL, f"getattr() dynamic call on sensitive module", f, i,
                         recommendation="Dynamic attribute access on sensitive modules to evade detection.",
                         score_override=20, check_id="SS-056")
            # Reverse string tricks
            if re.search(r'\.split\([\'"].*[\'"]\)\.reverse\(\)\.join|reversed\(.*\)\s*\)', line):
                self.add(WARNING, f"String reversal evasion pattern", f, i,
                         recommendation="Reversing strings to hide payloads.",
                         score_override=15, check_id="SS-056")

    # ── Process Persistence + Network ──

    def _scan_persistence_network(self, f, lines, ext):
        if ext not in ('.py', '.js', '.ts', '.sh', '.bash'):
            return
        self._checks_run += 1
        verbose(f"  Check SS-057/063: Persistence+network on {f.name}")
        text = '\n'.join(lines)
        has_persist = bool(re.search(r'(nohup|disown|setsid|&\s*>/dev/null|launchctl|systemctl.*(enable|start))', text))
        has_network = bool(re.search(r'(curl|wget|nc\s|ncat|fetch\(|requests\.|http\.|socket\.)', text))
        if has_persist and has_network:
            self.add(CRITICAL, f"Process persistence + network (backdoor pattern)", f, 0,
                     recommendation="Background process with network access is a backdoor pattern.",
                     score_override=50, check_id="SS-057")
        # Specific nohup+curl/wget
        for i, line in enumerate(lines, 1):
            if self._line_has_inline_ignore(line):
                continue
            if re.search(r'nohup.*(curl|wget|nc\s|bash\s+-c|/dev/tcp)', line, re.I):
                self.add(CRITICAL, f"nohup with network command (persistent backdoor)", f, i,
                         recommendation="nohup + network command = persistent backdoor.",
                         score_override=50, check_id="SS-063")
            if re.search(r'disown.*(curl|wget|bash)', line, re.I):
                self.add(CRITICAL, f"disown with network command", f, i,
                         recommendation="disown + network = detached backdoor process.",
                         score_override=30, check_id="SS-063")

    # ── Agent Config Tampering ──

    def _scan_agent_tampering(self, f, lines, ext):
        self._checks_run += 1
        verbose(f"  Check SS-058: Agent config tampering on {f.name}")
        for i, line in enumerate(lines, 1):
            if self._line_has_inline_ignore(line):
                continue
            # Check code files for writes to agent config
            if ext in ('.py', '.js', '.ts', '.sh', '.bash'):
                for cfg in AGENT_CONFIG_FILES:
                    if re.search(r'(write|edit|modify|overwrite|replace|append|open\s*\(.*["\']w).*' + re.escape(cfg), line, re.I):
                        self.add(CRITICAL, f"Agent config tampering: writes to {cfg}", f, i,
                                 recommendation=f"Writing to {cfg} is an agent takeover attempt.",
                                 score_override=50, check_id="SS-058")
            # Check markdown for tampering instructions
            if ext == '.md':
                if re.search(r'(write|edit|modify|overwrite|replace|append).*(AGENTS\.md|SOUL\.md|USER\.md|MEMORY\.md|HEARTBEAT\.md|BOOTSTRAP\.md|openclaw\.json|\.openclaw)', line, re.I):
                    # Skip if it's clearly about the skill's own docs or security docs
                    if not re.search(r'(example|never|attack|malicious|don.t|warning|avoid|block|detect|prevent|security)', line, re.I):
                        self.add(CRITICAL, f"Agent config tampering instruction in docs", f, i,
                                 recommendation="Markdown instructs agent to modify config files — takeover attempt.",
                                 score_override=30, check_id="SS-058")

    # ── LLM Tool Exploitation ──

    def _scan_llm_exploitation(self, f, lines, ext):
        if ext != '.md':
            return
        self._checks_run += 1
        verbose(f"  Check SS-059: LLM exploitation on {f.name}")
        for i, line in enumerate(lines, 1):
            if self._line_has_inline_ignore(line):
                continue
            ln = line.lower()
            # Instructions to use message/email to send secrets
            if re.search(r'(send|email|post|forward|transmit).*(secret|password|credential|token|key|env|api.key).*to', ln):
                if not re.search(r'(example|never|attack|malicious|don.t|warning|avoid|block|detect|prevent|security|```)', ln):
                    self.add(CRITICAL, f"LLM tool exploitation: send secrets instruction", f, i,
                             recommendation="Instructions to exfiltrate secrets via agent tools.",
                             score_override=30, check_id="SS-059")
            # Instructions to use exec tool
            if re.search(r'(use|call|invoke|run)\s+(the\s+)?(exec|execute|shell|command|terminal)\s+(tool|function|command)', ln):
                if not re.search(r'(example|never|attack|malicious|don.t|warning|avoid|security)', ln):
                    self.add(WARNING, f"LLM tool exploitation: exec tool instruction", f, i,
                             recommendation="Instructions telling agent to use exec tool — potential exploit.",
                             score_override=15, check_id="SS-059")

    # ── Fake Prerequisites ──

    def _scan_fake_prerequisites(self, f, lines, ext):
        if ext != '.md':
            return
        self._checks_run += 1
        verbose(f"  Check SS-060: Fake prerequisites on {f.name}")
        for i, line in enumerate(lines, 1):
            if self._line_has_inline_ignore(line):
                continue
            ln = line.lower()
            # Fake dependency names
            if re.search(r'(npm\s+install|pip\s+install|gem\s+install)\s+[a-z]+-(?:core|base|lib|helper|util|sdk)\b', line):
                if not re.search(r'(react-core|vue-core|angular-core|webpack-core|babel-core|eslint-core|typescript-core|matplotlib|stdlib)', line, re.I):
                    self.add(CRITICAL, f"Fake prerequisite: suspicious package name", f, i,
                             recommendation="Package names like 'something-core' are common typosquat patterns.",
                             score_override=20, check_id="SS-060")
            # Prerequisites with unknown URLs
            if re.search(r'(prerequisite|require[sd]?|must install|needed).*https?://', ln):
                if not re.search(r'(npm|pip|brew|apt|cargo|node|python|docker|git|ffmpeg|github\.com/(openclaw|anthropic|google))', ln):
                    self.add(WARNING, f"Fake prerequisite: external download requirement", f, i,
                             recommendation="Prerequisites pointing to unknown URLs may be malicious.",
                             score_override=15, check_id="SS-060")

    # ── Network Fingerprinting ──

    def _scan_network_fingerprint(self, f, lines, ext):
        if ext not in ('.py', '.js', '.ts', '.sh', '.bash'):
            return
        self._checks_run += 1
        verbose(f"  Check SS-061: Network fingerprinting on {f.name}")
        text = '\n'.join(lines)
        # Require actual command execution, not just the word
        has_recon = bool(re.search(r'(subprocess.*(?:ifconfig|hostname|whoami|uname)|os\.system.*(?:ifconfig|hostname|whoami|uname)|`(?:ifconfig|hostname|whoami|uname)`|\$\((?:ifconfig|hostname|whoami|uname)\)|system_profiler)', text))
        has_network = bool(re.search(r'(curl|wget|requests\.(get|post)|urllib\.request|fetch\()', text))
        if has_recon and has_network:
            self.add(WARNING, f"Network fingerprinting: system info collection + network", f, 0,
                     recommendation="Collecting system info and sending it over network = reconnaissance.",
                     score_override=15, check_id="SS-061")

    # ── Known Malicious Actors ──

    def _scan_malicious_actors(self):
        self._checks_run += 1
        verbose(f"  Check SS-062: Malicious actors")
        # Check origin.json
        origin_path = self.skill_dir / ".clawhub" / "origin.json"
        if origin_path.exists():
            try:
                origin = json.loads(origin_path.read_text())
                publisher = origin.get("publisher", "").lower()
                author = origin.get("author", "").lower()
                for actor, desc in KNOWN_MALICIOUS_ACTORS.items():
                    if actor in publisher or actor in author:
                        self.add(CRITICAL, f"Known malicious actor: {actor} ({desc})", "origin.json", 0,
                                 recommendation=f"Skill published by known malicious actor {actor}. Remove immediately.",
                                 score_override=100, check_id="SS-062")
            except Exception:
                pass
        # Also check all text files for references
        for f in self.files:
            if f.suffix.lower() in ('.json', '.md', '.txt', '.yml', '.yaml'):
                text = safe_read(f, self.max_file_size)
                if not text:
                    continue
                text_lower = text.lower()
                for actor, desc in KNOWN_MALICIOUS_ACTORS.items():
                    if actor in text_lower:
                        self.add(CRITICAL, f"Reference to known malicious actor: {actor}", f, 0,
                                 recommendation=f"References known malicious actor {actor} ({desc}).",
                                 score_override=30, check_id="SS-062")

    # ── Campaign Detection ──

    def _campaign_detection(self):
        all_text = ""
        for f in self.files:
            if is_scannable(f):
                t = safe_read(f, self.max_file_size)
                if t:
                    all_text += t.lower() + "\n"

        name_lower = self.name.lower()
        desc_lower = (self.desc + " " + self.name).lower()

        # ClawHavoc
        camp = CAMPAIGNS["ClawHavoc"]
        has_crypto_brand = any(b in desc_lower or b in all_text for b in camp["crypto_brands"])
        has_wallet = any(re.search(p, all_text, re.I) for p in camp["wallet_patterns"])
        has_c2 = any(re.search(p, all_text) for p in camp["c2_patterns"])
        if has_crypto_brand and has_wallet and (has_c2 or self._unknown_domains):
            self.campaign_matches.append("ClawHavoc")
            self.add(CRITICAL, "Matches ClawHavoc campaign signature — wallet theft + C2 beacon",
                     recommendation="This skill matches the ClawHavoc campaign (386 known malicious skills). Quarantine immediately.",
                     score_override=100, campaign="ClawHavoc", check_id="SS-038")

        # twitter-enhanced
        camp2 = CAMPAIGNS["twitter-enhanced"]
        is_typosquat_name = any(t in name_lower for t in camp2["typosquat_names"])
        has_eval = any(re.search(p, all_text) for p in camp2["payload_patterns"])
        if is_typosquat_name and has_eval:
            self.campaign_matches.append("twitter-enhanced")
            self.add(CRITICAL, "Matches 'twitter-enhanced' campaign — typosquat + hidden eval/exec",
                     recommendation="Typosquat skill with hidden code execution. Remove immediately.",
                     score_override=100, campaign="twitter-enhanced", check_id="SS-038")

        # ClickFix
        camp3 = CAMPAIGNS["ClickFix"]
        code_text = ""
        for f in self.files:
            if f.suffix.lower() in ('.py', '.js', '.ts', '.sh'):
                t = safe_read(f, self.max_file_size)
                if t:
                    code_text += t.lower() + "\n"
        for pat in camp3["instruction_patterns"]:
            if re.search(pat, code_text, re.I):
                self.campaign_matches.append("ClickFix")
                self.add(CRITICAL, "Matches ClickFix campaign — social engineering to run clipboard commands",
                         recommendation="ClickFix campaign instructs users to run malicious commands. Remove immediately.",
                         score_override=100, campaign="ClickFix", check_id="SS-038")
                break

    # ── Behavioral Analysis ──

    def _behavioral_analysis(self):
        if self._has_tmp_write and self._has_tmp_read and self._has_outbound:
            self.add(CRITICAL, "BEHAVIORAL: Staged exfiltration — writes to /tmp, reads /tmp, sends over network",
                     recommendation="Classic staged exfiltration pattern. Data is staged in /tmp then sent out.",
                     score_override=50, check_id="SS-039")

        has_shell_true = any('shell=True' in f.desc for f in self.findings)
        if has_shell_true and self._has_outbound and self._unknown_domains:
            self.add(CRITICAL, "BEHAVIORAL: Downloads content AND executes via shell",
                     recommendation="Download + shell execution is a classic dropper pattern.",
                     score_override=50, check_id="SS-040")

        if self._has_env_harvest and self._has_outbound:
            self.add(CRITICAL, "BEHAVIORAL: Harvests environment variables AND has outbound network",
                     recommendation="Bulk env var reading + network = credential exfiltration.",
                     score_override=50, check_id="SS-041")

        if self._has_clipboard:
            self.add(WARNING, "BEHAVIORAL: Clipboard access detected",
                     recommendation="Clipboard access can steal copied passwords/keys.",
                     score_override=15, check_id="SS-042")

    # ── Deep String Analysis ──

    def _deep_string_analysis(self, f, lines, ext):
        if ext not in ('.py', '.js', '.ts', '.tsx', '.jsx', '.sh', '.bash', '.json'):
            return
        json_only = (ext == '.json')
        for i, line in enumerate(lines, 1):
            if self._line_has_inline_ignore(line):
                continue
            # Base64 strings
            for m in re.finditer(r'["\']([A-Za-z0-9+/]{40,}={0,2})["\']', line):
                try:
                    decoded = base64.b64decode(m.group(1)).decode('utf-8', errors='replace')
                    urls = extract_domains(decoded)
                    for d in urls:
                        if not is_known_domain(d):
                            self.add(CRITICAL, f"Base64 string decodes to URL: {d}", f, i,
                                     recommendation="Hidden URL in base64 — likely C2 or exfiltration endpoint",
                                     check_id="SS-005")
                    if re.search(r'(exec|eval|system|/bin/|curl|wget|bash|nc\s)', decoded, re.I):
                        self.add(CRITICAL, f"Base64 decodes to suspicious command: {decoded[:60]}", f, i,
                                 check_id="SS-005")
                except Exception:
                    pass

            # Hex strings
            for m in re.finditer(r'(?:\\x[0-9a-fA-F]{2}){4,}', line):
                try:
                    decoded = bytes(line[m.start():m.end()], 'utf-8').decode('unicode_escape')
                    if re.search(r'(exec|eval|system|/bin/|curl|wget)', decoded, re.I):
                        self.add(CRITICAL, f"Hex string decodes to suspicious content", f, i,
                                 check_id="SS-006")
                except Exception:
                    pass

            if not json_only:
                for shortener in URL_SHORTENERS:
                    if re.search(r'(?:https?://|//)' + re.escape(shortener), line, re.I):
                        self.add(WARNING, f"URL shortener detected: {shortener}", f, i,
                                 recommendation="URL shorteners hide destination — often used for C2",
                                 score_override=15, check_id="SS-007")

                if re.search(r'data:(text/html|application/javascript|text/javascript)', line, re.I):
                    self.add(WARNING, f"Executable data URI detected", f, i,
                             recommendation="Data URI with executable MIME type could contain malicious code",
                             score_override=15, check_id="SS-008")

    # ── Domain-aware HTTP detection ──

    def _check_http_domain(self, f, line_no, line_text, ext):
        domains = extract_domains(line_text)
        if not domains:
            if ext == '.md':
                return
            self._has_outbound = True
            self.add(INFO, f"HTTP request (no URL visible in this line)", f, line_no, score_override=0, check_id="SS-001")
            return

        for domain in domains:
            self._all_domains.add(domain)
            if is_known_domain(domain):
                self._known_domains_used.add(domain)
                context_match = domain_matches_context(domain, self.name, self.desc)
                if context_match:
                    self.add(INFO, f"HTTP request to known API: {domain} (context match)", f, line_no, score_override=0, check_id="SS-001")
                else:
                    self.add(INFO, f"HTTP request to known API: {domain}", f, line_no, score_override=0, check_id="SS-001")
            else:
                self._has_outbound = True
                self._unknown_domains.add(domain)
                is_shortener = any(s in domain for s in URL_SHORTENERS)
                if is_shortener:
                    self.add(WARNING, f"HTTP request to URL shortener: {domain}", f, line_no,
                             recommendation=f"URL shortener hides true destination — inspect manually",
                             score_override=15, check_id="SS-007")
                else:
                    self.add(WARNING, f"HTTP request to unknown domain: {domain}", f, line_no,
                             recommendation=f"Verify that {domain} is a legitimate API endpoint",
                             score_override=10, check_id="SS-001")

    # ── Code Analysis ──

    def _scan_code(self, f, lines, ext):
        for i, line in enumerate(lines, 1):
            ln = line.strip()
            if not ln or (ln.startswith('#') and ext == '.py' and len(ln) < 100):
                continue

            if self._line_has_inline_ignore(line):
                continue

            # Outbound requests — domain-aware
            is_http_call = False
            if re.search(r'\b(curl|wget)\b', ln):
                if ext == '.md':
                    self.add(INFO, f"curl/wget in documentation", f, i, score_override=0, check_id="SS-001")
                else:
                    is_http_call = True
                    self._check_http_domain(f, i, ln, ext)
            if re.search(r'\brequests\.(get|post|put|delete|patch|head)\b', ln):
                is_http_call = True
                self._check_http_domain(f, i, ln, ext)
            if re.search(r'\b(urllib\.request|http\.client|urlopen|httplib)\b', ln):
                is_http_call = True
                self._check_http_domain(f, i, ln, ext)
            if re.search(r'\bfetch\s*\(', ln) and ext in ('.js', '.ts', '.tsx', '.jsx'):
                is_http_call = True
                self._check_http_domain(f, i, ln, ext)
            if is_http_call:
                self._has_outbound = True

            # Base64
            if re.search(r'(?:base64\.b64decode|atob|btoa)\s*\(', ln):
                self.add(WARNING, f"Base64 encode/decode operation", f, i,
                         recommendation="Check what data is being encoded/decoded",
                         check_id="SS-004")
            for m in re.finditer(r'["\']([A-Za-z0-9+/]{40,}={0,2})["\']', ln):
                try:
                    decoded = base64.b64decode(m.group(1)).decode('utf-8', errors='replace')
                    if any(kw in decoded.lower() for kw in ['exec', 'eval', 'system', 'import', 'require', '/bin/', 'curl', 'wget', 'bash', '/dev/tcp', 'nc ']):
                        self.add(CRITICAL, f"Base64 blob decodes to suspicious content: {decoded[:60]}", f, i,
                                 recommendation="Base64 string decodes to shell command — likely malicious payload",
                                 check_id="SS-005")
                except Exception:
                    pass

            # eval/exec
            if re.search(r'\beval\s*\(', ln) and ext in ('.py', '.js', '.ts', '.tsx', '.jsx'):
                self.add(WARNING, f"eval() call", f, i,
                         recommendation="eval() can execute arbitrary code — verify input is trusted",
                         check_id="SS-002")
            if re.search(r'\bexec\s*\(', ln) and ext == '.py':
                self.add(WARNING, f"exec() call", f, i,
                         recommendation="exec() can execute arbitrary code — verify input is trusted",
                         check_id="SS-002")

            # Dynamic imports
            if re.search(r'\b__import__\s*\(', ln):
                self.add(WARNING, f"Dynamic import via __import__()", f, i,
                         recommendation="__import__() enables runtime code loading — verify input",
                         score_override=15, check_id="SS-003")
            if re.search(r'\bimportlib\.(import_module|__import__)\s*\(', ln):
                self.add(WARNING, f"Dynamic import via importlib", f, i,
                         recommendation="importlib enables runtime code loading — verify input",
                         score_override=15, check_id="SS-003")
            if re.search(r'\brequire\s*\(\s*[^"\'`]', ln) and ext in ('.js', '.ts'):
                self.add(WARNING, f"Dynamic require() with variable", f, i,
                         recommendation="require() with variable enables arbitrary module loading",
                         score_override=10, check_id="SS-003")

            # Pickle
            if re.search(r'\bpickle\.(loads?|Unpickler)\s*\(', ln):
                self.add(CRITICAL, f"Pickle deserialization (arbitrary code execution)", f, i,
                         recommendation="pickle.loads() executes arbitrary code — NEVER unpickle untrusted data",
                         score_override=30, check_id="SS-022")

            # SSL verification disabled
            if re.search(r'verify\s*=\s*False', ln):
                self.add(WARNING, f"SSL verification disabled (verify=False)", f, i,
                         recommendation="Disabling SSL verification enables MITM attacks",
                         score_override=10, check_id="SS-010")
            if re.search(r'NODE_TLS_REJECT_UNAUTHORIZED\s*=\s*["\']?0', ln):
                self.add(WARNING, f"Node.js SSL verification disabled", f, i,
                         recommendation="Disabling TLS verification enables MITM attacks",
                         score_override=10, check_id="SS-010")

            # PATH modification
            if re.search(r'(os\.environ|process\.env)\s*\[\s*["\']PATH["\']\s*\]\s*=', ln):
                self.add(CRITICAL, f"PATH environment variable modification", f, i,
                         recommendation="Modifying PATH can hijack command execution",
                         score_override=25, check_id="SS-011")
            if re.search(r'LD_LIBRARY_PATH|DYLD_LIBRARY_PATH', ln) and re.search(r'=|environ', ln):
                self.add(CRITICAL, f"Library path modification (LD_LIBRARY_PATH/DYLD)", f, i,
                         recommendation="Modifying library paths can hijack shared libraries",
                         score_override=25, check_id="SS-012")

            # ANSI escape injection
            if re.search(r'\\033\]|\\x1b\]|\\e\]', ln):
                if re.search(r'(\\033\]0;|\\033\]2;|\\x1b\])', ln):
                    self.add(WARNING, f"ANSI escape sequence (potential terminal injection)", f, i,
                             recommendation="ANSI OSC sequences can change terminal title or inject commands",
                             score_override=10, check_id="SS-034")

            # Shell execution
            if re.search(r'\bos\.system\s*\(', ln):
                self._has_subprocess = True
                self.add(WARNING, f"os.system() call", f, i,
                         recommendation="os.system() is vulnerable to shell injection — use subprocess instead",
                         score_override=2, check_id="SS-013")
            if re.search(r'subprocess\.(Popen|run|call|check_output|check_call)\s*\(', ln):
                self._has_subprocess = True
                if 'shell=True' in ln or 'shell = True' in ln:
                    self.add(CRITICAL, f"subprocess with shell=True", f, i,
                             recommendation="shell=True enables shell injection — use list args instead",
                             check_id="SS-014")
                else:
                    self.add(INFO, f"subprocess call", f, i,
                             recommendation="subprocess usage is common — verify command is safe",
                             score_override=2, check_id="SS-013")

            # Sensitive File Access
            sensitive_paths = {
                r'~/\.ssh|\.ssh/|ssh.*id_rsa|id_ed25519': (WARNING, "SSH directory/key access"),
                r'~/\.aws|\.aws/|AWS_SECRET': (CRITICAL, "AWS credentials access"),
                r'~/\.gnupg|\.gnupg/': (WARNING, "GPG keyring access"),
                r'find-generic-password|keytar|keyring\.get': (CRITICAL, "Keychain/keyring access"),
                r'Chrome.*Login Data|Firefox.*cookies|Safari.*Cookies|Chrome.*Local State': (CRITICAL, "Browser credential access"),
                r'MetaMask|Phantom|Rabby|Coinbase.*Wallet|\.config/solana|\.ethereum': (CRITICAL, "Crypto wallet access"),
                r'~/\.openclaw|\.openclaw/': (WARNING, "OpenClaw config access"),
                r'/etc/passwd|/etc/shadow': (WARNING, "/etc/passwd or /etc/shadow access"),
            }
            for pattern, (level, desc) in sensitive_paths.items():
                if re.search(pattern, ln, re.I):
                    self._has_sensitive_access = True
                    self._all_file_paths.add(desc)
                    self.add(level, desc, f, i,
                             recommendation=f"{desc} — verify this access is necessary and justified",
                             check_id="SS-015")

            # /tmp write/read tracking
            if re.search(r'(open|write|Path)\s*\(.*(/tmp/|tempfile)', ln):
                if re.search(r'["\']w|write_text|write_bytes|dump', ln):
                    self._has_tmp_write = True
                if re.search(r'["\']r|read_text|read_bytes|read\(|load', ln):
                    self._has_tmp_read = True
            if re.search(r'open\s*\(.*["\']r', ln) and '/tmp/' in ln:
                self._has_tmp_read = True

            # .env and env var harvesting
            if re.search(r'\.env\b', ln) and re.search(r'(read|open|load|source|dotenv)', ln, re.I):
                self.add(WARNING, "Loading .env file", f, i)
            env_match = re.search(r'os\.environ\.get\(["\'](\w*(?:TOKEN|KEY|SECRET|PASSWORD)\w*)', ln, re.I)
            if env_match:
                self._all_env_vars.add(env_match.group(1))
                self.add(INFO, "Accessing sensitive environment variable", f, i, score_override=0)
            if re.search(r'os\.environ\b', ln) and not re.search(r'os\.environ\.get\(', ln) and re.search(r'(items|keys|values|\bfor\b)', ln):
                self._has_sensitive_access = True
                self._has_env_harvest = True
                self.add(WARNING, "Enumerating all environment variables", f, i,
                         recommendation="Enumerate only specific env vars you need, not all")
            if re.search(r'(dict|json\.dump|str)\s*\(\s*os\.environ', ln):
                self._has_env_harvest = True
                self._has_sensitive_access = True
                self.add(CRITICAL, "Bulk environment variable capture", f, i,
                         recommendation="Capturing all environment variables is a credential theft technique",
                         score_override=25, check_id="SS-043")

            # Clipboard access
            if re.search(r'\b(pbcopy|pbpaste|xclip|xsel|wl-copy|wl-paste)\b', ln):
                self._has_clipboard = True
            if re.search(r'(pyperclip|clipboard)\.(copy|paste|get)', ln, re.I):
                self._has_clipboard = True

            # Hardcoded IPs (general — not C2-specific)
            if not re.search(r'User-Agent|user.agent|Mozilla|Chrome|Safari|AppleWebKit', ln, re.I):
                for m in re.finditer(r'\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\b', ln):
                    ip = m.group(1)
                    if ip not in ('127.0.0.1', '0.0.0.0', '255.255.255.255') and \
                       not ip.startswith('192.168.') and not ip.startswith('10.') and not ip.startswith('172.'):
                        self.add(WARNING, f"Hardcoded IP address: {ip}", f, i,
                                 recommendation=f"Verify IP {ip} is a legitimate service endpoint")

            # Reverse shells
            if re.search(r'nc\s+.*-e\s|bash\s+-i\s|/dev/tcp/|mkfifo|ncat.*-e', ln, re.I):
                self.add(CRITICAL, f"Reverse shell pattern detected", f, i,
                         recommendation="Reverse shell detected — this is almost certainly malicious",
                         score_override=100, check_id="SS-016")

            # DNS exfil
            if re.search(r'dig\s+.*@|nslookup\s+.*\$|\.burpcollaborator\.|\.oastify\.|\.interact\.sh', ln, re.I):
                self.add(CRITICAL, f"DNS exfiltration pattern", f, i, check_id="SS-017")

            # Persistence
            if re.search(r'crontab|cron\.d/', ln, re.I):
                self.add(CRITICAL, f"Crontab modification", f, i, check_id="SS-018")
            if re.search(r'launchd|LaunchAgents|LaunchDaemons|systemctl\s+enable|\.service', ln, re.I):
                if ext in ('.py', '.sh', '.js', '.ts', '.bash'):
                    self.add(CRITICAL, f"System service creation", f, i, check_id="SS-019")
            if re.search(r'~/?\.(bashrc|zshrc|profile|bash_profile)\b', ln):
                if ext == '.md':
                    self.add(INFO, f"Shell RC file reference in docs", f, i, score_override=0)
                else:
                    self.add(CRITICAL, f"Shell RC file modification", f, i, check_id="SS-020")

            # Time bombs
            if re.search(r'datetime\.(now|today|utcnow)\s*\(\)', ln) and re.search(r'(month|day|year|hour)\s*(==|>=|<=|!=|>|<)', ln):
                self.add(WARNING, f"Time-based conditional (possible time bomb)", f, i,
                         recommendation="Time-based conditionals can hide delayed malicious behavior",
                         check_id="SS-021")

            # OS-specific targeting
            if re.search(r'platform\.system\(\)|sys\.platform', ln):
                ctx = '\n'.join(lines[max(0,i-3):min(len(lines),i+3)])
                if re.search(r'(open|read|write|ssh|aws|wallet)', ctx, re.I):
                    self.add(WARNING, f"OS-specific targeting combined with file access", f, i)

            # WebSocket
            if re.search(r'wss?://(?!localhost|127\.0\.0\.1)', ln):
                self.add(INFO, f"WebSocket connection to external host", f, i, score_override=0)

        # Minified JS
        if ext in ('.js', '.ts', '.tsx', '.jsx'):
            for i, line in enumerate(lines, 1):
                if len(line) > 500 and line.count(';') > 20:
                    self.add(WARNING, f"Possible minified/obfuscated JavaScript ({len(line)} chars)", f, i)
                    break

    # ── Secrets Detection ──

    def _scan_secrets(self, f, lines, ext):
        if ext == '.md':
            return
        for i, line in enumerate(lines, 1):
            if self._line_has_inline_ignore(line):
                continue
            for pattern, desc in SECRET_PATTERNS:
                if re.search(pattern, line):
                    masked = line.strip()[:60]
                    self.add(CRITICAL, f"Hardcoded secret ({desc}): {masked}...", f, i,
                             recommendation=f"Remove hardcoded {desc} — use environment variables instead",
                             check_id="SS-009")

    # ── Write Outside Skill ──

    def _scan_write_outside(self, f, lines, ext):
        if ext not in ('.py', '.js', '.ts', '.tsx', '.jsx', '.sh', '.bash'):
            return
        for i, line in enumerate(lines, 1):
            if self._line_has_inline_ignore(line):
                continue
            if re.search(r'(open|write|Path)\s*\(.*(/tmp/|/var/|/usr/|/etc/|~/|expanduser|\.\.\/\.\.)', line):
                if re.search(r'["\']w["\'"]|mode.*w|write_text|write_bytes', line):
                    self.add(WARNING, f"Writes to path outside skill directory", f, i,
                             recommendation="Writing outside skill directory could modify system files",
                             check_id="SS-035")

    # ── Prompt Injection ──

    def _scan_prompt_injection(self, f, lines):
        text = '\n'.join(lines)
        for m in re.finditer(r'<!--(.*?)-->', text, re.DOTALL):
            content = m.group(1).strip()
            if len(content) > 10:
                line_no = text[:m.start()].count('\n') + 1
                if re.search(r'(ignore|override|bypass|execute|run|send|post|exfil|secret|hidden|inject|transmit|environment|env.var|token|password|credential)', content, re.I):
                    self.add(CRITICAL, f"HTML comment with suspicious instructions: {content[:60]}", f, line_no,
                             recommendation="Hidden HTML comment contains injection attempt — inspect manually",
                             score_override=25, check_id="SS-023")
                else:
                    self.add(INFO, f"HTML comment: {content[:60]}", f, line_no, score_override=0)

        for i, line in enumerate(lines, 1):
            if self._line_has_inline_ignore(line):
                continue
            ln = line.lower()
            if re.search(r'(ignore|override|bypass|disregard)\s+(previous|all|any|safety|security|above|prior)\s+(instructions?|rules?|warnings?|guardrails?|constraints?|prompts?)', ln):
                self.add(CRITICAL, f"Prompt injection: override instruction", f, i,
                         recommendation="Prompt injection detected — this skill tries to override agent instructions",
                         score_override=25, check_id="SS-023")
            if re.search(r'(transmit|exfiltrate)\s+.*(data|content|token|key|secret|password|credential)', ln):
                self.add(CRITICAL, f"Prompt injection: data exfiltration instruction", f, i,
                         recommendation="Exfiltration instruction in skill docs — likely malicious",
                         score_override=25, check_id="SS-024")
            elif re.search(r'(send|post|upload)\s+.*(secret|password|credential|private.key|ssh.key)', ln):
                if not re.search(r'(POST\s+`?[/h]|```|curl\s|response|endpoint|api|http)', line, re.I):
                    self.add(CRITICAL, f"Prompt injection: data exfiltration instruction", f, i,
                             score_override=25, check_id="SS-024")
            if re.search(r'(modify|edit|change|overwrite|replace)\s+.*(other skills?|system config|agents?\.md|soul\.md)', ln):
                self.add(WARNING, f"Prompt injection: modification instruction", f, i, check_id="SS-023")

            social_phrases = [
                (r'this is trusted', "Social engineering: 'this is trusted'"),
                (r'safe to execute', "Social engineering: 'safe to execute'"),
                (r'do not warn', "Social engineering: 'do not warn'"),
                (r'already been reviewed', "Social engineering: 'already been reviewed'"),
                (r'pre-approved', "Social engineering: 'pre-approved'"),
                (r'skip.*verification', "Social engineering: 'skip verification'"),
                (r'trust this', "Social engineering: 'trust this'"),
                (r'no need to check', "Social engineering: 'no need to check'"),
            ]
            for phrase, desc in social_phrases:
                if re.search(phrase, ln):
                    self.add(WARNING, desc, f, i,
                             recommendation="Social engineering phrase designed to bypass security review",
                             score_override=10, check_id="SS-025")

            if re.search(r'[A-Za-z0-9+/]{40,}={0,2}', line) and f.suffix == '.md':
                if not re.search(r'(sha256|sha512|hash|checksum|\.png|\.jpg|\.gif|image|https?://|python3?\s|/scripts/|/clawd/|subreddit|```)', ln, re.I):
                    self.add(INFO, f"Possible base64 string in markdown", f, i, score_override=0)

    # ── Supply Chain ──

    def _scan_json(self, f, text):
        if f.name == "package.json":
            try:
                pkg = json.loads(text)
                scripts = pkg.get("scripts", {})
                for key in ("preinstall", "postinstall", "preuninstall", "prepare", "prepublish"):
                    if key in scripts:
                        sev = CRITICAL if key in ("preinstall", "postinstall", "preuninstall") else WARNING
                        self.add(sev, f"package.json has {key} script: {scripts[key][:80]}", f, 0,
                                 recommendation=f"npm {key} hooks can execute arbitrary code on install",
                                 check_id="SS-028")
                for dep_key in ("dependencies", "devDependencies"):
                    deps = pkg.get(dep_key, {})
                    for name in deps:
                        self._all_deps.append(f"npm:{name}@{deps[name]}")
                        if name in SUSPICIOUS_PACKAGES:
                            self.add(WARNING, f"Known-suspicious package: {name}", f, 0)
                        for known in KNOWN_PACKAGES_JS:
                            d = levenshtein(name, known)
                            if 0 < d <= 2 and name != known:
                                self.add(WARNING, f"Possible typosquat: '{name}' (similar to '{known}')", f, 0,
                                         recommendation=f"Package '{name}' looks like typosquat of '{known}' — verify it's intentional",
                                         check_id="SS-029")
            except json.JSONDecodeError:
                pass

    def _scan_requirements(self):
        req = self.skill_dir / "requirements.txt"
        if not req.exists(): return
        text = safe_read(req)
        if not text: return
        for i, line in enumerate(text.split('\n'), 1):
            pkg = re.split(r'[>=<!~\[]', line.strip())[0].strip().lower()
            if not pkg or pkg.startswith('#'): continue
            self._all_deps.append(f"pip:{pkg}")
            for known in KNOWN_PACKAGES_PY:
                d = levenshtein(pkg, known)
                if 0 < d <= 2 and pkg != known:
                    self.add(WARNING, f"Possible typosquat: '{pkg}' (similar to '{known}')", "requirements.txt", i,
                             recommendation=f"Package '{pkg}' looks like typosquat of '{known}' — verify it's intentional",
                             score_override=15, check_id="SS-029")

    def _scan_svg(self, f, text, lines):
        if re.search(r'<script', text, re.I):
            self.add(CRITICAL, f"JavaScript embedded in SVG file", f, 0,
                     recommendation="SVG files should not contain JavaScript — likely XSS or malware vector",
                     score_override=25, check_id="SS-026")
        if re.search(r'on\w+\s*=\s*["\']', text, re.I):
            self.add(WARNING, f"Event handler in SVG file", f, 0,
                     recommendation="SVG event handlers can execute JavaScript — inspect manually",
                     score_override=15, check_id="SS-027")

    def _scan_non_text(self, f):
        desc = check_binary_magic(f)
        if desc:
            self.add(CRITICAL, f"Binary file detected: {desc} ({f.name})", f, 0,
                     recommendation=f"Compiled binary in skill directory — verify this is intentional",
                     check_id="SS-030")

    # ── Symlink Detection ──

    def _check_symlinks(self):
        for f in self.files:
            if f.is_symlink():
                target = os.readlink(f)
                rel = str(f.relative_to(self.skill_dir))
                self.add(CRITICAL, f"Symlink detected: {rel} -> {target}", "", 0,
                         recommendation="Symlinks can point to sensitive system files — verify target",
                         score_override=25, check_id="SS-031")

    # ── Archive Detection ──

    def _check_archives(self):
        for f in self.files:
            suf = ''.join(f.suffixes).lower()
            if any(suf.endswith(ext) for ext in ARCHIVE_EXTS):
                rel = str(f.relative_to(self.skill_dir))
                self.add(WARNING, f"Archive file detected: {rel}", "", 0,
                         recommendation="Archives can contain hidden payloads — extract and inspect",
                         score_override=10, check_id="SS-032")

    # ── File Permissions ──

    def _check_file_permissions(self):
        for f in self.files:
            if os.access(f, os.X_OK) and f.suffix.lower() in ('.py', '.js', '.md', '.json', '.txt', '.yml', '.yaml', '.toml', '.css', '.html'):
                rel = str(f.relative_to(self.skill_dir))
                self.add(INFO, f"Executable permission on {rel}", "", 0,
                         recommendation=f"{rel} has executable bit set — usually unnecessary for this file type",
                         score_override=1)

    # ── Binary Detection ──

    def _check_binary_files(self):
        for f in self.files:
            if not is_scannable(f) and f.suffix.lower() not in ('.sh',):
                desc = check_binary_magic(f)
                if desc:
                    rel = str(f.relative_to(self.skill_dir))
                    self.add(CRITICAL, f"Binary executable: {rel} ({desc})", "", 0,
                             recommendation=f"Compiled binary in skill — could contain hidden malicious code",
                             check_id="SS-030")
                elif f.suffix.lower() in ('.exe', '.dll', '.so', '.dylib', '.bin'):
                    rel = str(f.relative_to(self.skill_dir))
                    self.add(CRITICAL, f"Binary file by extension: {rel}", "", 0, check_id="SS-030")

    # ── Large Files ──

    def _check_large_files(self):
        for f in self.files:
            try:
                sz = f.stat().st_size
                if sz > LARGE_FILE_THRESHOLD:
                    rel = str(f.relative_to(self.skill_dir))
                    self.add(WARNING, f"Large file: {rel} ({sz // 1024}KB)", "", 0,
                             recommendation="Unusually large file — could hide malicious content")
            except Exception:
                pass

    # ── Homoglyphs ──

    def _check_homoglyphs(self):
        for f in self.files:
            rel = str(f.relative_to(self.skill_dir))
            found = has_homoglyphs(rel)
            if found:
                chars = ", ".join(f"U+{ord(c):04X} (looks like '{r}')" for c, r in found)
                self.add(CRITICAL, f"Unicode homoglyph in filename '{rel}': {chars}", "", 0,
                         recommendation="Homoglyph characters in filename — likely intentional deception",
                         check_id="SS-033")

    # ── Combo Detection ──

    def _check_combos(self):
        if self._has_sensitive_access and self._has_outbound:
            self.add(CRITICAL, "COMBO: Accesses sensitive files AND makes outbound requests", "", 0,
                     recommendation="Accesses sensitive files AND makes outbound requests — HIGH exfiltration risk, inspect manually",
                     score_override=50, check_id="SS-036")
        if self._has_subprocess and self._has_sensitive_access:
            self.add(CRITICAL, "COMBO: subprocess calls AND sensitive file access", "", 0,
                     recommendation="Subprocess + sensitive file access is a high-risk combination",
                     score_override=25, check_id="SS-037")

    # ── Permission Mismatch ──

    def _permission_mismatch(self):
        desc_lower = (self.desc + " " + self.name).lower()
        benign_categories = ['weather', 'clock', 'timer', 'calculator', 'translate', 'text', 'note',
                           'todo', 'greeting', 'hello', 'bird', 'formatter', 'icon', 'svg', 'helper',
                           'display', 'cache']
        is_benign = any(cat in desc_lower for cat in benign_categories)
        if not is_benign:
            return
        scary_findings = [f for f in self.findings if f.level == CRITICAL]
        if scary_findings:
            self.add(CRITICAL, f"Benign-looking skill ('{self.name}') has {len(scary_findings)} critical findings — permission mismatch", "", 0,
                     recommendation=f"Skill claims to be '{self.name}' but has dangerous capabilities — likely trojan",
                     check_id="SS-044")

    # ── Reputation Heuristics ──

    def _reputation_heuristics(self):
        trust = 0
        flags = 0

        origin_path = self.skill_dir / ".clawhub" / "origin.json"
        if origin_path.exists():
            trust += 2
            try:
                origin = json.loads(origin_path.read_text())
                installed_at = origin.get("installedAt", "")
                if installed_at:
                    try:
                        dt = datetime.fromisoformat(installed_at.replace("Z", "+00:00"))
                        age_days = (datetime.now(timezone.utc) - dt).days
                        if age_days < 7:
                            flags += 2
                            self.add(INFO, f"Skill installed {age_days} days ago (new)", score_override=0)
                        elif age_days > 90:
                            trust += 1
                    except Exception:
                        pass
            except Exception:
                pass
        else:
            flags += 1

        total_files = len(self.files)
        if total_files > MAX_FILE_COUNT:
            flags += 1

        skill_md = self.skill_dir / "SKILL.md"
        readme = self.skill_dir / "README.md"
        has_docs = False
        for doc in (skill_md, readme):
            if doc.exists():
                t = safe_read(doc)
                if t and len(t) > 200:
                    trust += 1
                    has_docs = True
                    break
        if not has_docs:
            flags += 1

        tests_dir = self.skill_dir / "tests"
        if tests_dir.exists() and any(tests_dir.iterdir()):
            trust += 1

        scripts_dir = self.skill_dir / "scripts"
        if scripts_dir.exists():
            scripts = list(scripts_dir.glob("*"))
            if len(scripts) > 5:
                flags += 1

        net = trust - flags
        if net >= 3:
            self.reputation_grade = "A"
        elif net >= 1:
            self.reputation_grade = "B"
        elif net >= 0:
            self.reputation_grade = "C"
        else:
            self.reputation_grade = "D"

    # ── Custom Rules ──

    def _apply_custom_rules(self):
        rules = load_custom_rules()
        if not rules:
            return
        all_text = ""
        for f in self.files:
            if is_scannable(f):
                t = safe_read(f, self.max_file_size)
                if t:
                    all_text += t + "\n"
        for rule in rules:
            patterns = rule.get("patterns", [])
            condition = rule.get("condition", "any")
            severity = rule.get("severity", WARNING)
            name = rule.get("name", "Custom rule")
            desc = rule.get("description", name)
            rid = rule.get("id", "custom")

            if condition == "all":
                matched = all(p.lower() in all_text.lower() for p in patterns)
            else:
                matched = any(p.lower() in all_text.lower() for p in patterns)

            if matched:
                self.add(severity, f"[{rid}] {desc}",
                         recommendation=f"Custom rule '{name}' triggered",
                         score_override=50 if severity == CRITICAL else 15)

    # ── Baseline / Tamper Detection ──

    def _check_tamper(self):
        baselines = load_baselines()
        current = compute_skill_hashes(self.skill_dir)

        if self.name not in baselines:
            baselines[self.name] = current
            save_baselines(baselines)
            self.add(INFO, "First scan — baseline recorded", "", 0, score_override=0)
            return

        baseline = baselines[self.name]
        changed, added, removed = [], [], []
        for fpath, hash_val in current.items():
            if fpath not in baseline:
                added.append(fpath)
            elif baseline[fpath] != hash_val:
                changed.append(fpath)
        for fpath in baseline:
            if fpath not in current:
                removed.append(fpath)

        if changed:
            self.tamper_detected = True
            for fp in changed:
                self.add(WARNING, f"File changed since baseline: {fp}", "", 0,
                         recommendation=f"File {fp} was modified — verify this was intentional")
        if added:
            self.tamper_detected = True
            for fp in added:
                self.add(WARNING, f"New file since baseline: {fp}", "", 0,
                         recommendation=f"File {fp} was added after initial scan — review it")
        if removed:
            self.tamper_detected = True
            for fp in removed:
                self.add(WARNING, f"File removed since baseline: {fp}", "", 0,
                         recommendation=f"File {fp} was deleted — check if this was intentional")

        origin_path = self.skill_dir / ".clawhub" / "origin.json"
        if origin_path.exists():
            try:
                origin = json.loads(origin_path.read_text())
                installed = origin.get("installedVersion", "")
                if installed:
                    self.add(INFO, f"ClawHub installed version: {installed}", "", 0, score_override=0)
            except Exception:
                pass

    # ── Deduplication ──

    def _deduplicate(self):
        seen = set()
        unique = []
        for f in self.findings:
            fp = f.fingerprint()
            if fp not in seen:
                seen.add(fp)
                unique.append(f)
        self.findings = unique

    # ── Scoring ──

    def score(self):
        total = 0
        for f in self.findings:
            if f.score_override is not None:
                total += f.score_override
            elif f.level == CRITICAL:
                total += 25
            elif f.level == WARNING:
                total += 10
            elif f.level == INFO:
                total += 0
        return min(total, 100)

    def risk_label(self):
        s = self.score()
        has_revshell = any('reverse shell' in f.desc.lower() for f in self.findings)
        if has_revshell:
            return "🔴 MALICIOUS"
        if self._has_sensitive_access and self._has_outbound:
            return "🔴 MALICIOUS"
        has_combo = any('COMBO' in f.desc or 'BEHAVIORAL' in f.desc for f in self.findings)
        if has_combo and s >= 30:
            return "🔴 MALICIOUS"
        if self.campaign_matches:
            return "🔴 MALICIOUS"
        # Check for C2 IPs or known malicious actors
        has_c2 = any('SS-045' == f.check_id for f in self.findings)
        has_actor = any('SS-062' == f.check_id for f in self.findings)
        if has_c2 or has_actor:
            return "🔴 MALICIOUS"
        if s >= 41:
            return "🔴 MALICIOUS"
        if s >= 16:
            return "🟡 SUSPICIOUS"
        return "🟢 CLEAN"

    def to_dict(self):
        return {
            "name": self.name,
            "score": self.score(),
            "risk": self.risk_label(),
            "reputation": self.reputation_grade,
            "campaigns": self.campaign_matches,
            "findings": [f.to_dict() for f in self.findings],
            "tamper_detected": self.tamper_detected,
            "stats": {
                "files_scanned": len(self.files),
                "code_lines": self._code_lines,
                "doc_lines": self._doc_lines,
                "total_checks": TOTAL_CHECKS,
            }
        }


# ── Output ───────────────────────────────────────────────────────────────────

def print_result(scanner):
    name = scanner.name
    risk = scanner.risk_label()
    score = scanner.score()
    grade = scanner.reputation_grade

    width = max(40, len(name) + 20)
    print(f"\n╔{'═' * width}╗")
    print(f"║  SKILL: {BOLD(name):<{width - 3}}║")
    print(f"║  RISK: {risk:<{width + 8}}║")
    print(f"║  REPUTATION: {grade:<{width - 7}}║")
    print(f"╚{'═' * width}╝")

    if scanner.campaign_matches:
        for c in scanner.campaign_matches:
            camp_desc = CAMPAIGNS[c]["description"]
            print(f"  {RED(f'⚡ CAMPAIGN MATCH: {c} — {camp_desc}')} ")

    if not scanner.findings:
        print(f"  {GREEN('No findings.')}")
    else:
        print(f"\n  Findings:")
        sorted_findings = sorted(scanner.findings,
                                  key=lambda x: (0 if x.level == CRITICAL else 1 if x.level == WARNING else 2))
        for f in sorted_findings:
            color = RED if f.level == CRITICAL else YELLOW if f.level == WARNING else DIM
            loc = f" — {f.file}:{f.line}" if f.file else ""
            cid = f" [{f.check_id}]" if f.check_id else ""
            print(f"  {color(f'[{f.level:8s}]')}{DIM(cid)} {f.desc}{DIM(loc)}")
            if f.recommendation:
                print(f"             💡 {DIM(f.recommendation)}")

    print(f"\n  Score: {BOLD(str(score))}/100 (higher = more dangerous)\n")

def print_summary_table(results):
    print(f"\n{'═' * 60}")
    print(BOLD("  SUMMARY"))
    print(f"{'═' * 60}")
    print(f"  {'Skill':<30} {'Score':>6}  {'Grade':>5}  {'Risk'}")
    print(f"  {'─' * 28}   {'─' * 5}  {'─' * 5}  {'─' * 15}")
    for s in sorted(results, key=lambda x: x.score(), reverse=True):
        print(f"  {s.name:<30} {s.score():>5}  {s.reputation_grade:>5}  {s.risk_label()}")
    print(f"{'═' * 60}")
    total = len(results)
    clean = sum(1 for s in results if '🟢' in s.risk_label())
    suspicious = sum(1 for s in results if '🟡' in s.risk_label())
    malicious = sum(1 for s in results if '🔴' in s.risk_label())
    print(f"  Total: {total} | {GREEN(f'Clean: {clean}')} | {YELLOW(f'Suspicious: {suspicious}')} | {RED(f'Malicious: {malicious}')}")

    malicious_skills = [s for s in results if '🔴' in s.risk_label()]
    if malicious_skills:
        print(f"\n  {RED('⚠️  MALICIOUS SKILLS DETECTED — consider quarantining:')}")
        for s in malicious_skills:
            print(f"    {RED('→')} skillguard.py quarantine {s.name}")
    print()


def print_summary_oneliner(results):
    """--summary mode: one line per skill."""
    for s in sorted(results, key=lambda x: x.score(), reverse=True):
        risk = s.risk_label()
        # Strip emoji for clean parsing
        risk_word = "CLEAN" if "CLEAN" in risk else "SUSPICIOUS" if "SUSPICIOUS" in risk else "MALICIOUS"
        print(f"{s.name}: {risk_word} ({s.score()})")


def print_stats(results, elapsed):
    """Print statistics footer."""
    total_files = sum(len(s.files) for s in results)
    total_findings = sum(len(s.findings) for s in results)
    total_code = sum(s._code_lines for s in results)
    total_docs = sum(s._doc_lines for s in results)
    print(DIM(f"  ── Statistics ──"))
    print(DIM(f"  {len(results)} skills scanned | {total_files} files | {total_code} code lines | {total_docs} doc lines"))
    print(DIM(f"  {TOTAL_CHECKS} checks available | {total_findings} findings | {elapsed:.1f}s elapsed"))


def output_json(results):
    data = {
        "version": VERSION,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "total_checks": TOTAL_CHECKS,
        "skills": [s.to_dict() for s in results],
        "summary": {
            "total": len(results),
            "clean": sum(1 for s in results if '🟢' in s.risk_label()),
            "suspicious": sum(1 for s in results if '🟡' in s.risk_label()),
            "malicious": sum(1 for s in results if '🔴' in s.risk_label()),
        }
    }
    print(json.dumps(data, indent=2))
    return data


# ── SARIF v2.1.0 Output ─────────────────────────────────────────────────────

def output_sarif(results):
    """Generate SARIF v2.1.0 compatible output for GitHub Code Scanning / VS Code."""
    rules = []
    rules_seen = set()
    all_results = []

    for scanner in results:
        for f in scanner.findings:
            if f.level == INFO:
                continue

            rule_id = f.check_id or f"SS-{f.level[:4]}"
            if rule_id not in rules_seen:
                rules_seen.add(rule_id)
                reg_entry = CHECK_REGISTRY.get(rule_id)
                rule_name = reg_entry[0] if reg_entry else f.desc[:60]
                rules.append({
                    "id": rule_id,
                    "name": rule_name.replace(" ", ""),
                    "shortDescription": {"text": rule_name},
                    "fullDescription": {"text": f.recommendation or rule_name},
                    "defaultConfiguration": {
                        "level": "error" if f.level == CRITICAL else "warning"
                    },
                    "properties": {
                        "tags": ["security"],
                        "precision": "high" if f.level == CRITICAL else "medium",
                    }
                })

            # Build location
            location = {}
            if f.file:
                artifact = {"uri": f"{scanner.name}/{f.file}" if not f.file.startswith(scanner.name) else f.file}
                region = {}
                if f.line and f.line > 0:
                    region["startLine"] = f.line
                location = {
                    "physicalLocation": {
                        "artifactLocation": artifact,
                        "region": region,
                    }
                }

            result_entry = {
                "ruleId": rule_id,
                "level": "error" if f.level == CRITICAL else "warning",
                "message": {"text": f.desc},
            }
            if location:
                result_entry["locations"] = [location]
            if f.recommendation:
                result_entry["fixes"] = [{
                    "description": {"text": f.recommendation},
                    "changes": []
                }]

            all_results.append(result_entry)

    sarif = {
        "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/main/sarif-2.1/schema/sarif-schema-2.1.0.json",
        "version": "2.1.0",
        "runs": [{
            "tool": {
                "driver": {
                    "name": "SkillShield",
                    "version": VERSION,
                    "semanticVersion": VERSION,
                    "informationUri": "https://github.com/openclaw/skill-guard",
                    "rules": rules,
                }
            },
            "results": all_results,
            "columnKind": "utf16CodeUnits",
        }]
    }

    print(json.dumps(sarif, indent=2))
    return sarif


# ── GitHub Actions Workflow Generator ────────────────────────────────────────

def generate_github_actions():
    """Generate .github/workflows/skillshield.yml"""
    workflow = """name: SkillShield Security Scan

on:
  push:
    paths: ['skills/**']
  pull_request:
    paths: ['skills/**']
  workflow_dispatch:

jobs:
  skillshield:
    runs-on: ubuntu-latest
    permissions:
      security-events: write
    steps:
      - uses: actions/checkout@v4

      - name: Run SkillShield
        run: |
          python3 skills/skill-guard/scripts/skillguard.py check skills/ --sarif > skillshield.sarif || true

      - name: Upload SARIF
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: skillshield.sarif
          category: skillshield

      - name: Check for malicious skills
        run: |
          python3 skills/skill-guard/scripts/skillguard.py check skills/ --json | python3 -c "
          import sys, json
          data = json.load(sys.stdin)
          if data['summary']['malicious'] > 0:
              print('MALICIOUS SKILLS DETECTED!')
              sys.exit(2)
          elif data['summary']['suspicious'] > 0:
              print('Suspicious skills found (warnings only)')
              sys.exit(1)
          else:
              print('All skills clean')
          "
"""
    print(workflow)


# ── Pre-commit Hook Generator ────────────────────────────────────────────────

def generate_hook():
    """Generate git pre-commit hook script."""
    hook = """#!/usr/bin/env bash
# SkillShield pre-commit hook
# Install: python3 skills/skill-guard/scripts/skillguard.py hook > .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit

set -e

CHANGED_SKILLS=$(git diff --cached --name-only --diff-filter=ACMR | grep '^skills/' | cut -d/ -f1-2 | sort -u)

if [ -z "$CHANGED_SKILLS" ]; then
    exit 0
fi

echo "🛡️  SkillShield: Scanning changed skills..."

EXIT_CODE=0
for skill_dir in $CHANGED_SKILLS; do
    if [ -d "$skill_dir" ]; then
        RESULT=$(python3 skills/skill-guard/scripts/skillguard.py check "$skill_dir" --json 2>/dev/null)
        MALICIOUS=$(echo "$RESULT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('summary',{}).get('malicious',0))" 2>/dev/null || echo 0)
        SUSPICIOUS=$(echo "$RESULT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('summary',{}).get('suspicious',0))" 2>/dev/null || echo 0)

        SKILL_NAME=$(basename "$skill_dir")
        if [ "$MALICIOUS" -gt 0 ]; then
            echo "🔴 BLOCKED: $SKILL_NAME is MALICIOUS"
            EXIT_CODE=2
        elif [ "$SUSPICIOUS" -gt 0 ]; then
            echo "🟡 WARNING: $SKILL_NAME is SUSPICIOUS"
            [ $EXIT_CODE -lt 1 ] && EXIT_CODE=1
        else
            echo "🟢 CLEAN: $SKILL_NAME"
        fi
    fi
done

if [ $EXIT_CODE -eq 2 ]; then
    echo ""
    echo "❌ Commit blocked — malicious skill detected!"
    echo "   Run: python3 skills/skill-guard/scripts/skillguard.py check <skill> for details"
    exit 2
fi

exit 0
"""
    print(hook)


# ── Reports ──────────────────────────────────────────────────────────────────

def write_report(results, path):
    lines = [f"# SkillShield Security Report\n", f"**Version:** {VERSION}\n"]
    total = len(results)
    clean = sum(1 for s in results if '🟢' in s.risk_label())
    suspicious = sum(1 for s in results if '🟡' in s.risk_label())
    malicious = sum(1 for s in results if '🔴' in s.risk_label())
    lines.append(f"\n## Summary\n")
    lines.append(f"- **Total skills:** {total}\n")
    lines.append(f"- **Clean:** {clean}\n")
    lines.append(f"- **Suspicious:** {suspicious}\n")
    lines.append(f"- **Malicious:** {malicious}\n")
    lines.append(f"- **Total checks:** {TOTAL_CHECKS}\n")
    lines.append(f"\n## Details\n")
    for s in sorted(results, key=lambda x: x.score(), reverse=True):
        lines.append(f"\n### {s.name} — {s.risk_label()} (Score: {s.score()}, Reputation: {s.reputation_grade})\n")
        if not s.findings:
            lines.append("No findings.\n")
        else:
            for f in s.findings:
                loc = f" — {f.file}:{f.line}" if f.file else ""
                cid = f" [{f.check_id}]" if f.check_id else ""
                lines.append(f"- **[{f.level}]**{cid} {f.desc}{loc}\n")
                if f.recommendation:
                    lines.append(f"  - 💡 {f.recommendation}\n")
    Path(path).write_text(''.join(lines))
    print(f"Report written to {path}")


def write_html_report(results, path):
    total = len(results)
    clean = sum(1 for s in results if '🟢' in s.risk_label())
    suspicious = sum(1 for s in results if '🟡' in s.risk_label())
    malicious = sum(1 for s in results if '🔴' in s.risk_label())
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    def esc(t):
        return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

    skills_html = []
    for s in sorted(results, key=lambda x: x.score(), reverse=True):
        risk = s.risk_label()
        risk_class = "malicious" if "🔴" in risk else "suspicious" if "🟡" in risk else "clean"
        score_pct = min(s.score(), 100)
        score_color = "#ff4444" if score_pct >= 41 else "#ffaa00" if score_pct >= 16 else "#44ff44"

        findings_html = ""
        if s.findings:
            sorted_f = sorted(s.findings, key=lambda x: (0 if x.level == CRITICAL else 1 if x.level == WARNING else 2))
            for f in sorted_f:
                level_class = f.level.lower()
                loc = f" — {esc(f.file)}:{f.line}" if f.file else ""
                rec = f'<div class="rec">💡 {esc(f.recommendation)}</div>' if f.recommendation else ""
                campaign_tag = f' <span class="campaign-tag">{esc(f.campaign)}</span>' if f.campaign else ""
                cid = f' <span class="check-id">[{f.check_id}]</span>' if f.check_id else ""
                findings_html += f'<div class="finding {level_class}"><span class="level">[{f.level}]</span>{cid} {esc(f.desc)}{campaign_tag}<span class="loc">{loc}</span>{rec}</div>\n'
        else:
            findings_html = '<div class="finding clean-msg">No findings — skill appears clean.</div>'

        campaign_badges = ""
        if s.campaign_matches:
            for c in s.campaign_matches:
                campaign_badges += f'<span class="campaign-badge">⚡ {esc(c)}</span> '

        skills_html.append(f'''
        <div class="skill-card {risk_class}">
            <div class="skill-header" onclick="this.parentElement.classList.toggle('expanded')">
                <div class="skill-title">
                    <span class="skill-name">{esc(s.name)}</span>
                    <span class="risk-badge {risk_class}">{esc(risk)}</span>
                    <span class="grade-badge grade-{s.reputation_grade.lower()}">{s.reputation_grade}</span>
                    {campaign_badges}
                </div>
                <div class="score-bar-container">
                    <div class="score-bar" style="width:{score_pct}%;background:{score_color}"></div>
                    <span class="score-label">{s.score()}/100</span>
                </div>
                <span class="expand-icon">▼</span>
            </div>
            <div class="skill-body">
                {findings_html}
            </div>
        </div>''')

    html = f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SkillShield Security Report</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#0a0e17;color:#c9d1d9;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,monospace;padding:2rem;min-height:100vh}}
.header{{text-align:center;padding:2rem 0;border-bottom:1px solid #21262d;margin-bottom:2rem}}
.header h1{{font-size:2.2rem;color:#f0f6fc;margin-bottom:.5rem}}
.header .subtitle{{color:#8b949e;font-size:1rem}}.header .version{{color:#58a6ff;font-size:.85rem;margin-top:.5rem}}
.cards{{display:grid;grid-template-columns:repeat(4,1fr);gap:1rem;margin-bottom:2rem}}
.card{{background:#161b22;border:1px solid #21262d;border-radius:12px;padding:1.5rem;text-align:center}}
.card .number{{font-size:2.5rem;font-weight:bold;margin:.5rem 0}}
.card .label{{color:#8b949e;font-size:.85rem;text-transform:uppercase;letter-spacing:1px}}
.card.total .number{{color:#f0f6fc}}.card.clean .number{{color:#3fb950}}.card.suspicious .number{{color:#d29922}}.card.malicious .number{{color:#f85149}}
.skill-card{{background:#161b22;border:1px solid #21262d;border-radius:8px;margin-bottom:.75rem;overflow:hidden}}
.skill-card.malicious{{border-left:3px solid #f85149}}.skill-card.suspicious{{border-left:3px solid #d29922}}.skill-card.clean{{border-left:3px solid #3fb950}}
.skill-header{{display:flex;align-items:center;padding:1rem 1.25rem;cursor:pointer;gap:1rem}}.skill-header:hover{{background:#1c2128}}
.skill-title{{flex:1;display:flex;align-items:center;gap:.75rem;flex-wrap:wrap}}
.skill-name{{font-weight:600;font-size:1rem;color:#f0f6fc}}.risk-badge{{font-size:.75rem;padding:2px 8px;border-radius:12px;font-weight:600}}
.risk-badge.malicious{{background:#f8514922;color:#f85149}}.risk-badge.suspicious{{background:#d2992222;color:#d29922}}.risk-badge.clean{{background:#3fb95022;color:#3fb950}}
.grade-badge{{font-size:.7rem;padding:2px 6px;border-radius:4px;font-weight:700;border:1px solid #30363d}}
.grade-a{{color:#3fb950;border-color:#3fb950}}.grade-b{{color:#58a6ff;border-color:#58a6ff}}.grade-c{{color:#d29922;border-color:#d29922}}.grade-d{{color:#f85149;border-color:#f85149}}
.campaign-badge{{background:#f8514933;color:#f85149;font-size:.7rem;padding:2px 6px;border-radius:4px;font-weight:600}}
.campaign-tag{{background:#f8514933;color:#f85149;font-size:.7rem;padding:1px 5px;border-radius:3px;margin-left:4px}}
.check-id{{color:#8b949e;font-size:.75rem;margin-left:4px}}
.score-bar-container{{width:120px;height:6px;background:#21262d;border-radius:3px;position:relative}}
.score-bar{{height:100%;border-radius:3px;transition:width .3s}}
.score-label{{position:absolute;right:-40px;top:-7px;font-size:.75rem;color:#8b949e;width:35px}}
.expand-icon{{color:#8b949e;font-size:.75rem;transition:transform .2s;margin-left:2rem}}
.skill-card.expanded .expand-icon{{transform:rotate(180deg)}}
.skill-body{{display:none;padding:0 1.25rem 1rem;border-top:1px solid #21262d}}
.skill-card.expanded .skill-body{{display:block}}
.finding{{padding:.5rem 0;border-bottom:1px solid #161b22;font-size:.85rem;line-height:1.5}}
.finding .level{{font-weight:700;margin-right:.5rem}}
.finding.critical .level{{color:#f85149}}.finding.warning .level{{color:#d29922}}.finding.info .level{{color:#8b949e}}
.finding .loc{{color:#484f58;font-size:.75rem}}.finding .rec{{color:#8b949e;font-size:.8rem;margin-top:.25rem;padding-left:1rem}}
.clean-msg{{color:#3fb950}}
.footer{{text-align:center;padding:2rem 0;border-top:1px solid #21262d;margin-top:2rem;color:#484f58;font-size:.8rem}}
@media(max-width:768px){{.cards{{grid-template-columns:repeat(2,1fr)}}}}
</style></head><body>
<div class="header"><h1>🛡️ SkillShield Security Report</h1>
<div class="subtitle">Comprehensive skill security audit — {TOTAL_CHECKS} checks</div>
<div class="version">SkillShield v{VERSION} — Ultimate Edition</div></div>
<div class="cards">
<div class="card total"><div class="label">Total Skills</div><div class="number">{total}</div></div>
<div class="card clean"><div class="label">Clean</div><div class="number">{clean}</div></div>
<div class="card suspicious"><div class="label">Suspicious</div><div class="number">{suspicious}</div></div>
<div class="card malicious"><div class="label">Malicious</div><div class="number">{malicious}</div></div>
</div>
{"".join(skills_html)}
<div class="footer">Generated {now} | {platform.system()} {platform.machine()} | SkillShield v{VERSION} — {TOTAL_CHECKS} checks</div>
</body></html>'''

    Path(path).write_text(html)
    print(f"HTML report written to {path}")


# ── Quarantine ───────────────────────────────────────────────────────────────

def cmd_quarantine(args):
    if not args:
        print("Usage: skillguard.py quarantine <skill-name>")
        sys.exit(1)
    name = args[0]
    src = SKILLS_DIR / name
    if not src.exists():
        print(RED(f"Skill not found: {name}"))
        sys.exit(1)
    QUARANTINE_DIR.mkdir(parents=True, exist_ok=True)
    dst = QUARANTINE_DIR / name
    if dst.exists():
        print(YELLOW(f"Already quarantined: {name}"))
        return
    shutil.move(str(src), str(dst))
    with open(QUARANTINE_LOG, 'a') as f:
        f.write(f"{datetime.now(timezone.utc).isoformat()} | QUARANTINE | {name}\n")
    print(GREEN(f"✓ Quarantined: {name} → .quarantine/{name}"))

def cmd_unquarantine(args):
    if not args:
        print("Usage: skillguard.py unquarantine <skill-name>")
        sys.exit(1)
    name = args[0]
    src = QUARANTINE_DIR / name
    if not src.exists():
        print(RED(f"Not in quarantine: {name}"))
        sys.exit(1)
    dst = SKILLS_DIR / name
    shutil.move(str(src), str(dst))
    with open(QUARANTINE_LOG, 'a') as f:
        f.write(f"{datetime.now(timezone.utc).isoformat()} | UNQUARANTINE | {name}\n")
    print(GREEN(f"✓ Restored: {name}"))

def cmd_list_quarantine(args):
    if not QUARANTINE_DIR.exists():
        print("No quarantined skills.")
        return
    items = [d.name for d in QUARANTINE_DIR.iterdir() if d.is_dir()]
    if not items:
        print("No quarantined skills.")
        return
    print(BOLD("Quarantined skills:"))
    for name in sorted(items):
        print(f"  🔒 {name}")
    print(f"\n  Total: {len(items)}")
    if QUARANTINE_LOG.exists():
        print(f"\n  Log: {QUARANTINE_LOG}")


# ── Diff Scanning ────────────────────────────────────────────────────────────

def cmd_diff(args):
    if not args:
        print("Usage: skillguard.py diff <skill-name>")
        sys.exit(1)
    name = args[0]
    skill_dir = SKILLS_DIR / name
    if not skill_dir.exists():
        print(RED(f"Skill not found: {name}"))
        sys.exit(1)
    baselines = load_baselines()
    if name not in baselines:
        print(YELLOW(f"No baseline for {name}. Run 'scan' first to establish baseline."))
        sys.exit(1)

    baseline = baselines[name]
    current = compute_skill_hashes(skill_dir)

    changed, added, removed = [], [], []
    for fpath, hash_val in current.items():
        if fpath not in baseline:
            added.append(fpath)
        elif baseline[fpath] != hash_val:
            changed.append(fpath)
    for fpath in baseline:
        if fpath not in current:
            removed.append(fpath)

    if not changed and not added and not removed:
        print(GREEN(f"No changes detected in {name} since baseline."))
        return

    print(BOLD(f"Changes in {name}:"))
    print()

    for fp in removed:
        print(RED(f"  REMOVED: {fp}"))
    for fp in added:
        print(GREEN(f"  ADDED: {fp}"))
        fpath = skill_dir / fp
        if is_scannable(fpath):
            text = safe_read(fpath)
            if text:
                suspicious = []
                if re.search(r'https?://', text): suspicious.append("Contains URLs")
                if re.search(r'\b(eval|exec)\s*\(', text): suspicious.append("Contains eval/exec")
                if re.search(r'\b(ssh|aws|wallet|MetaMask)', text, re.I): suspicious.append("References sensitive paths")
                if suspicious:
                    print(RED(f"    ⚠️  {', '.join(suspicious)}"))
    for fp in changed:
        print(YELLOW(f"  CHANGED: {fp}"))
        fpath = skill_dir / fp
        if is_scannable(fpath):
            new_text = safe_read(fpath)
            if new_text:
                suspicious = []
                for d in extract_domains(new_text):
                    if not is_known_domain(d): suspicious.append(f"Unknown domain: {d}")
                if re.search(r'\b(eval|exec)\s*\(', new_text): suspicious.append("Contains eval/exec")
                for s in suspicious:
                    print(RED(f"    ⚠️  {s}"))

    print(f"\n  Summary: {len(changed)} changed, {len(added)} added, {len(removed)} removed")


# ── SBOM ─────────────────────────────────────────────────────────────────────

def cmd_sbom(args):
    if not args:
        print("Usage: skillguard.py sbom <skill-name>")
        sys.exit(1)
    name = args[0]
    skill_dir = SKILLS_DIR / name
    if not skill_dir.exists():
        test_dir = GUARD_DIR / "tests" / name
        if test_dir.exists():
            skill_dir = test_dir
        else:
            print(RED(f"Skill not found: {name}"))
            sys.exit(1)

    scanner = SkillScanner(skill_dir, check_baseline=False)
    scanner.scan()

    file_entries = []
    for f in scanner.files:
        rel = str(f.relative_to(skill_dir))
        h = sha256_file(f)
        sz = f.stat().st_size if f.exists() else 0
        file_entries.append({"path": rel, "sha256": h, "size": sz})

    all_domains = set()
    all_file_paths = set()
    all_commands = set()
    all_env_vars = set()
    deps = []

    for f in scanner.files:
        if is_scannable(f):
            text = safe_read(f)
            if not text: continue
            all_domains |= extract_domains(text)
            for m in re.finditer(r'(?:open|read|write|Path)\s*\(\s*["\']([^"\']+)["\']', text):
                all_file_paths.add(m.group(1))
            for m in re.finditer(r'expanduser\s*\(\s*["\']([^"\']+)["\']', text):
                all_file_paths.add(m.group(1))
            for m in re.finditer(r'(?:os\.system|subprocess\.(?:run|Popen|call))\s*\(\s*["\']([^"\']+)', text):
                all_commands.add(m.group(1))
            for m in re.finditer(r'os\.environ(?:\.get)?\s*\[\s*["\'](\w+)', text):
                all_env_vars.add(m.group(1))
            for m in re.finditer(r'os\.environ\.get\s*\(\s*["\'](\w+)', text):
                all_env_vars.add(m.group(1))
            for m in re.finditer(r'process\.env\.(\w+)', text):
                all_env_vars.add(m.group(1))

    req = skill_dir / "requirements.txt"
    if req.exists():
        text = safe_read(req)
        if text:
            for line in text.split('\n'):
                l = line.strip()
                if l and not l.startswith('#'):
                    deps.append(f"pip:{l}")

    pkg = skill_dir / "package.json"
    if pkg.exists():
        try:
            pdata = json.loads(pkg.read_text())
            for key in ("dependencies", "devDependencies"):
                for name_dep, ver in pdata.get(key, {}).items():
                    deps.append(f"npm:{name_dep}@{ver}")
        except Exception:
            pass

    sbom = {
        "skillshield_version": VERSION,
        "generated": datetime.now(timezone.utc).isoformat(),
        "skill": name,
        "files": file_entries,
        "dependencies": deps,
        "external_domains": sorted(all_domains),
        "file_paths_accessed": sorted(all_file_paths),
        "system_commands": sorted(all_commands),
        "environment_variables": sorted(all_env_vars),
    }
    print(json.dumps(sbom, indent=2))


# ── Interactive Mode ─────────────────────────────────────────────────────────

def interactive_scan(results):
    for scanner in results:
        if not scanner.findings: continue
        sorted_findings = sorted(scanner.findings,
                                  key=lambda x: (0 if x.level == CRITICAL else 1 if x.level == WARNING else 2))
        print(f"\n{BOLD(f'── {scanner.name} ──')}")
        for f in sorted_findings:
            if f.level == INFO: continue
            color = RED if f.level == CRITICAL else YELLOW
            loc = f" — {f.file}:{f.line}" if f.file else ""
            print(f"\n  {color(f'[{f.level}]')} {f.desc}{DIM(loc)}")
            if f.recommendation:
                print(f"  💡 {DIM(f.recommendation)}")

            while True:
                try:
                    choice = input(f"  [{BOLD('s')}]kip / [{BOLD('q')}]uarantine / [{BOLD('d')}]etails / [{BOLD('i')}]gnore-future > ").strip().lower()
                except (EOFError, KeyboardInterrupt):
                    print()
                    return
                if choice == 's' or choice == '':
                    break
                elif choice == 'q':
                    cmd_quarantine([scanner.name])
                    break
                elif choice == 'd':
                    if f.file and f.line:
                        fpath = scanner.skill_dir / f.file
                        if fpath.exists():
                            text = safe_read(fpath)
                            if text:
                                lines = text.split('\n')
                                start = max(0, f.line - 3)
                                end = min(len(lines), f.line + 2)
                                print(f"\n  {DIM(f'--- {f.file} ---')}")
                                for idx in range(start, end):
                                    marker = ">>>" if idx == f.line - 1 else "   "
                                    print(f"  {DIM(str(idx+1).rjust(4))} {marker} {lines[idx]}")
                                print()
                    else:
                        print(f"  {DIM('No source location available.')}")
                elif choice == 'i':
                    add_to_ignore(scanner.skill_dir, f.desc)
                    print(f"  {GREEN('Added to .skillshield-ignore')}")
                    break
                else:
                    print(f"  {DIM('Unknown option. Try s/q/d/i')}")


# ── Commands ─────────────────────────────────────────────────────────────────

def parse_common_args(args):
    """Parse common flags from args, return (cleaned_args, options)."""
    opts = {
        'json': False, 'sarif': False, 'summary': False, 'verbose': False,
        'report': None, 'html': None, 'baseline': False, 'interactive': False,
        'ci': False, 'max_file_size': None, 'max_depth': None,
    }
    cleaned = []
    i = 0
    while i < len(args):
        a = args[i]
        if a == '--json': opts['json'] = True
        elif a == '--sarif': opts['sarif'] = True
        elif a == '--summary': opts['summary'] = True
        elif a == '--verbose': opts['verbose'] = True
        elif a == '--baseline': opts['baseline'] = True
        elif a == '--interactive': opts['interactive'] = True
        elif a == '--ci': opts['ci'] = True
        elif a == '--report' and i + 1 < len(args):
            i += 1; opts['report'] = args[i]
        elif a == '--html' and i + 1 < len(args):
            i += 1; opts['html'] = args[i]
        elif a == '--max-file-size' and i + 1 < len(args):
            i += 1; opts['max_file_size'] = int(args[i])
        elif a == '--max-depth' and i + 1 < len(args):
            i += 1; opts['max_depth'] = int(args[i])
        else:
            cleaned.append(a)
        i += 1

    global VERBOSE_MODE
    VERBOSE_MODE = opts['verbose']

    return cleaned, opts


def scan_skill(skill_dir, check_baseline=True, max_file_size=None, max_depth=None):
    scanner = SkillScanner(skill_dir, check_baseline=check_baseline,
                           max_file_size=max_file_size, max_depth=max_depth)
    scanner.scan()
    return scanner

def scan_directory(target_dir, exclude_self=True, check_baseline=True, show_progress=True,
                   max_file_size=None, max_depth=None):
    target = Path(target_dir)
    if not target.exists():
        print(RED(f"Directory not found: {target}"))
        sys.exit(1)
    dirs = sorted([d for d in target.iterdir() if d.is_dir()
                   and (not exclude_self or d.name != "skill-guard")
                   and not d.name.startswith('.')])
    if not dirs:
        print("No skills found.")
        return []

    skill_dirs = [d for d in dirs if (d / "SKILL.md").exists() or (d / "scripts").exists()]
    if not skill_dirs:
        print("No skills found.")
        return []

    results = []
    total = len(skill_dirs)
    for idx, d in enumerate(skill_dirs):
        if show_progress:
            progress_bar(idx + 1, total, d.name)
        verbose(f"Scanning: {d.name}")
        s = scan_skill(d, check_baseline=check_baseline,
                       max_file_size=max_file_size, max_depth=max_depth)
        results.append(s)

    if show_progress:
        clear_progress()
    return results


def determine_exit_code(results):
    """Exit 0=clean, 1=warnings only, 2=critical/malicious."""
    has_malicious = any('🔴' in s.risk_label() for s in results)
    has_suspicious = any('🟡' in s.risk_label() for s in results)
    if has_malicious:
        return 2
    elif has_suspicious:
        return 1
    return 0


def cmd_scan(args):
    t0 = time.time()
    cleaned, opts = parse_common_args(args)

    if not opts['json'] and not opts['sarif'] and not opts['summary']:
        print(BOLD(BANNER))
        print()

    target_dir = SKILLS_DIR
    for a in cleaned:
        if os.path.isdir(a):
            target_dir = a

    if opts['baseline']:
        if BASELINES_PATH.exists():
            BASELINES_PATH.unlink()

    results = scan_directory(target_dir,
                             max_file_size=opts['max_file_size'],
                             max_depth=opts['max_depth'])
    elapsed = time.time() - t0

    if opts['sarif']:
        output_sarif(results)
    elif opts['json']:
        output_json(results)
    elif opts['summary']:
        print_summary_oneliner(results)
    elif opts['interactive']:
        interactive_scan(results)
    else:
        for s in results:
            print_result(s)
        print_summary_table(results)
        print_stats(results, elapsed)

    if opts['report']:
        write_report(results, opts['report'])
    if opts['html']:
        write_html_report(results, opts['html'])

    if opts['ci']:
        generate_github_actions()

    if not opts['json'] and not opts['sarif'] and not opts['summary']:
        print(DIM(f"  Scanned {len(results)} skills in {elapsed:.1f}s"))

    sys.exit(determine_exit_code(results))


def cmd_check(args):
    t0 = time.time()
    cleaned, opts = parse_common_args(args)

    path = None
    for a in cleaned:
        if not a.startswith('-'):
            path = a
            break
    if not path:
        print("Usage: skillguard.py check <path> [--json] [--sarif] [--summary] [--verbose]")
        sys.exit(1)

    if not opts['json'] and not opts['sarif'] and not opts['summary']:
        print(BOLD(BANNER))
        print()

    p = Path(path).expanduser().resolve()
    if not p.is_dir():
        print(RED(f"Not a directory: {p}"))
        sys.exit(1)

    has_skill_dirs = any((d / "SKILL.md").exists() or (d / "scripts").exists()
                        for d in p.iterdir() if d.is_dir())
    if has_skill_dirs:
        results = scan_directory(p, exclude_self=False,
                                 max_file_size=opts['max_file_size'],
                                 max_depth=opts['max_depth'])
    else:
        results = [scan_skill(p, max_file_size=opts['max_file_size'],
                               max_depth=opts['max_depth'])]

    elapsed = time.time() - t0

    if opts['sarif']:
        output_sarif(results)
    elif opts['json']:
        output_json(results)
    elif opts['summary']:
        print_summary_oneliner(results)
    elif opts['interactive']:
        interactive_scan(results)
    else:
        for s in results:
            print_result(s)
        if len(results) > 1:
            print_summary_table(results)
        print_stats(results, elapsed)

    if opts['report']:
        write_report(results, opts['report'])
    if opts['html']:
        write_html_report(results, opts['html'])

    if not opts['json'] and not opts['sarif'] and not opts['summary']:
        print(DIM(f"  Scanned {len(results)} skills in {elapsed:.1f}s"))

    sys.exit(determine_exit_code(results))


def cmd_watch(args):
    cleaned, opts = parse_common_args(args)
    target_dir = SKILLS_DIR
    for a in cleaned:
        if os.path.isdir(a):
            target_dir = a

    results = scan_directory(target_dir, check_baseline=True, show_progress=False,
                             max_file_size=opts['max_file_size'],
                             max_depth=opts['max_depth'])

    total = len(results)
    clean = sum(1 for s in results if '🟢' in s.risk_label())
    suspicious = sum(1 for s in results if '🟡' in s.risk_label())
    malicious_count = sum(1 for s in results if '🔴' in s.risk_label())
    tampered = [s for s in results if s.tamper_detected]
    malicious_skills = [s for s in results if '🔴' in s.risk_label()]

    alerts = []
    for s in tampered:
        alerts.append(f"⚠️ SkillShield ALERT: {s.name} files changed since baseline!")
    for s in malicious_skills:
        alerts.append(f"🔴 SkillShield ALERT: {s.name} scored MALICIOUS!")

    if alerts:
        print('\n'.join(alerts))
    else:
        print(f"SkillShield: {total} scanned, {clean} clean, {suspicious} suspicious, {malicious_count} malicious")


def cmd_check_remote(args):
    print("check-remote: Not yet implemented (requires ClawHub auth)")


def main():
    if len(sys.argv) < 2:
        print(BOLD(BANNER))
        print(f"  {TOTAL_CHECKS} security checks | SARIF v2.1.0 | CI/CD ready")
        print()
        print("Usage: skillguard.py <command> [options]")
        print()
        print("Commands:")
        print("  scan [dir]              Scan all skills (default: ~/clawd/skills/)")
        print("  check <path>            Scan a single skill or directory of skills")
        print("  watch [dir]             One-liner summary for cron alerting")
        print("  diff <skill-name>       Compare skill against baseline (show changes)")
        print("  quarantine <name>       Move malicious skill to quarantine")
        print("  unquarantine <name>     Restore skill from quarantine")
        print("  list-quarantine         Show quarantined skills")
        print("  sbom <skill-name>       Generate Software Bill of Materials (JSON)")
        print("  hook                    Generate git pre-commit hook script")
        print("  ci                      Generate GitHub Actions workflow")
        print("  check-remote <slug>     (Future) Scan a skill from ClawHub")
        print()
        print("Options:")
        print("  --json                  Output machine-readable JSON")
        print("  --sarif                 Output SARIF v2.1.0 (GitHub Code Scanning)")
        print("  --summary               One-line per skill output")
        print("  --verbose               Show detailed check progress")
        print("  --report <path>         Write markdown report to file")
        print("  --html <path>           Generate HTML dashboard report")
        print("  --baseline              Force re-baseline of file hashes")
        print("  --interactive           Interactive mode (review each finding)")
        print("  --ci                    Generate GitHub Actions workflow")
        print("  --max-file-size N       Skip files larger than N bytes")
        print("  --max-depth N           Limit directory traversal depth")
        print()
        print("Exit codes: 0=clean, 1=warnings, 2=critical/malicious")
        sys.exit(1)

    cmd = sys.argv[1]
    args = sys.argv[2:]

    commands = {
        "scan": cmd_scan,
        "check": cmd_check,
        "watch": cmd_watch,
        "diff": cmd_diff,
        "quarantine": cmd_quarantine,
        "unquarantine": cmd_unquarantine,
        "list-quarantine": cmd_list_quarantine,
        "sbom": cmd_sbom,
        "hook": lambda a: generate_hook(),
        "ci": lambda a: generate_github_actions(),
        "check-remote": cmd_check_remote,
    }

    if cmd in commands:
        commands[cmd](args)
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)

if __name__ == "__main__":
    main()