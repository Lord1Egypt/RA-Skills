## v4.12.3 — 2026-05-25

### 📊 逐TP数量追踪 + p6_merge补缺命令 + fix_hints fallback

**背景**：V4.12.2云端复盘，占位符检测生效（0条占位符✅），但每TP只生成1条（44TP→48条），P5预估110条。

**修复（4项）**：
1. _save_single_tp 数量累计+比对：多次save同一TP自动累计case，保存后比对expected_case_count，不足返回saved_shortfall状态+补缺提示
2. _build_single_tp_prompt 强化数量要求：prompt中明确「🔴 必须生成N条用例（不是1条！）」
3. p6_merge shortfall统计增强：返回逐TP补缺命令（含具体tp-index和--save命令）
4. _build_p7_fix_hints 通用fallback：fix_hints为空时自动生成基础修复指引（不再依赖模型生成）

**影响范围**：orchestrator.py _save_single_tp(~25行) + prompt(~5行) + p6_merge(~15行) + p7_fix_hints(~8行)

---

## v4.12.2 — 2026-05-25

### 🛡️ 三层防护：占位符检测 + 前置动作 + 门禁分级

**背景**：V4.12.1云端复盘发现Agent跳过11章节P6 prompt，用Python脚本批量注入模板占位符，103条中98条为占位符。

**修复（4项）**：
1. `paragraph_5.md` 新增前置动作章节（必须先读P6 prompt + P5数据 + 理解参数用法）
2. `_save_single_tp` 新增 `_check_placeholder_patterns` 占位符检测（关键词+空洞+相似度）
3. `p7_code_check` fix_hints增加tp_N→TP-(N+1)映射关系 + 修复后先merge再check提示
4. `export_excel.py` 门禁分级：用例数<50%预估→BLOCK, 50%-80%→WARNING不阻断

**影响范围**：paragraph_5.md(~25行) + orchestrator.py(~80行) + export_excel.py(~10行)

---

## v4.12.1 — 2026-05-25

### 🔧 _save_single_tp 19列补全 + LLM输出5核心字段

**背景**：V4.12.0云端首跑（task_20260525_113858），MiniMax LOW模型只输出title/steps/expected_results，p6_merge schema验证失败。根因是`_save_single_tp`单TP模式只补全7字段，batch模式已有的12字段补全未同步。

**修复（3项）**：
1. `_save_single_tp` 新增10字段自动补全（project/case_type/requirement/menu_path/creator/assignee/test_case_type/status/screenshot/test_suite），与batch模式一致
2. LLM输出从3核心字段扩展为5核心字段（新增menu_path/preconditions），prompt中增加生成要求第7/8条+格式示例同步更新
3. `is_smoke` 智能推断：P0+main_flow/branch/integration → True

**影响范围**：orchestrator.py `_save_single_tp`(~15行) + `_build_single_tp_prompt`(~5行)

---

## v4.12.0 — 2026-05-25

### 🏗️ P6 prompt信息密度翻倍 + P5 description丰富化

**背景**：V4.11.2 P6用例91条步骤100%相同，P7质量门禁全FAIL。根因是三层信息衰减：
- P5产出operations_chain/ui_elements/field_checklist等丰富数据
- p6_generate_one的_write_tp_contexts丢弃了这些字段（只传9个基础字段）
- _build_single_tp_prompt仅420B极简prompt，LLM无据可依→模板化输出

**修复（5项）**：

1. **`_write_tp_contexts` 补全7字段**（orchestrator.py）：
   - 新增 page_path/precondition/step_expected_pairs/ui_elements/field_checklist/operations_chain/adjacent_tps
   - 所有新增字段带兜底空值，兼容旧P5数据

2. **`_build_single_tp_prompt` 重写**（orchestrator.py）：
   - prompt从~420B扩充到~1500B，包含页面路径/操作链路/UI元素清单/涉及字段/前置条件
   - 6条生成要求：步骤≥15字、引用UI元素、禁止通用描述、期望可观测、步骤差异化
   - 相邻TP差异化提示（前2后2）

3. **LOW格式示例模糊词修复**（orchestrator.py）：
   - "系统提示操作成功" → "列表刷新显示查询结果\n列表数据中员工姓名字段与输入值一致"

4. **P5 description丰富化**（prompts/P5_test_point_merge.md）：
   - 新增"第四步半"指令：description必须包含入口+操作+验证目标（50-150字）
   - 新增质量门禁第6条（description≥30字）、第7条（operations_chain≥2）

5. **相邻TP差异化提示**（orchestrator.py）：
   - context增加adjacent_tps字段（前2后2个相邻TP的title+category）
   - prompt中展示相邻TP并要求步骤差异化

**影响范围**：orchestrator.py（3处修改，~80行）+ prompts/P5_test_point_merge.md（~30行）

**预期效果**：
- 步骤差异化率：0% → 60-80%
- 步骤含具体UI元素比例：0% → 70%+
- 模糊词命中率：100% → <20%

---

## v4.11.2 — 2026-05-24

### 🔧 argparse choices补全 + SKILL.md P6流程表修正 + 旧API引用清零

（维护版本）

---

## v4.10.2 — 2026-05-24

### 🔧 P6 LOW模型校验B降级 + 骨架差异化 + context可靠性标记

**背景**：V4.10.1云端P6重跑复盘发现，batch 1-19全部被hard_issues校验B("所有测试点步骤完全相同")拒绝。根因分析发现：
- `_build_step_expected_pairs()` 的兜底模板同category下所有TP返回相同骨架
- LOW模型的`operations_chain`常为空，命中兜底→所有TP骨架相同→LOW模型照搬→校验B拒绝
- 校验B是同文件3处降级逻辑中唯一遗漏的LOW降级点

**修复（3项，均在orchestrator.py内）**：
1. **校验B LOW降级**（~line 6585）：新增LOW模型判断，降级为stderr warning不阻断保存
2. **兜底骨架差异化**（~line 4918）：`_build_step_expected_pairs()` 兜底分支注入TP的title/id作为差异化关键词
3. **context可靠性标记**（~line 5574）：context.json增加`step_expected_pairs_source`字段（operations_chain/fallback_template）

**影响范围**：orchestrator.py（3处修改，共约40行）+ SKILL.md版本号

**测试验证**：
- 同category不同title的TP骨架已差异化 ✅
- operations_chain存在时走正常路径不受影响 ✅
- 所有category下骨架均可差异化 ✅

---

## v4.10.1 — 2026-05-23

### 🔧 P6自动修复 + case_id兜底 + 完整性校验

**背景**：V4.10.0云端复盘报告发现窄聚焦模式Agent不输出case_id→45个case全空→Agent被逼违规(改p5/伪造gate/直调export/spawn子Agent)。

**修复（5项）**：
1. **case_id双保险**：prompt强制输出case_id + p6_save_batch顺序兜底(数量不匹配→拒绝)
2. **P6自动修复**：p6_save_batch拒绝时追加fix_hints→Agent按指引修复→--merge保存(重试上限3次)
3. **完整性校验**：step7_export校验merge_log完整性 + batch用例数一致性(防止Agent篡改)
4. **restart清理**：重启P6时清理残留agent_output文件
5. **prep_prompt子Agent拦截**：V4.8.10已有，无需新增

**影响范围**：orchestrator.py(~120行新增) + prompts/P6_low_simple.md + paragraph_5.md

---

## v4.10.0 — 2026-05-23

### 🏗️ LOW模型窄聚焦模式 — 精简prompt + 3核心字段 + 代码补全

**背景**：MiniMax M2.7用V4.9.x架构跑P6，19批仅3批通过(16%)。根因是5-10KB引导卡让模型注意力耗尽——同时处理业务理解+19列格式+质量规范+禁止词清单，MiniMax无法稳定产出。

**架构变更**：
- LOW模型prep_prompt不再输出引导卡，改输出**精简prompt(~1KB)**
- Agent只需产出 **title/steps/expected_results** 3个核心字段
- 其余16列(含case_id/priority/is_smoke/source_test_point/p5_description等)由代码从骨架自动补全
- prompt结构：业务上下文(从P0/P1提取) → 测试点列表 → 1-2条示例(从P1 scenario提取) → 3条简要规则

**新增文件**：
- `prompts/P6_low_simple.md`：精简prompt模板(~500字节)
- `_build_skeleton_for_batch()`：最小骨架生成函数

**影响范围**：orchestrator.py prep_prompt LOW分支 + prompts/P6_low_simple.md + paragraph_5.md

**升级路径**：HIGH模型保持现有架构不变。prompts/P6_low_simple.md不存在时自动降级到旧引导卡模式。

---

## v4.9.4 — 2026-05-23

### 🔧 复盘22项全修复 — 终版

基于云端Agent复盘报告(task_20260523_163208)，22项问题中21项已修复：
- paragraph_5.md 全面修复：⏸️顺序/禁止脚本/context指引/质量门澄清/修复指引/p6_guide说明/核心约束合并/禁止重复
- orchestrator.py: total_batches→complexity_groups(消除Agent混淆)
- 其余：通道B强制exec/P1 operations_chain/P0自动降级/MEDIA双通道等

📋 V4.10.0规划：进度跟踪/批量执行机制

---

## v4.9.3 — 2026-05-23

### 🔧 通道B强制化 — 报告文件确保发送

**背景**：云端Agent仍然只输出MEDIA路径文字不发送文件。通道B写成了列表项文字描述（`- exec: cat ...`），Agent不把它当exec指令执行。

**修复**：
1. `rules/paragraph_3.md` 步骤②：通道B改为显式 `exec:` 代码块 + 违规警告
2. `rules/paragraph_6.md`：同步强化
3. `SKILL.md`：`__must_emit__` 说明增加 `exec cat` 要求

---

## v4.9.2 — 2026-05-23

### 🔧 P1 operations_chain 字段名修复 — 根除模板通用化

**根因**：P1 prompt 输出字段名为 `operations_steps`，但 P5 代码读取 `operations_chain` → 字段名不匹配 → 读不到数据 → P5 全用兜底模板"进入该功能页面，执行核心操作流程" → P6 Agent 基于空泛骨架 → 所有用例步骤雷同 → G5 步骤唯一性 < 50% 被拒绝。

**修复**：
1. `prompts/P1_feature_scenario.md`：字段名 `operations_steps` → `operations_chain`，增加 `target`/`value`/`page_path`/`precondition` 为必填
2. `orchestrator.py` P5 merge + P6 prep：兼容读取 `operations_chain or operations_steps`（双保险）

**预期效果**：P1 scenario 输出具体操作链 → P5 有材料生成差异化 steps → P6 Agent 基于具体操作写步骤 → 步骤唯一性 > 50%

**影响范围**：prompts/P1_feature_scenario.md + orchestrator.py（2处兼容读取）

---

## v4.9.1 — 2026-05-23

### 🔧 P7自动修复 — fix_hints + --tp-ids + Agent按指引局部修复

**背景**：P6 Gate通过但P7 Gate失败的场景（覆盖率77%+模糊表述+禁止模式），当前策略是restart_from P6全量重跑。已花30分钟产出的合格用例被废弃，重跑大概率仍同样问题。邵老板提出"P7给处方而非病危通知书"。

**代码层（orchestrator.py）**：
1. **_build_p7_fix_hints函数** — 基于P7检查结果生成4类修复指引：generate_missing(覆盖率)/fix_step_expected(C2)/fix_vague_expected(G2)/fix_forbidden(G4)
2. **_find_batch_for_case函数** — 带缓存的case_id→batch_index索引查找（一次构建，多次查询）
3. **--tp-ids参数** — prep_prompt --step P6新增，支持指定TP子集（逗号分隔），P7修复用
4. **缓存失效** — p6_merge/p6_save_batch后自动清除batch索引缓存
5. **batch_index=99** — 修复专用批次号，无skeleton自动走宽松模式

**流程层（rules/paragraph_6.md）**：
1. Step 1b重写为"读fix_hints→逐类修复→p6_merge→重跑P7"的自动流程
2. 修复策略：coverage≥50%→local_repair(2轮)，<30%→restart_p6(1次)，兜底→low_quality
3. 修复顺序：generate_missing→fix_step_expected→fix_vague→fix_forbidden
4. 强制执行：禁止抛选择题，全自动

**预期效果**：P7失败修复 30分钟(全量重跑) → **5-8分钟**(局部修复)，已合格用例100%保留

**影响范围**：tools/orchestrator.py(~170行新增) + rules/paragraph_6.md + SKILL.md版本号

**背景**：SKILL.md 1084行/53KB/~13K tokens，Agent因指令过长导致注意力稀释、规则被忽略、段落边界跳步。

**架构变更**：
- **SKILL.md**：1084行→168行（-84%），仅保留元规则+段落概览表+约束矩阵+流程路由
- **rules/paragraph_1~6.md**：6个独立段落规则文件，Agent进入段落时 `read` 按需加载
- 每个段落文件：头部含元规则提醒+V3.5.2禁止行为引用+前置依赖摘要；尾部含终止锚点

**评审吸收（小析+小猿双人评审 ⚠️→✅）**：
1. ✅ 段落文件末尾终止锚点（防止迷路）
2. ✅ 段落文件头部元规则提醒（防忘记总控约束）
3. ✅ V3.5.2禁止行为：总控完整+段落3/4/5各1行引用
4. ✅ 段落文件前置依赖摘要（防跨段信息断裂）
5. ✅ orchestrator.py零改动确认

**预期效果**：
- Agent每次只加载当前段落~100-240行（原一次性1084行）
- 段落间物理隔离：Agent看不到下一段内容，无法连段执行
- 总控+规则总内容不变（1095行 vs 1084行），但按需加载降低Token消耗

**影响范围**：
- `SKILL.md`：重写为总控路由
- `rules/paragraph_1~6.md`：新增6个段落规则文件
- `tools/orchestrator.py`：SKILL_VERSION→4.9.0 + P5 ui_elements修复(P1 scenario数据注入)

### 🔧 P5 ui_elements空数组修复

**背景**：P5合并后所有测试点的ui_elements均为空数组`{"buttons":[],"inputs":[],"selectors":[],"labels":[]}`，导致P6 Agent生成用例时无UI元素参考，只能脑补操作步骤。

**根因**：`_build_ui_elements`从测试点的`field_specs`和`operations_chain`提取UI元素，但P2生成的测试点只有`source_scenario`引用，没有这些字段。数据在P1的scenario中，但未传递到P5。

**修复**：
1. P5 code_merge新增P1 scenario查找表，按source_scenario匹配注入operations_chain/page_path/precondition
2. _build_ui_elements增加page_path兜底提取：当field_specs和operations_chain都为空时，从page_path（如"分润管理→员工配置"）和scenario name提取UI关键词填充到labels

---

## v4.8.15 — 2026-05-23

### 🔴 段落边界跳步修复 + P6中介者模式澄清 + ⏸️后死循环修复

**背景**：云端P6执行复盘报告(task_20260523_111241)揭示3个严重问题：
1. Agent从段落2一口气跳到段落6，仅用2次「继续」跨过3个段落边界
2. P6中Agent未按LLM prompt生成用例，而是提取metadata套模板，导致步骤唯一性20-45%、覆盖率仅47%
3. 段落3 ⏸️ 后存在quality_check残留区块，Agent读到后回头重跑→30+分钟死循环

**修复**：
1. **每次「继续」只前进一段** — 运行协议新增4条禁止规则(gate存在≠可跨段、禁止连段执行等)
2. **P6中介者→LLM生成者** — 重写Step②/操作约束矩阵/三大红线表，明确"Agent即LLM，prep_prompt输出即prompt"
3. **P6禁止套模板** — 新增禁止规则：禁止只提取metadata批量生成，必须基于p5_description编写差异化步骤
4. **⏸️后死循环修复** — 删除段落3 ⏸️ 后的V4.2.0 quality_check残留区块
5. **P1分批循环进度汇报** — 每5个feature强制汇报进度，单feature超5分钟跳过

**影响范围**：仅 SKILL.md（描述澄清+规则强化），无代码变更

---

## v4.8.14 — 2026-05-23

### 🔴 段落3循环依赖修复 + P0/冒烟比例自动降级

**背景1 — 报告丢失**：V4.8.9起云端Agent持续跳过段落3的P0P1报告输出。根因定位为SKILL.md段落3存在**循环依赖死锁**。

**背景2 — P0比例超标**：云端P6执行复盘报告(2026-05-23)揭示**架构性矛盾**——P2给每个feature第1个main_flow升P0，导致P0占整体40-60%。LOW模型每批5个测试点，部分批次聚类3-5个P0→P0比例36-55%→Gate拒绝。24批中13批因此失败(54%失败率)。

---

### 修复1: SKILL.md 段落3循环依赖修复

**根因**：V4.8.13的"执行P2前强制自检"第一项为"P2 stdout中的__must_emit__已复制到回复"，但此时P2尚未执行，物理上不可能。Agent因逻辑矛盾跳过自检+P2或忘记提取__must_emit__。

**修复（SKILL.md 段落3重写）：**
1. **消除循环依赖** — P2前自检仅检查已存在项(质量评分/PRD报告/cloud_review)；P2后4步强制清单(①解析__must_emit__→②原样复制→③检查其他文件→④完成确认)
2. **移除过早的"段落3完成"** — "✅ 段落3完成"仅保留在P2完成后；P0+P1+quality_check完成后改为进度提示
3. **__must_emit__ 典型内容提供示例**，降低Agent解析门槛

---

### 修复2: P0/冒烟比例自动降级(orchestrator.py)

**原理**：在骨架生成阶段(`prep_prompt --step P6`)检测批次P0/冒烟比例，超标时自动降级，确保Agent基于合理骨架生成用例，Gate检查直接通过。

**实现**：
1. **P0自动降级** — 骨架生成后计算P0比例，若>35%(LOW)则按"非冷烟先降→冷烟后降"顺序降为P1，直到≤阈值
2. **冒烟自动降级** — 同上，若>30%则按"非P0冒烟先降→P0冒烟后降"顺序去除is_smoke标记
3. **降级后冷烟补全** — 降级后若无冷烟但仍有P0，自动补一个冷烟标记
4. **stderr日志** — 每次降级输出结构化JSON日志(action/批次/原始比例/降级条数/新比例)

**影响范围**：
- `tools/orchestrator.py`: prep_prompt P6骨架生成后新增~80行自动降级逻辑
- `SKILL.md`: 段落3重写
- 无API变化，向下兼容

---
## v4.8.13 — 2026-05-22

### 🏗️ 全链路管道修复 + Excel 导出对齐 + 段落确认加固

**代码层**：
- p2_code_generate 自动 export_p0p1 → `__must_emit__` 推送（Agent复制即可）
- P1 code_merge 自动注入 `requirement_id`（从task_meta）→ 修复 case_id/预置条件 REQ-UNKNOWN
- batch-index 0-based 统一（3处：prep_prompt/p6_save_batch/main() agent_output读取）
- export_excel.py 6项对齐（字典+English key/creator/项目/需求/case_type默认/remarks清理）

**SKILL.md层**：
- 段落3/4 "P2/P5自动"≠"段落过渡" 双重澄清
- 6段全加 ⏸️ 强制等待标记
- `__must_emit__` 概念说明
- P6 中介者模式+5步执行模板（Step①-⑤ with操作示例）
- 文件修改规则（batch源/可改, output聚合/不可改）
- P6_guided 提交前自检清单+case_type默认"测试用例"

**边界防御**：
- prep_prompt --step P6 子Agent入口拦截
- p6_save_batch 差1行自动补齐+裸数组自动包装
- 占位符质量标记（remarks不拒绝）

## v4.8.12 — 2026-05-22

### 🏗️ P6中介者模式 + 报告自动推送 + 执行指南重写

- p2_code_generate 自动触发 export_p0p1 → `__must_emit__` 推送 MEDIA（Agent 复制即可）
- P6 角色从"执行者"→"中介者"，三大红线明确"Agent不是生成者，把prompt发给LLM"
- P6 执行流程从 1 行模糊描述重写为 5 步模板（①②③④⑤）
- P6_guided.md 新增"提交前自检清单"（5项检查，不通过不提交）
- p6_save_batch 步骤-期望差1行自动补齐
- prep_prompt --step P6 入口子Agent拦截
- 占位符质量标记（标题/步骤/期望空洞 → remarks）

## v4.8.11 — 2026-05-22

### 🛡️ P6入口子Agent拦截 + 占位符质量标记

- prep_prompt --step P6 增加子Agent检测（入口拦截，子Agent连引导卡都拿不到）
- p6_save_batch 增加占位符质量检测：标记标题占位/步骤空洞/期望空洞到remarks，不拒绝

## v4.8.10 — 2026-05-22

### 🐛 云端 P6 三个阻断修复

**背景**：V4.8.9 云端 P6 卡住（80条用例，P7被阻塞）。修复P1→P2兼容、p6_merge LOW兜底stdout可见、裸数组自动包装。

- P1→P2: children→modules 自动转换
- p6_merge: quality_accepted_low 同步输出 stdout（原仅stderr，Agent看不到）
- p6_save_batch: 裸数组 [] 自动包装为 {"testcases":[]}

## v4.8.9 — 2026-05-22 (patch 2)

### 🐛 P1→P2兼容 + p6_merge LOW兜底可见 + 裸数组自动包装

**背景**：V4.8.9 云端测试发现 4 个问题：①P1骨架输出 children→P2 期望 modules 导致数据结构断裂；②p6_merge LOW 兜底只输出 stderr，Agent 看不到就停下来了；③Agent 输出裸数组 [] 而非 {"testcases":[]}，10条用例丢失；④Agent 仍用子Agent 跑 P6（已有代码检测）。

**修复**：
1. **P1→P2 children→modules 自动转换** (`p1_code_merge`) — 写入 p1_output.json 前将 children 转为 modules
2. **LOW兜底双通道输出** (`p6_merge`) — quality_accepted_low 同步输出 stdout+stderr，确保 Agent 能看到并继续执行 P7
3. **裸数组自动包装** (`p6_save_batch`) — 检测到 list 类型自动包装为 {"testcases": [...]}，不丢失用例
4. **子Agent检测已有** — p6_save_batch/p6_merge/p6_batch_info 三个入口均有 _is_sub_agent_session()，本次 Agent 违规是执行问题

## v4.8.9 — 2026-05-22

### 🏗️ P1 分批生成架构（根治截断问题）

**背景**：P1 一次性生成完整 feature_tree（含所有 scenario）时 JSON 可达 30-80KB，LOW 模型频繁截断。Agent 为规避截断主动压缩 scenario 数量，导致功能点覆盖不足。需长期有效方案。

**架构变更**：P1 拆分为三阶段——骨架→逐feature填充→代码合并

**新增 actions（3个）**：
- `p1_skeleton_save`：保存 module/feature 骨架（无 scenario），输出 feature 列表
- `p1_save_feature --feature-id ID`：保存单个 feature 的 scenarios，校验≥2+含positive
- `p1_code_merge`：代码拼装骨架+所有features → 完整 feature_tree → Gate pass（场景数量校验+操作覆盖校验）

**新增 prompts（2个）**：
- `P1_skeleton.md`：精简 prompt，只要求生成 module→feature 结构，每 feature 的 children 留空
- `P1_feature_scenario.md`：聚焦单一 feature，注入该 feature 上下文+P0 关联规则

**前向兼容**：
- 原 P1 prompt（P1_feature_tree_generation.md）保留，HIGH 模型仍可一shot（但分批是默认推荐路径）
- P1 step_run 仍可用（保留 P1 场景数量 Gate），但推荐用新分批流程
- P2/P3/P4/P5/P6 对 P1 的读取（feature_tree）完全不变

**SKILL.md 段落3 更新**：P1 流程从一shot改为分批三步（骨架→循环填充→合并）

## v4.8.8 — 2026-05-22

### 🔴 段落确认硬性门禁 + 19列字段对齐 + 第二轮云端复盘全量修复

**背景**：V4.8.7 云端测试暴露 8 个新问题（段落确认坍塌、字段缺失、文件名规则缺失等）。经小析+小猿双路评审（均⚠️有条件通过），合并吸收后全量修复。

**修复（8项）：**

**代码层（3项）：**
1. **P6_guided.md 19列全字段对齐** (`prompts/P6_guided.md`) — 格式表扩至19列（对齐export_excel.py），示范JSON含全部字段（含空值），Agent按模板生成不再缺字段
2. **p6_save_batch 错误提示增强** (`orchestrator.py`) — 错误消息明确预期文件名、排查步骤、修复建议
3. **p6_batch_info 时间估算** (`orchestrator.py`) — 新增 `estimated_minutes` 字段（LOW≈1.5分钟/批，HIGH≈0.5分钟/批）

**SKILL.md层（5项）：**
4. **标题去合并化** — "段落3+4合并输出"→"段落3收尾输出"，"段落5+6合并输出"→"段落4收尾输出"，消除标题诱导合段
5. **每段末尾 ⏸️ 强制等待标记** — 6段全加，格式统一为「⏸️ 段落X完成。必须等待用户回复「继续」后，才能进入段落Y。禁止自动跨段。」
6. **段内规则明确化** — 段落3/4新增段内规则说明：P0+P1在段内连续执行，确认仅在段落边界
7. **P6文件名规则明确化** — P6_guided.md 示范区标注文件命名为 `p6_batch_{batch_index:03d}_agent_output.json`（_agent_output后缀不可少）
8. **P6执行描述修正** — "自动连续执行"→"分批自动执行"，明确可设中断点

### 🔴 关键架构
- **段内连续 vs 段间等待**：P0+P1在段落3内连续执行，段落边界（⏸️标记处）才等待用户「继续」。标题去合并化+强制等待标记双保险
- **19列 ≠ 21列**：export_excel.py 实际只有 19 列，不存在 `description` 列

## v4.8.7 — 2026-05-22

### 🔴 LOW模型P6全链路增强 + 段落3MEDIA锚定 + 规则矛盾统一

**背景**：V4.8.6云端运行复盘，发现17项问题（代码7+文档6+流程4），涵盖段落3报告未推送、P6 LOW模型用例数严重不足、SKILL规则自相矛盾、P6失败后抛选择题等。

**修复**:

**代码层（7项）：**
1. **LOW引导卡预算注入** (`p6_guide.py`) — 引导卡新增 `expected_case_count` + `complexity` 字段，模型知道每个TP要生成几条
2. **P6_guided.md全量重写** — 新增预算段落、context文件读取提示、2条用例示范、expected_case_count强制要求
3. **LOW P0/smoke比例放宽** (`orchestrator.py p6_save_batch`) — P0从25%→35%，smoke从25%→30%，适配小批次
4. **p6_batch_info输出执行批次数** — 新增 `total_execution_batches` + `execution_hint` 字段，消除complexity批次和执行批次混淆
5. **规则矛盾统一** (`SKILL.md`) — HIGH模型merge失败强制restart，LOW模型merge失败接受当前用例
6. **p6_merge LOW兜底** (`action_p6_merge`) — LOW模型quality_rejected不再exit(1)，输出 `quality_accepted_low` 继续流程
7. **P6_guided.md context文件读取** — LOW引导卡新增context文件读取步骤

**SKILL.md层（6项）：**
- 段落3模板嵌入MEDIA行 + 质量评分 + cloud_review
- P6段落新增快速参考卡（LOW/HIGH对比表）
- P6段落新增元规则重申（禁止抛选择题）
- P6段落新增进度报告强制要求
- P6失败处理按HIGH/LOW分轨
- 3轮报错暂停指引保留并强化

### 🔴 关键架构说明
- **25% vs 30%/35%**：LOW模型每批3-5条用例，1条P0=20-33%极易突破25%门槛→放宽后用实际批次数验证
- **不restart vs 必须restart**：HIGH模型p6_merge失败重启P6，LOW模型接受当前用例继续
- **total_batches vs total_execution_batches**：前者是complexity分组，后者是LOW执行批次

## v4.8.6 — 2026-05-21

### 🐛 骨架+过滤修复 + P6红线集中化

**背景**：V4.8.5云端复盘发现3个代码bug + Agent违规问题。

**修复**:
1. **文件名过滤加强** (`action_p6_merge`)
   - 排除规则从 `_output` 扩展为 `_output` + `_agent_output`
   - 防止 `p6_batch_N_agent_output.json` 被错误当作context文件读取

2. **skeleton 文件位置统一** (`prep_prompt` + `p6_save_batch`)
   - 从 `data_dir/p6_batch_NNN_skeleton.json` → `data_dir/p6_batches/batch_NNN_skeleton.json`
   - 与 context 文件放在同一目录，降低Agent混淆风险

3. **p6_save_batch 无skeleton自动降级**
   - 骨架文件缺失时：跳过骨架锁定，质量检查降级为宽松模式
   - 不再因缺少skeleton直接拒绝批次

4. **SKILL.md P6 三大红线集中前置**
   - P6段落顶部新增表格：⓵禁止子Agent ⓶禁止跳过prep_prompt ⓷禁止forge gate
   - 在Agent进入P6前即看到红线，而非分散在段落后半部分

## v4.8.5 — 2026-05-21

### 🟢 LOW模型全链路增强

**背景**：V4.8.2云端复盘发现15个问题，其中5个阻塞级已修复，本次补全剩余增强项。

**新增**:
1. **P1 prompt LOW模型精简** (`action_prep_prompt`)
   - LOW模型下 P1 只注入核心5区块（objective + business_rules + constraints + unknowns + test_point_candidates）
   - 原53KB prompt → 预计15-20KB
   - 避免 MiniMax 等小模型 P1 输出被截断

2. **P1 输出截断检测** (`action_step_run`)
   - 检测 JSON 末尾是否完整闭合
   - 截断 → 明确报错 + 提示重跑（含LOW prompt已精简的提示）

3. **Gate LOW模型分级** (`_get_model_tier_for_dir`)
   - LOW模型：G1 + G1.5 从 BLOCK 降为 WARNING
   - 不再因步骤格式细节阻断流程，但仍标记供审查
   - G2/G3/G5/G6 保持 BLOCK 级别
   - 影响：p6_save_batch + p6_merge 两个Gate入口

4. **批次文件格式统一** (`action_p6_merge`)
   - p6_merge 只读取 `batch_[0-9]*.json`，排除 `*_output.json`
   - 避免旧格式文件导致 L3 校验失败

5. **烟雾比例自动纠正（增强）** (`action_p6_merge`)
   - smoke < 10% → 按优先级自动标记 main_flow 类用例为烟雾
   - 记录到 p6_post_process.json

## v4.6.8 — 2026-05-17

### 🔴 P6子任务超时问题修复（简化方案）

- **SKILL.md P6禁令标注**：段落5增加"🔴🔴🔴 V4.6.8 子任务执行禁令(最高优先级)"，明确P6禁止在子任务/子Agent环境中执行
- **删除无效的`--subagent-context`参数检测**：该方案依赖调用方主动传递，实际上不可靠，已移除
- **检测机制**：无（代码层检测走不通，已移除；仅保留SKILL.md禁令）
- **核心防护**：仅SKILL.md禁令（最有效的防护）+ 正确的执行流程（主会话按序执行P0→P1→P2→P3+P4→P5→P6→P7）

---

## v4.6.5 — 2026-05-17

### 🔴 HMAC密钥不一致修复

- **truncation_guard.py HMAC统一**：删除旧的_get_hmac_key_tg/_sign_gate_tg函数，改为从orchestrator.py直接导入_sign_gate，保证新生成的gate pass使用固定HMAC_SECRET
- **背景**：truncation_guard.py使用旧方法（基于文件哈希的HMAC密钥），orchestrator.py使用新方法（固定HMAC_SECRET），两者不一致导致潜在风险

---

## v4.6.4 — 2026-05-17

### 🔴 P7导出被跳过问题（阻塞问题修复）

- **SKILL.md段落5完成后加强提示**：增加强制指令，禁止Agent在此处宣布「任务完成」，必须执行段落6的Step 1（P7质量门禁）+ Step 2（Excel导出）
- **P0P1报告扩展名修复**：orchestrator.py 第5390行硬编码 `.html` → 改为 `.md`，与SKILL.md保持一致，解决Media failed问题

### 🔴 段落1完成后提示词修复

- **修复需求重复询问**：段落1完成后增加段间判断逻辑，如用户已在之前发送需求文档则直接执行step0，不再重复提示「请发送需求正文」

---

## v4.6.3 — 2026-05-17

### 🔴 飞书附件路径自动查找（阻塞问题修复）

- **Step 1 精准查找**：搜索 ~/Downloads、/tmp、~/Desktop、~/Documents、~/Library 最近30分钟内的 docx/txt/pdf 文件
- **Step 2 安全复制**：找到后 cp 到 data_dir/requirement.docx（使用 cp 而非 mv，保留源文件）
- **Step 3 兜底搜索**：Step 1 未找到时扩大范围到全盘搜索2小时内文件，返回最多5个候选让用户确认
- **覆盖路径**：解决飞书附件下载到非标准路径导致的"需求文档尚未上传到处理目录"错误

---

## v4.6.2 — 2026-05-16

### 🔴 知识库完整修复

- **新增knowledge目录**：复制skill_v2的knowledge到skill_v4（含methodology/company_standards/defect_patterns等完整知识体系）
- **SKILL.md增加文档保存说明**：明确上传文档必须移动到data_dir/requirement.docx

### 🔴 需求载荷前置重构（最高优先级）

- **新增⛔入口强制检查章节**：提升为技能最开头的独立章节，优先级高于运行协议
- **新增反面案例表格**：明确列出"等会发"、"稍后发"、"模糊引用"等不算已收到需求
- **新增常见误判场景附录**：Agent自我纠偏参考
- **6段确认模式中保留二次校验**：作为最后防线
- **强制需求载荷前置**:禁止无需求时进入Onboarding，必须先收到需求文档
- **Onboarding结束后直接开始分析**:不再等待「继续」，直接提示发送需求文档

### 🔧 三方审计修复

- **_extract_module动态化**：移除"债券投顾分润"硬编码，改用5级动态提取（tp.module_name > module_map.json > keyword_fallback > source_scenario > 编码展示）+ config/module_map.json配置
- **page_path全链路消费**：11个P6模板全部使用page_path（三重消费：scenario_inject + 模板引擎 + Gate G1/G7校验）
- **knowledge引用修复**：p6_templates.py新增knowledge_injected，引用reviewed_cases
- **batch_size统一**：p5_prepare.py导入orchestrator.P6_BATCH_SIZE=8
- **module_map.json默认配置**：填充M01-M10通用模块映射+关键词fallback
- **P6重试次数增加**：p6_retry_count 2→4次（指数退避）

### 🔴 P6 Prompt核心原则新增

- **不确定性处理**：新增"如果不确定，输出'待确认'而非编造"核心原则
- **5种情况明确处理方式**：字段名/页面路径/按钮文本/业务规则/操作顺序不确定时的正确做法
- **标记格式**：remarks中标注`待确认原因:XXX`，case_type标注为`条件验证`
- **效果**：带"待确认"的用例会被Gate拦截，由人工确认后补充

### 📝 其他修复

- **SKILL.md版本号统一**：标题和description统一为V4.6.0

---

## v4.3.0 — 2026-05-15

### 🏗️ 架构简化（P6三轨模式废弃，统一为单一流程）

- **废弃turbo/hybrid/strict三种P6模式**：统一为一条流程 `P5上下文 → AI生成 → 模板整理 → Gate检查 → 输出`
- **Onboarding简化为3步**：移除原第3步P6模式选择（set_p6_mode），3步为：PRD审查 → L5知识库 → 图片API密码
- **废弃命令**：`set_p6_mode`（Onboarding模式选择）、`p6_code_generate`（hybrid模式一键生成）
- **统一流程适用所有模型**：所有模型统一使用分批流程（p6_batch_info → prep_prompt+p6_save_batch循环 → p6_merge）
- **P6重试规则统一**：原strict模式的自动重试规则升格为所有模型的通用规则
- **p6_templates.py定位更新**：从"hybrid模式代码生成"改为"统一流程辅助"（模板整理阶段使用）
- **引用文件表同步更新**：p6_templates.py描述同步修改

---

## v4.2.0 — 2026-05-15

### 🔧 字段标准化（与评审工具v4.1.1对齐）

- **export_excel.py 需求列修复**: 改取 `case["project"]` 而非 `case["requirement"]`（后者存的是task_id无业务含义）
- **export_excel.py 创建者固定**: 固定返回 `"AI"`（之前为空）
- **export_excel.py 经办人**: 保持空字符串

### 📝 字段定义19列标准

| 列名 | 字段 | 说明 |
|------|------|------|
| 项目 | project | 取P6 JSON的project字段 |
| 类型 | case_type | 固定"测试用例" |
| 用例编号 | case_id | 原始编号 |
| 需求 | project | 取P6 JSON的project字段 |
| 优先级 | priority | P0→Highest映射 |
| ... | ... | ... |

---

## v4.1.1 — 2026-05-12

### 🐛 Bug修复

- **P0段落3内容修复** (SKILL.md): 字段路径从顶层改为blocks下business_objects/operations/business_rules/test_point_candidates；clarification_questions不存在，改为读blocks.unknowns
- **评审链接不展示修复** (orchestrator.py): cloud_review增加pushed字段，解决Agent读undefined→不展示链接
- **模型名归一化** (orchestrator.py): 新增_normalize_model_name()，去空格/连字符/下划线后匹配，解决deepseek-v4-pro vs deepseek v4 pro匹配失败
- **知识库同步URL修复** (cloud_sync.py+orchestrator.py): 修复嵌套结构review_tool.api_url读取逻辑，解决知识库从未同步问题

### ⚡ 性能/体验优化

- 云端知识库同步为唯一数据源，本地knowledge/目录已移除，58文件按需拉取
- 更名为qc-req2testcase-generator，触发词同步更新
- 废弃文件清理（SKILL.md.bak、prompts/archive、tools/review_tool）

# Changelog

## Changelog

### v4.0.1 (2026-05-11)

**变更类型**: enhancement（Phase 1-4 优化）

**Phase 1：评审推送闭环**
1. **SKILL.md段落8评审推送指令补全**：step7_export返回cloud_review字段时，Agent需输出评审链接
2. **SKILL.md段落3评审推送指令补全**：export_p0p1返回cloud_review字段时，Agent需输出评审链接
3. **orchestrator新增 `_push_p0p1_to_review_tool`**：段落3完成后推送P0/P1摘要到评审工具
4. **step5-7.md P7旧流程清理**：移除"构造Prompt+调用LLM"等过时描述
5. **用户交互指令表增加"重试推送"**：`retry_push` action
6. **`_enqueue_failed_push` 增加 `push_type` 字段**：区分P6用例推送和P0/P1摘要推送
7. **p0p1_summary补充模块名列表**：`p1_modules` 字段

**Phase 2：业务域匹配完善**
8. **project_domain_mapping.json升级v2.0**：10组项目映射（11→10，SMT合并）+ 16条同义词
9. **同义词模糊匹配**：`_match_project_to_domains` 增加第二层同义词匹配
10. **task_meta写入域匹配结果**：新增 `domains`/`matched_projects`/`matched_synonyms`/`project_name` 字段
11. **domain字段统一为中文域名**：`resolved_domain` 优先用域匹配结果
12. **4层注入支持同义词触发**：纯同义词匹配限制L1注入防prompt膨胀
13. **推送传递project_name**：`_push_to_review_tool` 补充project_name读取

**Phase 3：评审工具前端改造**
14. **后端新增 `GET /api/projects/dict`**：项目字典下拉框数据（动态读取+种子降级）
15. **后端新增 `dictionary.js`**：完整项目字典CRUD（增删改查+Levenshtein模糊匹配+别名）
16. **前端新建项目改为下拉选择**：el-select filterable + 手动输入切换
17. **导入匹配优先用project_name**：orchestrator推送的真实项目名
18. **新建项目同步创建字典条目**：保持数据一致性
19. **前端重名预检**：创建前检查避免重复提交

**Phase 4：文档清理**
20. **cloud.json.example更新**：实际腾讯云地址+experience_sync标注为预留

**四路交叉评审**：每阶段均经过小析/小文/小猿+小墨四路评审，所有P0/P1问题已修复

---

### v4.0.0 (2026-05-09)

**变更类型**: major feature

**变更内容**:
1. **云端评审推送**：新增 `_push_to_review_tool()` 和 `_retry_pending_reviews()`，段落3完成后自动推送P0/P1/P6数据到评审工具
2. **知识库同步**：新增 `_sync_knowledge_from_cloud()`，支持从云端拉取评审经验反馈到L6经验库
3. **项目→业务域匹配**：新增 `_match_project_to_domains()`，基于project_domain_mapping.json自动匹配12个一级业务域
4. **HMAC来源审计**：Gate Pass增加 source_action 字段，step7_export全链路审计来源合法性
5. **重试队列**：推送失败的评审记录写入 pending_reviews.jsonl，支持后续手动/自动重试
6. **P0/P1报告导出**：新增 `export_p0p1.py`，段落3完成后自动生成P0/P1结构化报告（MD+HTML）
7. **PRD审查增强**：新增 `export_prd_review.py`，PRD审查结果独立导出为Excel
8. **业务域扩展**：从8域扩展到12域（新增投顾/投研/自营/互联网终端）
9. **Onboarding交互优化**：需求载荷就绪前置检查，防止空需求启动流程
10. **架构声明升级**：SKILL.md metadata版本统一为V4.0.0，description更新

**新增文件**:
- tools/export_p0p1.py
- tools/export_prd_review.py
- config/project_domain_mapping.json
- prompts/P0_prd_review_enhance.md
- prompts/P6_api_rules.md

**影响范围**:
- orchestrator.py: 新增4个action（step7_export增强、retry_push、knowledge_sync、domain_match）
- SKILL.md: 架构声明、版本号、引用文件表全面更新

### v3.5.8 (2026-05-08)

**变更类型**: feature (段落3完成后发送P0/P1报告文件)

**新增：段落3完成后自动生成并发送需求理解与功能点拆解报告**

问题：用户反馈段落3完成后，页面上虽然显示了需求结构化的markdown和问题清单，但没有文件可以下载发送给产品经理审阅。

修复：
1. **新增export_p0p1.py脚本** — 将P0的blocks_markdown/issues和P1的feature_tree导出为结构化的Markdown文件
2. **orchestrator.py新增export_p0p1 action** — 调用导出脚本，生成p0p1_report.md文件
3. **SKILL.md指令更新** — 段落3完成后，自动执行export_p0p1并通过MEDIA指令发送文件给用户

文件内容：
- 第一部分：P0需求结构化（需求目标、质量评分、需求结构化内容、问题清单）
- 第二部分：P1功能点拆解（模块/功能点/场景树，带统计信息）

影响：
- 用户在段落3完成后可以直接收到p0p1_report.md文件，方便发送给产品经理审阅
- 如果开启了PRD审查，同时发送prd_review_report.md文件
- 不影响其他段落的执行流程

---

### v3.5.7 (2026-05-08)

**变更类型**: bugfix (PRD报告文件自动生成)

**修复：Agent未调用quality_check导致PRD报告文件未生成**

问题：V3.5.5将PRD报告文件生成逻辑放在quality_check action中，但Agent在P0完成后没有调用quality_check（直接用step_run通过），导致报告文件未生成，用户无法下载。

修复：
1. **step_run中自动生成报告** — P0的step_run成功后，如果prd_quality_review=True，自动读取p0_output.json并生成prd_review_report.md
2. **SKILL.md指令更新** — 段落3完成后，Agent检查报告文件是否存在，存在则发送下载链接

影响：
- 不依赖Agent是否调用quality_check，只要P0完成且开启PRD审查，报告文件必定生成
- 跳过PRD审查的任务不受影响

---

### v3.5.6 (2026-05-07)

**变更类型**: enhancement (PRD审查内容质量校验)

**新增：PRD审查内容质量三项校验**

在V3.5.4字段存在性校验的基础上，新增内容质量校验：

1. **blocks_markdown最小长度校验** — 内容不得少于200字符，防止Agent输出空字符串或过于简单的内容
2. **关键维度检查** — blocks_markdown必须至少包含2个维度（输入/输出、业务规则、角色权限、状态流转、约束条件），防止Agent只输出模块功能点列表
3. **issues格式校验** — issues数组中的对象必须包含severity/location/type/problem/suggestion字段，防止Agent输出不完整的问题清单

**错误类型**
- 字段缺失：`prd_review_validation_failed`
- 内容质量不达标：`prd_review_quality_failed`

**影响**
- 跳过PRD审查的任务不受影响
- 开启PRD审查后，Agent必须输出高质量的blocks_markdown和issues，否则step_run拒绝

---

### v3.5.5 (2026-05-07)

**变更类型**: enhancement (PRD审查报告文件输出 + blocks_markdown增强)

**新增：PRD审查结果自动生成Markdown报告文件**

1. **自动生成报告文件** — quality_check返回时自动将PRD审查结果写入 `{data_dir}/prd_review_report.md`，包含质量评分、结构化结果、问题清单
2. **Agent发送文件链接** — SKILL.md指令Agent在展示PRD审查结果后，发送文件下载链接给用户（像Excel一样）
3. **blocks_markdown增强** — 增加业务规则、角色权限、状态流转、约束条件等5个维度，输出更丰富的需求结构化内容

**改动文件**
- `tools/orchestrator.py`: quality_check中增加报告文件生成逻辑，返回prd_review_report_path字段
- `SKILL.md`: 段落3中P0执行后增加文件发送指令
- `prompts/P0_prd_review_enhance.md`: blocks_markdown输出要求增强，新增5个维度

**用户体验提升**
- PRD审查结果可下载保存，方便分享给产品经理
- 结构化结果更丰富，包含业务规则、权限、约束等测试用例设计关键信息

---

### v3.5.4 (2026-05-07)

**变更类型**: bugfix (PRD审查字段强制校验)

**修复：Agent忽略PRD审查字段导致输出缺失**

问题：开启PRD审查后，prompt正确注入了blocks_markdown和issues输出要求，但Agent（如DeepSeek-v4-pro）忽略了这两个字段，只输出基础字段，导致PRD审查增强功能完全无效。

修复：
1. **step_run中加PRD审查字段强制校验** — 当prd_quality_review=True时，检查P0的agent_output是否包含blocks_markdown和issues，缺少直接返回prd_review_validation_failed错误并拒绝
2. **SKILL.md中加强警告** — 在段落3的P0执行指令前增加红色高亮警告，明确告知Agent这两个字段是代码层强制校验的必填字段

影响：开启PRD审查后，Agent必须输出blocks_markdown和issues，否则step_run拒绝。跳过PRD审查的任务不受影响。

---

### v3.5.3 (2026-05-07)

**变更类型**: bugfix (step0覆盖task_meta)

**修复：step0全量覆盙task_meta.json导致prd_quality_review丢失**

问题：set_prd_review在Onboarding时正确写入prd_quality_review:true到task_meta.json，但step0执行时全量重建meta对象并覆盖写入，导致该字段丢失。

修复：step0写入task_meta前先读取已有内容，保留已有字段（如prd_quality_review），新字段覆盖旧字段。

---

### v3.5.2 (2026-05-07)

**变更类型**: security hardening (Agent绕过防护)

**核心功能：防止Agent绕过orchestrator伪造执行结果**

问题背景：MiniMax M2.7等弱模型在orchestrator返回错误时，不按SKILL.md指令重试，而是直接用Python调用内部函数伪造gate/output/state文件。

**新增防护机制：**
1. **SKILL.md绝对禁止规则** — 7条硬规则，明确禁止直接写gate/output/state、import orchestrator、伪造结果
2. **gate来源校验** — gate文件新增source_action字段，验证时检查来源是否合法
3. **全局变量_CURRENT_ACTION** — 只在main() dispatch时设置，Agent import时为空→指纹不匹配
4. **output文件写入保护** — step_run前检测文件是否被Agent提前写入，是则删除
5. **step7全链路审计** — 导出前检查所有gate的source_action是否合法，非法来源拒绝导出

**改动文件**
- `tools/orchestrator.py`: _CURRENT_ACTION全局变量 + _VALID_GATE_SOURCES映射 + _write_signed_gate加source_action + _verify_gate_hmac加来源校验 + step_run加output保护 + step7_export加审计
- `SKILL.md`: 操作约束矩阵追加V3.5.2绝对禁止行为

**兼容性**
- 旧版本gate文件（无source_action字段）自动跳过来源校验，不影响现有任务
- HMAC签名机制不变，新增字段参与签名计算

---

### v3.5.1 (2026-05-07)

**变更类型**: feature enhancement (PRD审查增强)

**核心功能：PRD质量审查增强输出**

用户在Onboarding选择「开启PRD审查」后，P0完成时自动输出：
- 需求结构化Markdown（带❗️不清晰标识）
- 问题清单（severity/location/type/description/suggestion）
- 评分<0.5仍然中断（保持现有逻辑），但中断前输出内容
- 评分≥0.5时展示内容后自动继续P1，不增加交互

**新增文件**
- `prompts/P0_prd_review_enhance.md` — PRD审查增强prompt（条件注入）

**新增action**
- `set_prd_review` — 设置PRD审查开关（Onboarding第1步用户选择后调用）

**改动文件**
- `tools/orchestrator.py`: prep_prompt条件注入 + quality_check增强返回 + set_prd_review action + 版本号3.5.1
- `SKILL.md`: 段落1第1步追加set_prd_review调用 + 段落3追加quality_check展示指令 + 版本号3.5.1

**兼容性**
- 跳过PRD审查时完全不触发新代码
- P1-P7无任何变化
- gate pass/HMAC签名不受影响
- 非交互模式不变（不增加等待点）

---

### v3.5.0 (2026-05-06)

**变更类型**: major release (推广前最终版)

**核心修复：turbo 模式绕路问题（三层防线）**

**问题**：turbo 模式云端测试中，Agent 以"耗时长"为由自行调用 `p6_code_generate`（hybrid 路径），导致用例质量低（步骤截断、内容重复），`generation_method: code_template` 而非 Agent 直出。

**修复1：orchestrator 代码硬拦截**
- `action_p6_code_generate` 入口增加模式检查，turbo/strict 模式调用直接返回 `mode_blocked` 错误
- hybrid 模式正常通过

**修复2：step7_export 模式一致性校验**
- 导出 Excel 前检查 `generation_method` 与 `p6_mode` 是否匹配
- turbo/strict 模式下 `generation_method=code_template` 直接拒绝导出，返回修复指引
- hybrid 模式下 `generation_method` 必须为 `code_template`

**修复3：SKILL.md 硬约束**
- turbo 段落开头加两条红色严禁标记
- 明确禁止调用 `p6_code_generate`，禁止以"耗时长"为由切换模式

**合并修复（V3.4.6~V3.4.11 全部变更）**
- V3.4.6: step0 自动发现需求文档
- V3.4.7: P0 提升改为 feature 级，P2 异常每 feature 只生 1 条
- V3.4.8: P1 scenario ≤6 硬校验
- V3.4.9: 空 data_dir 误命中修复，P0 expected_case_count 上限 2
- V3.4.10: export_excel.py 冒烟阈值同步修复（8%→5%）
- V3.4.11: 项目名自动提取（从需求文件名）

**验证结果**
- turbo/strict 模式调用 p6_code_generate → mode_blocked ✅
- hybrid 模式调用 p6_code_generate → 通过模式检查 ✅
- SKILL.md 约束文本到位 ✅
- 语法检查通过 ✅

---


**变更类型**: bugfix (测试用例项目名为空)

**问题**: 生成的测试用例 Excel 中项目字段为空。

**根因**: orchestrator 对每条用例执行 `tc.setdefault("project", "")`，直接设为空字符串，未从任何地方读取项目名。

**修复**:
1. **step0 自动提取项目名**：从需求文件名提取（去掉路径、扩展名、云端上传附加的 UUID 后缀 `---xxxx`），写入 task_meta.json 的 `project` 字段
2. **p6_code_generate 读取项目名**：从 task_meta.json 读取 `project` 字段，填充到每条用例

**示例**：
- 文件名 `集团CRM_V1.0.14_兴光闪耀活动机构战报优化产品需求文档---7bc1d4d1-...docx`
- 提取项目名：`集团CRM_V1.0.14_兴光闪耀活动机构战报优化产品需求文档`

---


**变更类型**: bugfix (小析+小猿评审发现的两个隐性问题 + export_excel冒烟阈値漏改)

**问题1: `_auto_discover_requirement` 空 data_dir 误命中**
- 根因：`os.path.dirname("")` 返回 `""`，原代码用 `os.path.isdir(d)` 判断，在某些系统下 `isdir("")` 可能返回 True，导致跳过空路径检查直接扫描 Downloads 误命中无关文件
- 修复：在 `isdir` 判断前增加明确的非空字符串检查 `if not d`，彻底屏蔽空路径

**问题2: 冒烟比例数学上仍不达标8%**
- 根因：P0 测试点因 category 为 exception/integration 被判 L3，`expected_case_count=3`，导致 P0 用例展开过多、冒烟比例被稀释；最坏情况冒烟比例 5.3% < 8%
- 修复1：P0 测试点 `expected_case_count` 强制上限为 2（P2 complexity 标注和 P5 merge 两处同步修复）
- 修复2：冒烟门槛下限从 8% 调整为 5%（orchestrator.py P6_QUALITY_RULES + export_excel.py 两处同步修复）
- 数学验证：12 features 最坏情况冒烟 5.6%，达标5%门槛

**问题3: export_excel.py 冒烟阈値漏改（云端测试发现）**
- 根因：orchestrator.py 的 P6_QUALITY_RULES 已改为 5%，但 export_excel.py 第309行独立硬编码了 `0.08`，导致冒烟比例 7.95% 被拦截（> 5% 但 < 8%）
- 修复：export_excel.py 冒烟阈値从 0.08 改为 0.05，与 orchestrator.py 一致

**云端测试验证结果（兴光闪耀需求，4模块/12功能点）**
- P1 scenarios: 39（原52，降25%），所有feature的scenario数量≤ 6 ✅
- P2 测试点: 68（原130，降48%），P0=12 ✅
- P5 测试点: 67，total_expected_cases=151
- P6 用例: 151条（原320，降53%），冒烟12条(7.9%) ✅
- P7 门禁: PASS ✅，Excel导出: 成功 ✅

---


**变更类型**: bugfix (P1 scenario数量膨胀根治)

**问题**: P1 Agent将单个feature拆出11个scenario（如「月榜榜单查看」「月榜数据导入」），导致P2测试点膨胀。即使已修复异常用例生成逻辑，根源过多的scenario仍会导致用例过多。

**修复内容**:
1. **P1 prompt新增约束4**：每feature的scenario建议2-5个，最多不超过6个；超过时必须合并相似场景
2. **P1质量门禁新增第6条**：任何单个feature的scenario数量不得超过6个，超过时必须在coverage_check.scenario_overflow中标注
3. **orchestrator P1 quality_check新增硬校验**：任何feature超过6个scenario直接拒绝，返回具体超过的feature列表

**预期效果**：同样需求（兴光闪耀，4模块/12功能点）：P1 scenario从52个降至最多72个，P2测试点从130条降至约60-80条，总用例从320降至约150-200条

---


**变更类型**: bugfix (冒烟比低 + 用例数量过多)

**问题1: 冒烟比例1%（应≥8%）**
- 根因：P0提升逻辑是“每module只提升第1个main_flow”，4个module只产生4个P0测试点，320条用例中冒烟只有4条(1%)
- 修复：改为“每feature第1个main_flow升为P0”，12个功能点就有‒12个P0测试点，冒烟比例大幅提升

**问题2: 用例数量320条过多**
- 根因：P2代码生成对每scenario无条件生成「正向+异常」2条，12个功能点平均含多个scenario，导致P2测试点膨胀到130条
- 修复：异常验证改为「每feature只生成1条」，避免每scenario都生成异常用例；权限验证增加scenario_type信号判断，不再仅凭多角色就生成

**预期效果**：
- 同样需求（兴光闪耀，4模块/12功能点）：P2测试点从130条降至约60-70条，总用例从320降至约150-180条
- 冒烟比例：从1%提升至预期8-15%

---


**变更类型**: bugfix (段落2 requirement_length=0 根治)

**核心问题**: V3.4.5云端测试中，Agent未正确替换SKILL.md中的`{docx_path}`占位符，导致step0收到空的requirement_file，requirement_length=0，后续所有段落无需求文本可用。

**根因**: SKILL.md段落2指令依赖Agent正确替换`{docx_path}`，但Agent在云端环境下直接原样传入占位符或传空字符串。

**修复内容**:
1. **新增`_auto_discover_requirement(data_dir)`函数**：当requirement_file和requirement_text均为空时，自动扫描以下路径（按优先级）：
   - data_dir同级目录
   - ~/Downloads
   - ~/Desktop
   - ~/.openclaw/workspace/sharetasks
   - 当前工作目录(cwd)
   - 优先.docx，其次.md，最后.txt；同目录取最新修改时间的文件
2. **step0返回auto_discovered字段**：自动发现时返回`auto_discovered:true`和warning说明，便于Agent感知
3. **step0无文件时明确报错**：扫描仍未找到时返回`status:error`并给出明确提示，exit(1)
4. **step0_8_prep兜底**：requirement_file为空时先从task_meta.json读取，避免Agent跨段落传参丢失

---


**变更类型**: bugfix (移除$ORCH引用触发安全检查)

**核心问题**: V3.4.4云端测试中，step_3_display和step_4_display包含`$ORCH`字符串，触发了云端exec工具的shell变量注入安全检查，导致orchestrator完全无法执行

**修复内容**:
1. 移除step_3_display和step_4_display中的`$ORCH`、`exec:`、双引号包裹等可能触发安全检查的内容
2. 改为纯文本描述（"执行 orchestrator --action xxx"），不包含shell变量或引号

---

### v3.4.4 (2026-05-05)

**变更类型**: bugfix (Onboarding第3/4步执行指令补全)

**核心问题**: V3.4.3云端测试中Agent正确展示了交互选项，但用户输入密码后没有执行check_image_api验证命令，导致图片理解未启用

**根因**: step_3_display和step_4_display只包含展示文案，没有告诉Agent收到用户回复后要执行什么命令

**修复内容**:
1. **step_3_display增加执行指令**: 用户选模式后必须执行set_p6_mode
2. **step_4_display增加执行指令**: 用户输密码后必须执行check_image_api验证

---

### v3.4.3 (2026-05-05)

**变更类型**: bugfix (Onboarding交互内容修复)

**核心问题**: V3.4.2云端测试中Agent展示了交互步骤（修复生效），但内容完全错误——Agent自由发挥而非按SKILL.md中的文案展示

**根因**: Agent读到了步骤名称但没有读SKILL.md中每步的具体展示内容，自己"创造性"理解后输出了错误文案

**修复内容**:
1. **onboarding返回JSON包含每步完整展示文案**: step_1_display到step_4_display，Agent只需原样输出
2. **版本号统一为3.4.3**

**设计原则**: Agent不需要理解步骤含义，只需要按顺序原样输出orchestrator返回的display文案

---

### v3.4.2 (2026-05-05)

**变更类型**: bugfix (Onboarding交互流程修复)

**核心问题**: V3.4.0云端测试中Agent跳过了Onboarding的分步交互（第1-4步全部未展示），导致P6模式未选择、图片密码未输入

**根因**: SKILL.md第3步（P6模式选择）的描述过于复杂（包含“Agent执行onboarding”、变量替换、多层代码块），Agent解析困难后跳过了整个交互流程

**修复内容**:
1. **简化SKILL.md第3步格式**: 与第1步、第2步保持一致的简洁格式（标题+代码块选项+等待提示）
2. **移除多余指令**: 删除“Agent执行 onboarding（如已执行则跳过）”等混淆指令
3. **统一四步格式**: 第1-4步全部采用相同结构，降低Agent解析难度
4. **orchestrator onboarding返回增加next_action字段**: 明确告知Agent"接下来必须展示4步交互"，不允许跳过
5. **SKILL.md强化onboarding指令**: “段落1还没完成！必须继续执行4步交互”
6. **onboarding返回包含每步完整展示文案**: step_1_display到step_4_display，Agent只需原样输出，不需自己创造内容

**测试验证**: SKILL.md格式一致性确认 ✅

---

### v3.4.0 (2026-05-05)

**变更类型**: architecture (P6双轨架构 + 模板引擎)

**核心问题**: minimax-m2.7在P6阶段反复证明无法稳定生成高质量差异化用例，需要根据模型能力提供不同执行路径

**竞品借鉴**: AITestCraft (github.com/liwanlei/AITestCraft)

**核心改动**:
1. **P6双轨架构（3条路径）**:
   - turbo: 强模型直出，宽松门禁，P7兆底
   - hybrid: 代码生成全部用例 + 可选Agent润色P0+P1
   - strict: 严格门禁 + 自动重试（V3.3.5逻辑）
2. **新增p6_templates.py模板引擎**: 11套category模板，基于P5测试点自动生成完整用例
3. **新增action p6_code_generate**: hybrid模式核心，一条命令完成全部P6
4. **新增action set_p6_mode**: 用户选择执行路径
5. **Onboarding新增第3步**: P6模式选择（系统推荐+用户决定）
6. **P7模式感知**: turbo下C2/C6.1降级为WARNING
7. **p6_save_batch模式分支**: turbo宽松/strict严格/hybrid拒绝
8. **MODEL_RECOMMENDATIONS**: 模型→推荐模式映射表
9. **SKILL.md段7三模式分支**: 根据p6_mode执行不同流程

**模板引擎覆盖**: main_flow/branch/integration/permission/exception/boundary/compatibility/performance/security/state_migration/api

**测试结果**:
- p6_code_generate: 149条用例秒级生成 ✅
- set_p6_mode: turbo/hybrid/strict切换正常 ✅
- 语法检查: OK ✅

---

### v3.3.5 (2026-05-05)

**变更类型**: quality + efficiency (P6质量提升 + 竞品借鉴 + 效率优化)

**核心问题**: V3.3.4云端P6生成151条用例但P7门禁失败（C2步骤数≠期望结果数，C6.1前置条件检测过严）

**竞品借鉴**: AITestCraft (github.com/liwanlei/AITestCraft)
- 极简schema思路：Agent只生成8个核心字段，代码补全其余11个
- 自动重试机制：p6_save_batch失败时Agent自动重试，不报告用户
- 正面规则替代禁止描述：告诉Agent怎么做而不是不要做什么
- 确定性输出：temperature=0思路

**修复内容**:
1. **骨架改为step_expected_pairs配对格式**: 天然保证步骤数=期望结果数，根因修复
2. **p6_save_batch增加步骤-结果数量校验**: 阈值15%，差≥11即判定，P6阶段拦截不等P7
3. **P6 prompt增加最佳实践示例**: 含正向/异常/权限三种场景的完整示例，正面引导
4. **P6输出简化**: Agent只生成8个核心字段，代码自动补全其余11个
5. **SKILL.md增加P6自动重试规则**: 最多2次自动重试，用户无感
6. **P7 C6.1检测放宽**: 2/3匹配即通过 + 关键词扩充
7. **P6 prompt增加确定性输出提示**: 借鉴AITestCraft temperature=0思路

**增量修补铺路(V3.4)**: P7输出增加fixable_cases字段，为后续增量修补做准备

---

### v3.3.4 (2026-05-05)

**变更类型**: hardening + quality (Agent遵循性强制约束 + P6用例质量改善)

**核心问题**: V3.3.2云端测试中Agent无视SKILL.md指令，P2仍走老路径(prep_prompt+step_run)；P6生成占位符内容通不过质量门禁

**修复内容**:
1. **step_run增加P2硬拒绝**: 与P5/P6/P7对齐，代码层强制拒绝非法调用
2. **prep_prompt增加P2/P5/P7准入检查**: 更早拦截，阻止无效LLM调用浪费Token
3. **p6_save_batch增加步骤唯一性检查**: 所有用例步骤相同时直接拒绝（占位符检测）
4. **P6 prompt增加反占位符警告**: 明确告知Agent不允许泛化描述
5. **SKILL.md顶部增加操作约束矩阵**: 结构化表达每个Step的Agent角色和唯一正确命令
6. **SKILL.md段落4精简**: 删除所有"禁止"描述，只保留唯一正确路径

**设计原则**: 纵深防御——SKILL.md约束矩阵 → prep_prompt准入 → step_run硬拒绝，三层拦截确保Agent只能走正确路径

**测试结果**:
- step_run P2: REJECTED ✅
- prep_prompt P2: REJECTED ✅
- prep_prompt P5: REJECTED ✅
- prep_prompt P6: OK（分批流程需要） ✅
- p2_code_generate: 正常执行 ✅

**P6用例质量改善（同版本追加）**:
7. **batch_size从10降到6**: 降低模型单批生成压力，每批12-18条用例
8. **骨架预生成steps_hint/expected_hint**: 基于category+description为每条用例预生成差异化步骤草稿，Agent任务从"从零创造"降级为"细化补充"
9. **P6 prompt增加反面few-shot示例**: 明确展示不合格输出vs合格输出
10. **步骤唯一性检查改为跨测试点级别**: 同测试点内步骤相似是合理的，只拦截跨测试点完全相同的占位符

---

### v3.3.2 (2026-05-05)

**变更类型**: optimization (P2代码路径 + P6 prompt瘦身)

**核心问题**: V3.3.1云端测试中P2步骤Agent未能正常执行LLM推理，手动构造了机械化测试点；P6因prompt过长(68KB/47K chars)导致Agent无法生成有效JSON

**数据来源**: V3.3.1云端测试 task_20260505_002437 全量JSON产物分析 + 小猿交叉评审

**核心原则**: P2代码硬控结构，零Agent依赖；P6减少注意力分散，提高指令遵循精度

**修复内容**:
1. **新增action_p2_code_generate**（核心改动，~170行新增代码）：
   - 从P1 feature_tree自动生成测试点，零Agent依赖
   - 规则引擎：每scenario生成2-4个测试点（正向+异常+按需补充边界/权限）
   - 优先级硬控：main_flow=P1，exception=P2，boundary=P3，permission=P1，每module第1个正向升P0
   - 覆盖率校验：确保所有module和feature被覆盖
   - complexity/expected_case_count自动标签
   - truncation_guard + gate pass完整流程
2. **P6 prompt瘦身**（47577→29493 chars，压缩38%）：
   - 移除完整p5_output.json注入（-40.9%），改为批次信息中注入P1 scenario语义详情
   - 移除defect_schema知识注入（-6.3%，与P6用例生成无关）
   - 接口测试规则拆分为独立文件，按需加载（-9.5%，无接口场景时）
   - 骨架JSON改compact格式（-4.2%）
   - 新增全局上下文摘要（告知模型需求整体范围）
   - 新增P1 scenario语义注入（替代被移除的完整p5，给P6业务上下文）
   - 新增输出长度预估提示（帮助模型规划输出结构）
3. **新增_check_api_features函数**（~30行）：
   - 检查P0 operations和P1 feature names中是否包含接口相关关键词
   - 决定是否注入接口测试规则
4. **P6模板拆分**：
   - P6_testcase_generation.md: 603行→468行（移除接口规则段落）
   - P6_api_rules.md: 新建135行（从原模板拆出，按需加载）
5. **SKILL.md段4更新**: 从Agent推理改为代码路径（p2_code_generate）
6. **版本号统一为3.3.2**: orchestrator.py + SKILL.md

**测试结果**:
- p2_code_generate: 35条测试点，P0:5/P1:10/P2:15/P3:5，覆盖5/5模块 ✅
- P6 prompt: 47577→29493 chars（压缩38%） ✅
- _check_api_features: 正确识别推送功能 ✅
- 语法检查: OK ✅

**交叉评审**: 小猿评审通过（有条件），3个BLOCK项已在实现中修正

---

### v3.3.1 (2026-05-04)

**变更类型**: version-bump (版本号统一)

**核心问题**: V3.3.0发布时orchestrator.py的SKILL_VERSION残留为"3.2.9"，与SKILL.md版本号不一致

**修复内容**:
1. **版本号全量统一为3.3.1**: orchestrator.py SKILL_VERSION、SKILL.md version、export_excel.py标题、HTML报告版本号
2. **CHANGELOG补全**: 补充V3.3.0和V3.3.1变更记录

### v3.3.0 (2026-05-04)

**变更类型**: architecture-change (P7代码硬校验 + 校验去重)

**核心问题**: V3.2.9云端测试中P7质量自检阶段Agent无法生成有效JSON（输入350KB/89K tokens过大），导致任务卡死在P7，无法进入step7_export

**数据来源**: V3.2.9云端测试 task_20260503_233148 全量JSON产物深度分析 + 双路交叉评审（小析测试分析+小猴代码实现）

**核心原则**: P7代码硬校验，零Agent依赖，秒级完成。与P5(p5_code_merge)、P6(p6_save_batch+p6_merge)一样走代码路径。

**修复内容**:
1. **新增action_p7_code_check**（核心改动，501行新增代码）：
   - C1要素完整性[BLOCK]: 必填7项字段非空校验
   - C2步骤-结果对应[分级]: ±1=INFO, ±2=WARNING, ≥3=BLOCK
   - C3 P0占比[WARNING]: ≤20%通过, 20-40%警告, >40%阻塞
   - C4冒烟占比[WARNING]: 按总数分档校验
   - C5步骤描述质量[WARNING]: 上下文感知正则，模糊词表过滤（误报率从34%降至4.7%）
   - C6期望结果质量[WARNING]: 负向模式正则，只匹配句末孤立模糊描述（误报率从66%降至16.8%）
   - C6.1前置条件三要素[BLOCK]: 账号/权限 + 数据构造 + 环境配置关键词检测
   - C7测试点覆盖率[BLOCK]: P5 active测试点必须100%覆盖
   - C7.1语义覆盖[WARNING]: 业务实体匹配（从需求提取固定术语，0%误报）
   - C8冒烟合规性[WARNING]: 冒烟用例priority应为P0/P1
   - C9伞形用例检测[WARNING]: 正则检测“同上/同理/与…一致”
   - 自动生成p7_output.json + p7_report.html + P7.pass.json(HMAC签名)
   - INFO级统计: 优先级分布、步骤唯一率、平均步骤长度、标题重复度
2. **step_run禁止P7**（与P5/P6一样）：
   - `step_run --step P7`直接拒绝，返回错误提示必须用p7_code_check
3. **step7_export去重**（移除P6质量重复校验）：
   - 移除smoke比例、P0比例、优先级分布校验（P7已覆盖）
   - 只保留用例数量底线(≥15) + P7 source校验(source="p7_code_check")
4. **p6_merge去重**（精确比例校验移至P7）：
   - smoke/P0改为底线校验(>0)，移除比例校验和步骤去重
   - 保留skeleton一致性、用例数量、测试点覆盖校验
5. **P7 prompt归档**: P7_quality_gate.md移至prompts/archive/目录
6. **SKILL.md段8更新**: P7指令从`step_run --step P7`改为`p7_code_check`
7. **P7 HTML报告自动生成**: 校验完成后自动生成p7_report.html，包含各Check状态、WARNING用例列表、统计指标

**集成测试**（V3.2.9云端190条用例验证）:
- Gate: PASS
- BLOCK: 4/4全通过（C1/C2/C6.1/C7）
- WARNING: 3/7触发（C4冒烟8.9%偏低、C8一条P2+smoke、C9三条伞形）
- 性能: 190条用例全量校验1.2ms，远低于3秒目标

**影响范围**:
- tools/orchestrator.py: 新增501行P7代码 + step_run/step7_export/p6_merge改造 (2700行→3164行)
- tools/export_excel.py: 版本号更新
- SKILL.md: 版本号+段8指令更新
- prompts/P7_quality_gate.md: 移至archive/

**兼容性**: ✅ 向后兼容。P0-P6流程不变，P7从“Agent审计”改为“代码校验”，Agent只需调用一条命令。

### v3.2.9 (2026-05-03)

**变更类型**: 代码层硬控全面升级 (基于V3.2.8云端测试失败分析+小析交叉评审)

**核心问题**: V3.2.8云端测试证明依赖prompt指令约束Agent行为不可靠。168条用例只有2种步骤模板，冷烟50%，P0=0，L3全部只展开2条。

**核心原则**: 代码硬控 > prompt指令。凡是仅靠Agent“自觉遵守”的方案都不可接受。

**修复内容**:
1. **priority/is_smoke代码预分配+锁定**（核心改动）：
   - prep_prompt为每个测试点生成case骨架（case_id/source_test_point/priority/is_smoke）
   - 冷烟分配策略：仅P0+主流程类别(main_flow/branch/integration)标冷烟
   - 骨架写入p6_batch_NNN_skeleton.json
   - save_batch时强制用代码原值覆盖Agent返回的priority/is_smoke，Agent无法篡改
2. **p6_save_batch硬校验**（从软校验升级）：
   - 逐测试点校验expected_case_count达标（不只看批次总数）
   - 冷烟比例≨25%（单批宽松）
   - P0比例≨25%
   - 步骤去重检测：唯一步骤<50%直接拒绝
   - 关键字段非空：title/steps/expected_results
   - 不达标直接拒绝保存，删除不合格文件
3. **p6_merge全局硬校验**（从warning升级为硬拒绝）：
   - 总用例数≥总预算(total_expected_cases)
   - 逐测试点展开数达标
   - 全局冷烟8%-20%
   - 全局P0>0且≨20%
   - 全局步骤去重≥50%
   - 不达标直接拒绝合并
4. **step7_export失败自动回流**（代码层实现）：
   - 失败时返回`auto_retry`状态+明确指令
   - 状态文件记录p6_retry_count
   - 最多重试2次，超过才报告用户
   - 禁止Agent向用户抛选择题

### v3.2.8 (2026-05-03)

**变更类型**: 质量校验加固 + 代码层优化 + complexity预算体系 + 交叉评审修复 (基于V3.2.7四路评审反馈+V3.2.8小析交叉评审)

**核心问题**: V3.2.7四路评审发现多个可优化点：P6展开数量全靠prompt猜、p6_save_batch无质量预检、P2门禁静态形同虚设、is_smoke格式多处重复判断、p6_merge无P5覆盖校验

**数据来源**: V3.2.7四路评审（小析有条件通过+6条建议、小猩有条件通过+3条建议、小执通过）

**修复内容**:
1. **P5 complexity标签体系**（小析核心建议，治本之策）：
   - p5_code_merge给每个测试点打`complexity`(L1/L2/L3)和`expected_case_count`(1/2/3)标签
   - 分级规则：根据测试点类型、风险标记、PCI标记、来源、描述长度综合评分
   - L1(简单:display/compatibility)≥1条, L2(常规:main_flow/branch)≥2条, L3(复杂:permission+risk/exception+pci)≥3条
   - P5输出新增coverage_summary.complexity_distribution和total_expected_cases
2. **P6 prep_prompt注入用例预算**（配合#1）：
   - 每个batch注入“本批次应生成至少N条”和每个测试点的展开预算
   - Agent不再猜展开数量，按预算执行
3. **P6动态门禁升级**（配合#1）：
   - quality_check和step7_export的P6最低用例数优先用P5的total_expected_cases
   - 其次回退到P5测试点数×1.5（V3.2.7兼容）
4. **p6_save_batch加软校验**（小猩V3.2.8建议）：
   - 保存批次时检查：用例数是否为0、is_smoke格式是否为布尔值、priority格式是否合规、title/steps是否为空
   - warning级别不阻塞保存，但尽早暴露质量问题
5. **P2 MIN_OUTPUT_COUNTS动态化**（小猩V3.2.8建议）：
   - `max(8, P1叶节点数×2)`替代静态底线8
6. **is_smoke格式统一**（小析V3.2.8建议）：
   - 新增`_is_smoke()`公共函数，替换orchestrator.py中4处重复判断
   - export_excel.py同步统一
7. **p6_merge加P5覆盖校验**（小析V3.2.8建议）：
   - 合并后检查每个P5测试点是否都被P6用例覆盖
8. **小析交叉评审修复——export_excel.py门禁同步**（小析评审必修#1）：
   - export_excel.py的P6质量门禁从写歭15升级为动态计算（与orchestrator完全一致）
   - 优先用P5的total_expected_cases，其次P5测试点×1.5，底线15
   - P0比例阈值从40%修正为20%（与orchestrator的P6_QUALITY_RULES一致）
9. **小析交叉评审修复——export_excel.py is_smoke统一**（小析评审必修#2）：
   - 新增`_is_smoke_check()`函数，与orchestrator的`_is_smoke()`完全一致
   - 替换export_excel.py质量检查中的内联判断
   - 消除双真源漂移风险
10. **小析交叉评审修复——P6 batch_points精简字段版**（小析评审中风险）：
   - batch_points不再用`json.dumps(full)[:5000]`截断
   - 改为精简字段版（只保留id/description/category/priority/risk_flag/pci_flag/complexity/expected_case_count）
   - 确保预算和测试点语义的绑定不会被截断削弱

### v3.2.7 (2026-05-02)

**变更类型**: 用例质量优化 + 效率提升 (基于V3.2.6云端测试JSON深度分析)

**核心问题**: V3.2.6云端测试成功完成但用例数量偏少（24条），P2每场景只生成1个测试点、P6每测试点只展开为1条用例；段7 batch文件命名试错浪费时间；段8 P0比例反复调整

**数据来源**: V3.2.6云端测试 task_20260502_204631 全量JSON产物深度分析

**修复内容**:
1. **P2 prompt强化最低展开数**（用例数量优化）：
   - 原规则：每个叶节点至少生成1个测试点
   - 新规则：每个叶节点至少生成**2个**测试点（1条正向+1条反向/异常/边界）
   - 质量门禁同步更新
2. **P6 prompt强化展开规则**（用例数量优化）：
   - 原规则：每个测试点展开为1~N个用例
   - 新规则：每个测试点必须展开为至少**2条**用例，并按测试点类型给出展开数量参考
   - prep_prompt注入规则同步更新
3. **P6质量门禁动态化**（代码层硬控）：
   - 原规则：MIN_OUTPUT_COUNTS["P6"]=15（静态）
   - 新规则：max(15, P5测试点数×1.5)（动态计算）
   - quality_check和step7_export同步使用动态阈值
4. **SKILL.md段7 batch文件命名格式明确**（效率优化）：
   - 明确标注`p6_batch_{N:03d}_agent_output.json`（3位零填充：001/002/003）
   - 避免Agent试错浪费时间
5. **P6 prep_prompt注入P0比例约束**（效率优化）：
   - 明确告知Agent "P0不得超过20%"，避免段8反复调整

### v3.2.6 (2026-05-02)

**变更类型**: 安全加固 + 结构校验 (基于V3.2.5四路评审反馈)

**核心问题**: Agent可通过直接写入gate pass文件、伪造p5/p6_output.json等方式绕过流程控制，step_run硬控只堵了一条路

**数据来源**: V3.2.5四路评审（小析发现5条未防护绕过路径，小猩提供HMAC方案，小文发现段6禁止列表不对称+CHANGELOG格式不一致）

**修复内容**:
1. **HMAC签名机制**（核心安全加固）：
   - 所有gate pass写入时加HMAC签名（基于orchestrator.py文件哈希派生密钥）
   - `check_gate()`验证时同时校验HMAC，签名不匹配则拒绝
   - 覆盖全部gate写入入口：onboarding/step_run/p5_code_merge/p6_merge/quality_check/truncation_guard
   - Agent无法获取密钥（依赖代码文件哈希），从根本上杠绝伪造gate pass
2. **P5结构特征校验**（辅助防线）：
   - step7_export导出前校验P5的merge_log必含from_p2/from_p3/from_p4
   - 确保P5由p5_code_merge生成，而非Agent自己写的
3. **P6批次结构校验**（辅助防线）：
   - step7_export导出前校验p6_batches目录存在且含batch文件
   - 确保P6由分批流程生成，而非Agent一次性写入
4. **SKILL.md段6禁止列表补全**（小文反馈）：
   - 段6禁止列表补充`write: p5_output.json`和`write: gates/P5.pass.json`，与段7对称
   - 段7禁止列表补充`write: gates/P6.pass.json`
5. **truncation_guard.py同步HMAC**：
   - truncation_guard写入gate pass时同样加HMAC签名
   - 密钥派生算法与orchestrator.py一致
6. **p6_merge/p6_save_batch/p6_batch_info加P5前置gate校验**（V3.2.6四路评审反馈）：
   - 小析发现：Agent可伪造batch文件后调p6_merge，借 orchestrator签发合法HMAC gate
   - 修复：p6_batch_info/p6_save_batch/p6_merge入口均加check_gate("P5")前置校验
   - 没有合法P5 gate pass就无法进入P6流程
7. **export_excel.py加HMAC验签**（V3.2.6四路评审反馈）：
   - 小析发现：Agent可直接调用export_excel.py绕过step7_export的全部门禁
   - 修复：export_excel.py的gate检查加HMAC验签+task_id校验，与orchestrator同等安全级别

### v3.2.5 (2026-05-01)

**变更类型**: bugfix + 流程硬控 (基于V3.2.4云端测试task_20260501_211514分析)

**核心问题**: Agent绕过p5_code_merge自己写P5、绕过P6分批流程一次性生成用例、P7 gate_result格式不兼容导致step7_export崩溃

**数据来源**: V3.2.4云端测试 task_20260501_211514 全量JSON产物分析

**修复内容**:
1. **P7 gate_result兼容性修复**（P1级Bug）：
   - Agent生成的P7 output中`gate_result`是字符串"PASSED"，但step7_export期望对象`{status:"PASS"}`
   - `"PASSED".get("status")` → AttributeError，导致导出崩溃
   - 修复：兼容字符串"PASS"/"PASSED"和对象{status:"PASS"}两种格式
2. **P5/P6 step_run代码层硬控**（流程强化）：
   - `step_run --step P5` 直接拒绝，返回错误提示必须用p5_code_merge
   - `step_run --step P6` 直接拒绝，返回错误提示必须用分批流程
   - 根因：V3.2.4云端测试中Agent绕过p5_code_merge自己写P5（risk_flagged=0），绕过分批流程一次性生成62条用例（前置条件全部相同、步骤平均2.6步、期望结果只有1条）
3. **SKILL.md段6/段7指令强化**：
   - 段6：明确禁止step_run/自己写P5/Python脚本生成，加代码层硬控说明
   - 段7：明确禁止step_run/直接写p6_output/Python脚本生成，加代码层硬控说明
   - 段落对照表加强说明

### v3.2.4 (2026-05-01)

**变更类型**: P0级bugfix (基于V3.2.3云端测试JSON产物深度分析)

**核心问题**: Excel导出除优先级/冒烟外全部空白，quality_check/p6_merge/step7_export读不到fields嵌套字段

**数据来源**: V3.2.3云端测试 task_20260501_073619 全量JSON产物分析

**修复内容**:
1. **新增`_get_case_field()`统一读取函数**（P0级Bug）：
   - P6用例数据结构为嵌套的`{id, source_test_point, fields: {19列字段}}`
   - 但orchestrator和export_excel全部用`case.get(field)`只读顶层，读不到fields子对象
   - 新增`_get_case_field(case, field)`: 先读顶层→再读fields子对象，兼容两种结构
   - 影响范围: orchestrator.py的quality_check/p6_merge/step7_export + export_excel.py的build_workbook
2. **export_excel.py列21列→P6 prompt 19列对齐**（P0级Bug）：
   - 旧版列21列定义与P6 prompt的19列字段映射表不一致
   - project/requirement/test_case_type/test_suite/screenshot这5个字段P6生成了但Excel不导出
   - executor/module/feature等7个字段Excel要导出但P6没生成
   - 现在严格按P6 prompt的19列字段映射表导出
3. **quality_check通过后自动创建gate文件**（P1级Bug）：
   - 旧版quality_check通过后不创建gate，Agent被迫手动创建P7.pass.json绕过门禁
   - 现在quality_check passed后自动写入gates/{step}.pass.json
4. **P0 prompt强调顶层必填字段**（P2级）：
   - P0 prompt的JSON模板缺少`quality_score`和`objective`顶层字段
   - 但orchestrator的P0_REQUIRED_FIELDS要求这两个字段必须在顶层
   - Agent第一次生成时漏了，校验失败后自行修补（“已添加缺失的顶层字段”）
   - 现在在JSON模板前加🔴强调标记，并在模板中明确展示这两个字段

### v3.2.3 (2026-04-30)

**变更类型**: bugfix + ux (基于V3.2.2云端测试反馈的流程强化)

**核心问题**: Agent把段4-6合并成一个“段4”，把段7(P6)当“段5”执行时错误调用step_run而非分批流程

**数据来源**: V3.2.2云端测试(minimax-m2.7) task_20260430_220353 全量JSON产物分析

**云端验证结果**: P0-P5全部通过，P5合并首次成功(39条测试点，risk_flagged=29，pci_flagged=24，P0卣18.4%)

**修复内容**:
1. **段落编号强制对照表**：在运行协议顶部加8段编号对照表，明确禁止合并段落
2. **段7 P6分批流程强化**：加🔴🔴🔴三重标记，明确Step 1/2/3三步分批流程，绝对禁止用step_run执行P6
3. **四路评审修复**（V3.2.2评审反馈）：
   - 边界安全前缀匹配：startswith(prefix)改为startswith(prefix+'-')，防止M01-F01误匹配M01-F010
   - P3全量匹配：feature级风险映射到该feature下所有scenario，不再break
   - P4全量匹配：blocked_scenarios全量匹配所有blocked的P2点，不再break
   - P0阈值收紧：40%→20%，推荐10-15%
   - schema JSON title更新：4个文件V3.2.0→V3.2.3

### v3.2.2 (2026-04-30)

**变更类型**: bugfix (基于V3.2.1云端实际JSON数据分析的深层修复)

**核心问题**: P5合并匹配逻辑与P3/P4实际字段不匹配，P2优先级分布失控

**数据来源**: V3.2.1云端测试(minimax-m2.7) task_20260430_194811 全量JSON产物分析

**修复内容**:
1. **P5合并匹配逻辑升级**（P0级Bug）：
   - P3匹配：新增`source_node`字段读取 + 前缀匹配（P3用feature级别M01-F01，P2用scenario级别M01-F01-S01）
   - P4匹配：新增`blocked_scenarios`数组精确匹配（P4的source字段写的是"P1"无用，但blocked_scenarios有正确的scenario ID）
   - 匹配策略：精确匹配→前缀匹配→新增独立点（三级降级）
   - 根因：V3.2.1的p5_code_merge只读source_scenario做精确匹配，但P3实际用source_node、P4实际source="P1"，导致26条全部未匹配
2. **P2优先级分布注入**（P0级）：
   - P2 prep_prompt注入优先级分布要求：P0≤40%、P1占主体40-60%、不允许全同一优先级
   - 根因：V3.2.1云端P2产出P0卣63.2%，远超40%上限，即使P5过了P6质量门禁也会拒绝
3. **SKILL.md 5段→8段残留清理**（已在V3.2.1修复）

### v3.2.1 (2026-04-30)

**变更类型**: bugfix + architecture (拆段优化 + 字段契约修复 + Onboarding分步强化)

**核心问题**: V3.2.0云端测试发现段4太重导致Agent崩溃、P5合并缺字段、Onboarding多项合并展示

**修复内容**:
1. **拆段5→8段**（解决段4太重导致Agent崩溃的根因）：
   - 段1: init+onboarding
   - 段2: step0+图片理解
   - 段3: P0+P1
   - 段4: P2（测试点）← 原段4拆出
   - 段5: P3+P4（风险+PCI）← 原段4拆出
   - 段6: P5（代码自动合并）← 原段4拆出
   - 段7: P6（用例生成）← 原段5拆出
   - 段8: P7+Excel ← 原段5拆出
2. **P5合并补齐priority/status字段**（解决truncation_guard L3校验失败）：
   - p5_code_merge合并后统一补齐priority（从priority_hint读取）和status（默认active）
   - P2 prep_prompt注入priority/status字段要求，让Agent生成时就带上
3. **P6 prep_prompt注入字段格式要求**：
   - is_smoke必须是boolean(true/false)
   - priority必须是P0/P1/P2/P3
   - testcases必须小写
4. **P7 prep_prompt强调gate_result字段名**：
   - 明确gate_result不是quality_check
5. **Onboarding分步交互强化**：
   - 每步加🔴强制标记
   - 必须等用户回复后才展示下一项
   - 不允许多项合并展示

### v3.2.0 (2026-04-29)

**变更类型**: architecture-fix (路线A止血版)

**核心问题**: Agent可绕过orchestrator直接写JSON/调用export_excel，质量门禁全部失效

**修复策略**: 不加指令，从代码层堵住绕过路径

**变更内容**:
1. **T2: export_excel.py加gate pass前置检查** — 即使Agent直接调用也必须有完整gate pass + P6质量校验
2. **T6: api_key密码缓存机制** — check_image_api成功后缓存到task目录，step0_8_prep自动读取，不再依赖Agent跨段落传递
3. **T4: 图片理解API串行→并行** — ThreadPoolExecutor(max_workers=3)，19张图从~570s→~190s
4. **T8: P5合并下沉代码层** — 新增p5_code_merge action，代码合并P2+P3+P4→P5，Agent不再参与合并
5. **T9: SKILL.md段落4更新** — P5改为调用p5_code_merge，Agent只需执行P2/P3/P4

### v3.1.0 (2026-04-29)

**变更类型**: fix + feature (系统性契约统一 + 图片理解升级)

**核心问题**: schema/prompt/orchestrator/实际产物四套口径并存，导致质量校验失效、字段读取失败、门禁被绕过

**修复策略**: 以云端实际JSON产物为真源，反向修 orchestrator代码

**变更内容**:
1. **REQUIRED_FIELDS统一到云端实际字段名**: P1 modules→feature_tree, P6删除statistics, P7 quality_check→gate_result
2. **MIN_OUTPUT_COUNTS多候选路径**: P0 blocks.operations|pages|business_rules, P1 feature_tree.modules|modules
3. **_get_nested()升级**: 支持多候选路径（用|分隔）
4. **step_run必需字段校验（代码硬控）**: 写入tmp后、guard前校验REQUIRED_FIELDS，缺失→删tmp+拒绝+明确错误
5. **step7_export内置P6质量硬门禁**: 导出前强制校验用例数≥15/冒烟8%-20%/P0≤40%/优先级分布 + P7 gate_result必须PASS
6. **prep_prompt注入P1/P7必需字段提醒**: 减少Agent猜测
7. **P6质量规则统一真源**: prep_prompt和quality_check完全一致，冒烟超限从 warning→issue(拒绝)
8. **Qwen VL升级为主引擎**: 语义理解能力远强CI，CI降为OCR辅助
9. **Qwen VL失败自动降级CI**: VL失败→CI(OCR+标签)→caption_only三级降级
10. **图片选图上限5→50**: 避免大量图片被跳过
11. **API超时30→120秒**: Qwen VL复杂图需要更长时间
12. **partial结果消费**: server返回partial时orchestrator保留有效内容，不再丢弃
13. **Onboarding 4B密码重试**: 3次重试+自动降级
14. **真实文件类型校验**: 图片头魔数检查
15. **统一失败语义**: ok/partial/error三态

**部署验证** (2026-04-29):
- 图片理解API 8项端到端验证全部通过
- Qwen VL语义理解质量远超CI
- 云端实际JSON数据验证全部通过

### v3.0.3 (2026-04-29)

**变更类型**: feature (图片理解API集成)

**变更内容**:
1. **图片理解API服务**：新增image_api_server/server.py，部署在腾讯云，调用数据万象OCR+图片标签
2. **step0_8_prep重构**：orchestrator直接调用API理解图片，不依赖Agent行为
3. **降级策略**：API未配置/失败→caption_only（用前后文推断），不回退Agent看图
4. **api_key安全**：Onboarding交互时用户输入密码，运行时传入，不写入任何文件
5. **task_meta脱敏**：preferences中image_api只保留url/model/timeout，api_key不落盘
6. **Onboarding检查4B**：新增图片理解API密码交互（输入密码/跳过+验证）
7. **预检+熔断**：API auth-check验证、401/403不重试、429限流熔断、连续3次失败熔断
8. **支持双引擎**：ci=数据万象(默认), qwen=通义千问VL(可选)
9. **新增接口**：/api/auth-check密码验证专用接口（health不鉴权问题修复）
10. **COS签名修复**：有效期0秒→300秒、参数排序字典序、ci-process全小写格式
11. **代码优化**：抽取_cos_sign()签名函数（消除6处重复）、UUID防并发冲突、删除SDK死代码
12. **空文件拦截**：0字节文件显式返回400 empty_file
13. **gunicorn配置优化**：timeout 60→120s、max-requests 500防内存泄漏

**部署验证**（2026-04-29 已通过）：
- /api/health ✅
- 正确/错误密码auth-check ✅
- 图片分析OCR+标签 ✅
- 空文件/错误密码拦截 ✅
- orchestrator check_image_api端到端 ✅

### v3.0.2 (2026-04-28)

**变更类型**: fix

**变更内容**:
1. **段间gate验证**：每段开头exec status确认上一段gate pass存在
2. **MEDIA文件发送**：step7_export返回media_instruction，SKILL.md要求输出MEDIA指令
3. **全链路gate校验**：step7_export检查onboarding/P0-P7全部9个gate pass

### v3.0.1 (2026-04-28)

**变更类型**: fix

**变更内容**:
1. **state持久化完善**：skill_dir/data_dir在init和onboarding中写入state；requirement_file/current_phase在step0中写入
2. **SKILL.md {SKILL_DIR}占位符修复**：改为ORCH变量自动发现，Agent不需要知道skill_dir路径
3. **restart_from action新增**：支持"从P{N}重新开始"，清除指定步骤及后续的gate pass和output
4. **find_latest_task安全加固**：查找范围从5个缩减为3个，减少多任务串扰风险
5. **CHANGELOG补全**：补充patch2/patch3/v3.0.1记录
6. **版本号统一为v3.0.1**

### v3.0.0 (2026-04-28)

**变更类型**: architecture-change (重大架构重构)

**变更内容**:
1. **orchestrator.py核心框架**：1150行Python脚本，14个action，代码控制全流程
2. **架构从指令驱动改为orchestrator驱动**：Agent不再自行决定流程，只负责执行prompt返回JSON
3. **文件写入完全由代码控制**：所有写入通过orchestrator→truncation_guard→gate pass，Agent无法绕过
4. **prep_prompt action**：为P0-P7自动准备完整prompt（含知识注入/上游产物/PX增强）
5. **P6分批全套**：p6_batch_info+p6_save_batch+p6_merge，代码控制分批和合并
6. **quality_check action**：最小产出数量/P0评分/P6冒烟比例+优先级分布，代码强制校验
7. **PX图片理解由orchestrator调度**：step0_8_prep价值选图+Agent逐张read+step0_8_save保存
8. **断点续跑由代码实现**：resume action自动扫描gate pass确定下一步
9. **SKILL.md重写**：从186行指令约束→120行orchestrator调用流程
10. **Agent交互协议**：新增orchestrator_protocol.md定义Agent↔orchestrator交互格式

**影响范围**:
- 新增 tools/orchestrator.py（核心）
- 新增 references/orchestrator_protocol.md
- SKILL.md 完全重写
- references/*.md 新增V3.0架构声明

**兼容性**: ⚠️ 重大架构变更，从指令驱动改为orchestrator驱动。现有Prompt/Schema/工具脚本全部保留兼容。

### v3.0.0-patch1 (2026-04-28)

**变更类型**: fix (四路评审修复)

**变更内容**:
1. **image_enhance.py A-2适配层**：新增_adapt_a2_format()函数，将A-2方案的results/understanding_mode/confidence(字符串)映射为旧格式的images/processing_status/classification.confidence(数值)，解决PX增强完全失效问题
2. **Onboarding门禁时序修复**：task_id创建从Step 0提前到Onboarding完成时，解决"task_id未创建→无法写onboarding.pass.json→无法进入Step 0"的时序悖论
3. **Step 0门禁检查增强**：从"扫描最新pass文件"改为"校验当前task_id的pass文件+task_id一致性验证"
4. **step0-px.md顶部OCR残留清理**：删除"OCR不可用时先装Tesseract"旧约束，替换为A-2方案说明
5. **skill_version更新**：step0-px.md中task_meta.json的skill_version从2.4.0更新为2.5.0
6. **状态行模板统一**：所有references中旧格式`✅ Step X(PX)完成!-`统一为新格式`✅ P{N}完成 | {指标} | 文件已保存`
7. **执行模型表述统一**：onboarding.md"零暂停"改为"自动推进"；step0-px.md"一气呵成"改为"按顺序自动推进"；step1-4.md/step5-7.md顶部新增"顶层协议优先"声明
8. **model_detect.py退出范围精确化**：从"退出主流程"改为"退出PX主流程（仍在P5分批模式中使用）"；引用文件清单新增退出标注

**影响范围**:
- tools/image_enhance.py: 新增A-2适配层
- references/onboarding.md: task_id提前创建+门禁时序修复+自动推进表述
- references/step0-px.md: 顶部OCR清理+skill_version+门禁检查增强+执行模型统一
- references/step1-4.md: 状态行统一+顶层协议优先声明
- references/step5-7.md: 状态行统一+顶层协议优先声明
- SKILL.md: 引用文件清单退出标注

### v2.5.0 (2026-04-28)

**变更类型**: fix + architecture-change

**变更内容**:
1. **需求载荷前置规则**：触发技能后必须先确认需求已就绪才启动Onboarding,未收到需求时仅输出固定等待话术,不输出步骤清单或能力介绍
2. **需求上下文判定规则**：支持本条消息含需求/含附件/明确引用近期需求三种就绪判定,禁止复用已完成task的旧需求
3. **Onboarding完成状态门禁**：Onboarding完成后写入onboarding.pass.json,Step 0前置检查该文件存在才允许进入主流程,从"指令约束"升级为"状态门禁"
4. **三阶段执行规则**：从两阶段(Onboarding+主流程)升级为三阶段(需求等待+Onboarding+主流程)
5. **对话输出硬约束**：从白名单改为计数硬约束(每步严格限1行),新增固定状态行格式和动作链模板
6. **PX图片理解A-2方案重构**：
   - 删除三级降级架构(model_detect→vision/OCR/context_only)
   - 改为Agent直接read图片,能看懂就用,看不懂就降级为caption+上下文
   - 图片选择改为价值优先(流程图>原型页>规则表>其他),最多5张
   - 新增三条件理解判定标准(识别类型+提取2个元素+1个测试价值点)
   - px_understand.json新增understanding_mode/confidence/evidence/selection_reason等字段
   - model_detect.py/image_understand.py/image_ocr.py退出主流程(保留文件不删除)
7. **P0内联必需字段**：在step1-4.md中直接内联P0顶层必需字段(quality_score/blocks/objective),减少Agent读schema的认知负担
8. **截断防护规则**：禁止单exec写完整P0-P7逻辑;禁止单轮回复连续推进超过一个Step;新增按gate pass精准恢复规则(支持P2/P3/P4复合步骤局部续跑)
9. **每步输出提醒**：所有Step指令开头新增"⚠️ 本步只输出1行状态"提醒

**影响范围**:
- SKILL.md: 运行协议重写(三阶段+需求前置+输出硬约束+截断防护+动作链模板)
- references/onboarding.md: 新增需求载荷前置规则+onboarding.pass.json门禁
- references/step0-px.md: Step 0新增onboarding门禁检查;Step 0.8整段重写为A-2方案
- references/step1-4.md: P0内联字段+各步输出提醒
- references/step5-7.md: 各步输出提醒

**兼容性**: ⚠️ 重大架构变更,PX从三级降级改为Agent直接视觉,Onboarding新增状态门禁


### v2.3.3 (2026-04-27)

**变更类型**: fix + architecture-change

**变更内容**:
1. **truncation_guard.py 四级截断检测脚本**：L1文件存在→L2 JSON有效→L3结构完整→L4内容完整，支持 `--auto-mv` 原子操作（校验通过自动mv+生成gate pass，失败自动rm tmp），Agent无法绕过
2. **thresholds.json L4阈值外部化配置**：P5输出≥max(15, P2×0.6)，P6输出≥max(10, P5×0.8)
3. **所有P0-P7统一改为tmp→truncation_guard→mv原子写入**：禁止heredoc直写正式文件，截断时最多损坏tmp不污染正式缓存
4. **gate pass链式依赖机制**：每步校验通过后自动生成gates/{step}.pass.json，下游步骤必须检查上游pass才能启动
5. **断点续跑改为"gate pass才能复用"**：不再只看"文件存在且非空"，必须pass存在且task_id一致
6. **P6降级产物隔离**：降级产物写入p6_output.degraded.json，不生成gate pass
7. **P5双模式执行**：新增model_detect.py output_capacity检测（high/medium/low三级），P5根据模型能力自动选择single/auto_batch/force_batch策略
8. **P5分批模式**：新增p5_prepare.py（按模块分组生成batch_context）+ P5a_batch_merge.md（批内合并子Prompt）+ Step 4c跨批汇总（脚本级ID去重+统计口径重定义）
9. **P5统计口径重定义**：merge_log区分batch_merge和cross_batch_dedup，coverage_summary新增source_covered_ratio
10. **Onboarding恢复交互模式**：PRD审查和L5上传恢复为用户可选择的开/跳过
11. **PX视觉模式修复**：支持视觉的模型必须走Agent直接调用路径（CLI无法提供model_caller），禁止CLI调用视觉模式
12. **OCR自动安装**：Tesseract不可用时先尝试自动安装（apt/yum/brew/apk），只有安装失败后才降级
13. **export_excel.py字典值映射修复**：优先级→Highest/High/Medium/Low，用例类型→正例/反例，测试类别→功能测试等
14. **P5严禁跳步强化**：明确禁止跳过P5/P6/P7直接生成Excel
15. **L4组合校验**：P5增加模块覆盖+优先级保留+merge_log一致性；P6增加P0全展开率；WARNING不阻塞流程
16. **revision简化版**：current_revision.json管理+断点续跑revision校验+bump-revision时清除下游gate pass+备份策略(.prev.json)
17. **SKILL.md指令冲突修复（根因级）**：对话输出白名单追加"Onboarding交互输出"豁免；元叙述硬禁令追加"Onboarding阶段例外"；全流程交互规则重构为两阶段制（Onboarding交互+主流程零暂停）；消除"零暂停"误杀Onboarding交互的根因
18. 专属触发词新增「xy测试用例生成」

**影响范围**:
- 新增 tools/truncation_guard.py（四级截断检测脚本）
- 新增 tools/thresholds.json（L4阈值配置）
- 新增 tools/p5_prepare.py（P5分批预处理脚本）
- 新增 prompts/P5a_batch_merge.md（P5批内合并子Prompt）
- 修改 tools/model_detect.py（新增output_capacity检测）
- SKILL.md: 所有Step写入方式改造、gate pass链式依赖、断点续跑升级、P5双模式执行、关键产物门禁重写
- export_excel.py: PRIORITY_MAP/TEST_CASE_TYPE_MAP/TEST_CATEGORY_MAP重写
- P6_testcase_generation.md: 字段映射对齐公司字典

**兼容性**: ⚠️ 重大架构变更，所有Step写入方式改变，新增gate pass机制

### v2.3.2 (2026-04-27)

**变更类型**: fix + behavior-change

**变更内容**:
1. **Onboarding 恢复交互模式**:PRD质量审查和L5知识库上传恢复为交互式询问,用户可选择「开启/跳过」和「上传/跳过」,之前的非交互模式导致能力丢失
2. **PX 图片理解视觉模式修复**:
   - 视觉模式(vision)禁止通过CLI调用(CLI无法提供model_caller,导致静默降级)
   - 支持视觉的模型(Doubao-Seed-2.0-pro等)必须走Agent直接调用路径:用read工具逐张读取图片,Agent用自己的视觉能力理解
   - 新增视觉模式Agent调用流程和VISION_QUEUE机制
3. **OCR引擎自动安装**:OCR不可用时先尝试自动安装Tesseract(含中文语言包),支持apt/yum/brew/apk四种包管理器,只有安装失败后才降级为纯文本模式
4. PX 跳过原因输出增强:跳过时必须附带具体原因
5. P5 截断自愈规则加强:明确禁止跳过P5/P6/P7直接生成Excel
6. export_excel.py 字典值映射修复:
   - 优先级:P0→Highest / P1→High / P2→Medium / P3→Low
   - 用例类型:正向类→「正例」,异常/边界/安全类→「反例」
   - 测试类别:功能→功能测试 / 性能→性能测试 / 安全→安全性测试 等
7. P6 Prompt 和 testcase_design_spec.md 字段映射说明同步更新
8. 专属触发词新增「xy测试用例生成」

**影响范围**:
- SKILL.md: Onboarding交互模式恢复、PX视觉模式调用方式变更、OCR自动安装、P5严禁跳步
- export_excel.py: PRIORITY_MAP / TEST_CASE_TYPE_MAP / TEST_CATEGORY_MAP 全部重写
- P6_testcase_generation.md: 字段映射说明对齐公司字典
- testcase_design_spec.md: 字段映射说明对齐公司字典

**兼容性**: ⚠️ 行为性变更,Onboarding从非交互恢复为交互,PX视觉模式调用方式变更

### v2.3.1 (2026-04-26)

**变更类型**: fix

**变更内容**:
1. model_detect.py 增加 provider 前缀剥离,修复 Doubao-Seed-2.0-pro 等带前缀模型ID被误判降级为OCR的问题
2. model_vision_capability.json 新增 doubao-seed-2.0-pro 等精确匹配条目
3. SKILL.md Step 3/4 JSON 写入改用 heredoc 方式,解决弱模型 tool calling 失败问题
4. SKILL.md Step 5 (P6) 大JSON采用 write→校验→mv 分步写入策略
5. SKILL.md 新增关键产物门禁:P0-P4 JSON写入后必须校验,失败则终止
6. SKILL.md 新增跳步分级规则:关键产物缺失必须终止,非关键步骤允许受控降级
7. SKILL.md 新增工具调用指导(弱模型适配)和禁止自建脚本规则
8. SKILL.md Onboarding 输出加"已自动继续"后缀,防止被误解为需用户回复
9. SKILL.md 检查1.5路径发现增加环境变量兜底和容器常见路径
10. model_detect.py 增加日志输出,便于排查模型能力检测结果
11. 门禁校验脚本assert改为if+sys.exit(1),防止python3 -O优化跳过
12. P6写入策略移除5KB阈值判断,统一使用write→校验→mv方式(避免LLM无法精确判断字节数)
13. P5提升为二级关键产物:写入失败必须终止,质量不达标允许降级
14. 跳步分级触发条件新增"JSON格式无效",与关键产物门禁一致
15. 路径发现失败时Markdown降级改为内联输出(不依赖export_markdown.py脚本)
16. P6校验失败时清理p6_raw.json临时文件(mv替代cp)
17. Onboarding非交互总则升级为全流程非交互规则(覆盖Onboarding→Step 0-7)
18. Step 7新增导出门禁,Excel/Markdown导出后强制校验文件存在且非空
19. P6降级操作具体化:最小可行用例集+degraded:true标记+警告输出
20. 工具调用指导vs门禁优先级明确:关键产物门禁>工具调用指导
21. 异常处理兆底规则与跳步分级规则措辞统一
22. 路径发现find命令加timeout 10和-print -quit优化

**影响范围**:
- model_detect.py: model_id 预处理逻辑变更,所有带 provider 前缀的模型ID受影响
- SKILL.md: Step 3/4/5 写入方式变更,Onboarding/路径发现/跳步规则增强

### v2.3.0 (2026-04-26)

**变更类型**: fix + behavior-change

**变更内容**:
1. Step 0.5 blocker 处理:从「等待用户强制跳过」改为「自动转 PCI 继续执行」,新增 `auto_skipped`/`skipped_blocker_count` 字段
2. Step 1 质量门禁:从「等待用户强制继续」改为「自动 CONDITIONAL_PASS 继续执行」,新增 `auto_forced`/`original_score` 字段,禁止写 `PASSED`
3. 新增「执行诚实规则」(全流程10条),解决 Excel 文件幻觉发送问题
4. 新增「跨步骤可测性分流规则」:可测/条件可测/不可测三分类
5. 新增「异常处理兆底规则」:执行错误→终止,不等用户
6. Step 7 输出增加文件生成验证和三级降级机制(Excel→Markdown→JSON)
7. MEDIA 指令强制全大写,独占一行,无前后空白
8. 新增 `export_markdown.py` 降级脚本,禁止 `cp .json → .md` 伪装
9. `export_excel.py` 增加 try-catch 兜底、空列表警告、写入异常捕获
10. P6 质量门禁冒烟占比从固定"10%~20%"改为分档规则(与生成规则/P7一致)
11. P6/P7 P0占比从强制"≤15%"改为建议"≤40%"(非强制,避免缩减必要用例)
12. P6 增加 blocked 测试点可测性分流(含6类核心缺失判定清单)
13. p6_output.schema.json 新增"条件验证" enum
14. P6 新增"禁止伞形用例规则",P7 新增 C9 伞形用例检测(WARNING级别)
15. SKILL.md blocked不可测落盘位置从 P5 的 blocked_test_points 改为 P6 的 statistics.risk_items

**影响范围**:
- 所有步骤的"等待用户"指令被非交互模式覆盖
- `p0_output.json` 新增可选字段 `auto_forced`/`original_score`(quality_check 对象内),status 新增 `CONDITIONAL_PASS` 枚举值
- `p0.5_output.json` 新增可选字段 `auto_skipped`/`skipped_blocker_count`(根级别)
- Step 7 行为变更:先验证后发送,支持降级输出

**兼容性**: ⚠️ 行为性变更,原有"等待用户确认"语义不再生效
