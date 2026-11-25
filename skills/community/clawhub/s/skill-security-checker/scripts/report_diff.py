#!/usr/bin/env python3
"""
Version Security Diff - compare two full-report JSONs (old vs new).

Outputs added / removed / unchanged risk items. Newly introduced risks are
marked red in the HTML view — a gate for "what risk did this upgrade introduce".

Pure stdlib. Author: njskills@agent.qq.com
Version: 1.0.0
"""

import json
from pathlib import Path
from datetime import datetime

VERSION = "1.0.0"
SEV_ORDER = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3, 'info': 4}
SEV_LABEL = {'critical': '严重', 'high': '高危', 'medium': '中等', 'low': '低', 'info': '提示'}


def _fingerprint(result):
    """Stable identity of a finding: category+severity+file+line+pattern/message."""
    return '|'.join([
        str(result.get('category', '')),
        str(result.get('severity', '')),
        str(result.get('file', '')),
        str(result.get('line', '')),
        str(result.get('pattern', '') or result.get('message', '')),
    ])


def _load(path):
    data = json.loads(Path(path).read_text(encoding='utf-8'))
    if not isinstance(data, dict) or 'results' not in data:
        raise ValueError(f'不是有效的完整报告 JSON: {path}')
    return data


def diff_reports(old_report, new_report):
    """Compute a structured diff between two report dicts. Never raises."""
    old = {_fingerprint(r): r for r in old_report.get('results', [])}
    new = {_fingerprint(r): r for r in new_report.get('results', [])}

    added_keys = set(new) - set(old)
    removed_keys = set(old) - set(new)
    common_keys = set(new) & set(old)

    def sort_key(k):
        return SEV_ORDER.get(str(new[k].get('severity', '')), 9)

    added = sorted([new[k] for k in added_keys], key=lambda r: SEV_ORDER.get(str(r.get('severity', '')), 9))
    removed = sorted([old[k] for k in removed_keys], key=lambda r: SEV_ORDER.get(str(r.get('severity', '')), 9))
    common = sorted([new[k] for k in common_keys], key=lambda r: SEV_ORDER.get(str(r.get('severity', '')), 9))

    old_score = old_report.get('score')
    new_score = new_report.get('score')

    return {
        'meta': {
            'tool': 'skill-security-checker',
            'version': VERSION,
            'generated_at': datetime.now().isoformat(timespec='seconds'),
            'old_version': (old_report.get('meta', {}) or {}).get('version', ''),
            'new_version': (new_report.get('meta', {}) or {}).get('version', ''),
            'old_scan_time': (old_report.get('meta', {}) or {}).get('scan_time', ''),
            'new_scan_time': (new_report.get('meta', {}) or {}).get('scan_time', ''),
        },
        'summary': {
            'added': len(added),
            'removed': len(removed),
            'unchanged': len(common),
            'old_score': old_score,
            'new_score': new_score,
            'verdict': 'risk_increased' if added else ('risk_reduced' if removed else 'no_change'),
        },
        'added': added,
        'removed': removed,
        'unchanged': common,
    }


def to_html(diff, output_path=None):
    """Render diff to a single HTML file; added risks marked red."""
    def rows(items, mark):
        out = ''
        for r in items:
            sev = str(r.get('severity', ''))
            label = SEV_LABEL.get(sev, sev)
            out += (f'<tr class="{mark}"><td>{_e(label)}</td><td>{_e(r.get("category", ""))}</td>'
                    f'<td>{_e(r.get("file", ""))}:{_e(r.get("line", ""))}</td>'
                    f'<td>{_e(r.get("message", ""))}</td></tr>')
        return out

    s = diff['summary']
    verdict_text = {
        'risk_increased': '本次更新新增了安全风险，建议谨慎升级',
        'risk_reduced': '本次更新消除了部分风险',
        'no_change': '本次更新风险项无变化',
    }[s['verdict']]
    verdict_class = 'bad' if s['verdict'] == 'risk_increased' else ('good' if s['verdict'] == 'risk_reduced' else 'plain')

    html = f'''<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>版本安全 Diff</title>
<style>
  body {{ font-family: -apple-system, "Microsoft YaHei", sans-serif; margin: 0; padding: 28px; color: #1a1a1a; }}
  .page {{ max-width: 1000px; margin: 0 auto; }}
  h1 {{ font-size: 20px; }} h2 {{ font-size: 15px; margin-top: 26px; }}
  .banner {{ border-radius: 10px; padding: 14px 18px; font-size: 15px; margin-bottom: 18px; }}
  .banner.bad {{ background: #fdecec; color: #c0392b; }}
  .banner.good {{ background: #eaf7ee; color: #1e8449; }}
  .banner.plain {{ background: #f4f6f8; color: #555; }}
  table {{ border-collapse: collapse; width: 100%; font-size: 13px; }}
  th, td {{ border: 1px solid #e5e5e5; padding: 8px 10px; text-align: left; }}
  th {{ background: #fafafa; }}
  tr.added {{ background: #fdecec; color: #a93226; }}
  tr.removed {{ background: #eaf7ee; color: #1e8449; }}
  .meta {{ color: #888; font-size: 12px; }}
</style></head><body><div class="page">
  <h1>版本安全 Diff</h1>
  <div class="meta">{_e(diff['meta']['old_version'])} ({_e(s['old_score'])}) → {_e(diff['meta']['new_version'])} ({_e(s['new_score'])}) ｜ 生成 {_e(diff['meta']['generated_at'])}</div>
  <div class="banner {verdict_class}">{_e(verdict_text)}</div>
  <p>新增 <b>{s['added']}</b> 项 ｜ 消失 <b>{s['removed']}</b> 项 ｜ 未变 <b>{s['unchanged']}</b> 项</p>
  <h2 style="color:#c0392b">新增风险（红色）</h2>
  <table><tr><th>严重度</th><th>类别</th><th>位置</th><th>说明</th></tr>
  {rows(diff['added'], 'added') or '<tr><td colspan="4">无</td></tr>'}</table>
  <h2 style="color:#1e8449">消失风险</h2>
  <table><tr><th>严重度</th><th>类别</th><th>位置</th><th>说明</th></tr>
  {rows(diff['removed'], 'removed') or '<tr><td colspan="4">无</td></tr>'}</table>
</div></body></html>'''
    if output_path:
        Path(output_path).write_text(html, encoding='utf-8')
    return html


def to_text(diff):
    s = diff['summary']
    lines = [
        "=" * 56,
        "  版本安全 Diff",
        "=" * 56,
        f"  {s['old_version']} ({s['old_score']}) → {s['new_version']} ({s['new_score']})",
        f"  新增 {s['added']} / 消失 {s['removed']} / 未变 {s['unchanged']}",
        "-" * 56,
    ]
    if diff['added']:
        lines.append("  🔴 新增风险:")
        for r in diff['added']:
            lines.append(f"    [{SEV_LABEL.get(str(r.get('severity','')), r.get('severity',''))}] "
                         f"{r.get('category','')} — {r.get('message','')}")
    if diff['removed']:
        lines.append("  🟢 消失风险:")
        for r in diff['removed']:
            lines.append(f"    [{SEV_LABEL.get(str(r.get('severity','')), r.get('severity',''))}] "
                         f"{r.get('category','')} — {r.get('message','')}")
    if not diff['added'] and not diff['removed']:
        lines.append("  风险项无变化")
    lines.append("=" * 56)
    return '\n'.join(lines)


def _e(text):
    import html as _html
    return _html.escape(str(text if text is not None else ''))


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser(description='Compare two full-report JSON files')
    p.add_argument('old_report', help='Old version report JSON')
    p.add_argument('new_report', help='New version report JSON')
    p.add_argument('-o', '--output', help='Output HTML file (else text to stdout)')
    p.add_argument('--json', action='store_true', help='Output structured JSON')
    a = p.parse_args()
    diff = diff_reports(_load(a.old_report), _load(a.new_report))
    if a.output:
        to_html(diff, a.output)
        print(f"Diff HTML 已生成：{a.output}")
    elif a.json:
        print(json.dumps(diff, ensure_ascii=False, indent=2))
    else:
        print(to_text(diff))
