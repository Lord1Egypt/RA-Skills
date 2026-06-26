# 新增案例入库提示

当用户要求“把一个新历史案例加入案例库”时，按下面流程执行：

1. 先判断这是不是要持久化入库，而不是临时举例。
2. 如果用户信息不完整，只追问 1-3 个最关键的问题。
3. 把用户的自然语言整理成单条 JSON，对齐案例模板。
4. 不要要求用户手工改仓库文件；优先由你直接调用本地脚本写入。
5. 写入成功后，返回新增案例的 `id`，并告知以后检索会自动加载。

必须补齐或确认的字段：

- `title`
- `summary`
- `situation_tags`
- `chosen_action`
- `key_reasons`
- `transferable_principles`
- `source_note`

推荐执行命令：

```powershell
@'
{
  "id": "example-case-id",
  "title": "案例标题",
  "dynasty": "朝代或时期",
  "era": "历史阶段",
  "year_range": "时间范围",
  "main_figures": ["人物甲", "人物乙"],
  "summary": "事件与局面概述",
  "situation_tags": ["改革推进"],
  "decision_maker": "主要决策者",
  "objective": "想达成的目标",
  "visible_information": ["公开条件 1"],
  "hidden_constraints": ["隐性限制 1"],
  "options_available": ["选项 1", "选项 2"],
  "chosen_action": "最终动作",
  "short_term_outcome": "短期结果",
  "long_term_outcome": "长期结果",
  "success_or_failure": "mixed",
  "key_reasons": ["原因 1"],
  "transferable_principles": ["原则 1"],
  "non_transferable_factors": ["不可照搬因素 1"],
  "modern_analogy_keywords": ["关键词 1"],
  "source_note": "来源说明"
}
'@ | python scripts/add_case.py --stdin
```

如果用户还没说清楚，不要编造史料或来源。
