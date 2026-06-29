---
name: smarttable-weekly-check
description: 企业微信智能表格周报检查工具。通过 Puppeteer 启动浏览器，利用内部 API 获取结构化数据，按4条规则检查组员周报质量。支持多周链接批量检查、自动登录等待、自动报告生成、项目维度汇总。触发词：智能表格周报检查、小组周报检查、周报链接检查、检查周报链接、smarttable check、数字员工周报检查。
---

# 智能表格周报检查

## 概述

**方案：Puppeteer + 企业微信内部 API（全自动、零配置、精确）**

企业微信智能表格内部有 `/dop-api/opendoc` API 可返回完整的结构化 JSON 数据。只需提供智能表格的**分享链接**，脚本自动启动浏览器、检测登录状态、等待扫码、提取数据。

**一键操作：** 整个提取流程已封装为 `scripts/extract_weekly.js`，自动完成启动浏览器→登录检测→等待扫码→提取数据→保存→关闭。

## 检查规则

| 规则 | 说明 | 不合格标准 |
|------|------|-----------|
| 规则1：内容变动 | 最近一个月工作内容是否有变动 | 连续4周工作内容完全相同（单一职责例外） |
| 规则2：描述清晰度 | 工作内容是否描述清晰，是否支撑一周工作量 | 任务条目＜3条，或无进度/时间标注 |
| 规则3：文字数量 | 个人周报有效字符数 | < 50 字符 → 直接不合格（态度问题） |
| 规则4：必填与重复 | 本周工作内容、下周工作计划必填，下周计划不可重复 | 空字段或近4周下周计划完全相同 |

## 前提条件

1. **Node.js 18+** 已安装
2. 链接文件准备就绪（每行一个智能表格链接）

首次运行会自动下载 Chromium（约 150MB），后续运行复用。

> 脚本会自动启动浏览器、检测登录状态。如未登录，会自动弹出浏览器窗口等待扫码，登录成功后自动继续。

## 快速使用（3条命令）

```bash
# 1. 安装依赖（首次）
npm install

# 2. 一键提取数据（输入：链接文件）
node scripts/extract_weekly.js "链接文件.txt"

# 3. 生成周报检查报告
node scripts/analyze.js

# 4. 生成项目维度汇总（可选）
node scripts/project_summary.js
```

提取脚本会自动：
- 启动浏览器（使用持久化用户数据目录，保留登录态）
- 检测企业微信登录状态
- 未登录时自动等待扫码（轮询检测，最多5分钟）
- 登录成功后自动提取所有周数据
- 保存到 `smartsheet_data/w1.json` ~ `wN.json`
- 关闭浏览器

## 脚本说明

| 脚本 | 用途 |
|------|------|
| `extract_weekly.js <links_file>` | 一键提取：启动浏览器→登录检测→API提取→保存→关闭 |
| `analyze.js` | 4规则检查，生成 `report.md` |
| `project_summary.js [weekIdx]` | 项目维度汇总，生成 `project_summary.md`（默认取最新周） |
| `fix_json.js` | 修复弯引号编码损坏的 JSON 文件 |

## 输出文件

| 文件 | 说明 |
|------|------|
| `smartsheet_data/w1.json` ~ `wN.json` | 各周提取数据 |
| `smartsheet_data/report.md` | 周报检查报告 |
| `smartsheet_data/project_summary.md` | 项目维度汇总 |

## 内部原理

### API 数据结构

`/dop-api/opendoc` 返回的 JSON 结构：

```
rawJson
  .clientVars
    .title                           // 表格标题（含周期信息）
    .retcode                         // 0=成功，538002=空文档/无权限
    .collab_client_vars
      .initialAttributedText
        .text[0]
          .smartsheet                // ⬅ 核心数据，一个 JSON 字符串
```

`JSON.parse(smartsheet)` 得到 `[meta, cells]` 数组：

**meta (data[0][0])** 结构：
```javascript
meta.c['3']['3']   // → 字段定义 {fLXRMW: {30:'姓名',31:7}, fn6ks7: {30:'本周工作内容',31:1}, ...}
meta.c['3']['5']   // → 用户映射 {userId: {2:'姓名',3:'头像URL',...}, ...}
```

**cells (data[0][1])** 结构：
```javascript
cells.c['2']['1']  // → 行数据 {rowId: {1: {fieldId: cellValue, ...}}, ...}
```

**字段值类型：**
- 类型 1（文本）：`field['1']` 为 `[{1:'text', 2:'文字内容'}, ...]` 的段落数组
- 类型 2（数字）：`field['2']` 直接为数值
- 类型 7（用户）：`field['7']` 为 `[{1:'userId'}, ...]`

### 字段自动探测

不硬编码字段 ID，通过遍历 `meta.c['3']['3']` 按 `finfo['30']`（字段标题）匹配：
- `'姓名'` → nameFid
- `'本周工作内容'` → workFid
- `'下周工作计划'` → planFid

兼容不同表格的字段 ID 差异。

### 登录状态检测

1. 打开第一个链接后，通过 `page.evaluate(fetch(...))` 调用内部 API
2. 若返回 `errcode: 30004`，判定为未登录
3. 每 3 秒轮询一次，最长等待 5 分钟
4. 用户扫码登录后，API 自动返回正常数据，脚本继续执行
5. 浏览器使用持久化 `userDataDir`（`~/.smarttable-check-browser/`），下次运行可免登录

## 踩坑记录

### 坑1：WebBridge evaluate 不调用函数表达式

**已弃用 WebBridge 方案。** 现使用 Puppeteer，`page.evaluate()` 可直接返回异步函数结果，无此问题。

### 坑2：Windows PowerShell 编码全链路问题

**已解决。** 使用 Puppeteer 后，所有数据在浏览器内提取，通过 `page.evaluate()` 返回 Node.js，全程不经过 PowerShell 处理中文。

### 坑3：空文档/API 错误未处理

**现象：** 某些链接 API 返回 `retcode: 538002`，`errmsg: "Get content error"`。

**解决：** 提取代码中检查 `retcode`，非零时返回错误信息，脚本自动跳过该周。

### 坑4：姓名解析为空

**现象：** 部分人员姓名解析为空。

**原因：** 该用户的 userId 不在用户映射表中。

**解决：** 对 userName 映射做容错，userId 查不到时 name 设为空字符串，该行直接跳过。

### 坑5：登录态丢失

**现象：** 每次运行都需要重新扫码。

**解决：** 使用 Puppeteer 的 `userDataDir` 参数指定持久化目录，Cookie 和登录态在多次运行间保留。用户只需扫码一次，后续自动登录。

## 备用方案：截图 + 视觉识别

当 API 方案不可用时（如页面结构变更），回退到截图方案：

1. Puppeteer 打开链接，等待加载
2. `page.screenshot()` 截图
3. 从截图视觉识别表格数据

## 定时自动检查

可使用 OpenClaw cron 配置定期自动检查：

```bash
# 每周五下午 5 点自动执行检查
openclaw cron add \
  --cron "0 17 * * 5" \
  --agent main \
  --message "检查本周智能表格周报，链接列表在 D:\Users\13589\Desktop\周报.txt" \
  --name "weekly_smartsheet_check" \
  --description "每周智能表格周报自动检查"
```

## 注意事项

- **首次运行需联网下载 Chromium**（约 150MB），后续运行无需下载
- **首次使用需扫码登录企业微信**，登录态会被保留，后续运行自动登录
- 多周检查时先确认所有链接是否属于同一小组（通过标题判断）
- 字段 ID 通过自动探测获取，无需硬编码，兼容不同表格
- **空文档需检查 retcode**，retcode 非零表示获取失败，自动跳过
- **姓名为空的行自动跳过**，不纳入检查

## 文件结构

```
smarttable-weekly-check/
├── SKILL.md                    # 使用说明（本文件）
├── package.json                # npm 依赖（puppeteer）
├── scripts/
│   ├── extract_weekly.js       # 一键提取（Puppeteer→登录检测→API提取→保存→关闭）
│   ├── analyze.js              # 4规则检查 → report.md
│   ├── project_summary.js      # 项目维度汇总 → project_summary.md
│   └── fix_json.js             # JSON 修复（弯引号编码问题）
├── references/
│   └── rules-detail.md         # 检查规则详解
└── smartsheet_data/           # 数据与报告输出目录
    ├── w1.json ~ wN.json       # 各周提取数据
    ├── report.md               # 周报检查报告
    └── project_summary.md      # 项目维度汇总
```
