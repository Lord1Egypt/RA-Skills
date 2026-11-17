"""Legacy ``scripts.scan`` import surface, separate from the product CLI."""

import os
from pathlib import Path

from skill_vitals import __version__
from skill_vitals.adapters.claude import lookup_usage, read_host_config
from skill_vitals.adapters.codex import apply_codex_runtime as _apply_codex_runtime, find_codex_executable, read_codex_runtime
from skill_vitals.adapters.hermes import read_hermes_external_dirs
from skill_vitals.adapters.openclaw import apply_openclaw_runtime, find_openclaw_bundled_skills, read_openclaw_roots, read_openclaw_runtime
from skill_vitals.adapters.workbuddy import WORKBUDDY_ORPHANED, _safe_segment, read_workbuddy_builtin_roots, read_workbuddy_welcome_mode, workbuddy_skill_active
from skill_vitals.analysis import LEVEL_RANK, LEVEL_RANK_BY_HOST, level_rank
from skill_vitals.cli import CODEX_FALLBACK_DESC_BUDGET, DEFAULT_DESC_BUDGET, DEFAULT_ROOTS, SCHEMA_VERSION, ZOMBIE_MIN_AGE_DAYS, main
from skill_vitals.diff import _diff_entry, _sorted_keys
import skill_vitals.discovery as discovery_module
from skill_vitals.discovery import DOC_DIRS, PLUGIN_PATH_RE, PLUGIN_WRAPPER_DIRS, REPO_META, VERSION_SEGMENT_RE, plugin_identity
from skill_vitals.doctor import DOCTOR_WIDTH, NOT_ASSESSED, SECURITY_CODES, SECURITY_SEVERITY, SEVERITY_GLYPH, SEVERITY_RANK, _NO_LINE_START, _WIDE_RANGES, _cols, _diag, _doctor_evidence_lines, _doctor_not_loaded_breakdown, _doctor_snapshot, _wrap, diagnose, render_doctor
from skill_vitals.explain import FUNNEL_GLYPH, FUNNEL_STAGES, _budget_at_risk_names, _days_since_epoch, _enabled_stage, _explain_fix_lines, _print_explain, _shadow_map, explain_record, find_skills, funnel, render_explain
from skill_vitals.frontmatter import FRONTMATTER_RE, parse_frontmatter
from skill_vitals.inventory import build_inventory
from skill_vitals.lifecycle import DEFAULT_DORMANT_DAYS, human_last_used, human_tokens, lifecycle_status, load_state, render_list
from skill_vitals.overlap import DEFAULT_OVERLAP_MIN, _STOP_EN, _STOP_ZH, _cjk_runs, _shared_display, _tokenize, overlap_pairs, render_overlap
from skill_vitals.redact import INSTANCE_NAME_KEYS, PLUGIN_KEY_KEYS, PLUGIN_NAME_KEYS, SKILL_NAME_KEYS
import skill_vitals.redact as redact_module
from skill_vitals.report import build_report
from skill_vitals.security import CITATION_HINTS, EXEC_EXT, OPEN_QUOTES, SECURITY_PATTERNS, SELF_SKILL_ROOT, URL_RE, is_cited, security_scan
from skill_vitals.snapshots import SNAPSHOT_DIR_MODE, SNAPSHOT_FILE_MODE, SNAPSHOT_KEEP, _diff_name, _overlap_keys, diff_against, latest_snapshot, list_snapshots, render_diff, render_snapshot, save_snapshot, snapshot_dir
from skill_vitals.util import est_tokens, norm, safe_str

HOME_N = norm(Path(os.path.expanduser("~")))
CWD_N = norm(Path.cwd())

def classify(skill_dir, host, *, home_n=None, cwd_n=None):
    return discovery_module.classify(skill_dir, host, home_n or HOME_N, cwd_n or CWD_N)

def days_since(ms):
    return discovery_module.days_since(ms)

def redact(obj, names=False, name_map=None, *, home_n=None, cwd_n=None):
    return redact_module.redact(obj, names=names, name_map=name_map, home_n=home_n or HOME_N, cwd_n=cwd_n or CWD_N)

def scan_skill_dir(skill_dir, host, enabled_plugins, usage, plugins_known, source_meta=None, *, home_n=None, cwd_n=None):
    return discovery_module.scan_skill_dir(skill_dir, host, enabled_plugins, usage, plugins_known, source_meta, home_n=home_n or HOME_N, cwd_n=cwd_n or CWD_N)

def apply_codex_runtime(skills, runtime, *, scanner=None):
    return _apply_codex_runtime(skills, runtime, scanner or scan_skill_dir)

def collect(roots, enabled_plugins, usage, plugins_known, *, home_n=None, cwd_n=None):
    return discovery_module.collect(roots, enabled_plugins, usage, plugins_known, home=home_n or HOME_N, cwd=cwd_n or CWD_N)

COMPAT_EXPORTS = tuple(name for name in globals() if not name.startswith("__") and name not in {"os", "Path", "discovery_module", "redact_module"})
