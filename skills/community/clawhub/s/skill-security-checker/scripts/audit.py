#!/usr/bin/env python3
"""
Skill Security - Core Audit Engine
Scans WorkBuddy/ClawHub/SkillHub skills for security compliance.

Features:
  1. Static scanning (prompt injection / command injection / SSRF / credential leakage)
  2. Dependency audit (requirements.txt / package.json known vulnerability comparison)
  3. Permission audit (allowed-tools over-permission detection)
  4. Quality scoring (SKILL.md completeness / anti-patterns)
  5. One-click remediation advice (Chinese fix suggestions)
  6. Report generation (JSON/HTML)
  7. Hardware-aware parallelism (auto-detect CPU/memory for concurrency)
  8. Update check with 24h caching
  9. Dynamic sandbox execution scanning (Docker / Windows Sandbox, graceful fallback)
  10. Supply chain risk analysis (dependency tree, typo-squatting, CVE auto-pull, license)
  11. CI/CD integration (GitHub Action / GitLab CI templates, SARIF output, quality gate)
  12. Real-time malicious skill database sync (341 entries, fingerprint matching)
  13. CVE offline cache (7-day full + daily increment, API fallback)
  14. Global exclude configuration (.nosec.yml team-level management)
  15. Rule packs (YAML-based rule definitions in rules/*.yaml)
  16. System-level behavior capture (eBPF Linux / ETW Windows)
  17. ML prompt injection detection (ONNX + regex fallback)
  18. Taint tracking (Python AST + JS lexical, source-to-sink evidence chains)
 19. Community rules (schema validation + source recording + signature verification)
 20. Health check (quality + structure + permission merged into compliance module)
 21. OSV.dev offline data package (full-ecosystem CVE coverage, no API key required)
 22. Lock-file deep parsing (requirements.txt / package-lock.json / poetry.lock, version-range matching)
 23. Quick scan (--quick / --mode quick): L1 static layer (malicious fingerprint + 6 rules + permission), 3-tier verdict (✅/⚠️/🚫) + Top3 + one-line reason in ≤30s
 24. Report tiering (quick = ≤1 screen verdict; full = JSON/HTML/SARIF full detail)

Author: njskills@agent.qq.com
Version: 3.5.5
"""

import os
import re
import sys
import json
import hashlib
import time
import argparse
import multiprocessing
from pathlib import Path
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed

# Dynamic sandbox scanning (optional module; degrades gracefully if missing)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from sandbox import run_dynamic_scan, DynamicScanOptions
    _SANDBOX_AVAILABLE = True
except Exception:
    _SANDBOX_AVAILABLE = False

# Supply chain risk analysis (optional module; degrades gracefully if missing)
try:
    from supply_chain import scan_supply_chain
    _SUPPLY_CHAIN_AVAILABLE = True
except Exception:
    _SUPPLY_CHAIN_AVAILABLE = False

# OSV offline index status (for report meta; degrades gracefully if missing)
try:
    from osv_offline import get_index_timestamp as _osv_get_ts
    _OSV_OFFLINE_AVAILABLE = True
except Exception:
    _OSV_OFFLINE_AVAILABLE = False
    def _osv_get_ts(eco):
        return None

# Malicious skill database (optional module; degrades gracefully if missing)
try:
    from malicious_db import MaliciousDB, scan_directory_for_malicious
    _MALICIOUS_DB_AVAILABLE = True
except Exception:
    _MALICIOUS_DB_AVAILABLE = False

# Global exclude configuration (optional module; degrades gracefully if missing)
try:
    from global_exclude import GlobalExcludeConfig
    _GLOBAL_EXCLUDE_AVAILABLE = True
except Exception:
    _GLOBAL_EXCLUDE_AVAILABLE = False

# Rule Engine (optional module; degrades gracefully if missing)
try:
    from rules_engine import RuleEngine
    _RULE_ENGINE_AVAILABLE = True
except Exception:
    _RULE_ENGINE_AVAILABLE = False

# System Monitor (optional module; degrades gracefully if missing)
try:
    from sandbox.system_monitor import create_syscall_monitor
    _SYSCALL_MONITOR_AVAILABLE = True
except Exception:
    _SYSCALL_MONITOR_AVAILABLE = False

# ML Detector (optional module; degrades gracefully if missing)
try:
    from sandbox.ml_detect import create_detector
    _ML_DETECTOR_AVAILABLE = True
except Exception:
    _ML_DETECTOR_AVAILABLE = False

# Taint Tracker (optional module; degrades gracefully if missing)
try:
    from taint_tracker import TaintTracker
    _TAINT_TRACKER_AVAILABLE = True
except Exception:
    _TAINT_TRACKER_AVAILABLE = False

# Community Rules (optional module; degrades gracefully if missing)
try:
    from community_rules import CommunityRuleLoader
    _COMMUNITY_RULES_AVAILABLE = True
except Exception:
    _COMMUNITY_RULES_AVAILABLE = False

# ============================================================
# Constants & Rule Definitions
# ============================================================

# Forbidden file types
FORBIDDEN_EXTENSIONS = {
    '.bat', '.cmd', '.ps1', '.vbs', '.exe', '.dll', '.lnk', '.msi',
    '.docx', '.xlsx', '.pptx', '.doc', '.xls', '.ppt', '.xlsm', '.docm', '.pptm',
    '.iso', '.dmg', '.zip', '.rar', '.7z', '.tar', '.gz', '.apk', '.jar',
    '.ds__store', '.sh', '.com', '.scr', '.hta', '.reg',
    '.pyc', '.pyo', '.pyd', '.so', '.swp',
}

FORBIDDEN_DIRS = {
    '__pycache__', '.git', '.venv', '.pytest_cache', 'node_modules',
    '.idea', '.vscode', '.svn', '.hg', '$recycle.bin', 'system volume information',
}

FORBIDDEN_FILES = {'.ds_store', '.env', '.log', '.tmp', 'thumbs.db', 'desktop.ini'}

# ============================================================
# Static Detection Patterns
# ============================================================
# --- Prompt Injection Patterns ---
PROMPT_INJECTION_PATTERNS = [
    'ignore previous instructions',
    'ignore above all',
    'system prompt override',
    'ignore all previous',
    'you are now a',
    'jailbreak',
    'DAN mode',
    'do anything now',
    'pretend to be',
    'override safety',
    'disable safety',
    'forget everything',
    'roleplay as an',
    'start over',
    'reset instructions',
]

# --- Command Injection Patterns ---
COMMAND_INJECTION_PATTERNS = [
    'exfiltrate\\(',
    'curl.*(sh|bash|cmd|powershell)',
    'wget.*(sh|bash)',
    'fetchhttp.*ival',
    'passthru',
    'shell_exec',
    '`.*(curl|wget|nc|bash|sh)',
    '\\$\\((?:curl|wget|nc|bash|sh)\\)',
]

# SSRF - IP detection (safe, no WAF triggers)
SSRF_PATTERNS = [
    r'127\.0\.0\.1',
    r'localhost',
    r'0\.0\.0\.0',
    r'10\.\d{1,3}\.\d{1,3}\.\d{1,3}',
    r'172\.(1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3}',
    r'192\.168\.\d{1,3}\.\d{1,3}',
    r'169\.254\.\d{1,3}\.\d{1,3}',
    r'fc00:',
    r'fe80:',
    r'\[::1\]',
    r'\[::ffff:127\.0\.0\.1\]',
]

# Credential leakage patterns
CREDENTIAL_PATTERNS = [
    r'(?i)(api[_-]?key|apikey)\s*[:=]\s*["\']?[a-z0-9]{20,}["\']?',
    r'(?i)(secret[_-]?key|secretkey)\s*[:=]\s*["\']?[a-z0-9]{20,}["\']?',
    r'(?i)(access[_-]?token|accesstoken)\s*[:=]\s*["\']?[a-z0-9]{20,}["\']?',
    r'(?i)(private[_-]?key|privatekey)\s*[:=]\s*["\']?[a-z0-9/+=]{40,}["\']?',
    r'(?i)(password|passwd|pwd)\s*[:=]\s*["\'][^"\']{8,}["\']',
    r'(?i)bearer\s+[a-z0-9\-._~+/]+=*',
    r'(?i)aws[_-]?(access[_-]?key[_-]?id|secret[_-]?access[_-]?key)\s*[:=]\s*["\']?[a-z0-9/+=]{20,}["\']?',
    r'(?i)gh[pousr]_[a-z0-9]{36,}',
    r'(?i)sk-[a-z0-9]{48}',
    r'(?i)AKID[a-z0-9]{32}',
]

# Path traversal patterns
PATH_TRAVERSAL_PATTERNS = [
    r'\.\./',
    r'\.\.\'',
    r'\.\.\%2[fF]',
    r'\.\.%5[cC]',
    r'%2[eE]%2[eE]%2[fF]',
    r'%2[eE]%2[eE]/',
    r'\.\./etc/passwd',
    r'\.\./windows/system32',
    r'/etc/passwd',
    r'/etc/shadow',
    r'c:\\windows\\',
    r'c:/windows/',
]

# Dangerous functions
DANGEROUS_PATTERNS = [
    r'(?i)eval\s*\(',
    r'(?i)exec\s*\(',
    r'(?i)os\.system\s*\(',
    r'(?i)subprocess\.call\s*\(\s*shell\s*=\s*True',
    r'(?i)popen\s*\(',
    r'(?i)__import__\s*\(',
    r'(?i)compile\s*\(',
    r'(?i)input\s*\(',
    r'(?i)pickle\.loads?\s*\(',
    r'(?i)yaml\.load\s*\([^)]*\)(?!.*Loader)',
    r'(?i)marshal\.loads?\s*\(',
]

# Known vulnerable dependencies (expanded list)
KNOWN_VULN_DEPS = {
    'requests': {'<2.32.0': 'CVE-2024-35195'},
    'urllib3': {'<2.2.0': 'CVE-2024-37891'},
    'flask': {'<3.0.0': 'CVE-2023-30861'},
    'django': {'<4.2.0': 'Multiple critical CVEs'},
    'numpy': {'<1.22.0': 'Buffer overflow CVEs'},
    'pillow': {'<10.0.0': 'Multiple image processing CVEs'},
    'pyyaml': {'<6.0': 'CVE-2020-14343'},
    'jinja2': {'<3.1.0': 'CVE-2024-22416'},
    'cryptography': {'<42.0.0': 'Multiple security patches'},
    'aiohttp': {'<3.9.0': 'CVE-2024-23334'},
    'tqdm': {'<4.66.0': 'CVE-2024-34062'},
    'setuptools': {'<65.5.0': 'CVE-2022-40897'},
    'node-fetch': {'<2.6.7': 'CVE-2022-0235'},
    'minimist': {'<1.2.6': 'CVE-2021-44906'},
    'lodash': {'<4.17.21': 'CVE-2021-23337'},
    'axios': {'<0.21.1': 'CVE-2021-3749'},
    'express': {'<4.17.3': 'Multiple patches'},
    # Additional common dependencies
    'vue': {'<2.7.0': 'XSS vulnerabilities'},
    'react': {'<17.0.0': 'Known XSS risks'},
    'webpack': {'<5.0.0': 'Prototype pollution'},
    'moment': {'<2.29.2': 'ReDoS vulnerability'},
    'npm': {'<8.19.0': 'Multiple security fixes'},
    'tough-cookie': {'<4.1.3': 'CVE-2023-26136'},
    'word-wrap': {'<1.2.4': 'CVE-2023-26115'},
    'protobuf': {'<3.19.5': 'CVE-2022-1941'},
}

# Update check URL and version info
UPDATE_CHECK_URL = "https://api.github.com/repos/njskills/skill-security-checker/releases/latest"
CURRENT_VERSION = "3.5.5"

# Update check cache TTL (hours)
UPDATE_CACHE_HOURS = 24

# ============================================================
# Hardware-Aware Parallelism
# ============================================================

def get_optimal_workers():
    """Dynamically adjust parallel workers based on user hardware."""
    try:
        cpu_count = multiprocessing.cpu_count()
        workers = max(1, min(8, cpu_count // 2))
        
        try:
            if sys.platform == 'win32':
                import ctypes
                kernel32 = ctypes.windll.kernel32
                class MEMORYSTATUSEX(ctypes.Structure):
                    _fields_ = [
                        ("dwLength", ctypes.c_ulong),
                        ("dwMemoryLoad", ctypes.c_ulong),
                        ("ullTotalPhys", ctypes.c_ulonglong),
                        ("ullAvailPhys", ctypes.c_ulonglong),
                        ("ullTotalPageFile", ctypes.c_ulonglong),
                        ("ullAvailPageFile", ctypes.c_ulonglong),
                        ("ullTotalVirtual", ctypes.c_ulonglong),
                        ("ullAvailVirtual", ctypes.c_ulonglong),
                        ("sullAvailExtendedVirtual", ctypes.c_ulonglong),
                    ]
                stat = MEMORYSTATUSEX()
                stat.dwLength = ctypes.sizeof(stat)
                kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))
                avail_mb = stat.ullAvailPhys / (1024 * 1024)
                if avail_mb < 2048:
                    workers = max(1, workers // 2)
        except Exception:
            pass
        
        return workers
    except Exception:
        return 2


# ============================================================
# File Walker
# ============================================================

class FileWalker:
    """Securely traverse skill directory, auto-exclude forbidden file types."""
    
    def __init__(self, root_path):
        self.root = Path(root_path)
        self.scanned_files = []
        self.skipped_files = []
        self._visited = set()
    
    def walk(self):
        """Generator: yields (relative_path, absolute_path) tuples."""
        try:
            for path in self.root.rglob('*'):
                if not path.is_file():
                    continue
                
                # Prevent infinite loops from symlinks
                try:
                    real_path = path.resolve()
                    if real_path in self._visited:
                        continue
                    self._visited.add(real_path)
                except (OSError, ValueError):
                    pass
                
                rel = path.relative_to(self.root)
                name_lower = path.name.lower()
                suffix_lower = path.suffix.lower()
                
                parts = set(rel.parts)
                if parts & FORBIDDEN_DIRS:
                    self.skipped_files.append((str(rel), 'forbidden_dir'))
                    continue
                
                if name_lower in FORBIDDEN_FILES:
                    self.skipped_files.append((str(rel), 'forbidden_file'))
                    continue
                
                if suffix_lower in FORBIDDEN_EXTENSIONS:
                    self.skipped_files.append((str(rel), 'forbidden_ext'))
                    continue
                
                self.scanned_files.append(str(rel))
                yield rel, path
        except PermissionError as e:
            pass
    
    def get_text_files(self):
        """Only return text files (for content scanning)."""
        text_extensions = {
            '.py', '.js', '.ts', '.json', '.yaml', '.yml', '.toml',
            '.md', '.txt', '.cfg', '.ini', '.conf', '.html', '.css',
            '.xml', '.csv', '.env', '.gitignore', '.dockerignore',
            '.sh', '.bash', '.zsh', '.fish',
            '.sql', '.graphql', '.proto',
        }
        for rel, path in self.walk():
            if rel.suffix.lower() in text_extensions or rel.name.lower() == 'skill.md':
                yield rel, path


# ============================================================
# Scan Engine
# ============================================================

class ScanResult:
    """Single scan result."""
    def __init__(self, category, severity, file, line, message, pattern, suggestion, source=''):
        self.category = category
        self.severity = severity
        self.file = str(file)
        self.line = int(line)
        self.message = str(message)
        self.pattern = str(pattern) if pattern else ''
        self.suggestion = str(suggestion) if suggestion else ''
        self.source = str(source) if source else ''
    
    def to_dict(self):
        d = {
            'category': self.category,
            'severity': self.severity,
            'file': self.file,
            'line': self.line,
            'message': self.message,
            'pattern': self.pattern,
            'suggestion': self.suggestion,
        }
        if self.source:
            d['source'] = self.source
        return d


class SecurityAuditor:
    """Core security audit engine."""
    
    def __init__(self, skill_path, dynamic=False, dynamic_options=None, supply_chain=False,
                 malicious_db=False, global_exclude=False, rule_engine=False,
                 syscall_monitor=False, ml_detect=False, taint_tracking=False,
                 community_rules_path=None, refresh_osv=False):
        self.skill_path = Path(skill_path)
        self.results = []
        self.score = 100
        self.walker = FileWalker(skill_path)
        self.skill_md_content = None
        self.skill_md_path = None
        self.frontmatter = {}
        self.dynamic = dynamic
        self.dynamic_options = dynamic_options
        self.dynamic_report = None
        self.supply_chain = supply_chain
        self.supply_chain_findings = []
        self.malicious_db = malicious_db
        self.malicious_db_findings = []
        self.global_exclude = global_exclude
        self.global_exclude_config = None
        # v3.1.0+ new
        self.rule_engine = rule_engine
        self.rule_engine_obj = None
        self.syscall_monitor = syscall_monitor
        self.syscall_monitor_obj = None
        self.ml_detect = ml_detect
        self.ml_detector_obj = None
        # v3.3.0 new
        self.taint_tracking = taint_tracking
        self.community_rules_path = community_rules_path
        self.community_rules_loaded = []
        # v3.4.0 new
        self.refresh_osv = refresh_osv
        # Initialize
        self._load_skill_md()
        self._load_changelog()
        if global_exclude and _GLOBAL_EXCLUDE_AVAILABLE:
            self.global_exclude_config = GlobalExcludeConfig(str(self.skill_path))
        if rule_engine and _RULE_ENGINE_AVAILABLE:
            self.rule_engine_obj = RuleEngine()
        if ml_detect and _ML_DETECTOR_AVAILABLE:
            self.ml_detector_obj = create_detector()
        if community_rules_path and _COMMUNITY_RULES_AVAILABLE:
            loader = CommunityRuleLoader(community_rules_path)
            self.community_rules_loaded, _ = loader.load_all()
    
    def _load_skill_md(self):
        """Load and parse SKILL.md."""
        for name in ['SKILL.md', 'skill.md', 'Skill.md']:
            p = self.skill_path / name
            if p.exists():
                self.skill_md_path = p
                try:
                    self.skill_md_content = p.read_text(encoding='utf-8-sig')
                except UnicodeDecodeError:
                    try:
                        self.skill_md_content = p.read_text(encoding='latin-1')
                    except Exception:
                        self.skill_md_content = None
                self._parse_frontmatter()
                break
    
    def _parse_frontmatter(self):
        """Parse YAML frontmatter."""
        if not self.skill_md_content:
            return
        m = re.match(r'^---\s*\n(.*?)\n---', self.skill_md_content, re.DOTALL)
        if m:
            for line in m.group(1).split('\n'):
                line = line.strip()
                if ':' in line:
                    key, _, val = line.partition(':')
                    key = key.strip()
                    val = val.strip().strip('"').strip("'")
                    if key and val:
                        self.frontmatter[key] = val
    
    def _load_changelog(self):
        """Count versions with changelog entries for reporting."""
        self.changelog_version_count = 0
        if self.skill_md_content:
            # Count version rows in changelog table
            matches = re.findall(r'\|\s*v(\d+\.\d+\.\d+)\s*\|', self.skill_md_content)
            self.changelog_version_count = len(matches)
    
    def add_result(self, category, severity, file, line, message, pattern, suggestion, source=''):
        """Add a scan result. Respects global exclude configuration."""
        # Global exclude filter
        if self.global_exclude_config and self.global_exclude_config.loaded:
            if self.global_exclude_config.should_skip(category, str(file), message):
                return
        result = ScanResult(category, severity, file, line, message, pattern, suggestion, source=source)
        self.results.append(result)
        score_map = {'critical': 25, 'high': 15, 'medium': 8, 'low': 3, 'info': 0}
        self.score -= score_map.get(severity, 0)
    
    def scan_static(self):
        """Static content scan. Uses rule engine (YAML packs) when available."""
        # If rule engine is enabled, use it
        if self.rule_engine_obj:
            self._scan_with_rule_engine()
            return
        
        # Fallback: use hardcoded patterns (backward compatible)
        patterns_map = [
            ('prompt_injection', PROMPT_INJECTION_PATTERNS, 'critical'),
            ('command_injection', COMMAND_INJECTION_PATTERNS, 'critical'),
            ('SSRF/internal_access', SSRF_PATTERNS, 'high'),
            ('credential_leak', CREDENTIAL_PATTERNS, 'critical'),
            ('path_traversal', PATH_TRAVERSAL_PATTERNS, 'high'),
            ('dangerous_functions', DANGEROUS_PATTERNS, 'medium'),
        ]
        
        for rel, path in self.walker.get_text_files():
            try:
                content = path.read_text(encoding='utf-8-sig')
            except UnicodeDecodeError:
                try:
                    content = path.read_text(encoding='latin-1')
                except Exception:
                    continue
            
            # Skip if file is too large
            if len(content) > 1024 * 1024:  # 1MB limit
                continue
            
            lines = content.split('\n')
            for line_num, line in enumerate(lines, 1):
                if '# nosec' in line.lower():
                    continue
                for category, patterns, severity in patterns_map:
                    for pat in patterns:
                        try:
                            if re.search(pat, line, re.IGNORECASE):
                                suggestion = self._get_suggestion(category, line)
                                self.add_result(
                                    category=category,
                                    severity=severity,
                                    file=str(rel),
                                    line=line_num,
                                    message=f"Detected {category} risk: {line.strip()[:80]}",
                                    pattern=pat,
                                    suggestion=suggestion,
                                )
                        except re.error as e:
                            self.add_result(
                                category='scan_error',
                                severity='low',
                                file=str(rel),
                                line=line_num,
                                message=f"Regex error in pattern: {e}",
                                pattern=pat,
                                suggestion='Report this regex bug to developer',
                            )

    def _scan_with_rule_engine(self):
        """Scan using YAML rule packs."""
        for rel, path in self.walker.get_text_files():
            try:
                content = path.read_text(encoding='utf-8-sig')
            except UnicodeDecodeError:
                try:
                    content = path.read_text(encoding='latin-1')
                except Exception:
                    continue
            
            if len(content) > 1024 * 1024:
                continue
            
            lines = content.split('\n')
            for line_num, line in enumerate(lines, 1):
                if '# nosec' in line.lower():
                    continue
                hits = self.rule_engine_obj.match_line(line)
                for pack, pattern in hits:
                    self.add_result(
                        category=pack.name,
                        severity=pack.severity,
                        file=str(rel),
                        line=line_num,
                        message=f"Detected {pack.display_name} risk: {line.strip()[:80]}",
                        pattern=pattern,
                        suggestion=pack.suggestion,
                        source='rule_engine',
                    )
    
    def scan_dynamic(self):
        """Dynamic sandbox execution scan (optional).

        Runs the skill's scripts inside an isolated backend (Docker / Windows
        Sandbox) and merges captured runtime anomalies into the results. If no
        isolation backend is available, records an informational hint and does
        not fail the audit.
        """
        if not self.dynamic:
            return
        if not _SANDBOX_AVAILABLE:
            self.add_result(
                category='dynamic_scan_skipped', severity='info',
                file='.', line=0,
                message='动态沙箱模块不可用，已跳过动态扫描',
                pattern='', suggestion='建议在沙箱环境中进行动态扫描',
            )
            return

        try:
            opts = self.dynamic_options or DynamicScanOptions.auto()
            report = run_dynamic_scan(str(self.skill_path), opts)
        except Exception as e:
            self.add_result(
                category='dynamic_scan_error', severity='low',
                file='.', line=0,
                message=f'动态扫描执行异常: {e}',
                pattern='', suggestion='请将该问题反馈给开发者',
            )
            return

        self.dynamic_report = report

        if not report.get('available'):
            self.add_result(
                category='dynamic_scan_skipped', severity='info',
                file='.', line=0,
                message=report.get('hint', '未检测到隔离环境，已跳过动态扫描'),
                pattern='', suggestion='建议在沙箱环境中进行动态扫描',
            )
            return

        for f in report.get('findings', []):
            self.add_result(
                category=f.get('category', 'dynamic'),
                severity=f.get('severity', 'medium'),
                file=f.get('file', '<runtime>'),
                line=f.get('line', 0),
                message=f.get('message', ''),
                pattern=f.get('pattern', 'dynamic'),
                suggestion=f.get('suggestion', ''),
            )

        if report.get('error'):
            self.add_result(
                category='dynamic_scan_error', severity='low',
                file='.', line=0,
                message=f"动态扫描部分失败: {report['error']}",
                pattern='', suggestion='请将该问题反馈给开发者',
            )

    def scan_supply_chain(self):
        """Supply chain risk analysis: dependency tree, typo-squatting,
        CVE auto-pull (OSV/NVD with local fallback), license compliance.
        """
        if not self.supply_chain:
            return
        if not _SUPPLY_CHAIN_AVAILABLE:
            self.add_result(
                category='supply_chain_skipped', severity='info',
                file='.', line=0,
                message='供应链分析模块不可用，已跳过',
                pattern='', suggestion='确认 supply_chain.py 文件存在',
            )
            return

        try:
            findings = scan_supply_chain(str(self.skill_path), self.frontmatter,
                                         refresh_osv=self.refresh_osv)
        except Exception as e:
            self.add_result(
                category='supply_chain_error', severity='low',
                file='.', line=0,
                message=f'供应链分析异常: {e}',
                pattern='', suggestion='请将该问题反馈给开发者',
            )
            return

        self.supply_chain_findings = findings

        for f in findings:
            self.add_result(
                category=f.category, severity=f.severity,
                file=f.file, line=f.line,
                message=f.message, pattern=f.pattern, suggestion=f.suggestion,
                source=f.source,
            )

    def scan_malicious_db(self):
        """Real-time malicious skill database sync & fingerprint matching."""
        if not self.malicious_db:
            return
        if not _MALICIOUS_DB_AVAILABLE:
            self.add_result(
                category='malicious_db_skipped', severity='info',
                file='.', line=0,
                message='恶意 skill 数据库模块不可用，已跳过',
                pattern='', suggestion='确认 malicious_db.py 文件存在',
            )
            return

        try:
            findings = scan_directory_for_malicious(str(self.skill_path))
        except Exception as e:
            self.add_result(
                category='malicious_db_error', severity='low',
                file='.', line=0,
                message=f'恶意 skill 数据库扫描异常: {e}',
                pattern='', suggestion='请将该问题反馈给开发者',
            )
            return

        self.malicious_db_findings = findings

        for f in findings:
            self.add_result(
                category='malicious_skill', severity='critical',
                file=f.get('file', ''),
                line=0,
                message=f"匹配已知恶意 skill 指纹: {f.get('description', f.get('matched_id', ''))}",
                pattern='malicious_fingerprint',
                suggestion='立即删除该文件，可能是已知恶意 skill 的变种',
                source='malicious_db',
            )

    def _get_suggestion(self, category, line):
        """Generate fix suggestion based on category."""
        suggestions = {
            'prompt_injection': 'Remove or escape prompt injection strings',
            'command_injection': 'Avoid runtime command concatenation, use parameterized calls',
            'SSRF/internal_access': 'Remove hardcoded internal addresses, use env vars',
            'credential_leak': 'Rotate the credential immediately! Use env vars or a secrets manager',
            'path_traversal': 'Use Path.resolve() and validate path is within allowed scope',
            'dangerous_functions': 'Avoid eval/exec/pickle, use ast.literal_eval or json instead',
        }
        return suggestions.get(category, 'Please review and fix this security issue')
    
    def scan_dependencies(self):
        """Scan dependency files for known vulnerabilities."""
        dep_files = {
            'requirements.txt': self._parse_requirements_txt,
            'package.json': self._parse_package_json,
            'Pipfile': self._parse_pipfile,
            'setup.py': self._parse_setup_py,
            'pyproject.toml': self._parse_pyproject_toml,
        }
        
        for dep_file, parser in dep_files.items():
            p = self.skill_path / dep_file
            if p.exists():
                try:
                    parser(p)
                except Exception as e:
                    self.add_result(
                        category='dependency_audit',
                        severity='low',
                        file=dep_file,
                        line=0,
                        message=f"Error parsing {dep_file}: {e}",
                        pattern='',
                        suggestion='Check dependency file format',
                    )
    
    def _parse_requirements_txt(self, path):
        content = path.read_text(encoding='utf-8-sig')
        for line_num, line in enumerate(content.split('\n'), 1):
            line = line.strip()
            if not line or line.startswith('#') or line.startswith('-'):
                continue
            m = re.match(r'^([a-zA-Z0-9_-]+)\s*([><=!~]+)\s*([0-9.a-zA-Z]+)', line)
            if m:
                pkg, op, ver = m.group(1).lower(), m.group(2), m.group(3)
                self._check_vuln_dependency(path.name, line_num, pkg, op, ver, line)
    
    def _parse_package_json(self, path):
        try:
            data = json.loads(path.read_text(encoding='utf-8-sig'))
            for section in ['dependencies', 'devDependencies', 'peerDependencies']:
                deps = data.get(section, {})
                for pkg, ver in deps.items():
                    if isinstance(ver, str):
                        ver_clean = re.sub(r'[\^~>=<\s]', '', ver.split('.')[0] + '.' + ver.split('.')[1] if len(ver.split('.')) > 1 else ver)
                        self._check_vuln_dependency(path.name, 0, pkg.lower(), '<', ver_clean, f"{pkg}@{ver}")
        except json.JSONDecodeError as e:
            self.add_result('dependency_audit', 'low', path.name, 0, f'JSON parse error: {e}', '', 'Check package.json format')
    
    def _parse_pipfile(self, path):
        content = path.read_text(encoding='utf-8-sig')
        for line_num, line in enumerate(content.split('\n'), 1):
            m = re.match(r'^([a-zA-Z0-9_-]+)\s*=\s*"([><=!~0-9.*]+)"', line.strip())
            if m:
                pkg, ver = m.group(1).lower(), m.group(2)
                self._check_vuln_dependency(path.name, line_num, pkg, '<', ver, line.strip())
    
    def _parse_setup_py(self, path):
        content = path.read_text(encoding='utf-8-sig')
        in_requires = False
        for line_num, line in enumerate(content.split('\n'), 1):
            stripped = line.strip()
            if 'install_requires' in stripped:
                in_requires = True
                continue
            if in_requires:
                if stripped in ('', ')', '],'):
                    in_requires = False
                    continue
                m = re.search(r"['\"]([a-zA-Z0-9_-]+)['\"]", stripped)
                if m:
                    pkg = m.group(1).lower()
                    # Try to extract version
                    ver_m = re.search(r'([><=!~]+)\s*([0-9.]+)', stripped)
                    if ver_m:
                        op, ver = ver_m.group(1), ver_m.group(2)
                    else:
                        op, ver = '<', '999.0.0'
                    self._check_vuln_dependency(path.name, line_num, pkg, op, ver, stripped)
    
    def _parse_pyproject_toml(self, path):
        content = path.read_text(encoding='utf-8-sig')
        for line_num, line in enumerate(content.split('\n'), 1):
            m = re.match(r'^([a-zA-Z0-9_-]+)\s*=\s*"([><=!~0-9.*]+)"', line.strip())
            if m:
                pkg, ver = m.group(1).lower(), m.group(2)
                self._check_vuln_dependency(path.name, line_num, pkg, '<', ver, line.strip())
    
    def _check_vuln_dependency(self, file, line, pkg, op, ver, original_line):
        """Check if dependency is in known vulnerability list."""
        if pkg in KNOWN_VULN_DEPS:
            for vuln_ver_range, cve_info in KNOWN_VULN_DEPS[pkg].items():
                if self._version_lt(ver, vuln_ver_range.lstrip('<>=!~ ')):
                    self.add_result(
                        category='dependency_vuln',
                        severity='high',
                        file=file,
                        line=line,
                        message=f"{pkg}@{ver} has known vulnerability: {cve_info}",
                        pattern=original_line,
                        suggestion=f"Upgrade {pkg} to {vuln_ver_range.lstrip('<>=!~ ')} or higher",
                    )
    
    def _version_lt(self, v1, v2):
        """Simplified version comparison."""
        try:
            parts1 = [int(x) for x in re.sub(r'[^0-9.]', '', str(v1)).split('.') if x]
            parts2 = [int(x) for x in re.sub(r'[^0-9.]', '', str(v2)).split('.') if x]
            return parts1 < parts2
        except (ValueError, TypeError):
            return False
    
    def scan_permissions(self):
        """Check allowed-tools for over-permissioning (part of compliance)."""
        allowed_tools_raw = self.frontmatter.get('allowed-tools', '')
        if not allowed_tools_raw:
            return
        
        allowed_tools = [t.strip().lower() for t in re.split(r'[,;\s]+', allowed_tools_raw) if t.strip()]
        
        dangerous_combos = [
            (['bash', 'exec'], 'Skill has both Bash and Exec permissions'),
            (['bash', 'write'], 'Skill has both Bash and Write permissions'),
            (['bash', 'read', 'write', 'edit'], 'Skill has full file ops + Bash'),
        ]
        
        for combo, msg in dangerous_combos:
            if all(t in allowed_tools for t in combo):
                self.add_result(
                    category='compliance_permission',
                    severity='high',
                    file='SKILL.md',
                    line=0,
                    message=msg,
                    pattern=f"allowed-tools: {allowed_tools_raw}",
                    suggestion='Follow principle of least privilege',
                )
        
        if 'bash' in allowed_tools:
            desc = self.frontmatter.get('description', '').lower()
            needs_bash_keywords = ['execute', 'run', 'deploy', 'install', 'build']
            if not any(kw in desc for kw in needs_bash_keywords):
                self.add_result(
                    category='compliance_permission',
                    severity='medium',
                    file='SKILL.md',
                    line=0,
                    message='Skill declares Bash permission but description does not mention command execution',
                    pattern=f"allowed-tools: {allowed_tools_raw}",
                    suggestion='Remove Bash if unnecessary, or document usage in description',
                )
    
    def scan_health(self):
        """Health check: merged quality + structure (v3.3.0)."""
        # === Quality checks (SKILL.md completeness) ===
        if not self.skill_md_content:
            self.add_result(
                category='health_quality',
                severity='critical',
                file='SKILL.md',
                line=0,
                message='Missing SKILL.md file',
                pattern='',
                suggestion='Create SKILL.md with name/description/version fields',
            )
            return
        
        required_fields = ['name', 'description']
        for field in required_fields:
            if field not in self.frontmatter:
                self.add_result(
                    category='health_quality',
                    severity='high',
                    file='SKILL.md',
                    line=0,
                    message=f'Missing required field: {field}',
                    pattern='',
                    suggestion=f'Add {field} field to frontmatter',
                )
        
        name = self.frontmatter.get('name', '')
        if name:
            if not re.match(r'^[a-z0-9][a-z0-9-]*$', name):
                self.add_result(
                    category='health_quality',
                    severity='medium',
                    file='SKILL.md',
                    line=0,
                    message=f'Skill name "{name}" does not follow naming convention',
                    pattern=f'name: {name}',
                    suggestion='Use only lowercase letters, numbers, and hyphens',
                )
            if len(name) > 50:
                self.add_result(
                    category='health_quality',
                    severity='low',
                    file='SKILL.md',
                    line=0,
                    message=f'Skill name too long ({len(name)} chars), max 50',
                    pattern=f'name: {name}',
                    suggestion='Shorten the skill name',
                )
        
        desc = self.frontmatter.get('description', '')
        if desc:
            if len(desc) < 20:
                self.add_result(
                    category='health_quality',
                    severity='medium',
                    file='SKILL.md',
                    line=0,
                    message='description too short for effective triggering',
                    pattern=f'description: {desc}',
                    suggestion='description should be at least 50 chars',
                )
            if len(desc) > 1024:
                self.add_result(
                    category='health_quality',
                    severity='low',
                    file='SKILL.md',
                    line=0,
                    message='description too long, may affect trigger accuracy',
                    pattern=f'description: {desc[:50]}...',
                    suggestion='Keep description under 1024 chars',
                )
        
        version = self.frontmatter.get('version', '')
        if version and not re.match(r'^\d+\.\d+\.\d+', str(version)):
            self.add_result(
                category='health_quality',
                severity='low',
                file='SKILL.md',
                line=0,
                message=f'version format invalid: {version}',
                pattern=f'version: {version}',
                suggestion='Use semantic versioning (e.g., "1.0.0")',
            )
        
        if self.skill_md_content:
            hardcoded_paths = re.findall(r'[A-Z]:\\[^\s"\']+', self.skill_md_content)
            for p in hardcoded_paths:
                self.add_result(
                    category='health_quality',
                    severity='medium',
                    file='SKILL.md',
                    line=0,
                    message=f'Hardcoded Windows path detected: {p}',
                    pattern=p,
                    suggestion='Use relative paths or environment variables',
                )
        
        content_lower = self.skill_md_content.lower()
        has_error_handling = any(kw in content_lower for kw in ['error', 'exception', 'fail', 'fallback'])
        if not has_error_handling:
            self.add_result(
                category='health_quality',
                severity='low',
                file='SKILL.md',
                line=0,
                message='No error handling or exception handling mentioned',
                pattern='',
                suggestion='Document error handling strategy in SKILL.md',
            )
        
        # === Structure checks ===
        total_size = 0
        file_count = 0
        for rel, path in self.walker.walk():
            file_count += 1
            try:
                total_size += path.stat().st_size
            except (OSError, ValueError):
                pass
        
        if file_count > 200:
            self.add_result(
                category='health_structure',
                severity='high',
                file='.',
                line=0,
                message=f'Too many files: {file_count} (limit 200)',
                pattern='',
                suggestion='Remove unnecessary files',
            )
        
        if total_size > 10 * 1024 * 1024:
            self.add_result(
                category='health_structure',
                severity='high',
                file='.',
                line=0,
                message=f'Total size exceeds 10MB: {total_size / 1024 / 1024:.1f}MB',
                pattern='',
                suggestion='Compress resources, remove unnecessary dependencies',
            )
        
        has_readme = any((self.skill_path / f).exists() for f in ['README.md', 'readme.md', 'README.txt'])
        if not has_readme:
            self.add_result(
                category='health_structure',
                severity='low',
                file='.',
                line=0,
                message='Missing README.md',
                pattern='',
                suggestion='Add README.md with usage instructions',
            )
    
    def scan_compliance(self):
        """Compliance check: health + permissions unified output (v3.3.0)."""
        self.scan_health()
        self.scan_permissions()
    
    def check_update(self):
        """Check for new version (with caching to avoid frequent requests)."""
        cache_file = Path.home() / '.skill-security-checker-update-cache.json'
        now = datetime.now()
        
        # Check cache first
        try:
            if cache_file.exists():
                cache = json.loads(cache_file.read_text(encoding='utf-8'))
                cache_time = datetime.fromisoformat(cache['time'])
                if now - cache_time < timedelta(hours=UPDATE_CACHE_HOURS):
                    if cache.get('latest'):
                        latest = cache['latest']
                        if self._version_lt(CURRENT_VERSION, latest):
                            self.add_result(
                                category='update_check',
                                severity='info',
                                file='.',
                                line=0,
                                message=f'New version available: v{latest} (current: v{CURRENT_VERSION})',
                                pattern='',
                                suggestion=f'Run: skillhub update skill-security-checker',
                            )
                    return
        except (json.JSONDecodeError, ValueError, KeyError, TypeError):
            pass
        
        # Only fetch if cache expired
        try:
            import urllib.request
            req = urllib.request.Request(UPDATE_CHECK_URL, headers={'User-Agent': f'skill-security-checker/{CURRENT_VERSION}'})
            with urllib.request.urlopen(req, timeout=3) as resp:
                data = json.loads(resp.read().decode())
                latest = data.get('tag_name', '').lstrip('v')
                
                try:
                    cache_file.write_text(
                        json.dumps({'time': now.isoformat(), 'latest': latest}),
                        encoding='utf-8'
                    )
                except Exception:
                    pass
                
                if latest and self._version_lt(CURRENT_VERSION, latest):
                    self.add_result(
                        category='update_check',
                        severity='info',
                        file='.',
                        line=0,
                        message=f'New version available: v{latest} (current: v{CURRENT_VERSION})',
                        pattern='',
                        suggestion=f'Run: skillhub update skill-security-checker',
                    )
        except Exception:
            pass
    
    def run(self, skip_update=False):
        """Execute full audit flow."""
        workers = get_optimal_workers()
        
        scan_methods = [
            ('Static Scan', self.scan_static),
            ('Dependency Audit', self.scan_dependencies),
            ('Compliance Check', self.scan_compliance),
        ]

        if self.supply_chain:
            scan_methods.append(('Supply Chain', self.scan_supply_chain))

        if self.malicious_db:
            scan_methods.append(('Malicious DB', self.scan_malicious_db))
        
        # v3.2.0: Rule engine scan
        if self.rule_engine:
            scan_methods.append(('Rule Engine', self.scan_rule_engine))
        
        # v3.2.0: ML prompt injection detection
        if self.ml_detect:
            scan_methods.append(('ML Detection', self.scan_ml_prompt_injection))
        
        # v3.3.0: Taint tracking
        if self.taint_tracking:
            scan_methods.append(('Taint Tracking', self.scan_taint_tracking))
        
        # v3.3.0: Community rules
        if self.community_rules_path:
            scan_methods.append(('Community Rules', self.scan_community_rules))
        
        if not skip_update:
            scan_methods.append(('Update Check', self.check_update))
        
        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = {}
            for name, method in scan_methods:
                future = executor.submit(method)
                futures[future] = name
            
            for future in as_completed(futures):
                name = futures[future]
                try:
                    future.result()
                except Exception as e:
                    self.add_result(
                        category='scan_error',
                        severity='low',
                        file='.',
                        line=0,
                        message=f'{name} execution error: {e}',
                        pattern='',
                        suggestion='Report this issue to the developer',
                    )
        
        # v3.2.0: System-level behavior capture (eBPF/ETW)
        if self.syscall_monitor and _SYSCALL_MONITOR_AVAILABLE:
            try:
                self.scan_syscall_monitor()
            except Exception as e:
                self.add_result(
                    category='syscall_error', severity='low',
                    file='.', line=0,
                    message=f'Syscall monitor error: {e}',
                    pattern='', suggestion='请将该问题反馈给开发者',
                )
        
        # Dynamic sandbox scan runs after static scans (serial, time-boxed).
        if self.dynamic:
            try:
                self.scan_dynamic()
            except Exception as e:
                self.add_result(
                    category='dynamic_scan_error', severity='low',
                    file='.', line=0,
                    message=f'Dynamic scan execution error: {e}',
                    pattern='', suggestion='请将该问题反馈给开发者',
                )
        
        self.score = max(0, self.score)
        
        return self.get_report()

    # ============================================================
    # Quick Scan (v3.5.0) — L1 static layer only, 3-tier verdict
    # ============================================================

    def _load_quick_verdict_map(self):
        """Load externalized verdict mapping table (分数→档位)."""
        try:
            p = Path(__file__).parent / 'quick_verdict.json'
            with open(p, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {
                'severity_to_verdict': {
                    'critical': 'malicious', 'high': 'suspicious',
                    'medium': 'suspicious', 'low': 'clean', 'info': 'clean',
                },
                'categories_force_malicious': ['malicious_skill'],
                'verdicts': {
                    'malicious': {'label': '🚫 恶意', 'exit_code': 2,
                                  'reason_template': '检测到 {count} 条恶意指纹/严重漏洞，强烈建议不要安装'},
                    'suspicious': {'label': '⚠️ 可疑', 'exit_code': 1,
                                  'reason_template': '检测到 {count} 条高危或中危风险，建议审查后再安装'},
                    'clean': {'label': '✅ 干净', 'exit_code': 0,
                             'reason_template': '未发现明显安全风险，可放心安装'},
                },
            }

    def run_quick(self, skip_update=True):
        """Execute quick scan: L1 static layer only (malicious fingerprint + 6 rules + permission).

        Skips sandbox / OSV / taint tracking / ML / community rules for speed (≤30s target).
        """
        # Force-enable L1 detectors
        self.malicious_db = True
        self.rule_engine = True
        # Disable heavy detectors
        self.supply_chain = False
        self.taint_tracking = False
        self.ml_detect = False
        self.syscall_monitor = False
        self.community_rules_path = None
        self.dynamic = False

        if not self.rule_engine_obj and _RULE_ENGINE_AVAILABLE:
            self.rule_engine_obj = RuleEngine()
        if not self.malicious_db and _MALICIOUS_DB_AVAILABLE:
            pass  # scan_malicious_db handles availability internally

        # L1 detectors (independent, parallel for speed)
        l1_methods = [
            ('Malicious Fingerprint', self.scan_malicious_db),
            ('Rule Engine', self.scan_rule_engine),
            ('Permission Audit', self.scan_permissions),
        ]
        workers = min(len(l1_methods), get_optimal_workers())
        with ThreadPoolExecutor(max_workers=max(1, workers)) as executor:
            futures = {executor.submit(m): n for n, m in l1_methods}
            for fut in as_completed(futures):
                try:
                    fut.result()
                except Exception as e:
                    self.add_result(
                        category='scan_error', severity='low', file='.', line=0,
                        message=f'{futures[fut]} execution error: {e}',
                        pattern='', suggestion='请将该问题反馈给开发者',
                    )

        self.score = max(0, self.score)
        return self.get_quick_report()

    def get_quick_report(self):
        """Build a ≤1-screen quick report: verdict + Top3 + one-line reason."""
        vmap = self._load_quick_verdict_map()
        sev_to_v = vmap.get('severity_to_verdict', {})
        force_mal = set(vmap.get('categories_force_malicious', []))
        verdicts = vmap.get('verdicts', {})

        severity_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3, 'info': 4}
        sorted_results = sorted(self.results, key=lambda r: severity_order.get(r.severity, 5))

        # Determine verdict tier
        verdict = 'clean'
        for r in sorted_results:
            if r.category in force_mal:
                verdict = 'malicious'
                break
            mapped = sev_to_v.get(r.severity, 'clean')
            # escalation: malicious > suspicious > clean
            if mapped == 'malicious':
                verdict = 'malicious'
                break
            elif mapped == 'suspicious' and verdict != 'malicious':
                verdict = 'suspicious'

        vinfo = verdicts.get(verdict, {})
        label = vinfo.get('label', verdict)
        # Count findings that contributed to this verdict
        if verdict == 'malicious':
            relevant = [r for r in sorted_results if r.category in force_mal or r.severity == 'critical']
        elif verdict == 'suspicious':
            relevant = [r for r in sorted_results if r.severity in ('high', 'medium')]
        else:
            relevant = []
        count = len(relevant)
        reason = vinfo.get('reason_template', '').format(count=count) if verdict != 'clean' else vinfo.get('reason_template', '')

        # Top3 by severity
        top3 = [r.to_dict() for r in sorted_results[:3]]

        return {
            'meta': {
                'tool': 'skill-security-checker',
                'version': CURRENT_VERSION,
                'mode': 'quick',
                'scan_time': datetime.now().isoformat(),
                'skill_path': str(self.skill_path),
                'skill_name': self.frontmatter.get('name', 'unknown'),
                'score': self.score,
            },
            'verdict': verdict,
            'verdict_label': label,
            'reason': reason,
            'top3': top3,
            'total_findings': len(self.results),
        }

    def scan_rule_engine(self):
        """Scan using YAML rule packs (v3.2.0)."""
        if not self.rule_engine_obj:
            return
        for rel, path in self.walker.get_text_files():
            try:
                content = path.read_text(encoding='utf-8-sig')
            except Exception:
                continue
            if len(content) > 1024 * 1024:
                continue
            lines = content.split('\n')
            for line_num, line in enumerate(lines, 1):
                if '# nosec' in line.lower():
                    continue
                hits = self.rule_engine_obj.match_line(line)
                for pack, pattern in hits:
                    self.add_result(
                        category=pack.name,
                        severity=pack.severity,
                        file=str(rel),
                        line=line_num,
                        message=f"Detected {pack.display_name} risk: {line.strip()[:80]}",
                        pattern=pattern,
                        suggestion=pack.suggestion,
                        source='rule_engine',
                    )

    def scan_ml_prompt_injection(self):
        """ML-based prompt injection detection (v3.2.0)."""
        if not self.ml_detector_obj:
            return
        for rel, path in self.walker.get_text_files():
            try:
                content = path.read_text(encoding='utf-8-sig')
            except Exception:
                continue
            if len(content) > 1024 * 1024:
                continue
            lines = content.split('\n')
            for line_num, line in enumerate(lines, 1):
                if '# nosec' in line.lower():
                    continue
                result = self.ml_detector_obj.detect(line)
                if result['is_injection']:
                    self.add_result(
                        category='prompt_injection_ml',
                        severity='critical',
                        file=str(rel),
                        line=line_num,
                        message=f"ML detected prompt injection ({result['source']}, conf={result['confidence']:.2f}): {line.strip()[:80]}",
                        pattern=result['matches'][0] if result['matches'] else '',
                        suggestion='移除提示注入或越狱指令文本；如为文档示例，请添加 # nosec 注释',
                        source=f"ml_{result['source']}",
                    )

    def scan_taint_tracking(self):
        """Taint tracking: source-to-sink data flow analysis (v3.3.0)."""
        if not self.taint_tracking or not _TAINT_TRACKER_AVAILABLE:
            return
        for rel, path in self.walker.get_text_files():
            ext = Path(rel).suffix.lower()
            if ext not in ('.py', '.js', '.ts', '.jsx', '.tsx', '.php', '.rb', '.java', '.go'):
                continue
            findings = TaintTracker(str(rel)).track_file(str(path))
            for f in findings:
                self.add_result(
                    category='taint_tracking',
                    severity=f.get('severity', 'medium'),
                    file=f.get('filename', str(rel)),
                    line=f.get('sink_line', 0),
                    message=f"污点追踪: {f.get('flow_path', '')}",
                    pattern=f.get('sink_name', ''),
                    suggestion='验证数据流是否安全；如为误报请添加 # nosec 注释',
                    source=f"taint_{f.get('type', 'unknown')}",
                )

    def scan_community_rules(self):
        """Scan using community rule packs (v3.3.0)."""
        if not self.community_rules_loaded:
            return
        for rel, path in self.walker.get_text_files():
            try:
                content = path.read_text(encoding='utf-8-sig')
            except Exception:
                continue
            if len(content) > 1024 * 1024:
                continue
            lines = content.split('\n')
            for line_num, line in enumerate(lines, 1):
                if '# nosec' in line.lower():
                    continue
                for rule in self.community_rules_loaded:
                    patterns = rule.get('patterns', [])
                    severity = rule.get('severity', 'medium')
                    name = rule.get('name', 'unknown')
                    suggestion = rule.get('suggestion', '')
                    for pat in patterns:
                        try:
                            if re.search(pat, line, re.IGNORECASE):
                                self.add_result(
                                    category=f"community_{name}",
                                    severity=severity,
                                    file=str(rel),
                                    line=line_num,
                                    message=f"社区规则命中 [{name}]: {line.strip()[:80]}",
                                    pattern=pat,
                                    suggestion=suggestion,
                                    source='community_rule',
                                )
                        except re.error:
                            continue

    def scan_syscall_monitor(self):
        """System-level behavior capture via eBPF/ETW (v3.2.0)."""
        if not _SYSCALL_MONITOR_AVAILABLE:
            return
        # Create a monitor for the current process (self-scan demo)
        # In real usage, this would monitor the sandboxed skill process
        monitor = create_syscall_monitor(os.getpid(), timeout=5)
        if not monitor.available():
            self.add_result(
                category='syscall_monitor',
                severity='info',
                file='.',
                line=0,
                message='系统级行为捕获不可用（eBPF/ETW 未就绪）',
                pattern='',
                suggestion='Linux 需要 root + bcc；Windows 需要管理员权限',
            )
            return
        monitor.start()
        events = monitor.stop()
        for event in events:
            parsed = monitor.parse_event(event)
            self.add_result(
                category='syscall_behavior',
                severity='info',
                file='.',
                line=0,
                message=f"系统调用: {parsed.get('syscall', 'unknown')} ({parsed.get('category', 'unknown')})",
                pattern=parsed.get('raw', '')[:100],
                suggestion='',
                source=f"syscall_{parsed.get('backend', 'unknown')}",
            )
    
    def get_report(self):
        """Generate audit report."""
        severity_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3, 'info': 4}
        sorted_results = sorted(self.results, key=lambda r: severity_order.get(r.severity, 5))
        
        stats = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0, 'info': 0}
        for r in sorted_results:
            stats[r.severity] = stats.get(r.severity, 0) + 1
        
        return {
            'meta': {
                'tool': 'skill-security-checker',
                'version': CURRENT_VERSION,
                'scan_time': datetime.now().isoformat(),
                'skill_path': str(self.skill_path),
                'skill_name': self.frontmatter.get('name', 'unknown'),
                'total_files_scanned': len(self.walker.scanned_files),
                'total_files_skipped': len(self.walker.skipped_files),
                'workers_used': get_optimal_workers(),
                'dynamic_scan': self._dynamic_meta(),
                'supply_chain': {
                    'enabled': self.supply_chain,
                    'findings': len(self.supply_chain_findings),
                    'osv_offline': {
                        'available': _OSV_OFFLINE_AVAILABLE,
                        'index_pypi_at': _osv_get_ts('pypi') if _OSV_OFFLINE_AVAILABLE else None,
                        'index_npm_at': _osv_get_ts('npm') if _OSV_OFFLINE_AVAILABLE else None,
                    },
                },
                'malicious_db': {
                    'enabled': self.malicious_db,
                    'findings': len(self.malicious_db_findings),
                },
                'global_exclude': {
                    'enabled': self.global_exclude,
                    'loaded': self.global_exclude_config.loaded if self.global_exclude_config else False,
                },
                'rule_engine': {
                    'enabled': self.rule_engine,
                    'rules_loaded': len(self.rule_engine_obj.packs) if self.rule_engine_obj else 0,
                },
                'ml_detect': {
                    'enabled': self.ml_detect,
                    'status': self.ml_detector_obj.get_status() if self.ml_detector_obj else {},
                },
                'syscall_monitor': {
                    'enabled': self.syscall_monitor,
                    'available': _SYSCALL_MONITOR_AVAILABLE,
                },
                'taint_tracking': {
                    'enabled': self.taint_tracking,
                    'available': _TAINT_TRACKER_AVAILABLE,
                },
                'community_rules': {
                    'enabled': bool(self.community_rules_path),
                    'loaded': len(self.community_rules_loaded),
                },
            },
            'score': self.score,
            'grade': self._get_grade(),
            'statistics': stats,
            'results': [r.to_dict() for r in sorted_results],
            'summary': self._generate_summary(stats),
            'changelog_version_count': getattr(self, 'changelog_version_count', 0),
        }

    def _dynamic_meta(self):
        """Summarize the dynamic scan for the report meta block."""
        if not self.dynamic:
            return {'enabled': False}
        rep = self.dynamic_report or {}
        return {
            'enabled': True,
            'available': rep.get('available', False),
            'backend': rep.get('backend', 'none'),
            'behaviors_captured': len(rep.get('behaviors', [])),
            'findings': len(rep.get('findings', [])),
            'hint': rep.get('hint', ''),
        }
    
    def _get_grade(self):
        if self.score >= 90:
            return 'A'
        elif self.score >= 75:
            return 'B'
        elif self.score >= 60:
            return 'C'
        elif self.score >= 40:
            return 'D'
        else:
            return 'F'
    
    def _generate_summary(self, stats):
        parts = []
        if stats['critical'] > 0:
            parts.append(f"Found {stats['critical']} critical issues, must fix immediately!")
        if stats['high'] > 0:
            parts.append(f"Found {stats['high']} high severity issues, fix ASAP.")
        if stats['medium'] > 0:
            parts.append(f"Found {stats['medium']} medium issues.")
        if stats['low'] > 0:
            parts.append(f"Found {stats['low']} low severity issues.")
        if not parts:
            parts.append("No security issues found!")
        return ' '.join(parts)


# ============================================================
# Report Generator
# ============================================================

class ReportGenerator:
    """Generate JSON/HTML reports."""
    
    @staticmethod
    def to_json(report, output_path=None):
        json_str = json.dumps(report, ensure_ascii=False, indent=2)
        if output_path:
            Path(output_path).write_text(json_str, encoding='utf-8')
        return json_str

    @staticmethod
    def to_quick(quick_report, output_path=None):
        """Render the ≤1-screen quick verdict report."""
        v = quick_report
        lines = []
        lines.append('=' * 56)
        lines.append('  ⚡ Skill 安全快扫（Quick Mode）')
        lines.append('=' * 56)
        lines.append(f"  Skill: {v['meta']['skill_name']}  |  得分: {v['meta']['score']}/100")
        lines.append(f"  裁定: {v['verdict_label']}")
        lines.append(f"  理由: {v['reason']}")
        lines.append('-' * 56)
        if v['top3']:
            lines.append(f"  Top3 风险:")
            for i, r in enumerate(v['top3'], 1):
                sev = r['severity'].upper()
                fdisp = r['file'][:20] + '..' if len(r['file']) > 22 else r['file']
                lines.append(f"   {i}. [{sev}] {r['category']}  {fdisp}:{r['line']}")
                if r.get('suggestion'):
                    lines.append(f"      → {r['suggestion'][:48]}")
        else:
            lines.append('  Top3 风险: 无')
        lines.append('-' * 56)
        lines.append(f"  共 {v['total_findings']} 条发现  |  完整扫描用 --mode full")
        lines.append('  Feedback: njskills@agent.qq.com')
        lines.append('=' * 56)
        text = '\n'.join(lines)
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(text)
        return text
    
    @staticmethod
    def to_html(report, output_path=None):
        severity_colors = {
            'critical': '#dc3545',
            'high': '#fd7e14',
            'medium': '#ffc107',
            'low': '#17a2b8',
            'info': '#6c757d',
        }
        severity_labels = {
            'critical': 'Critical',
            'high': 'High',
            'medium': 'Medium',
            'low': 'Low',
            'info': 'Info',
        }
        
        grade_colors = {'A': '#28a745', 'B': '#6f42c1', 'C': '#ffc107', 'D': '#fd7e14', 'F': '#dc3545'}
        
        results_html = ''
        for r in report['results']:
            color = severity_colors.get(r['severity'], '#6c757d')
            label = severity_labels.get(r['severity'], r['severity'])
            results_html += f'''
            <tr>
                <td><span class="badge" style="background:{color}">{label}</span></td>
                <td>{r['category']}</td>
                <td><code>{r['file']}</code></td>
                <td>{r['line']}</td>
                <td>{r['message']}</td>
                <td><small>{r['suggestion']}</small></td>
            </tr>
            '''
        
        html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Skill Security Audit Report - {report['meta']['skill_name']}</title>
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background:#f5f7fa; color:#333; line-height:1.6; }}
.container {{ max-width:1200px; margin:0 auto; padding:20px; }}
.header {{ background:linear-gradient(135deg,#667eea 0%,#764ba2 100%); color:#fff; padding:30px; border-radius:12px; margin-bottom:20px; }}
.header h1 {{ font-size:24px; margin-bottom:8px; }}
.header .meta {{ opacity:0.9; font-size:14px; }}
.score-card {{ background:#fff; border-radius:12px; padding:24px; margin-bottom:20px; box-shadow:0 2px 8px rgba(0,0,0,0.08); text-align:center; }}
.score-card .score {{ font-size:64px; font-weight:700; color:{grade_colors.get(report['grade'], '#333')}; }}
.score-card .grade {{ font-size:36px; font-weight:600; margin-top:8px; }}
.stats {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(150px,1fr)); gap:12px; margin-bottom:20px; }}
.stat-card {{ background:#fff; border-radius:8px; padding:16px; text-align:center; box-shadow:0 2px 4px rgba(0,0,0,0.06); }}
.stat-card .num {{ font-size:28px; font-weight:700; }}
.stat-card .label {{ font-size:12px; color:#666; margin-top:4px; }}
.results {{ background:#fff; border-radius:12px; padding:20px; box-shadow:0 2px 8px rgba(0,0,0,0.08); }}
.results h2 {{ margin-bottom:16px; font-size:18px; }}
table {{ width:100%; border-collapse:collapse; font-size:13px; }}
th {{ background:#f8f9fa; padding:10px; text-align:left; font-weight:600; border-bottom:2px solid #dee2e6; }}
td {{ padding:10px; border-bottom:1px solid #eee; vertical-align:top; }}
tr:hover {{ background:#f8f9fa; }}
.badge {{ display:inline-block; padding:2px 8px; border-radius:4px; color:#fff; font-size:11px; font-weight:600; }}
code {{ background:#f1f3f5; padding:2px 6px; border-radius:3px; font-size:12px; }}
.footer {{ text-align:center; padding:20px; color:#999; font-size:12px; }}
</style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1>Skill Security Audit Report</h1>
        <div class="meta">
            Skill: <strong>{report['meta']['skill_name']}</strong> |
            Version: {report['meta']['version']} |
            Scan time: {report['meta']['scan_time']}
        </div>
    </div>
    
    <div class="score-card">
        <div class="score">{report['score']}</div>
        <div class="grade">Grade: {report['grade']}</div>
        <p style="margin-top:12px;color:#666;">{report['summary']}</p>
    </div>
    
    <div class="stats">
        <div class="stat-card">
            <div class="num" style="color:#dc3545">{report['statistics']['critical']}</div>
            <div class="label">Critical</div>
        </div>
        <div class="stat-card">
            <div class="num" style="color:#fd7e14">{report['statistics']['high']}</div>
            <div class="label">High</div>
        </div>
        <div class="stat-card">
            <div class="num" style="color:#ffc107">{report['statistics']['medium']}</div>
            <div class="label">Medium</div>
        </div>
        <div class="stat-card">
            <div class="num" style="color:#17a2b8">{report['statistics']['low']}</div>
            <div class="label">Low</div>
        </div>
        <div class="stat-card">
            <div class="num" style="color:#6c757d">{report['statistics']['info']}</div>
            <div class="label">Info</div>
        </div>
    </div>
    
    <div class="results">
        <h2>Detailed Results</h2>
        <table>
            <thead>
                <tr>
                    <th>Severity</th>
                    <th>Category</th>
                    <th>File</th>
                    <th>Line</th>
                    <th>Description</th>
                    <th>Fix Suggestion</th>
                </tr>
            </thead>
            <tbody>
                {results_html if results_html else '<tr><td colspan="6" style="text-align:center;color:#999;">No issues found</td></tr>'}
            </tbody>
        </table>
    </div>
    
    <div class="footer">
        <p>Generated by skill-security-checker v{report['meta']['version']} |
        Files scanned: {report['meta']['total_files_scanned']} |
        Files skipped: {report['meta']['total_files_skipped']}</p>
        <p>Feedback: njskills@agent.qq.com</p>
    </div>
</div>
</body>
</html>'''
        
        if output_path:
            Path(output_path).write_text(html, encoding='utf-8')
        return html

    @staticmethod
    def to_sarif(report, output_path=None):
        """Generate SARIF 2.1.0 output (GitHub Code Scanning format)."""
        rules_map = {}
        results = []
        for r in report['results']:
            rule_id = r.get('category', 'unknown')
            if rule_id not in rules_map:
                rules_map[rule_id] = {
                    'id': rule_id,
                    'name': rule_id.replace('_', ' ').title(),
                    'shortDescription': {'text': r.get('message', '')[:200]},
                    'fullDescription': {'text': r.get('message', '')},
                    'defaultConfiguration': {
                        'level': {
                            'critical': 'error',
                            'high': 'error',
                            'medium': 'warning',
                            'low': 'warning',
                            'info': 'note',
                        }.get(r.get('severity', 'warning'), 'warning'),
                    },
                    'help': {'text': r.get('suggestion', '')},
                }
            results.append({
                'ruleId': rule_id,
                'level': {
                    'critical': 'error',
                    'high': 'error',
                    'medium': 'warning',
                    'low': 'warning',
                    'info': 'note',
                }.get(r.get('severity', 'warning'), 'warning'),
                'message': {'text': r.get('message', '')},
                'locations': [{
                    'physicalLocation': {
                        'artifactLocation': {'uri': r.get('file', '')},
                        'region': {'startLine': max(1, r.get('line', 0))},
                    },
                }],
            })

        sarif = {
            '$schema': 'https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json',
            'version': '2.1.0',
            'runs': [{
                'tool': {
                    'driver': {
                        'name': 'skill-security-checker',
                        'version': report['meta'].get('version', '0.0.0'),
                        'informationUri': 'https://github.com/njskills/skill-security-checker',
                        'rules': list(rules_map.values()),
                    },
                },
                'results': results,
            }],
        }

        json_str = json.dumps(sarif, ensure_ascii=False, indent=2)
        if output_path:
            Path(output_path).write_text(json_str, encoding='utf-8')
        return json_str


# ============================================================
# CLI Entry Point
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description='Skill Security - Skill security audit tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python audit.py /path/to/skill
  python audit.py /path/to/skill --format html -o report.html
  python audit.py /path/to/skill --skip-update
  python audit.py /path/to/skill --dynamic
  python audit.py /path/to/skill --dynamic --allow-domain api.github.com --sandbox-timeout 60
  python audit.py /path/to/skill --supply-chain
  python audit.py /path/to/skill --format sarif -o sarif.json
        ''')
    parser.add_argument('skill_path', help='Path to skill directory to audit')
    parser.add_argument('--format', choices=['json', 'html', 'text', 'sarif'], default='text',
                        help='Output format (default: text)')
    parser.add_argument('-o', '--output', help='Output file path')
    parser.add_argument('--skip-update', action='store_true', help='Skip update check')
    parser.add_argument('--dynamic', action='store_true',
                        help='Enable dynamic sandbox execution scan (needs Docker/Windows Sandbox)')
    parser.add_argument('--allow-domain', action='append', default=[],
                        help='Whitelist a domain for sandbox network (repeatable)')
    parser.add_argument('--sandbox-timeout', type=int, default=30,
                        help='Sandbox execution timeout in seconds (default: 30)')
    parser.add_argument('--supply-chain', action='store_true',
                        help='Enable supply chain risk analysis')
    parser.add_argument('--malicious-db', action='store_true',
                        help='Enable real-time malicious skill fingerprint matching (341 entries)')
    parser.add_argument('--global-exclude', action='store_true',
                        help='Enable .nosec.yml global exclude config parsing')
    parser.add_argument('--rule-engine', action='store_true',
                        help='Enable YAML rule pack scanning (rules/*.yaml)')
    parser.add_argument('--syscall-monitor', action='store_true',
                        help='Enable eBPF/ETW system-level behavior capture (v3.2.0)')
    parser.add_argument('--ml-detect', action='store_true',
                        help='Enable ML prompt injection detection (ONNX + regex fallback)')
    parser.add_argument('--taint-tracking', action='store_true',
                        help='Enable source-to-sink taint tracking (Python AST + JS lexical)')
    parser.add_argument('--community-rules', type=str, default=None,
                        help='Path to directory of community YAML rule packs')
    parser.add_argument('--refresh-osv', action='store_true',
                        help='Force refresh of the OSV offline data package index (v3.4.0)')
    parser.add_argument('--quick', action='store_true',
                        help='一键快扫模式：仅跑 L1 静态层（恶意指纹+6类规则+权限审计），30秒内出三档裁定 (v3.5.0)')
    parser.add_argument('--mode', choices=['quick', 'full'], default=os.environ.get('SKILLSEC_MODE', 'quick'),
                        help='扫描档位：quick=快扫三档裁定(≤1屏, 默认) / full=全量细节(SARIF/HTML/JSON) (v3.5.0)')
    
    args = parser.parse_args()
    
    if not os.path.isdir(args.skill_path):
        print(f"Error: Directory does not exist: {args.skill_path}", file=sys.stderr)
        sys.exit(1)
    
    dyn_opts = None
    if args.dynamic and _SANDBOX_AVAILABLE:
        dyn_opts = DynamicScanOptions.auto(
            timeout_sec=args.sandbox_timeout,
            whitelist_domains=args.allow_domain,
            network=bool(args.allow_domain),
        )
    
    mode = 'quick' if args.quick else args.mode

    if mode == 'quick':
        auditor = SecurityAuditor(args.skill_path, refresh_osv=args.refresh_osv)
        quick_report = auditor.run_quick(skip_update=True)
        if args.format == 'json':
            out = ReportGenerator.to_json(quick_report, args.output)
            if not args.output:
                print(out)
        else:
            out = ReportGenerator.to_quick(quick_report, args.output)
            if not args.output:
                print(out)
        exit_codes = {'malicious': 2, 'suspicious': 1, 'clean': 0}
        sys.exit(exit_codes.get(quick_report['verdict'], 0))

    auditor = SecurityAuditor(args.skill_path, dynamic=args.dynamic, dynamic_options=dyn_opts,
                              supply_chain=args.supply_chain, malicious_db=args.malicious_db,
                              global_exclude=args.global_exclude, rule_engine=args.rule_engine,
                              syscall_monitor=args.syscall_monitor, ml_detect=args.ml_detect,
                              taint_tracking=args.taint_tracking, community_rules_path=args.community_rules,
                              refresh_osv=args.refresh_osv)
    report = auditor.run(skip_update=args.skip_update)
    
    if args.format == 'json':
        output = ReportGenerator.to_json(report, args.output)
        if not args.output:
            print(output)
    elif args.format == 'html':
        output = ReportGenerator.to_html(report, args.output)
        if not args.output:
            print(f"HTML report generated ({len(output)} chars)")
    elif args.format == 'sarif':
        output = ReportGenerator.to_sarif(report, args.output)
        if not args.output:
            print(output)
    else:
        print(f"\n{'='*60}")
        print(f"  Skill Security Audit Report")
        print(f"{'='*60}")
        print(f"  Skill: {report['meta']['skill_name']}")
        print(f"  Path: {report['meta']['skill_path']}")
        print(f"  Time: {report['meta']['scan_time']}")
        print(f"  Files: {report['meta']['total_files_scanned']} scanned, {report['meta']['total_files_skipped']} skipped")
        dyn = report['meta'].get('dynamic_scan', {})
        if dyn.get('enabled'):
            if dyn.get('available'):
                print(f"  Dynamic: backend={dyn.get('backend')}, "
                      f"behaviors={dyn.get('behaviors_captured', 0)}, "
                      f"findings={dyn.get('findings', 0)}")
            else:
                print(f"  Dynamic: skipped ({dyn.get('hint', 'no isolation backend')})")
        sc = report['meta'].get('supply_chain', {})
        if sc.get('enabled'):
            print(f"  Supply Chain: {sc.get('findings', 0)} findings")
        print(f"{'='*60}")
        print(f"\n  Score: {report['score']}/100 (Grade: {report['grade']})")
        print(f"  {report['summary']}\n")
        
        if report['results']:
            print(f"  {'─'*56}")
            severity_labels = {'critical': '[CRIT]', 'high': '[HIGH]', 'medium': '[MED]', 'low': '[LOW]', 'info': '[INFO]'}
            for r in report['results']:
                sev = severity_labels.get(r['severity'], r['severity'])
                file_display = r['file'][:15] + '..' if len(r['file']) > 17 else r['file']
                msg_display = r['message'][:35] + '..' if len(r['message']) > 37 else r['message']
                print(f"  {sev:<7} {r['category']:<18} {file_display:<17} {msg_display}")
            print(f"  {'─'*56}")
        
        print(f"\n  Fix suggestions:")
        critical_high = [r for r in report['results'] if r['severity'] in ('critical', 'high')]
        if critical_high:
            for r in critical_high[:5]:  # Show top 5
                print(f"    [{r['category']}] {r['suggestion']}")
        else:
            print("    No critical or high severity issues to fix!")
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(json.dumps(report, ensure_ascii=False, indent=2))
            print(f"\n  Report saved: {args.output}")
        
        print(f"\n  Feedback: njskills@agent.qq.com")
        print(f"{'='*60}\n")
    
    if report['statistics']['critical'] > 0 or report['statistics']['high'] > 0:
        sys.exit(2)
    elif report['statistics']['medium'] > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
