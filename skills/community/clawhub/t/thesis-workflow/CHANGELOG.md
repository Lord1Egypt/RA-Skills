# CHANGELOG - MBA/学术论文多Agent协作工作流

所有重要更新都会记录在此文件。

## [v2.0.0] - 2026-06-23

### 🎉 大版本升级

v2.0.0 是 outline-anchored 分支的全面合并版，整合了 Step 9-12 的全部能力增强。

### ⚠️ 重大变更（破坏性）

**从 v1.7.3 升级到 v2.0.0 是破坏性升级，请仔细阅读迁移指南。**

#### 1. Phase 1.3 强制流程

v1.7.3 中用户可以直接调用 `confirm_phase1` 进入 Phase 2，开题报告归因是可选的。
v2.0.0 拍板强制：Phase 1.3 必须上传 docx 或粘贴目录文本，确认归因后才能进 Phase 2。

**迁移代码**（旧调用 → 新调用）：
```python
# v1.7.3 旧代码（跳过 Phase 1.3）
orchestrate(paper, action="phase1_confirm")  # → phase2
orchestrate(paper, phase="phase2", ...)

# v2.0.0 新代码（必走 Phase 1.3）
orchestrate(paper, action="phase1_1_init", input_type="docx", input_data=docx_path)
orchestrate(paper, action="phase1_confirm")
orchestrate(paper, action="phase1_3_submit")
orchestrate(paper, action="phase1_3_confirm")
orchestrate(paper, phase="phase2", ...)
```

#### 2. outline_state 结构变化

v2.0.0 中每个 L1 章节末尾自动插入虚拟节点 `__ch{N}_summary__`，节点总数 = 原节点 + L1 章节数。
`state["outline"]["outline_tree"]["metadata"]` 新增 `virtual_nodes` 和 `real_nodes` 字段。
节点字段新增 `content_hint`（开题报告提取或用户手写）。

#### 3. orchestrate_state 结构变化

新增 5 个 phase1_3_* 字段：
```json
{
  "phase1_3_status": "pending|submitted|confirmed|skipped",
  "phase1_3_docx_path": null,
  "phase1_3_result": null,
  "phase1_3_submitted_at": null,
  "phase1_3_confirmed_at": null
}
```

#### 4. generate_bridge 三级降级链

v1.7.3 仅支持 P1（前序节点）和 P2（父节点）。
v2.0.0 新增 P3（上一章节虚拟摘要）作为 fallback。

#### 5. 写作前信息检查

v1.7.3 节点写作时仅依赖前置节点的 key_conclusion。
v2.0.0 引入 `check_info_scarcity()`：content_hint / user_hints / bridge 任一为空 → 返回 `action="needs_user_input"`，Orchestrator 必须处理 3 决策路径。

### 新增能力

- **Step 9** — 跨父节点 Bridge：章节摘要节点 + P3 fallback，跨章节首节点自动引用上一章节摘要
- **Step 10** — 写作前信息检查：3 项信息源 + 标准 A + 3 决策路径（用户补充 / AI 自行生成 / 跳过）
- **Step 11** — Orchestrator Phase 1.3 集成：Phase 1.1 docx/text 解析入口 + Phase 1.3 归因状态机
- **Step 12** — 全链路集成测试：3 个端到端测试覆盖全部组件协同

### 代码变更总览

**新增函数**：
- `outline_parser.py`：`insert_chapter_summary_nodes()` / `get_chapter_summary_id()` / `get_chapter_id_from_summary()` / `save_content_hints_to_outline()`
- `orchestrator_v2.py`：`orchestrate_phase1_1()` / `orchestrate_phase1_3()` / `confirm_phase1_3()` / `update_node_content_hint()` / `skip_phase1_3()` / `check_info_scarcity()` / `apply_user_decision()` / `is_last_child_of_chapter()` / `synthesize_chapter_summary()`
- `state_manager_v2.py`：`_get_prev_chapter_summary()`
- `context_builder.py`：`_build_bridge_from_chapter_summary()`

**修改函数**：
- `orchestrator_v2.py`：`init_orchestrate_state()` 新增 phase1_3 字段；`confirm_phase1()` 不再直接进 phase2；`orchestrate_phase2()` 强制检查 phase1_3；`orchestrate()` 入口新增 6 个 actions
- `state_manager_v2.py`：`outline_update_status()` 新增 content_hint 字段
- `context_builder.py`：`generate_bridge()` 三级降级链；`build_prompt_package()` 集成 content_hint
- `write_single_node()` Step 1.5（写作前信息检查）+ Step 4.5（章节摘要触发）

### 测试覆盖

总测试数：**72 个**，全部通过 ✅

| 模块 | 测试数 |
|------|--------|
| outline_parser | 6 |
| context_builder | 7 |
| node_writer | 全部 |
| orchestrator | 14 |
| reviewer | 全部 |
| Step 9 增强项1（章节摘要） | 14 |
| Step 10 增强项4（信息检查） | 8 |
| Step 11 Phase 1.3 集成 | 16 |
| Step 12 全链路集成 | 3 |
| 其他既有测试 | 4 |

### 设计文档

新增 `references/chapter-summary-design.md`（178 行）：增强项1 完整设计说明。

### 本地 commit 总状态（feature/outline-anchored 分支）

```
af66161 feat(step12): full workflow integration test + finalize outline-anchored
69342ce feat(step11): Orchestrator Phase 1.3 integration (proposal attribution)
e79f343 feat(step10): enhancement 4 — pre-writing info check + content_hint pipeline
c2adf09 feat(step9): enhancement 1 — cross-parent bridge via chapter summary nodes
```

按 MEMORY 规则：不 push 不 publish，等龙哥确认后再推送到 GitHub + ClawHub。

---

## [v1.7.7] - 2026-06-23

### Step 12 — 全流程测试 + 提交（outline-anchored 分支完成）

**目的**：验证 Step 1-11 全部组件跨 Phase 端到端协同工作，为后续 push + publish 做准备。

### 新增

- **`scripts/tests/test_full_workflow.py`**（3 个集成测试）：
  - 测试 A：完整 docx 流程（Phase 1.1 → 1.2 → 1.3 → 用户调整 → 1.3 确认 → 章节摘要合成）
  - 测试 B：失败回退流程（解析失败 3 次 → 重试成功 → Phase 2）
  - 测试 C：增强项1 + 增强项4 + Step 11 协同（章节摘要 + bridge 跨章节）

### 修订

- **`scripts/state_manager_v2.py`**：`_get_prev_chapter_summary()` 触发条件从「level == 2」改为「prev_sibling_id == None」（章节首节点）。修复了 L3 首节点无法触发跨章节 bridge P3 fallback 的问题。

### 测试总览

总测试数：**72 个**（25 + 20 + 8 + 16 + 3），全部通过 ✅

| 模块 | 测试数 |
|------|--------|
| outline_parser | 6 |
| context_builder | 全部 |
| node_writer | 全部 |
| orchestrator | 14 |
| reviewer | 全部 |
| **Step 9 增强项1（章节摘要）** | 14 |
| **Step 10 增强项4（信息检查）** | 8 |
| **Step 11 Phase 1.3 集成** | 16 |
| **Step 12 全链路集成** | 3 |

### 本地分支总状态（feature/outline-anchored）

```
69342ce feat(step11): Orchestrator Phase 1.3 integration (proposal attribution)
e79f343 feat(step10): enhancement 4 — pre-writing info check + content_hint pipeline
c2adf09 feat(step9): enhancement 1 — cross-parent bridge via chapter summary nodes
```

按 MEMORY 规则：不 push 不 publish，等龙哥确认后再推送到 GitHub + ClawHub。

## [v1.7.6] - 2026-06-23

### Step 11 — Orchestrator Phase 1.3 集成（开题报告归因子阶段）

**问题**：原 Phase 1 流程只走「目录确认」直接进 Phase 2，**跳过开题报告归因**，导致 Phase 2 第一次写作时所有节点 `content_hint` 为空 → 触发增强项4「写作前信息检查」全节点暂停。

**拍板决策**（龙哥 2026-06-23 确认）：
- 强制 A：Phase 1.3 必走才能进 Phase 2（不允许跳过生产路径）
- 方案 B：枚举字段 `phase1_3_status = "pending|submitted|confirmed|skipped"`
- 时机 A：submit 时一次性写入 state（持久化）
- 允许用户手动覆盖 content_hint
- 细粒度：返回每个节点的归因详情（content_hint + matched_paragraphs + matched_count）

### 代码变更

- **`orchestrator_v2.py`**：
  - `init_orchestrate_state()`：新增 5 个 phase1_3_* 字段
  - `confirm_phase1()`：修改后不直接进 phase2，保持 phase="phase1"，phase1_3_status="pending"
  - `orchestrate_phase1_3(docx_path, llm_func)`：提交开题报告做归因，调用 extract_proposal_content + extract_content_hints + save_content_hints_to_outline，返回细粒度 node_details
  - `update_node_content_hint(node_id, new_hint)`：用户手动调整 content_hint，标记 user_modified
  - `confirm_phase1_3()`：状态机 submitted → confirmed → phase="phase2"
  - `skip_phase1_3()`：保留跳过代码路径（拍板 #1 禁用，仅未来扩展）
  - `orchestrate_phase2()`：强制检查 phase1_3_status == "confirmed"
  - `orchestrate()` 入口：新增 5 个 Phase 1.3 actions（submit / update_hint / confirm / skip）

- **`scripts/tests/test_orchestrator.py`**：
  - 更新 test_confirm_phase1：现在 phase="phase1" + phase1_3_status="pending"（Step 11 拍板）
  - 更新 TestReviewDecision.setUp：调用 skip_phase1_3 进入 phase2（保留原有评审测试路径）

### 测试覆盖（10 个测试用例）

- `test_phase1_3.py`：
  - init phase1_3 字段默认（1）
  - confirm_phase1 不进 phase2（1）
  - 未确认时拒绝 / docx 不存在拒绝（2）
  - submit 状态机转换（1）
  - 细粒度 node_details 返回（1）
  - 用户修改 content_hint（1）
  - confirm_phase1_3 状态机（1）
  - Phase 2 强制检查（1）
  - 端到端集成（1）

总测试数：25 (v1.7.3) + 20 (v1.7.4) + 8 (v1.7.5) + **10 (v1.7.6) = 63 个**

## [v1.7.5] - 2026-06-23

### 增强项4 — 写作前信息检查（content_hint 接入 + 信息贫瘠检查）

**问题**：节点写作前如果完全没有外部信息（content_hint 空 + 用户 hints 空 + bridge 三级全空），NodeWriter 拿到 prompt 后缺乏上下文，LLM 自由发挥质量差。

**拍板决策**（龙哥 2026-06-23 确认）：
- 判断标准 A：content_hint + user_hints + bridge **任一为空** → needs_user_input
- 3 个选项全保留：用户提供 hint / AI 自行生成 / 跳过节点
- Phase 1 完成时一次性写入 state（持久化）
- 允许用户手动覆盖 content_hint

### 代码变更

- **`outline_parser.py`**：
  - `save_content_hints_to_outline(paper, hints)`：提取的 content_hint 写入 outline_state，跳过特殊 key 和不存在节点
- **`state_manager_v2.py`**：
  - `outline_update_status()` 新增 `content_hint` 字段透传参数
- **`context_builder.py`**：
  - `build_prompt_package()` 新增 `content_hint` 字段
  - `build_prompt_package_text()` 新增 `## 开题报告方向参考` section
- **`orchestrator_v2.py`**：
  - `check_info_scarcity(paper, node_id)`：3 项数据源检查 + 标准 A 判断
  - `apply_user_decision(paper, node_id, decision, user_hint)`：3 个决策路径处理
  - `write_single_node()` Step 1.5：写作前信息检查，需要时返回 `action="needs_user_input"`

### 测试覆盖（8 个测试用例）

- `test_info_scarcity.py`：
  - save_content_hints 基本写入 + 跳过特殊 key
  - 3 项全空 → needs_user_input
  - 部分缺失 → needs_user_input（标准 A）
  - 3 项齐备 → proceed
  - 决策 1/2/3 三个路径
  - 完整端到端闭环

总测试数：25 (v1.7.3) + 20 (v1.7.4) + **8 (v1.7.5) = 53 个**

## [v1.7.4] - 2026-06-23

### 增强项1 — 跨父节点 Bridge（章节摘要节点）

**问题**：`2.1` 找不到 `1.2` 的 `key_conclusion`，bridge 断裂 → NodeWriter 拿不到承接段。

**方案 C**：在每个 L1 章节末尾插入虚拟章节摘要节点 `__ch{N}_summary__`，吸收本章所有 L2/L3 子节点的 `key_conclusion`，为下一章节 bridge 提供承接依据。

### 代码变更

- **`outline_parser.py`**（新增 3 函数）：
  - `insert_chapter_summary_nodes(outline)`：在每个 L1 章节末尾插入虚拟节点（幂等）
  - `get_chapter_summary_id(chapter_id)`：`ch1` → `__ch1_summary__`
  - `get_chapter_id_from_summary(summary_id)`：`__ch1_summary__` → `ch1`
- **`orchestrator_v2.py`**（新增 3 函数 + 修改 1 函数）：
  - `is_last_child_of_chapter(paper, node_id)`：判断节点是否是所属章节最后一个完成的子节点
  - `synthesize_chapter_summary(paper, chapter_id, llm_func, user_input=None)`：LLM 合成 200-300 字章节摘要，写入虚拟节点
  - `_build_summary_prompt(chapter_title, child_conclusions, user_input)`：合成 prompt
  - `write_single_node()` Step 4.5：节点完成回调中自动检测并触发章节摘要合成
- **`context_builder.py`**（新增 1 函数 + 修改 1 函数）：
  - `_build_bridge_from_chapter_summary(prev_chapter_summary, current)`：P3 fallback 跨章节桥接
  - `generate_bridge()`：新增 P3 优先级（P1 prev → P2 parent → P3 prev_chapter_summary）
- **`state_manager_v2.py`**（新增 1 函数 + 修改 1 函数）：
  - `_get_prev_chapter_summary(node, nodes, node_map)`：查上一章节虚拟摘要
  - `outline_get_context()`：自动附加 `prev_chapter_summary` 字段

### 测试覆盖（20 个测试用例）

- `test_chapter_summary.py`：单/多章节插入、L3 纳入 synthesizes、幂等性、边界、辅助函数（6 个）
- `test_synthesize_summary.py`：last_child 检测、LLM 路径、用户输入路径、LLM 失败 ask_user、空子节点、超长截断（6 个）
- `test_bridge_p3_fallback.py`：P1/P2 优先级、P3 跨章节桥接、不可用降级、首章节、context 自动附加（6 个）
- `test_integration_chapter_summary.py`：happy path + LLM 失败 fallback 端到端（2 个）

### 拍板决策（龙哥 2026-06-23 确认）

1. ✅ 方案 C（虚拟摘要节点）
2. ✅ 200-300 字够了
3. ✅ **LLM 失败时询问用户**（不是简单拼接）
4. ✅ 章节摘要不参与 Phase 3 评审（仅作内部辅助 bridge）
5. ✅ 在 `references/` 增加设计文档

## [v1.7.3] - 2026-06-19

### P0 修复

- **分页逻辑修正**：每章标题前分页（原为标题后分页导致空页），首章跳过
- **审核报告匹配增强**：改用 glob 通配匹配 + 结构化评分字段优先，不再依赖 emoji 硬编码
- **Verification Loop 真实校验**：新增字体/字号/行距/三线表边框/加粗残留/参考文献分编 6 项 Word 格式实质检查
- **空壳校验填补**：`check_table_format` 和 `check_table_caption_position` 从永远 `return True` 改为真实列数一致性和表标题位置检测
- **文件名泛化**：`*report*.md` 收窄为中文 `*报告*.md` + 大小写补充，`_find_review_report` Level 3 加论文关键词过滤
- **`_check_report_passed` 优先级重排**：综合评级 → 结构化评分 → emoji 回退，🔴 阈值从 5 放宽到 8
- **`_copy_proposal_cover` 锚点式匹配**：从硬编码"研究背景与研究问题"改为多锚点正则（第X章/1./研究背景/摘要等）
- **去重格式校验**：`md2docx_strict.py` 移除 `validate_md_format()`，统一由 `loop_self_check.py` 负责
- **硬编码参数化**：`min_lines`/`min_citations` 改为常量配置
- **代码风格统一**：8 个内部函数统一下划线 `_` 前缀

### Loop 架构落地

- **新增 `scripts/orchestrator.py`**：决策引擎 + 审核 Loop 自动重审 + Phase 完成自动校验
- **增强 `scripts/state_manager.py`**：新增 `parse_p0_from_report`、`set_hil_pause`、`clear_hil_pause`、`next_phase_name` 等 6 个方法
- **新增 `scripts/tests/`**：25 个单元测试覆盖 state_manager/loop_self_check/md2docx_strict
- **SKILL.md 精简**：1142 行 → 253 行（-78%），新增 Orchestrator 生命周期管理与 HIL 节点表

### 依赖变更

- `install.sh`：`pip install` → `python3 -m pip install --user python-docx`

## [v1.7] - 2026-06-17

### Loop Agent 架构（新增）

- **Orchestrator Loop**：每 Phase 完成后自动判断下一步，取代手动 trigger 模式
- **Phase 内部自检 Loop**：Observe → Think → Act → Verify 四步循环
- **审核 Loop**：Phase 3.5 → 修订 → 自动重审 → 连续 2 轮无新 P0 → 通过
- **Guardrails 校验**：10 项自动化规范检查（章节完整性/字数/引用/三线表/加粗等）
- **Verification Loop**：Word 输出后自动校验格式
- **Human-in-the-loop 检查点**：4 个强制人工确认节点

### 新增文件

- `scripts/loop_self_check.py`：Guardrails 自动化校验脚本（10 项校验 + JSON 输出）
- `references/checklist.md`：学术规范人工对照清单
- `references/loop-design.md`：Loop 设计原理说明文档

### 规则型 vs 审核型分工

- 脚本已覆盖的规范（字体/行距/标题层级/三线表），Agent 不再重复检查
- Agent 专注于脚本无法处理的事项（摘要字数/逻辑链/数据可信度/学术创新性）

---

## [v1.6] - 2026-06-02

### 新增功能

- **Phase 5.1 可选去AI味**：新增 HumanizerAgent，调用 humanize-chinese skill 执行学术风格降重，支持 CLI 脚本批量处理 + 差异报告
- **Phase 5.2 Word生成**：拆分独立步骤，支持生成两份Word（原版 + 润色后版）
- **前置检测机制**：去AI味前自动检测 humanize-chinese skill 是否安装，未安装则提示用户确认后自动安装
- **Phase 2 执行前检查表**：每次启动 Phase 2 前强制确认，包括 Phase 1 七项清单、章节×版本对照表、完成判定标准
- **章节×版本对照表**：枚举每个章节的 Executor（版本O）和 Hermes（版本H）要求，明确「必须」spawn，不可遗漏
- **Phase 2 强制检索要求**：新增5项强制检索检查项（PESTEL分析前/五力模型前/战略理论前/引用来源/检索记录≥3次），不满足则打回补充
- **Phase 2 完成判定标准**：版本O文件6个+版本H文件4个全部存在，ls验证，缺一则禁止进入 Phase 2.5
- **正文目录章节禁止规则**：写作规范新增，明确禁止在正文章节内自建「目录」章节
- **md2docx_strict.py 审核报告模糊匹配**：支持 `审核报告*.md` 命名规范模糊匹配（Level 1精确/Level 2模糊/Level 3候选列表）

### 移除功能

- **移除邮件发送流程**：Phase 5.2 改为仅生成Word并告知存储位置（`~/.openclaw/workspace/`）
- **移除联系方式必填**：Phase 1 确认清单去掉联系方式（微信/飞书ID）要求，去AI味后由用户自行取用文件
- **删除 Phase 5.5 成果发送**：整节移除，减少不必要的流程节点

### 架构升级

- **Agent 角色体系重构**：Orchestrator（调度）/ Executor（H-generator执行）/ Reviewer（规则型审核）/ DeepReviewer（学术深度评审）/ Integrator（整合方案）/ WordAgent（Word输出）/ HumanizerAgent（去AI味）七类专职分离
- **Agent 设计原则**：职责单一化，调度者不执行，执行者不调度；职责边界清晰
- **Phase 3.5 固定节点**：Phase 3 完成即触发，不得跳过，作为固定流程节点
- **Phase 3.5 分级标准**：P0（致命）/ P1（严重）/ P2（建议），审核报告结构化分级

### 修复问题

- **Phase 2 章节遗漏问题**：通过章节×版本对照表强制要求每个 ✅ 都是独立 spawn，防止核心章节（3/4/5/6）遗漏版本O或版本H
- **正文目录章节问题**：新增写作规范禁止正文内自建目录章节

---

## [v1.5] - 2026-06-01

### 新增功能

- **md2docx_strict.py 合规脚本**：严格按MBA论文格式规范转换（分页符/三线表/加粗过滤/标题层级/行距/中英文字体）
- **Phase 5 Word输出流程**：Review Agent终审 → 格式自检 → md2docx_strict.py → 发送，三步缺一不可

### 修复问题

- **Word格式问题**：分页符、标题层级、行距、加粗过滤、中英文参考文献格式
- **审核报告命名规范**：统一为 `审核报告_{论文题目}_Phase{N}_{版本}.md`

---

## [v1.0] - 2026-05-31

### 首次发布

- 多Agent协作工作流（Phase 1-5）
- 双版本起草机制（版本H + 版本O）
- Phase 3 审核（7个维度）
- Phase 4 整合方案
- md2docx 脚本（基础版）
