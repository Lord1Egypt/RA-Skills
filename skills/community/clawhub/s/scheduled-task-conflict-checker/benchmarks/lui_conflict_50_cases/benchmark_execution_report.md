# 定时任务冲突检测 Benchmark 执行报告

## 执行结论

- Benchmark 总数：50
- 本地确定性校验：50 通过，0 失败，0 错误
- 每条 case 均包含 `initial_tasks`，用于模拟用户已经配置过的定时任务
- Runner 在每条 case 执行前清空临时任务池，写入当前 case 的 `initial_tasks`，执行后再次删除临时任务池
- 执行结束后确认：`runtime/task_pool.json` 不存在

## 覆盖范围

| 类别 | 数量 |
| --- | ---: |
| 店铺绑定/授权边界 | 8 |
| ISV 高级版权限边界 | 8 |
| 平台能力不支持 | 5 |
| 完全重复/语义重复/流程重复 | 9 |
| 策略部分重复 | 6 |
| 高风险重复 | 6 |
| 高频堆积/时间窗口集中 | 4 |
| 通知边界 | 2 |
| 正常可创建 | 2 |

## 关键校验点

- 已有同店铺、同任务、同时间、同策略任务时，返回 `reuse_or_update`，不新增任务。
- 已有同目标但策略不同任务时，返回 `ask_confirmation`，要求用户确认修改原任务、新建或取消。
- 已有高风险写任务重叠时，返回 `ask_confirmation`，不能静默合并。
- 指定未绑定店铺、店铺授权失效、ISV 高级版权限缺失时，按阻断或部分创建处理。
- 每 5/10 分钟等高频任务返回 `warn_then_proceed`，提示堆积风险。
- 微信未绑定但仅作为通知渠道时，任务可创建，通知回退到任务中心或 App Push。

## 执行命令

```bash
python3 openclaw_skill_eval/tools/generate_benchmark.py
python3 openclaw_skill_eval/tools/run_benchmark.py
```

## 产物

- `test_cases_50.csv`：50 组 case 索引表。
- `test_prompts_50.md`：50 组自然语言请求和预期结果说明。
- `fixtures/case_001` 至 `fixtures/case_050`：每组隔离输入，包含 `initial_tasks`。
- `results/benchmark_results.json`：机器可读执行结果。
- `results/benchmark_results.md`：人工可读执行结果。
