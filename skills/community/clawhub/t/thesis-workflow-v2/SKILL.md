---
name: thesis-workflow-v2
description: "Write, review, and export MBA / academic theses end-to-end as Word / DOCX. Covers outline planning → node-by-node writing → chapter review → academic deep review → Word export with GB/T 7714 references and 南大-style formatting. Triggers: 论文 / thesis / dissertation / 答辩 / 开题 / MBA / 章节 / 文献综述 / 参考文献 / chapter outline. ⚠️ v2 is beta (outline-anchored + 9 HIL + BGE multi-search); install independently and do not overwrite v1. Prefer v1 (`thesis-workflow`) for production unless user explicitly asks for v2 / 新框架 / outline-anchored / 9 HIL."
platforms: [linux, macos, windows]
metadata:
  # ↓ OpenClaw 私有配置（仅 ClawHub 加载器识别；不影响标准 platforms 字段）
  clawdbot:
    emoji: "📝"
    version: "2.1.2-beta.1"   # 单一真实来源，发布前必须先改这里。发布规则见 scripts/release.py
    requires: {}
    os: ["linux", "darwin", "win32"]
---

# MBA/学术论文多Agent协作工作流

> 完整文档见：`references/checklist.md`（学术规范清单）、`references/loop-design.md`（Loop 设计原理）

## 🔌 平台依赖（加载后必看）

本 skill **不是**通用 Hermes skill，专为 OpenClaw 设计。在调用本 skill 任何 Python 入口前，先确认平台依赖：

| 维度              | 依赖项                                                                 |
|-------------------|------------------------------------------------------------------------|
| **Agent 启动**    | `sessions_spawn`（OpenClaw 子 agent 机制）                            |
| **状态文件目录**  | `~/.openclaw/workspace/{paper_name}/`（**非** Hermes 标准路径）         |
| **工具后端**      | `web_search` / `tavily_search` / `arxiv_search`（OpenClaw MCP 工具链） |
| **CLI 入口**      | `python3 scripts/run_workflow.py {paper_name} --phase auto`           |
| **Python 路径**   | `PYTHONPATH=scripts python3 ...`（CLI 内部期望 scripts 在 path 上）    |

**反模式：** 不要把本 skill 当作标准 Hermes skill 调用——Hermes 的 file / search / web 工具链不能驱动 v2 的状态机和 HIL 拦截。如果你需要把论文流程迁回 Hermes，先做"状态层适配"（用 Hermes 的 workspace 概念替代 `~/.openclaw/workspace/`，并把 `sessions_spawn` 改成 Hermes 的子任务机制），再启用本 skill。

## ⚠️ 触发规则

当用户请求生成 Word 文档且满足以下任一条件时，**必须**调用本 skill 的 Word 输出流程，不得使用简单 md2docx 脚本：
- 输入文件路径匹配：`论文*.md`、`*thesis*.md`、`*dissertation*.md`
- 上下文中存在「论文」「MBA」「答辩」「开题」等关键词
- 用户明确要求导出 `.docx` 格式且文件性质为学术论文

**正确流程：** 写作语法预检 → Review Agent 终审（`scripts/loop_self_check.py` 校验通过）→ `scripts/md2docx_strict.py` 合规转换 → Word 输出

## ⚠️ v1 / v2 选择矩阵（加载后必看）

v2 仍处于 beta，**生产论文默认走 v1**。仅当用户明确要求时再切 v2：

| 场景 | 选择 | 触发依据 |
|------|------|---------|
| 用户说「稳一点 / 跑过答辩 / 已用 v1 / 默认」 | ✅ v1 (`thesis-workflow`) | 默认基线 |
| 论文已在 `~/.openclaw/workspace/{paper}/` 下运行 v1 | ❌ 切 v2 | 状态文件不兼容 |
| 用户说「用 v2 / 新框架 / outline-anchored / 9 HIL / BGE 多工具并行」 | ✅ 本 skill (v2) | 显式升级 |
| 用户未明示 + 新论文 | ⚠️ 走 v1 | 避开 beta 风险 |

**反模式：** 不要因为「本 skill 描述更新」就把现有 v1 论文切到 v2——v2 的 `_orchestrate_state.json` schema 与 v1 不兼容。

### v2 HIL 节点一览（确定用 v2 之后再读）

v2 在 9 个位置**强制 human-in-the-loop**：每到这些点状态机会 hard pause，必须用户确认才能推进。如果 agent 想绕过任何一项，v2.0.6 的拦截规则会拒绝（见 §v2.0.6 拦截规则）：

| #  | 触发位置                       | 检查内容                       | 决策                          |
|----|--------------------------------|--------------------------------|-------------------------------|
| 1  | Phase 1.1 后                  | 大纲结构 + 公司映射            | 接受(actual_name/跳过) / 修改 |
| 2  | Phase 1.3 后                  | 归因结果                       | 接受 / 调整 hint             |
| 3  | 在 `write_single_node()` 写入单节点前 | info_scarcity            | 提供 hint / AI 生成 / 跳过   |
| 4  | Phase 2 评审后                | quality=medium/low             | 接受 / 重写                  |
| 5  | Phase 2 完成后                | 章节内容预览                   | 通过 / 修改                  |
| 6  | Phase 3 整合后                | 整合版内容                     | 通过 / 修改反馈              |
| 7  | Phase 3.5 P0 修复             | 超 3 轮未收敛                  | 接受 / 继续修订              |
| 8  | Phase 4 整合方案              | 方案是否接受                   | 接受 / 修改                  |
| 9  | Phase 5.2 后                  | Word 输出                      | 导出 / 修改                  |

**HIL #1 公司映射（v2.1.2+）：** HIL #1 同时确认大纲 + 采集公司 `actual_name`：
- 输入 `[1] vivo` → 接受大纲，`actual_name="vivo"`
- 输入 `[2]` → 接受大纲，`skip_mapping=true`（仅适用于纯理论论文）
- 输入 `[3]` → 取消，不修改 state
- 不提供 actual_name 且不跳过 → `confirm_phase1()` 返回错误「公司映射未填写」

> **总计 9 HIL 节点**（公司映射合并入 #1，不新增节点）。

**反模式：** 不要给 agent 传 `allow_skip_hil=True` 或在 prompt 里写"自动通过所有 HIL"——HIL 是论文质量最后一道防线，绕过它的代价是错版交付给导师。

### v2.0.6 拦截规则（与 HIL 表配套必读）

如果 agent 想绕过 HIL 或绕过"独立评审"，v2.0.6 在 orchestrator 层有 3 类硬拦截：

| 拦截点 | 强制规则 | 失败场景 |
|--------|----------|----------|
| **拍板 #1 强制** | `phase1_3_skip` 不允许；`skip_phase1_3()` 需要 `MBA_THESIS_PRODUCTION=1` + 必填 `reason`/`operator` + audit log | 跳过 Phase 1.3 → 论文方向错位无人工把关，全文跑偏 |
| **B-2 幂等保护** | `outline_update_status()` 默认拒绝覆盖已 completed 节点 | 误重写已通过审核的节点 → 评审历史回滚，质量倒退 |
| **独立 Reviewer** | `write_single_node()` 默认要求 `reviewer_func ≠ llm_func` | 生成+评审用同一 LLM → 自我审核，"我写的都对"假阳性 |

**反模式：** 不要在 prompt 里"建议 agent 用 force=True 绕过"或"把 allow_skip_hil 设为 True"——v2.0.6 的拦截规则会拒绝并返回错误。绕过拦截的代价比"卡在 HIL 等用户确认"高得多。

## 核心架构

```
Phase 1（规划）→ Phase 2（逐节点写作）→ Phase 2.5（内容确认）
→ Phase 3（整合）→ Phase 3.5（学术深度评审）
→ Phase 4（修复）→ Phase 5（终审 + Word 输出）
```

⚠️ **阶段强制顺序：** 全部 Phase 必须按顺序执行，不得跳过。Phase 2.5（人工确认门槛）和 Phase 3.5（深度评审）是固定节点，不得跳过。

## Agent 设计原则

**每个 Agent 只做一件事。** Agent 间通过文件传递结果，不共享上下文。Orchestrator 专注调度，不执行执行性工作。

| Agent | 调用方式 | 主责 |
|-------|---------|------|
| **Orchestrator** | 当前 session | 调度 / 推进 / 决策 |
| **NodeWriter** | `sessions_spawn` | 逐节点内容生成 |
| **Reviewer** | `sessions_spawn` | Phase 3/5 规则型审核 |
| **DeepReviewer** | `sessions_spawn` | Phase 3.5 学术深度评审 |
| **Integrator** | `sessions_spawn` | Phase 4 整合方案 |
| **WordAgent** | `exec python3` | md2docx执行 + 格式校验 |

## 关键实现说明

### 公司信息处理

- 用真实公司名搜索公开数据，填入正文时替换为代号（A公司/B公司）
- 搜索 prompt 用真实名，输出 prompt 用代号
- 映射关系不进入最终文档

#### 公司映射状态字段（v2.1.2+）

```json
"company_info": {
  "code_name": "A公司",      // 从开题报告 docx 自动提取
  "actual_name": "vivo",     // HIL #1 由用户填入；空/null = 未填
  "skip_mapping": false,     // true = 显式跳过(纯理论论文)
  "confirmed": true,         // confirm_phase1() 校验通过
  "confirmed_at": "2026-07-02T..."
}
```

**强制校验：** `confirm_phase1()` 在 v2.1.2+ 会拒绝 `actual_name=None && skip_mapping=false` 的 state，必须二选一。

**使用场景：**
- Phase 2 数据检索：搜 `actual_name` 公开数据
- Phase 2 写作锚定：写文档时确保代换为 `code_name`
- Phase 5 输出前：脱敏校验，确认 `actual_name` 不在最终 Word 正文里

**安全约束：** 该字段**不会进入最终 Word 文档**，仅作为写作过程的内部状态。

### 检索同步规则

所有 Phase 调用数据查询工具（`web_search` / `academic-research`）时，必须：
1. 同步输出工具名称 + 查询条件 + 结果摘要（<50字）
2. Subagent 用 `sessions_send` 向主 session 发送同步
3. 大型检索完成后输出结构化结果摘要

### 数据查询工具（v2 多工具并行策略）

> **核心原则**：4个工具并行发出，取长补短，去重排序，任意失败不阻断。
> `web_search` 等内置工具 Agent 直接调用，无需经过 Python 层包装。

**工具矩阵：**

| 工具 | 来源 | 适用场景 |
|------|------|---------|
| `web_search` | OpenClaw 内置（头条搜索） | 行业数据、市场规模、新闻动态 |
| `tavily_search` | Tavily MCP（OpenClaw 走内置桥接；Hermes 走 mcporter） | 结构化摘要、权威来源 |
| `arxiv_search` | arXiv MCP（mcporter） | 前沿学术论文、技术细节 |
| `openalex_search` | scholar-search.py（OpenAlex） | 学术文献、引用分析 |

**Tavily MCP 检测（v2.1.2+）：** `_check_tavily_mcp()` 自动检测运行平台：
- **OpenClaw runtime**：通过 `openclaw skills list --json` 检测 `tavily-mcp` 是否注册，注册即通过
- **Hermes 兼容**：降级调 `mcporter call tavily-mcp.tavily_search`
- **其他**：报错

Tavily 在 v2.1.2+ 已改为 `install_category="none"`，pre-flight 不再卡 needs_ai_deps 流程。OpenClaw runtime 下 agent 可直接调用内置 `tavily-mcp__tavily_search` 工具。

**Python 层调用（`research_tools.py`）：**
```python
from research_tools import quick_search, research_enrich

# 快速检索（返回文本，供注入 prompt）
result = quick_search("竞争战略 市场规模 2024")

# 节点级检索（自动取 outline 中的 research_keywords）
ctx = research_enrich(node_id, paper_name)
```

**并行执行逻辑：**
1. 四工具同时发出，不串行等待
2. 各工具独立降级（超时/失败 → 静默忽略）
3. 结果按 URL 去重 + score 排序
4. 输出格式：`[来源] 标题\n  摘要\n  URL`

**Agent 视角：**
- Agent 可继续直接使用 `web_search(query=...)` 等内置工具
- `quick_search()` 是 Python 层的补充，用于学术/论文场景的结构化检索

## Phase 详解

### Phase 1：规划与定稿

**🔴 红线：** Phase 1.1 / 1.3 **禁止**直接调用 Python API，必须经 `run_workflow.py`（详见 §A.6）。直接 `import orchestrator_v2` 在 Phase 1 阶段会绕过用户 HIL 确认，论文签收前的方向错误会全白做。

通过问答输出确认清单，用户逐项确认后方可动笔。

**红色星标项（必填）：**
- ⭐ 实际公司名称（仅用于数据检索，正文以A公司/B公司呈现，不进入公开文档）
- ⭐ 大纲结构（7章大纲逐章确认）
- 论文基本信息（题目/作者/专业/学位类型/答辩年份）

→ 生成「写作任务书」用户签收后进入 Phase 2。

### Phase 2：逐节点写作

**前置检查：** Phase 1 必填项已确认

**🔴 红线：**
- ❌ 跳过 `run_workflow.py` 直接读写 `_orchestrate_state.json`（必须经 CLI 入口）→ 失败场景：CLI 内部维护"状态机锁 + phase 推进历史 + audit log"，直接读写会绕过锁，导致下一 Phase 跳号或死锁
- ❌ 手工修改状态文件的 `phase*_status` 字段（会破坏 Orchestrator Loop 的下一阶段判断）
- ❌ 长任务不汇报进度（必须按 25% / 50% / 75% / 100% 节点主动汇报，含 `completed_nodes` 数）→ 失败场景：Phase 2 写作耗时 20+ 分钟无汇报，用户以为 session 卡死会主动打断，导致已写 30 节点的章节全部丢失、状态半成品

Orchestrator 遍历 outline 树中的每个节点，调用 `write_single_node()` 逐个生成内容。
每个节点写作前通过 `context_builder.py` 构建 prompt 包，自动注入：
- 承接上文（auto bridge）
- 分析维度建议（规则推导）
- 开题报告方向参考（content_hint）
- 行业数据参考（quick_search 多工具检索）

**Phase 2 强制检索要求**（关键词中的 `{论文主题行业}` 由 Orchestrator 自动提取）：
- 第3章 PESTEL 分析前 → 多工具并行搜索「{论文主题行业} 市场规模/趋势/政策」
- 第3章 五力模型分析前 → 多工具并行搜索「{论文主题行业} 主要竞争对手/市场份额」
- 战略理论部分 → 多工具并行搜索「{论文主题行业} 竞争战略 应用」
- 每章至少 1 个引用标注来源，全文检索记录 ≥ 3 次
- **多工具并行检索**：调用 `quick_search()` 或 `research_enrich()`，结果自动去重排序

**状态文件机制：** `_orchestrate_state.json`（`scripts/state_manager_v2.py`）

→ 全部节点写完且字数达标后进入 Phase 2.5（内容确认）。

### Phase 3：整合

Reviewer 对整合版论文进行审核。审核维度：格式 / 大纲 / 内容准确性 / 查重风险 / 学术规范 / 写作语法。

### Phase 3.5：深度学术评审（固定节点）

DeepReviewer 对 Phase 3 报告进行二次审查，输出 P0/P1/P2 分级问题清单。P0 问题进入修订 → 重审闭环（见审核 Loop）。

### Phase 4：整合

Integrator 汇总 Phase 3 + Phase 3.5 全部评审结果，制定整合方案。核心原则：取长补短，不为统一而破坏内容质量。

**自动验证：** 整合版运行 `python3 scripts/loop_self_check.py` 校验，100%通过方可输出 Word。

### Phase 5：终审与输出

- Phase 5：Reviewer 终审
- Phase 5.1：[可选] `humanize-chinese` skill 去AI味
- Phase 5.2：**调用 `thesis-docx-export` skill**（Word 转换 + 10 项 Guardrails 校验）

## Orchestrator 生命周期管理

**🔴 红线：** Phase 1 / 5.x **必须**经 `run_workflow.py` 入口；Phase 2-4 才允许 `import orchestrator_v2` 直接调 Python API（且仅在已通过 run_workflow 进入论文状态之后）。
- ❌ 跳过 `run_workflow.py` 直接 `from orchestrator_v2 import orchestrate` → 失败场景：CLI 内部维护"状态机锁 + phase 推进历史 + audit log"，直接 import 绕过锁，导致下一 Phase 跳号或死锁
- ❌ Phase 1 任何子阶段（1.1 / 1.2 / 1.3）直接 import orchestrator_v2 调 `phase1_*` → 失败场景：绕过用户在 Phase 1.1 / 1.3 末尾的 HIL 签收，论文方向错位无人工把关
- ❌ 把 `force=True` / `allow_skip_hil=True` 作为 prompt 默认值 → 失败场景：v2.0.6 拦截规则会拒绝并抛错；agent 越权操作进退两难

### 真实入口（v2.0.6 新增）

> **执行脚本**：`scripts/run_workflow.py`（v2 真实入口 CLI）
> **状态文件**：`~/.openclaw/workspace/{paper_name}/_orchestrate_state.json`
> **设计原则**：驱动状态机 + 9 个 HIL 节点 hard pause

```bash
# 仅查看状态
python3 scripts/run_workflow.py <paper_name> --status

# auto 模式：根据 state 自动判断下一步
python3 scripts/run_workflow.py <paper_name> --phase auto

# 指定阶段
python3 scripts/run_workflow.py <paper_name> --phase phase1
python3 scripts/run_workflow.py <paper_name> --phase phase2  # 需 --llm
python3 scripts/run_workflow.py <paper_name> --phase phase3
```

### Python API（v2.0.9）

```python
import sys
sys.path.insert(0, "scripts")
from orchestrator_v2 import orchestrate, write_single_node, apply_user_decision

# Phase 1.1: 解析开题报告（docx 或文本）
r = orchestrate(paper_name, action="phase1_1_init",
                input_type="docx", input_data="path/to/proposal.docx")

# Phase 1.2: 确认大纲（用户 HIL）
r = orchestrate(paper_name, action="phase1_confirm")

# Phase 1.3: 提交开题报告归因
r = orchestrate(paper_name, action="phase1_3_submit",
                docx_path="path/to/proposal.docx", llm_func=my_llm)

# Phase 1.3: 确认归因（用户 HIL）
r = orchestrate(paper_name, action="phase1_3_confirm")

# Phase 2: 逐节点写作（v2.0.4 推荐调用模式）
for node_id in next_nodes:
    r = write_single_node(paper_name, node_id,
                          reviewer_func=my_reviewer)  # 独立评审，llm_func 内部从 session 获取

# Phase 3: 整合
r = orchestrate(paper_name, action="phase3_review")

# Phase 3.5: 深度学术评审（自动进入 Phase 3.5/4/5 链）
# Phase 3 → orchestrate_phase3_5() → P0修复 → Phase 4 → Phase 5
r = orchestrate(paper_name, phase="phase3", action="phase3_export")

# Phase 5: Word 输出提示
print(r.get("message", ""))
```

### HIL 节点（v2.0.6 完整 9 个）

> 9 个 HIL 节点的速查表已前移到 `## 核心架构` 之前（紧跟 v1/v2 选择矩阵后）。在 §"v2 HIL 节点一览"查看完整表。

### v2.0.6 拦截规则（enforcement）

> v2.0.6 拦截规则段（拍板 #1 / B-2 幂等 / 独立 Reviewer）已前移到 `## 核心架构` 之前（紧跟 9 个 HIL 节点表后）。在 §"v2.0.6 拦截规则"查看完整表。

### 审核 Loop 自动重审

Phase 3.5 完成 → orchestrator 解析 P0 计数 → 有 P0？→ 自动进入修订
→ 修订完成 → 自动回到 Phase 3.5 重审 → 连续 2 轮无新 P0 → 通过
→ 超过 3 轮 → HIL 暂停

### Phase 内部自检

每 Phase 完成后，orchestrator 自动运行 `loop_self_check.py` 校验：
```bash
python3 scripts/orchestrator.py 状态文件.json --validate
```
校验失败 → RETRY 打回 → Agent 修复 → 再次校验（最多 3 次）

## ⚠️ Loop 设计原则

5 个 Loop 元素的详细定义、终止条件、HIL 检查点对照、与 OpenClaw Agent Loop 的差异比较：详见 `references/loop-design.md`（302 行）。

**速记：** 每个 Loop 最多重试 3 次；Phase 1 / 2.5 / 4 / 5.2 末尾为强制 HIL 节点（必须用户确认才能推进）。

## Guardrails 校验（10 项）

```bash
python3 scripts/loop_self_check.py --file 论文_xxx.md   # 单文件
python3 scripts/loop_self_check.py --phase 2 --workspace ~/.openclaw/workspace/  # Phase 级别
python3 scripts/loop_self_check.py --file 论文_xxx.docx --verify-docx           # Word 校验
```

| # | 校验项 | 失败阻断 |
|---|--------|---------|
| 1 | 章节完整性（7章齐全） | Phase 2/4 |
| 2 | 字数门槛（每章≥100行） | Phase 2/4 |
| 3 | 参考文献存在 | Phase 4 |
| 4 | 无 `## 第X章` 混合格式 | Phase 2/4 |
| 5 | 无 `**正文加粗**` | Phase 2/4 |
| 6 | 引用完整性（逐章≥1处，全文≥10处） | Phase 2/4 |
| 7 | 三线表列数一致 | Phase 4 |
| 8 | 表标题在表上方 | Phase 4 |
| 9 | 无合并残留（`===END===`） | Phase 4 |
| 10 | 核心章节关键词（第5章战略/第6章实施） | Phase 2.5 |

## Word 输出

> **本段已外移。** Word 转换、加粗过滤、三线表、分页、Guardrails 10 项校验等所有 Word 相关细节，由独立 skill `thesis-docx-export` 承载。
>
> 调用入口和文档：
> - Skill：`thesis-docx-export/SKILL.md`
> - 18 项格式规范清单：`thesis-docx-export/references/checklist.md`
> - 10 项 Guardrails 校验：`thesis-docx-export/scripts/loop_self_check.py`（软链接 → `scripts/loop_self_check.py`）
>
> 主 skill 只在 Phase 5.2 阶段调用本 skill，不在 Phase 1-5 重复展开。

## 附录：脚本与文档结构

```
thesis-workflow/
├── SKILL.md                    ← 本文件（简版触发器 + 核心逻辑）
├── README.md / README_EN.md    ← 安装/使用说明
├── CHANGELOG.md                ← 版本日志
├── config.template             ← 配置模板
├── install.sh                  ← 安装脚本
├── .clawhubignore / .github/workflows/skill-publish.yml
├── scripts/
│   ├── md2docx_strict.py       ← Word 合规转换（真身在主 skill；docx-export 软链接共享）
│   ├── loop_self_check.py      ← Guardrails 自动化校验（10项）（真身在主 skill；docx-export 软链接共享）
│   ├── state_manager.py        ← 状态文件管理
│   └── tests/                  ← 单元测试
├── references/
│   ├── checklist.md            ← 软链接 → thesis-docx-export/references/checklist.md
│   ├── content-hint-fallback.md ← 附录 B 外移版（v7.0 跑题事故修复方案）
│   ├── chapter-summary-design.md ← 章节摘要节点设计
│   ├── git-workflow.md         ← 双版本发布策略
│   └── loop-design.md          ← Loop 设计原理说明
└── thesis-docx-export/         ← 独立 skill（Phase 5.2 Word 输出）
    ├── SKILL.md                ← docx-export 入口文档
    ├── README.md / CHANGELOG.md
    ├── scripts/                ← 软链接主 skill scripts/
    └── references/             ← checklist.md 真身在此
```

## 附录 A：论文项目运行 Checklist（agent 必遵守）

> **来源**：v7.0 事故复盘 → 运营者 22:19 反馈 / 2026-06-29  
> **适用对象**：跑 thesis-workflow-v2 的任何 agent（含 main session 和 isolated）  
> **生效日期**：2026-06-29 起

### A.1 触发即汇报

启动任何 thesis-workflow-v2 阶段前，先发一条汇报：
- 论文名 / 阶段 / 启动时间 / 监考路径（如有 PID/log）
- 5-30 字，简洁不啰嗦

### A.2 阶段切换必汇报

- Phase 1 → Phase 2（写作开始）
- Phase 2 → Phase 3（整合开始）
- Phase 3 → Phase 3.5（评审开始）
- Phase 3.5 → Phase 4 / Phase 5（终审/导出）

每切换发一条"已到 X 阶段"短汇报。

### A.3 长跑阶段主动节拍

Phase 2 写作阶段（如有 background 任务）：

| 进度节点 | 必汇报 |
|---------|--------|
| 启动 | ✅ |
| 完成 25% | ✅ |
| 完成 50% | ✅ |
| 完成 75% | ✅ |
| 完成 100% / 失败 | ✅ |

- 每次汇报含当前 `completed_nodes` 数量
- 用 `cat _orchestrate_state.json` 拿实时数据

### A.4 异常即停 + 主动汇报

触发任一异常情况，**立即**停下来汇报（不等用户问）：
- content_hint 覆盖率 < 50% → Phase 1.3 异常
- 大量节点 failed → Phase 2 失败
- 整合版字数异常（< 30k 或 > 200k）
- outline_state 节点结构与 _orchestrate_state 不一致

### A.5 完成必汇报（含产出清单）

论文交付时，必汇报：
- 终稿路径
- 字数（中文字数 / 总字符数）
- 章节完成情况
- 异常/缺陷（如有）
- 邮件/通知状态

### A.6 红线禁止（继承自 AGENTS.md）

- ❌ 跳过 run_workflow.py 操作状态文件
- ❌ 不汇报长任务进度
- ❌ Phase 1.3 / 1.1 直接调用 Python API
- ❌ 状态文件手工修改 phase*_status 字段

### A.7 辅助工具（可选）

如需手动查看状态，可用：
```bash
python3 ~/.openclaw/scripts/thesis_progress_reporter.py --idle-minutes 60
```

脚本全局通用，跨 macOS/Linux/Windows，纯 stdlib。idle 60min 自动静默。

## 附录 B（指针）：已批准改进方案 — content_hint fallback

历史事故与代码实现已外移到 `references/content-hint-fallback.md`（139 行）。当 `node.content_hint` 为空时，`scripts/context_builder.py` 会自动注入"大纲骨架 + 反面警示"以防 LLM 跑题。

如需查具体函数实现（`_extract_paper_subject` / `_build_outline_skeleton` / `_build_no_runoff_warning`）或验收标准，跳到 references 文件即可。

