> 🔴 元规则：禁止伪造结果 | 禁止连段执行(本段结束必须⏸️) | 禁止抛选择题
> 🔴 V3.5.2禁止行为：禁止直接写gate/output/state文件 | 禁止import orchestrator | 禁止跳过orchestrator
> 📋 来源：SKILL.md 段落3 | 版本 V4.9.0

## 前置依赖
- 段落2已完成：需求已解析，图片模式已确定
- Gate: step0 gate pass必须存在
- PRD审查模式：从onboarding配置获取

---

**🔴 段内规则**: P0和P1在段落3内部连续执行（不需逐个等用户确认），段落3的确认点在P2自动完成后（见下方⏸️标记）。段落边界才需要用户回复「继续」。

用户确认后执行:

**🔴 段间验证(必须先执行):**
```
exec: python3 "$ORCH" --action status
```
确认step0的gate pass存在(说明段落2已完成,P0/P1尚未执行是正常的)。如不存在,必须重新执行段落2。

**P0执行（一shot生成+校验）:**
```
exec: python3 "$ORCH" --action prep_prompt --step P0
→ 获得 prompt_file 路径
read {prompt_file} → 用推理能力生成JSON
write {DATA_DIR}/p0_agent_output.json → JSON结果
exec: python3 "$ORCH" --action step_run --step P0
→ orchestrator校验+truncation_guard+gate pass
```

**P1执行（V4.8.9分批流程——骨架→逐feature填充→合并）:**

**Step 1: 生成P1骨架（module+feature结构，不含scenario）**
```
exec: python3 "$ORCH" --action prep_prompt --step P1 --mode skeleton
→ 获得骨架prompt
→ 生成module→feature树，每个feature的children留空[]
write {DATA_DIR}/p1_skeleton_agent_output.json
exec: python3 "$ORCH" --action p1_skeleton_save
→ 输出feature列表（如: M01-F01, M01-F02, M02-F01 ...）
```

**Step 2: 逐feature填充scenarios（循环每个feature_id）**
```
🔴 P1分批循环进度规则（强制执行）:
  - 每完成5个feature,必须输出进度: 🔄 P1进度: {已完成}/{总数} features ({完成率}%)
  - 总feature数>20时,每10个feature汇报一次
  - 单个feature超5分钟无响应→跳过该feature,记录到remarks
  - 累计失败≥3个feature→停止循环,执行p1_code_merge(用已完成的部分)

对每个feature_id重复:
  exec: python3 "$ORCH" --action prep_prompt --step P1 --feature-id {feature_id}
  → 获得该feature的专属prompt（含P0关联规则）
  → 生成2-5个scenario JSON
  write {DATA_DIR}/p1_feature_{feature_id}_agent_output.json
  exec: python3 "$ORCH" --action p1_save_feature --feature-id {feature_id}
  → 校验scenario数量≥2、含positive类型

所有feature完成后:
exec: python3 "$ORCH" --action p1_code_merge
→ 代码自动拼装骨架+所有feature→完整feature_tree→gate pass
```

**V3.5.4: P0执行完成后追加quality_check(PRD审查增强):**
```
🔴🔴🔴 重要:如果用户开启了PRD审查,P0的JSON输出必须包含 blocks_markdown 和 issues 两个字段!
这是代码层硬校验,缺少任何一个字段,step_run将直接返回 prd_review_validation_failed 错误并拒绝。

当 prd_quality_review=True 时,P0的JSON输出必须包含:
  - blocks_markdown: string  ← 需求结构化Markdown,必须输出,不得省略
  - issues: array            ← 问题清单数组,无问题时输出空数组[]

P0的step_run成功后,立即执行:
  exec: python3 "$ORCH" --action quality_check --step P0
  → 如果返回中包含 prd_review_enabled: true,则必须展示以下内容:

  📋 **需求结构化结果**
  {blocks_markdown内容,原样输出,保持Markdown格式}

  **展示示例**(供Agent参考,实际输出以blocks_markdown内容为准):
  ```
  ## 模块1:月亮晒榜单优化(PC端)

  ### F01 有效机构户排名优化
  **输入/输出**
  - 输入:机构户数据、统计周期(月度) ✅
  - 输出:排名列表(增量排名替代原排名) ✅

  **业务规则**
  - 增量排名 = 本期新增机构户数排序 ✅
  - ⚠️ 未明确增量排名排序规则(降序?平局如何处理?)

  **约束条件**
  - 统计周期:自然月 ✅
  - ⚠️ 未定义"有效机构户"的判定标准

  **场景**
  - 正常展示、无新增机构户、多机构并列

  ---

  ### F02 重点机构业务优化
  **输入/输出**
  - 输入:重点机构业务数据 ✅
  - 输出:删除"目标完成率(%)"列 ✅

  **业务规则**
  - 删除操作:前端隐藏该列 ✅
  - ⚠️ 未说明存量数据是否保留(物理删除 or 逻辑隐藏)

  **状态流转**
  - 删除前 → 确认提示 → 删除后刷新列表 ✅

  ---

  ### F05-F07 福建区域新增三张表
  **输入/输出**
  - 输入:金种子/商机沙盘/海交综服数据 ✅
  - 输出:三张新增tab,各含11个统计字段 ✅

  **业务规则**
  - 11个统计字段:⚠️ 未定义字段名称、计算公式、数据来源

  **约束条件**
  - 数值字段:⚠️ 未定义数据类型(整数/小数)、单位、精度
  - 必填项:⚠️ 未明确哪些字段必填

  **角色权限**
  - 福建区域用户可见 ✅
  - ⚠️ 其他区域用户是否可见未说明
  ```

  ⚠️ **问题清单**(共{prd_issues数量}项)
  | 严重度 | 位置 | 类型 | 问题 | 建议 |
  |--------|------|------|------|------|
  {遍历prd_issues数组渲染表格}

  📊 **质量评分:{quality_score}**

  → 如果 quality_check 返回中包含 prd_review_report_path 字段:
    发送文件: 📄 PRD审查报告已生成,点击下载:{prd_review_report_path}
    (使用相对路径或绝对路径均可,确保用户可点击下载)

  → 如果 quality_check 返回 quality_failed(评分<0.5):
    输出: ❌ 需求质量不合格,流程中断。请根据问题清单修改需求后重新提交。
    停止执行(不继续P1)
  → 如果 quality_check 返回 ok:
    展示内容后自动继续P1,不等待用户
  → 如果返回中不包含 prd_review_enabled(用户跳过了PRD审查):
    仍必须展示质量评分摘要:
    ```
    📊 P0需求质量评分: {quality_score} (阈值≥0.7为✅通过, <0.5为❌不合格)
    📋 待确认问题: N条(见下方问题清单,若无则显示"无")
    ```
    → 如果 quality_score < 0.5: 输出❌不合格提示,流程中断
    → 如果 quality_score >= 0.5: 直接继续P1,不等待用户
```

**📊 P0需求质量评分展示（P0+quality_check完成后立即展示,然后自动继续P1）:**
→ 从 quality_check stdout 读取 quality_score 和结构化数据
→ 如果 quality_score < 0.5: ❌ 流程中断,停止
→ 如果 quality_score >= 0.5: 展示评分后自动继续P1

📋 **需求结构化结果**（prd_quality_review=False时展示精简版）:
- **需求目标**: {objective,空时显示"未提供"}
- **质量评分**: {quality_score} (≥0.7✅合格 / <0.5❌不合格)
- **业务对象**: {N}条
- **核心操作**: {N}条
- **业务规则**: {N}条
- **测试关注点**: {N}条

📋 **待确认问题**: {blocks.unknowns为空则"✅ 无",否则列出阻塞(🚨)和非阻塞(⚠️)问题}

---

**P1分批循环中的进度汇报（每5个feature必须汇报一次）:**
→ 格式: `🔄 P1进度: {已完成数}/{总数} features ({完成率}%) | 耗时: {已用分钟}min`
→ 如果总feature数>20,每10个feature汇报一次

---

P0+P1+quality_check全部完成后输出:
```
📊 P0需求质量评分: X.XX | P1模块:N个/功能点:M个
```
→ **注意:此处不输出"段落3完成"**,因为P2尚未执行。段落3的确认点在P2自动完成后。

**🔴🔴🔴 执行P2前自检(先确认以下已完成的项,再发P2命令):**
□ 质量评分已在回复中展示（格式: `📊 P0需求质量评分: X.XX`，≥0.7✅ / <0.5❌）
□ 如果开启了PRD审查且存在 prd_review_report.md → 已发送MEDIA
□ cloud_review 推送结果已在回复中展示（如已配置API密码;无cloud_review字段则跳过本项）
→ **以上3项全部确认后，立即执行P2 auto。任一项未完成则先补做，不允许跳过直接跑P2。**
→ **🔴 这是P2的前置条件，先自检，后P2。**

**⚡ 自检全部通过，立即自动执行P2（无需用户确认）：**

**段间验证:** `exec: python3 "$ORCH" --action status`(确认P0+P1 gate pass存在)

**P2由代码自动生成,Agent执行以下命令即可:**
```
exec: python3 "$ORCH" --action p2_code_generate
```
→ 代码自动读P1 feature_tree → 规则引擎生成测试点 → gate pass
→ 🔴 **"P2自动"仅指执行P2不需要用户确认，不等于段落3→段落4自动过渡。段落边界必须等待用户回复「继续」。**

---

**🔴🔴🔴 P2执行成功后——段落3收尾输出(必须逐项执行,禁止跳过任何一项):**

步骤① 解析P2 stdout的JSON,提取 `__must_emit__` 字段:
  → 从exec返回的stdout中解析JSON对象（exec输出可能混有stderr，提取第一个完整JSON块）
  → 方法:用正则匹配 `\{[^{}]*"__must_emit__"[^{}]*\}` 定位含__must_emit__的JSON对象
  → 如果stdout混有其他文本，先 `re.search(r'\{[\s\S]*\}', exec_stdout)` 提取完整JSON
  → 读取 `__must_emit__` 字段的值（一个多行字符串）
  → 如果 `__must_emit__` 字段不存在 → ❌ P2异常(报告未生成),停止,排查原因

步骤② 发送报告文件给用户（双通道，两个通道都必须执行，缺一不可）:

  🔴 第一步 — 通道A（输出MEDIA路径）:
    将 `__must_emit__` 字段内容**原样复制**到回复中(独占一段)

  🔴 第二步 — 通道B（读取并展示报告内容，无条件强制）:
    ```
    exec: cat {data_dir}/p0p1_report.md | head -40
    ```
    → 将exec输出结果展示给用户
    → 告知用户：📁 完整报告: {data_dir}/p0p1_report.md

  ⚠️ 必须两个通道都执行，只输出路径不给文件内容 = 违规

步骤③ 检查data目录是否还有其他待发送文件:
  → 如果开启了PRD审查:检查 prd_review_report.md 是否存在,存在则 `MEDIA:{data_dir}/prd_review_report.md`
  → 从P2 stdout JSON解析 cloud_review 字段(如有):
    - `cloud_review.pushed == True` → 输出: 🔗 需求理解已推送到评审工具: {cloud_review.review_url}
    - `cloud_review.pushed == False` → 输出: ⚠️ 需求推送失败({cloud_review.message}),不影响后续流程

步骤④ 输出段落3完成确认:
  [自动] P2测试点生成完成 | 测试点:X条(自动生成)

→ 🔴 **以上步骤①-④全部完成后,段落3才算结束。缺任一步骤,段落3不完整。禁止跳过进入段落4。**

⏸️ **段落3完成。必须等待用户回复「继续」后，才能进入段落4。禁止自动跨段。**
---
🔴🔴🔴 本段执行完毕 → ⏸️ 停止 → 等待用户回复「继续」
🔴 P2 stdout中的 __must_emit__ 字段必须已原样复制到回复
🔴 禁止继续读取 rules/paragraph_4.md 或 SKILL.md 后续内容
