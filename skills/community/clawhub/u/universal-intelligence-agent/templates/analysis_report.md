=== {{ query }} 深度分析 ===

一、信息汇总
  引擎: {{ total_engines }}台 | 结果: {{ total_results }}条 | 去重: {{ deduplicated }}条
  来源分布: 国内{{ cn_count }}条, 国际{{ global_count }}条
  时效: {{ date_range }}

二、关键实体
  人物: {{ entities.persons }}
  机构: {{ entities.organizations }}
  时间线: {{ entities.dates }}

三、可信度评估
  高可信: {{ credibility.high }}条
  中等: {{ credibility.medium }}条
  低可信/存疑: {{ credibility.low_dubious }}条

四、情感/倾向
  整体: {{ sentiment.overall }}

五、交叉验证
  一致内容: {{ cross_validation.consistent }}
  分歧内容: {{ cross_validation.divergent }}
  待核实: {{ cross_validation.unverified }}

六、结论
{% for c in conclusions %}
{{ loop.index }}. {{ c }}
{% endfor %}

---
{% for source in sources %}
- [{{ source.source }}] {{ source.title }} ({{ source.date }})
{% endfor %}
