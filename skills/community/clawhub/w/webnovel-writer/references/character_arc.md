# 角色弧线追踪模板

角色弧线追踪与状态机互补：状态机追踪"角色在哪、知道什么、有什么"（外部状态），弧线追踪"角色变成了谁"（内部演变）。

## 一、弧线追踪文件格式

每部小说维护 `character_arcs.json`，与 `character_states.json` 同级。

```json
{
  "陆远": {
    "arc_overview": {
      "start_trait": "封闭、过度理性、不敢建立亲密关系",
      "end_trait": "学会信任、接受不完美、愿意为爱冒险",
      "core_conflict": "25年孤独vs渴望被理解",
      "total_phases": 4
    },
    "phases": [
      {
        "id": "isolation",
        "name": "孤岛期",
        "chapter_range": [1, 50],
        "trait_snapshot": "理性到冷血，拒绝所有人靠近",
        "behavior_patterns": ["遇事先计算概率", "用冷幽默回避情感", "独处时焦虑但绝不示人"],
        "trigger_to_next": "沈清的出现打破了他的计算逻辑"
      },
      {
        "id": "cracking",
        "name": "裂痕期",
        "chapter_range": [51, 120],
        "trait_snapshot": "开始犹豫、偶尔感性，但立刻自我否定",
        "behavior_patterns": ["做决定时会想'沈清会怎么看'", "第一次主动分享秘密", "噩梦增多"],
        "trigger_to_next": "刘阳之死让他质疑理性是否有意义"
      },
      {
        "id": "breaking",
        "name": "破碎期",
        "chapter_range": [121, 200],
        "trait_snapshot": "理性外壳崩塌，暴露脆弱和愤怒",
        "behavior_patterns": ["不再说'正常营业'", "主动寻求帮助", "情绪失控频率增加"],
        "trigger_to_next": "接受父亲的遗产，理解孤独不是宿命"
      },
      {
        "id": "rebuilding",
        "name": "重建期",
        "chapter_range": [201, 300],
        "trait_snapshot": "带着伤疤但选择信任，理性与感性并存",
        "behavior_patterns": ["愿意展示弱点", "为爱做不理性的决定但不后悔", "能用幽默化解而不是回避"],
        "trigger_to_next": null
      }
    ],
    "current_phase": "isolation",
    "phase_transitions": [
      {
        "from_phase": "isolation",
        "to_phase": "cracking",
        "chapter": null,
        "event": null,
        "completed": false
      }
    ]
  }
}
```

### 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| arc_overview | object | 弧线总览：起点性格、终点性格、核心冲突、阶段总数 |
| phases | array | 性格演变阶段列表，按顺序排列 |
| phases[].id | string | 阶段唯一标识（用于状态机关联） |
| phases[].name | string | 阶段中文名（如"孤岛期"） |
| phases[].chapter_range | [int,int] | 预计章节范围（可调整） |
| phases[].trait_snapshot | string | 该阶段性格特征一句话描述 |
| phases[].behavior_patterns | [string] | 该阶段的典型行为模式（写作时对照） |
| phases[].trigger_to_next | string/null | 进入下一阶段的触发事件描述 |
| current_phase | string | 当前所处阶段的 id |
| phase_transitions | array | 已发生的阶段转换记录 |

## 二、关系演变追踪

在 `character_arcs.json` 中为每对重要关系维护演变轨迹：

```json
{
  "relationship_arcs": {
    "陆远×沈清": {
      "trajectory": ["客户", "对手", "同谋", "决裂", "理解", "恋人", "战友"],
      "current_stage": "客户",
      "milestones": [
        {
          "stage": "对手",
          "chapter": null,
          "event": "商业谈判中的正面冲突",
          "completed": false
        },
        {
          "stage": "同谋",
          "chapter": null,
          "event": "共同发现永盛的秘密",
          "completed": false
        }
      ],
      "tension_level": "低",
      "trust_score": 1
    },
    "陆远×赵恒": {
      "trajectory": ["搭档", "怀疑", "真相", "原谅", "生死之交"],
      "current_stage": "搭档",
      "milestones": [],
      "tension_level": "低",
      "trust_score": 7
    }
  }
}
```

### 字段说明

| 字段 | 说明 |
|------|------|
| trajectory | 关系演变的完整路径（从起点到终点） |
| current_stage | 当前处于哪个阶段 |
| milestones | 每个阶段转换的具体事件记录 |
| tension_level | 当前张力等级（低/中/高/极高） |
| trust_score | 信任度 1-10（10为完全信任） |

### 常见关系演变模式

| 模式 | 轨迹示例 | 适用场景 |
|------|----------|----------|
| 缓慢建立信任 | 陌生→试探→合作→信任→生死相托 | 主角团队 |
| 先甜后苦 | 热恋→裂痕→背叛→敌对 | 反转角色 |
| 宿敌变盟友 | 敌对→理解→尊重→合作 | 对手角色 |
| 背叛与救赎 | 信任→背叛→孤立→赎罪→原谅 | 复杂配角 |

## 三、性格变化检测

写作时用以下规则检测角色行为是否符合当前阶段：

### 检测逻辑

```
IF 角色处于"孤岛期"（trait: 封闭、理性）:
  ✅ 合理行为：拒绝帮助、用数据说话、独来独往
  ⚠️ 需铺垫：偶尔流露温柔（必须有触发事件）
  ❌ 不合理：主动倾诉、轻易信任陌生人、情感失控

IF 角色处于"裂痕期"（trait: 犹豫、偶尔感性）:
  ✅ 合理行为：犹豫不决、事后后悔感性、试探性靠近
  ⚠️ 需铺垫：完全信任他人（还不够）
  ❌ 不合理：回到完全封闭（已回不去了）
```

### 检测规则模板（写入 consistency_check.py 的扩展）

```python
# 性格一致性检测规则
ARC_BEHAVIOR_RULES = {
    "isolation": {
        "allowed": ["理性决策", "冷幽默", "回避亲密", "独自行动"],
        "needs_setup": ["流露感情", "主动求助", "表达信任"],
        "forbidden": ["情感失控", "无条件信任", "主动倾诉内心"]
    },
    "cracking": {
        "allowed": ["犹豫", "矛盾", "试探性信任", "事后自我否定"],
        "needs_setup": ["完全信任", "理性决策（恢复）"],
        "forbidden": ["完全回到封闭", "无条件信任"]
    },
    "breaking": {
        "allowed": ["情绪失控", "愤怒", "主动求助", "展示脆弱"],
        "needs_setup": ["理性回归"],
        "forbidden": ["完美理性决策", "假装无事发生"]
    },
    "rebuilding": {
        "allowed": ["有限度信任", "带着伤疤前行", "理性与感性并存"],
        "needs_setup": [],
        "forbidden": ["回到完全封闭", "无条件信任所有人"]
    }
}
```

### Agent 检测指令

写完每章后，对照角色的 `current_phase`，检查：
1. 角色行为是否匹配当前阶段的 `behavior_patterns`
2. 如果角色出现了 `needs_setup` 中的行为，是否有充分的触发事件
3. 如果出现了 `forbidden` 中的行为，标记为**性格断裂bug**

## 四、与状态机的整合方式

### 架构关系

```
character_states.json（状态机）    character_arcs.json（弧线）
├── location                        ├── arc_overview
├── knows / not_knows               ├── phases + current_phase
├── has                             ├── relationship_arcs
├── emotional_state                 └── （性格阶段信息）
└── relationships（简述）
          ↓ 互相引用 ↓
    snapshots[X].arc_phase = "isolation"
    phases[X].chapter_range 覆盖 snapshot 章节
```

### 整合规则

1. **状态机 snapshot 新增 `arc_phase` 字段**：每章 snapshot 标注角色当前所处的弧线阶段
   ```json
   "snapshots": {
     "5": {
       "arc_phase": "isolation",
       "location": "...",
       ...
     }
   }
   ```

2. **弧线阶段变更时同步更新**：当角色经历触发事件进入新阶段时，同时更新两个文件：
   - `character_arcs.json`：更新 `current_phase`，记录 `phase_transitions`
   - `character_states.json`：后续 snapshot 的 `arc_phase` 字段改为新阶段

3. **关系信息双向同步**：
   - 状态机 `relationships` 记录简要关系描述（向后兼容）
   - 弧线文件 `relationship_arcs` 记录详细演变轨迹和张力

4. **一致性检查联动**：consistency_check.py 同时读取两个文件：
   - 状态机检查：位置冲突、知识泄露、物品凭空出现
   - 弧线检查：性格断裂、关系跳跃、阶段回退

### 文件读写顺序

```
每章写完后：
1. 更新 character_states.json（snapshot）
2. 检查是否有弧线阶段变更 → 有则更新 character_arcs.json
3. 检查是否有关系阶段变更 → 有则更新 relationship_arcs
4. 运行 consistency_check.py 验证一致性
```

## 五、具体示例

### 示例1：陆远（悬疑类小说主角）

```json
{
  "陆远": {
    "arc_overview": {
      "start_trait": "封闭、过度理性、25年孤独让他不相信任何人",
      "end_trait": "学会信任、接受不完美、愿意为所爱之人冒险",
      "core_conflict": "理性自保vs情感渴望",
      "total_phases": 4
    },
    "phases": [
      {
        "id": "isolation",
        "name": "孤岛期",
        "chapter_range": [1, 50],
        "trait_snapshot": "冷静到冷血，看到所有人倒计时却从不干预",
        "behavior_patterns": [
          "永远说'正常营业'",
          "用概率和数据解释一切",
          "深夜失眠但不让任何人知道",
          "8块钱牛肉面是他唯一的'人情味'"
        ],
        "trigger_to_next": "沈清让他意识到有些事算不清概率"
      },
      {
        "id": "cracking",
        "name": "裂痕期",
        "chapter_range": [51, 120],
        "trait_snapshot": "理性外壳出现裂缝，开始有计算之外的冲动",
        "behavior_patterns": [
          "第一次对别人的倒计时产生情绪反应",
          "开始主动调查而不是被动观察",
          "试探性地向赵恒透露更多信息",
          "偶尔忘了说'正常营业'"
        ],
        "trigger_to_next": "刘阳之死——他计算对了但人还是死了"
      },
      {
        "id": "breaking",
        "name": "破碎期",
        "chapter_range": [121, 200],
        "trait_snapshot": "理性完全失效，被迫面对情感和信任",
        "behavior_patterns": [
          "不再假装冷静",
          "主动寻求沈清的帮助",
          "做出'不理性'的选择但不后悔",
          "第一次为别人流泪（不是7岁的自己）"
        ],
        "trigger_to_next": "理解父亲的牺牲，接受孤独不是命运"
      },
      {
        "id": "rebuilding",
        "name": "重建期",
        "chapter_range": [201, 300],
        "trait_snapshot": "理性仍在但不再排斥感性，带着伤疤信任",
        "behavior_patterns": [
          "该算的算，该赌的赌",
          "不再回避'爱'这个字",
          "偶尔还能冷幽默，但底色是温暖的",
          "愿意展示脆弱，因为沈清接住了"
        ],
        "trigger_to_next": null
      }
    ],
    "current_phase": "isolation",
    "phase_transitions": []
  },
  "relationship_arcs": {
    "陆远×沈清": {
      "trajectory": ["客户", "对手", "同谋", "决裂", "理解", "恋人", "战友"],
      "current_stage": "客户",
      "milestones": [],
      "tension_level": "低",
      "trust_score": 2
    },
    "陆远×赵恒": {
      "trajectory": ["搭档", "怀疑", "真相", "原谅", "生死之交"],
      "current_stage": "搭档",
      "milestones": [],
      "tension_level": "低",
      "trust_score": 7
    }
  }
}
```

### 示例2：林昭（催泪类小说主角）

```json
{
  "林昭": {
    "arc_overview": {
      "start_trait": "温暖的普通人，不善社交但真诚，被推着走",
      "end_trait": "独立、有担当、带着999个前世的爱活成最好的自己",
      "core_conflict": "依赖前世vs成为自己",
      "total_phases": 6
    },
    "phases": [
      {
        "id": "passive",
        "name": "被动期",
        "chapter_range": [1, 90],
        "trait_snapshot": "被前世的价值观碰撞推着走，依赖锦囊做决定",
        "behavior_patterns": [
          "遇到困难第一反应是'锦囊怎么说'",
          "对前世言听计从，不敢质疑",
          "社交场合沉默，不敢表达自己",
          "创业决策犹豫，需要前世推一把"
        ],
        "trigger_to_next": "Ch91独立宣言——第一次违抗前世的建议"
      },
      {
        "id": "awakening",
        "name": "觉醒期",
        "chapter_range": [91, 150],
        "trait_snapshot": "开始有自己的判断，但还不坚定",
        "behavior_patterns": [
          "偶尔做出与前世建议相反的决定",
          "事后会怀疑自己是不是错了",
          "开始主动与前世对话而非被动接受",
          "第一次对前世说'不'"
        ],
        "trigger_to_next": "Ch150破茧——彻底独立"
      },
      {
        "id": "independent",
        "name": "独立期",
        "chapter_range": [151, 201],
        "trait_snapshot": "能独立判断，但锦囊能力让他过于依赖",
        "behavior_patterns": [
          "有自己的决策逻辑",
          "锦囊从依赖变成辅助工具",
          "创业开始独当一面",
          "与前世关系从'听令'变成'朋友'"
        ],
        "trigger_to_next": "Ch202锦囊反噬"
      },
      {
        "id": "backlash",
        "name": "反噬期",
        "chapter_range": [202, 219],
        "trait_snapshot": "能力失控，人格分裂征兆，跌入谷底",
        "behavior_patterns": [
          "能力失控导致无法正常工作",
          "前世记忆反噬导致身份混乱",
          "苏晚不离不弃是唯一锚点",
          "学会区分'自己的声音'和'前世的声音'"
        ],
        "trigger_to_next": "Ch218-219融合自我"
      },
      {
        "id": "fusion",
        "name": "融合期",
        "chapter_range": [220, 400],
        "trait_snapshot": "融合前世经验，形成独立人格，有温度的强者",
        "behavior_patterns": [
          "不再需要锦囊做决定，但尊重前世的智慧",
          "创业成功但不忘初心",
          "面对危机有担当，不再逃避",
          "与前世的告别是温暖的而非痛苦的"
        ],
        "trigger_to_next": "失去所有能力"
      },
      {
        "id": "ordinary",
        "name": "凡人期",
        "chapter_range": [401, 502],
        "trait_snapshot": "失去能力成为普通人，但内在强大",
        "behavior_patterns": [
          "没有能力但比有能力时更从容",
          "传承给新持有者",
          "守护空影院——999个空座位是荣耀不是悲伤",
          "和苏晚过上普通生活，珍惜每一天"
        ],
        "trigger_to_next": null
      }
    ],
    "current_phase": "passive",
    "phase_transitions": []
  },
  "relationship_arcs": {
    "林昭×苏晚": {
      "trajectory": ["前女友", "客户", "暧昧", "伴侣", "妻子", "母亲", "灵魂伴侣"],
      "current_stage": "前女友",
      "milestones": [],
      "tension_level": "中",
      "trust_score": 5
    },
    "林昭×何薇": {
      "trajectory": ["邻居", "同事", "合伙人", "铁搭档"],
      "current_stage": "邻居",
      "milestones": [],
      "tension_level": "低",
      "trust_score": 3
    },
    "林昭×001号": {
      "trajectory": ["权威", "导师", "朋友", "告别"],
      "current_stage": "权威",
      "milestones": [],
      "tension_level": "低",
      "trust_score": 6
    },
    "林昭×666号李归墟": {
      "trajectory": ["陌生", "共鸣", "理解", "互相救赎"],
      "current_stage": "陌生",
      "milestones": [],
      "tension_level": "低",
      "trust_score": 1
    }
  }
}
```

## 六、Agent 操作指令

### 初始化弧线文件

```bash
# 在小说目录下创建 character_arcs.json
# 从设定集提取主角和核心配角的信息填入
```

### 每章写完后更新

```bash
# 1. 检查本章是否触发了弧线阶段变更
# 2. 如有变更：更新 current_phase + 记录 phase_transitions + 同步 character_states.json 的 arc_phase
# 3. 检查关系是否有阶段变化 → 更新 relationship_arcs
# 4. 运行一致性检查
```

### 性格一致性检查

写完每章后，对出场角色执行：
1. 读取角色的 `current_phase` 和对应 `behavior_patterns`
2. 检查角色行为是否在 `allowed` 列表中
3. 如果行为在 `needs_setup` 中，检查是否有铺垫
4. 如果行为在 `forbidden` 中，标记为 bug

### 与伏笔管理的联动

弧线阶段转换通常是伏笔回收的好时机：
- 角色进入新阶段时，检查是否有与之相关的伏笔可以回收
- 伏笔的回收可以作为阶段转换的触发事件
