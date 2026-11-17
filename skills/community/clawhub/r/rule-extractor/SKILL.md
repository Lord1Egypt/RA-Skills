---
name: rule-extractor
version: 1.0.0
description: "规则自动提取器。从失败和成功中自动提取规则，注入到后续会话的 system prompt。"
---

# Rule Extractor

## 功能
- 从追踪记录提取 avoid/prefer 规则
- 从 .learnings/ 目录提取学习规则
- 格式化为 System Prompt / JSON / Markdown

## 使用方法
```python
from extractor import RuleExtractor
from formatter import RuleFormatter

# 提取规则
extractor = RuleExtractor()
rules = extractor.extract_from_traces(traces)
rules.extend(extractor.extract_from_learnings(".learnings/"))

# 格式化
formatter = RuleFormatter()
prompt = formatter.format_as_prompt(rules)
print(prompt)
```

## 集成点
- self-improving skill（任务完成后提取规则）
- coding-framework Step 6（收尾检查时注入规则）
