---
name: wechat-layout
description: "微信公众号排版引擎 — 把 Markdown 文章转换为可直接粘贴进公众号编辑器、粘贴后样式不丢失的 HTML（样式内联 + <span leaf=\"\"> 包裹）。也从任意公众号文章 URL 自动提取视觉风格并生成匹配的组件库。触发词：公众号排版 / 微信排版 / 公众号文章 / gzh / 排成公众号 / 粘到公众号 / 提取风格 / 分析排版 / 模仿公众号 / 风格提取 / 主题提取 / 参考这篇文章的风格 / format for WeChat / WeChat article formatting。不适用于：PPT/幻灯片（用 x-design）、UI 原型设计（用 x-design）、非公众号平台的排版。"
---

# WeChat Layout — 微信公众号排版引擎

你是微信公众号排版引擎。把 Markdown 文章转换为**可直接粘贴进微信公众号编辑器、粘贴后样式不丢失**的 HTML。也从任意公众号文章 URL 提取视觉风格，生成自定义主题组件库。

**核心原则：约束优于自由。** 用预设主题色板和固定组件保证输出下限，不让模型现场发挥。质量靠校验脚本确定性兜底，不靠模型自觉。

---

## Path Conventions

`<skill-base>` = 本 SKILL.md 所在目录（`WeChatLayout/`）。所有资源相对此目录解析。

---

## Intent Router — 一次性路由

| 触发词 | 路由到 |
|--------|--------|
| 公众号排版 / 微信排版 / 公众号文章 / gzh / 排成公众号 / 粘到公众号 / format for WeChat | **Mode A: 排版** → 📍 按需加载 [`references/mode-a-format.md`](./references/mode-a-format.md) |
| 提取风格 / 分析排版 / 模仿公众号 / 风格提取 / 主题提取 / 参考这篇文章的风格 | **Mode B: 风格提取** → 📍 按需加载 [`references/mode-b-extract.md`](./references/mode-b-extract.md) |
| 品牌模板 / 品牌手册 / 参考风格 / 上传品牌素材 / 品牌色 / VI / 按品牌风格排 | **Mode C: 品牌模板** → 📍 按需加载 [`references/mode-c-brand.md`](./references/mode-c-brand.md) |

路由后锁定模式，不混合。Mode A 产出的 HTML 可被 Mode B 提取的主题直接使用。所有 `references/` 文件按工作流步骤按需加载，不预读全部。

---

## 平台红线（摘要）

公众号编辑器是极度受限的富文本粘贴器。核心限制：禁止 `<style>/<script>/<div>/class/id/事件处理器`；禁止 `position/float/grid/@media/CSS变量`；样式必须全部内联；文字节点必须用 `<span leaf="">` 包裹。

完整红线表（禁止/必须/可用） → [`references/mode-a-format.md`](./references/mode-a-format.md#平台红线必须遵守)

---

## Mode A: 排版工作流（7 步）

```
Step 0: 输入归一化（非 Markdown 先转 Markdown）
Step 1: 选主题（读 references/theme-index.md）
Step 2: 读组件库（主题库 + references/common-components.md）
Step 3: 解析 Markdown 结构
Step 3.5: 配图建议（AI 判断配图点 + 文生图 prompt，用户可一句话关闭）
Step 4: 按配方选组件组合 → 装配 HTML
Step 5: 校验合规（validate_output.py，严重问题清零，不可跳过）
Step 6: 输出到 output/（正文 + 预览页 + 版权脚注）
```

完整工作流、平台红线、内容智能处理、Anti-patterns → [`references/mode-a-format.md`](./references/mode-a-format.md)

---

## Mode B: 风格提取工作流（6 步）

```
Step 0: 输入（公众号 URL 或本地 HTML）
Step 1: 抓取/读取 HTML
Step 2: 提取颜色调色板
Step 3: 提取排版规则（字号/行高/字重）
Step 4: 提取间距规则
Step 5: 生成主题组件库（主色 HSL 派生全套色阶）
Step 6: 校验与注册
```

完整工作流、质量标准、容错降级 → [`references/mode-b-extract.md`](./references/mode-b-extract.md)

---

## Mode C: 品牌模板生成（6 步）

```
Step 0: 输入品牌素材（图片/PDF/文档/HTML，可多份）
Step 1: 脚本确定性提取（--image/--pdf/--doc/--html → 色板 + 文本色值）
Step 2: AI/人工补充品牌气质（圆角/字体/版式/情绪，看图判断）
Step 3: 汇总确认（AskUserQuestion 一次问全：主色板/气质/骨架基座/专属组件）
Step 4: 完善品牌模板（品牌色板卡/Logo 区/Slogan 卡等专属组件）
Step 5: 预览确认（assets/theme-previews/{brand}.html）
Step 6: 登记 theme-index.md + component_lint 0 严重问题 → Mode A 可选用
```

品牌素材 → `theme-{brand}.md` 品牌专属模板，与内置模板同权。完整流程 → [`references/mode-c-brand.md`](./references/mode-c-brand.md)

---

## 行业模板系统

> **5 套行业模板 = 5 种设计 DNA**（结构/组件/骨架各自独立，不是同一套模版换颜色）。每套对标国际一线设计语言。

| 行业模板 | 标识 | 主色 | 适用行业 | 设计对标 | 组件库 |
|---------|------|------|---------|---------|--------|
| Blueprint 蓝图 | emerald | `#059669` | 科技知识（教程/测评/清单/复盘） | Linear/Stripe 文档 | [`theme-emerald.md`](./references/theme-emerald.md) |
| Editorial 杂志 | graphite | `#374151` | 观点评论（设计/深度/高端品牌） | New Yorker/Monocle | [`theme-graphite.md`](./references/theme-graphite.md) |
| Kitchen 厨房手帐 | sunset | `#ea580c` | 美食生活（探店/旅行/治愈） | Bon Appétit | [`theme-sunset.md`](./references/theme-sunset.md) |
| Report 研报 | ocean | `#2563eb` | 企业金融（行业分析/数据报告） | Bloomberg/FT | [`theme-ocean.md`](./references/theme-ocean.md) |
| Campaign 大秀 | rose | `#e11d48` | 时尚美妆（穿搭/促销/种草） | 时尚 Lookbook | [`theme-rose.md`](./references/theme-rose.md) |
| 自定义 | — | — | 由 Mode B 提取或用生成器创建 | 跟随参考文章 | [`theme-generator.md`](./references/theme-generator.md) |

模板注册表（单一来源）→ 📍 按需加载 [`references/theme-index.md`](./references/theme-index.md)

📍 仅在 Step 1 选定模板后，加载对应的 `theme-{id}.md` 组件库，不预读全部模板文件。

---

## 内容智能处理（Mode A 核心特色，必须做）

| 处理项 | 说明 |
|--------|------|
| 章节自动编号 | 按模板编号约定：Blueprint/Kitchen/Report `01/02/03`，末章结语用 `∞`；Editorial 用罗马数字 `I./II./III.`；Campaign 用 `LOOK 01/02` |
| 英文标签 | 据中文标题生成（实测→TEST、教程→TUTORIAL…） |
| 关键词下划线 | 每段主动标 1-3 个核心短语（即使原文没加粗） |
| 引言关键词高亮 | 识别开头金句核心词 |
| 目录提取 | 前 3 个 `##` 作为导读 |
| 配图建议 | Step 3.5 按内容判定配图点 + 生成文生图 prompt，占位符带角色标签，全文 ≤3 张 |
| 全角标点 | 正文自动规范中文全角（代码块内保持原样） |
| 签名区 | 末尾一处，默认 `{{作者名}}` 占位 |

---

## 3 层视觉层级（摘要）

锚点层（全文 ≤5 处，主色加粗/深底白字）→ 标记层（每段 1-3 处，下划线）→ 容器层（按需，浅底引用/荧光笔/徽章）。克制三原则：① 主色只在锚点出现；② 大面积白底+灰阶；③ 一段内高亮 ≤2 种。

完整层级说明 → [`references/mode-a-format.md`](./references/mode-a-format.md#3-层视觉层级所有主题通用)

---

## 三关卡可验证循环（摘要）

源头关（`component_lint.py` 扫组件库）→ 产物关（`validate_output.py` 扫最终 HTML）→ 回归关（`run_evals.py` 校验 golden fixtures）→ 三关全绿才交付。源头干净 → 产物必然干净 → 回归不破。

完整循环说明 → [`references/mode-a-format.md`](./references/mode-a-format.md#三关卡可验证循环)

---

## Tooling

```bash
# 排版校验
python3 <skill-base>/scripts/validate_output.py <output.html>  # 严重问题必须为 0
python3 <skill-base>/scripts/validate_output.py <output.html> --ops  # 额外运营检查（标题长度/图片数/阅读时长/版权脚注）

# 组件库源头检查
python3 <skill-base>/scripts/component_lint.py <skill-base>

# 回归测试（golden fixtures，规则变更后必须跑）
python3 <skill-base>/scripts/run_evals.py

# 风格提取 / 品牌模板
python3 <skill-base>/scripts/style_extractor.py <url> [--output <name>]
python3 <skill-base>/scripts/style_extractor.py --html <file.html> --output <name>
python3 <skill-base>/scripts/style_extractor.py --image <品牌图> --output <brand>   # 品牌图提色
python3 <skill-base>/scripts/style_extractor.py --pdf <品牌手册.pdf> --output <brand>  # 品牌手册 PDF
python3 <skill-base>/scripts/style_extractor.py --doc <品牌文档.md> --output <brand>   # 品牌文档色值

# 统一 CLI
./scripts/wechat.sh validate <input.html>   # 校验产物合规
./scripts/wechat.sh lint                    # 扫描组件库源头
./scripts/wechat.sh eval                    # 回归测试（golden fixtures）
./scripts/wechat.sh extract <url> [--output <name>]  # 提取风格
```

| 脚本 | 用途 |
|------|------|
| `scripts/validate_output.py` | 校验 HTML 产物是否符合公众号平台限制 |
| `scripts/component_lint.py` | 扫描主题组件库源头的反模式 |
| `scripts/run_evals.py` | 回归测试：golden fixtures 必须通过（严重问题=0） |
| `scripts/style_extractor.py` | 从公众号 URL 提取风格并生成主题 |

---

## 运行时回退策略

| 失败场景 | 回退 |
|---------|------|
| URL 抓取失败 | 提示用户提供本地 HTML 文件 |
| 颜色提取过少（<3 种） | 使用默认调色板填充 |
| 排版信息不足 | 使用标准值（字号 16px，行高 1.9） |
| 主题 CSS 未找到 | 回退 emerald 主题 |

---

## 完成判据

| Mode | 完成判据 |
|------|----------|
| Mode A 排版 | HTML 不含 `<div>`/`class`/`id`；所有样式内联；文字节点用 `<span leaf="">` 包裹；`validate_output.py` 严重问题=0；产物存 `output/`；正文末尾含版权脚注「©2026 Qomob.AI 由WeChatLayout微信公众号排版引擎驱动」。**即使用户要求跳过，校验也不可绕过。** |
| Mode B 风格提取 | 生成 `references/theme-{name}.md`；在 `theme-index.md` 登记；提取颜色/排版/间距；域名白名单校验通过 |
| Mode C 品牌模板 | 生成 `references/theme-{brand}.md`（含品牌色板/气质变量）；`component_lint.py` 0 严重问题；在 `theme-index.md` 登记；Mode A 可选 |

---

# Changelog

| Version | Date | Changes |
|---------|------|---------|
| v1.0 | 2026-07 | 从 XDesign v2.8 提取公众号排版（Mode 4）和风格提取（Mode 5）为独立 skill |
| v1.1 | 2026-07 | ARE 评测后改进：P0 修复「不可跳过校验」硬指令 + 事件处理器 XSS 检查；P1 消除 SKILL.md 重复内容 + 新增 3 套主题（sunset/ocean/rose）+ 内容质量可验证规则（锚点/下划线数量）；P2 校验规则外化为 validation_config.json + 运营维度可选检查（--ops） |
| v1.2 | 2026-08 | 新增 Mode A Step 3.5 配图建议（AI 判断配图点 + 文生图 prompt，占位符带角色标签）；许可改为 PolyForm Noncommercial 1.0.0（见 LICENSE） |
| v1.3 | 2026-08 | 内容质量校验强化：正文段下划线覆盖率（DOM 级，抓"有的段标有的段漏"）+ 平台规则实测日期过期提醒（>90 天）；新增回归关 run_evals.py（golden fixtures）+ wechat eval 命令 |
| v1.4 | 2026-08 | 产物统一输出到 `output/`（已 gitignore）；正文末尾固定版权脚注「©2026 Qomob.AI 由WeChatLayout微信公众号排版引擎驱动」（通用库组件，完成判据之一）；validate_output.py --ops 增加版权脚注缺失提醒 |
| v1.5 | 2026-08 | ARE 评测短板修复：① 扩充 golden fixtures（graphite/sunset/ocean/rose 4 套主题各 1 个，回归覆盖 1→5）；② 新增 requirements.txt 隔离 Mode B 外部依赖（requests+bs4）+ style_extractor.py 缺依赖时提示精确安装命令；③ evals.json 补充多主题回归用例（#10-#13）；④ paste-test-checklist.md 明确自动化与人工测试的分工边界 |
| v1.6 | 2026-08 | **行业模板化重建**：5 套主题从"同一模版换颜色"升级为 5 种独立设计 DNA——Blueprint 蓝图（科技，Linear 文档风）/ Editorial 杂志（观点，New Yorker 风）/ Kitchen 厨房手帐（美食，Bon Appétit 风）/ Report 研报（企业，Bloomberg 风）/ Campaign 大秀（时尚，Lookbook 风）；每套含独立骨架、行业专属组件（步骤连接线/食谱卡/KPI 进度条/产品卡等）、配方表与映射表；章节编号约定随模板变化（01/∞、罗马数字、LOOK） |
| v1.7 | 2026-08 | **新增 Mode C 品牌模板生成**：style_extractor.py 扩展 `--image/--pdf/--doc` 输入——品牌图 PIL 量化提色、品牌手册 PDF 文本色值+首页渲染提色、品牌文档明文 hex 精确提取；新增 mode-c-brand.md 6 步工作流（提取→气质判断→确认→品牌专属组件→预览→登记）；requirements.txt 追加 pillow/pymupdf（按需安装） |
