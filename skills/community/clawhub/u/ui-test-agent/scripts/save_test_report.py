#!/usr/bin/env python3
"""
save_test_report.py — 将录制的 session 生成完整的 HTML 测试报告

特性：
  - 嵌入 Base64 截图，报告为单文件无外部依赖
  - 步骤时间轴展示，可折叠查看命令详情
  - 通过/失败/跳过步骤颜色标注
  - 汇总统计：总步骤数、耗时、通过率

用法:
    python save_test_report.py \
        --session <session_file.json> \
        --output <report.html> \
        --test-name "测试名称" \
        [--description "描述"] \
        [--tester "测试人"]
"""

import argparse
import base64
import json
import os
import sys
from datetime import datetime


def parse_args():
    parser = argparse.ArgumentParser(description="生成 HTML 测试报告")
    parser.add_argument("--session",     required=True,  help="session JSON 文件路径")
    parser.add_argument("--output",      required=True,  help="输出 HTML 报告路径")
    parser.add_argument("--test-name",   required=True,  help="测试用例名称")
    parser.add_argument("--description", default="",     help="测试描述")
    parser.add_argument("--tester",      default="Auto Agent", help="测试人")
    parser.add_argument("--base-url",    default="",     help="被测系统基础 URL")
    return parser.parse_args()


def load_session(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def embed_image(path: str) -> str:
    """将图片转为 base64 data URI，若文件不存在则返回占位符。"""
    if not path or not os.path.exists(path):
        return ""
    ext = os.path.splitext(path)[1].lower().lstrip(".")
    mime = {"jpg": "jpeg", "jpeg": "jpeg", "png": "png",
            "gif": "gif", "webp": "webp"}.get(ext, "png")
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    return f"data:image/{mime};base64,{data}"


def status_badge(status: str) -> str:
    colors = {"passed": "#22c55e", "failed": "#ef4444", "skipped": "#f59e0b"}
    labels = {"passed": "✅ 通过", "failed": "❌ 失败", "skipped": "⏭ 跳过"}
    color = colors.get(status, "#6b7280")
    label = labels.get(status, status.upper())
    return (f'<span style="background:{color};color:#fff;padding:2px 10px;'
            f'border-radius:12px;font-size:12px;font-weight:600">{label}</span>')


def render_step(step: dict, idx: int) -> str:
    num       = step["step_num"]
    desc      = step["description"]
    cmd       = step.get("command", "")
    status    = step.get("status", "passed")
    selector  = step.get("selector", "")
    inp_val   = step.get("input_value", "")
    url       = step.get("url", "")
    ts        = step.get("timestamp", "")
    error     = step.get("error_msg", "")
    shot_path = step.get("screenshot", "")
    img_src   = embed_image(shot_path)

    border_colors = {"passed": "#22c55e", "failed": "#ef4444", "skipped": "#f59e0b"}
    border = border_colors.get(status, "#6b7280")

    screenshot_html = ""
    if img_src:
        screenshot_html = f"""
        <div style="margin-top:12px">
          <img src="{img_src}" alt="step-{num}-screenshot"
               style="max-width:100%;border-radius:8px;border:1px solid #e2e8f0;
                      box-shadow:0 2px 8px rgba(0,0,0,.12);cursor:pointer"
               onclick="this.style.maxWidth=this.style.maxWidth==='100%'?'none':'100%'" />
          <div style="font-size:11px;color:#94a3b8;margin-top:4px">
            📸 {os.path.basename(shot_path) if shot_path else "截图"}
          </div>
        </div>"""

    meta_parts = []
    if url:
        meta_parts.append(f'<span>🌐 <code>{url}</code></span>')
    if selector:
        meta_parts.append(f'<span>🎯 选择器: <code>{selector}</code></span>')
    if inp_val:
        meta_parts.append(f'<span>⌨️ 输入值: <code>{inp_val}</code></span>')
    if ts:
        meta_parts.append(f'<span>🕐 {ts[:19].replace("T"," ")}</span>')
    meta_html = ('<div style="display:flex;flex-wrap:wrap;gap:12px;font-size:12px;'
                 f'color:#64748b;margin-top:6px">{"".join(meta_parts)}</div>' if meta_parts else "")

    error_html = ""
    if error:
        error_html = f"""
        <div style="background:#fef2f2;border:1px solid #fecaca;border-radius:6px;
                    padding:8px 12px;margin-top:8px;font-size:13px;color:#dc2626">
          ⚠️ {error}
        </div>"""

    return f"""
    <div id="step-{idx}" style="border-left:4px solid {border};background:#fff;
         border-radius:8px;padding:16px 20px;margin-bottom:16px;
         box-shadow:0 1px 4px rgba(0,0,0,.06)">
      <div style="display:flex;align-items:center;gap:12px;margin-bottom:4px">
        <span style="background:#f1f5f9;color:#475569;font-weight:700;font-size:13px;
                     border-radius:6px;padding:2px 8px;min-width:36px;text-align:center">
          #{num}
        </span>
        <span style="font-weight:600;font-size:15px;color:#1e293b;flex:1">{desc}</span>
        {status_badge(status)}
      </div>
      {meta_html}
      <details style="margin-top:10px">
        <summary style="cursor:pointer;font-size:13px;color:#6366f1;user-select:none">
          🖥 查看命令
        </summary>
        <pre style="background:#0f172a;color:#e2e8f0;padding:12px 16px;border-radius:6px;
                    font-size:12px;margin-top:8px;overflow-x:auto;white-space:pre-wrap">{cmd}</pre>
      </details>
      {error_html}
      {screenshot_html}
    </div>"""


def render_report(session: dict, test_name: str, description: str,
                  tester: str, base_url: str) -> str:
    steps     = session.get("steps", [])
    total     = len(steps)
    passed    = sum(1 for s in steps if s.get("status") == "passed")
    failed    = sum(1 for s in steps if s.get("status") == "failed")
    skipped   = total - passed - failed
    pass_rate = f"{passed/total*100:.1f}%" if total else "—"
    created   = session.get("created_at", "")[:19].replace("T", " ")
    generated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    status_color = "#22c55e" if failed == 0 else "#ef4444"
    status_label = "全部通过" if failed == 0 else f"{failed} 步失败"

    steps_html = "".join(render_step(s, i + 1) for i, s in enumerate(steps))

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>UI 测试报告 — {test_name}</title>
<style>
  *{{box-sizing:border-box;margin:0;padding:0}}
  body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
        background:#f8fafc;color:#1e293b;line-height:1.6}}
  code{{font-family:"Fira Code","Cascadia Code",Consolas,monospace;
        background:#f1f5f9;padding:1px 5px;border-radius:4px;font-size:.9em}}
  details>summary::-webkit-details-marker{{display:none}}
  details>summary::marker{{display:none}}
  @media print{{.no-print{{display:none}}}}
</style>
</head>
<body>
<!-- ===== HEADER ===== -->
<div style="background:linear-gradient(135deg,#1e293b 0%,#334155 100%);
            color:#fff;padding:32px 40px">
  <div style="max-width:960px;margin:0 auto">
    <div style="display:flex;align-items:center;gap:16px;margin-bottom:8px">
      <span style="font-size:28px">🧪</span>
      <h1 style="font-size:24px;font-weight:700">{test_name}</h1>
      <span style="background:{status_color};padding:4px 14px;border-radius:20px;
                   font-size:13px;font-weight:600;margin-left:auto">{status_label}</span>
    </div>
    <p style="color:#94a3b8;font-size:14px">{description}</p>
  </div>
</div>

<!-- ===== META INFO ===== -->
<div style="background:#fff;border-bottom:1px solid #e2e8f0;padding:0 40px">
  <div style="max-width:960px;margin:0 auto;display:flex;flex-wrap:wrap;gap:0">
    {"".join(f'''<div style="padding:14px 24px;border-right:1px solid #f1f5f9;text-align:center">
      <div style="font-size:11px;color:#94a3b8;text-transform:uppercase;letter-spacing:.5px">{k}</div>
      <div style="font-size:16px;font-weight:700;color:#1e293b;margin-top:2px">{v}</div>
    </div>''' for k, v in [
        ("总步骤", str(total)),
        ("通过", f'<span style="color:#22c55e">{passed}</span>'),
        ("失败", f'<span style="color:#ef4444">{failed}</span>'),
        ("跳过", f'<span style="color:#f59e0b">{skipped}</span>'),
        ("通过率", f'<span style="color:{status_color}">{pass_rate}</span>'),
        ("测试人", tester),
        ("开始时间", created or "—"),
        ("生成时间", generated),
    ])}
    {"" if not base_url else f'<div style="padding:14px 24px;text-align:center"><div style="font-size:11px;color:#94a3b8">被测系统</div><div style="font-size:14px;font-weight:600;color:#6366f1;margin-top:2px"><a href="{base_url}" target="_blank" style="color:inherit">{base_url}</a></div></div>'}
  </div>
</div>

<!-- ===== STEPS ===== -->
<div style="max-width:960px;margin:32px auto;padding:0 24px">
  <h2 style="font-size:16px;font-weight:700;color:#475569;margin-bottom:20px;
             text-transform:uppercase;letter-spacing:.5px">执行步骤</h2>
  {steps_html if steps_html else '<p style="color:#94a3b8;text-align:center;padding:40px">暂无步骤记录</p>'}
</div>

<!-- ===== FOOTER ===== -->
<div style="border-top:1px solid #e2e8f0;padding:20px 40px;text-align:center;
            font-size:12px;color:#94a3b8;margin-top:24px">
  由 <strong>ui-test-agent</strong> Skill 自动生成 · {generated}
</div>

<script>
  // 点击图片全屏预览
  document.querySelectorAll('img[alt*="screenshot"]').forEach(img => {{
    img.title = "点击切换缩放";
  }});
</script>
</body>
</html>"""


def main():
    args = parse_args()

    if not os.path.exists(args.session):
        print(f"❌ Session 文件不存在: {args.session}", file=sys.stderr)
        sys.exit(1)

    session = load_session(args.session)
    html    = render_report(session, args.test_name, args.description,
                            args.tester, args.base_url)

    out_dir = os.path.dirname(os.path.abspath(args.output))
    os.makedirs(out_dir, exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(html)

    steps  = session.get("steps", [])
    passed = sum(1 for s in steps if s.get("status") == "passed")
    failed = sum(1 for s in steps if s.get("status") == "failed")
    print(f"✅ HTML 测试报告已生成: {args.output}")
    print(f"   📊 共 {len(steps)} 步 | 通过 {passed} | 失败 {failed}")


if __name__ == "__main__":
    main()
