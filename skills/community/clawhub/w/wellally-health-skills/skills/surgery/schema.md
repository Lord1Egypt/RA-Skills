# Surgery Record Schema

个人手术历史记录的完整数据结构定义。

## Schema 文件

完整的 JSON Schema 定义：[schema.json](schema.json)

## 字段速查

### 必填字段

| 字段 | 类型 | 说明 |
|-----|------|-----|
| `id` | string | 手术记录唯一标识符 (surgery_YYYYMMDD_HHMMSS) |
| `basic_info.surgery_name` | string | 手术全称 (医学术语) |
| `basic_info.surgery_date` | string | 手术日期 (YYYY-MM-DD) |
| `basic_info.preoperative_diagnosis` | string | 术前诊断 |
| `basic_info.body_part` | enum | 手术部位 |
| `implants.has_implants` | boolean | 是否有植入物 |

### 手术类型 (surgery_type)

`elective` (择期手术) | `emergency` (急诊手术) | `day_surgery` (日间手术) | `diagnostic` (诊断性手术) | `therapeutic` (治疗性手术) | `palliative` (姑息手术) | `reconstructive` (重建手术)

### 麻醉方式 (anesthesia_type)

`general` (全身麻醉) | `local` (局部麻醉) | `spinal` (腰麻) | `epidural` (硬膜外) | `nerve_block` (神经阻滞) | `mac` (监测下麻醉护理) | `other` (其他)

### 手术部位 (body_part)

`头部` | `颈部` | `胸部` | `腹部` | `背部` | `脊柱` | `上肢` | `下肢` | `盆腔` | `会阴` | `全身` | `其他`

### 植入物类型

- 人工关节/植入物
- 支架/导管
- 金属内固定物 (钢板、螺钉、钢针等)
- 人工瓣膜/起搏器
- 疝修补片/补片
- 其他植入物

## 数据存储

- 位置: `data/手术记录/YYYY-MM/YYYY-MM-DD_手术名称.json`
- 格式: JSON 对象
- 模式: 新建文件
