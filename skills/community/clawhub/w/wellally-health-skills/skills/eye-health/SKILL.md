---
name: eye-health
description: Manage comprehensive eye health tracking including vision records, intraocular pressure, fundus exams, eye disease screening, habits, and checkup reminders. Use for vision monitoring, glaucoma/cataract screening, and eye care management.
argument-hint: <操作类型 视力/眼压/检查结果，如：vision left 1.0 right 0.8>
allowed-tools: Read, Write
schema: eye-health/schema.json
---

# Eye Health Management Skill

Comprehensive vision monitoring, eye examination, and eye disease screening management.

## Medical Safety Disclaimer

This system is for health monitoring records only and cannot replace professional medical diagnosis and treatment.

**Cannot Do:**
- Do not provide specific ophthalmic treatment plans
- Do not recommend prescription medications or surgical plans
- Do not diagnose eye diseases or determine prognosis
- Do not replace professional ophthalmologist examinations

**Can Do:**
- Provide vision monitoring records and trend analysis
- Provide eye examination records and reminders
- Provide eye disease screening records (for reference only)
- Provide eye care habit recommendations and medical visit reminders

## 核心流程

```
用户输入 → 识别操作类型 → [vision/iop/fundus] 解析数值 → 保存记录
                              ↓
                         [screening] 解析结果 → 评估风险 → 保存
                              ↓
                         [habit] 解析习惯 → 提供建议 → 保存
                              ↓
                         [status/trend/checkup] 读取数据 → 显示报告
```

## 步骤 1: 解析用户输入

### 操作类型识别

| Input Keywords | Operation Type |
|----------------|----------------|
| vision | vision - Record vision exam |
| iop | iop - Record intraocular pressure |
| fundus | fundus - Record fundus exam |
| screening | screening - Eye disease screening |
| habit | habit - Record eye care habits |
| status | status - View eye health status |
| trend | trend - View vision trends |
| checkup | checkup - Checkup reminders |
| medication | medication - Eye medication |

## 步骤 2: 解析数值

### 视力数值解析

| Input | Uncorrected VA | Corrected VA |
|-----|---------------|--------------|
| left 1.0 right 0.8 | Left 1.0 Right 0.8 | - |
| uncorrected 0.5 | 0.5 | - |
| corrected 1.2 | - | 1.2 |
| sphere -3.5 cylinder -0.5 axis 180 | - | Refraction |

### 眼压解析

| Input | Left Eye | Right Eye | Reference |
|-----|----------|-----------|-----------|
| left 15 right 16 | 15 | 16 | 10-21 mmHg |
| 15 16 | 15 | 16 | Normal range |

### 眼底检查结果解析

| Input | Result |
|-----|--------|
| normal | Normal |
| diabetic_mild | Diabetic retinopathy (mild) |
| hypertensive_grade_1 | Hypertensive retinopathy (grade 1) |
| amd_drusen | Macular degeneration (drusen) |

### 筛查结果解析

| Screening Type | Result Values |
|----------------|--------------|
| glaucoma | negative/suspect/early/moderate/advanced |
| cataract | none/grade_1/grade_2/grade_3/mature |
| amd | none/early/intermediate/late |
| diabetic_retinopathy | none/mild/moderate/severe/proliferative |
| dry_eye | none/mild/moderate/severe |

## 步骤 3: 检查信息完整性

### vision 必填:
- 至少提供一只眼的视力值或屈光度数

### iop 必填:
- 左眼和右眼的眼压值

### fundus 必填:
- 检查结果（正常或异常描述）

### screening 必填:
- 筛查类型和结果

## 步骤 4: 生成 JSON

### 视力记录数据结构

```json
{
  "id": "vision_20250102000001",
  "date": "2025-01-02",
  "left_eye": {
    "uncorrected_va": 0.5,
    "corrected_va": 1.0,
    "sphere": -3.50,
    "cylinder": -0.50,
    "axis": 180
  },
  "right_eye": {
    "uncorrected_va": 0.4,
    "corrected_va": 1.0,
    "sphere": -4.00,
    "cylinder": -0.75,
    "axis": 175
  },
  "exam_type": "routine",
  "created_at": "2025-01-02T00:00:00.000Z"
}
```

### 眼压记录数据结构

```json
{
  "id": "iop_20250102000001",
  "date": "2025-01-02",
  "time": "10:00",
  "left_iop": 15,
  "right_iop": 16,
  "measurement_method": "goldmann_applanation_tonometer",
  "reference_range": "10-21"
}
```

## 步骤 5: 保存数据

1. 读取 `data/eye-health-tracker.json`
2. 更新对应记录段
3. 写回文件

## 视力分级参考

| Uncorrected VA | Assessment | Estimated Myopia (Reference) |
|---------------|------------|---------------------------|
| 1.0-1.5 | Normal | 0 ~ -0.5D |
| 0.8-0.9 | Mild decrease | -0.5D ~ -1.5D |
| 0.4-0.7 | Moderate decrease | -1.5D ~ -3.0D |
| 0.1-0.3 | Severe decrease | -3.0D ~ -6.0D |
| <0.1 | Very severe decrease | >-6.0D (high myopia) |

## 眼压参考值

| Category | IOP (mmHg) |
|----------|------------|
| Normal | 10-21 |
| Elevated | 22-25 |
| Suspected glaucoma | 26-30 |
| Possible glaucoma | >30 |

## 筛查频率建议

### Adult Routine Checkup
- 18-40 years: Every 2 years
- 40-60 years: Every 1-2 years
- >60 years: Annually

### High Risk Groups
- Diabetes: Annual fundus exam
- Hypertension: Annual fundus exam
- High myopia (>-6.0D): Annual fundus exam
- Glaucoma family history: Annual IOP and visual field exam |

更多示例参见 [examples.md](examples.md)。
