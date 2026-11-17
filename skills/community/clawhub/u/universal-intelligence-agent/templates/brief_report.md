=== {{ query }} 简报 ===
来源: {{ total_engines }}引擎 ({{ total_results }}条) | 去重后: {{ deduplicated }}条
可信度: {{ credibility_stars }}

核心发现:
{% for finding in key_findings %}
{{ loop.index }}. {{ finding }}
{% endfor %}

关键信息:
{% for info in key_info %}
- {{ info }}
{% endfor %}

{% for source in sources %}
[{{ source.source }}] ({{ source.date }}) [{{ source.title }}] [可信度:{{ source.trust_level }}]
{% endfor %}
