---
name: html-report-generator
version: 1.0.0
description: "任意数据输入 → 精美可视化HTML报告页面。触发词：生成报告/精美HTML/可视化页面/数据大屏/制作网页。"
---

# HTML报告生成器 · SKILL.md

## 核心能力

用户给出数据 → 自动生成精美可视化HTML页面 → 直接部署链接

## 使用方法

用户说："帮我把这个数据做成精美HTML页面" → 执行本skill

## 执行流程

### Step 1：分析数据结构
读取用户提供的数据（文字/表格/JSON），确定：
- 有哪些指标/字段
- 数据类型（数值/文本/时间序列）
- 适合的图表类型

### Step 2：选择配色方案
根据主题选择配色：

**科技感（蓝色系）：**
```css
background: #06060f
accent: #00d4ff
gradient: linear-gradient(135deg, #0d1b3e, #0a2540)
```

**品牌感（紫色系）：**
```css
background: #080810
accent: #a78bfa
gradient: linear-gradient(135deg, rgba(139,92,246,0.1), rgba(59,130,246,0.05))
```

**商业感（深灰+金色）：**
```css
background: #0f0f0f
accent: #f5c842
gradient: linear-gradient(135deg, #1a1400, #0d0f00)
```

**医疗/健康（绿色系）：**
```css
background: #040f0a
accent: #34d399
gradient: linear-gradient(135deg, rgba(16,185,129,0.08), rgba(0,0,0,0))
```

### Step 3：生成HTML

使用以下标准组件库：

**组件1：Hero区**
```html
<div class="hero" style="background: linear-gradient(135deg, #0d1b3e, #0a2540); padding: 48px 40px; text-align: center; border-bottom: 1px solid rgba(0,150,255,0.15);">
  <h1 style="font-size:2.2em;font-weight:800;color:#fff;">标题</h1>
  <p style="color:rgba(255,255,255,0.5);margin-top:8px;">副标题</p>
</div>
```

**组件2：KPI数字墙**
```html
<div class="kpi-bar" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin-bottom:32px;">
  <div class="kpi" style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.07);border-radius:12px;padding:20px;text-align:center;">
    <div class="num" style="font-size:1.8em;font-weight:800;color:#00d4ff;">51.9<span style="font-size:0.5em;">%</span></div>
    <div class="label" style="font-size:0.8em;color:rgba(255,255,255,0.4);margin-top:4px;">青少年近视率</div>
  </div>
</div>
```

**组件3：卡片网格**
```html
<div class="card" style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);border-radius:14px;padding:24px;margin-bottom:16px;">
  <h3 style="color:#fff;font-size:1em;margin-bottom:10px;">标题</h3>
  <p style="color:#9a9a9a;font-size:0.85em;line-height:1.7;">描述文字</p>
</div>
```

**组件4：时间线**
```html
<div class="timeline" style="position:relative;padding-left:28px;">
  <div class="timeline::before" style="content:'';position:absolute;left:8px;top:0;bottom:0;width:1px;background:rgba(255,255,255,0.08);"></div>
  <div class="timeline-item" style="position:relative;margin-bottom:20px;">
    <div style="font-size:0.75em;color:#00d4ff;font-weight:600;margin-bottom:2px;">PHASE 1</div>
    <div style="font-weight:600;color:#fff;">阶段名称</div>
    <div style="color:#888;font-size:0.82em;line-height:1.6;">描述</div>
  </div>
</div>
```

**组件5：表格**
```html
<table style="width:100%;border-collapse:collapse;margin-top:12px;">
  <tr>
    <th style="background:rgba(0,212,255,0.1);color:#00d4ff;font-size:0.75em;padding:8px 12px;text-align:left;font-weight:600;border-bottom:1px solid rgba(0,212,255,0.1);">列1</th>
    <th>列2</th>
  </tr>
  <tr>
    <td style="color:#9a9a9a;font-size:0.8em;padding:8px 12px;border-bottom:1px solid rgba(255,255,255,0.04);">内容</td>
    <td style="color:#00d4ff;font-weight:600;">重点</td>
  </tr>
</table>
```

**组件6：标签云**
```html
<div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:10px;">
  <span style="background:rgba(0,212,255,0.08);color:#00d4ff;border:1px solid rgba(0,212,255,0.15);padding:3px 10px;border-radius:10px;font-size:0.78em;">标签</span>
</div>
```

**组件7：引用框**
```html
<div style="background:linear-gradient(135deg,rgba(0,212,255,0.06),rgba(0,100,200,0.04));border-left:3px solid #00d4ff;border-radius:0 12px 12px 0;padding:16px 20px;margin:12px 0;font-size:0.9em;color:rgba(255,255,255,0.8);line-height:1.7;font-style:italic;">
  引用文字
</div>
```

**组件8：双色徽章**
```html
<span style="display:inline-block;background:rgba(255,80,80,0.1);color:#ff6060;border:1px solid rgba(255,80,80,0.2);padding:2px 10px;border-radius:8px;font-size:0.72em;font-weight:700;">高优先级</span>
```

### Step 4：生成完整HTML模板

```html
<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{报告标题}</title>
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  body { font-family:-apple-system,'PingFang SC',sans-serif; background:#06060f; color:#e8e6e3; min-height:100vh; }
  .hero { background:linear-gradient(135deg,#0d1b3e,#0a2540); padding:48px 40px; text-align:center; border-bottom:1px solid rgba(0,150,255,0.15); }
  .hero h1 { font-size:2.2em; font-weight:800; color:#fff; }
  .hero .sub { color:rgba(255,255,255,0.5); font-size:0.95em; margin-top:8px; }
  .container { max-width:960px; margin:0 auto; padding:40px 24px; }
  .section { margin-bottom:40px; }
  .section-title { font-size:1em; font-weight:700; color:#fff; margin-bottom:16px; padding-bottom:8px; border-bottom:1px solid rgba(255,255,255,0.08); }
  .kpi-bar { display:grid; grid-template-columns:repeat(auto-fit,minmax(150px,1fr)); gap:12px; margin-bottom:32px; }
  .card { background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.07); border-radius:14px; padding:24px; margin-bottom:14px; }
  .card h3 { color:#fff; font-size:0.95em; margin-bottom:10px; }
  .card p { color:#9a9a9a; font-size:0.85em; line-height:1.7; }
  .footer { text-align:center; color:#333; font-size:0.75em; padding:40px 0 20px; border-top:1px solid rgba(255,255,255,0.04); margin-top:40px; }
</style>
</head>
<body>
  {内容区}
</body>
</html>
```

### Step 5：部署

```bash
# 保存HTML
write /workspace/{project}/index.html

# 部署
deploy --dist_dir /workspace/{project} --project_name {项目名}
```

## 输出

部署后返回链接，用户可直接打开。

## 设计规范（设计师参考）

| 元素 | 规范 |
|------|------|
| 主背景 | #06060f 或 #080810 |
| 强调色 | #00d4ff（蓝）或 #a78bfa（紫）或 #34d399（绿）|
| 渐变 | linear-gradient(135deg, #0d1b3e, #0a2540) |
| 卡片圆角 | border-radius: 12px~16px |
| 内边距 | padding: 20px~28px |
| 边框 | border: 1px solid rgba(255,255,255,0.06)~0.1 |
| 标题字重 | font-weight: 700~800 |
| 正文字号 | font-size: 0.82em~0.9em |
| 行高 | line-height: 1.6~1.7 |
