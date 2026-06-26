# 场景配置规范

## 目录

- [概述](#概述)
- [配置结构](#配置结构)
- [预设场景](#预设场景)
- [配置参数](#配置参数)

## 概述

场景模式允许用户通过一条指令触发多个车辆控制操作。本文档定义场景配置的 JSON Schema 和使用规范。

## 配置结构

### 完整 Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["name", "commands"],
  "properties": {
    "name": {
      "type": "string",
      "description": "场景名称（英文标识）"
    },
    "display_name": {
      "type": "object",
      "description": "多语言显示名称",
      "properties": {
        "zh-CN": "回家模式",
        "en-US": "Go Home Mode",
        "ja-JP": "ホームモード"
      }
    },
    "description": {
      "type": "string",
      "description": "场景描述"
    },
    "icon": {
      "type": "string",
      "description": "图标标识"
    },
    "trigger_keywords": {
      "type": "array",
      "description": "触发关键词（多语言）",
      "items": {
        "type": "object",
        "properties": {
          "lang": {"type": "string"},
          "keywords": {"type": "array", "items": {"type": "string"}}
        }
      }
    },
    "conditions": {
      "type": "array",
      "description": "执行条件",
      "items": {
        "type": "object",
        "properties": {
          "type": {"enum": ["engine_status", "speed", "time", "location"]},
          "operator": {"enum": ["eq", "ne", "lt", "gt", "in"]},
          "value": {}
        }
      }
    },
    "commands": {
      "type": "array",
      "description": "控制指令序列",
      "items": {
        "type": "object",
        "required": ["action"],
        "properties": {
          "action": {"type": "string"},
          "target": {"type": "string"},
          "parameters": {"type": "object"},
          "delay": {"type": "integer", "description": "延迟执行（毫秒）"},
          "condition": {"type": "string", "description": "执行条件表达式"}
        }
      }
    },
    "on_failure": {
      "type": "string",
      "enum": ["continue", "rollback", "stop"],
      "default": "continue",
      "description": "失败处理策略"
    }
  }
}
```

## 预设场景

### 回家模式 (go_home)

```json
{
  "name": "go_home",
  "display_name": {
    "zh-CN": "回家模式",
    "en-US": "Go Home Mode",
    "ja-JP": "ホームモード"
  },
  "description": "自动设置导航回家，开启空调和座椅加热",
  "icon": "home",
  "trigger_keywords": [
    {"lang": "zh-CN", "keywords": ["回家", "回家模式", "送我回家"]},
    {"lang": "en-US", "keywords": ["go home", "go-home", "head home"]}
  ],
  "conditions": [
    {"type": "engine_status", "operator": "eq", "value": "running"},
    {"type": "speed", "operator": "eq", "value": 0}
  ],
  "commands": [
    {
      "action": "navigation_set_destination",
      "parameters": {"type": "home"}
    },
    {
      "action": "climate_on",
      "target": "all",
      "parameters": {"mode": "auto"},
      "delay": 2000
    },
    {
      "action": "climate_set",
      "parameters": {"temperature": 22},
      "delay": 1000
    },
    {
      "action": "seat_heat",
      "target": "driver",
      "parameters": {"level": 2},
      "delay": 3000
    },
    {
      "action": "turn_signal_left",
      "parameters": {"duration": 3}
    }
  ],
  "on_failure": "continue"
}
```

### 上班模式 (go_work)

```json
{
  "name": "go_work",
  "display_name": {
    "zh-CN": "上班模式",
    "en-US": "Work Mode"
  },
  "description": "导航到公司，关闭不必要的耗电设备",
  "icon": "briefcase",
  "trigger_keywords": [
    {"lang": "zh-CN", "keywords": ["上班", "上班模式", "去公司"]},
    {"lang": "en-US", "keywords": ["go to work", "work mode"]}
  ],
  "conditions": [
    {"type": "engine_status", "operator": "eq", "value": "running"}
  ],
  "commands": [
    {
      "action": "navigation_set_destination",
      "parameters": {"type": "work"}
    },
    {
      "action": "climate_on",
      "parameters": {"mode": "auto"}
    },
    {
      "action": "window_close",
      "target": "all"
    }
  ],
  "on_failure": "continue"
}
```

### 休息模式 (rest_mode)

```json
{
  "name": "rest_mode",
  "display_name": {
    "zh-CN": "休息模式",
    "en-US": "Rest Mode"
  },
  "description": "熄火等待时使用，保持舒适环境",
  "icon": "moon",
  "trigger_keywords": [
    {"lang": "zh-CN", "keywords": ["休息", "休息模式", "小憩"]},
    {"lang": "en-US", "keywords": ["rest", "rest mode", "take a break"]}
  ],
  "conditions": [
    {"type": "engine_status", "operator": "eq", "value": "off"},
    {"type": "speed", "operator": "eq", "value": 0}
  ],
  "commands": [
    {
      "action": "seat_position_set",
      "parameters": {"position": "recline"}
    },
    {
      "action": "climate_on",
      "parameters": {"mode": "auto", "fan_speed": 1}
    },
    {
      "action": "climate_set",
      "parameters": {"temperature": 24}
    },
    {
      "action": "door_lock",
      "parameters": {"from_outside": false}
    },
    {
      "action": "window_close",
      "target": "all"
    }
  ],
  "on_failure": "continue"
}
```

### 快速降温 (quick_cool)

```json
{
  "name": "quick_cool",
  "display_name": {
    "zh-CN": "快速降温",
    "en-US": "Quick Cool"
  },
  "description": "夏日快速降低车内温度",
  "icon": "snowflake",
  "trigger_keywords": [
    {"lang": "zh-CN", "keywords": ["太热了", "降温", "快速降温", "凉快一下"]},
    {"lang": "en-US", "keywords": ["too hot", "cool down", "quick cool"]}
  ],
  "commands": [
    {
      "action": "climate_on",
      "parameters": {"mode": "cool", "fan_speed": 7}
    },
    {
      "action": "climate_set",
      "parameters": {"temperature": 18}
    },
    {
      "action": "window_open",
      "target": "sunroof",
      "parameters": {"position": "vent"},
      "delay": 1000
    },
    {
      "action": "window_open",
      "target": "all",
      "parameters": {"position": "vent"},
      "delay": 3000
    },
    {
      "action": "window_close",
      "target": "all",
      "delay": 60000
    },
    {
      "action": "climate_set",
      "parameters": {"temperature": 24},
      "delay": 120000
    }
  ],
  "on_failure": "continue"
}
```

### 露营模式 (camping_mode)

```json
{
  "name": "camping_mode",
  "display_name": {
    "zh-CN": "露营模式",
    "en-US": "Camping Mode"
  },
  "description": "车内过夜使用，保持通风和舒适温度",
  "icon": "tent",
  "trigger_keywords": [
    {"lang": "zh-CN", "keywords": ["露营", "露营模式", "过夜"]},
    {"lang": "en-US", "keywords": ["camping", "camping mode", "overnight"]}
  ],
  "conditions": [
    {"type": "engine_status", "operator": "eq", "value": "off"},
    {"type": "speed", "operator": "eq", "value": 0}
  ],
  "commands": [
    {
      "action": "window_open",
      "target": "sunroof",
      "parameters": {"position": "vent"}
    },
    {
      "action": "window_open",
      "target": "rear_left",
      "parameters": {"position": "vent"}
    },
    {
      "action": "window_open",
      "target": "rear_right",
      "parameters": {"position": "vent"}
    },
    {
      "action": "climate_on",
      "parameters": {"mode": "auto", "fan_speed": 1}
    },
    {
      "action": "climate_set",
      "parameters": {"temperature": 23}
    },
    {
      "action": "seat_position_set",
      "target": "rear",
      "parameters": {"position": "flat"}
    },
    {
      "action": "interior_light",
      "parameters": {"mode": "off"}
    },
    {
      "action": "door_lock",
      "parameters": {"from_outside": false}
    }
  ],
  "on_failure": "continue"
}
```

## 配置参数

### 常用参数值

| 参数 | 可选值 | 说明 |
|------|--------|------|
| position | foreaft, height, recline | 座椅位置参数 |
| level | 0-3 | 加热/通风级别 |
| temperature | 16-30 | 温度（摄氏度） |
| fan_speed | 0-7 | 风速级别 |
| mode | auto, cool, heat, defrost | 空调模式 |
| direction | face, feet, face_feet, defrost | 出风方向 |

### 条件操作符

| operator | 说明 |
|----------|------|
| eq | 等于 |
| ne | 不等于 |
| lt | 小于 |
| gt | 大于 |
| in | 在范围内 |

### 导航目的地类型

| type | 说明 |
|------|------|
| home | 家庭地址 |
| work | 公司地址 |
| favorite_1 ~ 5 | 收藏地点 |
| current | 当前位置 |
