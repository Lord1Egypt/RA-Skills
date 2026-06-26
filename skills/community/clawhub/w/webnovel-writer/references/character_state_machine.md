# 角色状态机模板

每部小说应维护 `character_states.json`，用于结构化追踪角色动态状态。
角色状态包含两层：**状态层**（位置/知识/物品）和**弧线层**（成长阶段/性格演变/关系变化）。

## 文件格式

```json
{
  "陆远": {
    "first_appearance": 1,
    "role": "主角",
    "pov": true,
    "base_info": {
      "age": 28,
      "job": "永盛集团分析师",
      "personality": "冷静、理性、好奇心强"
    },
    "snapshots": {
      "1": {
        "location": "永盛集团12层办公区",
        "knows": ["自己能看到死亡倒计时", "孙磊的倒计时异常"],
        "not_knows": ["倒计时的真正原因", "永盛的秘密"],
        "has": ["手机", "工牌"],
        "emotional_state": "震惊、恐惧",
        "relationships": {
          "孙磊": "同事，关系一般",
          "赵恒": "大学好友，远程联系"
        }
      },
      "2": {
        "location": "永盛集团食堂",
        "knows": ["孙磊的倒计时消失了"],
        "not_knows": ["为什么消失"],
        "has": ["手机", "工牌", "孙磊给的数据盘"],
        "emotional_state": "困惑、警觉",
        "key_events": ["发现孙磊余额变为空白"]
      }
    }
  },
  "孙磊": {
    "first_appearance": 1,
    "role": "关键配角",
    "pov": false,
    "base_info": {
      "age": 35,
      "job": "永盛集团高级经理"
    },
    "snapshots": {
      "1": {
        "location": "永盛集团",
        "knows": [],
        "not_knows": ["陆远能看到倒计时"],
        "has": ["数据盘"],
        "emotional_state": "正常",
        "countdown": "42年137天"
      },
      "9": {
        "countdown": "空白（已消失）",
        "emotional_state": "未知（未出场）"
      }
    }
  }
}
```

## 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| first_appearance | int | 首次出场章节 |
| role | string | 角色定位（主角/核心配角/配角/路人） |
| pov | bool | 是否有视角（能否描写内心） |
| base_info | object | 不变的基础信息 |
| snapshots | object | 每章的状态快照，key为章节号（字符串） |

### snapshot 字段

| 字段 | 必填 | 说明 |
|------|------|------|
| location | 是 | 角色当前所在位置 |
| knows | 是 | 角色目前已知道的信息列表 |
| not_knows | 是 | 角色尚不知道的信息（防剧透） |
| has | 是 | 角色持有的关键物品 |
| emotional_state | 是 | 当前情绪状态 |
| relationships | 否 | 当前与其他角色的关系 |
| key_events | 否 | 本章发生在此角色身上的关键事件 |
| countdown | 否 | 特殊机制数值（如倒计时、余额） |

## 维护规则

1. **每章写完必须更新** 所有出场角色的 snapshot
2. **只更新出场角色** — 未出场的角色保持上一章状态不变
3. **knows 只增不减** — 角色获得的信息不能"忘记"（除非有剧情原因）
4. **not_knows 要同步移除** — 角色获知信息后从 not_knows 移到 knows
5. **has 要准确** — 物品获得/丢失/转移都要记录
6. **location 每章更新** — 即使没移动也要确认

## 一致性检查要点

- 角色在A地，但同一章另一角色在同一地点没看到他 → 位置冲突
- 角色做出了基于某信息的决策，但 knows 里没有这个信息 → 知识泄露
- 角色使用了某物品，但 has 里没有 → 物品凭空出现
- 角色情绪与上一章不衔接且没有过渡事件 → 情绪断裂
- 角色行为与其当前成长阶段不符 → 弧线断裂（如处于"怀疑"阶段却主动对抗）
- 角色关系变化没有触发事件 → 关系跳跃

---

# 角色弧线追踪模板

## 概述

状态层追踪"角色在哪里、知道什么、有什么"，弧线层追踪"角色经历了什么变化、成长到哪一步"。两层共享同一个 `character_states.json`，弧线信息存放在角色的 `arc` 字段中。

## 文件格式（arc 部分新增）

```json
{
  "陆远": {
    "first_appearance": 1,
    "role": "主角",
    "pov": true,
    "base_info": {
      "age": 32,
      "job": "投行合伙人",
      "personality": "冷静、理性、好奇心强"
    },
    "arc": {
      "growth_stages": [
        {
          "stage": "隐忍",
          "chapter_range": [1, 30],
          "description": "25年来假装正常，看到余额但不敢干预，三次失败后发誓不再插手",
          "personality_traits": ["过度理性", "自我封闭", "冷幽默掩盖焦虑"],
          "trigger_events": ["发现孙磊余额消失"]
        },
        {
          "stage": "怀疑",
          "chapter_range": [31, 80],
          "description": "主动调查，不再被动接受，开始质疑系统",
          "personality_traits": ["主动", "警觉", "挣扎于理性和直觉之间"],
          "trigger_events": ["发现永盛的秘密入口", "遇到赵恒异常行为"]
        },
        {
          "stage": "确认",
          "chapter_range": [81, 150],
          "description": "完全了解系统运作，开始寻找对抗方法",
          "personality_traits": ["决断", "责任感", "第一次允许自己信任他人"],
          "trigger_events": ["父亲真相揭露"]
        },
        {
          "stage": "对抗",
          "chapter_range": [151, 250],
          "description": "正面挑战系统，承受代价",
          "personality_traits": ["勇敢但脆弱", "愿意牺牲", "与沈清并肩"],
          "trigger_events": ["沈清觉醒能力"]
        },
        {
          "stage": "解决",
          "chapter_range": [251, 372],
          "description": "找到平衡，接受自己，重建生活",
          "personality_traits": ["平和", "接纳", "不再需要伪装"],
          "trigger_events": ["系统终结"]
        }
      ],
      "personality_timeline": [
        {
          "chapter": 1,
          "trait": "冷理性",
          "evidence": "看到孙磊余额异常，第一反应是数据验证而不是恐慌"
        },
        {
          "chapter": 50,
          "trait": "开始信任",
          "evidence": "第一次向沈清透露自己的秘密"
        }
      ],
      "relationship_arcs": {
        "沈清": {
          "stages": [
            {"phase": "陌生人", "chapter_range": [1, 10], "key_event": "业务会面"},
            {"phase": "客户", "chapter_range": [11, 40], "key_event": "合作项目"},
            {"phase": "同谋", "chapter_range": [41, 100], "key_event": "共同发现系统秘密"},
            {"phase": "决裂", "chapter_range": [101, 130], "key_event": "刘阳之死"},
            {"phase": "复合", "chapter_range": [131, 180], "key_event": "沈清觉醒"},
            {"phase": "并肩", "chapter_range": [181, 350], "key_event": "对抗系统"},
            {"phase": "恋人", "chapter_range": [351, 372], "key_event": "重建生活"}
          ]
        },
        "赵恒": {
          "stages": [
            {"phase": "搭档", "chapter_range": [1, 60]},
            {"phase": "怀疑对象", "chapter_range": [61, 100]},
            {"phase": "敌人", "chapter_range": [101, 150]},
            {"phase": "理解", "chapter_range": [151, 200]},
            {"phase": "告别", "chapter_range": [201, 250]}
          ]
        }
      },
      "internal_conflicts": [
        {
          "conflict": "理性 vs 情感",
          "chapter_range": [1, 150],
          "resolution": "学会接受不理性的一面",
          "resolution_chapter": 150
        },
        {
          "conflict": "自我保护 vs 责任",
          "chapter_range": [30, 200],
          "resolution": "选择承担但不再孤军奋战",
          "resolution_chapter": 180
        }
      ],
      "key_turning_points": [
        {"chapter": 1, "event": "发现孙磊余额消失", "impact": "从被动观察转向主动调查"},
        {"chapter": 80, "event": "父亲真相", "impact": "从怀疑转向确认，找到行动方向"},
        {"chapter": 150, "event": "沈清决裂", "impact": "第一次暴露真正的情感需求"}
      ]
    },
    "snapshots": { }
  }
}
```

## arc 字段说明

### 顶层字段

| 字段 | 必填 | 说明 |
|------|------|------|
| growth_stages | 是 | 角色成长阶段列表，至少2个阶段 |
| personality_timeline | 否 | 性格特征变化时间线 |
| relationship_arcs | 否 | 与其他角色的关系演变 |
| internal_conflicts | 否 | 内心冲突及其解决 |
| key_turning_points | 否 | 关键转折点 |

### growth_stages 阶段项

| 字段 | 必填 | 说明 |
|------|------|------|
| stage | 是 | 阶段名称（简短，如"隐忍""怀疑""确认""对抗""解决"） |
| chapter_range | 是 | [起始章, 结束章]，结束章可用 null 表示尚未写到 |
| description | 是 | 该阶段角色的心理状态和行为模式 |
| personality_traits | 是 | 该阶段的3-5个性格关键词 |
| trigger_events | 是 | 推动角色进入下一阶段的关键事件 |

### personality_timeline 性格时间线项

| 字段 | 必填 | 说明 |
|------|------|------|
| chapter | 是 | 性格变化发生的章节 |
| trait | 是 | 新出现/变化的性格特征 |
| evidence | 是 | 正文中的具体表现（用于审校时对照） |

### relationship_arcs 关系弧线

key 为对方角色名，value 的 stages 为关系阶段列表：

| 字段 | 必填 | 说明 |
|------|------|------|
| phase | 是 | 关系阶段名称 |
| chapter_range | 是 | [起始章, 结束章] |
| key_event | 否 | 推动关系变化的关键事件 |

### internal_conflicts 内心冲突项

| 字段 | 必填 | 说明 |
|------|------|------|
| conflict | 是 | 冲突描述（"A vs B"格式） |
| chapter_range | 是 | 冲突持续的章节范围 |
| resolution | 否 | 冲突如何解决 |
| resolution_chapter | 否 | 解决的章节 |

### key_turning_points 转折点项

| 字段 | 必填 | 说明 |
|------|------|------|
| chapter | 是 | 转折发生的章节 |
| event | 是 | 事件描述 |
| impact | 是 | 对角色弧线的影响 |

## 常见成长阶段模板

不同类型小说可参考以下阶段模型：

### 悬疑/推理类
```
无知 → 发现异常 → 调查 → 发现真相 → 对抗 → 解决
```

### 催泪/成长类
```
被推着走 → 建立连接 → 独立判断 → 承受代价 → 自我融合 → 传承
```

### 爽文/逆袭类
```
低谷 → 觉醒 → 爆发 → 瓶颈 → 突破 → 巅峰
```

### 虐恋/感情类
```
相遇 → 确认心意 → 误会/阻碍 → 分离 → 成长 → 重逢/告别
```

## 维护规则

1. **大纲阶段预填** — 开写前根据大纲预填 growth_stages 的阶段名和 chapter_range
2. **每10章回顾** — 检查角色是否按预期推进到下一阶段，如果偏离则记录原因
3. **性格变化必记** — 只要有显著性格变化就追加 personality_timeline
4. **关系变化必记** — 每次关系阶段转换都要更新 relationship_arcs
5. **转折点即时记** — 写完转折章节立即补充 key_turning_points
6. **与 snapshots 配合** — snapshot 记录"此刻的状态"，arc 记录"为什么会变成这样"

## 与状态层的整合

| 层 | 追踪内容 | 更新频率 | 用途 |
|------|------|------|------|
| 状态层 (snapshots) | 位置/知识/物品/情绪 | 每章 | 防止硬性矛盾 |
| 弧线层 (arc) | 成长阶段/性格演变/关系变化 | 每10章+转折点 | 保证角色发展连贯 |

**交叉检查**：
- snapshot.emotional_state 应与 arc 当前阶段的 personality_traits 匹配
- snapshot.knows 的新增信息应与 arc.key_turning_points 的事件对应
- snapshot.relationships 的变化应与 arc.relationship_arcs 的阶段转换一致

## 初始化方法

对新角色或已有角色补充弧线数据：

```bash
# 从大纲提取成长阶段
grep -n "成长\|弧线\|阶段\|转变" 设定集.md

# 从正文提取性格变化证据
grep -n "性格\|变了\|不再\|第一次" chapters/*.md

# 从大纲提取关系变化
# 对照大纲中两人互动的章节，标记关系阶段转换点
```
