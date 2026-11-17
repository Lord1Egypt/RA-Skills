---
name: se-semantic-graph
description: 软件工程语义图谱——把项目全知识域（客户画像/需求/成本/架构/分层/模块运行逻辑/历史决策）落进 axolotl 图库，修 bug/加功能/重构时沿跨域语义边定向查询精确上下文，根治上下文爆炸与注意力分散。触发词：项目语义图谱、修 bug 前查上下文、这段代码为什么存在、功能来源、为何这么设计、影响面查询。
description_zh: "软件工程语义图谱：图库定向查询项目语义上下文，根治上下文爆炸"
---

# 软件工程语义图谱（se-semantic-graph）

## 是什么

把经典软件工程的**全知识域**（不是只有需求）落进 axolotl 图库，节点带字段级摘要，跨域语义边连接。编程/调试/重构时，从任意入口（报错栈函数、模块、需求、决策）沿语义边**定向遍历**，只取与当前任务相关的上下文——替代"把整个项目塞进 prompt 硬扛"。

## 核心命题

编程中反复调试修改的根因，往往不是"不会写"，而是**上下文爆炸 + 注意力分散**：
修 bug 时看不到这段代码服务于什么需求、为什么存在、当初为什么这么设计。
写作用图库解决"长篇跨章一致性"，编程用图库解决"跨代码库的功能-需求-约束一致性"。
**同一个病，同一副药。**

## 依赖（前置安装）

底层 axolotl 图库需支持 `in_neighbors`（入边遍历）：

```bash
# axolotl (dev 分支) 需含 in_neighbors API：
# src/graph_db.rs / mmap_graph.rs / py_bindings.rs 三层都已补齐后构建：
cd <axolotl>/prototype-rust
maturin build --release --features python-bindings -o target/wheels
# 用有 axolotl_rs 的 venv python 安装 wheel
pip install --force-reinstall --no-deps target/wheels/axolotl_rs-*.whl
```

验证：`python -c "import axolotl_rs; print('in_neighbors' in dir(axolotl_rs.AxolotlGraph))"` → `True`

## 环境变量

| 变量 | 含义 | 默认 |
|---|---|---|
| `SE_SEMANTIC_DIR` | 图文件目录（**每个项目一个目录**） | `~/.workbuddy/se-semantic-graph` |
| `SE_SEMANTIC_ENGINE` | lobster-memory 引擎目录 | `~/.workbuddy/skills/lobster-memory` |

## 运行

```bash
PY=<lobster-memory venv python>   # 有 axolotl_rs 的那个
RUN=~/path/to/se-semantic-graph/runner.py
export SE_SEMANTIC_DIR=<项目自己的图目录>

$PY $RUN init                                  # 初始化项目图
$PY $RUN add --id <id> --label <名> --type <类型> --summary <一句话> --source <来源>
$PY $RUN connect --from <id> --to <id> --kind <边类型> [--note <说明>]
$PY $RUN trace --start <id> --direction up|down --depth 4 [--verbose]   # 核心
$PY $RUN list --type <类型>
$PY $RUN stats
$PY $RUN types                                 # 列出全部节点/边类型
```

## 四域节点类型

| 域 | 类型 | 说明 |
|---|---|---|
| 问题域 | `persona` 客户画像 | 谁在用、场景、痛点 |
| 问题域 | `requirement` 需求 | 功能/非功能、优先级、来源 |
| 问题域 | `cost` 成本约束 | 预算、时间线、ROI、为何不做更重的 |
| 问题域 | `business_rule` 业务规则 | 不可违背的领域约束 |
| 方案域 | `architecture` 架构层 | 分层架构中的一层（接入/业务/领域/设施） |
| 方案域 | `module` 模块 | 职责边界、归属层 |
| 方案域 | `interface` 接口契约 | 对外服务定义 |
| 方案域 | `tech_stack` 技术栈 | 选型 |
| 实现域 | `runtime_logic` 运行逻辑 | 状态机、关键路径 |
| 实现域 | `data_flow` 数据流 | 输入输出、流转 |
| 实现域 | `data_model` 数据模型 | 实体关系 |
| 实现域 | `function` 函数锚点 | 被反复改动的重点函数 |
| 决策域 | `decision` 历史决策 ADR | 为何这么写 |
| 决策域 | `rejected` 被否方案 | 被否的替代方案（往往更值钱） |

## 跨域语义边（⚠️ 方向约定，勿反）

**所有边统一方向 = 问题域 → 实现域**（from 在上游，to 在下游）：

```
画像 → 需求 → 架构层 → 模块 → 运行逻辑 → 函数
  ↑drives   ↑mapped_to ↑part_of ↑implements ↑traced_to
成本/规则 → 需求（constrains）
决策 → 任意（affects）   决策 → 被否方案（rejects）
```

- **修 bug 反向追溯（为什么做）** = 沿边反向 = `trace --direction up`（原生 in_neighbors）
- **加功能正向展开（影响什么）** = 沿边正向 = `trace --direction down`（原生 out_neighbors）

反了方向（如 serves 写成 模块→需求）会导致追溯断链——录入时严格照此约定。

## 对话驱动工作流（核心，勿跳步）

**本技能不只是查询工具，它定义项目怎么推进。** 四个阶段严格顺序，每阶段结束必须用户确认，确认后才能进下一阶段。跳步 = 用假设替代用户真实意图 = 上下文爆炸的另一种形式。

```
阶段一 画像对话  →  阶段二 需求对话  →  阶段三 架构评审  →  阶段四 开发+实时录入
（用户确认画像）    （用户确认需求）    （用户确认架构）      （边写边录，修 bug 时 trace）
```

### 阶段一：画像对话（必须主动问，不猜）
- **向用户提问，不自行假设**：谁在用？什么场景？什么痛点？什么算"玩得好"？
- 问题示例：目标用户是谁 / 核心体验是什么 / 一个"爽"时刻 / 一个"崩溃"时刻 / 平台与分发
- 用户回答后录入 `persona` 节点，**展示给用户确认**后才算完成
- 完整提问脚手架见 `templates/onboarding-dialogue.md`

### 阶段二：需求对话（基于画像，逐条确认）
- 基于已确认画像，把玩法拆成需求，**逐条问用户**：这个功能是必须(M)/想要(W)/不做(N)？
- 区分功能需求与非功能需求（性能/平台/发布）
- **⚠️ 按项目类型的维度清单覆盖所有"不可避免"的需求维度**，不能只讨论机制/逻辑：
  - 每个维度至少问一遍（哪怕答案是"本轮不做"也要确认，不能跳过）
  - 例（游戏项目）：玩法机制 / 画面视觉 / 音乐音效 / 操作方式 / 手感 / UI与UX / 性能 / 平台兼容 / 发布分发
  - 维度清单见 `templates/requirement-dimensions.md`（含多类项目：游戏/Web/CLI/库/服务）
- 每条需求录入 `requirement` 节点，连 `drives`（画像→需求）
- 需求清单**展示给用户确认**，确认后不再自行增删
- 提问脚手架见 `templates/onboarding-dialogue.md`

### 阶段三：架构评审（设计方案给用户看，不直接写码）
- 基于已确认需求，产出：分层架构 / 模块划分 / 关键流程（状态机）/ 数据流
- **把设计画出来/写清楚给用户评审**（图或文字均可），用户拍板后才落图
- 录入 `architecture` / `module` / `runtime_logic` 节点 + `mapped_to` / `part_of` / `implements` 边
- 用户对设计的修改意见，作为 `decision` 节点记录
- 评审呈现脚手架见 `templates/onboarding-dialogue.md`

### 阶段四：开发 + 实时录入（架构确认后）
- 按确认的架构写码；写码/调试中**顺手**录入/更新语义节点（低成本、贴近现场）
- 关键调试教训（如"为什么不能用信号"）→ `decision` 节点
- 修 bug 前必查：`trace --start <定位点> --direction up` 拿"为什么"链
- 加功能前必查：`trace --start <需求> --direction down` 看影响面

### 跳步惩罚（写进意识）
- 跳过阶段一二 = 画像是猜的、需求是编的 → 架构评审没依据 → 开发出来不是用户要的
- 跳过阶段三 = 代码结构由手顺决定而非设计 → 模块边界模糊 → 语义图谱的模块节点变虚
- 用户说"直接做"时，至少把阶段一二的问题快速问一遍再动手（哪怕一句话确认）

## 使用惯例

### 什么时候录入（按工作流阶段，不脱离流程）
- **阶段一二三**：用户确认画像/需求/架构后，立即录对应节点（不等到开发）
- **阶段四**：龙虾写码/改码时，顺手把接触到的需求/模块/逻辑/决策按模板 `add` + `connect`
- 架构级决策、需求变更，由用户确认后落图（高质量、可观察）
- 不要等"文档完备"才录——边写边录，图库是活的 traceability

### 什么时候查询（修 bug 前必查）
1. 拿到报错栈，定位到函数/模块
2. `trace --start <id> --direction up --depth 4` → 拿"为什么"链（需求/画像/成本/决策）
3. 需要看影响面时 `trace --direction down` 或交给 LSP 查调用关系
4. **只把查到的字段级摘要带进 prompt，不塞全项目**

### 查询只输出差异
图库价值 = 边定向遍历 + 字段级提取 + 只输出差异。**禁止全量 dump 图库给模型**（图库不是存储桶）。查询结果就是"与本次任务相关的上下文子图"。

## 字段规范

每个节点只存摘要级字段，不存全文/源码：
- `id`：稳定标识符（英文/拼音，无空格）
- `label`：可读名称
- `type`：节点类型
- `summary`：一句话摘要（≤200 字，字段级提取的关键）
- `detail_ref`：详细文档/源码位置引用（不存全文）
- `source`：来源（需求文档/issue/PR/会议/对话）

## 与 lobster-memory 的关系

- **底层共用** axolotl 图库（axolotl_rs），但不共用图文件——lobster-memory 记对话记忆（`~/.workbuddy/lobster-memory/memory.axeb`），本技能记**项目语义**（每个项目一个 `SE_SEMANTIC_DIR`）
- 语义边方向约定是本技能特有的：问题域→实现域，使 up/down 天然对应 in/out
