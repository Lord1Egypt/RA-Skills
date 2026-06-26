# 📊 头条号数据看板

> 更新时间: {{update_time}}

---

## 今日概览

| 指标 | 数值 | 日环比 |
|-----|------|-------|
| 👥 粉丝数 | {{fans_total}} | {{fans_change}} |
| 👁️ 阅读量 | {{read_today}} | {{read_change}} |
| 💰 收益 | ¥{{income_today}} | {{income_change}} |

---

## 粉丝趋势（近7天）

```
{{fans_trend_chart}}
```

| 日期 | 粉丝数 | 新增 |
|-----|-------|-----|
{{#each fans_trend}}
| {{date}} | {{count}} | {{change}} |
{{/each}}

---

## 内容表现

- 📝 文章总数: {{article_count}} 篇
- 📖 总阅读量: {{total_read}}
- 📈 平均阅读: {{avg_read}}

---

## 收益统计

| 时间周期 | 收益 |
|---------|-----|
| 今日 | ¥{{income_today}} |
| 昨日 | ¥{{income_yesterday}} |
| 本月 | ¥{{income_month}} |
| 累计 | ¥{{income_total}} |

---

{{#if alerts}}
## ⚠️ 数据提醒

{{#each alerts}}
- {{this}}
{{/each}}
{{/if}}

---

*数据来源: 头条号后台 | 仅供个人参考*
