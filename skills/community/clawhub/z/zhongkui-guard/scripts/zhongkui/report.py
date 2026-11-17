from __future__ import annotations

import html
import json
from pathlib import Path

def write_report(data: dict, output: Path) -> None:
    lines = ["# 钟馗卫士报告", "", f"- 操作：`{html.escape(str(data.get('operation', 'unknown')))}`", f"- 状态：`{html.escape(str(data.get('status', 'unknown')))}`", "", "## 覆盖范围", "", "```json", json.dumps(data.get("coverage", {}), ensure_ascii=False, indent=2), "```", "", "## 发现项", ""]
    findings=data.get("findings", [])
    if findings:
        for item in findings:
            lines.extend([f"### {html.escape(item.get('rule_id',''))} · {html.escape(item.get('severity',''))}", "", f"- 位置：`{html.escape(str(item.get('location',{})))}`", f"- 证据：{html.escape(item.get('evidence_redacted',''))}", f"- 原因：{html.escape(item.get('reason',''))}", f"- 建议：{html.escape(item.get('recommendation',''))}", ""])
    else: lines.extend(["未返回风险 finding。此结果不代表绝对安全。", ""])
    lines.extend(["## 限制", ""] + [f"- {html.escape(str(x))}" for x in data.get("limitations", [])] + [""])
    output.parent.mkdir(parents=True, exist_ok=True); output.write_text("\n".join(lines), encoding="utf-8")
