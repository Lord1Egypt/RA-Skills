---
name: self-improving-tech-ppt
version: 1.1.0
license: MIT
description: >-
  Model-agnostic self-improving agent workflow (提示 → 利用 → 记忆 → 自检循环) for designing
  and iterating high-density executive technical planning PPT slides (native editable .pptx
  via Python, hard programmatic color/density/anti-AI gates, QuickLook visual inspection,
  and persistent critique memory). Use when the user asks to create, refine, or iterate
  technical architecture/planning slides, single-page technical schematics, or executive PPT
  decks that require crisp logic, zero AI buzzwords, and visual QA across multiple rounds.
metadata:
  openclaw:
    requires:
      bins:
        - python3
---

# 自我改进技术 PPT 代理（提示 → 利用 → 记忆 → 自检循环）

本技能将「**提示 → 利用 → 记忆 → 自检循环**」固化为**跨模型一致（ChatGPT / DeepSeek / Claude / Gemini 通用）**的标准工作流，用于打造**高信息密度、去 AI 味、原生可编辑（`.pptx`）的技术架构与技术规划汇报页**。

核心原则：**不靠空泛文字祈祷模型自觉，而是用「高密度架构蓝图 + 代码级配色/密度/反 AI 硬门禁 + 真实渲染图审图 + 持久纠偏记忆」四重约束，杜绝不同模型回落到低密度「AI 博客风 PPT」或深绿配橙黄的廉价 AI 配色。**

---

## 零、跨模型防漂移铁律（所有模型强制遵守！）

> 很多强对话模型（如 ChatGPT）默认偏好生成「Gamma/Keynote 博客风」稀疏图文页（超大标题 + 1 句例句黑条 + 2 栏大留白文字表 + 底部整行橙黄框 + 拆成十来页稀释水页）。**以下四条为代码级硬红线，违反将被 `run_self_check(mode="tech-arch")` 直接拦截：**

1. **严禁擅自切换主题，默认锁死 `executive-blue`**：
   - 除非用户在当前指令中明确指定切换风格或提供企业 VI 色板，**必须使用默认 `executive-blue`（沉稳企业蓝）**；严禁模型自作主张挑选深青绿/薄荷绿或高饱和撞色。
2. **严禁画「底部整行橙黄/琥珀提示条」**：
   - 琥珀色（`amber_bg / amber_bdr`）**仅限极小异常分支节点与虚线箭头**（单节点宽 `≤ 240pt`、全页总面积 `≤ 4.5%`），绝不许拉通整页底部的橙色提示框。
3. **严禁「Gamma 博客风稀疏水页」**：
   - 禁止「小横线眉标 + 超大 24~32pt 标题 + 一句话原话黑条 + 2 栏稀疏表格」版式；禁止用一整页只讲一句玩具业务例句；
   - 技术规划/架构页必须直接基于 [examples/demo_tech_slide.py](./examples/demo_tech_slide.py) 的**完整四区高密度架构蓝图**（顶部 `问题→目标` + 左侧 `3 大挑战与核心概念` + 右侧 `1:1 对应技术泳道与说明卡` + 底部 `演进回归条`），单页不少于 `35` 个结构化节点与 `6` 条正交连接线。
4. **必须调用严格模式自检**：
   - 每次生成后必须执行 `run_self_check(scene, mode="tech-arch")`（同时开启 `enforce_palette=True` 配色锁、琥珀面积上限、防超大标题与四象限密度校验），绝不允许跳过或降级为 `minimal` 交付。

---

## 核心四步循环（每轮必走）

```text
[1. 提示解构] ──▶ [2. 利用与构建] ──▶ [3. 记忆沉淀] ──▶ [4. 双重自检] ──▶ 交付预览
      ▲                                                       │
      └──────────── 发现逻辑/文案/渲染缺陷 → 就地修复重跑 ──────────┘
```

### 第一步：提示解构（Prompt Deconstruction）
收到新需求或用户反馈后，**先拆清四项边界，严禁直接堆框画图**：
1. **锁死四问主线**：**为什么做 → 解决什么问题 → 关键技术是什么 → 怎么实现**。绝不把技术架构页画成业务流程图。
2. **分离「锁定项」与「改动项」**：
   - 用户明确说「内容不动，调排版」「组件对了，色调不好」时，先列出**已锁定不可回退的资产**（如已过审文案、组件结构、配色基线），再做定点外科手术，**严禁整版推倒重来或过度回退**。
3. **吸收参考图的正确姿势**：参考优秀范例时，只提取其**信息密度、视觉层次、图形语言与配色克制感**；**严禁照抄外部格式壳子**（如为了抄「左 2 右 2」强行破坏本页「左 3 挑战 ↔ 右 3 泳道」的一一对应关系）。
4. **先理清概念逻辑再动笔**：
   - **杜绝循环论证**：我们要引入的解决方案载体（如 `DSL`、新框架、新引擎）**只能出现在目标与方案区**，绝不能写进「问题」和「技术挑战」里；
   - **缩写与落地形态必须讲透**：引入核心英文缩写（如 `DSL`）时，必须写清全称、中文定义、为何能破题，以及**产出物和最终运行形态**（如生成标准定义文件、编译为代码执行或配合运行层执行）；
   - **技术概念严谨性评审**：容易引发歧义的专业词（如 `URI` 易听成网页 `URL`）优先用无歧义中文（如「标准标识」「引用」）；继承关系（如 `is-a`）必须严守逻辑边界，不能把互斥冲突强行挂成父子继承。

### 第二步：利用与构建（Leverage & Build）
1. **先归档再修改**：每次改版前先将当前 `.pptx` 备份到 `archive/<name>_vN存档.pptx`，保留可追溯基线。
2. **复用引擎脚本**：直接复用本技能附带的 [ppt_engine.py](./scripts/ppt_engine.py)（见示例 [demo_tech_slide.py](./examples/demo_tech_slide.py)），原生生成 16:9 (`960×540 pt`) 可编辑 PowerPoint 文件 + 矢量图标 + SVG 预览。
   - 若当前环境未安装 `python-pptx` 与 `Pillow`，先创建独立虚拟环境：
     ```bash
     python3 -m venv .ppt_venv && .ppt_venv/bin/pip install python-pptx pillow
     ```
3. **风格可切换，默认锁死且绝不擅自换色**：
   - 默认风格强制为沉稳企业蓝（`executive-blue`）；仅在用户明确提出换风格时，才切换到 `slate-minimal` / `steel-teal` / `academic-indigo`，或通过 `build_theme(base=..., overrides={...})` 注入指定品牌色；
   - 若用户提供了参考图或企业 VI 色板，优先吸纳其色调并写入当前任务的记忆账本锁定，绝不生搬硬套其他主题色。
4. **遵循规范参考**：构建前阅读 [design-and-anti-ai-rules.md](./references/design-and-anti-ai-rules.md)，严格执行反 AI 味黑名单、主题克制原则与精细组件比例（杜绝「大方块、大圆柱」）。

### 第三步：记忆沉淀（Persistent Memory）
在当前任务工作目录或 scratch 目录下维护一份持久记忆账本（模板见 [memory-template.md](./references/memory-template.md)）：
1. **把用户每一次纠偏转成三条硬资产**：
   - **写入记忆账本**：记录「用户指出的问题 → 根因 → 永久禁令 → 已锁定保留项」；
   - **追加代码黑名单**：把暴露出的 AI 词、病句、口语词、跨页硬编码章节号、易混缩写立即加入脚本的 `BANNED_WORDS` 或 `forbid_terms` 校验；
   - **固化视觉参数**：把用户认可的色调、字号、组件高度与对齐坐标固定为常量。
2. **每轮生成前必先回读记忆账本**，确认本轮修改不破坏任何历史锁定项。

### 第四步：双重自检循环（Automated + Visual Self-Check Loop）
**严禁把未经实图检查的 `.pptx` 交给用户！** 必须串联通过两道门禁，任一门禁不通过直接自修重跑，直到零缺陷：

1. **门禁 A · 代码级静态与审美自检（`run_self_check(scene, mode="tech-arch")` 自动拦截）**：
   - **0 越界配色与 AI 橙黄横幅**：严格锁定活动 `scene.theme` 色板，琥珀色节点单宽 `≤ 240pt` 且全页占比 `≤ 4.5%`；
   - **0 稀疏水页与超大标题**：强制单页结构密度（`≥ 35` 节点、`≥ 6` 正交连线、四象限均衡覆盖 `≥ 55%`、字号 `≤ 19pt`），自动拦截 Gamma/Keynote 式博客表格页；
   - **0 斜线**：所有连线必须 100% 90° 横平竖直正交；
   - **0 循环论证**：问题与挑战节点开启 `forbid_terms` 拦截核心方案词；
   - **0 禁词与病句**：逐节点扫描 `BANNED_WORDS`（AI 味空词、伪口语、生僻自造词、跨页章节号、玩具案例、`原话/解析示意` 稀释信号）；
   - **0 括号与溢出**：正文字段零圆括号，单行标记节点绝不意外折行，所有文本框总高度不得超出容器可用高度。
2. **门禁 B · 真实渲染图视觉核验（QuickLook + 局部放大裁剪 + `read_file` 肉眼审图）**：
   - **必须用真实的 `.pptx` 渲染结果审图**（macOS 用 `qlmanage -t -s 1920` 渲染 `.pptx`，不能只看 Chrome 渲染的 SVG，防止 PowerPoint 原生字体/圆柱盖/菱形边距差异漏检！）；
   - 调用 `render_quicklook_and_crop()` 生成整页高清图 + **关键密集区域放大裁剪图**，并用 `read_file` 亲自逐区检查：
     - 有无文字贴边、裁切、意外换行、重叠？
     - 有无粗笨的「大方块、大圆柱」或大块空洞留白？
     - 渐变方向（特别是旋转三角形 `wedge_r`）、圆柱盖边距、箭头对齐是否横平竖直？
     - 整页逐句默读一遍：有无语病、重复用词、生僻缩写或逻辑断层？
3. **同步交付**：
   - 将**真实的 QuickLook 渲染图**同步到输出 PNG、预览文档及在线协作文档；
   - 回复用户时简洁列出本轮改动点与交付文件路径。

---

## 附带资源索引

- **设计规范、去 AI 味黑名单与组件防踩坑指南**：[references/design-and-anti-ai-rules.md](./references/design-and-anti-ai-rules.md)
- **每轮迭代记忆账本模板**：[references/memory-template.md](./references/memory-template.md)
- **原生 PPTX / 图标 / 自检 / QuickLook 渲染引擎**：[scripts/ppt_engine.py](./scripts/ppt_engine.py)
- **最小可运行单页示例**：[examples/demo_tech_slide.py](./examples/demo_tech_slide.py)
