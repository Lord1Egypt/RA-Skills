# TCMS Planner（中文说明）

**`tcms-*` 系列的一员** —— 面向科技产品营销团队的品牌方内容 Skill。
*不是中立第三方产业研究，那是 `industry-deep-dive-pipeline` 的职责。*

## 功能

基于知识库更新、竞品信号、内容日历，产出结构化选题 Brief。每次产出 1-3 个带优先级的选题。

不写文章正文，也不自动触发下游 Skill（那是 `tcms-writer` 的职责）。

## 触发词

选题, 本周内容, content plan, 选题建议, 内容规划

## 流水线位置

`tcms-planner`（选题）→ `tcms-writer`（初稿）→ `tcms-compliance-reviewer`（预审）→ `tcms-adapter`（渠道）→ `tcms-performance-analyst`（月度报告）
