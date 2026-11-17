---
name: de-ai
description: 自动扫描项目生成HTML检测报告，检测AI常用色、Emoji图标、英文报错暴露，支持一键替换为专业品牌风格。触发词：去掉AI味道、UI美化、专业化、统一配色、去除AI味、de-ai、品牌风格
version: 1.0.0
author: moan19921019-code
tags:
  - UI美化
  - 品牌设计
  - 前端优化
  - 去AI味道
  - 配色替换
homepage: https://github.com/moan19921019-code/remove-ai-sence
license: MIT
---

# 去除 AI 味道 · UI 美化 Skill

## 何时使用

- 用户说"去掉AI味道"、"UI美化"、"专业化"、"统一配色"
- 产品界面看起来像 AI 生成的（紫色系、大 emoji、AI 徽章）
- 需要建立品牌 UI 规范并自动修复

## 执行流程

### Step 1: 扫描检测

扫描目标目录中所有前端文件（HTML/CSS/JS/Vue/React），检测以下三类"AI 味道"：

| 类别 | 检测规则 | 严重程度 |
|------|---------|---------|
| **AI常用色** | 紫色系：`#6366f1` `#4f46e5` `#4338ca` `#8b5cf6` `#7c3aed` `#6d28d9` `#a78bfa` `#c4b5fd` `#ddd6fe` `#ede9fe` `#f5f3ff` `#eef2ff` `#e0e7ff` `#c7d2fe` `#818cf8` `#3730a3` `#a5b4fc` `rgba(99,102,241,*)` / 霓虹粉：`#d946ef` `#c026d3` `#e879f9` `#f0abfc` `#fae8ff` `#ff00ff` `#ff1493` / 彩虹渐变含 purple/violet/indigo | 高 |
| **Emoji图标** | 按钮/标签/标题中使用彩色 emoji（📊📝💾🤖✨ 等）代替专业图标 | 中 |
| **英文技术报错** | 前端 `catch(e) { alert(... e.message ...) }` 把浏览器/网络层的英文错误直接抛给用户 | 高 |
| **AI 标签（可选）** | `🤖` `AI 分析` `AI 解读` `AI生成` `AI助手` `重新AI分析` — 默认不替换，用户确认后执行 | 低 |

### Step 2: 生成 HTML 检测报告（必须）

**扫描完成后必须生成一个独立的 HTML 报告文件**，保存到项目根目录，命名 `AI味道检测报告_{日期}.html`。

报告需包含：
1. **顶部汇总卡片**：各维度检测数量和严重程度
2. **维度一表格**：AI常用色 — 文件、行号、当前值、建议替换值
3. **维度二表格**：Emoji图标 — 按文件分组，列出每处 emoji 及其建议 SVG
4. **维度三表格**：英文报错暴露 — 列出每处 `e.message` 的模式和修复建议
5. **底部优先级**：P0/P1/P2 修复建议和预估工作量

**报告 HTML 模板：**

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>AI味道检测报告 — {项目名}</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'Microsoft YaHei',sans-serif;background:#f5f6fa;color:#1e293b;padding:40px 20px}
.report{max-width:1100px;margin:0 auto}
.header{background:linear-gradient(135deg,#0B1A3B,#162D5A);color:#fff;padding:36px 32px 28px;border-radius:16px;margin-bottom:24px}
.header h1{font-size:24px;font-weight:900}
.header .sub{font-size:14px;color:#94a3b8;margin-top:4px}
.header .meta{font-size:12px;color:#64748b;margin-top:12px;padding-top:12px;border-top:1px solid rgba(255,255,255,.1)}
.summary{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:14px;margin-bottom:28px}
.summary-card{background:#fff;border-radius:14px;padding:24px;border:1px solid #e5e7eb;text-align:center}
.summary-card .count{font-size:42px;font-weight:900}
.summary-card .label{font-size:13px;color:#64748b;margin-top:6px}
.section{background:#fff;border-radius:14px;padding:28px;margin-bottom:18px;border:1px solid #e5e7eb}
.section h2{font-size:17px;margin-bottom:20px}
.badge{font-size:11px;padding:3px 10px;border-radius:12px;font-weight:700}
.badge-red{background:#fef2f2;color:#dc2626}.badge-amber{background:#fffbeb;color:#d97706}.badge-blue{background:#eff6ff;color:#2563eb}
table{width:100%;border-collapse:collapse;font-size:13px;margin-bottom:12px}
th{background:#f1f5f9;padding:9px 14px;text-align:left;font-weight:600;color:#475569;border-bottom:2px solid #e2e8f0;font-size:11px}
td{padding:8px 14px;border-bottom:1px solid #f0f0f0;vertical-align:top;line-height:1.5}
tr:hover td{background:#fafbfc}
.file{font-family:Consolas,monospace;font-size:12px;color:#3b82f6}
.line{font-family:Consolas,monospace;font-size:11px;color:#94a3b8}
.code{font-family:Consolas,monospace;font-size:12px;background:#f8fafc;padding:3px 8px;border-radius:5px;word-break:break-all}
.severity{display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:4px}
.sev-high{background:#ef4444}.sev-med{background:#f59e0b}.sev-low{background:#3b82f6}
.rec{color:#10b981;font-size:12px}
h3{font-size:14px;color:#334155;margin:24px 0 12px;padding-bottom:8px;border-bottom:1px solid #f1f5f9}
.footer{text-align:center;padding:24px;color:#9ca3af;font-size:11px}
/* 预览列样式 */
.preview-col{width:180px;min-width:140px}
.preview-compare{display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.preview-before,.preview-after{display:flex;flex-direction:column;align-items:center;gap:3px}
.preview-label{font-size:9px;color:#94a3b8;text-transform:uppercase;letter-spacing:.5px}
.preview-swatch{width:40px;height:24px;border-radius:5px;border:1px solid #e5e7eb;display:inline-block;flex-shrink:0}
.preview-swatch-after{width:40px;height:24px;border-radius:5px;border:1px solid #10b981;display:inline-block;flex-shrink:0}
.preview-arrow{color:#94a3b8;font-size:11px;flex-shrink:0}
.preview-emoji-render{font-size:32px;line-height:1.2;text-align:center}
.preview-emoji-after{width:32px;height:32px;display:flex;align-items:center;justify-content:center}
.preview-toast{font-size:11px;padding:8px 12px;border-radius:6px;max-width:340px;line-height:1.4}
.preview-toast-error{background:#fef2f2;border:1px solid #fecaca;color:#dc2626}
.preview-toast-fixed{background:#f0fdf4;border:1px solid #bbf7d0;color:#16a34a}
.preview-toast-label{font-size:9px;font-weight:700;margin-bottom:3px;text-transform:uppercase;letter-spacing:.5px}
/* SVG 图标通用 */
.icon-svg{display:inline-block;vertical-align:middle;flex-shrink:0}
.icon-lg{width:36px;height:36px}
.icon-md{width:20px;height:20px}
</style></head>
<body><div class="report">
<div class="header"><h1><svg class="icon-svg icon-lg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="10.5" cy="10.5" r="6.5"/><line x1="15.5" y1="15.5" x2="21" y2="21"/></svg> AI 味道检测报告</h1><div class="sub">{项目名}</div><div class="meta">扫描范围：{扫描范围} | 检测维度：AI常用色 / Emoji图标 / 英文报错 | 扫描时间：{日期}</div></div>
<div class="summary">
  <div class="summary-card"><div style="margin-bottom:4px"><svg class="icon-svg icon-lg" viewBox="0 0 24 24" fill="none" stroke="#ef4444" stroke-width="1.5"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="3"/><circle cx="5" cy="7" r="2.5"/><circle cx="19" cy="7" r="2.5"/><circle cx="19" cy="17" r="2.5"/><circle cx="5" cy="17" r="2.5"/></svg></div><div class="count" style="color:#ef4444">{紫色数}</div><div class="label">AI 常用色残留</div></div>
  <div class="summary-card"><div style="margin-bottom:4px"><svg class="icon-svg icon-lg" viewBox="0 0 24 24" fill="none" stroke="#f59e0b" stroke-width="1.5"><circle cx="12" cy="12" r="10"/><path d="M8 14s1.5 2 4 2 4-2 4-2"/><line x1="9" y1="9" x2="9.01" y2="9"/><line x1="15" y1="9" x2="15.01" y2="9"/></svg></div><div class="count" style="color:#f59e0b">{emoji数}</div><div class="label">Emoji 图标</div></div>
  <div class="summary-card"><div style="margin-bottom:4px"><svg class="icon-svg icon-lg" viewBox="0 0 24 24" fill="none" stroke="#ef4444" stroke-width="1.5"><path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/></svg></div><div class="count" style="color:#ef4444">{报错数}</div><div class="label">英文技术报错暴露</div></div>
</div>
<!-- 维度一：AI常用色 -->
<div class="section"><h2><span class="badge badge-red">维度一</span> AI 常用色 <span style="font-size:12px;color:#94a3b8">检测：紫色系 + 霓虹粉 + 彩虹渐变</span></h2>
<table><thead><tr><th></th><th>文件</th><th>行号</th><th>色块预览</th><th>当前值</th><th>建议替换</th></tr></thead><tbody>
{颜色表格行}
</tbody></table></div>
<!-- 维度二：Emoji 图标 -->
<div class="section"><h2><span class="badge badge-amber">维度二</span> Emoji 图标 → SVG</h2>
<p style="font-size:13px;color:#64748b;margin-bottom:16px">表格按文件分组，预览列展示 Emoji 在 UI 中的真实渲染效果及 SVG 替换方案。</p>
<table><thead><tr><th></th><th>文件</th><th>行号</th><th>图标预览</th><th>当前 Emoji</th><th>建议 SVG</th></tr></thead><tbody>
{emoji表格行}
</tbody></table>
</div>
<!-- 维度三：英文报错 -->
<div class="section"><h2><span class="badge badge-red">维度三</span> 英文技术报错暴露给用户</h2>
<p style="font-size:13px;color:#64748b;margin-bottom:16px"><code>e.message</code> 会把浏览器/网络层的英文错误直接抛给用户，应替换为友好中文提示。</p>
<table><thead><tr><th></th><th>文件</th><th>行号</th><th>错误效果模拟</th><th>当前暴露方式</th></tr></thead><tbody>
{报错表格行}
</tbody></table></div>
<!-- 修复优先级 -->
<div class="section"><h2><svg class="icon-svg icon-md" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-right:6px"><rect x="4" y="3" width="16" height="18" rx="2"/><line x1="8" y1="8" x2="16" y2="8"/><line x1="8" y1="12" x2="16" y2="12"/><line x1="8" y1="16" x2="12" y2="16"/></svg> 修复优先级</h2>
<table><thead><tr><th>优先级</th><th>维度</th><th>数量</th><th>修复方案</th><th>预估工作量</th></tr></thead><tbody>
<tr><td style="color:#ef4444;font-weight:700">P0</td><td>报错暴露 e.message</td><td>{报错数}处</td><td>friendlyError() 工具函数统一包装</td><td>30分钟</td></tr>
<tr><td style="color:#f59e0b;font-weight:700">P1</td><td>Emoji → SVG</td><td>{emoji数}处</td><td>SVG icon 组件替换</td><td>1-2小时</td></tr>
<tr><td style="color:#3b82f6;font-weight:700">P2</td><td>AI常用色</td><td>{紫色数}处</td><td>按映射表批量替换</td><td>5分钟</td></tr>
</tbody></table></div>
<div class="footer">de-ai 检测报告 · {日期}</div>
</div></body></html>
```

**关键要求**：
- 三个维度都要有具体的表格，每行标注文件、行号、当前内容和建议
- **所有表格必须包含预览列**，展示修复前后的视觉对比（色块对比 / Emoji渲染 / 报错模拟）
- Emoji 表格按文件分组，列出每个 emoji 及其用途
- 报告文件写入后用浏览器打开供用户查看
- 报告底部必须有优先级排序（P0报错 > P1图标 > P2颜色）

**各维度表格行的 HTML 模板：**

维度一（颜色）每行格式 — 包含色块修复前后对比：
```html
<tr>
  <td><span class="severity sev-high"></span></td>
  <td class="file">styles.css</td>
  <td class="line">L42</td>
  <td class="preview-col">
    <div class="preview-compare">
      <div class="preview-before">
        <span class="preview-swatch" style="background:#6366f1"></span>
        <span class="preview-label">修复前</span>
      </div>
      <span class="preview-arrow">→</span>
      <div class="preview-after">
        <span class="preview-swatch-after" style="background:#3b82f6"></span>
        <span class="preview-label">修复后</span>
      </div>
    </div>
  </td>
  <td><code class="code">#6366f1</code></td>
  <td><code class="code rec">#3b82f6</code></td>
</tr>
```

维度二（Emoji）每行格式 — 包含 Emoji 渲染与 SVG 对比：
```html
<tr>
  <td><span class="severity sev-med"></span></td>
  <td class="file">index.html</td>
  <td class="line">L28</td>
  <td class="preview-col">
    <div class="preview-compare">
      <div class="preview-before">
        <span class="preview-emoji-render">📊</span>
        <span class="preview-label">修复前</span>
      </div>
      <span class="preview-arrow">→</span>
      <div class="preview-after">
        <span class="preview-emoji-after"><svg width="32" height="32" viewBox="0 0 16 16"><rect x="1" y="3" width="3" height="10" rx="0.5"/><rect x="6.5" y="1" width="3" height="12" rx="0.5"/><rect x="12" y="5" width="3" height="8" rx="0.5"/></svg></span>
        <span class="preview-label">修复后</span>
      </div>
    </div>
  </td>
  <td>📊</td>
  <td>条形图 SVG（见映射表）</td>
</tr>
```

维度三（报错）每行格式 — 包含错误弹窗模拟与修复对比：
```html
<tr>
  <td><span class="severity sev-high"></span></td>
  <td class="file">app.js</td>
  <td class="line">L156</td>
  <td class="preview-col">
    <div class="preview-compare" style="flex-direction:column;align-items:stretch;gap:6px">
      <div class="preview-toast preview-toast-error">
        <div class="preview-toast-label" style="color:#dc2626">修复前 · 用户看到</div>
        Failed to fetch: NetworkError
      </div>
      <div class="preview-toast preview-toast-fixed">
        <div class="preview-toast-label" style="color:#16a34a">修复后 · 用户看到</div>
        网络连接不畅，请检查网络后重试
      </div>
    </div>
  </td>
  <td><code class="code">alert('Failed: ' + e.message)</code></td>
</tr>
```

### Step 3: 确认后执行替换

替换前**必须让用户选择配色方案**，不强制默认蓝色。

#### 配色方案选项

展示给用户选择：

```
请选择替换配色方案：

A. 品牌蓝（推荐） — #3b82f6 系列，专业稳重，适合企业产品
B. 科技青        — #0891b2 系列，明快现代，适合SaaS/工具
C. 深灰          — #4b5563 系列，极简中性，适合数据面板
D. 自定义        — 你指定主色，我自动计算配套色阶
```

#### 各方案完整映射

| 紫色（AI味道） | A.品牌蓝 | B.科技青 | C.深灰 | 典型用途 |
|---------------|---------|---------|--------|---------|
| `#6366f1` | `#3b82f6` | `#0891b2` | `#4b5563` | 按钮、链接、边框 |
| `#4f46e5` | `#2563eb` | `#0e7490` | `#374151` | hover 状态 |
| `#4338ca` | `#1d4ed8` | `#155e75` | `#1f2937` | 深色文字 |
| `#8b5cf6` | `#3b82f6` | `#0891b2` | `#4b5563` | 品牌按钮 |
| `#7c3aed` | `#2563eb` | `#0e7490` | `#374151` | 按钮 hover |
| `#a78bfa` | `#60a5fa` | `#22d3ee` | `#9ca3af` | 浅色图标 |
| `#c4b5fd` | `#93c3fd` | `#67e8f9` | `#d1d5db` | 浅色边框 |
| `#ddd6fe` | `#bfdbfe` | `#a5f3fc` | `#e5e7eb` | 卡片边框 |
| `#ede9fe` | `#dbeafe` | `#cffafe` | `#f3f4f6` | 浅色背景 |
| `#f5f3ff` | `#eff6ff` | `#ecfeff` | `#f9fafb` | 最浅背景 |
| `#e0e7ff` | `#dbeafe` | `#cffafe` | `#f3f4f6` | Badge 背景 |
| `#eef2ff` | `#eff6ff` | `#ecfeff` | `#f9fafb` | 选中背景 |
| `#818cf8` | `#93c3fd` | `#67e8f9` | `#d1d5db` | 边框 |
| `#c7d2fe` | `#bfdbfe` | `#a5f3fc` | `#e5e7eb` | 选中态边框 |
| `#3730a3` | `#1e40af` | `#164e63` | `#111827` | 深色 hover 文字 |
| `#a5b4fc` | `#93c3fd` | `#67e8f9` | `#d1d5db` | 标签边框 |
| `rgba(99,102,241,X)` | `rgba(59,130,246,X)` | `rgba(8,145,178,X)` | `rgba(75,85,99,X)` | 半透明 |

#### 霓虹粉 → 各方案映射

| 霓虹粉色 | A.品牌蓝 | B.科技青 | C.深灰 |
|---------|---------|---------|--------|
| `#d946ef` `#c026d3` `#e879f9` | 对应蓝色阶 | 对应青色阶 | 对应灰色阶 |
| `#f0abfc` `#fae8ff` | 对应浅蓝阶 | 对应浅青阶 | 对应浅灰阶 |

#### Emoji → SVG

| Emoji | SVG 替代 |
|-------|---------|
| 📊 报表 | `<svg viewBox="0 0 16 16"><rect x="1" y="3" width="3" height="10" rx="0.5"/><rect x="6.5" y="1" width="3" height="12" rx="0.5"/><rect x="12" y="5" width="3" height="8" rx="0.5"/></svg>` |
| 📝 文本 | `<svg viewBox="0 0 16 16"><rect x="2" y="3" width="12" height="10" rx="1" stroke="currentColor" fill="none" stroke-width="1.3"/><line x1="5" y1="6" x2="11" y2="6"/><line x1="5" y1="9" x2="9" y2="9"/></svg>` |
| 💾 保存 | `<svg viewBox="0 0 16 16"><path d="M14 11v3H2v-3M5 7l3 3 3-3M8 10V2" stroke="currentColor" fill="none" stroke-width="1.5"/></svg>` |
| ➕ 新增 | `<svg viewBox="0 0 16 16"><line x1="8" y1="2" x2="8" y2="14" stroke="currentColor" stroke-width="1.5"/><line x1="2" y1="8" x2="14" y2="8" stroke="currentColor" stroke-width="1.5"/></svg>` |
| 🤖 AI | 改为文字标签并降低视觉权重 |
| ← 返回 | `<svg viewBox="0 0 16 16"><polyline points="9 4 5 8 9 12" stroke="currentColor" fill="none" stroke-width="1.5"/></svg>` |
| ✨ 生成 | `<svg viewBox="0 0 16 16"><polygon points="9 1 4 9 7 9 6 15 12 7 9 7 10 1"/></svg>` |

#### 英文报错 → 友好中文提示

创建统一错误处理函数，替换所有 `e.message` 暴露：

```javascript
function friendlyError(e, fallback) {
  var msg = e.message || '';
  if (/Unexpected token|is not valid JSON/i.test(msg))
    return '服务器暂时无法响应，请稍后重试';
  if (/Failed to fetch|NetworkError/i.test(msg))
    return '网络连接不畅，请检查网络后重试';
  if (/timeout|TIMEOUT/i.test(msg))
    return '请求超时，请稍后重试';
  return fallback || '操作未成功，请稍后重试';
}
```

规则：所有 `'xxx：' + e.message` → `'xxx：' + friendlyError(e, 'xxx未成功，请稍后重试')`

**禁止**直接拼接 `e.stack` 到用户可见的输出中。

#### AI 标签替换（可选，默认不执行）

| 原表述 | 替换为 |
|-------|--------|
| `AI 解读` / `AI 分析` | `数据解读` / `智能分析` |
| `AI 报表助手` | `报表助手` |
| `重新AI分析` | `重新分析` |
| `生成 AI 解读` | `生成解读` |
| `🤖 生成 AI 解读` | `生成数据解读` |

### Step 4: 验证

替换完成后验证：
- [ ] 所有 AI 常用色（紫色/霓虹粉）已替换
- [ ] 没有残留的紫色 hex 值
- [ ] UI 中的 emoji 图标已替换为 SVG
- [ ] `e.message` 不再直接暴露给用户，已用 `friendlyError()` 包装
- [ ] AI 标签已改为中性表述（如用户选择了此项）
- [ ] 运行语法检查确认无错误

### Step 5: 生成规范文件

在项目中创建 `.claude/ui-spec.md`，记录本次替换的完整规范和色板，方便后续开发者遵循。

## 色彩语义标准（默认方案A · 品牌蓝）

| 颜色 | 色值 | 用途 |
|------|------|------|
| 蓝（主色） | `#3b82f6` | 按钮、链接、强调、选中态 |
| 蓝（hover） | `#2563eb` | hover/active |
| 深蓝 | `#1d4ed8` | 深色文字、激活态 |
| 浅蓝背景 | `#eff6ff` | 选中背景、card |
| 浅蓝边框 | `#bfdbfe` | 选中边框 |
| 绿（涨） | `#10b981` / `#16a34a` | 正增长、成功 |
| 红（跌） | `#ef4444` / `#dc2626` | 负增长、删除、错误 |
| 黄（警告） | `#f59e0b` | 自定义徽章 |
| 灰（次级） | `#64748b` / `#94a3b8` | 次要文字 |

## 图表色板

```
['#3b82f6','#10b981','#f59e0b','#ef4444','#06b6d4','#14b8a6','#f97316','#84cc16']
```

## 关键原则

- **先报告再动手**：必须展示检测报告，等用户确认
- **逐文件替换**：每改完一个文件立即保存
- **不改变逻辑**：只替换颜色值和文本标签，不改功能代码
- **保留语义**：class 名 `.purple` 可以保留（只改 CSS 值），不改 HTML class
- **图表色板特殊处理**：图表中保留1-2个紫色作为数据系列色是允许的

**最后更新**: 2026-06-24

