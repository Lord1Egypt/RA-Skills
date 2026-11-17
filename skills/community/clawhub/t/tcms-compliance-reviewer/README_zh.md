# TCMS Compliance Reviewer（中文说明）

**`tcms-*` 系列的一员** —— 面向科技产品营销团队的品牌方内容 Skill。
*不是中立第三方产业研究，那是 `industry-deep-dive-pipeline` 的职责。*

## 功能

对品牌方稿件（技术博客、客户案例、产品解读、新闻稿）做发布前合规与质量预审——检查事实引用、客户脱敏、产品命名、竞品规则、内部信息泄露。

只报告问题与修改建议，绝不自动修改原文。月度效果分析请用 `tcms-performance-analyst`。

## 触发词

预审, 审核, 审稿, 终审, review, 检查初稿, fact check, 合规检查, 发布前审核, 发稿前检查, pre-publication review

## 流水线位置

`tcms-planner`（选题）→ `tcms-writer`（初稿）→ `tcms-compliance-reviewer`（预审）→ `tcms-adapter`（渠道）→ `tcms-performance-analyst`（月度报告）
