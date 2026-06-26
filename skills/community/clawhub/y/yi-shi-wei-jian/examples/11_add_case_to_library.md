# Natural Language Case Ingestion

## User Request

```text
把“赵武灵王胡服骑射”这个案例加入案例库，后续检索也要能用。核心局面是改革推进和以弱对强，关键决策是主动改制和推动军事转型，短期内阻力很大，但长期提升了赵国机动战力。来源请记《史记·赵世家》。
```

## Expected Skill Behavior

- 判断用户目标是“持久化入库”，不是临时分析
- 对缺失字段只追问 1-3 个关键问题
- 把自然语言整理成单条 JSON
- 调用本地脚本写入 `data/user_cases.json`
- 返回新增案例 `id`，并告知以后检索会自动加载
