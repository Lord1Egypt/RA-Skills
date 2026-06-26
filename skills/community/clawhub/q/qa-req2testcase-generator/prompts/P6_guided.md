---
id: P6_guided
name: 弱模型引导式用例生成
version: "4.8.13"
last_updated: "2026-05-22"
model_tier: LOW
---

# 测试用例设计任务

你是一名券商测试用例设计师。基于以下设计引导，为每个测试点生成测试用例。

---

## ❗ 用例预算（必须遵守，违反会被拒绝）

引导卡中的 `expected_case_count` 表示该测试点**至少需要**生成的用例数量：
- `complexity: L1`（简单）→ 至少 1 条
- `complexity: L2`（常规）→ 至少 2 条（1条正向 + 1条异常/边界）
- `complexity: L3`（复杂）→ 至少 3 条（1条正向 + 1条异常 + 1条边界）

**你必须为每个测试点生成至少 expected_case_count 条用例**。
输出 JSON 的 testcases 数组中，每个测试点必须有 expected_case_count 条对应的用例。

---

## 📋 上下文数据（必须先读取）

生成用例前，先读取本批次的完整上下文文件：
`{data_dir}/p6_batches/batch_{batch_index:03d}_context.json`

该文件包含：操作骨架 step_expected_pairs、字段清单 field_checklist、UI 元素 ui_elements、风险标记等关键信息。
**用例中的具体步骤、字段名、UI元素名必须基于 context 文件中的真实数据，不允许凭空编造。**

---

## 设计引导

```json
{{guides}}
```

---

## 格式规范（必须包含以下全部 19 个字段）

每条用例必须输出以下字段，写入 JSON 数组。**缺失任一字段将导致保存失败。**

| 字段 | 说明 | 默认值/来源 |
|------|------|------------|
| case_id | 用例ID | TC-{test_point_id}-{序号}，序号从001开始 |
| priority | 优先级 | skeleton 原值（不改动） |
| title | 用例标题 | 基于 p5_description 概括（≤30字） |
| preconditions | 前置条件 | p5_precondition + "1. 已登录XX系统" |
| steps | 操作步骤 | step_pattern 组织，每步≥15字，用 key_ui 具体名称 |
| expected_results | 预期结果 | expected_pattern 描述可观测现象，每步1条 |
| is_smoke | 是否冒烟 | skeleton 原值（不改动） |
| source_test_point | 来源测试点 | test_point_id（不改动） |
| test_category | 测试类别 | category 原值（main_flow/branch/boundary/exception） |
| project | 项目名 | `""`（留空，Excel 导出时自动填充） |
| case_type | 用例类型 | `"测试用例"` |
| requirement | 需求 | `""`（留空，Excel 导出时自动填充） |
| menu_path | 用例菜单 | 从 context 文件 field_checklist 提取页面路径，无则 `""` |
| creator | 创建者 | `"AI自动生成"` |
| assignee | 经办人 | `""`（留空） |
| test_case_type | 测试类型 | `""`（留空） |
| status | 执行状态 | `"待执行"` |
| screenshot | 截图 | `""`（留空） |
| test_suite | 测试用例集 | 模块名（从 context 文件提取），无则 `""` |
| remarks | 备注 | `""`（留空，如有特殊说明则填写） |

### 步骤规则

1. 每条步骤必须 ≥15 字
2. 步骤中**禁止使用**：`{{step_must_avoid_sample}}`
3. 格式：`{序号}. {动作词}「{UI元素名}」{操作内容}`

### 期望规则

1. 期望中**禁止使用**：`{{expected_must_avoid_sample}}`
2. 格式：`{序号}. {可观测现象}`（必须引用具体值/状态/文案）
3. 🔴 步骤数 = 期望结果数

---

## 示范（注意：一个测试点生成了 2 条用例，每条包含全部 19 个字段）

**🔴 保存时文件名必须为** `p6_batch_{batch_index:03d}_agent_output.json`
**（缺少 _agent_output 后缀会导致 p6_save_batch 报"不含JSON"错误）**

```json
{
  "case_id": "TC-TP-001-001",
  "priority": "P0",
  "title": "新增债券投顾分润规则-正向",
  "preconditions": "1. 已登录CRM系统\n2. 进入债券投顾页面",
  "steps": "1. 使用有权限账号登录CRM系统，进入首页→营销管理→协同分润→债券投顾页面\n2. 点击「新增」按钮\n3. 在「产品名称」下拉框中选择「债券A」\n4. 在「分润比例(%)」输入框中输入「30」\n5. 点击「保存」按钮",
  "expected_results": "1. 页面跳转到债券投顾列表页，URL 包含 /bond-advisory\n2. 弹出「新增分润规则」弹窗\n3. 「产品名称」下拉框展开，显示可用产品列表\n4. 「分润比例(%)」输入框显示「30」\n5. 弹窗关闭，页面顶部出现绿色 Toast 提示「保存成功」，列表新增 1 条记录",
  "is_smoke": true,
  "source_test_point": "TP-001",
  "test_category": "main_flow",
  "project": "",
  "case_type": "测试用例",
  "requirement": "",
  "menu_path": "营销管理→协同分润→债券投顾",
  "creator": "AI自动生成",
  "assignee": "",
  "test_case_type": "",
  "status": "待执行",
  "screenshot": "",
  "test_suite": "债券投顾分润",
  "remarks": ""
}
{
  "case_id": "TC-TP-001-002",
  "priority": "P1",
  "title": "新增债券投顾分润规则-比例超限",
  "preconditions": "1. 已登录CRM系统\n2. 进入债券投顾页面",
  "steps": "1. 使用有权限账号登录CRM系统，进入首页→营销管理→协同分润→债券投顾页面\n2. 点击「新增」按钮\n3. 在「产品名称」下拉框中选择「债券A」\n4. 在「分润比例(%)」输入框中输入「101」\n5. 点击「保存」按钮",
  "expected_results": "1. 页面跳转到债券投顾列表页\n2. 弹出「新增分润规则」弹窗\n3. 下拉框展开并选中「债券A」\n4. 「分润比例(%)」输入框显示「101」，下方出现红色提示「分润比例不得超过100%」\n5. 「保存」按钮置灰不可点击，弹窗不关闭",
  "is_smoke": false,
  "source_test_point": "TP-001",
  "test_category": "boundary",
  "project": "",
  "case_type": "测试用例",
  "requirement": "",
  "menu_path": "营销管理→协同分润→债券投顾",
  "creator": "AI自动生成",
  "assignee": "",
  "test_case_type": "",
  "status": "待执行",
  "screenshot": "",
  "test_suite": "债券投顾分润",
  "remarks": ""
}
```

---

## 🔴 提交前自检（必须逐条检查后再保存）

**在调用 p6_save_batch 之前，必须逐条自检以下内容。不通过就不提交，不要等 Gate 报错。**

□ **步骤数 = 期望结果数**：每条用例的 steps 行数必须等于 expected_results 行数
□ **步骤 ≥ 15 字**：去除序号后每条步骤 ≥ 15 字
□ **含具体 UI 元素名**：步骤中必须引用 key_ui 中的具体名称（如「新增」「保存」）
□ **期望可观测**：expected_results 引用具体值/状态/文案，禁用"操作成功""结果正确"
□ **19 个字段全**：每条用例含全部 19 个字段，空值填 `""`

→ **🔴 自检不通过就修改 JSON，直到全部通过才调用 p6_save_batch。不要抱着"Gate 能过"的侥幸心理提交。**

---

## 输出

1. 将生成的 JSON 数组保存到文件：**`p6_batch_{batch_index:03d}_agent_output.json`**（注意 `_agent_output` 后缀不能少）
2. 直接输出完整的 testcases JSON 数组，不要添加解释。
3. **确保每个 test_point_id 出现 expected_case_count 次**（即该测试点有 expected_case_count 条用例）。
4. **确保每条用例包含上述全部 19 个字段**，即使值为空字符串也要保留。
