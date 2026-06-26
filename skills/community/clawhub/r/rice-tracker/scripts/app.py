#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大米消耗采购提醒系统 v2.0 - 支持分批进货、欠款追踪、对账管理
"""

import json
from datetime import date, datetime, timedelta
from flask import Flask, request, jsonify, render_template_string, redirect, url_for
from pathlib import Path

app = Flask(__name__)

DATA_FILE = Path.home() / ".openclaw" / "workspace" / "rice-shop-records.json"
PORT = 5001
HOST = "0.0.0.0"

# ── 数据读写 ────────────────────────────────────────────────────────────────

def load_records():
    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_records(records):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

def get_stock_info(record):
    """计算客户总库存和剩余天数"""
    if not record.get("purchases"):
        return {"total": 0, "days_left": -1, "expected_date": "无记录"}
    
    total_quantity = sum(p.get("quantity", 0) for p in record["purchases"])
    if total_quantity <= 0:
        return {"total": 0, "days_left": -1, "expected_date": "已吃完"}
    
    # 找到最早购买日期
    dates = [datetime.strptime(p["date"], "%Y-%m-%d").date() for p in record["purchases"]]
    earliest = min(dates)
    
    today = date.today()
    people = record.get("people", 1)
    daily_rate = record.get("daily_rate", 0.4)
    frequency = record.get("frequency", "daily")
    
    # 计算消耗
    days_passed = (today - earliest).days
    if days_passed < 0:
        days_passed = 0
    
    if frequency == "workdays":
        workdays = sum(1 for i in range(days_passed + 1) if (earliest + timedelta(i)).weekday() < 5)
        consumed = workdays * people * daily_rate
    elif frequency == "weekends":
        weekends = sum(1 for i in range(days_passed + 1) if (earliest + timedelta(i)).weekday() >= 5)
        consumed = weekends * people * daily_rate
    else:
        consumed = days_passed * people * daily_rate
    
    remaining = total_quantity - consumed
    if remaining <= 0:
        return {"total": total_quantity, "days_left": -1, "expected_date": "已吃完"}
    
    # 估算剩余天数
    if frequency == "workdays":
        days_per_jin = 1.0 / (people * daily_rate * 5 / 7) if people * daily_rate > 0 else float('inf')
    elif frequency == "weekends":
        days_per_jin = 1.0 / (people * daily_rate * 2 / 7) if people * daily_rate > 0 else float('inf')
    else:
        days_per_jin = 1.0 / (people * daily_rate) if people * daily_rate > 0 else float('inf')
    
    days_left = int(remaining * days_per_jin) if days_per_jin != float('inf') else 999
    expected_date = (today + timedelta(days=days_left)).strftime("%Y-%m-%d")
    
    return {"total": total_quantity, "days_left": days_left, "expected_date": expected_date}

# ── HTML 模板 ────────────────────────────────────────────────────────────────

CSS = """
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, "PingFang SC", "Microsoft YaHei", sans-serif; background: #f0f2f5; color: #1a1a2e; min-height: 100vh; }
.container { max-width: 1100px; margin: 0 auto; padding: 20px; }
.header { background: linear-gradient(135deg, #1a1a2e, #0f3460); color: white; padding: 20px 24px; border-radius: 16px; margin-bottom: 20px; }
.header h1 { font-size: 1.3em; font-weight: 700; }
.header .subtitle { font-size: 0.8em; opacity: 0.7; margin-top: 4px; }

/* Tab 导航 */
.tabs { display: flex; gap: 8px; margin-bottom: 16px; flex-wrap: wrap; }
.tab { padding: 10px 20px; background: white; border: none; border-radius: 10px; font-size: 0.95em; font-weight: 600; cursor: pointer; color: #666; transition: all 0.2s; }
.tab:hover { background: #e8e8e8; }
.tab.active { background: linear-gradient(135deg, #e94560, #c73e54); color: white; }
.tab-content { display: none; }
.tab-content.active { display: block; }

/* 卡片 */
.card { background: white; border-radius: 14px; padding: 20px; margin-bottom: 16px; box-shadow: 0 2px 12px rgba(0,0,0,.06); }
.card-title { font-size: 1.05em; font-weight: 700; color: #0f3460; margin-bottom: 16px; border-left: 4px solid #e94560; padding-left: 10px; }

/* 表单 */
.form-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 14px; }
.form-grid .full { grid-column: 1 / -1; }
.form-grid label { font-size: 0.82em; color: #666; margin-bottom: 4px; display: block; }
.form-grid input, .form-grid select { width: 100%; padding: 9px 12px; border: 1.5px solid #e0e0e0; border-radius: 9px; font-size: 0.95em; background: #fafafa; }
.form-grid input:focus, .form-grid select:focus { outline: none; border-color: #0f3460; background: white; }
.btn { padding: 10px 22px; border: none; border-radius: 9px; font-size: 0.95em; font-weight: 600; cursor: pointer; }
.btn-primary { background: linear-gradient(135deg, #e94560, #c73e54); color: white; }
.btn-success { background: #00b894; color: white; }
.btn-danger { background: #ff4757; color: white; padding: 6px 14px; font-size: 0.82em; }
.btn-row { display: flex; gap: 10px; margin-top: 16px; flex-wrap: wrap; }

/* 表格 */
table { width: 100%; border-collapse: collapse; font-size: 0.85em; }
th { text-align: left; padding: 10px; background: #f5f5f5; font-weight: 500; font-size: 0.8em; color: #888; border-bottom: 2px solid #e8e8e8; }
td { padding: 10px; border-bottom: 1px solid #f0f0f0; }
.badge { display: inline-block; padding: 3px 10px; border-radius: 20px; font-size: 0.75em; font-weight: 600; }
.badge-red { background: #ffe5e5; color: #d63031; }
.badge-orange { background: #fff3e0; color: #e17055; }
.badge-green { background: #e5f9ed; color: #00b894; }
.badge-blue { background: #e8f0fe; color: #1565c0; }
.badge-gray { background: #f0f0f0; color: #666; }
.badge-corporate { background: #ede7f6; color: #5e35b1; }

/* 统计卡片 */
.stats-row { display: flex; gap: 16px; margin-bottom: 16px; flex-wrap: wrap; }
.stat-card { flex: 1; min-width: 140px; background: white; padding: 16px; border-radius: 12px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,.04); }
.stat-card .num { font-size: 1.6em; font-weight: 800; }
.stat-card .label { font-size: 0.75em; color: #888; margin-top: 4px; }
.stat-card.danger .num { color: #d63031; }
.stat-card.warning .num { color: #ffa502; }
.stat-card.success .num { color: #00b894; }

/* 警报横幅 */
.alert-bar { background: linear-gradient(90deg, #ff4757, #ff6b81); color: white; padding: 12px 20px; border-radius: 12px; margin-bottom: 16px; font-weight: 600; }
.alert-bar.warning { background: linear-gradient(90deg, #ffa502, #ff6348); }

/* 下拉选择 */
select.customer-select { padding: 8px 12px; border: 1.5px solid #e0e0e0; border-radius: 8px; font-size: 0.95em; background: white; min-width: 150px; }

/* 月份选择 */
.month-select { padding: 8px 16px; border: 1.5px solid #e0e0e0; border-radius: 8px; font-size: 0.95em; background: white; }

/* 空状态 */
.empty { text-align: center; padding: 40px; color: #bbb; }
.empty-icon { font-size: 3em; margin-bottom: 10px; }

/* 操作按钮 */
.action-btns { display: flex; gap: 6px; flex-wrap: wrap; }
.action-btns button { padding: 4px 10px; font-size: 0.75em; border-radius: 6px; border: none; cursor: pointer; }
.action-btns .btn-pay { background: #00b894; color: white; }
.action-btns .btn-del { background: #ff4757; color: white; }

@media (max-width: 600px) {
    .form-grid { grid-template-columns: 1fr; }
    table { font-size: 0.75em; }
    th, td { padding: 6px 4px; }
}
"""

INDEX_HTML = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>大米采购管理系统 v2.0</title>
</head>
<body>
""" + CSS + """
<div class="container">

<div class="header">
  <h1>🍚 大米采购管理系统 v2.0</h1>
  <div class="subtitle">分批进货 · 欠款追踪 · 对账管理</div>
</div>

<!-- Tab 导航 -->
<div class="tabs">
  <button class="tab active" onclick="showTab('stock')">📦 库存追踪</button>
  <button class="tab" onclick="showTab('purchase')">📝 进货记录</button>
  <button class="tab" onclick="showTab('reconcile')">💰 对账管理</button>
</div>

<!-- Tab 1: 库存追踪 -->
<div id="stock" class="tab-content active">
  <div class="card">
    <div class="card-title">➕ 添加新客户</div>
    <form method="post" action="/api/add-customer">
      <div class="form-grid">
        <div><label>客户姓名 *</label><input name="owner" placeholder="如：张三" required></div>
        <div><label>手机号</label><input name="phone" placeholder="方便联系"></div>
        <div><label>家庭人口 *</label><input name="people" type="number" min="1" value="1" required></div>
        <div><label>人均每天消耗（斤）</label><input name="daily_rate" type="number" step="0.05" value="0.4" required></div>
        <div class="full">
          <label>消耗频率</label>
          <select name="frequency">
            <option value="daily">每天都吃</option>
            <option value="workdays">只在工作日吃</option>
            <option value="weekends">只在周末吃</option>
          </select>
        </div>
        <div class="full"><label>备注</label><input name="note" placeholder="如：家里有老人"></div>
      </div>
      <div class="btn-row"><button type="submit" class="btn btn-primary">➕ 添加客户</button></div>
    </form>
  </div>

  <!-- 统计 -->
  <div class="stats-row">
    <div class="stat-card"><div class="num">{{ records|length }}</div><div class="label">客户总数</div></div>
    <div class="stat-card danger"><div class="num">{{ urgent_count }}</div><div class="label">库存不足</div></div>
    <div class="stat-card warning"><div class="num">{{ unsettled_count }}</div><div class="label">待对账</div></div>
    <div class="stat-card success"><div class="num">{{ total_stock }}</div><div class="label">总库存(斤)</div></div>
  </div>

  <!-- 警告 -->
  {% if urgent_records or settle_alerts %}
    {% if urgent_records %}
    <div class="alert-bar">🚨 <strong>库存提醒</strong>：{{ urgent_records|length }} 位客户大米即将吃完！</div>
    {% endif %}
    {% if settle_alerts %}
    <div class="alert-bar warning">💰 <strong>对账提醒</strong>：{{ settle_alerts|length }} 笔账目到期未付！</div>
    {% endif %}
  {% endif %}

  <div class="card">
    <div class="card-title">📋 客户库存列表</div>
    {% if records %}
    <table>
      <thead><tr><th>客户</th><th>总库存</th><th>剩余天数</th><th>预计吃完</th><th>状态</th><th>操作</th></tr></thead>
      <tbody>
      {% for r in records %}
        <tr>
          <td><strong>{{ r.owner }}</strong>{% if r.phone %}<br><span style="font-size:0.75em;color:#999">{{ r.phone }}</span>{% endif %}</td>
          <td>{{ r.stock_info.total }} 斤</td>
          <td>{% if r.stock_info.days_left < 0 %}<span style="color:#d63031">已吃完</span>{% else %}{{ r.stock_info.days_left }} 天{% endif %}</td>
          <td>{{ r.stock_info.expected_date }}</td>
          <td>
            {% if r.stock_info.days_left < 0 %}<span class="badge badge-red">已吃完</span>
            {% elif r.stock_info.days_left <= 3 %}<span class="badge badge-orange">即将耗尽</span>
            {% elif r.stock_info.days_left <= 7 %}<span class="badge badge-blue">注意</span>
            {% else %}<span class="badge badge-green">充足</span>{% endif %}
          </td>
          <td>
            <form method="post" action="/api/delete-customer/{{ loop.index0 }}" onsubmit="return confirm('确定删除？')">
              <button type="submit" class="btn-danger">删除</button>
            </form>
          </td>
        </tr>
      {% endfor %}
      </tbody>
    </table>
    {% else %}
    <div class="empty"><div class="empty-icon">📦</div><div>暂无客户，请添加</div></div>
    {% endif %}
  </div>
</div>

<!-- Tab 2: 进货记录 -->
<div id="purchase" class="tab-content">
  <div class="card">
    <div class="card-title">📝 添加进货记录</div>
    <form method="post" action="/api/purchase">
      <div class="form-grid">
        <div>
          <label>选择客户 *</label>
          <select name="owner" class="customer-select" required>
            {% for r in records %}<option value="{{ r.owner }}">{{ r.owner }}</option>{% endfor %}
          </select>
        </div>
        <div><label>进货日期 *</label><input name="date" type="date" value="{{ today }}" required></div>
        <div><label>斤数 *</label><input name="quantity" type="number" step="0.1" min="0.1" placeholder="如：1000" required></div>
        <div><label>单价（元/斤）</label><input name="price_per_jin" type="number" step="0.01" placeholder="如：3.4"></div>
        <div>
          <label>账户类型</label>
          <select name="account_type">
            <option value="personal">对私（微信/支付宝）</option>
            <option value="corporate">对公（公户转账）</option>
          </select>
        </div>
        <div><label>结账日期</label><input name="settle_date" type="date" placeholder="如：2026-04-30"></div>
        <div class="full"><label>备注</label><input name="note" placeholder="如：第二批货"></div>
      </div>
      <div class="btn-row"><button type="submit" class="btn btn-primary">💾 添加进货记录</button></div>
    </form>
  </div>

  <div class="card">
    <div class="card-title">📋 全部进货记录</div>
    {% if all_purchases %}
    <table>
      <thead><tr><th>客户</th><th>日期</th><th>斤数</th><th>单价</th><th>金额</th><th>类型</th><th>付款状态</th><th>结账日</th><th>操作</th></tr></thead>
      <tbody>
      {% for p in all_purchases %}
        <tr>
          <td><strong>{{ p.owner }}</strong></td>
          <td>{{ p.date }}</td>
          <td>{{ p.quantity }} 斤</td>
          <td>{% if p.price_per_jin %}{{ p.price_per_jin }}元{% else %}-{% endif %}</td>
          <td>{% if p.total_amount %}{{ p.total_amount }}元{% else %}-{% endif %}</td>
          <td>{% if p.account_type == 'corporate' %}<span class="badge badge-corporate">对公</span>{% else %}<span class="badge badge-gray">对私</span>{% endif %}</td>
          <td>
            {% if p.paid %}<span class="badge badge-green">已付</span>
            {% else %}<span class="badge badge-red">未付</span>{% endif %}
          </td>
          <td>{% if p.settle_date %}{{ p.settle_date }}{% else %}-{% endif %}</td>
          <td>
            <div class="action-btns">
              {% if not p.paid %}
              <form method="post" action="/api/mark-paid/{{ p.customer_idx }}/{{ p.purchase_idx }}">
                <button type="submit" class="btn-pay">✓ 已付</button>
              </form>
              {% endif %}
            </div>
          </td>
        </tr>
      {% endfor %}
      </tbody>
    </table>
    {% else %}
    <div class="empty"><div class="empty-icon">📝</div><div>暂无进货记录</div></div>
    {% endif %}
  </div>
</div>

<!-- Tab 3: 对账管理 -->
<div id="reconcile" class="tab-content">
  <div class="card">
    <div class="card-title">📅 月度对账单</div>
    <form method="get" action="/" style="margin-bottom:16px">
      <label>选择月份：</label>
      <select name="month" class="month-select" onchange="this.form.submit()">
        {% for m in months %}
        <option value="{{ m }}" {% if m == selected_month %}selected{% endif %}>{{ m }}</option>
        {% endfor %}
      </select>
      <input type="hidden" name="tab" value="reconcile">
    </form>

    {% if month_data %}
    <div class="stats-row">
      <div class="stat-card"><div class="num">{{ month_data.total_jin }}</div><div class="label">进货总量(斤)</div></div>
      <div class="stat-card"><div class="num">¥{{ month_data.total_amount }}</div><div class="label">总金额</div></div>
      <div class="stat-card success"><div class="num">¥{{ month_data.paid_amount }}</div><div class="label">已付金额</div></div>
      <div class="stat-card danger"><div class="num">¥{{ month_data.unpaid_amount }}</div><div class="label">待收金额</div></div>
    </div>

    <table>
      <thead><tr><th>客户</th><th>进货斤数</th><th>金额</th><th>已付</th><th>欠款</th><th>类型</th><th>结账日</th><th>操作</th></tr></thead>
      <tbody>
      {% for r in month_data.customers %}
        <tr>
          <td><strong>{{ r.owner }}</strong></td>
          <td>{{ r.total_jin }} 斤</td>
          <td>¥{{ r.total_amount }}</td>
          <td>{% if r.paid %}<span class="badge badge-green">已付清</span>{% else %}<span class="badge badge-red">未付</span>{% endif %}</td>
          <td style="color:#d63031;font-weight:700">¥{{ r.unpaid }}</td>
          <td>{% if r.account_type == 'corporate' %}<span class="badge badge-corporate">对公</span>{% else %}<span class="badge badge-gray">对私</span>{% endif %}</td>
          <td>{% if r.settle_date %}{{ r.settle_date }}{% else %}-{% endif %}</td>
          <td>
            {% if r.unpaid > 0 %}
            <form method="post" action="/api/mark-paid/{{ r.customer_idx }}/{{ r.purchase_idx }}">
              <button type="submit" class="btn-pay">标记已付</button>
            </form>
            {% endif %}
          </td>
        </tr>
      {% endfor %}
      </tbody>
    </table>
    {% else %}
    <div class="empty"><div class="empty-icon">💰</div><div>该月无对账记录</div></div>
    {% endif %}
  </div>

  <!-- 到期提醒 -->
  {% if settle_alerts %}
  <div class="card">
    <div class="card-title">⚠️ 到期未付款提醒</div>
    <table>
      <thead><tr><th>客户</th><th>金额</th><th>结账日</th><th>类型</th><th>操作</th></tr></thead>
      <tbody>
      {% for a in settle_alerts %}
        <tr>
          <td><strong>{{ a.owner }}</strong></td>
          <td style="color:#d63031;font-weight:700">¥{{ a.amount }}</td>
          <td>{{ a.settle_date }}</td>
          <td>{% if a.account_type == 'corporate' %}<span class="badge badge-corporate">对公</span>{% else %}<span class="badge badge-gray">对私</span>{% endif %}</td>
          <td>
            <form method="post" action="/api/mark-paid/{{ a.customer_idx }}/{{ a.purchase_idx }}">
              <button type="submit" class="btn-pay">确认收款</button>
            </form>
          </td>
        </tr>
      {% endfor %}
      </tbody>
    </table>
  </div>
  {% endif %}
</div>

<div style="text-align:center;color:#bbb;font-size:0.75em;padding:20px 0">
  数据文件：{{ data_file }}
</div>
</div>

<script>
function showTab(tabId) {
  document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  document.getElementById(tabId).classList.add('active');
  event.target.classList.add('active');
}

// 处理 URL 参数中的 tab
const params = new URLSearchParams(window.location.search);
if (params.get('tab')) {
  showTab(params.get('tab'));
}
</script>
</body>
</html>"""

# ── 路由 ────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    records = load_records()
    today_str = date.today().isoformat()
    
    # 计算每个客户的库存信息
    urgent_count = 0
    total_stock = 0
    settle_alerts = []
    all_purchases = []
    
    for idx, r in enumerate(records):
        stock_info = get_stock_info(r)
        r["stock_info"] = stock_info
        total_stock += stock_info["total"]
        if stock_info["days_left"] < 0 or stock_info["days_left"] <= 3:
            urgent_count += 1
        
        # 收集进货记录
        for pidx, p in enumerate(r.get("purchases", [])):
            all_purchases.append({
                "owner": r["owner"],
                "customer_idx": idx,
                "purchase_idx": pidx,
                "date": p.get("date", ""),
                "quantity": p.get("quantity", 0),
                "price_per_jin": p.get("price_per_jin", 0),
                "total_amount": p.get("total_amount", 0),
                "paid": p.get("paid", True),
                "settle_date": p.get("settle_date", ""),
                "account_type": p.get("account_type", "personal"),
                "note": p.get("note", "")
            })
        
        # 检查到期未付款
        today = date.today()
        for pidx, p in enumerate(r.get("purchases", [])):
            if not p.get("paid", True) and p.get("settle_date"):
                try:
                    settle_d = datetime.strptime(p["settle_date"], "%Y-%m-%d").date()
                    if settle_d <= today:
                        settle_alerts.append({
                            "owner": r["owner"],
                            "customer_idx": idx,
                            "purchase_idx": pidx,
                            "amount": p.get("total_amount", 0),
                            "settle_date": p["settle_date"],
                            "account_type": p.get("account_type", "personal")
                        })
                except:
                    pass
    
    # 按日期倒序排列进货记录
    all_purchases.sort(key=lambda x: x["date"], reverse=True)
    
    # 月份下拉选项
    months = []
    for i in range(6):
        m = date.today().replace(day=1) - timedelta(days=i*30)
        months.append(m.strftime("%Y-%m"))
    months = list(dict.fromkeys(months))
    
    # 获取选中的月份
    selected_month = request.args.get("month", months[0] if months else date.today().strftime("%Y-%m"))
    
    # 月度对账数据
    month_data = None
    if selected_month:
        month_customers = {}
        for r in records:
            for pidx, p in enumerate(r.get("purchases", [])):
                p_date = p.get("date", "")
                if p_date.startswith(selected_month):
                    owner = r["owner"]
                    if owner not in month_customers:
                        month_customers[owner] = {
                            "owner": owner,
                            "customer_idx": records.index(r),
                            "purchase_idx": pidx,
                            "total_jin": 0,
                            "total_amount": 0,
                            "paid": p.get("paid", True),
                            "paid_amount": 0,
                            "unpaid": 0,
                            "account_type": p.get("account_type", "personal"),
                            "settle_date": p.get("settle_date", "")
                        }
                    mc = month_customers[owner]
                    mc["total_jin"] += p.get("quantity", 0)
                    mc["total_amount"] += p.get("total_amount", 0)
                    if p.get("paid", True):
                        mc["paid_amount"] += p.get("total_amount", 0)
                    mc["unpaid"] = mc["total_amount"] - mc["paid_amount"]
        
        if month_customers:
            total_jin = sum(mc["total_jin"] for mc in month_customers.values())
            total_amt = sum(mc["total_amount"] for mc in month_customers.values())
            paid_amt = sum(mc["paid_amount"] for mc in month_customers.values())
            month_data = {
                "total_jin": total_jin,
                "total_amount": total_amt,
                "paid_amount": paid_amt,
                "unpaid_amount": total_amt - paid_amt,
                "customers": list(month_customers.values())
            }
    
    unsettled_count = len([p for p in all_purchases if not p["paid"]])
    
    return render_template_string(
        INDEX_HTML,
        records=records,
        today=today_str,
        urgent_count=urgent_count,
        unsettled_count=unsettled_count,
        total_stock=total_stock,
        settle_alerts=settle_alerts,
        all_purchases=all_purchases[:50],
        months=months,
        selected_month=selected_month,
        month_data=month_data,
        data_file=str(DATA_FILE),
    )

@app.route("/api/add-customer", methods=["POST"])
def add_customer():
    records = load_records()
    record = {
        "owner": request.form["owner"].strip(),
        "phone": request.form.get("phone", "").strip(),
        "people": int(request.form.get("people", 1)),
        "daily_rate": float(request.form.get("daily_rate", 0.4)),
        "frequency": request.form.get("frequency", "daily"),
        "note": request.form.get("note", "").strip(),
        "purchases": [],
        "created": date.today().isoformat(),
    }
    records.append(record)
    save_records(records)
    return redirect(url_for("index"))

@app.route("/api/purchase", methods=["POST"])
def add_purchase():
    records = load_records()
    owner = request.form["owner"].strip()
    quantity = float(request.form["quantity"])
    price_per_jin = float(request.form.get("price_per_jin") or 0)
    total_amount = round(quantity * price_per_jin, 2) if price_per_jin > 0 else 0
    
    purchase = {
        "date": request.form["date"],
        "quantity": quantity,
        "price_per_jin": price_per_jin,
        "total_amount": total_amount,
        "paid": False,
        "settle_date": request.form.get("settle_date") or "",
        "account_type": request.form.get("account_type", "personal"),
        "note": request.form.get("note", "").strip(),
    }
    
    # 找到客户并添加
    for r in records:
        if r["owner"] == owner:
            if "purchases" not in r:
                r["purchases"] = []
            r["purchases"].append(purchase)
            break
    
    save_records(records)
    return redirect(url_for("index") + "?tab=purchase")

@app.route("/api/mark-paid/<int:customer_idx>/<int:purchase_idx>", methods=["POST"])
def mark_paid(customer_idx, purchase_idx):
    records = load_records()
    if 0 <= customer_idx < len(records):
        r = records[customer_idx]
        if "purchases" in r and 0 <= purchase_idx < len(r["purchases"]):
            r["purchases"][purchase_idx]["paid"] = True
            save_records(records)
    return redirect(url_for("index") + "?tab=" + (request.args.get("tab", "reconcile")))

@app.route("/api/delete-customer/<int:idx>", methods=["POST"])
def delete_customer(idx):
    records = load_records()
    if 0 <= idx < len(records):
        del records[idx]
        save_records(records)
    return redirect(url_for("index"))

@app.route("/api/records")
def api_records():
    records = load_records()
    for r in records:
        r["stock_info"] = get_stock_info(r)
    return jsonify(records)

@app.route("/api/alert")
def api_alert():
    records = load_records()
    alerts = []
    settle_alerts = []
    
    for r in records:
        stock_info = get_stock_info(r)
        if stock_info["days_left"] < 0:
            alerts.append(f"🚨 【{r['owner']}】的大米已耗尽！请立即采购！")
        elif stock_info["days_left"] <= 3:
            alerts.append(f"⚠️ 【{r['owner']}】的大米预计 {stock_info['days_left']} 天后吃完！")
        
        today = date.today()
        for p in r.get("purchases", []):
            if not p.get("paid", True) and p.get("settle_date"):
                try:
                    settle_d = datetime.strptime(p["settle_date"], "%Y-%m-%d").date()
                    if settle_d <= today:
                        acct = "对公转账" if p.get("account_type") == "corporate" else "对私"
                        settle_alerts.append(f"💰 【{r['owner']}】{p.get('settle_date', '')}到期未付款（{p.get('total_amount', 0)}元，{acct}）！")
                except:
                    pass
    
    return jsonify({
        "has_alerts": len(alerts) > 0,
        "alerts": alerts,
        "has_settle_alerts": len(settle_alerts) > 0,
        "settle_alerts": settle_alerts,
        "checked_at": date.today().isoformat(),
    })

# ── 启动 ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print(f"\n🍚 大米采购管理系统 v2.0 已启动")
    print(f"   本地访问：http://localhost:{PORT}")
    print(f"   手机访问：http://<本机IP>:{PORT}")
    print(f"   数据文件：{DATA_FILE}")
    print(f"   按 Ctrl+C 停止服务\n")
    app.run(host=HOST, port=PORT, debug=False)
