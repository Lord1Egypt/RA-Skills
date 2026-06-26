# Orchestration Rules

## 规划原则

1. **最小必要原则**：只编排必须编排的部分，单步能完成的不要拆分
2. **显式依赖**：所有依赖必须通过 edge 显式声明，禁止隐式依赖
3. **并行优先**：无依赖的节点应该并行，不要串行化
4. **失败显式路由**：每个可能失败的节点必须有 `on_failure_route`

## DAG 设计规则

- 入口节点（entry_nodes）：没有入边的节点，通常是初始化/数据准备
- 出口节点（exit_nodes）：没有出边的节点，通常是汇总/报告/通知
- 扇出（fan-out）：一个节点的输出分发给多个下游节点，用多条 `from_node → to_node` 边
- 扇入（fan-in）：多个节点汇聚到一个下游节点，多条边指向同一个 `to_node`
- 条件边：使用 `condition_type: "conditional"` + `condition_expression`

## 节点设计规范

### 必填字段
| 字段 | 类型 | 说明 |
|------|------|------|
| node_id | string | 唯一标识，建议 `N1`, `N2` 或 `step_01_data_scan` |
| target_skill | string | 绑定的技能名称（必须在白名单内） |
| purpose | string | 一句话描述节点做什么 |
| scoped_state_keys | array | 该节点可访问的状态键列表 |

### 可选字段
| 字段 | 类型 | 说明 |
|------|------|------|
| input_mapping | object | 上游输出 → 本节点输入的映射 |
| output_mapping | object | 本节点输出 → 下游可消费的键 |
| retry_policy | object | 重试策略（max_retries, backoff_ms） |
| timeout_seconds | integer | 超时时间（秒） |
| human_review_required | boolean | 是否需要人工审批 |

## 条件边规范

```json
{
  "from_node": "N2",
  "to_node": "N3",
  "condition_type": "conditional",
  "condition_expression": "N2.result.status == 'approved'",
  "on_failure_route": "N4"
}
```

支持的 condition_type：
- `always`：无条件执行（默认）
- `on_success`：上游成功时执行
- `on_failure`：上游失败时执行（补偿路径）
- `conditional`：按条件表达式判断

## 常见编排模式

### 1. 线性流程
N1 → N2 → N3 → N4
适用于：严格按顺序的流水线

### 2. 并行分叉
N1 → N2
N1 → N3
N2 → N4
N3 → N4
适用于：N2 和 N3 可以并行

### 3. 条件分支
N1 → N2 (on_success)
N1 → N3 (on_failure)
适用于：失败补偿/降级路径
