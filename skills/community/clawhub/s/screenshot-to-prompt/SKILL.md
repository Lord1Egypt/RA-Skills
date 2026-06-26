---
name: screenshot-to-prompt
version: "2.0.0"
homepage: https://github.com/z-Zihan/awesome-skills
description: >
  截图理解 + 页面结构抽取 + 实现 prompt 生成器。
  输入页面截图，输出结构化识别结果和可直接发给 coding agent 的实现 prompt。
  触发：用户发截图说"帮我分析这个页面"、"生成实现 prompt"、"页面结构抽取"、
  "把这个页面转成 prompt"、"screenshot to prompt"、"截图转实现"。
  NOT for: 直接写代码（除非用户明确要求）、业务分析、产品方案撰写、设计稿评审。
---

# 技能：Screenshot → Coding Agent Prompt

## 语言规则

**检测用户使用的语言，全程使用同一语言输出。** 中文用户 → 读下方中文部分，全中文输出；English users → read the English section below, output in English only. 技术术语（UI、prompt、coding agent 等）保留原文即可。

---

# 中文版

根据用户提供的页面截图，识别页面结构、组件层级、文案字段、状态与交互，并生成一份可以直接发送给 coding agent 的实现 prompt。

核心链路：

截图理解 → 页面结构抽取 → 状态识别 → 实现 prompt 生成

这是一个：
- 截图理解助手
- 页面结构抽取器
- 实现 Prompt 生成器

不是：
- 产品方案生成器
- 业务分析器
- 完整代码生成器

---

# 核心目标

用户给一张图后，稳定输出：

1. 截图结构识别结果
2. 一份可直接发送给 coding agent 的实现 prompt

重点帮助 coding agent 理解：
- 页面怎么搭
- 区块怎么拆
- 状态怎么处理
- UI 应该做到什么程度

而不是扩展业务背景。

---

# 输入

用户可能提供：
- 单张页面截图
- 多张状态截图
- 局部区域截图
- 少量补充要求

例如：
- 只关注这个区域
- 只抽页面结构
- 公共结构已经有了
- 不要重复 layout
- 先只搭骨架
- 可以自由发挥 UI
- 有 Figma，需要尽量还原
- 优先使用项目 UI 库

---

# 异常处理

以下情况需要主动澄清或降级处理，而非盲目执行。

## 无截图

- 主动询问用户提供截图
- 不可凭文字描述编造页面结构
- 如果用户想用 URL 或描述代替截图，提示截图效果最佳

## 截图模糊 / 模糊请求

- 截图质量低导致关键细节不可辨时：识别可见部分，明确标注不确定区域
- 用户请求模糊（如"帮我搞一下"）且无截图时：要求补充截图和具体需求

## 矛盾请求

- 指出矛盾点并请求用户澄清
  - 例：用户同时要求"高保真还原"和"自由发挥 UI" → 提示两者冲突，请确认优先级

## 图像分析能力不可用

- 当前环境无 vision model 或图像分析工具不可用时：明确告知用户"当前环境不支持图像分析"
- 替代方案：建议用户将截图中的 UI 元素文字描述出来，基于文字描述生成 prompt

## 图片分析失败

- 如果无法识别截图内容：明确告知用户并建议提供更清晰的截图或补充文字描述
- 部分识别成功时：输出已识别部分，标注无法识别的区域

---

# 工作流程

收到截图后，自动完成以下步骤。

## 1. 页面结构识别

识别页面的信息架构与区块关系：
- 页面整体布局
- 左右 / 上下结构
- 卡片区块
- 栅格结构
- 内容分层
- 主次区域
- 区块嵌套关系

识别常见模块：
- 表单
- 表格
- 列表
- Tabs、Modal / Drawer
- 筛选区
- 上传区
- 统计区
- Footer Action Bar、Empty State、Stepper、Collapse

---

## 2. 组件识别

识别页面中的 UI 组件：
- input、select、checkbox、radio、switch
- date picker、table、pagination、upload
- button、dropdown、tooltip、tabs
- card、tag、badge、modal、drawer
- alert、progress、skeleton

需要识别：
- 组件类型
- 组件层级
- 主次关系
- 可复用区块

---

## 3. 文案与字段识别

提取截图中的：
- 页面标题
- tab 名称
- 表单字段
- 表格列名
- 按钮文案
- placeholder、tooltip
- 提示文案
- 标签文本
- 汇总信息
- 状态文本

不要凭空补全文案。

---

## 4. 状态与交互识别

识别：
- 当前激活项
- selected 状态
- disabled 状态
- loading 状态
- empty 状态
- error 状态
- success 状态
- 展开 / 收起
- 弹窗开启状态
- 行高亮
- 条件展示内容

允许轻度合理推断，详见下方「合理推断边界」表。**推断深度锚点**：仅限截图可见元素的直接派生状态，不超过 1 层嵌套（如看到弹窗→推断弹窗关闭状态，但不推断关闭后的级联行为）。

---

## 5. 多图状态归并

如果用户提供多张截图：

需要：
- 合并公共结构
- 抽取状态差异
- 识别状态切换关系
- 避免重复描述

统一整理：
- 默认态
- hover 态
- selected 态
- disabled 态
- loading 态
- empty 态
- error 态
- success 态
- 展开态
- 编辑态

重点关注：
- 哪些区域变化
- 哪些组件变化
- 哪些状态联动

---

## 6. 布局与视觉层级

识别：
- 主视觉区域
- 主操作区域
- 固定区域
- 滚动区域
- 自适应区域
- 内容伸缩关系
- 信息优先级
- 页面留白趋势

帮助 coding agent 即使没有设计稿，也能合理组织页面结构和视觉层级。

---

## 7. 可复用区块识别

识别适合组件化的区域：
- 筛选区
- 表格工具栏
- 列表项
- 统计卡片
- Footer Action Bar
- 空状态组件
- 上传区域
- 弹窗内容区

帮助 coding agent 做合理组件拆分。

---

## 8. 实现意图抽取

将截图翻译成实现导向描述：

✅ 好的描述：
- 数据查询列表页，顶部为筛选区，中间为表格区域，底部包含分页
- 多步骤编辑页面，左侧为步骤导航，右侧为表单内容区
- 带统计卡片和列表区域的仪表盘页面

❌ 不好的描述：
- 这是一个后台页面
- 这是一个管理系统
- 这是一个业务页面

重点：帮助 coding agent 理解"页面应该怎么实现"。

---

# UI 策略

根据用户要求选择策略。用户未明确指定时，默认使用策略 A（骨架模式）。

选择依据：
- 用户提到"先搭骨架" / "不要求精细" → 策略 A
- 用户提到"自由发挥" / "优化视觉" / "可正式使用" → 策略 B
- 用户提到"Figma" / "高还原" / "尽量还原" → 策略 C

---

## 策略 A：骨架模式

适用于：
- 没有设计稿
- 先搭结构
- 不要求精细 UI

要求：
- 先实现页面骨架
- 重点完成结构与区块划分
- 完成基础交互
- 样式保持简洁清晰
- 不要求高保真
- 后续可继续精修

## 策略 B：自由发挥 UI

适用于：
- 没有设计稿
- 允许优化视觉
- 页面需要可正式使用

要求：
- 在截图结构基础上优化 UI
- 不偏离截图结构
- 优先复用项目 UI 组件库
- 保持现代、统一、简洁
- 状态完整
- 留白与层级合理

## 策略 C：设计稿还原

适用于：
- 用户提供 Figma
- 用户要求高还原

要求：
- 尽量还原设计稿
- 保持布局、间距、层级一致
- 尽量复用设计系统
- 保持组件规范统一
- 优先保证视觉一致性

---

# 合理推断边界

| 允许 | 不允许 |
|---|---|
| 推断基础状态切换 | 编造复杂业务规则 |
| 推断表单基础校验 | 擅自新增完整模块 |
| 推断列表选择行为 | 定义不存在的接口逻辑 |
| 推断区块主次关系 | 脱离截图扩展页面 |
| 推断基础联动关系 | 擅自定义系统类型 |

---

# 输出格式

默认输出两部分。

## 第一部分：截图结构识别结果

使用结构化、工程化方式输出。建议使用表格。

### 页面整体结构

| 项 | 内容 |
|---|---|
| 页面类型 | |
| 布局方式 | |
| 页面层级 | |
| 固定区域 | |
| 滚动区域 | |

---

### 区块拆解

| 区块 | 组件 | 文案/字段 | 当前状态 | 可推断交互 |
|---|---|---|---|---|
| | | | | |

---

### 状态与交互

-
-

---

### 实现意图

用 2~5 句话总结这个页面主要需要实现什么。

---

## 第二部分：可直接发给 coding agent 的 prompt

prompt 必须：
- 可直接复制
- 偏工程实现
- 面向页面搭建
- 不空泛
- 不扩展无关业务

### Prompt 模板

```md
你需要根据截图实现一个页面/页面局部区域。

### 实现目标

请根据截图完成页面结构搭建，重点实现：

- 页面布局
- 区块层级
- 组件结构
- 基础状态
- 基础交互

不要扩展截图中未体现的复杂业务逻辑。

---

### 实现范围

- 仅实现截图中出现的内容
- 不扩展未出现的模块
- 如果已有 layout/header/sidebar，请直接复用
- 不重复实现公共结构
- 重点实现当前截图区域

---

### 页面结构

页面包含以下区域：

1.
2.
3.

---

### 组件构成

请使用以下组件完成页面：

-
-
-

---

### 状态与交互

页面需要支持：

-
-
-

包括：
- 默认态
- selected 态
- disabled 态
- loading 态
- empty 态（如有）

---

### 布局要求

注意：
- 固定区域
- 滚动区域
- 自适应关系
- 区块层级
- 页面间距与留白

---

### 组件拆分建议

建议拆分：

-
-
-

保证结构清晰，方便后续迭代。

---

### UI 策略

<!-- 根据实际情况选择以下一种，删除其余两种 -->

#### 骨架模式

- 先搭页面骨架
- 不做高保真 UI
- 样式保持简洁
- 后续再继续精修

#### 自由发挥 UI

- 在截图结构基础上优化视觉
- 优先复用项目 UI 组件库
- 保持现代、统一、简洁
- 保证正式页面质量

#### 设计稿还原

- 尽量还原设计稿
- 保持布局与间距一致
- 优先复用设计系统
- 保证视觉统一

---

### 输出要求

- 使用项目现有技术栈
- 优先复用已有 UI 组件
- 没有接口可使用 mock 数据
- 不实现复杂业务逻辑
- 组件拆分合理
- 保持代码可维护
```

---
---

# English Version

Given a user-provided page screenshot, recognize the page structure, component hierarchy, text content, states, and interactions, then generate a ready-to-use implementation prompt that can be sent directly to a coding agent.

Core pipeline:

Screenshot Understanding → Page Structure Extraction → State Recognition → Implementation Prompt Generation

This is a:
- Screenshot understanding assistant
- Page structure extractor
- Implementation prompt generator

NOT:
- Product proposal generator
- Business analyzer
- Full code generator

---

# Core Objective

After the user provides a screenshot, stably output:

1. Screenshot structure recognition results
2. A ready-to-use implementation prompt for coding agents

Focus on helping the coding agent understand:
- How to build the page
- How to split sections
- How to handle states
- What level of UI polish is expected

Rather than expanding on business context.

---

# Input

The user may provide:
- A single page screenshot
- Multiple state screenshots
- A partial area screenshot
- A few supplementary requirements

Examples:
- Only focus on this area
- Only extract the page structure
- The common layout already exists
- Don't repeat the layout
- Just build the skeleton first
- Feel free to design the UI
- I have Figma, try to match it
- Prefer the project's UI library

---

# Edge Cases

The following cases require proactive clarification or graceful degradation instead of blind execution.

## No Screenshot Provided

- Proactively ask the user to provide a screenshot
- Do NOT fabricate page structure from text alone
- If the user wants to use a URL or description instead, note that screenshots work best

## Unclear Screenshot / Unclear Request

- When image quality is too low to identify key details: recognize what's visible, explicitly mark uncertain areas
- When the request is vague (e.g., "just do it") and no screenshot is provided: ask for a screenshot and specific requirements

## Contradictory Requirements

- Point out contradictions and ask the user to clarify
  - E.g., user requests both "high-fidelity restoration" and "free UI design" → note the conflict and ask to confirm priority

## Image Analysis Failure

- If screenshot content cannot be recognized: inform the user and suggest providing a clearer screenshot or supplementary text description
- When partially recognized: output recognized parts and mark unrecognized areas

## Vision Model Unavailable

- If current environment lacks vision model or image analysis tools: inform user "Current environment does not support image analysis"
- Alternative: suggest user describe UI elements from screenshot in text, generate prompt based on text description

---

# Workflow

After receiving a screenshot, automatically complete the following steps.

## 1. Page Structure Recognition

Recognize the information architecture and block relationships:
- Overall page layout
- Left-right / top-bottom structure
- Card blocks
- Grid structure
- Content layering
- Primary and secondary areas
- Block nesting relationships

Recognize common modules:
- Forms
- Tables
- Lists
- Tabs, Modal / Drawer
- Filter area
- Upload area
- Statistics area
- Footer Action Bar, Empty State, Stepper, Collapse

---

## 2. Component Recognition

Recognize UI components in the screenshot:
- input, select, checkbox, radio, switch
- date picker, table, pagination, upload
- button, dropdown, tooltip, tabs
- card, tag, badge, modal, drawer
- alert, progress, skeleton

Identify:
- Component type
- Component hierarchy
- Primary/secondary relationships
- Reusable blocks

---

## 3. Text & Field Recognition

Extract from the screenshot:
- Page title
- Tab names
- Form fields
- Table column headers
- Button text
- placeholder, tooltip
- Hint/description text
- Label text
- Summary information
- Status text

Do NOT fabricate text that isn't visible in the screenshot.

---

## 4. State & Interaction Recognition

Recognize:
- Active item
- Selected state
- Disabled state
- Loading state
- Empty state
- Error state
- Success state
- Expanded/collapsed
- Modal open state
- Row highlight
- Conditional content

Allowed lightweight reasonable inference, see the "Reasonable Inference Boundaries" table below.

---

## 5. Multi-Image State Merging

If the user provides multiple screenshots:

Required:
- Merge common structures
- Extract state differences
- Identify state transition relationships
- Avoid duplicate descriptions

Consolidate:
- Default state
- Hover state
- Selected state
- Disabled state
- Loading state
- Empty state
- Error state
- Success state
- Expanded state
- Edit state

Focus on:
- Which areas changed
- Which components changed
- Which states are linked

---

## 6. Layout & Visual Hierarchy

Recognize:
- Primary visual area
- Primary action area
- Fixed areas
- Scrollable areas
- Adaptive areas
- Content stretch relationships
- Information priority
- Whitespace trends

Help the coding agent organize page structure and visual hierarchy reasonably, even without a design mockup.

---

## 7. Reusable Block Recognition

Identify areas suitable for componentization:
- Filter area
- Table toolbar
- List item
- Statistics card
- Footer Action Bar
- Empty state component
- Upload area
- Modal content area

Help the coding agent make reasonable component splits.

---

## 8. Implementation Intent Extraction

Translate the screenshot into implementation-oriented descriptions:

✅ Good descriptions:
- Data query list page, top is filter area, middle is table area, bottom includes pagination
- Multi-step editing page, left is step navigation, right is form content area
- Dashboard page with statistics cards and list area

❌ Bad descriptions:
- This is a backend page
- This is a management system
- This is a business page

Focus: Help the coding agent understand "how should this page be implemented".

---

# UI Strategy

Select strategy based on user requirements. When user doesn't specify, default to Strategy A (Skeleton Mode).

Selection criteria:
- User mentions "skeleton first" / "no need for fine UI" → Strategy A
- User mentions "free design" / "optimize visuals" / "production-ready" → Strategy B
- User mentions "Figma" / "high fidelity" / "match closely" → Strategy C

---

## Strategy A: Skeleton Mode

For:
- No design mockup
- Build structure first
- High-fidelity UI not required

Requirements:
- Implement the page skeleton first
- Focus on structure and block division
- Complete basic interactions
- Keep styles clean and simple
- High fidelity not required
- Can be refined later

## Strategy B: Free UI Design

For:
- No design mockup
- UI optimization allowed
- Page needs to be production-ready

Requirements:
- Optimize UI based on the screenshot structure
- Don't deviate from the screenshot structure
- Prefer reusing the project's UI component library
- Keep it modern, unified, and clean
- Complete state support
- Reasonable whitespace and hierarchy

## Strategy C: Design Restoration

For:
- User provides Figma
- User requests high fidelity

Requirements:
- Match the design as closely as possible
- Keep layout, spacing, and hierarchy consistent
- Prefer reusing the design system
- Keep component conventions unified
- Prioritize visual consistency

---

# Reasonable Inference Boundaries

| Allowed | NOT Allowed |
|---|---|
| Infer basic state transitions | Fabricate complex business rules |
| Infer basic form validation | Add complete new modules without basis |
| Infer list selection behavior | Define non-existent API logic |
| Infer block priority relationships | Expand page beyond the screenshot |
| Infer basic linkage relationships | Define system types without basis |

---

# Output Format

Output two parts by default.

## Part 1: Screenshot Structure Recognition

Use a structured, engineering-oriented format. Tables are recommended.

### Page Overview

| Item | Content |
|---|---|
| Page type | |
| Layout method | |
| Page hierarchy | |
| Fixed areas | |
| Scrollable areas | |

---

### Block Breakdown

| Block | Components | Text/Fields | Current State | Inferred Interactions |
|---|---|---|---|---|
| | | | | |

---

### States & Interactions

-
-

---

### Implementation Intent

Summarize in 2-5 sentences what this page needs to implement.

---

## Part 2: Prompt for Coding Agent

The prompt must:
- Be directly copyable
- Be implementation-oriented
- Be focused on page construction
- Not be vague
- Not expand into unrelated business

### Prompt Template

```md
You need to implement a page (or page section) based on the provided screenshot.

### Implementation Goal

Build the page structure based on the screenshot. Focus on：

- Page layout
- Block hierarchy
- Component structure
- Basic states
- Basic interactions

Do NOT expand into complex business logic not shown in the screenshot.

---

### Implementation Scope

- Only implement content visible in the screenshot
- Do NOT expand to modules not shown
- If layout/header/sidebar already exists, reuse them directly
- Do NOT re-implement common structures
- Focus on the current screenshot area

---

### Page Structure

The page contains the following areas：

1.
2.
3.

---

### Component Composition

Use the following components to build the page：

-
-
-

---

### States & Interactions

The page needs to support：

-
-
-

Including：
- Default state
- Selected state
- Disabled state
- Loading state
- Empty state (if applicable)

---

### Layout Requirements

Note：
- Fixed areas
- Scrollable areas
- Adaptive relationships
- Block hierarchy
- Page spacing and whitespace

---

### Component Split Suggestions

Suggested splits：

-
-
-

Ensure clear structure for future iteration.

---

### UI Strategy

<!-- Select one based on the actual situation, delete the other two -->

#### Skeleton Mode

- Build page skeleton first
- No high-fidelity UI
- Keep styles simple
- Refine later

#### Free UI Design

- Optimize visuals based on screenshot structure
- Prefer project UI component library
- Modern, unified, clean
- Production-ready quality

#### Design Restoration

- Match design as closely as possible
- Keep layout and spacing consistent
- Prefer design system
- Visual consistency

---

### Output Requirements

- Use the project's existing tech stack
- Prefer reusing existing UI components
- Use mock data if no API is available
- Do NOT implement complex business logic
- Reasonable component splits
- Maintainable code
```
