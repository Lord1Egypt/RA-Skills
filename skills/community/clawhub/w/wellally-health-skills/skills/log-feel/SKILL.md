---
name: log-feel
description: Log health/wellness feelings with structured output. Use when user describes physical symptoms, pain, discomfort, or health sensations. Interactively asks for missing details when needed.
argument-hint: <自然语言描述，如：肚子不舒服，左腹疼痛，疼痛感1>
allowed-tools: Read, Write
schema: log-feel/schema.json
---

# Health Feeling Logging Skill

Interactively record health feelings, converting natural language into structured JSON and saving.

## 核心流程

```
用户输入 → 解析信息 → 检查完整性 → [信息不足] 询问补充 → 生成JSON → 保存
                                          ↓
                                     [信息完整]
```

## 步骤 1: 解析用户输入

从用户输入中提取所有可用信息，映射到以下字段：

### 关键词映射

#### Body Part (bodyPart)

| Input Keywords | Value |
|---------------|-------|
| left abdomen | left_abdomen |
| right abdomen | right_abdomen |
| abdomen, stomach | abdomen |
| upper abdomen | upper_abdomen |
| head, headache | head |
| neck | neck |
| shoulder | shoulder |
| back | back |
| chest | chest |
| lower abdomen | lower_abdomen |
| arm | arm |
| left hand | left_hand |
| right hand | right_hand |
| leg, thigh | leg |
| left leg | left_leg |
| right leg | right_leg |
| foot | foot |
| whole body | whole_body |

#### Pain Level (painLevel + severity)

| Input | painLevel | severity |
|-------|-----------|----------|
| pain 1, level 1, mild | "1" | 1 |
| pain 2, level 2 | "2" | 2 |
| pain 3, level 3, moderate | "3" | 3 |
| pain 4, level 4 | "4" | 4 |
| pain 5, level 5, severe | "5" | 5 |
| pain 6, level 6 | "6" | 6 |
| pain 7, level 7 | "7" | 7 |
| pain 8, level 8 | "8" | 8 |
| pain 9, level 9 | "9" | 9 |
| pain 10, level 10, intense | "10" | 10 |

#### Pain Type (painType)

| Input | Value |
|-------|-------|
| dull ache, dull pain | dull |
| sharp, stabbing | sharp |
| bloating | bloating |
| colic | colic |
| vague pain | vague |
| burning | burning |
| throbbing | throbbing |
| no pain, painless | none |

## 步骤 2: 检查信息完整性

### Must Have (ask if missing):
- `symptom` - Symptom description

### Recommended (ask if missing):
- `bodyPart` - Body part (skip if can be inferred)
- `painLevel` / `severity` - Pain level (if pain is mentioned but no level given)

### Optional (do not ask):
- `painType` - Pain type
- `duration` - Duration
- `triggers` - Triggers
- `reliefFactors` - Relief factors
- `accompanyingSymptoms` - Accompanying symptoms
- `mood` - Mood
- `energyLevel` - Energy level
- `notes` - Notes
- `tags` - Tags

## 步骤 3: 交互式询问（信息不足时）

**采用面诊式对话风格**：友好、自然、一次问一个问题。

### 对话原则
- 像医生问诊一样，用日常语言交流
- 每次只问 1-2 个相关问题
- 根据用户回答自然引导下一问
- 避免机械的选项罗列

### 询问场景示例

#### Scenario A: Missing Symptom Description
```
OK, can you tell me in detail where you're feeling uncomfortable?
```

#### Scenario B: Missing Body Part
```
Is it on the left, right, upper, or lower side of your abdomen?
```

#### Scenario C: Pain Mentioned But Level Missing
```
How severe is the pain? If we rate it on a scale of 1 to 10,
where 1 is almost no feeling and 10 is unbearable pain,
what would you rate it?

#### 场景 D: 多个缺失信息（逐步询问）
```
第1问: 哪里不舒服？
用户: 肚子

第2问: 肚子的哪个位置？左边、右边、上面还是下面？
用户: 左边

第3问: 疼得厉害吗？1-10分的话大概几分？
用户: 3分吧
```

### Pain Level Reference (internal use, do not show to user)

| Level | Score | Description |
|-------|-------|-------------|
| Almost no sensation | 1 | Barely noticeable |
| Mild discomfort | 2 | Uncomfortable but doesn't affect activity |
| Mild pain | 3 | Slight pain, can be ignored |
| Moderate pain | 4 | Noticeable discomfort, occasionally noticed |
| Significant pain | 5 | Pain is obvious, affects attention |
| Heavy pain | 6 | Pain is significant, requires endurance |
| Severe pain | 7 | Pain is severe, affects daily activities |
| Intense pain | 8 | Intense pain, hard to concentrate |
| Extreme pain | 9 | Extreme pain, can barely do anything |
| Unbearable | 10 | Unbearable pain, needs immediate treatment |

## 步骤 4: 生成 JSON

信息完整后，生成符合 Schema 的 JSON：

```json
{
  "timestamp": "2026-02-03T10:30:00Z",
  "bodyPart": "left_abdomen",
  "symptom": "abdominal discomfort",
  "painLevel": "1",
  "severity": 1,
  "painType": "vague",
  "tags": ["pain", "abdomen"]
}
```

完整 Schema 定义参见 [schema.json](schema.json)。

## 步骤 5: 保存数据

1. 读取 `data/health-feeling-logs.json`
2. 将新记录追加到数组末尾
3. 写回文件

## 执行指令

```
1. 解析用户输入，提取所有可用信息
2. 检查必填字段（symptom）和建议字段（bodyPart, painLevel）
3. 如有缺失，使用 AskUserQuestion 询问用户
4. 生成符合 schema.json 的 JSON
5. 追加保存到 data/health-feeling-logs.json
6. 向用户确认保存成功，并显示摘要
```

## 示例交互

### 完整输入（无需询问）
```
用户: 肚子不舒服，左腹，轻微疼痛
→ 直接解析并保存
```

### 不完整输入（需要询问）
```
用户: 肚子疼
AI: 哪个部位疼？（左腹、右腹、上腹、下腹？）
用户: 左腹
AI: 疼痛程度如何？（1-10级）
用户: 2级
→ 解析并保存
```

更多示例参见 [examples.md](examples.md)。
