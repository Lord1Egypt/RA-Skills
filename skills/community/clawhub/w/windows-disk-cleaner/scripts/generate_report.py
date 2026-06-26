#!/usr/bin/env python3
"""
Windows 磁盘清理报告生成器
读取 scan_result.json，生成交互式 HTML 报告。
用户在报告中勾选要清理的项目，页面生成对应的 PowerShell 命令。

用法：
    python generate_report.py scan_result.json -o cleanup_report.html
"""

import json
import sys
import os
from datetime import datetime

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>磁盘清理报告 - {drive} 盘</title>
<style>
  :root {{
    --bg: #0f1117;
    --card: #1a1d27;
    --border: #2a2d3a;
    --text: #e4e4e7;
    --text-dim: #8b8d98;
    --green: #22c55e;
    --green-bg: rgba(34,197,94,0.1);
    --yellow: #eab308;
    --yellow-bg: rgba(234,179,8,0.1);
    --red: #ef4444;
    --blue: #3b82f6;
    --blue-bg: rgba(59,130,246,0.12);
    --accent: #818cf8;
  }}
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: var(--bg); color: var(--text);
    line-height: 1.6; padding: 20px; max-width: 1100px; margin: 0 auto;
  }}
  h1 {{ font-size: 1.5rem; margin-bottom: 4px; }}
  .subtitle {{ color: var(--text-dim); font-size: 0.85rem; margin-bottom: 24px; }}

  /* 概览卡片 */
  .overview {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px; margin-bottom: 28px; }}
  .stat-card {{
    background: var(--card); border: 1px solid var(--border); border-radius: 10px; padding: 16px;
  }}
  .stat-label {{ color: var(--text-dim); font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.05em; }}
  .stat-value {{ font-size: 1.5rem; font-weight: 700; margin-top: 4px; }}
  .stat-value.green {{ color: var(--green); }}
  .stat-value.yellow {{ color: var(--yellow); }}
  .stat-value.blue {{ color: var(--blue); }}

  /* 进度条 */
  .disk-bar {{ background: var(--border); border-radius: 6px; height: 18px; overflow: hidden; margin: 8px 0; position: relative; }}
  .disk-bar-fill {{ height: 100%; border-radius: 6px; transition: width 0.5s; }}
  .disk-bar-label {{ position: absolute; right: 8px; top: 0; font-size: 0.72rem; line-height: 18px; color: var(--text); }}

  /* 分类区块 */
  .section {{ margin-bottom: 28px; }}
  .section-header {{
    display: flex; align-items: center; gap: 10px;
    padding: 12px 16px; border-radius: 10px 10px 0 0; font-weight: 600; font-size: 0.95rem;
  }}
  .section-header.safe {{ background: var(--green-bg); color: var(--green); }}
  .section-header.review {{ background: var(--yellow-bg); color: var(--yellow); }}

  .item-list {{ border: 1px solid var(--border); border-top: none; border-radius: 0 0 10px 10px; overflow: hidden; }}
  .item {{
    display: grid; grid-template-columns: 40px 1fr 120px;
    align-items: center; padding: 10px 16px;
    border-bottom: 1px solid var(--border); transition: background 0.15s;
  }}
  .item:last-child {{ border-bottom: none; }}
  .item:hover {{ background: rgba(255,255,255,0.02); }}
  .item label {{ cursor: pointer; }}
  .item-info {{ display: flex; flex-direction: column; }}
  .item-name {{ font-weight: 500; font-size: 0.9rem; }}
  .item-desc {{ color: var(--text-dim); font-size: 0.78rem; }}
  .item-size {{ text-align: right; font-weight: 600; font-family: 'SF Mono', monospace; font-size: 0.88rem; }}

  /* 大文件表格 */
  .file-table {{ width: 100%; border-collapse: collapse; font-size: 0.82rem; }}
  .file-table th {{ text-align: left; color: var(--text-dim); padding: 8px 12px; border-bottom: 1px solid var(--border); font-weight: 500; }}
  .file-table td {{ padding: 8px 12px; border-bottom: 1px solid var(--border); }}
  .file-table tr:hover {{ background: rgba(255,255,255,0.02); }}
  .file-path {{ color: var(--text-dim); font-family: monospace; font-size: 0.75rem; word-break: break-all; }}

  /* 操作区 */
  .actions {{
    position: sticky; bottom: 0; background: var(--card); border: 1px solid var(--border);
    border-radius: 12px; padding: 16px 20px; margin-top: 20px;
    display: flex; align-items: center; justify-content: space-between; gap: 16px;
    box-shadow: 0 -4px 20px rgba(0,0,0,0.3);
  }}
  .actions-info {{ font-size: 0.9rem; }}
  .actions-info strong {{ color: var(--accent); font-size: 1.1rem; }}
  .btn {{
    padding: 10px 24px; border: none; border-radius: 8px; font-weight: 600;
    cursor: pointer; font-size: 0.88rem; transition: all 0.15s;
  }}
  .btn-primary {{ background: var(--accent); color: #fff; }}
  .btn-primary:hover {{ filter: brightness(1.15); }}
  .btn-copy {{ background: var(--border); color: var(--text); }}
  .btn-copy:hover {{ background: #3a3d4a; }}

  /* 命令弹窗 */
  .modal-overlay {{
    display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
    background: rgba(0,0,0,0.7); z-index: 100; justify-content: center; align-items: center;
  }}
  .modal-overlay.active {{ display: flex; }}
  .modal {{
    background: var(--card); border: 1px solid var(--border); border-radius: 12px;
    padding: 24px; width: 90%; max-width: 700px; max-height: 80vh; overflow-y: auto;
  }}
  .modal h2 {{ margin-bottom: 12px; font-size: 1.1rem; }}
  .modal pre {{
    background: var(--bg); border: 1px solid var(--border); border-radius: 8px;
    padding: 16px; overflow-x: auto; font-size: 0.82rem; line-height: 1.5;
    white-space: pre-wrap; word-break: break-all;
  }}
  .modal .btn {{ margin-top: 16px; }}

  input[type="checkbox"] {{
    width: 16px; height: 16px; accent-color: var(--accent); cursor: pointer;
  }}

  @media (max-width: 600px) {{
    .item {{ grid-template-columns: 32px 1fr 80px; padding: 8px 10px; }}
    .overview {{ grid-template-columns: 1fr 1fr; }}
  }}
</style>
</head>
<body>

<h1>🧹 磁盘清理报告 — {drive} 盘</h1>
<p class="subtitle">扫描时间: {scan_time} | 用户: {username}</p>

<!-- 概览 -->
<div class="overview">
  <div class="stat-card">
    <div class="stat-label">磁盘总容量</div>
    <div class="stat-value">{total_display}</div>
  </div>
  <div class="stat-card">
    <div class="stat-label">已用空间 ({used_percent}%)</div>
    <div class="stat-value" style="color:{used_color}">{used_display}</div>
    <div class="disk-bar">
      <div class="disk-bar-fill" style="width:{used_percent}%;background:{used_color}"></div>
      <div class="disk-bar-label">{used_percent}%</div>
    </div>
  </div>
  <div class="stat-card">
    <div class="stat-label">可用空间</div>
    <div class="stat-value green">{free_display}</div>
  </div>
  <div class="stat-card">
    <div class="stat-label">潜在可释放</div>
    <div class="stat-value blue">{potential_display}</div>
  </div>
</div>

<!-- 安全删除项 -->
<div class="section">
  <div class="section-header safe">🟢 安全删除项 — 共 {safe_display}</div>
  <div class="item-list" id="safe-list">
    {safe_items_html}
  </div>
</div>

<!-- 需确认项 -->
<div class="section">
  <div class="section-header review">🟡 需确认项 — 共 {review_display}</div>
  <div class="item-list" id="review-list">
    {review_items_html}
  </div>
</div>

<!-- 大文件列表 -->
{large_files_section}

<!-- 底部操作栏 -->
<div class="actions">
  <div class="actions-info">
    已选择 <strong id="selected-count">0</strong> 项，共 <strong id="selected-size">0 B</strong>
  </div>
  <div>
    <button class="btn btn-primary" onclick="generateCommands()">生成清理命令</button>
  </div>
</div>

<!-- 命令弹窗 -->
<div class="modal-overlay" id="modal">
  <div class="modal">
    <h2>📋 PowerShell 清理命令</h2>
    <p style="color:var(--text-dim);font-size:0.82rem;margin-bottom:12px">
      复制以下命令到 <b>管理员权限的 PowerShell</b> 中执行。建议先检查内容再运行。
    </p>
    <pre id="commands-output"></pre>
    <button class="btn btn-copy" onclick="copyCommands()">📋 复制到剪贴板</button>
    <button class="btn btn-copy" onclick="closeModal()" style="margin-left:8px">关闭</button>
  </div>
</div>

<script>
const itemData = {items_json};

function updateSelection() {{
  let count = 0, bytes = 0;
  document.querySelectorAll('input[data-size]').forEach(cb => {{
    if (cb.checked) {{
      count++;
      const s = parseInt(cb.dataset.size);
      if (s > 0) bytes += s;
    }}
  }});
  document.getElementById('selected-count').textContent = count;
  document.getElementById('selected-size').textContent = formatSize(bytes);
}}

function formatSize(bytes) {{
  if (bytes >= 1073741824) return (bytes / 1073741824).toFixed(2) + ' GB';
  if (bytes >= 1048576) return (bytes / 1048576).toFixed(2) + ' MB';
  if (bytes >= 1024) return (bytes / 1024).toFixed(2) + ' KB';
  return bytes + ' B';
}}

function selectAllSafe() {{
  document.querySelectorAll('#safe-list input[type=checkbox]').forEach(cb => {{ cb.checked = true; }});
  updateSelection();
}}

function generateCommands() {{
  const cmds = [];
  document.querySelectorAll('input[data-cmd]').forEach(cb => {{
    if (cb.checked && cb.dataset.cmd) {{
      cmds.push('# ' + cb.dataset.name);
      cmds.push(cb.dataset.cmd);
      cmds.push('');
    }}
  }});
  if (cmds.length === 0) {{
    alert('请先勾选要清理的项目');
    return;
  }}
  document.getElementById('commands-output').textContent = cmds.join('\n');
  document.getElementById('modal').classList.add('active');
}}

function copyCommands() {{
  const text = document.getElementById('commands-output').textContent;
  navigator.clipboard.writeText(text).then(() => {{
    const btn = event.target;
    btn.textContent = '✅ 已复制';
    setTimeout(() => btn.textContent = '📋 复制到剪贴板', 2000);
  }});
}}

function closeModal() {{
  document.getElementById('modal').classList.remove('active');
}}

document.addEventListener('change', e => {{
  if (e.target.matches('input[type=checkbox]')) updateSelection();
}});

// 初始选中所有安全项
selectAllSafe();
</script>
</body>
</html>"""


def format_size(b):
    if b is None or b < 0:
        return "未知"
    if b >= 1 << 30:
        return f"{b / (1 << 30):.2f} GB"
    if b >= 1 << 20:
        return f"{b / (1 << 20):.2f} MB"
    if b >= 1 << 10:
        return f"{b / (1 << 10):.2f} KB"
    return f"{b} B"


def make_item_html(item, idx, category):
    name = item.get("name", "未知")
    desc = item.get("description", "")
    size = item.get("size_bytes", 0)
    cmd = item.get("clean_command", "").replace('"', "&quot;").replace("'", "&#39;")
    size_display = item.get("size_display", format_size(size))
    checked = 'checked' if category == "safe" else ""

    return f"""<div class="item">
      <input type="checkbox" id="item-{idx}" data-size="{size}" data-cmd="{cmd}" data-name="{name}" {checked}>
      <label for="item-{idx}" class="item-info">
        <span class="item-name">{name}</span>
        <span class="item-desc">{desc}</span>
      </label>
      <span class="item-size">{size_display}</span>
    </div>"""


def make_large_files_section(files):
    if not files:
        return ""
    rows = ""
    for f in files:
        rows += f"""<tr>
          <td>{f.get('name','')}</td>
          <td class="file-path">{f.get('path','')}</td>
          <td style="text-align:right;white-space:nowrap">{f.get('size_display', format_size(f.get('size_bytes',0)))}</td>
          <td>{f.get('last_modified','')}</td>
        </tr>"""
    return f"""<div class="section">
  <div class="section-header review">📁 大文件 (>500MB)</div>
  <div style="border:1px solid var(--border);border-top:none;border-radius:0 0 10px 10px;overflow-x:auto;padding:4px">
    <table class="file-table">
      <tr><th>文件名</th><th>路径</th><th>大小</th><th>修改时间</th></tr>
      {rows}
    </table>
  </div>
</div>"""


def generate_report(data, output_path):
    drive = data.get("drive", "C:")
    total = data.get("total_bytes", 0)
    used = data.get("used_bytes", 0)
    free = data.get("free_bytes", 0)
    used_pct = data.get("used_percent", 0)
    summary = data.get("summary", {})

    used_color = "#ef4444" if used_pct > 90 else "#eab308" if used_pct > 75 else "#22c55e"

    safe_items = data.get("categories", {}).get("safe", [])
    review_items = data.get("categories", {}).get("review", [])

    idx = 0
    safe_html = ""
    for item in safe_items:
        safe_html += make_item_html(item, idx, "safe")
        idx += 1

    review_html = ""
    for item in review_items:
        review_html += make_item_html(item, idx, "review")
        idx += 1

    # 准备 JSON 数据给前端
    items_json = json.dumps(safe_items + review_items, ensure_ascii=False)

    large_files_section = make_large_files_section(data.get("top_large_files", []))

    html = HTML_TEMPLATE.format(
        drive=drive,
        scan_time=data.get("scan_time", ""),
        username=data.get("username", ""),
        total_display=format_size(total),
        used_display=format_size(used),
        free_display=format_size(free),
        used_percent=used_pct,
        used_color=used_color,
        potential_display=summary.get("potential_total_display", ""),
        safe_display=summary.get("safe_total_display", ""),
        review_display=summary.get("review_total_display", ""),
        safe_items_html=safe_html,
        review_items_html=review_html,
        large_files_section=large_files_section,
        items_json=items_json,
    )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ 报告已生成: {output_path}")
    print(f"   请在浏览器中打开查看和操作。")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="生成磁盘清理 HTML 报告")
    parser.add_argument("input", help="scan_result.json 路径")
    parser.add_argument("-o", "--output", default="cleanup_report.html", help="输出 HTML 路径")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        data = json.load(f)

    generate_report(data, args.output)
