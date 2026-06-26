---
name: wecom-workplan-summary
description: 团队工作计划周度/月度汇总分析。仅当用户**明确提供**了团队工作计划数据（粘贴内容或指向企微智能表格）并要求汇总/分析时触发。典型意图："这是团队工作计划，帮我看下上周/本周情况"、"我把数据复制过来了，分析一下"、"帮我从企微表格拉取工作计划汇总"。**不触发**：仅提到"周报"、"本周工作"等通用词但未提供数据或未明确指向企微表格。
allowed-tools: Bash(python3:*), Bash(mkdir:*), Write
---

# 团队工作计划汇总技能

按周度或月度汇总团队工作记录，支持两种输入方式：从企微智能表格读取（MCP 模式），或直接粘贴表格内容（粘贴模式）。脚本负责数据整理，你负责生成自然语言报告。

## 数据源（MCP 模式）

**智能表格**：
- docid: `dcrZNwuyF7QzK5GW4oQ9B3Y3i6Vdc_RzIxAc1zWMMVr9K4EWCEEza2Ea1XGGuQumBW2IKp9XR6au-lDtMi--j27A`
- sheet_id: `q979lj`
- 字段：`日期`、`今日计划`、`姓名`/`成员`/`提交人`、`岗位`/`职位`

## 执行步骤

### 分支 A — 粘贴模式（用户提供了工作计划内容）

**触发条件**：用户消息中包含多行表格内容（tab 或逗号分隔），并说明这是团队工作计划数据。

1. 将用户提供的表格内容原样写入 `/tmp/workplan_paste.tsv`

2. 根据用户是否指定时间范围调用脚本：

   **用户未指定时间**（脚本自动从数据中检测）：
   ```bash
   python3 ~/.openclaw/workspace/skills/wecom-workplan-summary/scripts/summary.py 周度 --data /tmp/workplan_paste.tsv
   ```

   **用户指定了"上周"/"本周"/"第X周"**（换算为周数后传入）：
   ```bash
   python3 ~/.openclaw/workspace/skills/wecom-workplan-summary/scripts/summary.py 周度 <week_num> <year> --data /tmp/workplan_paste.tsv
   ```

   **用户指定了月份**：
   ```bash
   python3 ~/.openclaw/workspace/skills/wecom-workplan-summary/scripts/summary.py 月度 <month> <year> --data /tmp/workplan_paste.tsv
   ```

3. 根据脚本输出的结构化原始数据，生成最终报告（见下方"报告生成规范"）

**粘贴数据格式要求**（可在执行前提示用户）：
- 必须包含列：`日期`、`姓名`（或`成员`/`提交人`）、`今日计划`（或`工作内容`/`工作计划`）
- 可选列：`岗位`/`职位`
- 支持 Tab 分隔（从企微/Excel/WPS 直接复制）或逗号分隔

### 分支 B — MCP 模式（用户未提供数据，要求从企微读取）

**触发条件**：用户明确说"从企微表格读取"、"帮我拉一下数据"等，未粘贴内容。

1. 调用 wecom_mcp 获取智能表格记录：

   ```
   wecom_mcp call doc smartsheet_get_records '{"docid":"dcrZNwuyF7QzK5GW4oQ9B3Y3i6Vdc_RzIxAc1zWMMVr9K4EWCEEza2Ea1XGGuQumBW2IKp9XR6au-lDtMi--j27A","sheet_id":"q979lj"}'
   ```

2. 根据用户指定时间范围调用脚本：

   ```bash
   python3 ~/.openclaw/workspace/skills/wecom-workplan-summary/scripts/summary.py 周度 <week_num> <year>
   python3 ~/.openclaw/workspace/skills/wecom-workplan-summary/scripts/summary.py 月度 <month> <year>
   ```

3. 根据脚本输出生成最终报告（见下方"报告生成规范"）

---

## 报告生成规范

脚本输出的是结构化原始数据（每人 + 每日计划明细），**你需要将其转化为自然语言报告**。

### 输出格式模板

```
📅 第N周工作周报（MM/DD-MM/DD）

{姓名} · {岗位}
本周：{自然语言汇总}

🔹 目标对齐：{一句话判断}
💡 建议：{针对性建议}

---

{姓名} · {岗位}
本周：...

🔹 目标对齐：...
💡 建议：...

---

注：{未提交情况说明}
```

### 生成原则

**本周汇总（最重要）**：
- 相同或高度相似的任务合并，标注天数：`HJJ驻场（4天）`
- 有明显进展逻辑的用 `→` 连接：`接口页面重构 → SOP重构 → 页面内容优化`
- 多个不同任务用 ` + ` 连接：`RAG知识库开发 + mineruAPI对接`
- 编号列表（1. 2. 3.）提炼为核心主题，不照搬编号
- 请假直接标注：`周三请假，其余时间：XX工作`

**🔹 目标对齐**：
- 判断该人工作与团队当前目标的关联，1句话，要有实质内容
- 不写"任务推进中"、"目标明确"等套话
- 例：`技术侧支撑AI标书工具开发` / `项目交付-前端重构推进` / `驻场支持客户现场`

**💡 建议**：
- 结合当周实际工作内容给出具体建议，不泛泛而谈
- 不写"持续推进"、"注意进度同步"等无意义话
- 例：`连续4天驻场，建议定期输出问题清单同步团队` / `单一任务深耕，可适当输出中间产物便于评估`

**结尾注释**：
- 全员提交：`注：本周全员均有记录`
- 有缺失：`注：以下人员本周未提交记录：XX、XX`

---

## 注意事项

1. 管理层（张鹏乐、王紫龙、付岩）放在最前面
2. 无记录人员单独在末尾说明，不猜测原因
3. 语气亲切、专业，不严厉

## 依赖工具

- wecom_mcp：MCP 模式下读取智能表格数据
- Bash(python3:*)：执行汇总脚本
