# LLM 参数

chain_planner.py plan 支持传入 LLM 判断结果：

```bash
--llm-chain-check '{"passed":true,"reason":"ok","milestones":"1,2"}'
--milestones "1,2"
--adhesion '{"resolved":true,"solutions":[{"mode":"manual","desc":"手动转换"}]}'
```

| 参数 | 格式 | 门禁 | 阻断条件 |
|------|------|------|---------|
| --llm-chain-check | JSON | llm_chain_verified | passed=false |
| --milestones | 逗号分隔 | milestones_set | 缺值 |
| --adhesion | JSON | adhesion_resolved | gap>0 但未解决 |

