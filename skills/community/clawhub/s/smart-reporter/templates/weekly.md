# {{report_title}}

**报告周期**: {{start_date}} - {{end_date}}
**生成时间**: {{timestamp}}

---

## 📊 本周概览

{{overview}}

## 📈 周度趋势

{{trend_chart}}

## 🎯 目标完成情况

| 目标 | 进度 | 状态 |
|------|------|------|
{{#goals}}
| {{name}} | {{progress}}% | {{status}} |
{{/goals}}

## 📋 本周成果

{{#achievements}}
### {{category}}
{{#items}}
- {{.}}
{{/items}}
{{/achievements}}

## 🔄 下周计划

{{#next_week_plans}}
- {{.}}
{{/next_week_plans}}

## 💡 洞察与建议

{{insights}}

---

*报告由 Smart Reporter 自动生成*
