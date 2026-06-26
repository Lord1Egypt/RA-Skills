---
name: teaching-app-builder
description: 把一段教学文本/知识点/讲义/概念做成单文件 HTML 交互教学展示 app。当用户想把内容做成网页演示、交互课件、可视化讲解、教学 demo、HTML 展示页，或想用 Chart.js/ECharts 图表、Mermaid 流程图、KaTeX/MathJax 公式、SVG 示意图、交互动画把某个知识点讲清楚时使用。产出单个 .html 文件（浏览器双击即开、无需服务器或构建），库通过中国大陆可访问的 CDN（BootCDN/staticfile/360/npmmirror）引用，内置 6 套专业配色方案。即使用户只说"做个网页/做个演示/可视化一下这段内容/把这章做成交互的"而没有明说"教学 app"，只要意图是把知识内容做成可交互的展示页面，也应使用本 skill。
---

# Teaching App Builder：文本 → 单文件交互教学 App

把一段教学内容变成**一个可双击打开的 HTML 文件**：所有 HTML/CSS/JS 内联其中，需要的库走中国大陆 CDN，配色专业，交互服务于理解。

## 四条核心原则

1. **单文件自洽**——所有代码在一个 `.html` 里，双击即开，不需要服务器、不需要 `npm`、不需要构建。外部只有 CDN 链接。
2. **CDN 必须国内可达**——库一律从 BootCDN / staticfile / 360 / npmmirror 引；URL 从 `references/cdn-catalog.md` 取（已逐条验证），不要凭记忆拼地址。
3. **交互为理解服务**——交互的唯一目的是让抽象可操作、过程可单步、对比可并置、因果可试错。讲得清的别加动效，动效不是目的。
4. **忠于原文**——把输入文本讲清楚、讲生动，但不编造原文没有的事实、数据、研究、引文。不确定的留白或标注，不要造。

## 工作流（5 步）

### 1. 读懂文本，定教学目标
这段内容的核心概念是什么？学完要能**理解什么、会做什么**？逐点判断：哪些"静态文字+一张图"就讲清了，哪些"非交互不可"（过程演化、参数因果、需要亲手试、需要并置对比）。只给后者做交互。

### 2. 把内容映射到交互形态
用下面的决策表，把每个知识点落到一种交互形态：

| 内容是…… | 交互形态 | 用什么 |
|---|---|---|
| 数值 / 统计 / 趋势 / 分布 | 可交互图表 | Chart.js（简单）/ ECharts（复杂、国产生态） |
| 流程 / 结构 / 关系 / 时序 / 分类树 | 图解 | Mermaid |
| 过程 / 推导 / 算法步骤 | 步骤器（分步揭示）+ 配图 | 零依赖 stepper（components.md）+ SVG/Canvas |
| 数学公式 / 含可调参数的关系 | 公式渲染 + 滑块联动 | KaTeX（常规）/ MathJax（复杂）+ range 滑块 |
| 自定义示意图 / 几何 / 状态机 | SVG 绘制（草图感加手绘） | SVG.js / 原生 SVG / Rough.js |
| 完全自定义的数据可视化交互 | 数据驱动 SVG | D3 |
| 元素入场 / 依次点亮 / 演示编排 | 补间动画 | anime.js（轻）/ GSAP（强） |
| 知识点分类 / 多观点对照 | 标签页 / 左右并置 / 手风琴 | 零依赖（components.md） |
| 代码教学 | 高亮 +（可选）Markdown 渲染 | Highlight.js + marked |
| 巩固 / 自测 | 即时反馈测验 | 零依赖 quiz（components.md） |
| 一页页翻的课件 | 翻页幻灯 | Reveal.js（仅当明确要"PPT/幻灯"） |
| 整体排版 / 响应式 | 栅格 / 现成组件 | Tailwind / Bootstrap，或只用配色变量手写 |

### 3. 选库——最小集
**能零依赖就零依赖**：标签页、手风琴、步骤器、滑块联动、测验、目录导航、术语提示，纯 HTML/CSS/JS 就做得好（`references/components.md`），别为它们引框架。确实需要图表/公式/图解/复杂动画时，才按 `references/libraries.md` 引——每个库给了即用片段和易错坑。引入的库必须真的用上。

### 4. 选配色方案
按学科语境从 `references/color-schemes.md` 选一套（深空蓝/学术纸张/清新薄荷/暖阳赭橙/靛青商务/暗夜霓虹），把它的 `:root` 段贴进去。6 套共用一套变量名，颜色全走 `var(--…)`。遵守 60-30-10：主色和点缀色是"盐"，不要大面积铺。

### 5. 组装单文件 + 自检
以 `references/skeleton.md` 的骨架为地基（它自带通用 UI 原子：card/btn/callout/badge/grid，省得从零写样式），填入内容与交互，**用 Write 工具写出文件**，然后逐条过 skeleton.md 末尾的质量清单。

## 输出约定

- **写成一个 `.html` 文件**，文件名用 kebab-case 反映主题（如 `entropy-explained.html`、`photosynthesis-steps.html`），不要含日期。
- 默认写到**当前工作目录**；用户指定了路径就用用户的。不确定放哪就先问一句，或放当前目录并在回复里给出完整路径。
- **不要把整份 HTML 源码贴进对话**——用 Write 工具写文件，对话里只给路径 + 一两句说明"这个 app 讲什么、关键交互是什么、用了哪几个库、哪套配色"。
- 默认界面语言跟随输入文本（中文内容→中文 UI）。

## 渐进式披露：何时读哪个文件

不要一上来把所有 reference 全读。按需 Read：

| 你正要…… | 读 |
|---|---|
| 拼任何一个 CDN 链接 / 加载 fallback / Tailwind 国内方案 | `references/cdn-catalog.md` |
| 选/贴配色，或让图表-Mermaid 配色和页面统一 | `references/color-schemes.md` |
| 用某个库（Chart.js/ECharts/Mermaid/KaTeX/D3/SVG/动画/代码/Reveal）需要正确初始化片段 | `references/libraries.md` |
| 做标签页/步骤器/手风琴/滑块联动/测验/目录/术语提示等零依赖交互 | `references/components.md` |
| 开新文件要骨架、或交付前过质量清单 | `references/skeleton.md` |

典型一次生成会读 2–4 个：`skeleton`（地基）+ `color-schemes`（选色）+ `libraries`/`components`（按选用的交互）+ 需要时 `cdn-catalog`（核对 URL）。

## 常见反模式（别犯）

- ❌ 为一个手风琴引整个 Bootstrap、为几个间距引整个 Tailwind——能零依赖就零依赖。
- ❌ 凭记忆写 CDN URL（库名大小写、版本号极易错）——查 cdn-catalog.md。
- ❌ 满屏炫动效却没讲清概念——交互必须服务理解。
- ❌ 大段正文上彩色、主色铺满背景——破坏专业感，守 60-30-10。
- ❌ 编造原文没有的"数据/研究/事实"来撑满图表——宁可少做交互，不可造假。
- ❌ Chart.js 的 canvas 不放固定高度容器（页面会被无限撑高）——见 libraries.md。
- ❌ 把几百行 HTML 源码糊进对话——Write 写文件，对话只给路径。
