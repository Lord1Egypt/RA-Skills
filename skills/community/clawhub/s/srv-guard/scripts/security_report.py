#!/usr/bin/env python3
"""security_report.py — 生成 HTML 安全报告

用法:
    python security_report.py --scan scan-result.json [--fix fix-result.json] [--monitor monitor-result.json] [--defend defend-result.json] --output report.html [--target name]

基于 assets/report-template.html 生成报告。
"""

import argparse
import html
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common
from _common import emit_json, log, read_resource


def sev_badge(sev):
    return f'<span class="badge {html.escape(sev)}">{html.escape(sev)}</span>'


def esc(s):
    return html.escape(str(s)) if s is not None else ""


def load_json(path):
    if not path or not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def scan_table(scan):
    if not scan:
        return '<p class="empty">未提供扫描结果</p>'
    findings = scan.get("findings", [])
    if not findings:
        return '<p class="ok">未发现漏洞</p>'
    rows = []
    for fnd in findings:
        rows.append(
            f"<tr><td>{sev_badge(fnd.get('severity',''))}</td>"
            f"<td>{esc(fnd.get('id'))}</td><td>{esc(fnd.get('title'))}</td>"
            f"<td>{esc(fnd.get('scope'))}</td>"
            f"<td class='ev'>{esc(fnd.get('evidence'))}</td>"
            f"<td>{'是' if fnd.get('auto_fixable') else '否'}</td></tr>")
    return ("<table><thead><tr><th>严重度</th><th>ID</th><th>标题</th>"
            "<th>范围</th><th>证据</th><th>可自动修复</th></tr></thead><tbody>"
            + "".join(rows) + "</tbody></table>")


def fix_table(fix):
    if not fix:
        return '<p class="empty">未执行修复</p>'
    if fix.get("status") == "requires_privilege":
        return ("<p class='warn'><strong>修复未执行（权限不足）:</strong> "
                + esc(fix.get("error", "")) + "</p>")
    results = fix.get("results", [])
    if not results:
        return '<p class="empty">无修复记录</p>'
    rows = []
    for r in results:
        cmds = "<br>".join(esc(c) for c in r.get("commands", []))
        rb = "<br>".join(esc(c) for c in r.get("rollback_commands", []))
        st = r.get("status", "")
        stc = "ok" if st == "fixed" else ("warn" if st in ("skipped", "would_fix") else "")
        rows.append(
            f"<tr><td class='{stc}'>{esc(st)}</td><td>{esc(r.get('item_id'))}</td>"
            f"<td class='ev'>{cmds}</td><td class='ev'>{rb}</td>"
            f"<td>{esc(r.get('message'))}</td></tr>")
    return ("<table><thead><tr><th>状态</th><th>项</th><th>命令</th>"
            "<th>回滚</th><th>说明</th></tr></thead><tbody>"
            + "".join(rows) + "</tbody></table>"
            + f"<p class='meta'>模式: {'dry-run' if fix.get('dry_run') else 'APPLIED'} | "
            f"汇总: {esc(fix.get('summary'))}</p>")


def monitor_table(mon):
    if not mon:
        return '<p class="empty">未执行攻击感知</p>'
    events = mon.get("events", [])
    if not events:
        return '<p class="ok">未检测到攻击事件</p>'
    rows = []
    for ev in events[:100]:
        ev_lines = "<br>".join(esc(e) for e in ev.get("evidence", [])[:3])
        rows.append(
            f"<tr><td>{sev_badge(ev.get('severity',''))}</td>"
            f"<td>{esc(ev.get('type'))}</td><td>{esc(ev.get('source_ip'))}</td>"
            f"<td class='ev'>{ev_lines}</td></tr>")
    return ("<table><thead><tr><th>严重度</th><th>类型</th><th>来源 IP</th>"
            "<th>证据</th></tr></thead><tbody>" + "".join(rows) + "</tbody></table>"
            + f"<p class='meta'>窗口: {esc(mon.get('window'))} | "
            f"分析日志: {esc(mon.get('logs_analyzed'))}</p>")


def defend_table(defend):
    if not defend:
        return '<p class="empty">未执行防御操作</p>'
    parts = [f"<p>动作: <strong>{esc(defend.get('action'))}</strong> | "
             f"状态: {esc(defend.get('status'))} | "
             f"模式: {'dry-run' if defend.get('dry_run') else 'APPLIED'}</p>"]
    blocked = defend.get("blocked_ips", [])
    if blocked:
        rows = "".join(
            f"<tr><td>{esc(b.get('ip'))}</td><td>{esc(b.get('reason'))}</td>"
            f"<td>{sev_badge(b.get('severity',''))}</td></tr>" for b in blocked)
        parts.append("<table><thead><tr><th>封禁 IP</th><th>原因</th><th>严重度</th>"
                     "</tr></thead><tbody>" + rows + "</tbody></table>")
    skipped = defend.get("skipped_ips", [])
    if skipped:
        rows = "".join(
            f"<tr><td>{esc(s.get('ip'))}</td><td>{esc(s.get('reason'))}</td></tr>" for s in skipped)
        parts.append("<p><strong>跳过（未封禁）:</strong></p>"
                     "<table><thead><tr><th>IP</th><th>原因</th></tr></thead><tbody>"
                     + rows + "</tbody></table>")
    ops = defend.get("operations", [])
    if ops:
        rows = "".join(
            f"<tr><td>{esc(o.get('op'))}</td><td class='ev'>{esc(o.get('command'))}</td>"
            f"<td>{'是' if o.get('applied') else '否（dry-run/失败）'}</td></tr>" for o in ops)
        parts.append("<p><strong>加固操作:</strong></p>"
                     "<table><thead><tr><th>操作</th><th>命令</th><th>已生效</th></tr></thead><tbody>"
                     + rows + "</tbody></table>")
    rb = defend.get("rollback_commands", [])
    if rb:
        parts.append("<p><strong>回滚命令:</strong></p><pre class='ev'>"
                     + "<br>".join(esc(c) for c in rb) + "</pre>")
    baks = defend.get("backup_files", [])
    if baks:
        parts.append("<p class='meta'>备份文件: " + esc(", ".join(baks)) + "</p>")
    warns = defend.get("warnings", [])
    if warns:
        parts.append("<p class='warn'><strong>需人工注意:</strong></p><ul>"
                     + "".join(f"<li>{esc(w)}</li>" for w in warns) + "</ul>")
    return "".join(parts)


def main():
    parser = argparse.ArgumentParser(description="生成 HTML 安全报告")
    parser.add_argument("--scan", help="scan-result.json")
    parser.add_argument("--fix", help="fix-result.json")
    parser.add_argument("--monitor", help="monitor-result.json")
    parser.add_argument("--defend", help="defend-result.json")
    parser.add_argument("--output", required=True, help="输出 HTML 路径")
    parser.add_argument("--target", default="unknown", help="目标名称")
    args = parser.parse_args()

    if not args.scan:
        log("至少需要 --scan", "ERROR")
        sys.exit(2)

    scan = load_json(args.scan)
    fix = load_json(args.fix)
    mon = load_json(args.monitor)
    defend = load_json(args.defend)

    template = read_resource("assets/report-template.html")

    sev = scan.get("summary", {}) if scan else {}
    replacements = {
        "{{TARGET}}": esc(args.target),
        "{{TIMESTAMP}}": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
        "{{SUM_CRITICAL}}": str(sev.get("CRITICAL", 0)),
        "{{SUM_HIGH}}": str(sev.get("HIGH", 0)),
        "{{SUM_MEDIUM}}": str(sev.get("MEDIUM", 0)),
        "{{SUM_LOW}}": str(sev.get("LOW", 0)),
        "{{SUM_INFO}}": str(sev.get("INFO", 0)),
        "{{SCAN_TABLE}}": scan_table(scan),
        "{{FIX_TABLE}}": fix_table(fix),
        "{{MONITOR_TABLE}}": monitor_table(mon),
        "{{DEFEND_TABLE}}": defend_table(defend),
    }
    out = template
    for k, v in replacements.items():
        out = out.replace(k, v)

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(out)
    log(f"报告已生成: {args.output}")
    emit_json({"status": "success", "output": args.output,
               "target": args.target, "timestamp": replacements["{{TIMESTAMP}}"]})


if __name__ == "__main__":
    main()
