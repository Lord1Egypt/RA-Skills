# AI 用量与提示词复盘助手（weekly-review）

面向任意 AI Agent 的自动复盘 Skill。

## 解决什么问题

1. 提升提示词表达能力  
2. 查看本周 AI 用量  
3. 总结工作低效与高效  
4. 复盘可视化图表（时间分布 / 归因 / Token）  
5. 清理/对齐开放对话  
6. AI 自动/定时周复盘  

## Install

```bash
npx skills add testman2025/weekly-review-skill --skill weekly-review
# or
openclaw skills install weekly-review
```

See the repo root [README](../../README.md).

## Output shape (locked)

1. Dashboard table (`指标 | 数值 | 口径说明`) + one-liner + optional chart paths  
2. Theme project sections with dimension tables (incl. disk verification)  
3. Problems + three-class root cause + positives  
4. Action ledger  
5. Open sessions  
6. Automations overview  
7. Fact corrections (optional)

## Render

```bash
python -m cli --input schema/review-input.example.json -o weekly-report.md
```

See `SKILL.md` and `schema/`.
