---
name: fall
description: Fall risk assessment for elderly including fall history recording, balance tests (TUG/Berg/single-leg-stance), gait analysis, home safety evaluation, and prevention recommendations.
argument-hint: <操作类型 跌倒详情/测试结果，如：record 2025-03-15 bathroom slippery_floor bruise>
allowed-tools: Read, Write
schema: fall/schema.json
---

# Fall Risk Assessment Skill

Manage fall risk assessment for elderly, including fall history records, balance function tests, gait analysis, and home environment safety assessment.

## Medical Safety Disclaimer

**Safety Boundaries:**
1. Do not handle post-fall injuries - fall injuries require immediate medical attention
2. Do not replace professional balance function assessment - balance tests require guidance from rehabilitation therapists
3. Do not provide specific rehabilitation training prescriptions - rehabilitation requires professional assessment

**Can Do:**
- Fall risk factor assessment
- Balance function test records (TUG/Berg/single-leg-stance)
- Gait analysis records
- Home environment safety assessment
- Fall prevention recommendations

## 核心流程

```
用户输入 → 识别操作类型 → [record] 解析跌倒事件 → 更新风险 → 保存
                              ↓
                         [tug/berg/single-leg-stance/gait] 解析测试结果 → 评估 → 保存
                              ↓
                         [home] 解析环境评估 → 更新建议 → 保存
                              ↓
                         [risk/risk-factors/interventions] 读取数据 → 显示报告
```

## 步骤 1: 解析用户输入

### 操作类型识别

| Input Keywords | Operation Type |
|---------------|----------------|
| record | record - Record fall event |
| history | history - View fall history |
| tug | tug - TUG test |
| berg | berg - Berg balance scale |
| single-leg-stance | single-leg-stance - Single leg stance test |
| gait | gait - Gait analysis |
| home | home - Home environment assessment |
| risk | risk - Fall risk assessment |
| risk-factors | risk-factors - View risk factors |
| interventions | interventions - Intervention recommendations |

## 步骤 2: 参数解析规则

### 跌倒事件 (record)

| Parameter | Extraction Rule |
|-----------|----------------|
| Date | `(\d{4}-\d{2}-\d{2})` or "today" |
| Location | bathroom, bedroom, living_room, kitchen, stairs |
| Cause | slippery_floor, trip, loss_balance, dizziness, weak |
| Injury | none, bruise, cut, fracture, head_injury |

### TUG测试 (tug)

| Time (s) | Result |
|----------|--------|
| <10 | Normal |
| 10-19 | Basically normal |
| 20-29 | Mobility limited |
| >=30 | Dependent |

### Berg平衡量表 (berg)

| Score | Result |
|-------|--------|
| 0-20 | Wheelchair required |
| 21-40 | Assistive walking required |
| 41-56 | Independent walking |

### 单腿站立 (single-leg-stance)

| Age | Normal Time (s) |
|-----|----------------|
| <60 | >30 |
| 60-69 | >15 |
| 70-79 | >5 |
| >=80 | >3 |

### 步态分析 (gait)

| Gait Speed (m/s) | Result |
|-----------------|--------|
| >1.0 | Normal |
| 0.6-1.0 | Mobility limited |
| <0.6 | Severely limited |

### 步态异常类型

| Keyword | Type |
|---------|------|
| shortened_step | Shortened step |
| widened_base | Widened base |
| unsteady_gait | Unsteady gait |
| shuffling | Shuffling |
| asymmetric | Asymmetric |

### 居家环境评估 (home)

#### Living Room
- floor_slippery - Slippery floor
- adequate_lighting - Adequate lighting
- obstacles_removed - Obstacles removed
- rugs_secure - Rugs secured

#### Bedroom
- bedside_light - Bedside lamp
- night_light - Night light
- bed_height_appropriate - Appropriate bed height
- clutter_free - Clutter-free

#### Bathroom
- non_slip_mat - Non-slip mat
- grab_bars - Grab bars
- shower_chair - Shower chair
- easy_access - Easy access

#### Stairs
- handrails - Handrails
- non_slip_treads - Non-slip treads
- adequate_lighting - Adequate lighting
- clutter_free - Clutter-free |

## 步骤 3: 生成 JSON

### 跌倒记录数据结构

```json
{
  "id": "fall_20250315_001",
  "date": "2025-03-15",
  "time": "10:30",
  "location": "bathroom",
  "cause": "slippery_floor",
  "injury_level": "bruise",
  "description": "在浴室因地滑跌倒，轻微擦伤",
  "required_medical_attention": false
}
```

### TUG测试数据结构

```json
{
  "id": "tug_20250315_001",
  "date": "2025-03-15",
  "time_seconds": 18,
  "interpretation": "基本正常",
  "fall_risk": "低风险"
}
```

### 居家环境评估数据结构

```json
{
  "last_assessed": "2025-03-15",
  "living_room": {
    "floor_slippery": false,
    "adequate_lighting": true,
    "obstacles_removed": true,
    "rugs_secure": true
  },
  "bathroom": {
    "non_slip_mat": true,
    "grab_bars": true,
    "shower_chair": false,
    "easy_access": true
  },
  "recommendations": [
    "建议在浴室安装淋浴椅",
    "确保卧室床头灯可用"
  ]
}
```

## 步骤 4: 风险评估

### Risk Factor Calculation

**Low risk (0-5 points):** All risk factors are under control
**Medium risk (6-12 points):** Multiple risk factors exist, need attention and intervention
**High risk (13-18 points):** Serious risk factors exist, immediate action required

### Risk Factors
- Age (>75 years)
- Past fall history
- Balance dysfunction
- Gait abnormality
- Muscle weakness
- Vision problems
- Cognitive impairment
- Medications (>4 types)
- Chronic diseases (>3 types)
- Home environmental hazards

## 步骤 5: 保存数据

1. 读取 `data/fall-risk-assessment.json`
2. 更新对应记录段
3. 重新计算 overall_risk
4. 写回文件

更多示例参见 [examples.md](examples.md)。
