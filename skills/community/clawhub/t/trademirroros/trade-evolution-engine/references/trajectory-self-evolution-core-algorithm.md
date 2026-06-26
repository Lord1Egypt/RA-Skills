# 轨迹自进化核心算法说明

更新日期：2026-04-14

英文版见：

- `trajectory-self-evolution-core-algorithm.en.md`

这份文档专门回答一个问题：Finance Journal 当前到底把“轨迹自进化”建模成了什么问题。

简化一句话：

> 当前实现不是把交易当成完整强化学习环境，而是把“闭环交易轨迹的压缩签名”建模成一个带上下文的排序问题，再用 bandit 风格指标决定“优先复用哪类历史路径、优先压制哪类老问题”。

对应代码入口主要在：

- `finance_journal_core/analytics.py`
- `finance_journal_core/app.py`
- `finance_journal_core/cli.py`

## 一、问题定义

当前系统里最稳定、最完整的数据单元，不是盘中逐秒序列，而是一笔已经闭环的交易记录：

- 开仓 / 平仓事实
- 计划区间与执行偏离
- 市场阶段
- 环境标签
- 逻辑标签 / 形态标签
- 情绪备注 / 失误标签
- 卖出后的 review 与 feedback

所以这里的“轨迹”，本质上是：

- 一笔交易的软结构摘要
- 一组可回看的上下文条件
- 一组可统计的结果反馈

而不是：

- 高频状态序列
- 连续动作序列
- 可直接做策略优化的 MDP 全量定义

这决定了当前版本更适合做：

1. 历史相似路径匹配
2. 交易风格优势 / 风险模式统计
3. 基于 bandit 的提醒排序

而不是直接做 offline RL。

## 二、为什么叫“轨迹自进化”

这里的“自进化”不是系统自动替用户下单，而是三层闭环：

1. 把每笔交易沉淀成结构化样本
2. 从样本里提炼可复用路径与风险基因
3. 在下一次相似情境出现时，把这些历史经验提前推回来

因此它更像一个“个人决策镜像系统”：

- 优质路径被优先提醒
- 风险模式被优先拦截
- 新交易又继续反哺历史库

## 三、核心建模对象

### 1. 路径臂 `path arm`

系统会把一笔闭环交易压缩成一个路径签名，核心组件来自 `_quality_path_components(...)`：

- 第一逻辑标签 -> `逻辑=...`
- 第一形态标签 -> `形态=...`
- 市场阶段 -> `阶段=...`
- 最多两个环境标签 -> `环境=...`
- 若存在正向执行纪律，则补一个 `纪律=买点在计划内` 或 `纪律=卖点在计划内`

当组件数不少于 2 个时，这笔交易才会形成一条可统计的路径臂。

它回答的问题是：

- “我过去在哪种组合条件下更容易做对？”

### 2. 基因臂 `gene arm`

系统也会把单个维度的标签看成可统计的基因臂，来源于 `_token_specs(...)`：

- `logic:*`
- `pattern:*`
- `stage:*`
- `environment:*`
- `mistake:*`
- `emotion:*`
- `execution:*`
- `review:*`
- `review_feedback:*`

它回答的问题是：

- “哪些单点特征长期有帮助？”
- “哪些单点特征反复带来亏损或动作变形？”

## 四、样本如何进入统计

`build_evolution_report(...)` 只处理满足以下条件的交易：

- `status == "closed"`
- `actual_return_pct` 不为空

每个样本会被抽取出以下统计基础：

- `pnl = actual_return_pct`
- `alpha = timing_alpha_pct`
- `holding = holding_days`
- `effective = _is_effective_trade(trade)`

其中“有效样本”定义很克制：

- 收益为正
- 如果存在 `timing_alpha_pct`，则 alpha 不能为负

也就是说，系统不是只看“赚没赚”，还会把“是否至少没有跑输自己的时机参考”作为附加约束。

## 五、路径与基因如何聚合

每个路径桶 / 基因桶都会累计这些统计量：

- `returns`
- `alphas`
- `holding_days`
- `wins`
- `losses`
- `effective_count`

随后 `_bucket_summary(...)` 会生成一组摘要指标：

- `sample_size`
- `win_rate_pct`
- `avg_actual_return_pct`
- `avg_timing_alpha_pct`
- `avg_holding_days`
- `effective_count`
- `loss_count`
- `positive_edge_score`

其中 `positive_edge_score` 是当前实现里的启发式综合分：

```text
positive_edge_score =
    win_rate_pct
    + avg_actual_return_pct * 2
    + avg_timing_alpha_pct
    + effective_count * 8
    - loss_count * 5
```

它不是概率模型，而是一个便于排序的经验评分，目的是把：

- 胜率
- 收益
- 相对时机质量
- 有效执行次数

压成一个容易比较的信号。

## 六、什么会被视为“优质路径”或“风险基因”

### 1. 优质路径

一条路径要进入 `quality_paths`，至少满足：

- `sample_size >= min_samples`
- `win_rate_pct >= 60`
- `avg_actual_return_pct > 0`

也就是说，当前实现不是追求“偶然暴利路径”，而是先要它：

- 有重复样本
- 胜率不过低
- 平均收益为正

### 2. 正向可复用基因

一个基因会进入 `reusable_genes`，通常满足两类条件之一：

- 本身就是明确正向 token，例如：
  - `execution:buy_in_plan`
  - `execution:sell_in_plan`
  - `review:good_exit`
  - `review_feedback:discipline_kept`
  - `review_feedback:good_exit_confirmed`
- 或者它虽然不是硬编码正向 token，但统计上满足：
  - `win_rate_pct >= 60`
  - `avg_actual_return_pct > 0`

### 3. 风险基因

以下 token 会被直接视作风险侧候选：

- 所有 `mistake:*`
- `execution:buy_off_plan`
- `execution:sell_off_plan`
- `review:sell_fly`
- `review_feedback:sell_fly_confirmed`
- 情绪类里的：
  - `急躁`
  - `慌张`
  - `冲动`
  - `上头`
  - `贪心`
  - `害怕`

此外，哪怕不是硬编码风险 token，只要统计均值收益为负，也会落入风险侧。

## 七、为什么这里用 bandit，而不是直接上 RL

### 1. 当前数据更像“单次决策反馈”

现有数据能稳定回答的是：

- 在某类上下文下，这种路径过去表现如何
- 某个标签历史上更偏正向还是负向

但它还不能稳定回答：

- 某一时刻为什么选动作 A 而不是 B
- 动作后经历了怎样的连续状态转移
- 如果换一个动作，路径会如何反事实展开

这使得当前问题天然更接近：

- contextual bandit
- hybrid bandit
- case-based ranking

而不是完整 MDP。

### 2. 当前 bandit 指标怎么计算

`_bandit_metrics(...)` 会把每个路径 / 基因摘要变成 bandit 风格分数。

先构造一个保守的 Beta 后验：

```text
posterior_alpha = 1 + win_count + max(effective_count - win_count, 0)
posterior_beta  = 1 + loss_count
posterior_mean  = posterior_alpha / (posterior_alpha + posterior_beta)
```

再给一个探索奖励：

```text
exploration_bonus =
    sqrt(2 * log(total_samples + 2) / (sample_size + 1))
```

同时把收益与 alpha 加成合成一个 reward component：

```text
reward_component =
    max(avg_actual_return_pct, 0) / 20
    + max(avg_timing_alpha_pct, 0) / 25
```

最终得到两个主要排序分：

```text
ucb_score =
    posterior_mean
    + 0.35 * exploration_bonus
    + reward_component

conservative_score =
    posterior_mean
    - 0.2 * exploration_bonus
    + 0.5 * reward_component
```

如果是风险臂，还会额外计算：

```text
risk_penalty_score =
    max(-avg_actual_return_pct, 0) / 12
    + loss_count / sample_size
    + 0.2 * exploration_bonus
```

可以把它理解成三种偏好：

- `posterior_mean`：历史胜率的保守均值
- `ucb_score`：适合“先看谁”
- `conservative_score`：适合“更稳地复用谁”
- `risk_penalty_score`：适合“先压制谁”

## 八、提醒层是怎么工作的

`build_evolution_reminder(...)` 并不会直接给买卖信号，而是先做上下文匹配。

查询侧会把输入转成 token：

- `logic:*`
- `pattern:*`
- `environment:*`
- `stage:*`

然后去和 `quality_paths` 的组件做重叠匹配：

- 若重叠数 `>= 2`，视作强匹配
- 若重叠数 `>= 1` 且查询 token 总数 `<= 2`，视作弱匹配

匹配后的路径按以下顺序排序：

1. `overlap_count`
2. `ucb_score`
3. `positive_edge_score`

同时，提醒层还会：

- 匹配正向基因 -> 给“可复用提醒”
- 匹配风险基因 -> 给“风险提醒”
- 从纪律 / 情绪 / 失误 / 回顾里再挑常见坏习惯 -> 给“习惯风险提醒”

最终输出的核心不是“买”或“卖”，而是三类信息：

1. 哪条历史路径更值得先复核
2. 哪个老毛病最该先按住
3. 下单前该先问自己的问题是什么

## 九、系统真正优化的目标

当前算法不是在优化收益最大化器，而是在优化一个更现实的目标：

- 提高复用优质历史的概率
- 提前暴露纪律 / 情绪 / 失误风险
- 让用户在样本不完备时也能得到有约束的提醒

所以它更像：

- “个人经验排序器”
- “风险模式拦截层”
- “会话式复盘辅助系统”

而不是自动交易策略引擎。

## 十、这套算法当前的边界

当前版本明确有这些边界：

1. “轨迹”仍是交易级压缩，不是盘中序列
2. 路径组件目前偏稀疏，只取首个逻辑 / 首个形态等摘要字段
3. `positive_edge_score` 与 risk 分数属于启发式，不是严格统计显著性检验
4. bandit 结果用于提醒排序，不直接驱动自动执行
5. 样本量很小时，任何“优势路径”都只能当作弱证据

## 十一、未来升级到 offline RL 需要补什么

如果未来要把“轨迹自进化”升级成真正的 trajectory policy，需要至少补齐：

- 盘中状态快照序列
- 加仓 / 减仓 / 止盈 / 止损 / 撤单动作序列
- 更细粒度 reward 定义
- 交易成本、回撤、仓位上限等显式约束
- 足够长时间、足够多市场状态的离线轨迹库

只有到这一步，才适合认真考虑：

- Decision Transformer
- IQL
- 其他保守 offline RL 路线

## 十二、给当前实现的结论

如果只用一句话概括当前版本：

> Finance Journal 目前把“轨迹自进化问题”定义成一个以交易级轨迹签名为样本、以 bandit 排序为核心、以提醒和复核为输出的个人决策增强问题。

这也是为什么当前系统会优先强调：

- 先把交易记完整
- 先把情绪 / 失误 / review 记录下来
- 先让下一次决策比上一次更可复盘

而不是急着把它包装成自动化策略。
