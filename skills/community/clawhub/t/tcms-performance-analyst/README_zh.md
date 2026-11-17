# TCMS Performance Analyst（中文说明）

**`tcms-*` 系列的一员** —— 面向科技产品营销团队的品牌方内容 Skill。
*不是中立第三方产业研究，那是 `industry-deep-dive-pipeline` 的职责。*

## 功能

对项目级内容做月度分析：已发布产出、排期偏差、渠道效果、产品线覆盖、知识库健康度，并给出下月建议。

绝不编造指标（缺失标注 DATA_MISSING），也不自动改排期或触发写作。单篇发布前预审请用 `tcms-compliance-reviewer`。

## 触发词

月度报告, 效果分析, 内容复盘, 月度复盘, 数据复盘, 发文统计, monthly report, content review, performance analysis

## 流水线位置

`tcms-planner`（选题）→ `tcms-writer`（初稿）→ `tcms-compliance-reviewer`（预审）→ `tcms-adapter`（渠道）→ **`tcms-performance-analyst`**（月度报告）
