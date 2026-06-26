# SkinHealthTracker Schema

皮肤健康追踪的完整数据结构定义。

## 字段速查

### 核心字段

| 字段 | 类型 | 说明 |
|-----|------|-----|
| `skin_concerns` | array | 皮肤问题记录 |
| `mole_records` | array | 痣的监测记录 |
| `skincare_routines` | array | 护肤程序记录 |
| `skin_exams` | array | 皮肤检查记录 |
| `sun_exposure` | array | 日晒防护和记录 |
| `skin_type` | enum | 皮肤类型 |
| `checkup_reminders` | object | 检查提醒 |
| `skin_health_score` | number | 皮肤健康评分 |

## skin_concerns 数组项

| 字段 | 类型 | 说明 |
|-----|------|-----|
| `issue_type` | enum | 问题类型 |
| `severity` | enum | 严重程度 |
| `location` | enum | 部位 |
| `specific_areas` | array | 具体区域 |
| `description` | string | 描述 |
| `triggers` | array | 诱因 |
| `resolved` | boolean | 是否已解决 |

### issue_type 枚举值
- acne（痤疮）
- eczema（湿疹）
- psoriasis（银屑病）
- pigmentation（色斑）
- rosacea（玫瑰痤疮）
- dermatitis（皮炎）
- dryness（皮肤干燥）
- oiliness（油光）
- sensitivity（敏感）
- scars（疤痕）

## mole_records 数组项

| 字段 | 类型 | 说明 |
|-----|------|-----|
| `location` | enum | 位置 |
| `size_mm` | number | 大小（毫米） |
| `color` | string | 颜色 |
| `shape` | enum | 形状 |
| `abcde_assessment` | object | ABCDE评估 |
| `risk_level` | enum | 风险等级 |
| `needs_followup` | boolean | 需要随访 |

### abcde_assessment 对象

| 字段 | 类型 | 说明 |
|-----|------|-----|
| `asymmetry` | boolean | 不对称 |
| `border` | boolean | 边缘异常 |
| `color` | boolean | 颜色异常 |
| `diameter` | boolean | 直径>6mm |
| `evolution` | boolean | 有变化 |

## skincare_routines 数组项

| 字段 | 类型 | 说明 |
|-----|------|-----|
| `routine_type` | enum | morning/evening/weekly |
| `steps` | array | 护肤步骤 |
| `products_used` | object | 使用的产品 |

### steps 枚举值
- cleanser（洁面乳）
- toner（爽肤水）
- serum（精华液）
- moisturizer（保湿霜）
- spf30/spf50（防晒霜）
- exfoliation（去角质）
- mask（面膜）
- eye_cream（眼霜）

## skin_exams 数组项

| 字段 | 类型 | 说明 |
|-----|------|-----|
| `exam_type` | enum | self/dermatologist/follow_up |
| `findings` | string | 检查发现 |
| `total_moles_count` | int | 痣总数 |
| `suspicious_moles` | int | 可疑痣数量 |
| `recommendations` | array | 建议 |
| `next_exam` | string | 下次检查日期 |

## sun_exposure 数组项

| 字段 | 类型 | 说明 |
|-----|------|-----|
| `record_type` | enum | protection/burn/exposure |
| `protection_used` | array | 防护措施 |
| `burn_severity` | enum | mild/moderate/severe |
| `exposure_duration_hours` | number | 暴露时长 |
| `exposure_level` | enum | low/medium/high |

## skin_type 枚举值

- dry（干性）
- oily（油性）
- combination（混合性）
- normal（中性）
- sensitive（敏感性）

## 数据存储

- 位置: `data/skin-health-tracker.json`
