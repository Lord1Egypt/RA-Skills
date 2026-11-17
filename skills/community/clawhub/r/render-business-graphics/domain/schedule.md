# 排期领域

## 适用范围

当任务有工期、前置关系、里程碑、负责人或分组时使用排期图。服务会计算最早/最迟时间、总时差、自由时差、关键路径和版面；Agent 不计算坐标和关键路径样式。

## 任务实体

```json
{
  "ref": "B",
  "name": "基础施工",
  "duration": 6,
  "predecessors": ["A"],
  "group": "实施阶段",
  "owner": "施工组",
  "milestone": false
}
```

`duration` 是正整数，`predecessors` 必须引用已有任务，不能自依赖或形成环。

## 版式选择

- `schedule.gantt`：默认，用于任务条、分组、负责人和里程碑。
- `schedule.time-scale-network`：明确要求双代号时标网络图时使用。
- `schedule.single-code-network`：明确要求单代号网络图时使用。

没有依赖、只有显式整数 `start` 时，只能使用 `gantt`，且所有任务都必须有 `start`，不能与 `predecessors` 混用。

## 文字规则

任务名建议 16 个字符以内，分组和负责人建议 12 个字符以内；长说明不应写入任务名，应拆成阶段、分组或多张图。
