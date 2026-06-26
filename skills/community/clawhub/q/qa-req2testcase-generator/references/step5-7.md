# Step 5-7 指令 (P6→P7→导出)

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

### Step 5:P6 用例展开

**⚠️ 本步输出:开始1行+每批进度1行+完成1行。不输出JSON或中间分析。**

> 📌 [Step 5→6 备忘] 分批生成,每批只输出进度行,不输出 JSON,完成后立即下一步

**禁止事项**(本步高风险误操作):
- 禁止在对话中输出任何用例 JSON 或数组
- 禁止在批次之间等待用户
- 禁止在 p6_output.json 写入失败时自行生成 Excel

**前置校验(gate pass 链式依赖)**:
```bash
exec: python3 -c "
import os, sys, json
data_dir = '{DATA_DIR}'
task_id = '{task_id}'
gp = os.path.join(data_dir, 'gates', 'P5.pass.json')
if not os.path.exists(gp):
    print('GATE_BLOCKED:P5:gate pass 缺失，P5未通过截断校验，无法启动P6'); sys.exit(1)
d = json.load(open(gp))
if d.get('task_id') != task_id:
    print('GATE_BLOCKED:P5:task_id 不匹配，需重跑P5'); sys.exit(1)
print('GATE_OK:P5已通过截断校验，可启动P6')
"
```
> 如果 P5 gate pass 不存在 → **必须停止执行**，不得继续生成用例。

**内部动作**(不输出到对话):

1. 读取 Prompt:`{SKILL_DIR}/prompts/P6_testcase_generation.md`
2. 注入知识(token 预算 ≤ 4000,本步放宽):
   - 必注入:`{SKILL_DIR}/knowledge/company_standards/testcase_design_spec.md`
   - 必注入:缺陷模式注入(见下方「缺陷模式注入逻辑」)
   - 可选(L6):检查 `{SKILL_DIR}/user_knowledge/experience/` 下是否有文件,有则读取最相关的 1~3 个作为 few-shot 示例注入,无则跳过
3. 读取:`{DATA_DIR}/p5_output.json`
4. 构造 Prompt:
   ```
   [P6 Prompt 模板内容]

   ---
   ## 注入知识

   ### 测试用例设计细则(公司标准)
   {testcase_design_spec content}

   ### 历史缺陷模式({domain},前 {max_defect_patterns} 条)
   {defect patterns text - 见下方转换格式}

   ### 经验库 few-shot(如有)
   {L6 content or "无"}

   ---
   ## 输入:带优先级测试点

   {p5_output JSON}
   ```
5. **开始时输出进度提示**:`⏳ 正在生成测试用例,预计需要 1-2 分钟,请稍候...`
6. **分批生成(强制)**:将 P5 测试点按每批 ≤ 10 个分批调用 LLM,每批完成后:
   - 输出进度:`已生成 X/N 条用例(第 Y 批完成)...`
   - 将本批结果追加到内存列表,并**立即落盘**到 `{DATA_DIR}/p6_batches/batch_{Y}.json`
   - 同步写入 `{DATA_DIR}/p6_progress.json`,记录 `completed_batches / total_batches / completed_case_count / failed_batches`
   - 合并规则:用例编号按模块前缀编号(如 TC-模块A-001),避免重复
7. **批次级恢复**:如中途中断或重试,仅补跑缺失/失败的 batch 文件,已完成批次直接复用,不得整轮重生
8. 所有批次完成后,合并批次结果统一写入临时文件 `{DATA_DIR}/p6_output.tmp.json`
   - **P6统一使用write→truncation_guard方式写入**(禁止heredoc,P6 JSON通常较大且结构复杂):
     1. 使用 `write` 工具写入临时文件 `{DATA_DIR}/p6_output.tmp.json`
     2. 截断校验+原子替换(L4启用,会检查用例数量阈值):
        ```bash
        exec: python3 {实际SKILL_DIR}/tools/truncation_guard.py \
          --file {DATA_DIR}/p6_output.tmp.json \
          --step P6 --data-dir {DATA_DIR} --task-id {task_id} --revision 1 --auto-mv
        ```
        > `GUARD_PASS:P6:数量` → 继续(tmp已自动mv为p6_output.json,gate pass已生成)
        > `TRUNCATION_DETECTED` → tmp已自动删除,按降级策略处理
9. 执行 JSON 解析兜底
10. **字段完整性校验(强制)**:`testcases[].fields` 中必须包含公司 19 列全部 key:
   `project, case_type, case_id, requirement, priority, title, menu_path, preconditions, steps, expected_results, is_smoke, creator, assignee, test_case_type, test_category, status, screenshot, test_suite, remarks`
   - 允许空字符串的字段:`assignee, status, screenshot`
   - 其余字段不得缺 key;如无值,也必须显式输出空字符串,不得省略字段
11. 若任一 case 缺少上述 key,或仅凭猜测/手工臆造 P5 active 数据生成 P6 输出 → 视为失败,必须回到真实 P5 结果重生,不得带病进入 Step 6/7

**对话输出**:
- 开始时:`⏳ 正在生成测试用例,预计需要 1-2 分钟,请稍候...`
- 每批完成:`已生成 X/N 条用例(第 Y 批完成)...`
- 全部完成:`✅ P6完成 | 用例{N}条 | 文件已保存`

**⚡ 自动推进**:完成后立即执行 Step 6,无需任何确认。

#### 缺陷模式注入逻辑

```
1. 读取 {SKILL_DIR}/knowledge/defect_patterns/defects_by_domain/{domain}.txt
2. 逐行解析 JSONL,每行是一个 JSON 对象
3. 按 severity 字段排序(high > medium > low)
4. 取前 N 条(N = preferences.max_defect_patterns,默认 20)
5. 每条转换为以下文本格式:

   ### 缺陷模式 [严重度: {severity}]
   - 类别: {category}
   - 模式描述: {description}
   - 测试建议: {test_suggestion}

6. 拼接所有条目,控制总量在 2000 tokens 以内
7. 如果 JSONL 文件不存在或为空,输出 "无历史缺陷模式" 并继续(不阻塞)
```

---

### Step 6:P7 质量自检

**⚠️ 本步只输出1行状态,不输出中间过程。**(支持自动重试)

> 📌 [Step 6→7 备忘] 写文件 → 一行状态 → 立即下一步

**禁止事项**(本步高风险误操作):
- 禁止在对话中输出质量自检的 JSON 报告
- 禁止在自检通过时暂停等待用户确认
- 禁止在重试次数未用尽时直接结束流程

**内部动作**(不输出到对话):

1. P7质量校验由代码自动执行(`p7_code_check`)，**不需要Agent构造Prompt，不需要调用LLM**
2. 代码自动读取 `p5_output.json` + `p6_output.json`，执行 C1-C9 + C7.1 共11项校验
3. 自动生成 `p7_output.json` + `p7_report.html` + `P7.pass.json`
4. 如果校验失败（FAILED），代码自动返回失败原因，Agent需输出失败信息并提示用户
5. ❌ **禁止用 `step_run --step P7`**，会被代码层拒绝
6. ❌ **禁止Agent自己生成P7的JSON或调用LLM**

**对话输出**(仅此一行):
`✅ P7完成 | 自检{PASSED/FAILED} | 文件已保存`

#### T2-06:置信度相关门禁规则(对齐方案 §10 + §20.6)

P7 质量自检时,需额外检查图片置信度相关项:

1. **中置信度图片关注**:检查 `_confidence_tier == "medium"` 的图片,其 derived_* 已入链路但需确认:
   - 对应的 derived_test_points 是否可执行(非泛泛描述)
   - 对应的 derived_risks 是否已标注置信度提醒
   - 如发现中置信度图片的 derived_* 质量不达标,在 P7 报告中标记为 warning(不阻断)

2. **低置信度图片确认**:检查 `_confidence_tier == "low"` 的图片,确认其 derived_* 未入链路:
   - 如发现低置信度图片的 derived_* 意外入链路,标记为 error

3. **ocr_degraded 视为已解析**(§20.6 边界注释):
   - P7 门禁检查"高价值图片是否已解析"时,ocr_degraded 视为已解析(已尝试处理且产出了结果)
   - 但 derived_* 是否入链路仍受置信度规则约束(< 0.5 不入链路)
   - 举例:一张 flowchart 在 OCR 模式下置信度 0.45,extraction_mode 为 ocr_degraded。P7 门禁"高价值图片是否已解析"→ 通过;但 derived_test_points 因置信度 < 0.5 不入链路

**⚡ 自动推进**:自检通过后立即执行 Step 7;自检失败且重试次数 < 2 时,自动回退 P6 重新生成,不暂停等待用户。

#### P7失败后自动回流P6重试(当P7校验FAILED且p7_retry_count < 2)

```
1. 从 P7 输出中提取不通过项列表 p7_failed_issues
2. p7_retry_count += 1
3. 输出:「🔄 质量自检未通过(第 {p7_retry_count} 次重试),正在将问题反馈给 P6 重新生成...」
4. 重新执行 Step 5(P6 用例展开),但在 P6 Prompt 末尾追加以下内容:

   ---
   ## 质量自检反馈(请修复以下问题后重新生成)
   {p7_failed_issues}

5. 优先复用 `{DATA_DIR}/p6_batches/` 中已通过校验的批次,仅重生成 `fix_actions` 命中的 case 所在批次或缺失批次
6. P6 重新生成完成后,先更新对应 batch 文件,再重新合并写入新的 `{DATA_DIR}/p6_output.json`
7. 回到 Step 6 第 2 步,重新执行 P7 质量自检
```

> **注意**:重试时仅重新执行 Step 5(P6)和 Step 6(P7),不影响其他步骤的缓存结果。重试时跳过断点续跑的缓存检查(因为需要强制重新生成)。

---

### Step 7:输出结果

> 📌 [Step 7 备忘] 这是唯一合法结束点,Excel 只能通过脚本生成

**禁止事项**(本步最高风险误操作):
- **禁止任何情况下绕过 `export_excel.py` 脚本,自行生成 Excel 内容**
- 禁止 `p6_output.json` 校验失败时继续执行
- 禁止输出中间用例数据、JSON 片段到对话
- 禁止修改公司 19 列 Excel 模板字段格式

**内部动作**(不输出到对话):

1. 前置校验（gate pass 全链路检查 + p6_output 完整性）:
   ```bash
   exec: python3 -c "
   import os, sys, json
   data_dir = '{DATA_DIR}'
   task_id = '{task_id}'
   # 全链路 gate pass 检查
   for step in ['P5', 'P6', 'P7']:
       gp = os.path.join(data_dir, 'gates', f'{step}.pass.json')
       if not os.path.exists(gp):
           print(f'GATE_BLOCKED:{step}:gate pass 缺失，全链路未完成，禁止导出'); sys.exit(1)
       d = json.load(open(gp))
       if d.get('task_id') != task_id:
           print(f'GATE_BLOCKED:{step}:task_id 不匹配'); sys.exit(1)
   # P6 降级检测
   degraded = os.path.exists(os.path.join(data_dir, 'p6_output.degraded.json'))
   if degraded:
       print('DEGRADED:P6为降级产物，导出时将标注降级草稿')
   else:
       # 正式产物：校验 p6_output.json
       path = os.path.join(data_dir, 'p6_output.json')
       if not os.path.exists(path) or os.path.getsize(path) == 0:
           print('FAIL:p6_output.json 缺失或为空'); sys.exit(1)
   print('GATE_OK')
   "
   ```
   > 返回 GATE_BLOCKED → **停止执行**，P5/P6/P7任一未通过截断校验都不得导出
   > 返回 DEGRADED → 允许导出，但必须标注"降级草稿"

2. 读取 `{DATA_DIR}/p6_output.json`
3. 统计用例数量 `case_count`
4. 生成 Markdown 格式用例摘要(前 5 条预览):
   ```markdown
   ## 测试用例生成结果

   任务ID:{task_id}
   业务域:{domain}
   用例总数:{case_count}
   质量自检:{p7_status}

   ### 用例预览(前 5 条)

   | 编号 | 用例简述 | 优先级 | 冒烟 |
   |------|---------|--------|------|
   | {case_id} | {title} | {priority} | {is_smoke} |
   ...
   ```
5. 生成 Excel(必须通过脚本):

   **文件名规则**:`测试用例_[需求名]_[任务ID].xlsx`
   - `[需求名]`:取需求文档标题中的系统名+版本号+核心功能关键词,最多20字,去除标点和空格。示例:`集团CRM_XCV1.0.12_兴光闪耀总榜`
   - `[任务ID]`:即 `{task_id}`,格式 `task_YYYYMMDD_HHMMSS`
   - 完整示例:`测试用例_集团CRM_XCV1.0.12_兴光闪耀总榜_task_20260422_121901.xlsx`

   ```bash
   exec: python3 {实际SKILL_DIR}/tools/export_excel.py --input {DATA_DIR}/p6_output.json --output {DATA_DIR}/测试用例_[需求名]_{task_id}.xlsx
   # 注意:{实际SKILL_DIR} 使用检查 1.5 中自动发现的实际路径,不得使用字面量 {SKILL_DIR}
   ```
   > 脚本失败 → **按统一导出失败策略处理,不得自行生成 Excel**

   **统一导出失败策略**:
   - 第 1 次失败:自动重试 1 次同一脚本命令
   - 重试成功:继续发送 Excel,流程正常结束
   - 重试仍失败:调用 `export_markdown.py` 生成真正的 Markdown 用例文件(禁止用 `cp .json → .md` 伪装):
     ```bash
     exec: python3 {实际SKILL_DIR}/tools/export_markdown.py --input {DATA_DIR}/p6_output.json --output {DATA_DIR}/测试用例_[需求名]_{task_id}.md
     ```
   - Markdown 生成成功:用 MEDIA 发送 .md 文件,完成消息说明「⚠️ Excel 生成失败,已发送 Markdown 格式用例文件」
   - Markdown 也失败且存在 `p6_output.json`:直接发送 JSON 原文件(保留 .json 后缀,不要伪装为 .md),完成消息说明「⚠️ Excel 生成失败,已发送 JSON 格式原始用例数据」
   - `p6_output.json` 缺失/为空:停止流程,提示用户发送"重新生成"重试
   - **任何情况下都不得绕过 `export_excel.py` 手工拼 Excel**

   **Excel 输出约束**:
   - 只输出用例数据行,**禁止在 Excel 末尾追加统计行**(如"用例总数""P0用例数"等汇总信息)
   - 统计信息只在对话中文字输出,不写入 Excel

6. **Step 7 导出门禁(强制)**:Excel/Markdown 导出后必须校验:
   ```bash
   exec: python3 -c "import os,sys; p='{DATA_DIR}/测试用例_[需求名]_{task_id}.xlsx'; sys.exit(0) if (os.path.exists(p) and os.path.getsize(p)>0) else (print(f'EXPORT_FAIL:文件不存在或为空: {p}'),sys.exit(1))"
   ```
   导出门禁失败后完整降级链(与统一导出失败策略一致):
   - EXPORT_FAIL → 重试export_excel.py一次
   - 仍失败 → 降级调用export_markdown.py生成Markdown文件
   - Markdown也失败 → 内联输出Markdown格式用例到对话(格式:表头含19列字段名、每个用例一行、末尾附统计)
   - 内联也失败 → 发送p6_output.json原文件
   - 全部失败 → 报错终止

7. 发送文件给用户:
   ```
   MEDIA:{DATA_DIR}/测试用例_[需求名]_{task_id}.xlsx
   ```
   > 重要:必须将 `{DATA_DIR}` 替换为实际路径(如 `/root/.openclaw/workspace/data/task_20260424_140500`),将 `[需求名]` 替换为实际需求名,将 `{task_id}` 替换为实际任务ID。不得输出占位符字面量。
   > **MEDIA 必须全大写**--OpenClaw 解析大小写敏感,`media:` 或 `Media:` 不会触发文件发送。行前后不能有任何空白字符,不能被 markdown 代码块包裹。
   > 示例:`MEDIA:/root/.openclaw/workspace/data/task_20260424_140500/测试用例_集团CRM_V1.0.14_兴光闪耀优化_task_20260424_140500.xlsx`

7. 输出 L6 学习邀请(固定追加,不可省略):
   ```
   💡 L6 经验学习:如果你对这批用例进行了评审或修改,可以把修改后的 Excel 发给我,我会对比原版和修改版,提取改动规律(如哪类场景被补充、哪类描述被优化),存入 L6 经验库,下次生成同类需求时自动参考,持续提升用例质量。
   回复「学习」并附上修改后的 Excel → 触发经验沉淀
   ```
   收到用户回复「学习」并附文件后:
   - 读取用户上传的 Excel 文件
   - 与 `{DATA_DIR}/p6_output.json` 对比,提取新增/修改/删除的用例及改动原因
   - 将经验摘要写入 `{SKILL_DIR}/user_knowledge/experience/{task_id}_experience.json`,格式:
     ```json
     {
       "task_id": "{task_id}",
       "domain": "{domain}",
       "requirement_summary": "需求简述",
       "lessons": [
         {"type": "补充场景", "description": "补充了文件大小边界值用例"},
         {"type": "优化描述", "description": "期望结果改为具体可观测的状态描述"}
       ],
       "created_at": "ISO8601"
     }
     ```
   - 输出「✅ 已学习 X 条经验,存入 L6 经验库。下次生成同类需求时将自动参考。」

**对话输出**:
`✅ 测试用例已生成,共 {case_count} 条。Excel 文件已发送。`


---

## JSON 解析兜底逻辑(每步必用)

每次调用 LLM 获得响应后,按以下顺序解析:

```
1. 尝试直接 JSON.parse(response)
   → 成功:使用解析结果

2. 失败 → 正则提取:
   - 尝试匹配 ```json\n...\n``` 代码块中的内容
   - 尝试匹配响应中第一个 { ... } 或 [ ... ] 块(贪婪匹配最外层)
   → 对提取内容再次 JSON.parse
   → 成功:使用解析结果

3. 仍失败 → 重试一次:
   - 在原 Prompt 末尾追加:「重要:只输出合法 JSON,不要包含任何其他文字、注释或 markdown 标记。」
   - 重新调用 LLM
   - 对响应重复步骤 1~2

4. 重试仍失败 → 报错:
   - 输出:「❌ Step {N} JSON 解析失败,已重试 1 次。原始响应已保存到 {DATA_DIR}/p{n}_raw_response.txt,供用户排查。」
   - 将原始响应写入 {DATA_DIR}/p{n}_raw_response.txt
   - 终止流程
```

---

