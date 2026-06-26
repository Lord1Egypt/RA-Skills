# Step 1-4 指令 (P0→P5)

> **🔴 V3.0 架构声明：本文件中的手动执行指令（如"Agent自行read/write/exec"）已被orchestrator.py替代。Agent不应直接按本文件的exec命令执行，而应通过orchestrator的action调用。本文件保留为prompt模板和知识注入的参考源，orchestrator的prep_prompt action会自动读取本文件中的prompt和知识路径。**

> **⚠️ 顶层协议优先**：本文件中"立即执行下一步""自动推进"表示逻辑顺序上的连续执行，不表示必须在同一个exec中完成。每个Step独立执行，遵循SKILL.md运行协议中的动作链模板。

---

## Gate Pass + 断点续跑规则（本文件内联）

## 断点续跑

每步开始前,检查 gate pass 是否存在且 task_id 一致:
- `{DATA_DIR}/gates/{step}.pass.json` 存在 且 `task_id` == 当前 `{task_id}` 且 `revision` == `current_revision.json` 中的 revision → **复用缓存结果**,输出 `「ℹ️ Step {N} 已有 gate pass(task_id+revision 一致),复用。」`
- gate pass 不存在 或 `task_id` 不匹配 或 `revision` 不一致 → 正常执行（即使 output.json 文件存在也重跑，因为无法确认其完整性）

> ⚠️ **重要区分**:gate pass 存在 + revision一致 = 该步骤已通过四级截断校验,数据可信。仅文件存在不代表数据完整（可能是半文件/脏文件）。

**revision管理机制**：
- `{DATA_DIR}/current_revision.json` 记录当前全局 revision 号
- 使用 `--bump-revision` 参数时，校验通过后自动 revision += 1，并清除当前Step及所有下游Step的旧gate pass
- 下游清除映射：P5→清除P5/P6/P7，P6→清除P6/P7，P7→清除P7，P2→清除P2/P3/P4/P5/P6/P7等

**备份策略**：auto-mv执行前，如果正式文件已存在，自动备份为 `{filename}.prev.json`（覆盖旧备份）

用户可发送「从 P{n} 重新开始」来强制从某步重新执行(删除该步及后续所有 gate pass 和 output 文件)。

---



---

### Step 0.5(可选):PRD 质量审查

**触发条件**:`preferences.json` 中 `prd_quality_review == true`

**执行指令**:

1. 读取 `{SKILL_DIR}/prompts/P0.5_prd_quality_review.md`
2. 构造 Prompt:将 `requirement_text` 填入模板
3. 调用 LLM
4. 解析输出 JSON(执行 JSON 解析兜底)
5. 写入:`{DATA_DIR}/p0.5_output.json`
6. **生成 PRD 质量审查报告 Excel**(云端用户必须通过文件获取完整报告):
   ```bash
   exec: python3 {实际SKILL_DIR}/tools/export_prd_review.py --input {DATA_DIR}/p0.5_output.json --output {DATA_DIR}/PRD质量审查报告_{task_id}.xlsx
   # {实际SKILL_DIR} 使用 Onboarding 检查 1.5 中自动发现的实际路径
   ```
   - 成功 → 执行步骤 7
   - 失败(openpyxl 不可用等)→ 降级为纯对话文字输出,不阻塞流程
7. **发送 Excel 文件给用户**:
   ```
   MEDIA:{DATA_DIR}/PRD质量审查报告_{task_id}.xlsx
   ```
8. **在对话中输出审查摘要**(简洁版,方便快速阅读):
   ```
   📋 PRD 质量审查完成
   综合评分:{overall_score} 分({grade} {grade_label})
   🔴 阻塞问题:{blocking_count} 条  🟡 警告:{warning_count} 条  i️ 建议:{info_count} 条
   完整报告已通过 Excel 文件发送,请查收。
   ```
9. 检查结果并执行流程控制:
   - 存在 `severity == "blocking"` 的问题 → **暂停,等待用户选择**:
     - 输出: `🔴 PRD存在 {N} 个阻塞问题,请选择: [1] 查看问题清单并中断修改 [2] 自动转为PCI继续生成用例`
     - 用户选[1] → 输出完整问题清单(含问题描述+位置+建议),输出 `❌ PRD质量不达标,流程中断。修改PRD后重新发起即可。`,终止流程
     - 用户选[2] → 自动将 blocker 转为 PCI 条目写入 `p0.5_output.json`,在根级别添加 `"auto_skipped": true`(boolean)和 `"skipped_blocker_count": {N}`(integer),输出 `⚠️ P0.5: {N} 个 blocker 已转为 PCI,继续执行`,立即继续
   - 仅 `warning` 级别 → 追加提示 `「⚠️ PRD 存在 {warning_count} 处警告,建议补充后再生成用例,或直接继续。」` → 继续执行
   - 无问题(A/B级)→ 追加提示 `「✅ PRD 质量良好,继续生成测试用例。」` → 继续执行

**未开启时**:跳过此步,直接进入 Step 1。

---

### Step 1:P0 需求结构化

> 📌 [Step 1→2 备忘] 写文件 → 一行状态 → 立即下一步

**禁止事项**(本步高风险误操作):
- 禁止在对话中输出 P0 的 JSON 结构体
- 禁止在质量评分 ≥ 0.7 时暂停等待用户确认
- 禁止输出"是否继续"等等待语句

**⚠️ 本步只输出1行状态,不输出中间过程。**

**P0必需顶层字段（内联,避免读schema开销）**:
- `quality_score`: number (0~1.0)
- `blocks`: object (含 modules/business_rules/unknowns 等子字段)
- `objective`: string (需求目标描述)
以 schema 文件为权威定义,此处仅列最小必需字段减少认知负担。

**内部动作**(不输出到对话):

1. 读取 Prompt:`{SKILL_DIR}/prompts/P0_requirement_structuring.md`
2. 注入知识(token 预算 ≤ 2000):
   - 必注入:`{SKILL_DIR}/knowledge/industry/{domain}.md`
   - 必注入:`{SKILL_DIR}/knowledge/methodology/design_methods.md`
   - 可选(L5):检查 `{SKILL_DIR}/user_knowledge/project/` 下是否有文件,有则读取内容最相关的 1~2 个文件(按文件名关键词匹配),无则跳过
3. 构造完整 Prompt:
   ```
   [P0 Prompt 模板内容]

   ---
   ## 注入知识

   ### 行业知识({domain})
   {industry knowledge content}

   ### 测试设计方法论
   {design_methods content}

   ### 项目知识(如有)
   {L5 content or "无"}

   ### PX 图片理解增强(如有)
   如果 {DATA_DIR}/px_enhance.json 存在,读取其中 step_subsets.P0 字段,注入以下内容:
   - derived_features:图片中提取的功能点(作为需求补充)
   - derived_test_points:图片中提取的测试点(作为需求补充)
   - degradation_notice:降级说明(如有)
   - 纯文本模式下:注入 image_context(图注 + 前后文)作为需求补充
   注入增量控制 ≤ 1500 token。无 px_enhance.json 则跳过。

   i️ T3-02 降级说明使用指引:
   - 如果 degradation_notice 字段非空,将其作为 P0 输出的一部分保留,传递到后续步骤
   - 降级说明中包含按图片类型细化的缺失信息提示,帮助用户判断哪些图片需要人工审阅
   - OCR 模式:区分降级类型(流程图/原型图/状态图)和中度提取类型(规则表/接口截图)
   - 纯文本模式:所有图类型均未解析,仅提供元数据

   ---
   ## 输入需求

   {requirement_text}
   ```
4. 调用 LLM
5. 执行 JSON 解析兜底(见下方统一逻辑)
6. 检查质量评分:
   - 解析结果中 `quality_score < 0.7` → **不阻塞,不等待用户**。自动将 `quality_check.status` 设为 `"CONDITIONAL_PASS"`(禁止写 `"PASSED"`,避免弱化质量信号),添加 `"auto_forced": true`(类型:boolean)和 `"original_score": {实际分值}`(类型:number,0~1.0),将 `missing_items` 转为 PCI 条目追加到 `blocks.unknowns` 中,输出一行警告 `⚠️ Step 1(P0): 质量评分 {score} < 0.7,已自动继续,缺失项已转 PCI`,然后立即继续
   - `quality_score >= 0.7` → 继续
7. 写入临时文件 `{DATA_DIR}/p0_output.tmp.json`(使用 write 工具或 exec heredoc)
8. 执行截断校验+原子替换:
   ```bash
   exec: python3 {实际SKILL_DIR}/tools/truncation_guard.py \
     --file {DATA_DIR}/p0_output.tmp.json \
     --step P0 --data-dir {DATA_DIR} --task-id {task_id} --revision 1 --auto-mv
   ```
   - `GUARD_PASS:P0:数量` → 继续; `TRUNCATION_DETECTED` → 终止流程

**对话输出**(仅此一行):
`✅ P0完成 | 评分{score} | 文件已保存`

**⚡ 自动推进**:完成后立即执行 Step 2,无需任何确认。

---

### Step 2:P1 功能点树

**⚠️ 本步只输出1行状态,不输出中间过程。**生成

> 📌 [Step 2→3 备忘] 写文件 → 一行状态 → 立即下一步

**禁止事项**(本步高风险误操作):
- 禁止在对话中输出 P1 的 JSON 结构体
- 禁止输出"是否继续"等等待语句
- 禁止跳过 Step 3 直接进入后续步骤

**内部动作**(不输出到对话):

1. 读取 Prompt:`{SKILL_DIR}/prompts/P1_feature_tree_generation.md`
2. 读取上一步输出:`{DATA_DIR}/p0_output.json`
3. 构造 Prompt:将 P0 输出填入 P1 模板
4. 调用 LLM
5. 执行 JSON 解析兜底
6. 写入临时文件 `{DATA_DIR}/p1_output.tmp.json`
7. 执行截断校验+原子替换:
   ```bash
   exec: python3 {实际SKILL_DIR}/tools/truncation_guard.py \
     --file {DATA_DIR}/p1_output.tmp.json \
     --step P1 --data-dir {DATA_DIR} --task-id {task_id} --revision 1 --auto-mv
   ```

**对话输出**(仅此一行):
`✅ P1完成 | {N}模块 | 文件已保存`

**⚡ 自动推进**:完成后立即执行 Step 3,无需任何确认。

---

### Step 3:P2/P3/P4 三路

**⚠️ 本步只输出1行状态(含P2/P3/P4各自完成指标),不输出中间过程。**分析(一步完成,中间不停顿)

> 📌 [Step 3→4 备忘] 写文件 → 一行状态 → 立即下一步

**禁止事项**(本步高风险误操作):
- 禁止在 3a/3b/3c 之间输出任何内容
- 禁止在 3a/3b/3c 之间等待用户
- 禁止展示任何中间 JSON

**前置验证**:
```bash
exec: cat {DATA_DIR}/p1_output.json
```
> 如果文件不存在或为空,停止执行,提示用户先完成 Step 2(P1)。

**内部动作**(不输出到对话):

**3a - P2 测试点草案**:
> 断点续跑:如果 `{DATA_DIR}/gates/P2.pass.json` 存在且 task_id == {task_id} 且 revision == current_revision.json 中的 revision,跳过 3a,直接执行 3b。
1. 读取 Prompt:`{SKILL_DIR}/prompts/P2_test_point_draft.md`
2. 注入知识(token 预算 ≤ 2000):
   - 必注入:`{SKILL_DIR}/knowledge/methodology/api_test_standard.md`
   - 必注入:`{SKILL_DIR}/knowledge/methodology/boundary_rules.md`
3. 读取:`{DATA_DIR}/p1_output.json`
4. 构造 Prompt:
   ```
   [P2 Prompt 模板内容]

   ---
   ## 注入知识

   ### 接口测试标准
   {api_test_standard content}

   ### 边界值规则
   {boundary_rules content}

   ### PX 图片测试点增强(如有)
   如果 {DATA_DIR}/px_enhance.json 存在,读取 step_subsets.P2.derived_test_points 注入。
   注入增量控制 ≤ 1500 token。

   ---
   ## 输入:功能点树

   {p1_output JSON}
   ```
5. 调用 LLM
6. 执行 JSON 解析兜底
7. 构造完整JSON后,先写入tmp文件:
   ```bash
   exec: cat << 'JSONEOF' > {DATA_DIR}/p2_output.tmp.json
   {LLM生成的完整JSON内容}
   JSONEOF
   ```
8. 截断校验+原子替换:
   ```bash
   exec: python3 {实际SKILL_DIR}/tools/truncation_guard.py \
     --file {DATA_DIR}/p2_output.tmp.json \
     --step P2 --data-dir {DATA_DIR} --task-id {task_id} --revision 1 --auto-mv
   ```
   > `GUARD_PASS:P2:数量` → 继续执行3b; `TRUNCATION_DETECTED` → 终止流程
9. 不输出任何内容,立即执行 3b

**3b - P3 风险点识别**:
> 断点续跑:如果 `{DATA_DIR}/gates/P3.pass.json` 存在且 task_id == {task_id} 且 revision == current_revision.json 中的 revision,跳过 3b,直接执行 3c。
1. 读取 Prompt:`{SKILL_DIR}/prompts/P3_risk_identification.md`
2. 注入知识(token 预算 ≤ 2000):
   - 必注入:`{SKILL_DIR}/knowledge/industry/{domain}.md`(风险规则部分)
   - PX 增强(如有):读取 {DATA_DIR}/px_enhance.json 中 step_subsets.P3.derived_risks 注入,增量 ≤ 1500 token
3. 读取:`{DATA_DIR}/p1_output.json`
4. 构造 Prompt:将知识和 P1 输出填入 P3 模板
5. 调用 LLM
6. 执行 JSON 解析兜底
7. 构造完整JSON后,先写入tmp文件:
   ```bash
   exec: cat << 'JSONEOF' > {DATA_DIR}/p3_output.tmp.json
   {LLM生成的完整JSON内容}
   JSONEOF
   ```
8. 截断校验+原子替换:
   ```bash
   exec: python3 {实际SKILL_DIR}/tools/truncation_guard.py \
     --file {DATA_DIR}/p3_output.tmp.json \
     --step P3 --data-dir {DATA_DIR} --task-id {task_id} --revision 1 --auto-mv
   ```
   > `GUARD_PASS:P3:数量` → 继续执行3c; `TRUNCATION_DETECTED` → 终止流程
9. 不输出任何内容,立即执行 3c

**3c - P4 待确认问题识别**:
> 断点续跑:如果 `{DATA_DIR}/gates/P4.pass.json` 存在且 task_id == {task_id} 且 revision == current_revision.json 中的 revision,跳过 3c,直接执行 3d。
1. 读取 Prompt:`{SKILL_DIR}/prompts/P4_pci_identification.md`
2. 读取:`{DATA_DIR}/p1_output.json`
3. 构造 Prompt:将 P1 输出填入 P4 模板
   - PX 增强(如有):读取 {DATA_DIR}/px_enhance.json 中 step_subsets.P4.derived_questions 注入,增量 ≤ 1500 token
4. 调用 LLM
5. 执行 JSON 解析兜底
6. 构造完整JSON后,先写入tmp文件:
   ```bash
   exec: cat << 'JSONEOF' > {DATA_DIR}/p4_output.tmp.json
   {LLM生成的完整JSON内容}
   JSONEOF
   ```
7. 截断校验+原子替换:
   ```bash
   exec: python3 {实际SKILL_DIR}/tools/truncation_guard.py \
     --file {DATA_DIR}/p4_output.tmp.json \
     --step P4 --data-dir {DATA_DIR} --task-id {task_id} --revision 1 --auto-mv
   ```
   > `GUARD_PASS:P4:数量` → 继续执行3d; `TRUNCATION_DETECTED` → 终止流程
8. 不输出任何内容,立即执行 3d

**3d - 验证(仅验证,不生成对话输出)**:
```bash
exec: python3 -c "
import os, sys, json
data_dir = '{DATA_DIR}'
task_id = '{task_id}'
for step in ['P2', 'P3', 'P4']:
    gp = os.path.join(data_dir, 'gates', f'{step}.pass.json')
    if not os.path.exists(gp):
        print(f'FAIL:{step}:gate pass 缺失'); sys.exit(1)
    d = json.load(open(gp))
    if d.get('task_id') != task_id:
        print(f'FAIL:{step}:task_id 不匹配'); sys.exit(1)
# 统计数量（从gate pass summary读取）
p2_gp = json.load(open(os.path.join(data_dir, 'gates', 'P2.pass.json')))
p3_gp = json.load(open(os.path.join(data_dir, 'gates', 'P3.pass.json')))
p4_gp = json.load(open(os.path.join(data_dir, 'gates', 'P4.pass.json')))
tp = p2_gp.get('summary', {}).get('test_points_count', 0)
risk = p3_gp.get('summary', {}).get('risk_points_count', 0)
pci = p4_gp.get('summary', {}).get('pci_list_count', 0)
print(f'PASS:{tp}:{risk}:{pci}')
"
```
> exec 返回 `PASS:{tp}:{risk}:{pci}` → 输出对话输出行,然后立即执行 Step 4
> exec 返回 `FAIL:{step}:{reason}` → 输出:`❌ Step 3 子任务 {step} gate pass 缺失({reason}),流程终止。用户可发送「重试Step3」从失败处恢复。`

**对话输出**(仅此一行):
`✅ P2/P3/P4完成 | 测试点{tp}条/风险{risk}条/PCI{pci}条 | 文件已保存`

**⚡ 自动推进**:验证通过后立即执行 Step 4,无需任何确认。

---

### Step 4:P5 测试点合并

**⚠️ 本步只输出1行状态,不输出中间过程。**与优先级

> 📌 [Step 4→5 备忘] 写文件 → 一行状态 → 立即下一步
> 📌 [Step 4 截断自愈] 若本步输出被截断、文件半写入、JSON 不完整或关键字段缺失,必须自动补全/重跑,不得等待用户追问
> 🔴 **[严禁跳步]** P5 是二级关键产物,即使输出被截断也**绝对禁止跳过P5/P6/P7直接生成Excel**。截断时必须重跑P5,重跑失败则终止流程。跳过P5/P6/P7直接出Excel = 交付失败,产出仅10-15条低质量用例。

**禁止事项**(本步高风险误操作):
- 禁止在对话中输出 P5 的 JSON 结构体
- 禁止输出"是否继续"等等待语句
- 禁止缺少 p2/p3/p4 任一输入时继续执行

**前置验证（gate pass 链式依赖）**:
```bash
exec: python3 -c "
import os, sys, json
data_dir = '{DATA_DIR}'
task_id = '{task_id}'
def check_pass(step, hard=True):
    gp = os.path.join(data_dir, 'gates', f'{step}.pass.json')
    if not os.path.exists(gp):
        if hard: print(f'GATE_BLOCKED:{step}:gate pass 缺失，前置步骤未完成'); sys.exit(1)
        else: print(f'GATE_WARN:{step}:gate pass 缺失（增强依赖，不阻塞）'); return
    d = json.load(open(gp))
    if d.get('task_id') != task_id:
        if hard: print(f'GATE_BLOCKED:{step}:task_id 不匹配，需重跑'); sys.exit(1)
        else: print(f'GATE_WARN:{step}:task_id 不匹配')
check_pass('P2', hard=True)   # 硬依赖
check_pass('P3', hard=False)  # 增强依赖，缺失时警告不阻塞
check_pass('P4', hard=False)  # 增强依赖，缺失时警告不阻塞
print('GATE_OK')
"
```

**内部动作**(不输出到对话):

**P5执行模式判断**：
```bash
exec: python3 {实际SKILL_DIR}/tools/model_detect.py "{model_id}" --output-capacity
```
根据返回的 `p5_strategy` 决定执行模式：
- **single** → 执行下方「单次模式」
- **auto_batch** → 当P2测试点总数>20时走「分批模式」（Step 4a→4b→4c），否则走单次模式
- **force_batch** → 强制走「分批模式」

---

**单次模式（single）**：

1. 读取 Prompt:`{SKILL_DIR}/prompts/P5_test_point_merge.md`
2. 注入知识(token 预算 ≤ 2000):
   - 必注入:`{SKILL_DIR}/knowledge/methodology/automation_scoring.md`
3. 读取三路输入:
   - `{DATA_DIR}/p2_output.json`
   - `{DATA_DIR}/p3_output.json`
   - `{DATA_DIR}/p4_output.json`
4. 构造 Prompt（将知识和三路输入填入P5模板）
5. 调用 LLM
6. 执行 JSON 解析兜底
7. 先写入tmp文件:
   ```bash
   exec: cat << 'JSONEOF' > {DATA_DIR}/p5_output.tmp.json
   {LLM生成的完整JSON内容}
   JSONEOF
   ```
8. 截断校验+原子替换(L4启用,会检查数量阈值):
   ```bash
   exec: python3 {实际SKILL_DIR}/tools/truncation_guard.py \
     --file {DATA_DIR}/p5_output.tmp.json \
     --step P5 --data-dir {DATA_DIR} --task-id {task_id} --revision 1 --auto-mv
   ```
9. 若校验失败:自动重跑一次(切换为分批模式);仍失败则报错终止

---

**分批模式（auto_batch / force_batch）**：

#### Step 4a：P5 分批预处理
```bash
exec: python3 {实际SKILL_DIR}/tools/p5_prepare.py \
  --data-dir {DATA_DIR} \
  --output-dir {DATA_DIR}/p5_batches \
  --batch-size 12
```
- 校验 `prepare_summary.json` 中 `total_test_points` 与 P2 输出测试点数一致

#### Step 4b：批内合并（逐批执行）
对 `p5_batches/` 下每个 `batch_{N}_context.json`：
1. 读取 batch_context 内容
2. 调用 `prompts/P5a_batch_merge.md`，传入 `{{batch_context}}`
3. 将输出写入 `{DATA_DIR}/p5_batches/batch_{N}_output.tmp.json`
4. 截断校验+原子替换:
   ```bash
   exec: python3 {实际SKILL_DIR}/tools/truncation_guard.py \
     --file {DATA_DIR}/p5_batches/batch_{N}_output.tmp.json \
     --step P5 --data-dir {DATA_DIR} --task-id {task_id} --revision 1 --auto-mv
   ```
5. 校验失败时重试当前批次(最多2次)
6. 每批完成后输出进度:`已合并 X/N 批(第 Y 批完成)...`

#### Step 4c：跨批汇总（脚本级，不需要LLM）
```bash
exec: python3 -c "
import json, os, sys
data_dir = '{DATA_DIR}'
batches_dir = os.path.join(data_dir, 'p5_batches')
summary = json.load(open(os.path.join(batches_dir, 'prepare_summary.json')))

all_tps = []
batch_dedup_total = 0
for b in summary['batches']:
    bp = os.path.join(batches_dir, f'batch_{b[\"batch_id\"]}_output.json')
    if not os.path.exists(bp):
        print(f'FAIL:batch_{b[\"batch_id\"]} output missing'); sys.exit(1)
    bd = json.load(open(bp))
    all_tps.extend(bd.get('test_points', []))
    batch_dedup_total += bd.get('batch_dedup_count', 0)

# 脚本级ID去重(安全兆底)
seen_ids = set()
merged = []
cross_dedup = 0
for tp in all_tps:
    if tp['id'] not in seen_ids:
        seen_ids.add(tp['id'])
        merged.append(tp)
    else:
        cross_dedup += 1

# 统计
active = sum(1 for t in merged if t.get('status') != 'blocked')
blocked = len(merged) - active
by_pri = {}
for t in merged:
    p = t.get('priority', 'P2')
    by_pri[p] = by_pri.get(p, 0) + 1

# P2覆盖率
p2_data = json.load(open(os.path.join(data_dir, 'p2_output.json')))
p2_ids = {tp['id'] for tp in p2_data.get('test_points', [])}
covered = len(p2_ids & seen_ids)
source_ratio = covered / len(p2_ids) if p2_ids else 1.0

output = {
    'test_points': merged,
    'merge_log': {
        'total_input': {'draft': len(p2_ids), 'risk': 0, 'pci': 0},
        'deduplicated': {
            'batch_merge': batch_dedup_total,
            'cross_batch_dedup': cross_dedup,
            'total': batch_dedup_total + cross_dedup
        },
        'final_count': len(merged)
    },
    'quality_warnings': [],
    'coverage_summary': {
        'total': len(merged),
        'active': active,
        'blocked': blocked,
        'by_priority': by_pri,
        'p0_ratio': round(by_pri.get('P0', 0) / len(merged), 3) if merged else 0,
        'source_covered_ratio': round(source_ratio, 3)
    }
}
with open(os.path.join(data_dir, 'p5_output.tmp.json'), 'w') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)
print(f'MERGE_OK:{len(merged)}')
"
```
然后截断校验+原子替换:
```bash
exec: python3 {实际SKILL_DIR}/tools/truncation_guard.py \
  --file {DATA_DIR}/p5_output.tmp.json \
  --step P5 --data-dir {DATA_DIR} --task-id {task_id} --revision 1 --auto-mv
```

---

**对话输出**(仅此一行):
`✅ P5完成 | 测试点{N}条 | 文件已保存`

**⚡ 自动推进**:完成后立即执行 Step 5,无需任何确认。

---

