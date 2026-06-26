---
name: tencent-docs-reader
version: 1.0.2
author: Cm-wenge
description: "Read Tencent Docs spreadsheet via agent-browser copy-paste method. Supports reading any sheet tab and returns tab-separated text. 腾讯文档在线表格读取工具，支持指定子表，返回制表符分隔的文本内容。"
license: MIT
repository: https://github.com/Cm-wenge/tencent-docs-reader
tags:
  - tencent-docs
  - spreadsheet
  - data-extraction
  - browser-automation
triggers:
  - "qq-doc-reader"
  - "read qq doc"
  - "read tencent doc"
  - "qq doc"
  - "腾讯文档"
  - "读取腾讯文档"
  - "qq表格"
  - "tencent docs"
---

# Tencent Docs Reader（腾讯文档读取器）📄

> Author: [Cm-wenge](https://github.com/Cm-wenge) | License: MIT

读取腾讯文档在线表格内容，通过 agent-browser 的复制粘贴技巧绕过 Canvas 渲染。

Read content from Tencent Docs (腾讯文档) spreadsheets using agent-browser's copy-paste trick.

## 为什么需要这个工具？/ Why This Skill?

当你把腾讯文档的共享链接发给大模型（如 ChatGPT、Claude、GLM），模型无法直接读取文档内容——它只能看到一个 URL，无法"打开"链接去查看里面的表格数据。

When you share a Tencent Docs link with an LLM (ChatGPT, Claude, GLM, etc.), the model cannot read the document content — it only sees a URL and has no way to "open" and view the spreadsheet inside.

这个工具解决的问题：

This tool solves the problem by:

- **让 AI Agent 能读取腾讯文档表格数据** — 自动打开链接、提取内容、返回结构化文本
- **绕过 Canvas 渲染** — 腾讯文档用 Canvas 画表格，传统网页抓取方式（DOM解析、accessibility tree）全部失效，本工具通过浏览器复制粘贴法成功提取
- **无需授权登录** — 不需要腾讯账号登录，只需文档设置为"所有人可读"即可读取，适合自动化场景
- **适用于自动化场景** — 定时读取周报表格、数据汇总、内容监控等

典型场景 / Typical use cases:

```
用户：帮我看看这个腾讯文档里谁还没交周报 https://docs.qq.com/sheet/xxx
Agent：（调用本工具读取表格）→ 解析内容 → 告诉你结果
```

## 原理 / How It Works

腾讯文档用 Canvas 渲染表格，accessibility tree 读不到内容。这个工具通过以下方式绕过：

Tencent Docs renders tables with Canvas (unreadable by accessibility tree). This skill bypasses it by:

1. 在 agent-browser 中打开文档 / Opens the spreadsheet in agent-browser
2. 如指定了 `--tab`，先切换到对应子表 / Switches to the specified tab
3. 点击表格区域获取焦点 / Clicks the table area to focus
4. Ctrl+A 全选 → Ctrl+C 复制 / Select all → Copy
5. 打开空白页，创建 textarea / Opens a blank page with a textarea
6. Ctrl+V 粘贴 → eval 读取内容 / Paste → Read value via eval
7. 关闭临时标签页，返回文本内容 / Closes temp tab, returns tab-separated text

## 用法 / Usage

```bash
python {baseDir}/scripts/read_sheet.py --url "https://docs.qq.com/sheet/XXXX" --tab "SheetName"
```

### 参数 / Options

| 参数        | 必填 | 说明                                                         |
|-------------|------|--------------------------------------------------------------|
| `--url`     | ✅   | 腾讯文档表格 URL / Tencent Docs spreadsheet URL              |
| `--tab`     | ❌   | 子表名称（如 `"0328"`），不填则读取当前活动子表 / Tab name  |
| `--auto-tab`| ❌   | 自动选择本周的周报标签页（本周五），找不到则选择当前日期前后两天内的标签页 |
| `--output`  | ❌   | 保存到文件，不指定则输出到 stdout / Save to file             |

**`--auto-tab` 逻辑说明**：
1. 优先选择本周五的标签页（如0410）
2. 如果找不到，选择当前日期前后两天内的标签页（如4月11日，范围0409~0413）
3. 如果都找不到，返回失败（退出码1），调用者可据此发送通知

### 示例 / Examples

```bash
# 读取指定子表 / Read a specific tab
python {baseDir}/scripts/read_sheet.py --url "https://docs.qq.com/sheet/YOUR_SHEET_ID" --tab "0328"

# 自动选择本周的周报标签页（本周五） / Auto-select current week tab (this Friday)
python {baseDir}/scripts/read_sheet.py --url "https://docs.qq.com/sheet/YOUR_SHEET_ID" --auto-tab

# 保存到文件 / Save to file
python {baseDir}/scripts/read_sheet.py --url "https://docs.qq.com/sheet/YOUR_SHEET_ID" --tab "0328" --output result.txt

# 读取当前活动子表 / Read active tab
python {baseDir}/scripts/read_sheet.py --url "https://docs.qq.com/sheet/YOUR_SHEET_ID"
```

## 依赖 / Requirements

- **Python 3.x** — 运行读取脚本 / Reader script runtime
- **agent-browser** — 全局安装（`npm install -g agent-browser`）并启动守护进程（`agent-browser start`）

## 限制 / Limitations

- 仅支持**在线表格**（spreadsheets），不支持在线文档（docs）和幻灯片（slides）
- **需要文档设置为"所有人可读"** — 本技能无需登录，但要求文档共享权限为"所有人可读"，需要登录或权限受限的文档无法读取
- 超大表格可能较慢（一次性复制全部内容）
- 腾讯文档前端改版可能导致失效，需适时更新

## 输出格式 / Output Format

制表符分隔，每行一条记录 / Tab-separated values, one row per line:

```
姓名    年龄    城市
张三    30      北京
李四    25      上海
```

可用 Python `csv.reader`（delimiter=`\t`）或标准文本工具解析。

---

## Install via ClawHub (coming soon)

```bash
npx clawhub install tencent-docs-reader
```
