# 监控规则参考

## 电商网站

监控目标：价格、库存、促销活动

```
监控字段：
- 价格：.price, [data-price], #product-price, .offer-price
- 库存：.stock-status, .availability, [data-stock]
- 促销：.discount, .sale-badge, .promo-tag

变动阈值：
- 价格变动 >5% → 立即通知
- 价格变动 1-5% → 日报汇总
- 库存从有到无 → 立即通知
- 新增促销标签 → 立即通知

监控频率：每小时（价格敏感场景）/ 每天（常规监控）
```

## 新闻网站

监控目标：标题、发布时间、关键词

```
监控字段：
- 标题：h1, h2, .article-title, .headline
- 时间：.publish-time, time[datetime], .date
- 摘要：.article-summary, .excerpt, meta[name="description"]

变动阈值：
- 新文章发布 → 立即通知（含关键词时）
- 标题修改 → 记录日志

监控频率：每小时
```

## 政府网站

监控目标：法规发布、公告通知

```
监控字段：
- 文号：.doc-number, .notice-id
- 标题：.notice-title, h1
- 发布日期：.publish-date, .release-date
- 正文：.content, .article-body

变动阈值：
- 新法规/公告发布 → 立即通知
- 内容修订 → 立即通知（附修订前后对比）

监控频率：每天
```

## 招聘网站

监控目标：职位发布、薪资范围

```
监控字段：
- 职位名称：.job-title, h1
- 薪资：.salary, .compensation, [data-salary]
- 要求：.requirements, .job-description
- 公司：.company-name

变动阈值：
- 新职位发布 → 日报汇总
- 薪资范围变化 → 立即通知

监控频率：每天
```

## 技术文档/开源项目

监控目标：版本更新、API 变更

```
监控字段：
- 版本号：.version, h1, .release-tag
- 更新日志：.changelog, .release-notes
- API 变更：.breaking-changes, .deprecated

变动阈值：
- 新版本发布 → 立即通知
- Breaking changes → 立即通知

监控频率：每天
```
