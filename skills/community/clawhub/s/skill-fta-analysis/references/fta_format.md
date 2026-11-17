# 故障树数据格式规范

## 概览

FTA技能使用JSON作为标准数据格式，支持YAML格式的导入导出。故障树由节点（事件和逻辑门）和边（父子关系）组成。

## 数据结构定义

```json
{
  "name": "string (必需)",
  "description": "string (可选)",
  "version": "string (可选, 默认1.0)",
  "top_event": "string (必需, 顶事件节点ID)",
  "nodes": {
    "<node_id>": {
      "type": "string (必需)",
      "name": "string (必需)",
      "probability": "number (basic类型必需, 0-1之间)",
      "description": "string (可选)"
    }
  },
  "edges": [
    {
      "from": "string (父节点ID)",
      "to": "string (子节点ID)"
    }
  ]
}
```

## 节点类型

| 类型 | 说明 | 是否需要probability |
|------|------|---------------------|
| `basic` | 基本事件（叶节点） | 是 |
| `intermediate` | 中间事件 | 否 |
| `and` | AND门（所有子事件同时发生） | 否 |
| `or` | OR门（任一子事件发生） | 否 |

## 验证规则

1. `top_event` 必须存在于 `nodes` 中
2. 每个节点ID必须唯一
3. `basic` 类型节点必须有 `probability` 字段
4. 所有边必须引用已定义的节点
5. 图必须是有向无环图（DAG）
6. `probability` 值必须在 [0, 1] 范围内

## 完整示例

### 简单OR门系统
```json
{
  "name": "电源系统故障分析",
  "description": "电源系统包含主电源和备用电源，任一电源故障即导致系统断电",
  "top_event": "system_failure",
  "nodes": {
    "system_failure": {
      "type": "or",
      "name": "系统断电",
      "description": "系统无法正常供电"
    },
    "main_power_failure": {
      "type": "basic",
      "name": "主电源故障",
      "probability": 0.05,
      "description": "主电源供电中断"
    },
    "backup_power_failure": {
      "type": "basic",
      "name": "备用电源故障",
      "probability": 0.10,
      "description": "备用电源未能启动"
    }
  },
  "edges": [
    {"from": "system_failure", "to": "main_power_failure"},
    {"from": "system_failure", "to": "backup_power_failure"}
  ]
}
```

### 复杂AND+OR混合系统
```json
{
  "name": "控制系统故障分析",
  "top_event": "control_failure",
  "nodes": {
    "control_failure": {
      "type": "or",
      "name": "控制系统失效",
      "description": "控制功能完全丧失"
    },
    "hardware_failure": {
      "type": "and",
      "name": "硬件故障",
      "description": "控制器和传感器同时故障"
    },
    "software_failure": {
      "type": "basic",
      "name": "软件故障",
      "probability": 0.02,
      "description": "控制软件崩溃"
    },
    "controller_failure": {
      "type": "basic",
      "name": "控制器故障",
      "probability": 0.01,
      "description": "控制器硬件损坏"
    },
    "sensor_failure": {
      "type": "basic",
      "name": "传感器故障",
      "probability": 0.015,
      "description": "传感器失效"
    }
  },
  "edges": [
    {"from": "control_failure", "to": "hardware_failure"},
    {"from": "control_failure", "to": "software_failure"},
    {"from": "hardware_failure", "to": "controller_failure"},
    {"from": "hardware_failure", "to": "sensor_failure"}
  ]
}
```

## YAML格式示例

```yaml
name: 电源系统故障分析
top_event: system_failure
nodes:
  system_failure:
    type: or
    name: 系统断电
  main_power_failure:
    type: basic
    name: 主电源故障
    probability: 0.05
  backup_power_failure:
    type: basic
    name: 备用电源故障
    probability: 0.10
edges:
  - from: system_failure
    to: main_power_failure
  - from: system_failure
    to: backup_power_failure
```

## 概率计算公式

### OR门
$$P_{OR} = 1 - \prod_{i=1}^{n}(1-P_i) = 1 - (1-P_1)(1-P_2)...(1-P_n)$$

### AND门
$$P_{AND} = \prod_{i=1}^{n}P_i = P_1 \times P_2 \times ... \times P_n$$

### 近似公式（当所有概率都很小时）
$$P_{OR} \approx \sum_{i=1}^{n}P_i$$
$$P_{AND} \approx \prod_{i=1}^{n}P_i$$

## 重要性度量

### Birnbaum重要性
$$I_B(i) = P(\text{部件i故障} | \text{顶事件发生})$$

### 临界重要度
$$I_C(i) = \frac{P_i}{P_T} \times I_B(i)$$

## 错误代码

| 错误码 | 说明 |
|--------|------|
| E001 | 无效的节点类型 |
| E002 | 基本事件缺少概率值 |
| E003 | 顶事件未定义 |
| E004 | 节点ID重复 |
| E005 | 边引用了未定义的节点 |
| E006 | 检测到循环引用 |
| E007 | 概率值超出有效范围 |
