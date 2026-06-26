# DAG Patterns

## 模式 1：顺序流水线

```
[Scan] → [Validate] → [Report] → [Notify]
```

适用场景：严格的 step-by-step 流程，每一步依赖上一步输出。

## 模式 2：并行分叉 + 汇聚

```
          → [IT Provisioning] → 
[Onboard]                         → [Notify]
          → [Facilities Setup]  →
```

适用场景：多个独立子任务可并行执行，最后汇总。

## 模式 3：条件分支

```
          → [Approve] → [Provision]
[Request]
          → [Reject] → [Notify]
```

适用场景：需要审批/判断后走不同路径。

## 模式 4：失败补偿

```
[Process] → [Fallback] (on_failure)
    ↓
[Success] (on_success)
```

适用场景：主流程失败时的降级/补偿方案。

## 模式 5：循环批处理 ⏳ 未来能力

> ⚠️ 此模式暂不支持。当前版本采用严格 DAG 模型，校验器会拒绝包含循环的计划。
> 循环批处理计划在后续版本（v1.1+）中实现。

分批处理大量数据时，建议拆分为多个线性批次（Batch1 → Batch2 → ...），或在工作流引擎层面控制迭代。

## 模式 6：审批门 ⏳ 未来能力

> ⚠️ 此模式中的 Revise → Review Gate 回环暂不支持。当前版本采用严格 DAG 模型。
> 可使用条件分支（模式 3）+ human_review_required 实现近似效果。

适用场景：需要人工审批后才能继续。
