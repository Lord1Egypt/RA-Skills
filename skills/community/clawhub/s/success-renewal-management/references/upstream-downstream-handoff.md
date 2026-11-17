# 上下游交接 + 7 种续约结果

## 上游交接（接什么）

| 上游 skill | 交接物 | 本 skill 用法 |
|---|---|---|
| 首价值证明（上游阶段） | 首价值证据包（定义卡+证据+叙事 3 版+决策层汇报）+ renewal-hooks 钩子清单 | Value Bridge「过去价值」段直接引用首价值证据包；续约对话预演用首价值叙事 |
| success-business-review | 业务回顾报告（识别续约风险 + 健康分趋势） | 健康分核算输入 + 风险根因识别 |

## 下游交接（交什么）

| 下游 | 触发 | 交接物 |
|---|---|---|
| success-expansion | 续约健康（绿档）+ 增购钩子触发 | 增购钩子清单 + Value Bridge「未来价值」段 + 客户增购信号 |
| 流失挽回 | 续约失败（红档 save 不足） | save 计划 + 风险根因记录 + 客户关系存档 |

## 7 种续约结果分类

| 结果 | 定义 | 影响 |
|---|---|---|
| Full Renewal + Expansion | 续约且增购 | NRR boost（增购交接 expansion） |
| Full Renewal (Flat) | 原值续约 | GRR 维持 |
| Renewal with Contraction | 续约但缩值 | 收入损失（缩范围/缩 seat） |
| Early Renewal | 到期前续约 | 锁定收入、降风险 |
| Multi-Year Renewal | 2-3 年承诺 | 可预测性 |
| Churn - Voluntary | 客户主动不续 | 流失（转挽回） |
| Churn - Involuntary | 被动流失（预算冻结/国产化替换/领导换届） | 流失（转挽回） |

## 绩效输出（支持 CS 续费率包干考核）

本 skill 产出可直接计入 CS 绩效包干：

- 续约预测表 → 续费率红线达成预判
- 风险档位分布 → 健康度作风险调节阀
- save 计划执行率 → 挽回率专项
- 多年期率 / 早续率 → 续约质量指标

## 交接铁律

- 续约健康客户**必须**埋增购钩子并交接 expansion（不埋 = expand 窗口流失，NRR 上不去）。
- 续约失败**必须**转流失挽回并交接 save 计划 + 根因（不交接 = 挽挽回无根因信息）。
- 本 skill 只续旧约，增购动作归 expansion，不在本 skill 展开。
