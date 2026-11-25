#!/usr/bin/env python3
"""
Gate Audit Logger - append-only JSONL log for install-time security gates.

Records every guard-mode scan: timestamp / target / verdict / user decision.
Stored OUTSIDE the skill repo (default ~/.workbuddy/gate-audit/gate-log.jsonl)
so no forbidden file types (.log etc.) ever land in the repo (死规则13).

Zero external dependencies. 90-day retention view. Pure stdlib.
Author: njskills@agent.qq.com
"""

import os
import json
import hashlib
from pathlib import Path
from datetime import datetime, timedelta

# Log lives outside the repo — never pollute the skill package.
LOG_DIR = Path.home() / ".workbuddy" / "gate-audit"
LOG_PATH = LOG_DIR / "gate-log.jsonl"

RETENTION_DAYS = 90
VERSION = "1.0.0"

VERDICT_LABELS = {
    'clean': '干净',
    'suspicious': '可疑',
    'malicious': '恶意',
}


class GateLogger:
    """Append-only JSONL logger with summary view and 90-day retention."""

    def __init__(self, log_path=None):
        self.log_path = Path(log_path) if log_path else LOG_PATH
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

    def _fingerprint(self, target):
        """Short stable hash of the target path (privacy: no full path stored by default)."""
        return hashlib.sha256(str(target).encode('utf-8', 'replace')).hexdigest()[:12]

    def log(self, target, verdict, decision='pending', reason='', score=None,
            skill_name='', top3=None, full_path=False, meta=None):
        """Append one gate scan record. Returns the record dict."""
        record = {
            'ts': datetime.now().isoformat(timespec='seconds'),
            'target': str(target) if full_path else self._fingerprint(target),
            'target_name': skill_name or Path(str(target)).name,
            'verdict': verdict,
            'verdict_label': VERDICT_LABELS.get(verdict, verdict),
            'decision': decision,  # pending / allowed / blocked / cancelled
            'reason': reason,
            'score': score,
            'top3': top3 or [],
            'tool_version': (meta or {}).get('tool_version', ''),
        }
        if full_path:
            record['target_fp'] = self._fingerprint(target)
        with open(self.log_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(record, ensure_ascii=False) + '\n')
        return record

    def _iter_records(self):
        if not self.log_path.exists():
            return
        with open(self.log_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    yield json.loads(line)
                except Exception:
                    continue

    def records(self, days=RETENTION_DAYS, verdict=None, decision=None):
        """Return records within the retention window, optionally filtered."""
        cutoff = datetime.now() - timedelta(days=days)
        out = []
        for r in self._iter_records():
            try:
                ts = datetime.fromisoformat(r.get('ts', ''))
            except Exception:
                continue
            if ts < cutoff:
                continue
            if verdict and r.get('verdict') != verdict:
                continue
            if decision and r.get('decision') != decision:
                continue
            out.append(r)
        return out

    def summary(self, days=RETENTION_DAYS):
        """Aggregate summary view: counts by verdict / decision + recent items."""
        recs = self.records(days=days)
        by_verdict = {'clean': 0, 'suspicious': 0, 'malicious': 0}
        by_decision = {}
        for r in recs:
            v = r.get('verdict')
            if v in by_verdict:
                by_verdict[v] += 1
            d = r.get('decision', 'pending')
            by_decision[d] = by_decision.get(d, 0) + 1
        return {
            'window_days': days,
            'total': len(recs),
            'by_verdict': by_verdict,
            'by_decision': by_decision,
            'recent': recs[-10:],
            'log_path': str(self.log_path),
            'version': VERSION,
        }

    def prune(self, days=RETENTION_DAYS):
        """Drop records older than `days`. Returns number removed."""
        if not self.log_path.exists():
            return 0
        cutoff = datetime.now() - timedelta(days=days)
        kept = []
        removed = 0
        for r in self._iter_records():
            try:
                ts = datetime.fromisoformat(r.get('ts', ''))
            except Exception:
                removed += 1
                continue
            if ts < cutoff:
                removed += 1
                continue
            kept.append(r)
        if removed:
            tmp = self.log_path.with_suffix('.jsonl.tmp')
            with open(tmp, 'w', encoding='utf-8') as f:
                for r in kept:
                    f.write(json.dumps(r, ensure_ascii=False) + '\n')
            os.replace(str(tmp), str(self.log_path))
        return removed

    def export(self, output_path, days=RETENTION_DAYS):
        """Export records to a JSON file. Returns count exported."""
        recs = self.records(days=days)
        Path(output_path).write_text(
            json.dumps(recs, ensure_ascii=False, indent=2), encoding='utf-8')
        return len(recs)


def format_summary_text(summary):
    """Human-readable Chinese summary view (≤1 screen)."""
    lines = [
        "=" * 56,
        "  拦截日志摘要（装机审计）",
        "=" * 56,
        f"  统计窗口: 最近 {summary['window_days']} 天",
        f"  扫描总数: {summary['total']}",
        "-" * 56,
        f"  ✅ 干净: {summary['by_verdict'].get('clean', 0)}",
        f"  ⚠️ 可疑: {summary['by_verdict'].get('suspicious', 0)}",
        f"  🚫 恶意: {summary['by_verdict'].get('malicious', 0)}",
        "-" * 56,
        "  用户决定: " + ", ".join(
            f"{k}={v}" for k, v in sorted(summary['by_decision'].items())),
    ]
    if summary['recent']:
        lines.append("-" * 56)
        lines.append("  最近记录:")
        for r in summary['recent'][-5:]:
            lines.append(f"    [{r.get('ts', '')}] {r.get('verdict_label', '')} "
                         f"{r.get('target_name', '')} → {r.get('decision', '')}")
    lines.append("=" * 56)
    lines.append(f"  日志位置: {summary['log_path']}")
    return '\n'.join(lines)


def log_gate_scan(target, verdict, decision='pending', reason='', score=None,
                  skill_name='', top3=None, full_path=False):
    """Convenience one-shot logger for gate mode."""
    return GateLogger().log(target, verdict, decision, reason, score,
                            skill_name, top3, full_path)


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser(description='Guard-mode audit log viewer')
    p.add_argument('--summary', action='store_true', help='Show summary view')
    p.add_argument('--days', type=int, default=RETENTION_DAYS, help='Retention window (default 90)')
    p.add_argument('--prune', action='store_true', help='Drop records older than --days')
    p.add_argument('--export', help='Export records to a JSON file')
    p.add_argument('--json', action='store_true', help='Output summary as JSON')
    a = p.parse_args()
    logger = GateLogger()
    if a.prune:
        n = logger.prune(days=a.days)
        print(f"已清理 {n} 条超期记录")
    if a.export:
        n = logger.export(a.export, days=a.days)
        print(f"已导出 {n} 条记录到 {a.export}")
    s = logger.summary(days=a.days)
    print(json.dumps(s, ensure_ascii=False, indent=2) if a.json else format_summary_text(s))
