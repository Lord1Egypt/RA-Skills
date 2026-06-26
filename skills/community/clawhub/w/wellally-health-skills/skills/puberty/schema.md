# PubertyTracker Schema

青春期发育评估的完整数据结构定义。

## Schema 文件

完整的JSON Schema定义：[schema.json](schema.json)

## 字段速查

### 根级别字段

| 字段 | 类型 | 说明 |
|-----|------|-----|
| `created_at` | string | ISO 8601 创建时间 |
| `last_updated` | string | ISO 8601 最后更新时间 |
| `puberty_tracking` | object | 青春期追踪数据 |
| `history` | array | 评估历史 |
| `settings` | object | 设置 |

### puberty_tracking 字段

| 字段 | 类型 | 说明 |
|-----|------|-----|
| `gender` | enum/null | 性别：female/male |
| `chronological_age` | number/null | 实际年龄 |
| `female_development` | object | 女孩发育数据 |
| `male_development` | object | 男孩发育数据 |
| `bone_age` | object | 骨龄数据 |
| `assessment` | enum/null | 发育评估 |
| `notes` | string | 备注 |

### female_development 字段

| 字段 | 类型 | 说明 |
|-----|------|-----|
| `breast_stage` | enum | 乳房分期：B1-B5 |
| `breast_stage_age` | number/null | 乳房发育开始年龄 |
| `pubic_hair_stage` | enum | 阴毛分期：P1-P5 |
| `pubic_hair_stage_age` | number/null | 阴毛发育开始年龄 |
| `menarche` | object | 初潮数据 |

### menarche 字段

| 字段 | 类型 | 说明 |
|-----|------|-----|
| `occurred` | bool/null | 是否发生初潮 |
| `age_at_menarche` | number/null | 初潮年龄 |

### male_development 字段

| 字段 | 类型 | 说明 |
|-----|------|-----|
| `testicular_volume` | object | 睾丸体积 |
| `genital_stage` | enum | 生殖器分期：G1-G5 |
| `pubic_hair_stage` | enum | 阴毛分期：P1-P5 |
| `penis_length` | number/null | 阴茎长度（cm） |
| `voice_break` | bool/null | 是否变声 |
| `voice_break_age` | number/null | 变声年龄 |

### bone_age 字段

| 字段 | 类型 | 说明 |
|-----|------|-----|
| `chronological_age` | number/null | 实际年龄 |
| `bone_age` | number/null | 骨龄 |
| `difference` | string/null | 骨龄差 |
| `assessment_date` | string/null | 评估日期 |

## Tanner分期标准

### 女孩乳房发育（B分期）
| 分期 | 描述 | 典型年龄 |
|------|------|---------|
| B1 | 青春期前 | - |
| B2 | 乳房芽萌出 | 8-13岁 |
| B3 | 乳房和乳晕增大 | 10-14岁 |
| B4 | 乳晕突出 | 11-15岁 |
| B5 | 成熟乳房 | 13-18岁 |

### 女孩阴毛发育（P分期）
| 分期 | 描述 | 典型年龄 |
|------|------|---------|
| P1 | 无阴毛 | - |
| P2 | 稀疏、长、色素浅 | 9-14岁 |
| P3 | 变粗、卷曲 | 11-15岁 |
| P4 | 成人型但范围小 | 12-16岁 |
| P5 | 成人型 | 13-18岁 |

### 男孩睾丸发育
| 分期 | 体积 | 典型年龄 |
|------|------|---------|
| G1 | <4ml | 青春期前 |
| G2 | 4-6ml | 9-14岁 |
| G3 | 6-10ml | 10-15岁 |
| G4 | 10-15ml | 11-16岁 |
| G5 | >=15ml | 13-18岁 |

### 男孩阴毛发育（P分期）
| 分期 | 描述 | 典型年龄 |
|------|------|---------|
| P1 | 无阴毛 | - |
| P2 | 稀疏、长、色素浅 | 12-16岁 |
| P3 | 变粗、卷曲 | 13-17岁 |
| P4 | 成人型但范围小 | 14-18岁 |
| P5 | 成人型 | 15-18岁 |

## 性早熟标准

### 性早熟定义
**女孩**: <8岁乳房发育或<10岁初潮
**男孩**: <9岁睾丸增大

### 青春期延迟定义
**女孩**: >13岁无乳房发育或>16岁无初潮
**男孩**: >14岁睾丸未增大

## 骨龄评估

| 骨龄与实际年龄差 | 意义 |
|-----------------|------|
| < -1岁 | 生长延迟 |
| -1 至 +1岁 | 正常范围 |
| > +1岁 | 性早熟/加速生长 |

## 枚举值

### assessment
`normal_progression` (正常发育) | `precocious_puberty` (性早熟) | `delayed_puberty` (发育延迟)

### breast_stage
`B1` | `B2` | `B3` | `B4` | `B5`

### pubic_hair_stage
`P1` | `P2` | `P3` | `P4` | `P5`

### genital_stage
`G1` | `G2` | `G3` | `G4` | `G5`

## 数据存储

- 主文件: `data/puberty-tracker.json`
- 详细记录: `data/青春期记录/YYYY-MM/YYYY-MM-DD_发育记录.json`
- 模式: 更新/追加
