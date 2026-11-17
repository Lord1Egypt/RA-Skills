# 领域导航

先判断业务实体和实体关系，再选择图形。读取领域文件后，还必须读取 `references/graphics/` 下对应的单类图形说明。

| 业务对象 | 领域说明 | 主要图形 |
| --- | --- | --- |
| 维度、指标、评分、对比 | [data-chart.md](data-chart.md) | `chart.*` |
| 父子职责和组织归属 | [organization.md](organization.md) | `organization` |
| 有序步骤、判断和回退 | [process.md](process.md) | `flow.*` |
| 概念关系和表达结构 | [conceptual-structure.md](conceptual-structure.md) | `smartart.*` |
| 工期、任务、依赖 | [schedule.md](schedule.md) | `schedule.*` |
| 参与方、调用、返回 | [interaction.md](interaction.md) | `sequence` |
| 日期、阶段、历史事件 | [chronology.md](chronology.md) | `timeline.*` |

## 先关系、后版式

“方案设计、建设实施、验收交付”是线性流程；“方案一与方案二在成本、周期、扩展性上的差异”是对比矩阵；“项目经理部下辖技术组和实施组”是组织树。不能因为内容都叫“流程”或“展示”就使用同一种图。

## 技术标识规则

保留业务名称和描述，只在契约要求时生成短 ref：流程图连线使用节点 `ref`，排期依赖使用任务 `ref`，时序消息使用参与方 `ref`，时间轴事件使用事件 `ref`。不要生成坐标、像素尺寸、SVG 路径或 ECharts 配置。
