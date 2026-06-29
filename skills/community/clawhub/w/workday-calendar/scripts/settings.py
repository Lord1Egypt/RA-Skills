#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
workday-calendar 配置服务器

提供 Web 配置界面，支持：
- 切换基础日程底板（法定节假日/排班表）
- 导出规则模板
- 导入规则
- 导出基板日历 HTML
- 导出个人日程 HTML

用法:
  python scripts/settings.py [port]
  默认端口 8765，打开 http://localhost:8765
"""

import json
import sys
import os
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

# 确保能导入 workday_calendar 模块
SKILL_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILL_DIR))

from scripts.workday_calendar import (
    load_config, save_config,
    export_rules_template, import_rules_from_template,
    generate_weekly_board_html, generate_schedule_html,
    export_schedule_table,
    calculate_total_workdays,
    get_skill_data_dir, datetime
)


PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8765


class ConfigHandler(BaseHTTPRequestHandler):

    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8"))

    def _send_html(self, html, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    def _read_body(self) -> dict:
        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            return {}
        raw = self.rfile.read(length)
        return json.loads(raw.decode("utf-8"))

    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self._send_html(self._generate_page())

        elif self.path == "/config":
            cfg = load_config()
            self._send_json(cfg)

        elif self.path == "/export-rules-template":
            year = datetime.now().year
            template = export_rules_template(year)
            self._send_json(template)

        elif self.path == "/export-board":
            year = datetime.now().year
            html = generate_weekly_board_html(year, embed_schedule=False)
            self._send_html(html)

        elif self.path == "/export-schedule-weekly":
            year = datetime.now().year
            html = generate_weekly_board_html(year, embed_schedule=True)
            self._send_html(html)

        elif self.path == "/export-schedule":
            html = generate_schedule_html()
            self._send_html(html)

        elif self.path.startswith("/export-schedule-table"):
            from urllib.parse import urlparse, parse_qs
            qs = parse_qs(urlparse(self.path).query)
            year = int(qs.get("year", [datetime.now().year])[0])
            mode = qs.get("mode", ["week"])[0]
            date_from = qs.get("date_from", [None])[0]
            date_to = qs.get("date_to", [None])[0]
            html = export_schedule_table(year, mode, date_from, date_to)
            self._send_html(html)

        elif self.path == "/done":
            self._send_html(self._generate_done_page())

        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/save":
            body = self._read_body()
            save_config(body)
            self._send_json({"status": "ok", "message": "配置已保存"})

        elif self.path == "/import-rules":
            body = self._read_body()
            result = import_rules_from_template(body)
            self._send_json({"status": "ok", "message": result})

        else:
            self.send_response(404)
            self.end_headers()

    def _generate_page(self) -> str:
        """生成配置页面 HTML"""
        return r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>workday-calendar 配置</title>
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "PingFang SC", "Microsoft YaHei", sans-serif;
  background: linear-gradient(135deg, #f5f0ff 0%, #e8f4f8 100%);
  color: #333; min-height: 100vh; padding: 20px;
}
.header {
  background: linear-gradient(135deg, #9b59b6 0%, #3498db 100%);
  color: #fff; border-radius: 16px; padding: 24px 30px; margin-bottom: 20px;
  box-shadow: 0 4px 20px rgba(155, 89, 182, 0.3);
}
.header h1 { font-size: 24px; }
.header p { opacity: 0.9; font-size: 14px; margin-top: 4px; }
.card {
  background: #fff; border-radius: 16px; padding: 24px; margin-bottom: 20px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.06);
}
.card h2 { font-size: 18px; color: #444; margin-bottom: 16px; display: flex; align-items: center; gap: 8px; }

/* Toggle Switch */
.toggle-wrap { display: flex; align-items: center; gap: 16px; padding: 12px 0; }
.toggle { position: relative; width: 52px; height: 28px; flex-shrink: 0; }
.toggle input { opacity: 0; width: 0; height: 0; }
.toggle .slider {
  position: absolute; inset: 0; background: #ccc; border-radius: 14px;
  cursor: pointer; transition: 0.3s;
}
.toggle .slider::before {
  content: ""; position: absolute; left: 3px; top: 3px;
  width: 22px; height: 22px; border-radius: 50%; background: #fff;
  transition: 0.3s;
}
.toggle input:checked + .slider { background: #3498db; }
.toggle input:checked + .slider::before { transform: translateX(24px); }
.toggle-label { font-size: 14px; color: #555; }
.toggle-desc { font-size: 12px; color: #999; margin-top: 2px; }

/* Buttons */
.btn {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 10px 24px; border: none; border-radius: 10px;
  font-size: 14px; font-weight: 500; cursor: pointer;
  transition: all 0.2s;
}
.btn-primary { background: linear-gradient(135deg, #9b59b6, #3498db); color: #fff; }
.btn-primary:hover { box-shadow: 0 4px 12px rgba(155,89,182,0.4); transform: translateY(-1px); }
.btn-success { background: #2ecc71; color: #fff; }
.btn-success:hover { box-shadow: 0 4px 12px rgba(46,204,113,0.4); }
.btn-warning { background: #f39c12; color: #fff; }
.btn-info { background: #3498db; color: #fff; }
.btn-outline { background: transparent; border: 1px solid #3498db; color: #3498db; }
.btn-outline:hover { background: #3498db10; }
.btn-sm { padding: 6px 16px; font-size: 13px; }

/* Grid */
.btn-grid { display: flex; flex-wrap: wrap; gap: 12px; margin-top: 12px; }

/* Textarea */
textarea {
  width: 100%; min-height: 200px; padding: 12px; border: 1px solid #e0e0e0;
  border-radius: 10px; font-family: "Cascadia Code", "Fira Code", "Consolas", monospace;
  font-size: 13px; line-height: 1.5; resize: vertical;
}
textarea:focus { outline: none; border-color: #3498db; box-shadow: 0 0 0 3px rgba(52,152,219,0.15); }

/* Toast */
.toast {
  position: fixed; bottom: 30px; right: 30px; padding: 14px 24px;
  border-radius: 12px; color: #fff; font-size: 14px; z-index: 999;
  transform: translateY(100px); opacity: 0; transition: all 0.4s;
}
.toast.show { transform: translateY(0); opacity: 1; }
.toast.success { background: #2ecc71; }
.toast.error { background: #e74c3c; }
.toast.info { background: #3498db; }

/* Loading */
.loading { text-align: center; padding: 40px; color: #999; }

/* Done page */
.done-page { text-align: center; padding: 80px 20px; }
.done-page .icon { font-size: 64px; margin-bottom: 20px; }
.done-page h2 { font-size: 24px; color: #444; margin-bottom: 12px; }
.done-page p { color: #888; }
</style>
</head>
<body>
<div class="header">
  <h1>&#128197; workday-calendar 配置中心</h1>
  <p>底板(法定假休+双休修正) → weekened_config → (可选)排班规则叠加 → 个人日程</p>
</div>

<!-- 基础周类型 -->
<div class="card">
  <h2>&#128196; 基础周类型</h2>
    <div class="toggle-wrap">
    <label class="toggle">
      <input type="checkbox" id="useScheduling">
      <span class="slider"></span>
    </label>
    <div>
      <div class="toggle-label">叠加排班规则到底板</div>
      <div class="toggle-desc" id="toggleDesc">关闭 = 仅底板(法定假休+双休修正) | 打开 = 底板+weekend_config+轮休/公休/临修</div>
    </div>
  </div>
  <div class="toggle-wrap" style="margin-top:4px;">
    <label class="toggle">
      <input type="checkbox" id="autoComplete">
      <span class="slider"></span>
    </label>
    <div>
      <div class="toggle-label">过期日程自动打标已完成</div>
      <div class="toggle-desc">关闭 = 打标已错过 | 打开 = 自动打标已完成</div>
    </div>
  </div>
  <button class="btn btn-primary" onclick="saveConfig()">&#128190; 保存配置</button>
</div>

<!-- 规则模板 -->
<div class="card">
  <h2>&#128203; 规则模板</h2>
  <p style="color:#888;font-size:13px;margin-bottom:12px;">导出当前配置为标准化规则模板，编辑后可重新导入</p>
  <div class="btn-grid">
    <button class="btn btn-info" onclick="exportRulesTemplate()">&#128230; 导出规则模板</button>
    <button class="btn btn-outline" onclick="copyTemplate()">&#128203; 复制到剪贴板</button>
  </div>
  <div style="margin-top:12px;">
    <textarea id="templateArea" placeholder="点击「导出规则模板」获取当前配置..."></textarea>
  </div>
</div>

<!-- 导入规则 -->
<div class="card">
  <h2>&#128229; 导入规则</h2>
  <p style="color:#888;font-size:13px;margin-bottom:12px;">粘贴编辑好的规则模板 JSON，点击导入</p>
  <textarea id="importArea" placeholder='粘贴规则模板 JSON，例如：
{
  "version": "1.0",
  "year": 2026,
  "base_type": "holiday",
  "rules": {
    "weekend_config": {"weekends": [0,6]},
    "holiday_intervals": [...],
    "compensatory_days": [...],
    "rotation_configs": [],
    "special_rests": []
  }
}'></textarea>
  <div class="btn-grid">
    <button class="btn btn-success" onclick="importRules()">&#128229; 导入规则</button>
    <button class="btn btn-outline" onclick="document.getElementById('importArea').value=''">&#128465; 清空</button>
  </div>
</div>

<!-- 导出 -->
<div class="card">
  <h2>&#128424; 导出</h2>
  <p style="color:#888;font-size:13px;margin-bottom:12px;">排班HTML = 底板+weekend_config+排班规则(可选) | 日程HTML = 排班HTML + 个人日程</p>
  <div class="btn-grid">
    <button class="btn btn-primary" onclick="exportBoard()">&#128197; 导出排班HTML</button>
    <button class="btn btn-success" onclick="exportScheduleBoard()">&#128467; 导出日程HTML</button>
  </div>
  <div style="margin-top:16px;padding-top:16px;border-top:1px solid #eee;">
    <h3 style="font-size:14px;color:#555;margin-bottom:8px;">&#128203; 导出排班表</h3>
    <div style="display:flex;flex-wrap:wrap;gap:10px;align-items:end;">
      <div>
        <label style="font-size:12px;color:#888;">年份</label><br>
        <input type="number" id="tbYear" value="2026" style="width:80px;padding:6px 8px;border:1px solid #ddd;border-radius:6px;font-size:13px;">
      </div>
      <div>
        <label style="font-size:12px;color:#888;">输出方式</label><br>
        <label style="font-size:13px;margin-right:8px;"><input type="radio" name="exportMode" value="week" checked> 按周</label>
        <label style="font-size:13px;"><input type="radio" name="exportMode" value="month"> 按月</label>
      </div>
      <div><label style="font-size:12px;color:#888;">起始日期(可选)</label><br><input type="date" id="tbDateFrom" style="width:140px;padding:5px 8px;border:1px solid #ddd;border-radius:6px;font-size:13px;"></div>
      <div><label style="font-size:12px;color:#888;">结束日期(可选)</label><br><input type="date" id="tbDateTo" style="width:140px;padding:5px 8px;border:1px solid #ddd;border-radius:6px;font-size:13px;"></div>
      <div><button class="btn btn-warning" onclick="exportTable()">&#128203; 导出</button></div>
    </div>
    <p style="font-size:11px;color:#aaa;margin-top:6px;">不选日期范围则导出全年</p>
  </div>
</div>
</div>

<div class="toast" id="toast"></div>

<script>
function showToast(msg, type) {
  var t = document.getElementById('toast');
  t.textContent = msg; t.className = 'toast ' + type;
  setTimeout(function() { t.classList.add('show'); }, 10);
  setTimeout(function() { t.classList.remove('show'); }, 3000);
}

// 加载配置
fetch('/config').then(function(r) { return r.json(); }).then(function(cfg) {
  document.getElementById('useScheduling').checked = cfg.use_scheduling_as_base || false;
  document.getElementById('autoComplete').checked = cfg.auto_mark_missed_as_completed || false;
}).catch(function(e) { showToast('加载配置失败: ' + e, 'error'); });

// 保存配置
function saveConfig() {
  var scheduling = document.getElementById('useScheduling').checked;
  var autoComplete = document.getElementById('autoComplete').checked;
  fetch('/save', {
    method: 'POST', headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({use_scheduling_as_base: scheduling, auto_mark_missed_as_completed: autoComplete})
  }).then(function(r) { return r.json(); }).then(function(d) {
    showToast(d.message || '配置已保存', 'success');
  }).catch(function(e) { showToast('保存失败: ' + e, 'error'); });
}

// 导出规则模板
function exportRulesTemplate() {
  fetch('/export-rules-template').then(function(r) { return r.json(); }).then(function(tpl) {
    document.getElementById('templateArea').value = JSON.stringify(tpl, null, 2);
    showToast('规则模板已加载', 'success');
  }).catch(function(e) { showToast('导出失败: ' + e, 'error'); });
}

// 复制模板
function copyTemplate() {
  var ta = document.getElementById('templateArea');
  if (!ta.value) { showToast('请先导出规则模板', 'error'); return; }
  if (navigator.clipboard) {
    navigator.clipboard.writeText(ta.value).then(function() {
      showToast('已复制到剪贴板', 'success');
    });
  } else {
    ta.select(); document.execCommand('copy');
    showToast('已复制到剪贴板', 'success');
  }
}

// 导入规则
function importRules() {
  var raw = document.getElementById('importArea').value;
  if (!raw) { showToast('请先粘贴规则模板 JSON', 'error'); return; }
  try { JSON.parse(raw); } catch(e) { showToast('JSON 格式错误: ' + e.message, 'error'); return; }
  var tpl = JSON.parse(raw);
  fetch('/import-rules', {
    method: 'POST', headers: {'Content-Type': 'application/json'},
    body: raw
  }).then(function(r) { return r.json(); }).then(function(d) {
    showToast(d.message || '导入成功', 'success');
  }).catch(function(e) { showToast('导入失败: ' + e, 'error'); });
}

// 导出排班HTML（不含个人日程）
function exportBoard() {
  downloadExport('/export-board', '排班');
}

// 导出日程HTML（含个人日程事件）
function exportScheduleBoard() {
  downloadExport('/export-schedule-weekly', '日程');
}

// 导出排班表（从表单读取参数）
function exportTable() {
  var year = document.getElementById('tbYear').value || 2026;
  var mode = document.querySelector('input[name=exportMode]:checked').value;
  var dateFrom = document.getElementById('tbDateFrom').value;
  var dateTo = document.getElementById('tbDateTo').value;
  var params = 'year=' + year + '&mode=' + mode;
  if (dateFrom) { params += '&date_from=' + dateFrom; }
  if (dateTo) { params += '&date_to=' + dateTo; }
  downloadExport('/export-schedule-table?' + params, '排班表_' + year + '_' + mode);
}

// 通用下载函数，避免 window.open 被弹窗拦截
function downloadExport(url, name) {
  fetch(url).then(function(r) { return r.text(); }).then(function(html) {
    var blob = new Blob([html], {type: 'text/html;charset=utf-8'});
    var a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = name + '-' + new Date().toISOString().slice(0,10) + '.html';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(a.href);
    showToast(name + 'HTML 已导出', 'success');
  }).catch(function(e) {
    showToast('导出失败: ' + e, 'error');
  });
}
</script>
</body>
</html>"""

    def _generate_done_page(self) -> str:
        return """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>配置完成</title>
<style>
body { font-family: -apple-system, 'PingFang SC', sans-serif; background: linear-gradient(135deg, #f5f0ff, #e8f4f8); min-height: 100vh; display: flex; align-items: center; justify-content: center; }
.done-page { text-align: center; background: #fff; border-radius: 16px; padding: 60px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); }
.icon { font-size: 64px; margin-bottom: 20px; }
h2 { font-size: 24px; color: #444; margin-bottom: 12px; }
p { color: #888; }
</style>
</head>
<body>
<div class="done-page">
  <div class="icon">&#10004;&#65039;</div>
  <h2>配置完成</h2>
  <p>已保存所有配置，可以关闭此页面</p>
</div>
</body>
</html>"""


def main():
    server = HTTPServer(("0.0.0.0", PORT), ConfigHandler)
    url = f"http://localhost:{PORT}"
    print(f"workday-calendar 配置服务器已启动")
    print(f"打开浏览器访问: {url}")
    print("按 Ctrl+C 停止服务器")
    webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n服务器已停止")
        server.server_close()


if __name__ == "__main__":
    main()
