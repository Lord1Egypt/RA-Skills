# Nutrition Tracker Schema

营养分析与补充剂管理的完整数据结构定义。

## Schema 文件

完整的 JSON Schema 定义：[schema.json](schema.json)

## 字段速查

### 餐型 (type)

`breakfast` (早餐) | `lunch` (午餐) | `dinner` (晚餐) | `snack` (加餐) | `morning_snack` (上午加餐) | `afternoon_snack` (下午加餐) | `evening_snack` (晚间加餐) | `late_night_snack` (夜宵)

### 宏量营养素

| 字段 | 说明 | 单位 |
|-----|------|-----|
| `calories` | 卡路里 | kcal |
| `protein_g` | 蛋白质 | g |
| `carbs_g` | 碳水化合物 | g |
| `fat_g` | 脂肪 | g |
| `fiber_g` | 膳食纤维 | g |

### 微量营养素 - 维生素

| 字段 | 说明 | 单位 |
|-----|------|-----|
| `vitamin_a_mcg` | 维生素A | μg |
| `vitamin_c_mg` | 维生素C | mg |
| `vitamin_d_mcg` | 维生素D | μg |
| `vitamin_e_mg` | 维生素E | mg |
| `vitamin_k_mcg` | 维生素K | μg |
| `vitamin_b1_mg` | 维生素B1 (硫胺素) | mg |
| `vitamin_b2_mg` | 维生素B2 (核黄素) | mg |
| `vitamin_b3_mg` | 维生素B3 (烟酸) | mg |
| `vitamin_b6_mg` | 维生素B6 | mg |
| `vitamin_b12_mcg` | 维生素B12 | μg |
| `folate_mcg` | 叶酸 | μg |

### 微量营养素 - 矿物质

| 字段 | 说明 | 单位 |
|-----|------|-----|
| `calcium_mg` | 钙 | mg |
| `iron_mg` | 铁 | mg |
| `magnesium_mg` | 镁 | mg |
| `phosphorus_mg` | 磷 | mg |
| `potassium_mg` | 钾 | mg |
| `sodium_mg` | 钠 | mg |
| `zinc_mg` | 锌 | mg |
| `selenium_mcg` | 硒 | μg |

### 特殊营养素

| 字段 | 说明 | 单位 |
|-----|------|-----|
| `omega_3_g` | Omega-3脂肪酸 | g |
| `omega_6_g` | Omega-6脂肪酸 | g |
| `choline_mg` | 胆碱 | mg |
| `fiber_soluble_g` | 可溶性纤维 | g |
| `fiber_insoluble_g` | 不溶性纤维 | g |

### 补充剂频次 (frequency)

`daily` (每日) | `weekly` (每周) | `as_needed` (按需) | `other` (其他)

### 服用时间 (timing)

`breakfast` (早餐后) | `lunch` (午餐后) | `dinner` (晚餐后) | `bedtime` (睡前) | `with_meal` (随餐) | `empty_stomach` (空腹) | `other` (其他)

## 每日推荐摄入量 (RDA) 参考

| 营养素 | 成年男性 | 成年女性 | 单位 |
|-------|---------|---------|-----|
| 维生素A | 900 | 700 | μg |
| 维生素C | 90 | 75 | mg |
| 维生素D | 15 | 15 | μg |
| 维生素E | 15 | 15 | mg |
| 钙 | 1000 | 1000 | mg |
| 铁 | 8 | 18 | mg |
| 镁 | 420 | 320 | mg |
| 锌 | 11 | 8 | mg |

## 数据存储

- 位置: `data/nutrition-tracker.json`
- 格式: JSON 对象
- 模式: 更新
