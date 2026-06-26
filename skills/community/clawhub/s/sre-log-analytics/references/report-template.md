# System Log Analysis Report | 系统日志分析报告

*Template variables are marked with `{{variable_name}}`*  
*模板变量使用 `{{variable_name}}` 标记*

---

## Analysis Overview | 分析概览

| Item | Value |
|------|-------|
| Analysis Time Range | `{{start_time}} ~ {{end_time}}` |
| Log File | `{{log_file}}` |
| Total Log Lines | {{total_lines}} |
| Error Lines | {{error_lines}} |
| Error Rate | {{error_rate}}% |

---

## System Health Score | 系统健康评分

**Score: {{health_score}} / 5**

{{health_description}}

---

## Operation Summary | 运行总结

{{summary}}

---

## Exception Details (Sorted by Severity) | 异常详情（按严重程度排序）

{% for error in errors %}

### {{error.rank}}. {{error.title}} (Occurred {{error.count}} times)

**Error Type:** {{error.type}}  
**Impact Scope:** {{error.impact}}

**Sample Log:**
```
{{error.sample}}
```

{% endfor %}

---

## Improvement Suggestions | 改善建议

### Short-term (Execute Immediately) | 短期（立即执行）

{% for suggestion in short_term %}
- {{suggestion}}
{% endfor %}

### Mid-term (Within 1 Week) | 中期（1周内）

{% for suggestion in mid_term %}
- {{suggestion}}
{% endfor %}

### Long-term (Within 1 Month) | 长期（1个月内）

{% for suggestion in long_term %}
- {{suggestion}}
{% endfor %}

---

*Generated on {{generated_at}} by system-log-analytics skill*  
*由 system-log-analytics 技能生成于 {{generated_at}}*
