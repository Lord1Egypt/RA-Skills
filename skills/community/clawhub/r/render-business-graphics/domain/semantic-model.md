# 语义模型

## 请求分层

V2 请求可以拆成五层：

1. `kind`：`chart`、`organization`、`flow`、`smartart`、`schedule`、`sequence`、`timeline`。
2. `variant`：家族内的具体版式；`organization` 和 `sequence` 不需要 variant。
3. 通用展示字段：`title`、`subtitle`、`theme`、`page`、`rasterScale`。
4. 业务 `data`：由选定图形的契约决定。
5. 家族字段：例如 `unit`、`direction`、`center`、`startDate`、`showTimeScale`。

服务会派生内部 ID、坐标、颜色、页面宽高、关键路径和线性流程连线。Agent 只提交业务事实和关系。

## 核心实体

| 实体 | 含义 | 关键字段 |
| --- | --- | --- |
| 指标观测 | 一个类别及其数值 | `label`、`value`，多系列再加 `series` |
| 组织节点 | 一个部门、角色或责任单元 | `name`，子级放入 `children` |
| 流程节点 | 一个动作、判断、文档或边界 | `text`，图模式还需要 `ref` |
| 流程连线 | 节点之间的有向关系 | `from`、`to`，可选 `label`、`relation` |
| SmartArt 项 | 一个概念点 | `title`，可选 `note`、`icon` |
| 排期任务 | 一个有工期的活动 | `ref`、`name`、`duration`、可选 `predecessors` |
| 参与方 | 一个用户、系统或部门 | 字符串或 `ref`/`name` 对象 |
| 消息 | 参与方之间的一次调用或返回 | `from`、`to`、`message`、可选 `kind` |
| 时间轴事件 | 一个日期或阶段事件 | `ref`、`date`、`title` |

## 语义字段和展示字段

`headcount`、`duration`、`predecessors`、`from`、`to` 是业务语义；坐标、颜色 HEX、连线虚实、关键路径样式和 SVG 路径属于渲染器内部数据，不能由 Agent 自行提交。

## 省略规则

省略是有意义的：没有色系要求时省略 `theme`，没有副标题时省略 `subtitle`，没有图标时省略 `icon`，没有明确方向时省略 `page`。不要用 `null`、空数组或“暂无”占位。

## 数据整理顺序

1. 保留用户的名称、标签、日期、单位和数值。
2. 数值使用 JSON number，不要把数值写成带单位的字符串。
3. 只有存在关系时才生成稳定短 ref。
4. 关系不清楚时提问，不要用自然语言猜测连线。
5. 标签尽量短，详细解释移到 `detail`、`note` 或 `description`。
