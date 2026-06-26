# Vaccination Record Schema

疫苗接种记录和计划管理的完整数据结构定义。

## Schema 文件

完整的 JSON Schema 定义：[schema.json](schema.json)

## 字段速查

### 必填字段

| 字段 | 类型 | 说明 |
|-----|------|-----|
| `id` | string | 疫苗记录唯一标识符 (vax_YYYYMMDDHHmmssSSS) |
| `vaccine_info.name` | string | 疫苗名称 |
| `series_info.total_doses` | integer | 总剂次数 |
| `series_info.current_dose` | integer | 当前剂次 |
| `doses` | object[] | 剂次列表 |

### 疫苗剂型 (dose_form)

`injection` (注射) | `oral` (口服) | `nasal` (鼻喷) | `other` (其他)

### 接种途径 (route)

`intramuscular` (肌肉注射) | `subcutaneous` (皮下注射) | `oral` (口服) | `intranasal` (鼻内) | `other` (其他)

### 接种部位 (site)

`left_arm` (左上臂) | `right_arm` (右上臂) | `left_thigh` (左大腿) | `right_thigh` (右大腿) | `buttock` (臀部) | `other` (其他)

### 接种程序类型 (schedule_type)

`0-1-6` | `0-2-6` | `2-6` | `annual` (年度) | `single` (单次)

### 剂次状态 (status)

`completed` (已完成) | `scheduled` (已计划) | `missed` (漏种) | `cancelled` (取消)

### 系列状态 (series_status)

`pending` (待开始) | `in_progress` (进行中) | `completed` (已完成) | `cancelled` (已取消)

### 不良反应严重程度 (severity)

`mild` (轻度) | `moderate` (中度) | `severe` (重度)

## 疫苗接种程序

| 程序 | 说明 | 剂次间隔 |
|-----|------|---------|
| 0-1-6 | 出生、1月龄、6月龄 | 1个月、5个月 |
| 0-2-6 | 出生、2月龄、6月龄 | 2个月、4个月 |
| 2-6 | 2月龄、6月龄 | 4个月 |
| annual | 年度接种 | 12个月 |

## 数据存储

- 位置: `data/vaccinations.json`
- 格式: JSON 对象
- 模式: 更新
