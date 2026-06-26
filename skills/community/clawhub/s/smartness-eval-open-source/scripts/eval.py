#!/usr/bin/env python3
"""OpenClaw Smartness Evaluation Engine v0.3.3

Three-layer scoring architecture:
  Layer 1 — Functional Tests (70%): deterministic capability tests via kernel --process
  Layer 2 — System Health    (20%): runtime metrics from kernel logs and state files
  Layer 3 — Growth           (10%): knowledge accumulation and self-improvement

Design principles:
  - Version-agnostic: all functional tests use cognitive-kernel --process
  - Capability-focused: tests WHAT the system can do, not HOW
  - Transparent: every score traceable to specific evidence
  - Upgrade-safe: new capabilities add score, upgrades don't break tests
"""

from __future__ import annotations

import argparse
import base64 as _b64
import hashlib
import json
import math
import os
import sqlite3
import statistics
import subprocess
import sys
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = SKILL_DIR / 'config'


def _resolve_workspace() -> Path:
    """Find OpenClaw workspace: env var > installed-skill parent > default."""
    if os.environ.get('OPENCLAW_WORKSPACE'):
        return Path(os.environ['OPENCLAW_WORKSPACE'])
    # When installed as skill: SKILL_DIR is inside workspace/skills/
    candidate = SKILL_DIR.parent.parent
    if (candidate / 'scripts').exists() and (candidate / 'state').exists():
        return candidate
    # Default
    return Path.home() / '.openclaw' / 'workspace'


WORKSPACE = _resolve_workspace()
STATE_DIR = WORKSPACE / 'state' / 'smartness-eval'
RUNS_DIR = STATE_DIR / 'runs'
REPORTS_DIR = STATE_DIR / 'reports'
RUNS_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

WS_STATE = WORKSPACE / 'state'
REASONING_DB = WORKSPACE / '.reasoning' / 'reasoning-store.sqlite'
KERNEL_LOG_DB = WS_STATE / 'v7-kernel-log.db'


# ---------------------------------------------------------------------------
# Skill signature (tamper-resistant)
# ---------------------------------------------------------------------------

def _skill_sig() -> dict:
    """Return skill authorship metadata. Do not modify or remove."""
    _a = _b64.b64decode(b'5ZyG6KeE').decode('utf-8')
    _h = hashlib.sha256((_a + 'openclaw-smartness-eval').encode()).hexdigest()[:12]
    return {'author': _a, 'skill': 'openclaw-smartness-eval', 'integrity': _h}


# ═══════════════════════════════════════════════════════════════════════════
# Utilities
# ═══════════════════════════════════════════════════════════════════════════

def load_json(path: Path, default=None):
    if not path.exists():
        return default if default is not None else {}
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except (json.JSONDecodeError, OSError):
        return default if default is not None else {}


def pct(values: list[float], p: float) -> float:
    if not values:
        return 0.0
    if len(values) == 1:
        return float(values[0])
    s = sorted(values)
    rank = (len(s) - 1) * p
    lo, hi = math.floor(rank), math.ceil(rank)
    if lo == hi:
        return float(s[lo])
    return float(s[lo] + (s[hi] - s[lo]) * (rank - lo))


def clamp(v: float, lo: float = 0.0, hi: float = 100.0) -> float:
    return max(lo, min(hi, v))


def ratio(num: float, den: float, default: float = 0.0) -> float:
    return num / den if den else default


def resolve_json_path(data, dotted: str):
    cur = data
    for part in dotted.split('.'):
        if isinstance(cur, dict):
            cur = cur.get(part)
        else:
            return None
    return cur


def validate_command(command: list[str]) -> tuple[bool, str]:
    if not isinstance(command, list) or not command:
        return False, 'invalid_command_format'
    if command[0] != 'python3':
        return False, 'only_python3_allowed'
    for token in command[1:]:
        if token == '-c' or token.startswith('-c'):
            return False, 'inline_python_disallowed'
        if 'exec(' in token:
            return False, 'exec_pattern_disallowed'
        p = Path(token)
        if p.is_absolute():
            return False, 'absolute_path_disallowed'
        if '..' in p.parts:
            return False, 'path_traversal_disallowed'
    return True, 'ok'


# ═══════════════════════════════════════════════════════════════════════════
# Layer 1: Functional Tests
# ═══════════════════════════════════════════════════════════════════════════

def run_cmd(command: list[str], timeout: int = 120) -> subprocess.CompletedProcess:
    return subprocess.run(command, cwd=str(WORKSPACE),
                          capture_output=True, text=True, timeout=timeout)


def evaluate_test(test: dict) -> dict:
    command = test.get('command', [])
    allowed, reason = validate_command(command)
    if not allowed:
        return {
            'id': test['id'], 'name': test['name'], 'passed': False,
            'returncode': -1, 'stdout_preview': '', 'stderr_preview': 'BLOCKED',
            'notes': [reason], 'dimensions': test.get('dimensions', {}),
        }
    try:
        result = run_cmd(command)
    except subprocess.TimeoutExpired:
        return {
            'id': test['id'], 'name': test['name'], 'passed': False,
            'returncode': -1, 'stdout_preview': '', 'stderr_preview': 'TIMEOUT',
            'notes': ['timeout'], 'dimensions': test.get('dimensions', {}),
        }
    stdout = (result.stdout or '').strip()
    stderr = (result.stderr or '').strip()
    passed = result.returncode == 0
    notes: list[str] = []

    if test['type'] in {'json_path_equals', 'json_path_exists'}:
        passed = True
        try:
            payload = json.loads(stdout) if stdout else {}
            actual = resolve_json_path(payload, test['path'])
            if test['type'] == 'json_path_equals':
                if actual != test.get('expected'):
                    passed = False
                    notes.append(f"expected={test.get('expected')} actual={actual}")
            else:
                if actual is None:
                    passed = False
                    notes.append(f"missing_path={test['path']}")
        except json.JSONDecodeError as exc:
            passed = False
            notes.append(f'invalid_json:{exc}')
    elif test['type'] == 'stdout_contains':
        passed = True
        for needle in test.get('contains', []):
            if needle not in stdout:
                passed = False
                notes.append(f'missing:{needle}')
    elif test['type'] == 'exit_code':
        expected = int(test.get('expected', 0))
        if result.returncode != expected:
            passed = False
            notes.append(f'expected_exit={expected} actual={result.returncode}')

    return {
        'id': test['id'], 'name': test['name'], 'passed': passed,
        'returncode': result.returncode,
        'stdout_preview': stdout[:300], 'stderr_preview': stderr[:200],
        'notes': notes, 'dimensions': test.get('dimensions', {}),
    }


def select_tests(task_suite: dict, mode: str, config: dict) -> list[dict]:
    tags = set(config.get('modes', {}).get(mode, {}).get('task_tags', []))
    return [t for t in task_suite.get('tests', [])
            if t.get('tags') and tags.intersection(t['tags'])]


def compute_dimension_scores(results: list[dict], config: dict) -> dict[str, float]:
    """Score = (earned_weight / possible_weight) * 100 per dimension."""
    dims = list(config.get('dimensions', {}).keys())
    earned = {d: 0.0 for d in dims}
    possible = {d: 0.0 for d in dims}
    for r in results:
        for dim, w in r.get('dimensions', {}).items():
            if dim in earned:
                possible[dim] += float(w)
                if r.get('passed'):
                    earned[dim] += float(w)
    return {d: round(earned[d] / possible[d] * 100, 2) if possible[d] > 0 else 0.0
            for d in dims}


# ═══════════════════════════════════════════════════════════════════════════
# Layer 2: System Health Metrics
# ═══════════════════════════════════════════════════════════════════════════

def collect_health_metrics(window_days: int) -> dict:
    cutoff = datetime.now() - timedelta(days=window_days)
    health: dict = {}

    # --- Latency from kernel log ---
    rule_latencies: list[float] = []
    llm_latencies: list[float] = []

    # Try V7 DB first, then V6 JSON log
    if KERNEL_LOG_DB.exists():
        try:
            conn = sqlite3.connect(str(KERNEL_LOG_DB))
            cutoff_str = cutoff.isoformat()
            for row in conn.execute(
                "SELECT source, total_ms FROM kernel_log WHERE total_ms>0 AND timestamp>=?",
                (cutoff_str,)
            ).fetchall():
                src, ms = row
                (llm_latencies if src == 'llm_analysis' else rule_latencies).append(ms)
            conn.close()
        except Exception:
            pass

    if not rule_latencies and not llm_latencies:
        kernel_json = load_json(WS_STATE / 'v6-kernel-log.json', [])
        if isinstance(kernel_json, list):
            for entry in kernel_json[-200:]:
                ms = entry.get('total_ms') or entry.get('latency_ms', 0)
                if ms > 0:
                    src = entry.get('source', '')
                    (llm_latencies if 'llm' in src else rule_latencies).append(float(ms))

    # Also try response-latency-metrics.json as fallback
    if not rule_latencies and not llm_latencies:
        lat_data = load_json(WS_STATE / 'response-latency-metrics.json', {'records': []})
        for item in lat_data.get('records', [])[-200:]:
            ms = item.get('latency_ms', 0)
            if ms > 0:
                rule_latencies.append(float(ms))

    health['rule_p50_ms'] = round(pct(rule_latencies, 0.5), 1) if rule_latencies else 0
    health['rule_p95_ms'] = round(pct(rule_latencies, 0.95), 1) if rule_latencies else 0
    health['llm_p50_ms'] = round(pct(llm_latencies, 0.5), 1) if llm_latencies else 0
    health['rule_samples'] = len(rule_latencies)
    health['llm_samples'] = len(llm_latencies)

    # --- Error control ---
    errors = load_json(WS_STATE / 'error-tracker.json', {'errors': []})
    items = errors.get('errors', [])
    windowed = []
    for err in items:
        ts = err.get('firstSeen') or err.get('lastSeen', '')
        try:
            dt = datetime.fromisoformat(str(ts).replace('Z', '+00:00'))
            naive = dt.replace(tzinfo=None) if dt.tzinfo else dt
            if naive >= cutoff:
                windowed.append(err)
        except Exception:
            windowed.append(err)

    health['total_errors'] = len(windowed)
    health['fixed_errors'] = sum(1 for e in windowed if e.get('fixApplied'))
    health['repeat_errors'] = sum(1 for e in windowed if int(e.get('count', 0)) >= 3)

    healing = load_json(WS_STATE / 'v6-healing-log.json', [])
    if isinstance(healing, list):
        health['healed'] = sum(1 for h in healing if h.get('success'))
    else:
        health['healed'] = 0

    total_fixable = max(health['total_errors'] + len(healing if isinstance(healing, list) else []), 1)
    health['fix_rate'] = round(ratio(health['fixed_errors'] + health['healed'], total_fixable), 3)

    # --- Cron health ---
    cron = load_json(WS_STATE / 'cron-governor-report.json', {'summary': {}})
    cs = cron.get('summary', {})
    health['cron_enabled'] = int(cs.get('enabled_jobs', 0))
    health['cron_erroring'] = int(cs.get('erroring_jobs', 0))

    return health


def score_latency(h: dict) -> float:
    score = 100.0
    rp50 = h.get('rule_p50_ms', 0)
    lp50 = h.get('llm_p50_ms', 0)
    if rp50 > 100:
        score -= min(30, (rp50 - 100) / 100 * 5)
    if lp50 > 5000:
        score -= min(40, (lp50 - 5000) / 1000 * 5)
    if h.get('rule_samples', 0) == 0 and h.get('llm_samples', 0) == 0:
        score = 50.0
    return round(clamp(score), 2)


def score_error_control(h: dict) -> float:
    fix_score = h.get('fix_rate', 0) * 100
    repeat_penalty = min(30, h.get('repeat_errors', 0) * 5)
    return round(clamp(fix_score * 0.7 + (100 - repeat_penalty) * 0.3), 2)


def score_infrastructure(h: dict) -> float:
    enabled = max(h.get('cron_enabled', 0), 1)
    err_rate = ratio(h.get('cron_erroring', 0), enabled)
    return round(clamp((1 - err_rate) * 100), 2)


# ═══════════════════════════════════════════════════════════════════════════
# Layer 3: Growth Metrics
# ═══════════════════════════════════════════════════════════════════════════

def collect_growth_metrics() -> dict:
    g: dict = {}

    # Knowledge
    if REASONING_DB.exists():
        try:
            conn = sqlite3.connect(str(REASONING_DB))
            g['reasoning_total'] = conn.execute('SELECT COUNT(*) FROM reasoning_logs').fetchone()[0]
            g['reasoning_high'] = conn.execute(
                "SELECT COUNT(*) FROM reasoning_logs WHERE confidence='high'").fetchone()[0]
            conn.close()
        except Exception:
            g['reasoning_total'] = 0
            g['reasoning_high'] = 0
    else:
        g['reasoning_total'] = 0
        g['reasoning_high'] = 0

    mem_db = WS_STATE / 'v6-memory-index.db'
    if mem_db.exists():
        try:
            conn = sqlite3.connect(str(mem_db))
            tables = [r[0] for r in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
            if 'memory_entries' in tables:
                g['memory_entries'] = conn.execute('SELECT COUNT(*) FROM memory_entries').fetchone()[0]
            elif 'entries' in tables:
                g['memory_entries'] = conn.execute('SELECT COUNT(*) FROM entries').fetchone()[0]
            else:
                g['memory_entries'] = 0
            conn.close()
        except Exception:
            g['memory_entries'] = 0
    else:
        g['memory_entries'] = 0

    # Self-improvement
    reports_dir = WS_STATE / 'reflection-reports'
    g['reflection_reports'] = len(list(reports_dir.glob('reflection-*.md'))) if reports_dir.exists() else 0
    rule_cands = load_json(WS_STATE / 'rule-candidates.json', {})
    g['rule_candidates'] = rule_cands.get('count', 0) if isinstance(rule_cands, dict) else 0

    # Pattern learning
    patterns = load_json(WS_STATE / 'pattern-library.json', {'patterns': []}).get('patterns', [])
    g['patterns_high_conf'] = sum(1 for p in patterns if p.get('confidence') == 'high')
    rules = load_json(WS_STATE / 'v6-rules.json', {'rules': []})
    rules_list = rules.get('rules', []) if isinstance(rules, dict) else []
    g['auto_rules_active'] = sum(1 for r in rules_list if r.get('status') == 'active')

    return g


def score_knowledge(g: dict) -> float:
    rs = min(g.get('reasoning_total', 0), 300) / 300 * 50
    rh = min(g.get('reasoning_high', 0), 100) / 100 * 25
    mem = min(g.get('memory_entries', 0), 200) / 200 * 25
    return round(clamp(rs + rh + mem), 2)


def score_self_improvement(g: dict) -> float:
    refl = min(g.get('reflection_reports', 0), 10) / 10 * 50
    rules = min(g.get('rule_candidates', 0), 20) / 20 * 50
    return round(clamp(refl + rules), 2)


def score_pattern_learning(g: dict) -> float:
    phc = min(g.get('patterns_high_conf', 0), 30) / 30 * 50
    ar = min(g.get('auto_rules_active', 0), 20) / 20 * 50
    return round(clamp(phc + ar), 2)


# ═══════════════════════════════════════════════════════════════════════════
# Score Aggregation
# ═══════════════════════════════════════════════════════════════════════════

def compute_overall(dim_scores: dict[str, float], config: dict) -> float:
    dims_cfg = config.get('dimensions', {})
    total_weight = sum(d.get('weight', 0) for d in dims_cfg.values())
    if total_weight == 0:
        return 0.0
    score = 0.0
    for dim, cfg in dims_cfg.items():
        w = cfg.get('weight', 0) / total_weight
        score += dim_scores.get(dim, 0.0) * w
    return round(score, 2)


def grade_for(score: float) -> str:
    for threshold, grade in [(92, 'A+'), (88, 'A'), (84, 'A-'), (80, 'B+'),
                              (76, 'B'), (72, 'B-'), (68, 'C+'), (64, 'C')]:
        if score >= threshold:
            return grade
    return 'D'


def compute_ci(scores: list[float], confidence: float = 0.95) -> list[float]:
    if len(scores) <= 1:
        v = scores[0] if scores else 0.0
        return [round(v, 2), round(v, 2)]
    mean = statistics.mean(scores)
    std = statistics.stdev(scores)
    z = 1.96 if confidence >= 0.95 else 1.645
    margin = z * std / math.sqrt(len(scores))
    return [round(clamp(mean - margin), 2), round(clamp(mean + margin), 2)]


def compute_pass_at_k(results_per_test: dict[str, list[bool]], k: int = 2) -> dict[str, float]:
    scores: dict[str, float] = {}
    for tid, outcomes in results_per_test.items():
        n, c = len(outcomes), sum(outcomes)
        if n < k:
            scores[tid] = c / n if n else 0.0
        elif n - c < k:
            scores[tid] = 1.0
        else:
            scores[tid] = 1.0 - math.comb(n - c, k) / math.comb(n, k)
    return scores


# ═══════════════════════════════════════════════════════════════════════════
# Trend Analysis
# ═══════════════════════════════════════════════════════════════════════════

def load_previous_run() -> dict | None:
    runs = sorted(RUNS_DIR.glob('*.json'))
    if not runs:
        return None
    try:
        return json.loads(runs[-1].read_text(encoding='utf-8'))
    except Exception:
        return None


def compute_trend(current: dict, previous: dict | None) -> dict | None:
    if not previous:
        return None
    trend = {
        'overall_delta': round(current['overall_score'] - previous.get('overall_score', 0), 2),
        'previous_generated_at': previous.get('generated_at'),
        'dimension_deltas': {},
    }
    prev_dims = previous.get('dimension_scores', {})
    for dim, score in current['dimension_scores'].items():
        old = prev_dims.get(dim)
        if old is not None:
            trend['dimension_deltas'][dim] = round(score - old, 2)
    declining = [d for d, v in trend['dimension_deltas'].items() if v < -5]
    if declining:
        trend['degradation_alert'] = declining
    return trend


# ═══════════════════════════════════════════════════════════════════════════
# LLM Judge (optional)
# ═══════════════════════════════════════════════════════════════════════════

LLM_JUDGE_PROMPT = """你是 OpenClaw 智能度评估的裁判。请对以下评估结果做主观质量打分。

维度评分:
{dim_summary}

关键证据:
{evidence_summary}

请给出 0-100 的主观可信度评分和简短评语（一句话），严格 JSON 输出:
{{"judge_score": <0-100>, "comment": "<评语>"}}"""


def llm_judge(result: dict) -> dict | None:
    api_key = os.environ.get('OPENAI_API_KEY') or os.environ.get('DEEPSEEK_API_KEY', '')
    if not api_key:
        return None
    base = os.environ.get('OPENAI_API_BASE', 'https://api.deepseek.com')
    dim_lines = '\n'.join(f'  {k}: {v}' for k, v in result['dimension_scores'].items())
    ev_lines = '\n'.join(f'  {e["metric"]}: {e["value"]}' for e in result['evidence'][:10])
    prompt = LLM_JUDGE_PROMPT.format(dim_summary=dim_lines, evidence_summary=ev_lines)
    payload = json.dumps({
        'model': 'deepseek-chat',
        'messages': [{'role': 'user', 'content': prompt}],
        'temperature': 0.3, 'max_tokens': 200,
    }).encode()
    req = urllib.request.Request(
        f'{base}/v1/chat/completions', data=payload,
        headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {api_key}'},
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            body = json.loads(resp.read())
        text = body['choices'][0]['message']['content'].strip()
        if text.startswith('```'):
            text = text.split('\n', 1)[1].rsplit('```', 1)[0].strip()
        return json.loads(text)
    except Exception:
        return None


# ═══════════════════════════════════════════════════════════════════════════
# Markdown Report
# ═══════════════════════════════════════════════════════════════════════════

def build_markdown(result: dict) -> str:
    r = result
    grade_emoji = {'A+': '🏆', 'A': '🥇', 'A-': '🥈', 'B+': '🥉',
                   'B': '📈', 'B-': '📊', 'C+': '⚠️', 'C': '⚠️', 'D': '🚨'}
    lines = [
        f"# OpenClaw Smartness Eval v0.3.3 — {r['generated_at']}",
        '',
        f"> **{grade_emoji.get(r['grade'], '')} Overall: {r['overall_score']} ({r['grade']})** "
        f"| mode: {r['mode']} | tests: {r['sample_size']}",
        '',
    ]

    dims = r['dimension_scores']
    weakest = min(dims, key=lambda k: dims[k])
    strongest = max(dims, key=lambda k: dims[k])
    lines.append(f'**最强**: {strongest} ({dims[strongest]})')
    lines.append(f'**最弱**: {weakest} ({dims[weakest]}) ← 优先提升')
    lines.append('')

    dims_cfg = r.get('_config_dimensions', {})
    for layer_name, layer_label in [('functional', '功能测试 (70%)'),
                                     ('health', '系统健康 (20%)'),
                                     ('growth', '成长进化 (10%)')]:
        layer_dims = [d for d, c in dims_cfg.items() if c.get('layer') == layer_name]
        if not layer_dims:
            continue
        lines.append(f'## {layer_label}')
        lines.append('| 维度 | 分数 | 权重 | 趋势 |')
        lines.append('|------|------|------|------|')
        trend = r.get('trend_vs_last') or {}
        deltas = trend.get('dimension_deltas', {})
        for d in layer_dims:
            v = dims.get(d, 0)
            w = dims_cfg[d].get('weight', 0)
            delta = deltas.get(d)
            arrow = f' ({delta:+.1f})' if delta is not None else ''
            lines.append(f'| {d} | {v} | {w}% | {arrow} |')
        lines.append('')

    if r.get('trend_vs_last'):
        trend = r['trend_vs_last']
        lines.append(f"## 趋势 (vs {trend.get('previous_generated_at', '?')})")
        lines.append(f"- 总分变化: **{trend.get('overall_delta', 0):+.2f}**")
        degrading = trend.get('degradation_alert', [])
        if degrading:
            lines.append(f"- ⚠️ 退化维度: {', '.join(degrading)}")
        lines.append('')

    lines.append('## 关键证据')
    lines.append('| 指标 | 值 |')
    lines.append('|------|----|')
    for e in r['evidence']:
        lines.append(f"| {e['metric']} | {e['value']} |")

    passed_tests = sum(1 for t in r.get('task_results', []) if t['passed'])
    total_tests = len(r.get('task_results', []))
    lines.extend(['', f'## 测试结果: {passed_tests}/{total_tests} 通过'])
    failed = [t for t in r.get('task_results', []) if not t['passed']]
    if failed:
        for t in failed[:10]:
            notes = ', '.join(t.get('notes', []))
            lines.append(f"- ❌ {t['name']} ({t['id']}): {notes}")
    else:
        lines.append('- ✅ 全部通过')

    judge = r.get('llm_judge')
    if judge:
        lines.extend([
            '', '## LLM Judge',
            f"- 可信度: **{judge.get('judge_score', '?')}**",
            f"- 评语: {judge.get('comment', '')}",
        ])

    _sig = _skill_sig()
    lines.extend([
        '', '---',
        f"> Skill: **{_sig['skill']}** | Author: **{_sig['author']}** | "
        f"Integrity: `{_sig['integrity']}`", '',
    ])
    return '\n'.join(lines)


# ═══════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description='OpenClaw Smartness Eval v0.3.3')
    parser.add_argument('--mode', choices=['quick', 'standard', 'deep'], default='standard')
    parser.add_argument('--format', choices=['json', 'markdown'], default='json')
    parser.add_argument('--compare-last', action='store_true')
    parser.add_argument('--llm-judge', action='store_true')
    parser.add_argument('--workspace', type=str, help='Override workspace path')
    args = parser.parse_args()

    # Allow CLI override of workspace
    if args.workspace:
        global WORKSPACE, STATE_DIR, RUNS_DIR, REPORTS_DIR, WS_STATE
        global REASONING_DB, KERNEL_LOG_DB
        WORKSPACE = Path(args.workspace)
        STATE_DIR = WORKSPACE / 'state' / 'smartness-eval'
        RUNS_DIR = STATE_DIR / 'runs'
        REPORTS_DIR = STATE_DIR / 'reports'
        RUNS_DIR.mkdir(parents=True, exist_ok=True)
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        WS_STATE = WORKSPACE / 'state'
        REASONING_DB = WORKSPACE / '.reasoning' / 'reasoning-store.sqlite'
        KERNEL_LOG_DB = WS_STATE / 'v7-kernel-log.db'

    config = load_json(CONFIG_DIR / 'config.json', {})
    task_suite = load_json(CONFIG_DIR / 'task-suite.json', {'tests': []})
    tests = select_tests(task_suite, args.mode, config)
    repeat_count = int(config.get('modes', {}).get(args.mode, {}).get('repeat_count', 1))
    window_days = int(config.get('modes', {}).get(args.mode, {}).get('window_days', 7))

    # === Run functional tests ===
    all_results: list[list[dict]] = []
    for _ in range(repeat_count):
        all_results.append([evaluate_test(t) for t in tests])

    flat_results = [r for batch in all_results for r in batch]
    func_scores = compute_dimension_scores(flat_results, config)

    # === Collect health & growth metrics ===
    health = collect_health_metrics(window_days)
    growth = collect_growth_metrics()

    # === Compute health dimension scores ===
    health_scores = {
        'latency': score_latency(health),
        'error_control': score_error_control(health),
        'infrastructure': score_infrastructure(health),
    }

    # === Compute growth dimension scores ===
    growth_scores = {
        'knowledge': score_knowledge(growth),
        'self_improvement': score_self_improvement(growth),
        'pattern_learning': score_pattern_learning(growth),
    }

    # === Merge all dimension scores ===
    all_dim_scores = {**func_scores, **health_scores, **growth_scores}

    # Only keep dimensions defined in config
    dims_cfg = config.get('dimensions', {})
    dim_scores = {d: all_dim_scores.get(d, 0.0) for d in dims_cfg}

    # === Overall score ===
    overall = compute_overall(dim_scores, config)

    # === CI from repeated runs ===
    overall_per_repeat: list[float] = []
    for batch in all_results:
        batch_func = compute_dimension_scores(batch, config)
        batch_all = {**batch_func, **health_scores, **growth_scores}
        batch_dim = {d: batch_all.get(d, 0.0) for d in dims_cfg}
        overall_per_repeat.append(compute_overall(batch_dim, config))

    ci = compute_ci(overall_per_repeat if len(overall_per_repeat) > 1 else [overall],
                    config.get('confidence_level', 0.95))

    # === pass@k ===
    results_per_test: dict[str, list[bool]] = {}
    for r in flat_results:
        results_per_test.setdefault(r['id'], []).append(r['passed'])
    passk = compute_pass_at_k(results_per_test) if repeat_count > 1 else None

    # === Build evidence ===
    evidence: list[dict] = [
        {'metric': 'functional_test_pass_rate',
         'value': f"{sum(1 for r in flat_results if r['passed'])}/{len(flat_results)}"},
        {'metric': 'rule_p50_ms', 'value': health.get('rule_p50_ms', 0)},
        {'metric': 'rule_p95_ms', 'value': health.get('rule_p95_ms', 0)},
        {'metric': 'llm_p50_ms', 'value': health.get('llm_p50_ms', 0)},
        {'metric': 'error_fix_rate', 'value': f"{health.get('fix_rate', 0) * 100:.1f}%"},
        {'metric': 'repeat_errors', 'value': health.get('repeat_errors', 0)},
        {'metric': 'cron_enabled', 'value': health.get('cron_enabled', 0)},
        {'metric': 'cron_erroring', 'value': health.get('cron_erroring', 0)},
        {'metric': 'reasoning_store', 'value': growth.get('reasoning_total', 0)},
        {'metric': 'reasoning_high_conf', 'value': growth.get('reasoning_high', 0)},
        {'metric': 'memory_entries', 'value': growth.get('memory_entries', 0)},
        {'metric': 'reflection_reports', 'value': growth.get('reflection_reports', 0)},
        {'metric': 'patterns_high_conf', 'value': growth.get('patterns_high_conf', 0)},
        {'metric': 'auto_rules_active', 'value': growth.get('auto_rules_active', 0)},
    ]

    # === Build result ===
    generated_at = datetime.now().isoformat(timespec='seconds')
    result: dict = {
        'meta': _skill_sig(),
        'generated_at': generated_at,
        'mode': args.mode,
        'overall_score': overall,
        'grade': grade_for(overall),
        'confidence_interval': ci,
        'dimension_scores': dim_scores,
        '_config_dimensions': dims_cfg,
        'task_results': flat_results,
        'health_metrics': health,
        'growth_metrics': growth,
        'evidence': evidence,
        'sample_size': len(flat_results),
    }

    # === Trend ===
    previous = load_previous_run() if args.compare_last else None
    result['trend_vs_last'] = compute_trend(result, previous)

    if passk:
        result['pass_at_k'] = passk

    # === LLM Judge ===
    if args.llm_judge:
        judge = llm_judge(result)
        if judge:
            result['llm_judge'] = judge

    # === Save ===
    ts = datetime.now().strftime('%Y%m%d-%H%M%S')
    run_path = RUNS_DIR / f'{ts}.json'
    report_path = REPORTS_DIR / f'{datetime.now().strftime("%Y-%m-%d")}.md'
    run_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    report_path.write_text(build_markdown(result), encoding='utf-8')

    history_row = {
        'generated_at': generated_at,
        'mode': args.mode,
        'overall_score': overall,
        'grade': result['grade'],
        'dimension_scores': dim_scores,
        'file': str(run_path),
    }
    with open(STATE_DIR / 'history.jsonl', 'a', encoding='utf-8') as fh:
        fh.write(json.dumps(history_row, ensure_ascii=False) + '\n')

    # === Output ===
    if args.format == 'markdown':
        print(build_markdown(result))
    else:
        # Remove internal config from JSON output
        output = {k: v for k, v in result.items() if not k.startswith('_')}
        print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
