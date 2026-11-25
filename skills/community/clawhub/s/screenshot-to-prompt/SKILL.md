---
name: screenshot-to-prompt
version: "2.1.0"
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

# 截图复杂度判断

在执行工作流之前，**必须先判断截图复杂度**，决定执行深度和输出详细程度：

| 复杂度 | 判定标准 | 工作流调整 |
|--------|---------|-----------|
| **简单** | 单组件或极少组件（如：登录框、单个弹窗、简单表单） | 步骤 1-2 合并为"结构与组件识别"，步骤 3-5 可跳过，步骤 6-8 简化输出 |
| **中等** | 多组件页面（如：带筛选的列表页、设置页、多 tab 页） | 步骤 1-5 正常执行，步骤 6-8 简化 |
| **复杂** | 完整页面含复杂交互（如：仪表盘、多区块联动、带弹窗+抽屉的页面） | 步骤 1-8 全部执行，输出完整 |

**判断时机：** 在分析截图后、输出结果前，首先声明复杂度等级（一行即可，如"复杂度：简单"）。

**简化输出规则（简单截图）：**
- 结构识别 + 组件识别合并为一个表格
- 不输出文案字段表、状态与交互表、多图归并、布局层级（除非截图中有明显内容）
- 实现意图 1-2 句话即可
- Prompt 模板简化：省略"组件拆分建议"和"布局要求"section

---

# 工作流程

收到截图后，先判断复杂度，再按对应深度执行以下步骤。

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

若已知项目 UI 库（用户说明或同会话上下文可见），把识别到的通用组件映射为该库的组件名（如 select → el-select / AntD Select），并写入输出；无法确定映射时保留通用名，不要编造库组件。映射结果直接供实现 prompt 的「组件构成」使用。

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

## 4.5 响应式断点处理

截图通常是单一视口（多为桌面宽度）。识别时评估页面在窄视口下的适配方式，并写进输出，避免 coding agent 产出桌面固定布局：

- 布局形态判断：识别当前结构是栅格卡片、左右分栏还是固定侧栏，推断窄视口下的合理折叠方式（分栏变堆叠、卡片列数递减、侧栏变抽屉/底部导航）
- 固定像素风险：截图无法给出断点数值，标注"哪些区块需要响应式"而不是编造具体断点；实现 prompt 中明确要求使用项目已有的响应式设施（如 UI 库栅格、容器查询、现有断点变量）
- 无法判断时：在实现意图中注明"截图为桌面视口，移动端布局需另行确认"，不要静默假设单端

以下情况跳过本步：用户明确说明只做桌面端，或截图本身就是窄视口（此时反向检查桌面适配同理）。

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

## 正反例说明

**规则：推断不超过 1 层嵌套** —— 仅允许从截图可见元素直接推断其直接派生属性/状态，不允许基于推断结果再做进一步推断。

✅ 允许（1 层推断）：
- 从按钮样式（醒目、主色调）推断"可能是提交按钮" → 直接属性推断
- 从弹窗的打开状态推断"弹窗可以关闭" → 直接状态推断
- 从表单字段旁的红星推断"该字段为必填" → 直接语义推断
- 从列表项的选中背景色推断"该列表支持选择" → 直接行为推断
- 从灰色按钮推断"该按钮当前禁用" → 直接状态推断

❌ 不允许（2 层嵌套推断）：
- 从按钮样式推断"这是登录页面的注册流程入口" → 按钮样式 → 功能推断 → 流程推断（2 层）
- 从表单校验推断"提交后会触发邮件通知" → 校验规则 → 提交行为 → 副作用推断（2 层）
- 从列表选择行为推断"选中后可以批量导出数据" → 选择 → 批量操作 → 具体功能（2 层）
- 从弹窗推断"弹窗关闭后会刷新父页面数据" → 弹窗 → 关闭 → 级联行为（2 层）
- 从页面布局推断"这是某个 SaaS 产品的后台" → 布局 → 页面类型 → 产品类型（2 层）

---

# 输出格式

默认输出两部分。

## 第一部分：截图结构识别结果

使用结构化、工程化方式输出。建议使用表格。

> **简单截图可省略以下子表格中无明显内容的表**，直接用一个合并的简洁表格覆盖。

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

用 2~5 句话总结这个页面主要需要实现什么。（简单截图 1-2 句即可）

---

## 第二部分：可直接发给 coding agent 的 prompt

prompt 必须：
- 可直接复制
- 偏工程实现
- 面向页面搭建
- 不空泛
- 不扩展无关业务

### Prompt 模板

> **简单截图使用简化版 Prompt**：省略"组件拆分建议"和"布局要求"section，其他 section 保留但内容精简。

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

<若结构识别已完成 UI 库映射：优先使用列出的库组件，找不到对应组件时用最接近的原生实现并注明>

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

响应式要求：

- 使用项目已有的响应式设施（UI 库栅格、断点变量、容器查询），不要引入新的断点体系
- <需要响应式的区块按结构识别结果填写；截图为单一视口，具体断点数值由项目现有设施决定>
- <截图仅单一视口时注明：移动端/窄视口布局需另行确认，不做静默假设>

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

> **This skill is written in Chinese.** For full details, please read the Chinese section above.
> You can ask AI to translate the Chinese section if needed.

## Summary

**screenshot-to-prompt** — Screenshot understanding + page structure extraction + implementation prompt generator.

### Core Purpose
Input a page screenshot → Output structured recognition results + a ready-to-use implementation prompt for coding agents.

### Key Pipeline
Screenshot Understanding → Page Structure Extraction → State Recognition → Prompt Generation

### Three UI Strategies
| Strategy | When to Use | Key Requirement |
|----------|-------------|-----------------|
| A: Skeleton Mode | No design, build structure first | Simple styles, basic interactions, refine later |
| B: Free UI Design | No design, optimization allowed | Modern, unified, production-ready |
| C: Design Restoration | Figma provided, high fidelity required | Match layout/spacing, reuse design system |

### Responsive Breakpoint Handling (NEW)
Screenshots are usually a single (desktop-width) viewport. Assess narrow-viewport adaptation and state it in the output: which blocks need responsive treatment, reuse the project's existing responsive facilities (UI library grid, breakpoint variables), and never silently assume a single device.

### UI Library Mapping (NEW)
When the project's UI library is known, map recognized generic components to library component names (e.g. select -> el-select / AntD Select) so the generated prompt is directly actionable. Keep generic names when mapping is uncertain.

### Screenshot Complexity Assessment
Before workflow execution, assess complexity to adjust output depth:
- **Simple** (single component like login form): Merge steps 1-2, skip steps 3-5, simplify output
- **Medium** (multi-component page like list with filters): Steps 1-5 normal, 6-8 simplified
- **Complex** (full page with modals/drawers/dashboard): All 8 steps, full output

### Edge Case Handling
- No screenshot → Ask user, never fabricate
- Unclear screenshot → Mark uncertain areas, recognize what's visible
- Contradictory requirements → Point out conflict, ask for clarification
- Vision model unavailable → Inform user, offer text-based alternative
- Analysis failure → Output partial results, mark unrecognized areas

### Reasonable Inference Boundaries
**Max 1 level of nesting** — only infer direct properties/states from visible elements, never chain inferences.

✅ Allowed (1 level): Button style → "likely a submit button"
❌ Not allowed (2 levels): Button style → "this is the registration entry in the login flow"

| Allowed | NOT Allowed |
|---------|-------------|
| Infer basic state transitions | Fabricate complex business rules |
| Infer basic form validation | Add complete new modules |
| Infer list selection behavior | Define non-existent API logic |
| Infer block priority | Expand page beyond screenshot |
| Infer basic linkage | Define system types |

### Key Constraints
- Do NOT fabricate text not visible in screenshot
- Do NOT expand business context beyond what's shown
- Output = Structure Recognition + Prompt (two parts)
- Prompt must be directly copyable and implementation-oriented
