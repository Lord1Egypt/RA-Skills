# {{report_title}}

**报告日期**: {{date}}
**生成时间**: {{timestamp}}

---

## 📊 今日概览

{{overview}}

## 📈 关键指标

| 指标 | 数值 | 变化 |
|------|------|------|
{{#metrics}}
| {{name}} | {{value}} | {{change}} |
{{/metrics}}

## ✅ 完成事项

{{#completed_tasks}}
- {{.}}
{{/completed_tasks}}

## 🔄 进行中

{{#in_progress}}
- {{.}}
{{/in_progress}}

## ⚠️ 注意事项

{{#alerts}}
- **{{level}}**: {{message}}
{{/alerts}}

## 📝 备注

{{notes}}

---

*报告由 Smart Reporter 自动生成*
