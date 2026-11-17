# 排期图

## 稳定 ID

- `schedule.gantt`：任务条、分组、负责人、里程碑和普通项目计划。
- `schedule.time-scale-network`：双代号时标网络图。
- `schedule.single-code-network`：单代号网络图。

## 请求结构

```json
{
  "kind": "schedule",
  "variant": "gantt",
  "title": "项目实施进度计划",
  "startDate": "2026-10-01",
  "unit": "day",
  "data": [
    {"ref":"A","name":"施工准备","duration":4},
    {"ref":"B","name":"基础施工","duration":6,"predecessors":["A"]},
    {"ref":"C","name":"验收交付","duration":2,"predecessors":["B"],"milestone":true}
  ]
}
```

每个任务必须有唯一 `ref`、`name` 和正整数 `duration`。`predecessors` 必须引用其他任务。可选字段是 `start`、`group`、`owner`、`milestone`，其中 `start` 只支持 `gantt`。

## 两种甘特模式

1. 依赖模式：使用 `predecessors`，由服务计算最早/最迟时间、时差、关键任务和布局。
2. 显式起始模式：所有任务都有整数 `start`，所有任务都没有前置关系，且 variant 必须是 `gantt`。

两种模式不能混用。不要计算或提交 CPM 字段，关键路径由服务派生。`startDate` 为 `YYYY-MM-DD`，`unit` 为 `day`、`week` 或 `stage`。最多 30 个任务，默认横版。任务名建议 16 个字符以内。
