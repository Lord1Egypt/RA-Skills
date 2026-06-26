#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大米销售管理系统 v3 - Flask Web App
运行方式：
  python3 app_v3.py
  然后浏览器打开 http://localhost:5001
"""

import json
import os
import uuid
from datetime import date, timedelta, datetime
from flask import Flask, request, jsonify, render_template_string, redirect, url_for
from pathlib import Path

app = Flask(__name__)

DATA_FILE = Path.home() / ".openclaw" / "workspace" / "rice-shop-records.json"
PORT = 5001
HOST = "0.0.0.0"

# ── 数据读写与迁移 ─────────────────────────────────────────────────────────

def load_records():
    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            # 兼容旧数据格式
            if isinstance(data, list):
                # 旧格式：直接是记录列表，每个记录包含 purchase_date, quantity 等
                # 需要迁移到新格式：客户记录 + purchase_history
                new_data = migrate_old_data(data)
                return new_data
            return data
    return []

def migrate_old_data(old_records):
    """将旧格式迁移到新格式"""
    new_records = []
    for r in old_records:
        # 旧格式有 purchase_date，说明是客户记录
        if "purchase_date" in r:
            # 创建新格式的客户记录
            purchase_date = r.get("purchase_date", date.today().isoformat())
            quantity = r.get("quantity", 0)
            daily_rate = r.get("daily_rate", 0.4)
            people = r.get("people", 1)
            frequency = r.get("frequency", "daily")
            
            # 创建订单记录
            order = {
                "id": generate_order_id(),
                "date": purchase_date,
                "quantity": quantity,
                "unit_price": r.get("price_per_jin", 2.5),
                "total_price": quantity * r.get("price_per_jin", 2.5),
                "deliveries": [
                    {"date": purchase_date, "quantity": quantity, "status": "done"}
                ],
                "delivery_status": "done",
                "payment_status": "paid",  # 旧数据默认已付款
                "paid_amount": quantity * r.get("price_per_jin", 2.5),
                "settle_date": calculate_settle_date(purchase_date, "realtime"),
                "bank_account": "",
                "invoice_needed": "no"
            }
            
            # 计算每天消耗总量
            if frequency == "workdays":
                daily_total = people * daily_rate * 5/7
            elif frequency == "weekends":
                daily_total = people * daily_rate * 2/7
            else:
                daily_total = people * daily_rate
            
            new_record = {
                "owner": r.get("owner", ""),
                "phone": r.get("phone", ""),
                "type": "personal",
                "company": "",
                "billing_cycle": "realtime",
                "price_per_jin": r.get("price_per_jin", 2.5),
                "people": people,
                "frequency": frequency,
                "daily_rate": daily_rate,
                "daily_rate_source": "manual",
                "note": r.get("note", ""),
                "purchase_history": [order],
                "learned_cycle_days": None,
                "learned_daily_total": round(daily_total, 2),
                "created": r.get("created", date.today().isoformat())
            }
            new_records.append(new_record)
    return new_records

def generate_order_id():
    """生成8位唯一订单ID"""
    return uuid.uuid4().hex[:8].upper()

def calculate_settle_date(order_date_str, billing_cycle):
    """计算结账日期"""
    order_date = date.fromisoformat(order_date_str)
    if billing_cycle == "realtime":
        return order_date.strftime("%Y-%m-%d")
    elif billing_cycle == "monthly":
        # 月结：下月25号
        if order_date.month == 12:
            next_month = date(order_date.year + 1, 1, 25)
        else:
            next_month = date(order_date.year, order_date.month + 1, 25)
        return next_month.strftime("%Y-%m-%d")
    elif billing_cycle == "quarterly":
        # 季度结：下季度首月25号
        quarter_end_month = ((order_date.month - 1) // 3 + 1) * 3
        if quarter_end_month == 12:
            next_quarter = date(order_date.year + 1, 1, 25)
        elif quarter_end_month > 12:
            next_quarter = date(order_date.year + 1, (quarter_end_month - 12), 25)
        else:
            next_quarter = date(order_date.year, quarter_end_month + 1, 25)
        return next_quarter.strftime("%Y-%m-%d")
    return order_date.strftime("%Y-%m-%d")

def save_records(records):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

# ── 消耗计算 ───────────────────────────────────────────────────────────────

def days_left(record):
    """计算剩余天数（基于最新订单）"""
    if not record.get("purchase_history"):
        return -1
    
    # 获取最新订单
    latest_order = record["purchase_history"][-1]
    today = date.today()
    purchased = date.fromisoformat(latest_order["date"])
    consumed_per_day = record["daily_rate"]
    freq = record.get("frequency", "daily")
    people = record["people"]
    
    # 获取已完成的送货总量
    delivered = sum(
        d["quantity"] for d in latest_order.get("deliveries", [])
        if d["status"] == "done"
    )
    
    if delivered <= 0:
        return 0
    
    if freq == "workdays":
        days = (today - purchased).days + 1
        workdays = sum(1 for i in range(days)
                       if (purchased + timedelta(i)).weekday() < 5)
        total_consumed = workdays * people * consumed_per_day
    elif freq == "weekends":
        days = (today - purchased).days + 1
        weekends = sum(1 for i in range(days)
                       if (purchased + timedelta(i)).weekday() >= 5)
        total_consumed = weekends * people * consumed_per_day
    else:
        total_consumed = (today - purchased).days * people * consumed_per_day
    
    remaining = delivered - total_consumed
    if remaining <= 0:
        return -1
    
    if freq == "workdays":
        days_per_consumed = 1.0 / (people * consumed_per_day)
        return round(remaining * days_per_consumed)
    elif freq == "weekends":
        days_per_consumed = 1.0 / (people * consumed_per_day)
        return round(remaining * days_per_consumed * (7/2))
    else:
        return round(remaining / (people * consumed_per_day))

def expected_date(record):
    d = days_left(record)
    if d < 0:
        return "已吃完"
    return (date.today() + timedelta(days=d)).strftime("%Y-%m-%d")

# ── 复购学习 ───────────────────────────────────────────────────────────────

def learn_from_repurchase(record, new_order_date):
    """复购时学习消耗周期"""
    if not record.get("purchase_history") or len(record["purchase_history"]) < 2:
        return
    
    # 获取上一个订单
    prev_order = record["purchase_history"][-2]
    prev_date = date.fromisoformat(prev_order["date"])
    new_date = date.fromisoformat(new_order_date)
    
    # 计算周期天数
    cycle_days = (new_date - prev_date).days
    if cycle_days > 0:
        record["learned_cycle_days"] = cycle_days
    
    # 计算日均消耗总量
    total_quantity = sum(d["quantity"] for d in prev_order.get("deliveries", []))
    daily_total = total_quantity / max(cycle_days, 1)
    record["learned_daily_total"] = round(daily_total, 2)
    
    # 如果没有手动设置过日消耗，自动设置
    if record.get("daily_rate_source") == "auto" or not record.get("daily_rate"):
        people = record.get("people", 1)
        if people > 0:
            record["daily_rate"] = round(daily_total / people, 2)
            record["daily_rate_source"] = "auto"

# ── HTML 模板 ───────────────────────────────────────────────────────────────

CSS = """
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
    font-family: -apple-system, "PingFang SC", "Microsoft YaHei", sans-serif;
    background: #f0f2f5;
    color: #1a1a2e;
    min-height: 100vh;
}
.container { max-width: 1100px; margin: 0 auto; padding: 20px; }

/* 标签页导航 */
.tabs {
    display: flex;
    gap: 4px;
    margin-bottom: 16px;
    background: #e8e8e8;
    padding: 4px;
    border-radius: 12px;
    overflow-x: auto;
}
.tab {
    padding: 10px 20px;
    border: none;
    background: transparent;
    border-radius: 10px;
    font-size: 0.95em;
    font-weight: 600;
    cursor: pointer;
    color: #666;
    white-space: nowrap;
    transition: all 0.2s;
}
.tab.active {
    background: white;
    color: #0f3460;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
.tab-content { display: none; }
.tab-content.active { display: block; }

/* 标题栏 */
.header {
    background: linear-gradient(135deg, #1a1a2e, #0f3460);
    color: white;
    padding: 20px 24px;
    border-radius: 16px;
    margin-bottom: 20px;
}
.header h1 { font-size: 1.3em; font-weight: 700; }
.header .subtitle { font-size: 0.8em; opacity: 0.7; margin-top: 2px; }
.header .stats {
    display: flex;
    gap: 24px;
    flex-wrap: wrap;
    margin-top: 14px;
}
.header .stat { text-align: center; }
.header .stat .num { font-size: 1.6em; font-weight: 800; }
.header .stat .label { font-size: 0.7em; opacity: 0.7; }

/* 报警横幅 */
.alert-bar {
    background: linear-gradient(90deg, #ff4757, #ff6b81);
    color: white;
    padding: 12px 20px;
    border-radius: 12px;
    margin-bottom: 16px;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 10px;
}
.alert-bar.warn { background: linear-gradient(90deg, #ffa502, #ff6348); }

/* 卡片 */
.card {
    background: white;
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 16px;
    box-shadow: 0 2px 12px rgba(0,0,0,.06);
}

/* 表单 */
.form-title {
    font-size: 1em;
    font-weight: 700;
    color: #0f3460;
    margin-bottom: 14px;
    border-left: 4px solid #e94560;
    padding-left: 10px;
}
.form-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 12px;
}
.form-grid .full { grid-column: 1 / -1; }
.form-grid label {
    font-size: 0.8em;
    color: #666;
    margin-bottom: 4px;
    display: block;
}
.form-grid input,
.form-grid select {
    width: 100%;
    padding: 8px 10px;
    border: 1.5px solid #e0e0e0;
    border-radius: 8px;
    font-size: 0.9em;
    font-family: inherit;
    transition: border-color 0.2s;
    background: #fafafa;
}
.form-grid input:focus,
.form-grid select:focus {
    outline: none;
    border-color: #0f3460;
    background: white;
}
.hint { font-size: 0.72em; color: #999; margin-top: 2px; }
.btn-row {
    display: flex;
    gap: 10px;
    margin-top: 14px;
    flex-wrap: wrap;
}
.btn {
    padding: 9px 18px;
    border: none;
    border-radius: 8px;
    font-size: 0.9em;
    font-weight: 600;
    cursor: pointer;
    font-family: inherit;
    transition: opacity 0.2s, transform 0.1s;
}
.btn:hover { opacity: 0.85; transform: translateY(-1px); }
.btn:active { transform: translateY(0); }
.btn-primary { background: linear-gradient(135deg, #e94560, #c73e54); color: white; }
.btn-secondary { background: #f0f2f5; color: #555; border: 1.5px solid #ddd; }
.btn-danger { background: #ff4757; color: white; padding: 5px 12px; font-size: 0.8em; }
.btn-sm { padding: 5px 12px; font-size: 0.8em; border-radius: 6px; }
.btn-success { background: #00b894; color: white; }

/* 表格 */
.table-title {
    font-size: 1em;
    font-weight: 700;
    color: #0f3460;
    margin-bottom: 12px;
    border-left: 4px solid #0f3460;
    padding-left: 10px;
}
table { width: 100%; border-collapse: collapse; font-size: 0.85em; }
thead tr { background: #f5f5f5; color: #888; }
th { text-align: left; padding: 8px 10px; font-weight: 500; font-size: 0.75em; border-bottom: 2px solid #e8e8e8; }
td { padding: 10px 8px; border-bottom: 1px solid #f0f0f0; vertical-align: middle; }
tr:last-child td { border-bottom: none; }
tr:hover td { background: #fafafa; }

/* 状态标签 */
.badge {
    display: inline-block;
    padding: 3px 9px;
    border-radius: 20px;
    font-size: 0.75em;
    font-weight: 600;
}
.badge-red { background: #ffe5e5; color: #d63031; }
.badge-orange { background: #fff3e0; color: #e17055; }
.badge-green { background: #e5f9ed; color: #00b894; }
.badge-blue { background: #e8f0fe; color: #1565c0; }
.badge-gray { background: #f0f0f0; color: #666; }
.badge-yellow { background: #fff8e1; color: #f39c12; }

/* 送货进度条 */
.progress-bar {
    width: 100%;
    height: 8px;
    background: #eee;
    border-radius: 4px;
    overflow: hidden;
    margin-top: 4px;
}
.progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #00b894, #55efc4);
    border-radius: 4px;
    transition: width 0.3s;
}
.progress-fill.partial { background: linear-gradient(90deg, #f39c12, #fdcb6e); }
.progress-fill.done { background: linear-gradient(90deg, #00b894, #55efc4); }
.progress-fill.pending { background: #ddd; }

/* 金额显示 */
.amount { font-weight: 600; }
.amount.negative { color: #d63031; }
.amount.positive { color: #00b894; }

/* 空状态 */
.empty { text-align: center; padding: 40px; color: #bbb; font-size: 0.9em; }
.empty-icon { font-size: 2.5em; margin-bottom: 10px; }

/* 筛选器 */
.filter-bar {
    display: flex;
    gap: 12px;
    margin-bottom: 14px;
    flex-wrap: wrap;
    align-items: center;
}
.filter-bar select,
.filter-bar input {
    padding: 6px 12px;
    border: 1.5px solid #e0e0e0;
    border-radius: 8px;
    font-size: 0.85em;
}

/* 响应式 */
@media (max-width: 600px) {
    .form-grid { grid-template-columns: 1fr; }
    .tabs { flex-wrap: nowrap; overflow-x: auto; }
    table { font-size: 0.75em; }
    .hide-mobile { display: none; }
}
"""

INDEX_HTML = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>大米销售管理系统 v3</title>
</head>
<body>
""" + CSS + """
<div class="container">

<!-- 标题栏 -->
<div class="header">
  <div>
    <h1>🍚 大米销售管理系统 v3</h1>
    <div class="subtitle">订单 · 欠款 · 对账 · 月报</div>
  </div>
  <div class="stats">
    <div class="stat"><div class="num">{{ customers|length }}</div><div class="label">客户数</div></div>
    <div class="stat"><div class="num" style="color:#ff4757">{{ unpaid_total }}</div><div class="label">未收款(元)</div></div>
    <div class="stat"><div class="num" style="color:#ffa502">{{ pending_deliveries }}</div><div class="label">待送货</div></div>
    <div class="stat"><div class="num" style="color:#d63031">{{ alerts|length }}</div><div class="label">提醒</div></div>
  </div>
</div>

<!-- 标签页导航 -->
<div class="tabs">
  <button class="tab active" onclick="switchTab('overview')">📊 概览</button>
  <button class="tab" onclick="switchTab('orders')">📦 订单</button>
  <button class="tab" onclick="switchTab('debt')">💰 欠款</button>
  <button class="tab" onclick="switchTab('reconciliation')">📋 对账</button>
  <button class="tab" onclick="switchTab('report')">📈 月报</button>
</div>

<!-- 概览标签页 -->
<div id="overview" class="tab-content active">
  <!-- 警告列表 -->
  {% if alerts %}
  <div class="alert-bar {% if urgent_alerts %}warn{% endif %}">
    🚨 <strong>提醒</strong>：{{ alerts|length }} 条待处理
  </div>
  {% endif %}

  <!-- 快速添加表单 -->
  <div class="card">
    <div class="form-title">➕ 快速添加客户</div>
    <form method="post" action="/add_customer">
      <div class="form-grid">
        <div>
          <label>客户姓名 *</label>
          <input name="owner" placeholder="如：张三" required>
        </div>
        <div>
          <label>手机号</label>
          <input name="phone" placeholder="方便联系">
        </div>
        <div>
          <label>客户类型</label>
          <select name="type">
            <option value="personal">个人</option>
            <option value="canteen">食堂/公司</option>
          </select>
        </div>
        <div>
          <label>食堂/公司名称</label>
          <input name="company" placeholder="如：XX公司食堂">
        </div>
        <div>
          <label>对账周期</label>
          <select name="billing_cycle">
            <option value="realtime">实时结账</option>
            <option value="monthly">月结</option>
            <option value="quarterly">季结</option>
          </select>
        </div>
        <div>
          <label>单价(元/斤)</label>
          <input name="price_per_jin" type="number" step="0.1" value="2.5">
        </div>
        <div>
          <label>家庭人口</label>
          <input name="people" type="number" min="1" value="1">
        </div>
        <div>
          <label>消耗频率</label>
          <select name="frequency">
            <option value="daily">每天吃</option>
            <option value="workdays">工作日</option>
            <option value="weekends">周末</option>
          </select>
        </div>
        <div>
          <label>日消耗(斤/人/天)</label>
          <input name="daily_rate" type="number" step="0.05" value="0.4">
        </div>
        <div>
          <label>对公账号</label>
          <input name="bank_account" placeholder="对公转账用">
        </div>
        <div>
          <label>需要发票</label>
          <select name="invoice_needed">
            <option value="no">不需要</option>
            <option value="yes">需要</option>
          </select>
        </div>
        <div class="full">
          <label>备注</label>
          <input name="note" placeholder="可选备注">
        </div>
      </div>
      <div class="btn-row">
        <button type="submit" class="btn btn-primary">💾 添加客户</button>
        <button type="reset" class="btn btn-secondary">🔄 重置</button>
      </div>
    </form>
  </div>

  <!-- 客户概览 -->
  <div class="card">
    <div class="table-title">👥 客户列表（共 {{ customers|length }} 人）</div>
    {% if customers %}
    <table>
      <thead>
        <tr>
          <th>客户</th>
          <th>类型</th>
          <th>最近订单</th>
          <th>剩余天数</th>
          <th>付款状态</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
      {% for c in customers %}
        <tr>
          <td>
            <strong>{{ c.owner }}</strong>
            {% if c.phone %}<br><span style="font-size:0.75em;color:#999">{{ c.phone }}</span>{% endif %}
          </td>
          <td>
            {% if c.type == 'canteen' %}
              <span class="badge badge-blue">食堂</span>
              {% if c.company %}<br><span style="font-size:0.75em">{{ c.company }}</span>{% endif %}
            {% else %}
              <span class="badge badge-gray">个人</span>
            {% endif %}
          </td>
          <td>
            {% if c.purchase_history %}
              {{ c.purchase_history[-1].quantity }}斤
              <br><span style="font-size:0.75em;color:#999">{{ c.purchase_history[-1].date }}</span>
            {% else %}
              <span style="color:#ccc">暂无订单</span>
            {% endif %}
          </td>
          <td style="text-align:center">
            {% set dl = c.days_left %}
            {% if dl < 0 %}
              <span style="color:#d63031;font-weight:700">已吃完</span>
            {% elif dl <= 3 %}
              <span style="color:#d63031;font-weight:700">{{ dl }}天</span>
            {% elif dl <= 7 %}
              <span style="color:#e17055;font-weight:700">{{ dl }}天</span>
            {% else %}
              <span style="color:#00b894;font-weight:700">{{ dl }}天</span>
            {% endif %}
          </td>
          <td>
            {% if c.purchase_history %}
              {% set order = c.purchase_history[-1] %}
              {% if order.payment_status == 'paid' %}
                <span class="badge badge-green">已付</span>
              {% elif order.payment_status == 'partial' %}
                <span class="badge badge-orange">部分 {{ order.paid_amount }}/{{ order.total_price }}</span>
              {% else %}
                <span class="badge badge-red">未付 {{ order.total_price }}元</span>
              {% endif %}
            {% endif %}
          </td>
          <td>
            <button class="btn btn-sm btn-secondary" onclick="showAddOrder('{{ c.owner }}')">➕ 订单</button>
          </td>
        </tr>
      {% endfor %}
      </tbody>
    </table>
    {% else %}
    <div class="empty"><div class="empty-icon">👥</div><div>暂无客户，请添加第一个客户</div></div>
    {% endif %}
  </div>
</div>

<!-- 订单标签页 -->
<div id="orders" class="tab-content">
  <div class="card">
    <div class="table-title">📦 全部订单</div>
    <table>
      <thead>
        <tr>
          <th>订单号</th>
          <th>客户</th>
          <th>日期</th>
          <th>数量</th>
          <th>金额</th>
          <th>送货进度</th>
          <th>状态</th>
        </tr>
      </thead>
      <tbody>
      {% for c in customers %}
        {% for order in c.purchase_history %}
        <tr>
          <td><code>{{ order.id }}</code></td>
          <td>{{ c.owner }}</td>
          <td>{{ order.date }}</td>
          <td>{{ order.quantity }}斤</td>
          <td>¥{{ order.total_price }}</td>
          <td>
            {% set delivered = order.deliveries|selectattr('status', 'equalto', 'done')|list|length %}
            {% set total = order.deliveries|length %}
            <div class="progress-bar">
              <div class="progress-fill {% if delivered == total %}done{% elif delivered > 0 %}partial{% else %}pending{% endif %}" 
                   style="width: {{ (delivered / total * 100)|round }}%"></div>
            </div>
            <span style="font-size:0.7em;color:#999">{{ delivered }}/{{ total }}批</span>
          </td>
          <td>
            {% if order.payment_status == 'paid' %}
              <span class="badge badge-green">已完成</span>
            {% elif order.delivery_status == 'partial' %}
              <span class="badge badge-orange">送货中</span>
            {% else %}
              <span class="badge badge-red">待送货</span>
            {% endif %}
          </td>
        </tr>
        {% endfor %}
      {% endfor %}
      </tbody>
    </table>
  </div>
</div>

<!-- 欠款标签页 -->
<div id="debt" class="tab-content">
  <div class="card">
    <div class="table-title">💰 欠款统计</div>
    <div class="filter-bar">
      <span>总未收：<strong class="amount negative">¥{{ unpaid_total }}</strong></span>
    </div>
    <table>
      <thead>
        <tr>
          <th>客户</th>
          <th>订单号</th>
          <th>订单金额</th>
          <th>已付</th>
          <th>欠款</th>
          <th>状态</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
      {% set has_debt = false %}
      {% for c in customers %}
        {% for order in c.purchase_history %}
          {% if order.payment_status in ['unpaid', 'partial'] %}
            {% set has_debt = true %}
            <tr>
              <td>{{ c.owner }}</td>
              <td><code>{{ order.id }}</code></td>
              <td>¥{{ order.total_price }}</td>
              <td>¥{{ order.paid_amount }}</td>
              <td><strong class="amount negative">¥{{ order.total_price - order.paid_amount }}</strong></td>
              <td>
                {% if order.payment_status == 'unpaid' %}
                  <span class="badge badge-red">未付款</span>
                {% else %}
                  <span class="badge badge-orange">部分付款</span>
                {% endif %}
              </td>
              <td>
                <form method="post" action="/payment/{{ order.id }}" style="display:inline">
                  <input type="number" name="amount" placeholder="金额" style="width:80px;padding:4px" step="0.01" required>
                  <button type="submit" class="btn btn-sm btn-success">付款</button>
                </form>
              </td>
            </tr>
          {% endif %}
        {% endfor %}
      {% endfor %}
      {% if not has_debt %}
      <tr><td colspan="7" style="text-align:center;color:#999;padding:30px">暂无欠款</td></tr>
      {% endif %}
      </tbody>
    </table>
  </div>
</div>

<!-- 对账标签页 -->
<div id="reconciliation" class="tab-content">
  <div class="card">
    <div class="table-title">📋 对账提醒</div>
    <table>
      <thead>
        <tr>
          <th>客户</th>
          <th>对账周期</th>
          <th>结账日期</th>
          <th>状态</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
      {% for c in customers %}
        {% if c.purchase_history %}
          {% set order = c.purchase_history[-1] %}
          <tr>
            <td>
              {{ c.owner }}
              {% if c.type == 'canteen' and c.company %}<br><span style="font-size:0.75em;color:#999">{{ c.company }}</span>{% endif %}
            </td>
            <td>
              {% if c.billing_cycle == 'realtime' %}<span class="badge badge-green">实时</span>
              {% elif c.billing_cycle == 'monthly' %}<span class="badge badge-blue">月结</span>
              {% else %}<span class="badge badge-yellow">季结</span>{% endif %}
            </td>
            <td>{{ order.settle_date }}</td>
            <td>
              {% set days_until = (date.fromisoformat(order.settle_date) - today).days %}
              {% if days_until < 0 %}
                <span class="badge badge-red">已逾期</span>
              {% elif days_until <= 3 %}
                <span class="badge badge-orange">即将到期</span>
              {% else %}
                <span class="badge badge-green">正常</span>
              {% endif %}
            </td>
            <td>
              {% if c.billing_cycle != 'realtime' %}
                <button class="btn btn-sm btn-secondary" onclick="settleBill('{{ c.owner }}')">结账</button>
              {% endif %}
            </td>
          </tr>
        {% endif %}
      {% endfor %}
      </tbody>
    </table>
  </div>
</div>

<!-- 月报标签页 -->
<div id="report" class="tab-content">
  <div class="card">
    <div class="table-title">📈 月度统计</div>
    <div class="filter-bar">
      <select id="reportYear" onchange="loadReport()">
        {% for y in range(2024, 2027) %}
        <option value="{{ y }}" {% if y == report_year %}selected{% endif %}>{{ y }}年</option>
        {% endfor %}
      </select>
      <select id="reportMonth" onchange="loadReport()">
        {% for m in range(1, 13) %}
        <option value="{{ m }}" {% if m == report_month %}selected{% endif %}>{{ m }}月</option>
        {% endfor %}
      </select>
    </div>
    
    <div class="stats" style="margin-bottom:16px">
      <div class="stat"><div class="num">{{ report.total_quantity }}</div><div class="label">进货量(斤)</div></div>
      <div class="stat"><div class="num">¥{{ report.total_amount }}</div><div class="label">总金额</div></div>
      <div class="stat"><div class="num" style="color:#00b894">¥{{ report.paid_amount }}</div><div class="label">已收款</div></div>
      <div class="stat"><div class="num" style="color:#d63031">¥{{ report.unpaid_amount }}</div><div class="label">未收款</div></div>
    </div>

    <table>
      <thead>
        <tr>
          <th>客户</th>
          <th>订单数</th>
          <th>进货量</th>
          <th>金额</th>
          <th>已收</th>
          <th>未收</th>
        </tr>
      </thead>
      <tbody>
      {% for item in report.details %}
        <tr>
          <td>{{ item.name }}</td>
          <td>{{ item.order_count }}</td>
          <td>{{ item.quantity }}斤</td>
          <td>¥{{ item.amount }}</td>
          <td class="amount positive">¥{{ item.paid }}</td>
          <td class="amount negative">¥{{ item.unpaid }}</td>
        </tr>
      {% endfor %}
      {% if not report.details %}
      <tr><td colspan="6" style="text-align:center;color:#999;padding:30px">该月无数据</td></tr>
      {% endif %}
      </tbody>
    </table>
  </div>
</div>

<!-- 底部 -->
<div style="text-align:center;color:#bbb;font-size:0.75em;padding:20px 0">
  数据：{{ data_file }} · 端口 {{ port }}
</div>

<script>
function switchTab(tabId) {
  document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  document.getElementById(tabId).classList.add('active');
  event.target.classList.add('active');
}

function loadReport() {
  const year = document.getElementById('reportYear').value;
  const month = document.getElementById('reportMonth').value;
  window.location.href = '/report?year=' + year + '&month=' + month;
}

function showAddOrder(owner) {
  const qty = prompt('请输入购买斤数：');
  if (qty) {
    const price = prompt('请输入单价(元/斤)：', '2.5');
    if (price !== null) {
      const form = document.createElement('form');
      form.method = 'POST';
      form.action = '/add_order';
      
      const ownerInput = document.createElement('input');
      ownerInput.name = 'owner';
      ownerInput.value = owner;
      form.appendChild(ownerInput);
      
      const qtyInput = document.createElement('input');
      qtyInput.name = 'quantity';
      qtyInput.value =