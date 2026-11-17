---
name: text-to-infographic
version: 1.5.0
description: 将文章/笔记/对话内容转化为结构化信息图 plan（JSON），经布局语义与数值一致性校验后，用内置渲染器产出自包含静态 HTML 信息图，可选导出 PNG（用本机已有浏览器截图，不安装任何东西）。校验结果带稳定规则码的机器回执（--json）与中文诊断（--explain），支持 --fail-on-warn 严格模式。支持文本→plan 自动构建（analyze 布局推荐）、8 种风格 preset 与 accent/ink/paper/muted 色彩 token。十种 chart_family 布局：飞轮/鱼骨/桑基/金字塔/时间线/仪表盘/对比双栏/2×2矩阵/流程步骤/韦恩图。仅在用户明确请求信息图时调用。
allowed-tools: Read, Write, Bash
---

# Text to Infographic v1.5.0

把内容压缩为**可编辑的结构化 plan**，校验信息正确性，再渲染为**零依赖、零脚本、零外链**的静态 HTML 信息图。

## 与其他可视化工具的边界

- 主打「可编辑 plan + 信息正确校验 + 安全渲染」，不与海报型生成工具拼视觉；
- chart_family（flywheel / fishbone / sankey / pyramid / timeline / dashboard / comparison / quadrant / flow / venn）是专用布局，通用图表请用图表类 skill。

## 何时使用

- 用户明确请求信息图（规格、HTML 或图片）；
- 用户提供了文章/笔记并希望可视化为单页信息图。

不要用于普通摘要、多页报告、幻灯片、照片编辑。

## 工作流（analyze → build → validate → render）

1. **分析文本（text→plan 入口）**：`python3 scripts/build_plan_from_text.py --analyze 文章.md`
   - 启发式推荐 chart_family 布局并给出证据（命中信号词/时间词/数字密度）；
   - LLM 依据推荐与 schemas/infographic-plan.schema.json 抽取 blocks 草稿（只抽要点，不搬运原文长句）。
2. **组装 plan**：`python3 scripts/build_plan_from_text.py --from-blocks draft.json -o plan.json [--layout flywheel] [--style editorial] [--title ...]`
   - 自动填 version / layout / visual_system，组装后立即做布局语义校验，有 ERROR 不产出 plan；
   - `--style` 可选 8 种 preset：terracotta / ocean / forest / ink / mono / **editorial / technical / warm**（v1.3.0 新增）。
3. **校验（可独立使用）**：`python3 scripts/validate_infographic_plan.py plan.json [--source 原文.txt] [--explain] [--json] [--fail-on-warn]`
   - 捕获布局语义错误：飞轮未闭环、鱼骨多头、桑基流量不守恒、仪表盘缺单位、时间线缺时标、并列内容被误写成流程；
   - `--explain` 输出中文诊断（为什么 + 怎么改），可直接念给内容作者听，也适合校验**其他工具产出的 plan**；
   - 每条 finding 带稳定规则码（如 FLY-002 未闭环、SANK-003 不守恒），`--json` 输出机器回执（code/level/subject/evidence/why/fix），`--rules` 列出全部码；
   - `--fail-on-warn`：WARN 也判失败，适合 CI / 批处理 / 上线前把关；
   - 提供 `--source` 时额外做数值溯源（B 层）；ERROR 必须修复，WARN 需向用户说明。
4. **渲染**：`python3 scripts/render_infographic_html.py plan.json out.html [--png out.png]`
   - 产出单文件静态 HTML：仅 HTML + 内联 CSS/SVG，**无 JavaScript、无外部请求、无第三方依赖**，可直接粘贴分享或打印；
   - `--png`（可选）：用本机已有 Chrome/Chromium/Edge 截图出 PNG（默认 2x，宽 852），供小红书/公众号直发；**不安装任何浏览器**，找不到就明确报错退出，HTML 主路径不受影响。
5. 迭代 = 改 plan 再重跑两步，不推倒重来。

## 视觉风格（v1.3.0）

- 8 种 palette preset，克制的 token 而非风格堆砌；
- 细调：`visual_system` 支持按 token 覆盖 `accent`（强调色）/ `ink`（正文）/ `paper`（纸面底色）/ `muted`（次要文字），值必须为十六进制颜色（安全边界，非法值拒绝渲染）。

## 安全承诺（Safe Rendering）

- 渲染器仅用 Python 标准库，**不安装任何浏览器或依赖**；PNG 导出同样只调用本机已有浏览器，绝不下载安装；
- 产物**不包含脚本、不发起任何网络请求**，可离线打开、可打印、可安全分发；
- 所有颜色 token 与 accent 同一安全边界：仅十六进制，渲染器入口强校验；
- 不上传、不发布、不写入用户未指定的外部状态。

## 输入边界

- 只使用当前对话中用户提供的内容与文件；不联网抓取或核验；
- 缺失的事实、数值、引用保持未指定，并在 plan 中标注。

## 验证清单

- plan 通过 validate 脚本（0 ERROR）；
- HTML 以 `<!doctype html>` 开始、无 `<script>`、无 `http(s)://` 外链；
- 布局语义正确（飞轮闭环 / 鱼骨单头 / 桑基守恒 / 时间线含时标 / 仪表盘带单位）；
- 中文渲染无乱码、无溢出；仅依赖颜色传达信息的地方有文字冗余。
