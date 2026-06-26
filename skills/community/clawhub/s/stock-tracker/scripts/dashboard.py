#!/usr/bin/env python3
"""自选股公告仪表盘 - Web 界面

启动: python3 scripts/dashboard.py
访问: http://localhost:5001
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, jsonify, render_template_string
import db
import html

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>自选股公告仪表盘</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: -apple-system, "PingFang SC", "Microsoft YaHei", sans-serif; background: #f5f6fa; color: #2d3436; }
  .header { background: linear-gradient(135deg, #0984e3, #6c5ce7); color: white; padding: 12px 32px; position: sticky; top: 0; z-index: 100; }
  .header h1 { font-size: 22px; font-weight: 600; }
  .header .sub { font-size: 13px; opacity: 0.8; margin-top: 4px; }
  .container { max-width: 1200px; margin: 20px auto; padding: 0 16px; }

  /* 股票表格 */
  .stock-table { width: 100%; border-collapse: collapse; background: white; table-layout: fixed; }
  .stock-table th { background: #dfe6e9; padding: 10px 14px; text-align: left; font-size: 13px; font-weight: 600; color: #636e72; }
  .stock-table th:first-child { width: 40%; }
  .stock-table th:not(:first-child) { width: 15%; }
  .stock-table td { padding: 10px 14px; border-bottom: 1px solid #f0f0f0; font-size: 14px; }
  .stock-table tr:hover { background: #f8f9ff; cursor: pointer; }
  .stock-table tr.expanded { background: #f0f4ff; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }

  /* 浮动个股栏 */
  .stock-float-bar { display: none; position: fixed; top: 70px; left: 0; right: 0; background: #f0f4ff; border-bottom: 2px solid #0984e3; padding: 10px 32px; z-index: 99; cursor: pointer; box-shadow: 0 2px 8px rgba(0,0,0,0.12); align-items: center; justify-content: space-between; }
  .stock-float-bar.show { display: flex; }
  .stock-float-bar .stock-name { font-weight: 700; font-size: 15px; color: #2d3436; }
  .stock-float-bar .stock-code { color: #636e72; font-size: 13px; margin-left: 8px; }
  .stock-float-bar .float-close { color: #0984e3; font-size: 13px; font-weight: 600; }
  .stock-name { font-weight: 600; }
  .stock-code { color: #636e72; font-size: 12px; margin-left: 6px; }
  .count-badge { display: inline-block; min-width: 28px; padding: 2px 8px; border-radius: 10px; font-size: 12px; font-weight: 600; text-align: center; }
  .count-7d { background: #dfe6e9; }
  .count-15d { background: #b2bec3; color: white; }
  .count-30d { background: #636e72; color: white; }

  /* 展开区域 */
  .ann-list { display: none; background: #fafbfc; }
  .ann-list.show { display: table-row; }
  .ann-list td { padding: 0; width: 100%; }
  .ann-item { width: 100%; padding: 14px 20px; border-bottom: 1px solid #eee; }
  .ann-item:last-child { border-bottom: none; }
  .ann-title { font-weight: 600; font-size: 15px; color: #2d3436; display: flex; justify-content: space-between; align-items: flex-start; gap: 12px; }
  .ann-date { font-size: 12px; color: #636e72; margin-top: 2px; }
  .ann-summary { margin-top: 8px; padding: 12px 16px; background: #e8f4fd; border-left: 3px solid #0984e3; border-radius: 4px; font-size: 14px; line-height: 1.7; color: #2d3436; position: relative; }
  .ann-tag { background: #0984e3; color: white; padding: 2px 10px; border-radius: 12px; font-size: 12px; font-weight: 600; white-space: nowrap; flex-shrink: 0; margin-top: 2px; }
  .ann-text-wrapper { margin-top: 10px; max-height: 400px; overflow-y: auto; width: 100%; }
  .ann-text { font-size: 13px; line-height: 1.7; color: #555; white-space: pre-wrap; word-wrap: break-word; width: 100%; display: none; }
  .ann-text.show { display: block; }
  .ann-summary { cursor: pointer; }
  .ann-title { cursor: pointer; }
  .ann-link { display: inline-block; margin-top: 6px; font-size: 12px; color: #0984e3; text-decoration: none; }
  .ann-link:hover { text-decoration: underline; }
  .toggle-icon { font-size: 12px; margin-left: 6px; transition: transform 0.2s; }
  .expanded .toggle-icon { transform: rotate(90deg); }

  .empty { text-align: center; padding: 40px; color: #b2bec3; }

  /* 搜索框 */
  .search-box { position: absolute; top: 50%; right: 32px; transform: translateY(-50%); }
  .search-box input { padding: 8px 14px; border: none; border-radius: 20px; font-size: 14px; width: 220px; outline: none; background: rgba(255,255,255,0.25); color: white; backdrop-filter: blur(4px); }
  .search-box input::placeholder { color: rgba(255,255,255,0.7); }
  .search-box input:focus { background: rgba(255,255,255,0.4); }

  /* table 圆角 wrapper */
  .table-wrapper { border-radius: 8px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.08); }
</style>
</head>
<body>
<div class="header">
  <h1>AI 公告雷达</h1>
  <div class="sub">数据来源：东财 / 巨潮资讯</div>
  <div class="search-box"><input type="text" id="searchInput" placeholder="搜索股票代码或名称..." oninput="filterStocks(this.value)"></div>
</div>
<div class="stock-float-bar" id="floatBar" onclick="toggleFloatBar()">
  <div><span class="stock-name" id="floatName"></span><span class="stock-code" id="floatCode"></span></div>
  <div class="float-close">点击折叠 ↑</div>
</div>
<div class="container">
  <div id="app"></div>
</div>

<script>
async function loadStocks() {
  const resp = await fetch('/api/stocks');
  const stocks = await resp.json();
  const app = document.getElementById('app');

  if (!stocks.length) {
    app.innerHTML = '<div class="empty">暂无公告数据</div>';
    return;
  }

  let html = '<div class="table-wrapper"><table class="stock-table"><thead><tr>';
  html += '<th style="width:40%">股票</th><th style="width:15%">7天</th><th style="width:15%">15天</th><th style="width:15%">30天</th><th style="width:15%">全部</th>';
  html += '</tr></thead><tbody>';

  for (const s of stocks) {
    html += `<tr class="stock-row" data-code="${s.stock_code}" onclick="toggleStock(this)">
      <td><span class="stock-name">${s.stock_name}</span><span class="stock-code">${s.stock_code}</span></td>
      <td><span class="count-badge count-7d">${s.valuable_7d}/${s.total_7d}</span></td>
      <td><span class="count-badge count-15d">${s.valuable_15d}/${s.total_15d}</span></td>
      <td><span class="count-badge count-30d">${s.valuable_30d}/${s.total_30d}</span></td>
      <td>${s.valuable_total}/${s.total}</td>
    </tr>`;
    html += `<tr class="ann-list" id="ann-${s.stock_code}"><td colspan="5">加载中...</td></tr>`;
  }

  html += '</tbody></table></div>';
  app.innerHTML = html;
}

let currentExpandedCode = null;

function updateFloatBar() {
  const floatBar = document.getElementById('floatBar');
  if (!currentExpandedCode) {
    floatBar.classList.remove('show');
    return;
  }
  const row = document.querySelector('.stock-row[data-code="' + currentExpandedCode + '"]');
  if (!row) return;
  const rect = row.getBoundingClientRect();
  const headerHeight = document.querySelector('.header').getBoundingClientRect().height;
  floatBar.style.top = headerHeight + 'px';
  if (rect.bottom < headerHeight) {
    floatBar.classList.add('show');
  } else {
    floatBar.classList.remove('show');
  }
}

function toggleFloatBar() {
  if (!currentExpandedCode) return;
  const row = document.querySelector('.stock-row[data-code="' + currentExpandedCode + '"]');
  if (row) toggleStock(row);
}

window.addEventListener('scroll', updateFloatBar);

async function toggleStock(row) {
  const code = row.dataset.code;
  const annRow = document.getElementById('ann-' + code);
  const floatBar = document.getElementById('floatBar');

  if (annRow.classList.contains('show')) {
    annRow.classList.remove('show');
    row.classList.remove('expanded');
    if (currentExpandedCode === code) {
      currentExpandedCode = null;
      floatBar.classList.remove('show');
    }
    return;
  }

  row.classList.add('expanded');
  annRow.classList.add('show');
  currentExpandedCode = code;
  document.getElementById('floatName').textContent = row.querySelector('.stock-name').textContent;
  document.getElementById('floatCode').textContent = row.querySelector('.stock-code').textContent;
  updateFloatBar();

  if (annRow.dataset.loaded) return;

  try {
    const resp = await fetch('/api/announcements/' + code);
    const anns = await resp.json();

    if (!anns.length) {
      annRow.innerHTML = '<td colspan="5" style="padding:14px 20px;color:#b2bec3;">暂无公告</td>';
      annRow.dataset.loaded = '1';
      return;
    }

  let html = '<td colspan="5" style="padding:0;">';
  for (const a of anns) {
    const textId = 'text-' + code + '-' + a.ann_id.substring(0, 8);
    let tagHtml = '';
    if (a.ann_type_category || a.ann_type_tag) {
      const parts = [];
      if (a.ann_type_category) parts.push(a.ann_type_category);
      if (a.ann_type_tag) parts.push(a.ann_type_tag);
      tagHtml = `<span class="ann-tag">${parts.join(' / ')}</span>`;
    }
    html += '<div class="ann-item">';
    html += `<div class="ann-title" onclick="toggleText('${textId}')">${a.title}${tagHtml}</div>`;
    html += `<div class="ann-date">${a.ann_date}`;
    if (a.url) html += ` &middot; <a class="ann-link" href="${a.url.replace(/"/g, '&quot;')}" target="_blank">查看原文</a>`;
    html += '</div>';
    if (a.summary) {
      html += `<div class="ann-summary" onclick="toggleText('${textId}')">${a.summary}</div>`;
    }
    if (a.clean_text) {
      html += `<div class="ann-text-wrapper"><div class="ann-text" id="${textId}">${a.clean_text}</div></div>`;
    }
    html += '</div>';
  }
  html += '</td>';

    annRow.innerHTML = html;
    annRow.dataset.loaded = '1';
  } catch (err) {
    annRow.innerHTML = '<td colspan="5" style="padding:14px 20px;color:#e74c3c;">加载失败，请刷新重试</td>';
  }
}

function toggleText(id) {
  const el = document.getElementById(id);
  if (el) el.classList.toggle('show');
}

function filterStocks(keyword) {
  const rows = document.querySelectorAll('.stock-row');
  const kw = keyword.trim().toLowerCase();
  for (const row of rows) {
    const code = row.dataset.code.toLowerCase();
    const name = row.querySelector('.stock-name').textContent.toLowerCase();
    const match = !kw || code.includes(kw) || name.includes(kw);
    row.style.display = match ? '' : 'none';
    const annRow = document.getElementById('ann-' + row.dataset.code);
    if (annRow) annRow.style.display = match ? '' : 'none';
  }
}

loadStocks();
</script>
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)


@app.route("/api/stocks")
def api_stocks():
    data = db.get_stock_overview()
    for item in data:
        item["stock_name"] = html.escape(item.get("stock_name", ""))
        item["stock_code"] = html.escape(item.get("stock_code", ""))
    return jsonify(data)


import re

_RE_STOCK_CODE = re.compile(r"^[0-9]{4,6}$")

@app.route("/api/announcements/<stock_code>")
def api_announcements(stock_code):
    if not _RE_STOCK_CODE.match(stock_code):
        return jsonify({"error": "股票代码格式错误"}), 400
    data = db.get_announcements_for_stock(stock_code, days=30)
    for item in data:
        item["title"] = html.escape(item.get("title", ""))
        item["summary"] = html.escape(item.get("summary", ""))
        item["clean_text"] = html.escape(item.get("clean_text", ""))
        item["ann_type_category"] = html.escape(item.get("ann_type_category", ""))
        item["ann_type_tag"] = html.escape(item.get("ann_type_tag", ""))
    return jsonify(data)


if __name__ == "__main__":
    db.init_db()
    port = int(os.environ.get("PORT", 5001))
    print(f"自选股公告仪表盘启动: http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)
