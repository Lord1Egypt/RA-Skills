# 配置候选（未生效）

> 以下来自 `config.yaml` 的配置块为**未来候选，当前未生效**（无现行消费者或默认关闭）；如需启用，请将对应块原文移回 `config.yaml`。

> v8.2.4 自 `config.yaml` 移出，原文（含注释）保留于此。

## trend_tracking（趋势追踪，enabled: false，无消费者）

```yaml
# 趋势追踪（v5.9.1 新增）— 历史快照对比
trend_tracking:
  enabled: false            # 仅在用户确认保存历史后启用
  max_snapshots: 52           # 保留近 52 次审计（约一年，按周审计）
  snapshot_file: ".data/stats.json" # 与 liveness_check 共用
```

## capacity_analysis（容量分析，enabled 但唯一消费者为已归档的 .archived/flow-v7/02-bis-capacity.md）

```yaml
# 容量分析（v5.9.1 多因子有效容量）
capacity_analysis:
  use_effective_capacity: true    # 启用多因子有效容量计算
  cognition_multiplier: 2.0       # 认知容量 = activity_count × 此值
  conflict_penalty: 0.3           # 冲突因子 = 1 - (contamination均分/5 × 此值)
```
