---
name: resume-styles-kit
description: "基于候选人真实经历生成风格化 PDF 简历。按 5 种 Skills 风格（双栏分类/侧栏pill/极简竖列/标签云/熟练度条）生成或优化简历、把项目经历写成有卖点不简化、支持还原 skills 结构与批量转 PDF。核心红线：内容不简化、严格基于真实经历不编造、量化成果、最新亮点项目置顶。"
metadata:
  version: 1.0.2
  author: anonymous
  license: MIT
  tags: [resume, cv, latex, skill-template, career, job-application]
  categories: [productivity, career]
  topics: [resume, skills-styles, pdf-generation, content-writing]
---

# 简历风格生成（resume-styles-kit）

基于候选人**真实经历**、通过 5 种 Skills 风格生成或优化可投递的 PDF 简历；把项目经历写成有卖点且**不简化**的内容；支持还原 skills 结构与批量转 PDF。

> ⚠️ **隐私红线**：技能必须**通用化、去隐私化**。不得包含任何真实姓名、联系方式、教育经历、具体公司项目、量化数据等个人私密信息。一律用占位符或通用示例代替。

## 铁律（Red Lines）

1. **内容绝不简化** —— 用户强调「不要简化」。完整简历的项目条目须完整保留（例：5 个项目共 25 条 li：A项目6 + B项目7 + C项目6 + D项目3 + E项目3）。任何「觉得太长想压缩」的念头都要先问用户，绝不擅自删内容。
2. **严格基于真实经历，不编造** —— 只写候选人实际做过的事。可增强表达（讲透细节、突出卖点、量化成果），但绝不虚构项目、指标、公司、技术栈。
3. **量化交付** —— 尽量用数字说话（提效百分比、减代码量、降缺陷率、业务线数、荣誉提名等），但数字必须来自候选人真实给出的数据。
4. **最新亮点项目置顶** —— 最新 / 转型亮点的项目总是放项目经历第一位。

## 工作流程

1. **确认内容**：先与候选人确认项目列表、每条 li 结构、项目排序（亮点置顶）、是否有新增真实经历。
2. **写 HTML**：页面构成 = 个人简介 + 专业技能(套某 Skills 风格) + 项目经历(多条完整) + 教育背景。数据一律用候选人的真实信息。
3. **转 PDF**：html → PDF，浏览器打印 A4（`@page size:A4; margin:0`，`.page` 宽 210mm、`min-height:297mm`）。
4. **页数检查**：确认页数合理；若 `.page` 有 `overflow:hidden` 需改流式分页 + `.proj { break-inside:avoid }` 防截断。
5. **交付核对**：逐份确认 li 数、项目顺序、配色、页数，与候选人确认后再交付。
6. **批量**：多份风格简历共用同一套正文，仅 skills 区不同 → 用 Python 脚本（`re.sub` 替换正文/项目块）批量生成，注意正则转义。

## 5 种 Skills 风格（A/B/C/D/E）

每种风格 = 各自 CSS + skills HTML 结构，正文其余部分共用同一套。

| 风格 | 结构特点 | 适用 |
|------|---------|------|
| **A 双栏分类式** | `grid 2列`，每项 `▍类目` + 描述 | 通用/最常用 |
| **B 侧栏 pill 式** | 行首浅色 pill + 同右描述（不强制换行，弱化对比） | 侧边栏风格 |
| **C 极简竖列式** | 左固定宽类目 + 右描述，黑白 | ATS 机器解析最稳 |
| **D 标签云式** | 彩色胶囊标签 `flex-wrap` | 技术岗视觉冲击 |
| **E 熟练度条式** | 每项 `技能名 + 等级 + 进度条`，条目数≥9 覆盖全栈 | 资深/管理岗 |

### Skills 内容来源（通用）
技术栈应来自候选人**真实使用的技术**，分门别类：
- **AI / LLM**：LangGraph、LangChain、LLM API、Embedding、VectorStore、可观测等（按候选人实际）
- **前端基础**：JS/TS、React 全家桶、Next.js、组件化与状态管理等
- **UI 生态**：组件库、CSS 方案、编辑器组件、拖拽等
- **工程化**：脚手架/构建工具、架构选型、重构、性能优化、Git/ESLint 等
- **全栈 / 移动端**：Node.js、MPA、WebView 桥接、监控等（按候选人实际）

### 用户反馈要点（务必遵守）
- **技能量要足够**：B 至少 7 个维度、E 至少 9 条，少了会被嫌「技能太少」。
- **不要强制换行**：pill 与描述同行。
- **重点别和其他内容差别太大**：弱化对比、轻量点缀。
- **进度条用同色系深浅分组**，避免单调。

## 还原 skills（撤销标签云/熟练度条）

用户可能要求把 skills「还原」成原 4 行 skill-item 结构。要点：
- 还原目标 = 原 4 行 skill-item（grid 两列 + `▍` 色块），**不是**标签云/熟练度条。
- 每个文件保留各自强调色（`::before` 色块用亮色系）。
- 生成脚本用**字符串拼接**而非 `str.format()`，避免 CSS 花括号冲突（报错：`KeyError: ' display'`）。
- 用 grep 验证无 cloud-tag 残留、CSS 已是 skill-item。

## 工具与技术要点

- HTML 源文件可用独立目录归档（便于改样式后重新转 PDF）。
- PDF 转换：`"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu --no-pdf-header-footer --print-to-pdf="out.pdf" "in.html"`
- 简历程序化生成可用 Next.js + Cloudflare D1（`.openclaw`/项目技能场景自定）。
- 目录路径含空格时，命令中需引号包裹。
- 文件删除优先用 `trash` 而非 `rm`；不确定就先问。

## 常见坑

- **AI 生成内容悄悄简化** —— 每次交付前必须核对 li 总数与细节完整度，这是用户最高频投诉。
- **同步后文件丢失** —— 同步到目标目录后要验证文件数量/齐全度，别只生成部分。
- **exec 临时失败(Aborted)** —— 执行环境偶发超时，简单命令也失败；稍后重试即可。
- **CSS 花括号 vs str.format** —— 生成脚本用字符串拼接，不用 `.format()`。
