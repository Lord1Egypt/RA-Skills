# TCMS Writer（中文说明）

**`tcms-*` 系列的一员** —— 面向科技产品营销团队的品牌方内容 Skill。
*不是中立第三方产业研究，那是 `industry-deep-dive-pipeline` 的职责。*

## 功能

基于产品知识库与品牌规范，产出**品牌营销类长文初稿**（技术博客、客户案例、产品解读）。仅从 content brief 产出 1500–3000 字长文。

不负责社交帖、短内容、渠道适配（见 `tcms-adapter`）。

## 适用场景

- 已有选题 Brief，需要品牌营销长文初稿。
- 文章属推广 / 产品定位性质。

## 不适用场景

- 中立第三方产业深度研究 → 用 `industry-deep-dive-pipeline`。
- 单篇发布前合规预审 → 用 `tcms-compliance-reviewer`。
- 渠道适配 → 用 `tcms-adapter`。

## 触发词

写文章, 写稿, 写初稿, 起草, 技术博客, 品牌技术稿, 案例文章, 客户案例, 产品解读, 产品稿, 新闻稿, content brief, draft, 按brief写

## 流水线位置

`tcms-planner`（选题）→ **`tcms-writer`**（初稿）→ `tcms-compliance-reviewer`（预审）→ `tcms-adapter`（渠道）→ `tcms-performance-analyst`（月度报告）
