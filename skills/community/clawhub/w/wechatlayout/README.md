# WeChatLayout

> **约束优于自由** — 微信公众号排版引擎。把 Markdown 文章转换为可直接粘贴进公众号编辑器、粘贴后样式不丢失的 HTML（样式内联 + `<span leaf="">` 包裹）。也从任意公众号文章 URL 提取视觉风格，生成匹配的组件库。

[![Version](https://img.shields.io/badge/Version-v1.7-green.svg)](./SKILL.md#changelog) [![Author](https://img.shields.io/badge/Author-Qomob.AI-blue.svg)](#版权与授权) [![License](https://img.shields.io/badge/License-PolyForm_Noncommercial_1.0.0-blue.svg)](LICENSE) [![Modes](https://img.shields.io/badge/Modes-A_+_B_+_C-orange.svg)](#三种工作模式) [![Themes](https://img.shields.io/badge/Industry_Templates-5_+_Custom-9cf.svg)](#行业模板系统) [![Evals](https://img.shields.io/badge/Regression-5_fixtures-green.svg)](#三关卡可验证循环)

---

## 一句话

给它一篇 Markdown，返还一段可直接粘贴到公众号编辑器的 `<section>` HTML 片段——样式不丢失、平台合规、视觉克制。

```
"把这篇 Markdown 排成公众号文章，用翡翠绿主题"
  → 输入归一化 → 选行业模板 → 读组件库 → 解析结构
    → 装配 HTML → validate_output.py 校验 → 输出
```

---

## 三种工作模式

| 模式 | 触发词 | 产物 |
|------|--------|------|
| **Mode A: 排版** | 公众号排版 / 微信排版 / gzh / 排成公众号 / 粘到公众号 | 纯 `<section>` 正文片段 + 预览页 |
| **Mode B: 风格提取** | 提取风格 / 分析排版 / 模仿公众号 / 风格提取 / 主题提取 | `references/theme-{name}.md` 组件库 + 主题注册登记 |
| **Mode C: 品牌模板** | 品牌模板 / 品牌手册 / 参考风格 / 上传品牌素材 / 品牌色 / VI | `references/theme-{brand}.md` 品牌专属模板 + 登记 |

路由后锁定模式，不混合。Mode A 产出的 HTML 可被 Mode B/C 提取的主题直接使用。

---

## 支持的 Markdown

`#` 标题 / `##` 章节 / `###` 子标题 / `>` 引用（开头为引言卡）/ 围栏代码块 / 行内代码 / 表格 / `-` 或 `1.` 列表 / 图片 / `---` 分割线 / `**加粗**`（锚点，全文 ≤5）/ `==高亮==` / `<u>下划线</u>`（或 `++下划线++`）。

## 与 CLI 原生模式的分工

- **Mode A 排版** 由 skill 主流程提供，产物通过 `scripts/validate_output.py` 校验。
- **Mode B 风格提取**（公众号 URL → 自定义主题）由 `scripts/style_extractor.py` 提供，提取出的主题可继续用 CLI 流程。
- **Mode C 品牌模板**（品牌素材 → 品牌专属模板）同样由 `scripts/style_extractor.py` 提供。
- 自动下划线 / 英文标签 / 副标题均为确定性启发式生成，可在排版时关闭或用 `**` 手动指定锚点。

---

## 行业模板系统

> 5 套行业模板 = 5 种设计 DNA（结构/组件/骨架各自独立，不是同一套模版换颜色），对标国际一线设计语言。

| 行业模板 | 标识 | 主色 | 适用行业 | 设计对标 |
|---------|------|------|---------|---------|
| Blueprint 蓝图 | emerald | `#059669` | 科技知识：教程/测评/清单/复盘 | Linear / Stripe 文档 |
| Editorial 杂志 | graphite | `#374151` | 观点评论：设计/深度分析/高端品牌 | The New Yorker / Monocle |
| Kitchen 厨房手帐 | sunset | `#ea580c` | 美食生活：探店/旅行/治愈 | Bon Appétit |
| Report 研报 | ocean | `#2563eb` | 企业金融：行业分析/数据报告 | Bloomberg / FT |
| Campaign 大秀 | rose | `#e11d48` | 时尚美妆：穿搭/促销/种草 | 时尚 Lookbook |
| 自定义 | — | — | 由 Mode B 提取或用 `theme-generator.md` 创建 | 跟随参考文章 |

---

## 平台红线

公众号编辑器是极度受限的富文本粘贴器。核心限制：

- **禁止**：`<style>` / `<script>` / `<div>` / `class` / `id` / 事件处理器 / `position` / `float` / `grid` / `@media` / CSS 变量
- **必须**：样式全部内联；文字节点用 `<span leaf="">` 包裹
- **可用**：`<section>` / `<span>` / `<p>` / `<img>` / `<table>` 等基础标签 + 内联 style 属性

完整红线表 → [`references/mode-a-format.md`](./references/mode-a-format.md)

---

## 三关卡可验证循环

| 关卡 | 脚本 | 作用 |
|------|------|------|
| **源头关** | `scripts/component_lint.py` | 扫描主题组件库源头的反模式 |
| **产物关** | `scripts/validate_output.py` | 扫描最终 HTML 是否符合平台限制 |
| **回归关** | `scripts/run_evals.py` | 校验 5 套主题 golden fixtures 全部通过（校验规则变更的确定性兜底） |

**三关全绿才交付。即使用户要求跳过，校验也不可绕过。**

```bash
# 排版校验（严重问题必须为 0）
python3 scripts/validate_output.py <output.html>
python3 scripts/validate_output.py <output.html> --ops   # 额外运营维度检查

# 组件库源头检查
python3 scripts/component_lint.py <skill-base>

# 回归测试（5 套主题 golden fixtures，规则变更后必须跑）
python3 scripts/run_evals.py

# 风格提取 / 品牌模板（需先安装 Mode B/C 依赖）
pip install -r requirements.txt
python3 scripts/style_extractor.py <url> [--output <name>]
python3 scripts/style_extractor.py --html <file.html> --output <name>
python3 scripts/style_extractor.py --image <品牌图> --output <brand>       # 品牌图提色
python3 scripts/style_extractor.py --pdf <品牌手册.pdf> --output <brand>   # 品牌手册 PDF
python3 scripts/style_extractor.py --doc <品牌文档.md> --output <brand>    # 品牌文档色值

# 统一 CLI
./scripts/wechat.sh validate <input.html>
./scripts/wechat.sh lint
./scripts/wechat.sh eval
./scripts/wechat.sh extract <url> [--output <name>]
```

---

## 内容智能处理（Mode A 核心特色）

| 处理项 | 说明 |
|--------|------|
| 章节自动编号 | `##` → 01/02/03，末章结语用 `∞` |
| 英文标签 | 据中文标题生成（实测→TEST、教程→TUTORIAL…） |
| 关键词下划线 | 每段主动标 1-3 个核心短语（即使原文没加粗） |
| 引言关键词高亮 | 识别开头金句核心词 |
| 目录提取 | 前 3 个 `##` 作为导读 |
| 全角标点 | 正文自动规范中文全角（代码块内保持原样） |
| 签名区 | 末尾一处，默认 `{{作者名}}` 占位 |

---

## 3 层视觉层级（克制三原则）

**锚点层**（全文 ≤5 处，主色加粗/深底白字）→ **标记层**（每段 1-3 处，下划线）→ **容器层**（按需，浅底引用/荧光笔/徽章）

克制三原则：① 主色只在锚点出现；② 大面积白底+灰阶；③ 一段内高亮 ≤2 种。

---

## 运行时回退策略

| 失败场景 | 回退 |
|---------|------|
| URL 抓取失败 | 提示用户提供本地 HTML 文件 |
| 颜色提取过少（<3 种） | 使用默认调色板填充 |
| 排版信息不足 | 使用标准值（字号 16px，行高 1.9） |
| 模板文件未找到 | 回退 Blueprint 蓝图（emerald）模板 |

---

## 目录结构

```
WeChatLayout/
├── SKILL.md                       # 入口文件（Intent Router + 工作流摘要）
├── README.md                      # 本文件
├── LICENSE                        # PolyForm Noncommercial 1.0.0 许可
├── requirements.txt               # Mode B/C 外部依赖（requests+bs4 / pillow / pymupdf）
├── references/
│   ├── mode-a-format.md           # Mode A 排版工作流完整定义
│   ├── mode-b-extract.md          # Mode B 风格提取工作流完整定义
│   ├── mode-c-brand.md            # Mode C 品牌模板生成工作流完整定义
│   ├── common-components.md       # 通用组件库
│   ├── format-normalize.md        # 输入归一化规则
│   ├── image-suggestion.md        # 配图建议工作流（Step 3.5）
│   ├── theme-index.md             # 行业模板注册表（SSOT）
│   ├── theme-emerald.md           # Blueprint 蓝图组件库（科技知识）
│   ├── theme-graphite.md          # Editorial 杂志组件库（观点评论）
│   ├── theme-sunset.md            # Kitchen 厨房手帐组件库（美食生活）
│   ├── theme-ocean.md             # Report 研报组件库（企业金融）
│   ├── theme-rose.md              # Campaign 大秀组件库（时尚美妆）
│   ├── theme-generator.md         # 自定义模板生成器
│   └── paste-test-checklist.md    # 粘贴测试清单
├── scripts/
│   ├── validate_output.py         # 产物关校验
│   ├── component_lint.py          # 源头关扫描
│   ├── run_evals.py               # 回归关（golden fixtures 校验）
│   ├── style_extractor.py         # 风格提取脚本
│   ├── validation_config.json     # 校验规则外化
│   └── wechat.sh                   # 统一 CLI 入口
└── evals/
    ├── evals.json                 # 评测用例（含 5 套主题回归用例）
    ├── trigger-queries.json       # 触发词测试
    └── fixtures/                  # 黄金对照样本（回归测试）
        ├── tutorial_python.md            # 输入 Markdown
        ├── tutorial_python_golden.html           # emerald 期望产物（严重问题=0）
        ├── tutorial_python_graphite_golden.html  # graphite 期望产物
        ├── tutorial_python_sunset_golden.html    # sunset 期望产物
        ├── tutorial_python_ocean_golden.html     # ocean 期望产物
        └── tutorial_python_rose_golden.html      # rose 期望产物
```

`output/`（运行时排版产物，已 gitignore，不入库）→ 见 [输出约定](#输出约定)

---

## 输出约定

- **统一输出目录**：所有排版产物（正文 HTML、预览页、配图建议清单）保存到 `output/`
- **版权脚注**：每个产物正文末尾必须包含「©2026 Qomob.AI 由WeChatLayout微信公众号排版引擎驱动」（通用库固定组件，遗漏 = 产物不合格）

---

## 完成判据

| Mode | 完成判据 |
|------|----------|
| **Mode A 排版** | HTML 不含 `<div>`/`class`/`id`；所有样式内联；文字节点用 `<span leaf="">` 包裹；`validate_output.py` 严重问题=0；产物存 `output/`；正文末尾含版权脚注「©2026 Qomob.AI 由WeChatLayout微信公众号排版引擎驱动」 |
| **Mode B 风格提取** | 生成 `references/theme-{name}.md`；在 `theme-index.md` 登记；提取颜色/排版/间距；域名白名单校验通过 |
| **Mode C 品牌模板** | 生成 `references/theme-{brand}.md`（含品牌色板/气质变量）；`component_lint.py` 0 严重问题；在 `theme-index.md` 登记；Mode A 可选 |

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| v1.0 | 2026-07 | 从 XDesign v2.8 提取公众号排版（Mode 4）和风格提取（Mode 5）为独立 skill |
| v1.1 | 2026-07 | ARE 评测后改进：P0 修复「不可跳过校验」硬指令 + 事件处理器 XSS 检查；P1 消除 SKILL.md 重复内容 + 新增 3 套主题（sunset/ocean/rose）+ 内容质量可验证规则；P2 校验规则外化为 validation_config.json + 运营维度可选检查（--ops） |
| v1.2 | 2026-08 | 新增 Mode A Step 3.5 配图建议（AI 判断配图点 + 文生图 prompt）；许可改为 PolyForm Noncommercial 1.0.0（见 LICENSE） |
| v1.3 | 2026-08 | 内容质量校验强化：正文段下划线覆盖率（DOM 级，抓"有的段标有的段漏"）+ 平台规则实测日期过期提醒；新增回归关 run_evals.py（golden fixtures）+ wechat eval 命令 |
| v1.4 | 2026-08 | 产物统一输出到 `output/`；正文末尾固定版权脚注「©2026 Qomob.AI 由WeChatLayout微信公众号排版引擎驱动」；validate_output.py --ops 增加版权脚注缺失提醒 |
| v1.5 | 2026-08 | ARE 评测短板修复：扩充 golden fixtures 至 5 套主题（回归覆盖 1→5）；新增 requirements.txt 隔离 Mode B 外部依赖；evals.json 补充多主题回归用例；paste-test-checklist.md 明确自动化与人工测试分工 |

完整 Changelog → [`SKILL.md#changelog`](./SKILL.md#changelog)

---

## 版权与授权

**作者**：Qomob.AI

**版权声明**：本作品版权归 **Qomob.AI** 所有，采用 [**PolyForm Noncommercial 1.0.0**](./LICENSE) 非商业软件许可。

### 许可摘要（完整条款见 LICENSE 文件）

| 场景 | 是否允许 |
|------|---------|
| ✅ 个人使用（研究、学习、实验、私人娱乐、业余项目） | 允许 |
| ✅ 非商业组织（公益机构、教育机构、公共研究机构、政府机构等） | 允许 |
| ✅ 修改与衍生作品 | 允许，但须保留 Required Notice 版权行 |
| ❌ 商业用途 | 禁止（含付费服务、销售副本、作为业务组成部分） |
| ❌ 再分发时移除版权声明 | 禁止，分发副本须附本许可条款或其 URL |

> **Required Notice**: Copyright Qomob.AI (https://github.com/Qomob-AI)
> 分发本软件任何副本时，必须随附上述版权行与本许可条款。

### 第三方素材声明

- **主题色板**：5 套预设主题（emerald / graphite / sunset / ocean / rose）的色阶色值参考自 [Tailwind CSS](https://tailwindcss.com) 调色板。Tailwind CSS 采用 [MIT 许可证](https://github.com/tailwindlabs/tailwindcss/blob/master/LICENSE)， Copyright (c) Adam Wathan, Jonathan Reinink, David Hemphill, Steve Schoger。本项目按 MIT 许可条款保留其版权声明，仅使用色值数字，未复制其源代码或样式表。
- **Python 依赖**：`requests`（Apache License 2.0）、`beautifulsoup4`（MIT License）、`pillow`（HPND License）、`pymupdf`（AGPL-3.0，仅 Mode C 品牌手册 PDF 提取时按需使用），按各自许可使用。

> 未经授权将本 skill 用于商业用途的，视为侵权行为，Qomob.AI 保留追究法律责任的权利。

# 加入群聊

<div align="center">
  <img src="https://qomob.ai/xskill.jpg" width="600" alt="XSkill">
</div>

