---
name: voice-vehicle-control
description: 语音控制车辆助手，支持启动熄火、车窗门锁、方向控制、状态查询与场景模式；适用于"帮我发动汽车"、"打开回家模式"或"查询电量"等语音交互场景
---

# 语音车辆控制助手

## 任务目标

本技能用于处理用户的语音车辆控制请求，实现以下能力：

- **基础控制**：车辆启动/熄火、开锁/关锁、开关车窗、天窗/遮阳帘
- **方向控制**：转向灯（左/右/双闪）、行驶方向指引
- **状态查询**：油量、电量、胎压、车门状态、车窗状态、空调状态
- **场景控制**：执行预设场景模式（回家模式、上班模式、休息模式等）
- **多语言交互**：支持中英文及其他语种的语音指令识别与反馈

## 前置准备

- 确保车辆已联网且控制接口可访问
- 用户已完成车辆账号绑定与授权
- 多语言场景下，识别用户语种并使用对应语言反馈

## 操作步骤

### 1. 语音指令解析

接收用户语音或文字指令，按以下流程处理：

1. **意图识别**：判断指令类型
   - 控制指令（我要开车/打开车窗）
   - 查询指令（电量还剩多少/胎压正常吗）
   - 场景指令（开启回家模式）

2. **实体提取**：从指令中提取关键参数
   - 目标对象：车、窗、锁、灯、空调、座椅
   - 操作动作：开/关、启动/熄火、调高/调低
   - 位置方向：左/右、前/后、主驾/副驾

3. **多语言适配**：
   - 检测指令语种
   - 使用对应语种生成反馈

### 2. 车辆控制指令生成

根据解析结果，生成符合车辆控制协议的控制指令。

**基础控制指令格式**：
```json
{
  "command": "vehicle_control",
  "action": "engine_start|engine_stop|door_lock|door_unlock|window_open|window_close|...",
  "target": "all|driver|passenger|rear_left|rear_right|sunroof|...",
  "parameters": {
    "position": "open|close|vent|...",
    "level": 0-100
  }
}
```

详细指令格式参见 [references/vehicle-protocol.md](references/vehicle-protocol.md)。

### 3. 状态查询处理

接收查询请求后，生成查询指令并返回结构化状态信息：

```json
{
  "query": "status_query",
  "items": ["fuel_level", "battery_level", "tire_pressure", "door_status", "..."]
}
```

**返回格式示例**：
```json
{
  "status": "success",
  "data": {
    "fuel_level": {"value": 65, "unit": "%"},
    "battery_level": {"value": 82, "unit": "%"},
    "tire_pressure": {
      "front_left": 2.3,
      "front_right": 2.3,
      "rear_left": 2.2,
      "rear_right": 2.2,
      "unit": "bar"
    },
    "door_status": {
      "driver": "closed",
      "passenger": "closed",
      "rear_left": "closed",
      "rear_right": "closed",
      "trunk": "closed"
    }
  }
}
```

### 4. 场景模式执行

接收场景指令后，解析场景配置并批量执行控制指令。

**场景指令格式**：
```json
{
  "command": "scenario_execute",
  "scenario": "go_home|work|rest|..."
}
```

场景配置规范参见 [references/scenario-config.md](references/scenario-config.md)。

### 5. 结果反馈

根据执行结果，使用用户母语生成自然反馈：

- 成功：确认操作已完成
- 失败：说明原因并提供替代建议
- 部分成功：列出成功项和失败项

## 使用示例

### 示例 1：基础控制

- **场景/输入**："帮我发动汽车" / "Start the car"
- **预期产出**：生成 engine_start 指令并反馈启动结果
- **关键要点**：识别启动同义词（发动、启动、点火）

### 示例 2：状态查询

- **场景/输入**："现在电量还剩多少" / "How much battery left?"
- **预期产出**：查询 battery_level 并返回百分比
- **关键要点**：使用用户语种反馈数值

### 示例 3：场景控制

- **场景/输入**："开启回家模式" / "Activate go-home mode"
- **预期产出**：加载场景配置，依次执行空调开启、座椅加热、导航回家等指令
- **关键要点**：多指令批量执行，按依赖顺序排列

### 示例 4：多语言切换

- **场景/输入**："Ouvrez la fenetre"（法语：打开窗户）
- **预期产出**：解析法语指令，执行 window_open，反馈 "La fenêtre est ouverte"
- **关键要点**：自动检测语种并匹配响应语言

### 示例 5：复杂指令

- **场景/输入**："把主驾窗户开一半，空调调到24度"
- **预期产出**：生成两条控制指令，window_open + climate_set
- **关键要点**：单句多意图识别

## 资源索引

- 车辆控制协议：见 [references/vehicle-protocol.md](references/vehicle-protocol.md)（完整指令格式、响应结构、错误码定义）
- 场景配置规范：见 [references/scenario-config.md](references/scenario-config.md)（场景Schema、预设场景示例）

## 注意事项

- 多意图指令需拆分为独立命令依次执行
- 危险操作（如行驶中开车门）需二次确认
- 状态查询返回空值时，明确告知用户该状态不可用
- 场景执行失败时，回滚已执行操作或提示用户手动处理
