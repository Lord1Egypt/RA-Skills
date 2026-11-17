# 流程可视化模板规范

## 目录
- [乌龟图模板](#乌龟图模板)
- [泳道图模板](#泳道图模板)
- [流程图模板](#流程图模板)
- [时间线模板](#时间线模板)
- [JSON配置格式](#json配置格式)

---

## 乌龟图模板

### 概念说明
乌龟图(5M1E分析)是质量管理和过程控制中常用的工具，从六个维度分析流程：
- Man (人): 操作人员、技能、培训
- Machine (机器): 设备、工装、工具
- Method (方法): 工艺、流程、SOP
- Material (材料): 原材料、半成品
- Measurement (测量): 检验、监控、数据
- Environment (环境): 工作条件、5S

### 布局结构
```
        [Man]
          |
          v
[Environment] ---> [中心] <--- [Machine]
          ^
          |
       [Material]
       
       [Method]
          ^
          |
      [Measurement]
```

### 典型配置示例
```json
{
  "title": "生产过程质量控制",
  "template": "turtle",
  "nodes": [
    {"id": "1", "name": "操作员培训", "type": "process", "category": "man"},
    {"id": "2", "name": "设备点检", "type": "process", "category": "machine"},
    {"id": "3", "name": "SOP执行", "type": "process", "category": "method"},
    {"id": "4", "name": "来料检验", "type": "process", "category": "material"},
    {"id": "5", "name": "过程检测", "type": "process", "category": "measurement"},
    {"id": "6", "name": "车间温湿度", "type": "process", "category": "environment"}
  ],
  "edges": [
    {"from": "1", "to": "2", "label": "培训后上岗"},
    {"from": "3", "to": "4", "label": "按规范检验"},
    {"from": "5", "to": "6", "label": "环境达标"}
  ]
}
```

---

## 泳道图模板

### 概念说明
泳道图(Swimlane Diagram)以横向分区展示不同责任部门或阶段的流程，每个泳道代表一个独立的职责范围。

### 布局结构
```
+-------------+-------------+-------------+-------------+
|   部门A     |   部门B     |   部门C     |   部门D     |
+-------------+-------------+-------------+-------------+
|   [任务1]   |             |             |             |
|      |      |             |             |             |
+-------------+------>[任务3]------>--------+-------------+
              |      |      |      |
+-------------+------>[任务4]      |
|             |             |    |
+-------------+-------------+----+-------------+-------------+
```

### 典型配置示例
```json
{
  "title": "订单处理流程",
  "template": "swimlane",
  "nodes": [
    {"id": "1", "name": "接收订单", "type": "process", "category": "销售部"},
    {"id": "2", "name": "信用审核", "type": "process", "category": "财务部"},
    {"id": "3", "name": "库存确认", "type": "process", "category": "仓储部"},
    {"id": "4", "name": "配货打包", "type": "process", "category": "仓储部"},
    {"id": "5", "name": "物流发货", "type": "process", "category": "物流部"},
    {"id": "6", "name": "客户签收", "type": "end", "category": "客户"}
  ],
  "edges": [
    {"from": "1", "to": "2", "label": "提交审核"},
    {"from": "2", "to": "3", "label": "审核通过"},
    {"from": "3", "to": "4", "label": "开始配货"},
    {"from": "4", "to": "5", "label": "发货"},
    {"from": "5", "to": "6", "label": "完成"}
  ]
}
```

---

## 流程图模板

### 概念说明
标准流程图(Flowchart)展示线性流程，含开始/结束节点、判断分支，用于描述业务操作步骤。

### 节点类型
| 类型 | 形状 | 用途 |
|------|------|------|
| start | 圆角矩形 | 流程起点 |
| end | 圆角矩形 | 流程终点 |
| process | 矩形 | 处理步骤 |
| decision | 菱形 | 判断条件 |

### 布局结构
```
[开始] --> [步骤1] --> [步骤2] --> (判断?) --yes--> [步骤3]
                                    |
                                   no
                                    v
                              [步骤4] --> [结束]
```

### 典型配置示例
```json
{
  "title": "项目立项审批流程",
  "template": "flowchart",
  "nodes": [
    {"id": "start", "name": "开始", "type": "start", "category": ""},
    {"id": "1", "name": "需求收集", "type": "process", "category": ""},
    {"id": "2", "name": "方案评审", "type": "decision", "category": ""},
    {"id": "3", "name": "立项审批", "type": "process", "category": ""},
    {"id": "4", "name": "返回修改", "type": "process", "category": ""},
    {"id": "end", "name": "项目启动", "type": "end", "category": ""}
  ],
  "edges": [
    {"from": "start", "to": "1", "label": ""},
    {"from": "1", "to": "2", "label": ""},
    {"from": "2", "to": "3", "label": "通过"},
    {"from": "2", "to": "4", "label": "驳回"},
    {"from": "4", "to": "1", "label": "重新提交"},
    {"from": "3", "to": "end", "label": ""}
  ]
}
```

---

## 时间线模板

### 概念说明
时间线图(Timeline)按时间顺序展示里程碑和关键节点，适合项目计划和进度展示。

### 布局结构
```
里程碑1    里程碑2    里程碑3    里程碑4
   |          |          |          |
   o----------o----------o----------o-------> 时间
```

### 典型配置示例
```json
{
  "title": "产品开发项目计划",
  "template": "timeline",
  "nodes": [
    {"id": "1", "name": "需求分析", "type": "start", "category": ""},
    {"id": "2", "name": "设计阶段", "type": "process", "category": ""},
    {"id": "3", "name": "开发迭代", "type": "process", "category": ""},
    {"id": "4", "name": "测试验收", "type": "process", "category": ""},
    {"id": "5", "name": "上线发布", "type": "end", "category": ""}
  ],
  "edges": []
}
```

---

## JSON配置格式

### 完整字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| title | string | 是 | 图表标题 |
| template | string | 是 | 模板类型: turtle/swimlane/flowchart/timeline |
| nodes | array | 是 | 节点列表 |
| edges | array | 否 | 连线列表 |

### Node字段

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | string | 是 | 唯一标识 |
| name | string | 是 | 显示名称 |
| type | string | 否 | 节点类型: start/end/process/decision |
| category | string | 否 | 分类(泳道名/5M1E类别) |

### Edge字段

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| from | string | 是 | 起始节点ID |
| to | string | 是 | 目标节点ID |
| label | string | 否 | 连线标签 |

### 验证规则

1. nodes数组至少有一个元素
2. 所有node.id必须唯一
3. edges中的from/to必须对应已存在的node.id
4. edges允许为空数组
5. 建议名称不超过20字符，避免显示溢出
