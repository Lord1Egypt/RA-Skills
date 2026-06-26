# Drive Engine 驱动引擎

## 核心定位

Drive Engine 是 SMS RPG 的目标与挑战生成系统，承上启下：
- **读取**：World State Graph（世界状态）
- **输出**：Genesis Engine（创世引擎）可执行的结构化目标/挑战数据

**核心使命**：让玩家永远有目标可追，有挑战可克服，维持"能达成但需努力"的张力。

---

## 一、目标系统 (Goal System)

### 1.1 目标层级

```
终极目标 (Ultimate Goal)
    └── 阶段目标 (Phase Goals) [2-3个并行]
            └── 小目标 (Milestones) [3-5个]
                    └── 日常任务 (Dailies) [可选]
```

**各层级职责**：

| 层级 | 数量 | 时间跨度 | 功能 |
|------|------|----------|------|
| 终极目标 | 1个 | 全游戏 | 方向感、终极驱动力 |
| 阶段目标 | 2-3个并行 | 20-40回合 | 中期正反馈来源 |
| 小目标 | 3-5个 | 5-10回合 | 短期成就感 |
| 日常任务 | 可选 | 1-3回合 | 填充空隙 |

### 1.2 目标数据结构

```json
{
  "goalSystem": {
    "ultimateGoal": {
      "id": "goal_ultimate_001",
      "title": "目标名称",
      "description": "目标描述",
      "theme": "cultivation|relationship|power|mystery|revenge",
      "milestones": ["阶段里程碑1", "阶段里程碑2"],
      "currentPhase": 1,
      "totalPhases": 3
    },
    "phaseGoals": [
      {
        "id": "goal_phase_001",
        "title": "阶段目标名称",
        "description": "描述",
        "theme": "cultivation",
        "progress": 0,
        "maxProgress": 100,
        "milestones": [
          {
            "id": "milestone_001",
            "title": "里程碑名称",
            "description": "描述",
            "completed": false,
            "requirements": [
              { "type": "item", "target": "物品ID", "count": 1 },
              { "type": "relationship", "target": "NPC_ID", "minLevel": 80 }
            ]
          }
        ],
        "deadline": null,
        "consequences": {
          "success": "成功后的结果",
          "failure": "失败后的后果"
        }
      }
    ],
    "dailyGoals": [
      {
        "id": "daily_001",
        "title": "日常任务",
        "description": "描述",
        "completed": false,
        "turnsRemaining": 3
      }
    ]
  }
}
```

### 1.3 目标生成规则

**终极目标生成**（游戏开始时）：
- 根据世界观自动生成一个终极目标
- 终极目标应该宏大但有明确的完成路径
- 示例：
  - 武侠修仙："成就无上大道"
  - 朝堂权谋："登基称帝"
  - 千倍返还："集齐九位道侣，觉醒系统真谛"

**阶段目标生成**：
- 每20-40回合需要新阶段目标
- 同时存在2-3个并行阶段目标（不同主题）
- 当一个阶段目标完成，自动生成下一个
- 必须与终极目标相关，但有独立意义

**小目标生成**：
- 每个阶段目标拆解为3-5个小目标
- 每个小目标可在5-10回合内完成
- 完成小目标给予即时反馈

### 1.4 目标完成检测

每回合结束时检测：
1. 检查小目标完成条件
2. 小目标全部完成 → 阶段目标完成
3. 阶段目标完成 → 触发剧情事件，生成新阶段目标
4. 终极目标完成 → 游戏结局

---

## 二、挑战系统 (Challenge System)

### 2.1 挑战类型

```
挑战类型
├── 能力挑战 (Ability Challenge)
│   ├── 修为门槛
│   ├── 技能要求
│   └── 资源门槛
├── 关系挑战 (Relationship Challenge)
│   ├── 心结 (Heart Knot)
│   ├── 外部阻力
│   └── 误解/猜忌
├── 环境挑战 (Environment Challenge)
│   ├── 地点限制
│   ├── 时间限制
│   └── 势力阻挠
└── 随机挑战 (Random Challenge)
    ├── 意外事件
    ├── 突发危机
    └── 敌人袭击
```

### 2.2 挑战数据结构

```json
{
  "challengeSystem": {
    "activeChallenges": [
      {
        "id": "challenge_001",
        "type": "relationship|ability|environment|random",
        "title": "挑战名称",
        "description": "挑战描述",
        "targetGoal": "goal_phase_001",
        "difficulty": 1-10,
        "requirements": {
          "type": "stats|items|relationship|quest",
          "details": {}
        },
        "progress": 0,
        "maxProgress": 100,
        "turnsActive": 0,
        "status": "active|overcome|failed",
        "resolution": {
          "method": "combat|dialogue|item|choice",
          "hints": ["提示1", "提示2"]
        }
      }
    ],
    "resolvedChallenges": []
  }
}
```

### 2.3 心结系统 (Heart Knot)

**心结**是关系类挑战的核心，专用于道侣/重要NPC。

```json
{
  "heartKnot": {
    "npcId": "NPC_ID",
    "name": "心结名称",
    "description": "心结背景描述",
    "type": "trauma|obligation|secret|duty|past",
    "severity": 1-10,
    "symptoms": ["表现1", "表现2"],
    "resolution": {
      "method": "dialogue|event|item|time|quest",
      "requiredSteps": ["步骤1", "步骤2"],
      "currentStep": 0
    },
    "blocksProgressUntil": true
  }
}
```

**心结类型**：

| 类型 | 描述 | 解法示例 |
|------|------|----------|
| trauma | 过去创伤 | 关键事件触发回忆，抚慰与陪伴 |
| obligation | 家族/宗门责任 | 帮助完成责任或证明更重要的事 |
| secret | 隐藏的秘密 | 自然揭露，然后接纳 |
| duty | 使命/誓言 | 共同完成使命，或证明已不再适用 |
| past | 过去的人/事 | 了结过去，或证明现在更重要 |

**心结规则**：
1. 所有重要NPC/潜在道侣必须有至少1个心结
2. 心结未解时，好感度上限为85
3. 心结解开后，好感度可达100+，并触发"心意相通"事件
4. 心结揭示需要时间，不能一次性解决

### 2.4 挑战生成规则

**时机**：
- 新目标生成时，自动生成对应挑战
- 玩家过于顺利时，生成随机挑战
- 特定剧情节点触发特定挑战

**难度控制**：
- 目标难度 = 目标重要性 × 当前回合数/10
- 确保玩家"差一点能达成"
- 挑战可以升级或降级

---

## 三、危机系统 (Crisis System)

### 3.1 危机定义

**危机**是突发的事件性挑战，打破日常节奏，推动剧情。

```json
{
  "crisisSystem": {
    "activeCrisis": null,
    "crisisHistory": [],
    "crisisTemplates": []
  }
}
```

**单个危机数据结构**：

```json
{
  "id": "crisis_001",
  "title": "危机名称",
  "description": "危机描述",
  "type": "enemy|faction|personal|natural|system",
  "severity": 1-10,
  "turnsRemaining": 5,
  "consequences": {
    "timeout": "超时后果",
    "success": "成功后果",
    "failure": "失败后果"
  },
  "options": [
    {
      "id": "option_1",
      "description": "选项描述",
      "requirements": {},
      "successRate": 0.7,
      "successEffect": "成功效果",
      "failureEffect": "失败效果"
    }
  ]
}
```

### 3.2 危机类型

| 类型 | 描述 | 示例 |
|------|------|------|
| enemy | 敌人威胁 | 仇家上门、魔修追杀 |
| faction | 势力冲突 | 宗门内斗、派系争权 |
| personal | 个人危机 | 道侣被抓、资源被抢 |
| natural | 自然灾害 | 灵脉暴动、秘境崩塌 |
| system | 系统事件 | 千倍返还异常、任务触发 |

### 3.3 危机生成规则

**时机**：
- 每15-25回合生成一次危机
- 危机强度随游戏进度增加
- 危机与当前目标相关联

**危机模板示例**：

```yaml
# templates/crises/relationship.yaml
crises:
  - id: "crisis_lover_captured"
    title: "道侣被掳"
    description: "{lover_name}被{enemy_name}带走，生死未卜"
    type: "personal"
    severity: 7
    duration: 5
    triggers:
      - condition: "hasLover AND relationship >= 80"
        weight: 0.3
    consequences:
      timeout: "{lover_name}被带往{enemy_faction}，营救难度大幅增加"
      success: "成功救回{lover_name}，关系大幅提升"
      failure: "营救失败，{lover_name}受伤，关系不变"
```

---

## 四、进度追踪器 (Progress Tracker)

### 4.1 数据结构

```json
{
  "progressTracker": {
    "overallProgress": {
      "cultivation": { "level": 0.65, "trend": "up" },
      "relationships": { "level": 0.45, "trend": "up" },
      "resources": { "level": 0.30, "trend": "stable" },
      "influence": { "level": 0.20, "trend": "up" }
    },
    "goalProgress": [
      {
        "goalId": "goal_phase_001",
        "progress": 0.35,
        "lastUpdate": "turn_42",
        "blockers": ["challenge_001"]
      }
    ],
    "recentAchievements": [
      { "turn": 45, "achievement": "突破元婴初期", "significance": 8 }
    ],
    "warnings": [
      { "type": "stagnation", "area": "relationships", "turns": 10 }
    ]
  }
}
```

### 4.2 追踪规则

**每回合更新**：
1. 计算各维度进度百分比
2. 记录趋势（up/down/stable）
3. 检测停滞（某维度超过10回合无进展）
4. 更新目标进度

**警告触发**：
- 停滞警告：某维度10回合无进展
- 危机预警：危机即将超时
- 目标阻塞：目标被挑战阻塞超过5回合

---

## 五、Drive Engine 工作流

### 5.1 每回合执行流程

```
回合开始
    │
    ├── 1. 检查危机系统
    │       └── 有活跃危机？→ 处理危机逻辑
    │
    ├── 2. 检查挑战系统
    │       └── 有可解决的挑战？→ 提供解决选项
    │
    ├── 3. 检查目标进度
    │       ├── 小目标完成？→ 给予反馈
    │       ├── 阶段目标完成？→ 触发事件
    │       └── 需要新目标？→ 生成新目标
    │
    ├── 4. 更新进度追踪器
    │       └── 计算进度、检测停滞
    │
    ├── 5. 生成剧情（Genesis Engine）
    │       └── 传入目标、挑战、进度数据
    │
    └── 6. 生成选项
            └── 包含目标相关选项、挑战解决选项
```

### 5.2 目标-挑战-剧情联动

```
目标 → 挑战 → 选项 → 剧情
 ↑                      │
 └──────────────────────┘
        反馈循环
```

**示例**：
1. **目标**：与苏清霜建立道侣关系
2. **挑战**：苏清霜有心结（霜华传承的秘密）
3. **选项**：送礼提升好感 + 探听她的过去
4. **剧情**：苏清霜透露一部分信息，好感+5
5. **反馈**：挑战进度+10%，更新目标进度

---

## 六、存档迁移

### 6.1 旧存档结构

```json
{
  "version": "2.0-instruction",
  "worldState": { ... },
  "turnHistory": [ ... ]
}
```

### 6.2 新存档结构

```json
{
  "version": "3.0-drive-engine",
  "worldState": { ... },
  "goalSystem": { ... },
  "challengeSystem": { ... },
  "crisisSystem": { ... },
  "progressTracker": { ... },
  "turnHistory": [ ... ]
}
```

### 6.3 迁移脚本逻辑

1. 读取旧存档
2. 根据 worldState 推断当前目标状态
3. 为重要NPC生成心结
4. 初始化进度追踪器
5. 保存为新格式

---

## 七、模板库

详见 `templates/` 目录：
- `templates/goals/cultivation.yaml` - 修仙类目标模板
- `templates/goals/relationship.yaml` - 关系类目标模板
- `templates/crises/relationship.yaml` - 关系危机模板
- `templates/crises/enemy.yaml` - 敌人危机模板
