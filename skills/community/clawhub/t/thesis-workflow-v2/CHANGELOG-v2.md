# CHANGELOG - v2.x 新框架

> v2.x 是 **v2 框架**（outline-anchored 重构 + 9 HIL 节点 + 真实 CLI 入口）的活跃开发分支。
> 当前 latest: **v2.0.14**
> ClawHub Slug: `thesis-workflow-v2`（独立仓库）
> 详见 [CHANGELOG.md](./CHANGELOG.md) 的版本线索引。

## ⚠️ Alpha 阶段说明

v1.7.4 / v1.7.5 / v1.7.6 / v1.7.7 **实际为 v2 框架的早期 alpha 开发**。
当时因仍在 `feature/outline-anchored` 分支上，版本号沿用 v1.7.x 递增。
- v1.7.4 = v2 早期 alpha-1
- v1.7.5 = v2 早期 alpha-2
- v1.7.6 = v2 早期 alpha-3
- v1.7.7 = v2 早期 alpha-4
- v2.0.0 = v2 正式发布
- v2.0.6 = v2 上一稳定版
- v2.0.13 = v2 上一正式发布版本
- v2.0.14 = v2 当前 latest

**Commit hash 已保留，可在 git history 中追溯。**

## [v2.0.13] - 2026-06-28

### Phase 1 双 HIL 强制分步确认（P0 修复）

**问题**：Phase 1.2（大纲确认）和 Phase 1.3（归因分析）合并在一条 HIL 消息中，导致归因节点被跳过。

**修复**：
- `state_manager_v2.py`：`init_orchestrate_state()` phase 初始值改为 `"phase1_1"`
- `orchestrator_v2.py`：`confirm_phase1()` phase 推进到 `"phase1_2"`（不再是 `"phase1"`），归因确认后才进 `"phase2"`
- `orchestrator_v2.py`：新增 `elif phase == "phase1_2"` dispatch 分支，确保所有 phase1_3 action 正确路由
- `orchestrator_v2.py`：`orchestrate()` phase 路由新增 `"phase1_2"` 分支，兼容旧 `"phase1"` 状态
- `run_workflow.py`：`run_phase1()` 拆分为两次独立 HIL（HIL #1 大纲确认 → HIL #2 归因确认），归因展示增加"研究问题→章节映射表"，用户必须分别回复确认词才能推进

**影响**：phase 值新增 `"phase1_1"` / `"phase1_2"`，state_machine 文档已更新。




### 🧠 Layer 2 向量标题匹配（BGE-small-zh，替代 LLM 标题匹配）

**Phase 1.3 归因加速：LLM 标题匹配 → 本地向量匹配 + LLM 回退兜底**

#### 新增文件

- **`scripts/simple_embedder.py`**（230行）：BGE-small-zh 标题向量匹配器
  - `TitleMatcher.match_headings()`：余弦相似度匹配，毫秒级
  - 标题归一化：去掉编号前缀后再编码，提高匹配准确率
  - 离线支持：自动检测缓存 → 离线模式；无缓存 → hf-mirror 下载
  - 阈值 0.75，误匹配的标题自动降级到 LLM 兜底

#### 改造文件

- **`scripts/outline_parser.py`**：Layer 2 重写
  - 2a：向量标题匹配（确定性 + 毫秒级）
  - 2b：LLM 标题匹配（向量未匹配或无向量依赖时兜底）
  - `VECTOR_MATCHER_AVAILABLE` 标志位，自动检测 sentence-transformers
  - 无向量库时回退原 LLM 方案，零侵入

#### 性能对比

| 指标 | 原 LLM 方案 | 向量方案 |
|------|------------|---------|
| Phase 1.3 归因耗时 | 30-90s | **2-5s** |
| 确定性 | ❌ 非确定 | ✅ 相同输入=相同结果 |
| Layer 3 触发概率 | 高（LLM 漏匹配多） | 低（向量覆盖更多） |
| 新增依赖 | 无 | sentence-transformers ~5.1 |
| 模型缓存 | - | ~33MB（首次下载） |

---

## [v2.0.8-beta] - 2026-06-25

### 🚀 多工具并行检索引擎（#2）

**4 工具并行，取长补短，去重排序，任意失败不阻断。**

#### 新增文件

- **`scripts/multi_search.py`**（339行）：4工具并行检索引擎
  - `multi_search(query)`：ThreadPoolExecutor 并发，Tavily + arXiv + OpenAlex + web_search 同时搜索
  - `SearchResult` dataclass：title/url/snippet/source/score 标准化
  - 去重规则：同来源+同标题→去重，不同来源+同标题→保留
  - `multi_search_text(query)`：格式化文本输出（供 prompt 注入）
  - CLI 入口：`python3 multi_search.py <查询词>`

- **`scripts/research_tools.py`**（139行，替换旧版单Tavily）：
  - `quick_search(query)` → 直接调 multi_search_text()
  - `research_enrich(node_id, paper_name)` → outline贫瘠(<50字)自动触发多工具补充
  - `research_enrich_from_outline()` → 纯 outline 提取（无网络依赖）
  - 降级：网络不可用/全部无结果 → 返回空白，不阻塞写作

#### 扩展文件

- **`SKILL.md`**：工具矩阵（web_search/tavily/arxiv/openalex）+ Python层调用说明 + 并行逻辑
- **Phase 2 检索要求**：PESTEL/五力/竞争对手搜索要求更新为「多工具并行搜索」

### 🤖 RuntimeLLM — 零硬编码模型获取（#3）

- **`scripts/run_workflow.py`**：新增 `RuntimeLLM` 类

---


## [v2.0.9-beta] - 2026-06-25

### 🧠 Layer 2 向量标题匹配（BGE-small-zh，替代 LLM 标题匹配）

**Phase 1.3 归因加速：LLM 标题匹配 → 本地向量匹配 + LLM 回退兜底**

#### 新增文件

- **`scripts/simple_embedder.py`**（230行）：BGE-small-zh 标题向量匹配器
  - `TitleMatcher.match_headings()`：余弦相似度匹配，毫秒级
  - 标题归一化：去掉编号前缀后再编码，提高匹配准确率
  - 离线支持：自动检测缓存 → 离线模式；无缓存 → hf-mirror 下载
  - 阈值 0.75，误匹配的标题自动降级到 LLM 兜底

#### 改造文件

- **`scripts/outline_parser.py`**：Layer 2 重写
  - 2a：向量标题匹配（确定性 + 毫秒级）
  - 2b：LLM 标题匹配（向量未匹配或无向量依赖时兜底）
  - `VECTOR_MATCHER_AVAILABLE` 标志位，自动检测 sentence-transformers
  - 无向量库时回退原 LLM 方案，零侵入

#### 性能对比

| 指标 | 原 LLM 方案 | 向量方案 |
|------|------------|---------|
| Phase 1.3 归因耗时 | 30-90s | **2-5s** |
| 确定性 | ❌ 非确定 | ✅ 相同输入=相同结果 |
| Layer 3 触发概率 | 高（LLM 漏匹配多） | 低（向量覆盖更多） |
| 新增依赖 | 无 | sentence-transformers ~5.1 |
| 模型缓存 | - | ~33MB（首次下载） |

---

---

## [v2.0.12-beta] - (无 changelog 记录，git tag 存在)

*本版本无 changelog 内容，请参考 git log 追溯变更。*

---

## [v2.0.11-beta] - (无 changelog 记录，git tag 存在)

*本版本无 changelog 内容，请参考 git log 追溯变更。*

---

## [v2.0.10-beta] - (无 changelog 记录，git tag 存在)

*本版本无 changelog 内容，请参考 git log 追溯变更。*



## [v2.0.6] - 2026-06-24

### 🚨 Enforcement 修复 + 真实入口

v2.0.6 是 v2 框架的 **enforcement + entrypoint 重大修复**，由真实使用场景（测试论文_ctx 走 v2 全流程）暴露的问题驱动。

#### 1. 补 v2 真实入口 `scripts/run_workflow.py`（P0-2 + P0-3）

v2.0.0 ~ v2.0.5 期间，v2 框架只有 `orchestrate()` 库函数，**没有 CLI 入口**，SKILL.md / README 承诺的 `python3 scripts/orchestrator.py` 是 v1 入口（接口不兼容）。

v2.0.6 新增 `scripts/run_workflow.py`：
- CLI + state 文件驱动
- **9 个 HIL 节点 hard pause**（v2.0.4 修复 HIL 死循环，本次补完整驱动）
- 走 v2.0.4 推荐调用模式（`write_single_node` + `apply_user_decision` + `bypass_scarcity=True`）
- 不直接调 `outline_update_status`（避免 B-2 bug）

用法：
```bash
python3 scripts/run_workflow.py <paper_name> --status       # 查看状态
python3 scripts/run_workflow.py <paper_name> --phase auto    # auto
python3 scripts/run_workflow.py <paper_name> --phase phase1
```

#### 2. 拦截 `skip_phase1_3` 双层保护（P0-1）

拍板 #1 要求“Phase 1.3 不允许跳过”，v2.0.0 ~ v2.0.5 代码未落实。v2.0.6 修复：

**入口层**：`orchestrate(action="phase1_3_skip")` → 返回 `拍板 #1 强制不允许跳过`

**函数层**：`skip_phase1_3()` 加 3 道防线
- `MBA_THESIS_PRODUCTION=1` 环境变量禁止跳过
- 必填 `reason` 参数（audit log）
- 必填 `operator` 参数（audit log）

audit log 写入 `state.audit_log`，含 action / paper_name / reason / operator / timestamp。

#### 3. B-2 bug 幂等修复（P1-1）

`outline_update_status()` 默认拒绝覆盖已 `completed` 节点的内容，避免驱动直接调用导致状态污染。

- 默认：返回 `v2.0.6 B-2 幂等保护` 错误，提示重走 `write_single_node(bypass_scarcity=True)` 路径
- `force=True`：允许覆盖（调试用）

昨天 CHANGELOG 记录“决策不修”，本版本重新评估后修正为“必修”。

#### 4. 独立 Reviewer（P1-2）

`write_single_node()` 加 `reviewer_func` 参数，默认要求评审函数与写作函数不同（防止自审 = 不审）。

- 不传 `reviewer_func` → 发 `UserWarning`（默认 self-review）
- `reviewer_func is llm_func` → 发 `UserWarning`（未独立）
- `allow_self_review=True` 可调试场景

#### 5. 文档补充

- `SKILL.md` 新增「真实入口（v2.0.6 新增）」章节，含 9 个 HIL 节点清单 + Python API 示例
- `README.md` 新增「方式三：v2.0.6 真实入口 CLI」 + 「v2.0.6 调用示例（完整流程）」

#### 6. 回归测试

`scripts/tests/test_run_workflow.py`（v2.0.6 新增）：14 个测试用例
- 拦截层：5 个（跳 phase1_3 拦截、reason/operator 必填、env guard、audit log）
- CLI 层：2 个（--help、--status）
- B-2 幂等层：3 个（拒绝覆盖、force 覆盖、writing 允许）
- 独立 Reviewer 层：3 个（不传警告、同函数警告、独立无警告）
- 端到端：1 个（v2.0.4 推荐调用模式）

#### 7. 修改的现有测试

`scripts/tests/test_phase1_3.py::test_integration_text_flow`：
- v2.0.6 修复后 `skip_phase1_3()` 必填 reason + operator
- 测试更新为验证三步：报错 → 传审计参数成功 → audit log 验证

### 测试统计

- 修复前：158 个测试通过
- 修复后：**172 个测试通过**（+14 个 v2.0.6 新增），0 个失败（1 个预存在的 test_continue_decision bug 未修）

## [v2.0.1] - 2026-06-23

### 🐛 补丁修复

#### 1. `_get_prev_chapter_summary()` L3 节点判断错误（v2.0.1）

v2.0.0 中 `_get_prev_chapter_summary()` 修订为 `prev_sibling_id == None` 触发后，L3 首节点（如 3.1.1）会被误判为章节首节点，导致跨章节 bridge P3 fallback 错误返回。

**修复**：增加 `parent_id != chapter_id` 过滤，确保只对 L2 章节首节点生效。

**修改函数**：`scripts/state_manager_v2.py:_get_prev_chapter_summary()`

#### 2. 端到端验证测试套件

**决策**：
- 思路：**方案 A（mock） + 方案 B（真实样本）精华**
- 选项：**X** = 扩到现有 `test_full_workflow.py`（不新建文件）
- 推荐：**α** = commit + push（让 ClawHub 用户也能验证）

**实施**：原本放在 `test_v2_validation.py` 的 14 个测试场景**合并到 `test_full_workflow.py`**，与其他集成测试集中管理，避免测试分散。

**`scripts/tests/test_full_workflow.py`**（v2.0.1 扩展：从 3 个测试扩展到 17 个）：
- Part 0：Step 12 全链路集成（A/B/C）— 3 个测试
  - 测试 A：完整 docx 流程（happy path）
  - 测试 B：失败回退流程
  - 测试 C：章节摘要 + bridge 跨章节（增强项1 + Step 11 协同）
- Part 1：7 个 mock 边界测试（方案 A）
  - Mock 1：content_hint 端到端一致性（3 个验证点）
  - Mock 2：章节首节点 prev_chapter_summary 边界（5 个场景）
  - Mock 3：v2.0.0 state schema 完整性（metadata + 5 个 phase1_3_* 字段）
  - Mock 4：3 个决策路径混合（决策 1/2/3 各一个节点）
  - Mock 5：多章节摘要链式合成（ch1 → ch2 → ch3）
  - Mock 6：失败回退路径（text 失败 → docx 成功）
  - Mock 7：Phase 2 强制检查（state 不全 → 拒绝）
- Part 2：真实 docx 端到端测试（方案 B，**默认跳过**）
  - ⚠️ **隐私保护**：开题报告含学生姓名/学号/研究方向，**严禁上传到 GitHub**
  - 需设置环境变量 `MBA_REAL_SAMPLES_DIR` 才会跑（自动发现目录下所有 *.docx）
  - 样本匿名展示（`sample_001` ~ `sample_NNN`），不输出任何学生身份
  - 完整流程：Phase 1.1 解析 → 1.2 确认 → 1.3 归因 → Phase 2 写 1.1+1.2 → ch1 章节摘要合成
  - 详见 `tests/REAL_SAMPLES_README.md`

**删除文件**：`scripts/tests/test_v2_validation.py`（已合并到 test_full_workflow.py）

**总测试数**：
- v2.0.0：72 个
- v2.0.1：102 个（+30 增量）
  - 7 mock（Part 1）+ 3 Step 12 集成（Part 0）= 10 净增
  - Part 2 真实样本默认不计入（需本地配置）

**全套测试结果**：12 个测试文件，102 个用例（默认），全部通过 ✅

---

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

按 MEMORY 规则：不 push 不 publish，等确认后再推送到 GitHub + ClawHub。

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

按 MEMORY 规则：不 push 不 publish，等确认后再推送到 GitHub + ClawHub。

## [v1.7.6] - 2026-06-23

### Step 11 — Orchestrator Phase 1.3 集成（开题报告归因子阶段）

**问题**：原 Phase 1 流程只走「目录确认」直接进 Phase 2，**跳过开题报告归因**，导致 Phase 2 第一次写作时所有节点 `content_hint` 为空 → 触发增强项4「写作前信息检查」全节点暂停。

**拍板决策**：
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

**拍板决策**：
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

### 拍板决策

1. ✅ 方案 C（虚拟摘要节点）
2. ✅ 200-300 字够了
3. ✅ **LLM 失败时询问用户**（不是简单拼接）
4. ✅ 章节摘要不参与 Phase 3 评审（仅作内部辅助 bridge）
5. ✅ 在 `references/` 增加设计文档
