---
name: quant-research-lab
description: "量化策略研发实验室 — 让 Claude 按顶级机构角色分工（高盛策略架构师、文艺复兴回测引擎、Two Sigma 风控、Citadel Alpha 研究、Jane Street 做市、AQR 因子模型...共 15 个角色）系统性地设计、验证、风控、执行量化交易策略。当用户要求设计量化策略、做回测、构建因子、风控建模、策略优化、执行算法设计时触发。用户可能提到：量化策略、回测、因子、alpha 信号、风控、仓位管理、做市、统计套利、配对交易、宏观交易、TWAP、VWAP、投资组合优化、交易系统架构。"
---

# quant-research-lab — 量化策略研发实验室

## 角色注册表

| ID | 角色 | 机构 | 文件 | depends_on | complexity | Phase |
|:---|:---|:---|:---|:---|:---|:---|
| 01 | 策略架构师 | Goldman Sachs | roles/01-gs-strategy-architect.md | - | high | 1 |
| 02 | 回测引擎 | Renaissance Technologies | roles/02-rentec-backtest-engine.md | 01 | normal | 1 |
| 03 | 风控经理 | Two Sigma | roles/03-twosigma-risk-manager.md | 01 | normal | 1 |
| 04 | Alpha 研究员 | Citadel | roles/04-citadel-alpha-researcher.md | - | high | 1 |
| 05 | 做市引擎 | Jane Street | roles/05-js-market-maker.md | 01 | normal | 3 |
| 06 | 因子模型 | AQR | roles/06-aqr-factor-builder.md | 02 | normal | 2 |
| 07 | 统计套利 | D.E. Shaw | roles/07-deshaw-stat-arb.md | 01 | normal | 2 |
| 08 | 宏观策略 | Bridgewater | roles/08-bridgewater-macro.md | 01 | normal | 3 |
| 09 | 数据管道 | Bloomberg | roles/09-bbg-data-pipeline.md | - | normal | 2 |
| 10 | 执行算法 | Virtu | roles/10-virtu-execution.md | 01 | normal | 1 |
| 11 | ML 研究员 | Point72 | roles/11-point72-ml-researcher.md | 01 | high | 3 |
| 12 | 组合优化 | Man Group | roles/12-man-portfolio-optimizer.md | 01,02,03,06 | normal | 2 |
| 13 | 交易系统 | Millennium | roles/13-millennium-trading-system.md | 10,12 | normal | 2 |
| 14 | 因子回测 | Dimensional | roles/14-dimensional-factor-backtest.md | 01 | normal | 3 |
| 15 | 合规框架 | Goldman Sachs | roles/15-gs-compliance.md | 13 | normal | 3 |

## 使用方式

### 触发 Skill

**自然语言**（推荐）：直接描述量化需求，Skill 自动激活。例如：
- "帮我设计一个费率套利策略"
- "做一下这个策略的回测"
- "优化入场信号"
- "启动量化流水线"

**显式加载**：`/quant-research-lab`

### 操作指令（Skill 加载后使用自然语言）

| 你说 | 行为 |
|:---|:---|
| "启动流水线" / "pipeline" / "跑全流程" | 展示轨道选择菜单，用户选择后启动对应 Pipeline |
| "因子流水线" / "因子挖掘" / "执行流水线" / "宏观流水线" / "套利流水线" / "ML流水线" / "做市流水线" | 直接启动指定轨道 Pipeline |
| "全量流水线" / "完整流水线" | 启动全部 15 角色完整流程 |
| "从角色 03 恢复" / "继续流水线" | 从角色 NN 断点恢复（需 state 文件存在） |
| "从角色 02 重新执行" / "重跑风控" | 丢弃 NN 及之后输出，从 NN 重新开始 |
| "用高盛角色" / "做回测" / "风控分析" / "alpha 研究" / "执行算法" | 单独触发某个角色（Toolbox 模式） |
| "结合上次结果做回测" | 单独触发 + 注入最近完成角色的上下文 |
| "流水线进度" / "status" | 查看进度 |
| "重置流水线" / "reset" | 清空状态重新开始 |

## 编排逻辑

### Step 0: 收集上下文

当 Skill 被激活时（通过自然语言触发或 `/quant-research-lab` 显式加载）：

1. **读取角色注册表**获取可用角色列表（从本文档 `## 角色注册表` 表格中解析 ID、角色名、文件名、depends_on、complexity、Phase）
2. **检查 `state/research-context.md` 是否存在**：
   - **不存在** → 新建，写入初始模板（含 YAML frontmatter 和空角色输出区）
   - **存在且 `status: in-progress`** → 提示用户可从断点恢复：`检测到未完成的 Pipeline（{pipeline_id}），已完成角色：{completed_roles}。说"从角色 {next_recovery} 恢复"即可继续。`
3. **如果是新 Pipeline，向用户确认 3 个必填项**：
   - 交易市场/标的（`{user_market}`）
   - 可用资金规模（`{user_capital}`）
   - 当前最想解决的问题（`{user_focus}`）
   将答案填入 state 文件的 `## 项目上下文` 区

### Toolbox 模式：触发单个角色

触发方式：用户说"用高盛角色"、"做回测"、"风控分析"、"alpha 研究"、"执行算法"等，或按角色名/关键词匹配

1. **匹配角色**：在注册表中按角色名称（如"回测"）或文件名（如"backtest"）模糊匹配，找到对应的 ID、文件路径和 depends_on
2. **加载模板**：Read `roles/{NN}-{role}.md`，获取角色的完整 prompt 模板
3. **收集上下文**：
   - 如 state 文件无项目上下文 → 向用户询问 `{user_market}`, `{user_capital}`, `{user_focus}`
   - 如用户说"结合上次结果"或提到需要前面角色的上下文 → 从 state 文件提取最近完成角色的关键参数层和推理摘要层作为 `{upstream_params}` 和 `{upstream_summary}`
   - 如 `depends_on` 字段非空 → 从 state 文件中提取依赖角色的输出，注入为 `{upstream_params}` 和 `{upstream_summary}`
   - 如项目存在 `CLAUDE.md` → 提取架构约定注入 `{project_architecture}`
4. **替换占位符**：将收集到的值替换模板中的 `{user_market}`, `{user_capital}`, `{user_focus}`, `{upstream_params}`, `{upstream_summary}`, `{project_architecture}`
5. **Dispatch subagent**：使用 Agent tool，`subagent_type: "general-purpose"`，`model: "sonnet"`（注册表中 `complexity: high` 的角色使用 `model: "opus"`），注入替换后的完整 prompt
6. **质量门检查**：subagent 完成后，解析输出中的 `[QAGATE]...[/QAGATE]` 块（见下方"质量门检查"）。有异常 → 追加标记（`[输出不完整]`, `[数值异常]` 等），必要时提示用户决定（重做 / 接受 / 手动修复）
7. **写入 state 文件**：按格式追加角色输出到 `state/research-context.md`：
   ```
   <!-- ROLE_OUTPUT_START:{NN} -->
   ### {NN} {角色名} ✅
   [subagent 输出内容]
   <!-- ROLE_OUTPUT_END:{NN} -->
   ```
   更新 frontmatter：`current_role_id`, `completed_roles`, `next_recovery`
8. **展示摘要**：向用户展示 1-2 行摘要 + 质量标记
9. **提示下一步**：扫描注册表中 `depends_on` 包含当前角色 ID 且 Phase 已实现的角色，提示：`下一步建议：用"{next_role}"角色，或说"从角色 {next_NN} 启动流水线"`

### Pipeline 模式：启动场景流水线

Pipeline 是 Toolbox 的序列化封装，**按预设轨道（Track）**串行调用角色，而非跑全部 15 个。每个角色的执行复用 Toolbox 步骤 2-7（加载模板 → 收集上下文 → 替换占位符 → dispatch subagent → 质量门 → 写入 state）。

**触发方式**：用户说"启动流水线"、"pipeline"、"跑全流程"，或指定轨道名如"因子流水线"、"执行流水线"。也支持"从角色 NN 恢复"、"从角色 NN 重新执行"。

#### Pipeline 轨道定义

15 个角色构成了一个有向无环图（DAG），而非一条线。不同策略场景走不同的角色序列：

| 轨道名称 | 触发关键词 | 角色序列 | 预估耗时 | 适用场景 |
|:---|:---|:---|:---|:---|
| **核心流水线**（默认） | "启动流水线" / "pipeline" | 01→02→03→04→10 | ~15min | 标准策略：设计→回测→风控→Alpha→执行 |
| 因子流水线 | "因子流水线" / "因子挖掘" | 01→02→06→14→12 | ~20min | 因子研究：构建→回测→因子验证→组合 |
| 执行流水线 | "执行流水线" / "交易系统" | 01→10→13→15 | ~18min | 系统落地：执行算法→交易系统→合规 |
| 宏观流水线 | "宏观流水线" / "宏观策略" | 01→08→03→12 | ~18min | 宏观策略+风控+组合配置 |
| 统计套利流水线 | "套利流水线" | 01→07→02→10 | ~18min | 配对交易/协整策略 |
| ML 流水线 | "ML流水线" / "机器学习" | 01→11→02→03 | ~18min | ML 驱动策略研发 |
| 做市流水线 | "做市流水线" | 01→05→10→13 | ~18min | 做市系统设计 |
| 全量流水线 | "全量" / "完整流水线" | 01→02→03→04→06→07→08→09→10→11→12→13→14→15 | ~40min | 端到端完整流程（慎用，建议分轨道跑） |

> **轨道设计原则**：每个轨道以 01（策略架构师）为根节点，按依赖拓扑序串联。独立角色（09 数据管道）可按需单独 Toolbox 触发。用户也可以自定义轨道："走 01→04→11 的流水线"——编排层按指定 ID 列表执行即可。

#### 串行调度流程

1. **选择轨道**：
   - 用户说"启动流水线" / "pipeline" 未指定轨道 → 展示轨道选择菜单：`请选择流水线轨道：1)核心流水线(默认) 2)因子 3)执行 4)宏观 5)套利 6)ML 7)做市 8)全量。直接说编号或轨道名即可。`
   - 用户指定了轨道关键词（如"因子流水线"）→ 匹配对应轨道
   - 用户说"全量" → 走全量流水线轨道
   - 用户自定义序列（如"走 01→04→11"）→ 解析 ID 列表作为自定义轨道
2. **确定起始角色**：
   - 用户说"从角色 NN 恢复" → 从所选轨道中 state 文件的 `current_role_id` 开始（断点恢复逻辑见下方）
   - 用户说"从角色 NN 重新执行" → 先丢弃 NN 及之后角色的输出（见下方"重新执行逻辑"），再从 NN 开始
   - 默认 → 从轨道的第一个角色开始
3. **生成执行序列**：从起始角色到轨道末尾，序列生成后向用户展示：`轨道: {track_name}。执行序列: [01, 02, 03, 04, 10]（共 5 个角色）。预计 {estimate} 分钟。确认开始？`
4. **逐角色串行执行**：对序列中每个角色：
   a. 检查 state 文件是否已有该角色输出（搜索 `ROLE_OUTPUT_START:{$id}` 标记）→ 有则跳过
   b. 执行 Toolbox 步骤 2-7（加载模板 → 收集上下文 → 替换占位符 → dispatch subagent → 质量门检查 → 写入 state）
   c. 上下文自动注入：当前角色完成后，提取 QAGATE 中的 `downstream_fields` 和 `core_conclusion` 注入下一个角色
   d. 展示摘要 + 进度：`[{i}/{total}] {id} {角色名} 完成 [QAGATE: PASS|WARN ...]`
   e. **用户中断处理**：用户可随时说"暂停"。完成当前角色后写入 state，更新 frontmatter（含 `pipeline_track`），展示恢复命令
5. **全部完成后**：设置 frontmatter `status: complete`。提示：`轨道 {track_name} 完成（{total}/{total}）。如需落地为生产代码，说"实现这个"。也可继续其他轨道，如"因子流水线"。`

#### 断点恢复（"从角色 NN 恢复"）

1. 读取 state 文件的 YAML frontmatter，提取 `pipeline_track` 轨道名
2. 验证 NN 属于当前轨道且 `ROLE_OUTPUT_START:NN` 标记存在
3. 如不包含：提示 `角色 {NN} 不在当前轨道 {pipeline_track} 中或无输出记录。`
4. 确定下一个待执行角色：当前轨道中 ID 序列里排在 NN 之后的第一个角色
5. 更新 frontmatter，从该角色继续执行

#### 重新执行（"从角色 NN 重新执行"）

1. 计算丢弃集合：`D = {NN} ∪ {当前轨道中排在 NN 之后的所有角色 ID}`
2. 对 D 中每个角色 ID，在 state 文件中删除 `<!-- ROLE_OUTPUT_START:{$id} -->` 至 `<!-- ROLE_OUTPUT_END:{$id} -->` 块
3. 从 frontmatter 的 `completed_roles` 中移除 D 中的 ID
4. 展示丢弃摘要并确认，从 NN 重新开始

#### Pipeline 中的质量门集成

Pipeline 模式下每个角色完成后，自动复用 `### 质量门检查` 中的检查流程：

1. 搜索 subagent 输出中的 `[QAGATE]...[/QAGATE]` 块
2. 执行 3 项检查（必填字段 / 数值合理性 / 双重签名）
3. 检查结果追加标记到角色输出块的末尾：`[QAGATE 结果: PASS|WARN ...]`
4. 展示给用户时包含标记：`[{i}/{total}] {id} {角色名} 完成 [QAGATE: PASS]`
5. **异常处理**：如标记含 WARN 或 FAIL：
   - 默认自动继续到下一个角色，但在输出中标注异常
   - 如用户说"严格模式"或触发时加 `--strict` → 遇到 WARN/FAIL 时暂停，提示用户选择：`质量门警告 [{角色名}]: {标记列表}。选择: (C)ontinue 忽略继续 / (R)etry 重新执行当前角色 / (A)bort 中断 Pipeline`
   - 用户未回应时默认选择 (C)ontinue

### 质量门检查

每个角色 subagent 完成后，编排层从 `[QAGATE]...[/QAGATE]` 块提取数据进行以下检查：

| 检查项 | 适用 | 检查方式 | 不通过时 |
|:---|:---|:---|:---|
| 必填字段 | 全部 | `[QAGATE]` 块存在 + 自由文本含核心结论/关键参数/传给下游的字段 | 标记 `[输出不完整]` |
| 数值合理性 | 数值角色 | 默认模式：Sharpe < 50, MaxDD > -99% | 标记 `[数值极端异常]` |
| 双重签名 | 数值角色 | method_signature 和 data_signature 均非空 | 标记 `[缺少签名]` |

**检查流程**：

1. 在 subagent 输出中搜索文本 `[QAGATE]` 和 `[/QAGATE]`（字面字符串匹配，非 markdown 解析）
2. 缺失 `[QAGATE]` 块 → 标记 `[缺少QAGATE]`，跳过后续检查
3. 提取 QAGATE 块内字段（按 `key: value` 或 YAML 格式解析）：
   - `core_conclusion` / `核心结论` — 自由文本字段，非空即通过
   - `key_params` / `关键参数` — 含关键参数列表即通过
   - `downstream_fields` / `传给下游` — 含下游字段即通过
   - `method_signature` — 方法签名，数值角色必须非空
   - `data_signature` — 数据签名，数值角色必须非空
4. 数值合理性仅在角色标签含"回测/风控/因子/优化"时检查
5. 检查结果追加到 subagent 输出末尾，展示给用户：`[QAGATE 结果: PASS | WARN 输出不完整]`

### 状态管理

**`state/research-context.md`** 是 Pipeline 的单一真相源。格式：

```yaml
---
pipeline_id: {project}-{date}
pipeline_track: "{track_name}"
status: in-progress | complete
current_role_id: "{NN}"
completed_roles: ["01", "02"]
next_recovery: "{next_role_id in track}"
created_at: {ISO 8601}
project: {basename}
---
```

**Toolbox 模式下的行为**：
- 仅追加已完成角色的输出块（`ROLE_OUTPUT_START/END` 分隔），不修改 `status`
- 更新 `current_role_id` 为最近完成的角色 ID
- 更新 `completed_roles` 追加当前角色 ID
- 更新 `next_recovery` 指向下一个 `depends_on` 包含当前角色 ID 的角色
- 当所有 Phase 1-3 注册表角色完成时，设置 `status: complete`

**初始模板**（新 Pipeline 时创建）：

```
---
pipeline_id: {project}-{date}
pipeline_track: "{track_name}"
status: in-progress
current_role_id: ""
completed_roles: []
next_recovery: ""
created_at: {now}
project: {project_basename}
---

## 项目上下文
- **交易市场/标的**：{user_market}
- **可用资金规模**：{user_capital}
- **当前核心问题**：{user_focus}

## 角色输出
<!-- 每个角色完成后由编排层追加 -->
```

**Pipeline 模式下的行为**：见上方 `### Pipeline 模式`。

### 查看进度（用户说"进度" / "status"）

1. 检查 `state/research-context.md` 是否存在
2. 如 state 文件不存在或 `status: ready` → 提示：`尚无活跃 Pipeline。说"启动流水线"开始新 Pipeline。`
3. 如 state 文件存在：
   - 读取 YAML frontmatter，提取 `pipeline_id`, `pipeline_track`, `status`, `current_role_id`, `completed_roles`, `next_recovery`, `project`
   - 展示进度摘要：
     ```
     ## Pipeline: {pipeline_id}
     - 轨道: {pipeline_track}
     - 状态: {status}
     - 项目: {project}
     - 已完成角色 ({len(completed_roles)}): {completed_roles}
     - 当前角色: {current_role_id}
     ```
   - 如 `status: in-progress`，追加恢复提示：`恢复命令：说"从角色 {next_recovery} 恢复"`
   - 如 `status: complete`，追加：`轨道 {pipeline_track} 已完成。可继续其他轨道，如"因子流水线"。`

### 重置（用户说"重置" / "reset"）

1. 检查 `state/research-context.md` 是否存在 → 不存在则提示：`尚无活跃 Pipeline，无需重置。`
2. 如 state 文件存在，向用户确认：`确认重置 Pipeline "{pipeline_id}"？这将清除所有角色输出。输入 yes 确认。`
3. 用户确认 `yes` 后：
   - **保留上下文模式**（默认）：将 state 文件重置为初始模板，保留 `## 项目上下文` 中的用户提供的信息（`{user_market}`, `{user_capital}`, `{user_focus}`），清空 `## 角色输出` 区所有 `ROLE_OUTPUT_START/END` 块，重置 frontmatter 为初始状态（`status: ready`, `current_role_id: ""`, `completed_roles: []`, `next_recovery: ""`）
   - **完全清除模式**（用户说"硬重置"）：直接删除 state 文件，下次触发时自动创建全新模板
4. 重置完成后提示：`Pipeline 已重置。说"启动流水线"重新开始。`

## 实现状态
- Phase 1: ✅ 已实现（01, 02, 03, 04, 10）
- Phase 2: ✅ 已实现（06, 07, 09, 12, 13）
- Phase 3: ✅ 已实现（05, 08, 11, 14, 15）
