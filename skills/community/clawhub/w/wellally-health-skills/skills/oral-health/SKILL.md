---
name: oral-health
description: Manage oral health tracking including dental checkups, treatment records, hygiene habits, problem monitoring, and screening. Use for dental visit records, cavity tracking, gum health, and oral care management.
argument-hint: <操作类型 牙科信息，如：checkup 2025-06-10 牙齿检查 16号牙有龋齿>
allowed-tools: Read, Write
schema: oral-health/schema.json
---

# Oral Health Management Skill

Record dental examinations, manage treatment records, track oral health status, and analyze oral health trends.

## Medical Disclaimer

This system is for health tracking and educational purposes only, and does not provide medical diagnosis or treatment advice.

**Cannot Do:**
- All oral health issues should be evaluated by a professional dentist
- Do not handle emergencies (severe toothache, trauma, etc.)
- Cannot replace professional dental examination and treatment

**Can Do:**
- Record and track oral health data
- Provide dental examination records and reminders
- Provide oral health assessment
- Provide general oral care recommendations

## 核心流程

```
用户输入 → 识别操作类型 → [checkup] 解析检查结果 → 保存记录
                              ↓
                         [treatment] 解析治疗信息 → 保存记录
                              ↓
                         [hygiene] 解析习惯 → 更新记录 → 保存
                              ↓
                         [issue] 解析问题 → 保存记录
                              ↓
                         [status/trend/reminder] 读取数据 → 显示报告
```

## 步骤 1: 解析用户输入

### 操作类型识别

| Input Keywords | Operation Type |
|---------------|----------------|
| checkup | checkup - Checkup record |
| treatment | treatment - Treatment record |
| hygiene | hygiene - Oral hygiene habits |
| issue | issue - Oral problem |
| status | status - View status |
| trend | trend - Trend analysis |
| reminder | reminder - Checkup reminder |
| screening | screening - Disease screening |

## 步骤 2: 参数解析规则

### Tooth Numbering (FDI System)

| User Input | Tooth |
|-----------|------|
| 16, tooth 16 | 16 (upper right first molar) |
| 26, tooth 26 | 26 (upper left first molar) |
| 36, tooth 36 | 36 (lower left first molar) |
| 46, tooth 46 | 46 (lower right first molar) |

### 治疗类型识别

| Input Keywords | Type |
|---------------|------|
| filling | filling |
| root_canal | root_canal |
| extraction | extraction |
| implant | implant |
| crown | crown |
| bridge | bridge |
| denture | denture |
| orthodontic | orthodontic |
| scaling | scaling |
| periodontal | periodontal |

### 口腔问题类型

| Input Keywords | Type |
|---------------|------|
| toothache | toothache |
| bleeding | bleeding |
| ulcer | ulcer |
| sensitivity | sensitivity |
| swelling | swelling |
| bad_breath | bad_breath |
| dry_mouth | dry_mouth |
| clicking | clicking |

### Severity

| Input | Severity |
|-------|----------|
| mild | mild |
| moderate | moderate |
| severe | severe |

## 步骤 3: 生成 JSON

### 检查记录数据结构

```json
{
  "id": "checkup_20250610_001",
  "date": "2025-06-10",
  "teeth_status": {
    "16": { "condition": "caries", "note": "Decay" },
    "26": { "condition": "filling", "note": "Filled" }
  },
  "periodontal_status": {
    "bleeding_on_probing": false,
    "probing_depth": "2-3mm",
    "gingival_recession": "none"
  },
  "soft_tissue": "normal",
  "occlusion": "normal",
  "tmj": "normal",
  "examined_by": "",
  "notes": "Regular checkup recommended"
}
```

### 治疗记录数据结构

```json
{
  "id": "treatment_20250610_001",
  "date": "2025-06-10",
  "tooth_number": "26",
  "treatment_type": "filling",
  "material": "composite_resin",
  "cost": 300,
  "anesthesia": "local",
  "notes": "Composite resin filling"
}
```

### 卫生习惯数据结构

```json
{
  "last_updated": "2025-06-10",
  "brushing": {
    "frequency": "twice_daily",
    "method": "bass_method",
    "duration_minutes": 2
  },
  "flossing": {
    "frequency": "daily",
    "time": "evening"
  },
  "mouthwash": {
    "frequency": "sometimes",
    "type": "fluoride"
  }
}
```

## 步骤 4: 保存数据

1. 读取 `data/oral-health-tracker.json`
2. 更新对应记录段
3. 写回文件

## FDI牙位标记法

### 恒牙编号（1-32）
- 右上象限：18 17 16 15 14 13 12 11
- 左上象限：21 22 23 24 25 26 27 28
- 左下象限：38 37 36 35 34 33 32 31
- 右下象限：48 47 46 45 44 43 42 41

### 乳牙编号（51-85）
- 右上象限：55 54 53 52 51
- 左上象限：61 62 63 64 65
- 左下象限：75 74 73 72 71
- 右下象限：85 84 83 82 81

## Hygiene Score

| Score | Description |
|-------|-------------|
| 9-10 | Excellent: Brushing 2+ times daily, flossing daily, regular cleanings |
| 7-8 | Good: Brushing 2 times daily, flossing 3+ times weekly |
| 5-6 | Fair: Brushing 1-2 times daily, occasionally flossing |
| 3-4 | Poor: Brushing once daily, rarely flossing |
| 1-2 | Very Poor: Irregular brushing, no flossing |

## Cavity Risk Level

| Risk | Description |
|------|-------------|
| Low | Low sugar diet, good hygiene habits, fluoride toothpaste, regular checkups |
| Medium | Moderate sugar intake, fair hygiene, occasional fluoride products |
| High | High sugar diet, poor hygiene, irregular checkups, history of cavities |

## Periodontal Health Classification

| Grade | Description |
|-------|-------------|
| Healthy | No bleeding, probing depth 1-3mm, no attachment loss |
| Gingivitis | Bleeding on probing, probing depth 3-4mm |
| Mild Periodontitis | Probing depth 4-5mm, mild attachment loss |
| Moderate Periodontitis | Probing depth 5-6mm, moderate attachment loss |
| Severe Periodontitis | Probing depth >6mm, severe attachment loss |

## Emergency Guide

### Requires Emergency Care (within 24 hours)
- Severe toothache unrelieved by medication
- Trauma causing tooth loss or fracture
- Facial swelling, especially with fever
- Excessive gum bleeding that won't stop

### Needs Prompt Care (within 1 week)
- Persistent toothache over 3 days
- Mouth ulcer not healing after 2 weeks
- Unknown lump or white patch in mouth

### Routine Appointment (within 1 month)
- Regular checkup and cleaning
- Mild tooth sensitivity
- Cosmetic dental consultation

更多示例参见 [examples.md](examples.md)。
