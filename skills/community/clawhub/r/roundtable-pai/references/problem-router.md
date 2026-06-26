# Problem Router

先判断问题本质，再选讨论骨架、讨论深度和问题标签。默认只输出一个最合适的 `discussion_frame`。

## 五类问题

- `decision`: 要不要做、要不要离职、要不要合作
- `judgment`: 怎么看、这个现象说明什么、该如何判断
- `execution`: 怎么做、怎么推进、接下来拆成什么步骤
- `reflection`: 我为什么总这样、我卡在哪、根因是什么
- `creative`: 给我新点子、还能怎么玩、怎么重新组合

## 骨架映射

- `decision` -> `decision_consult`
- `judgment` -> `judgment_debate`
- `execution` -> `execution_council`
- `reflection` -> `reflection_diagnosis`
- `creative` -> `creative_collision`

## 张力等级

- `low`: 脆弱、受伤、创伤、关系断裂、高风险心理困境
- `medium`: 默认等级，大多数普通决策与分析题
- `high`: 高冲突、高赌注、高压力的判断与取舍

## 讨论深度

- `light` -> `4` 轮
- `medium` -> `5` 轮
- `deep` -> `6` 轮
- `extended` -> `7` 轮

## 问题标签

从下面固定标签中选 `1-3` 个：

- `经济`
- `科技`
- `创业`
- `商业`
- `产品`
- `管理`
- `战略`
- `投资`
- `传播`
- `职业`
- `成长`
- `创意`
- `哲学心理`
- `历史政治`
- `执行`
- `体育`

## 推荐轮数判断

### 更适合 4 轮

- 问题比较单点
- 表层问法和真实卡点接近
- 不需要明显反转
- 快速交锋后就能进入结论

### 更适合 5 轮

- 问题有一定复杂度
- 需要完整开题、交锋和一次下潜
- 但不一定需要把修正单独拆成一轮

### 更适合 6 轮

- 问题涉及多层代价或多重前提
- 用户真实卡点可能和表层问法不完全一样
- 值得把“反转 / 修正”单独做成一轮

### 更适合 7 轮

- 问题复杂度高或分歧明显
- 需要两次下潜，或一次明显升级后再修正
- 值得形成完整的讨论弧线，而不是快速定结论

## 各骨架推荐区间

- `decision_consult`：4 到 6 轮
- `judgment_debate`：4 到 6 轮
- `execution_council`：5 到 7 轮
- `reflection_diagnosis`：5 到 7 轮
- `creative_collision`：5 到 6 轮

## 路由提示模板

```text
你现在不是在回答问题，而是在为一场三人讨论做前置路由。

输入：
- 用户问题

任务：
1. 判断问题更接近 decision / judgment / execution / reflection / creative 中哪一类。
2. 判断 tension_level 是 low / medium / high。
3. 选择唯一最合适的 discussion_frame。
4. 从固定标签表里选出 1 到 3 个最贴近这道题的 `problem_labels`。
5. 判断 discussion_depth 是 light / medium / deep / extended。
6. 给出 recommended_round_count，只能是 4 / 5 / 6 / 7 之一。
7. 提取 3 到 5 个真正决定讨论深度的 `decision_variables` 或 `judgment_variables`。
8. 用一句中文概括问题本质，写成 problem_summary。

要求：
- 只选一个主类型，不做“介于两者之间”的含混表述。
- 若问题同时涉及多个维度，优先按用户最想解决的主诉归类。
- `problem_labels` 要尽量宽泛而准确，不要细碎到只有少数人能命中。
- 允许问题同时命中多个标签，例如 `经济 + 科技`、`商业 + 管理`、`职业 + 成长`。
- `problem_labels` 是纯后台字段，自己决定即可，不要让用户确认。
- 轮数判断要看问题是否单层、是否存在更深一层的真实矛盾、是否需要角色修正、是否值得增加深水区。
- problem_summary 要点出当前矛盾，而不是复述原句。
- `decision_variables` / `judgment_variables` 必须贴住题目本身，例如平台规则、成本结构、流动性、时间窗口、供需关系、用户信任，而不是空泛词。
```
