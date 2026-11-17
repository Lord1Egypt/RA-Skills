# 需求卡片模板

复制为 `backlog/R-###.md`。id 自增，从 R-001 开始，不回收。

````markdown
---
id: R-001
title: <一句话描述需求>
status: draft
priority: medium              # high / medium / low
depends_on: []                # 依赖的需求 id，如 [R-002]
conflicts_with: []            # 语义冲突的需求 id
created: YYYY-MM-DD           # 创建时写一次
updated: YYYY-MM-DD           # 每次改动更新
---

## 背景 / 目标
## 验收标准
## 设计文档          → 外链 docs/superpowers/specs/<date>-<topic>-design.md
## 实现计划          → plans/<id>.md（相对项目全局根，派发时生成）
## 验收记录          → 合并后填：测试结果 / review 结论
````
