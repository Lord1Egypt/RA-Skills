# 托书字段定义（Booking Note Schema）

> 本文档定义 `shipping-booking` skill 的标准输出格式，适用于海运托书（Booking Note / Shipping Instruction / 订舱委托书）的结构化提取场景。

---

## 完整 JSON 输出示例

```json
{
  "shipper_name": "SHENZHEN ABC TRADING CO., LTD.",
  "shipper_address": "ROOM 1001, TOWER A, NO.88 SHENNAN RD, FUTIAN DISTRICT, SHENZHEN, CHINA",
  "consignee_name": "XYZ LOGISTICS PVT. LTD.",
  "consignee_address": "NO.123, MG ROAD, BANGALORE 560001, INDIA",
  "notify_name": "SAME AS CONSIGNEE",
  "notify_address": null,
  "pol": "SHANGHAI",
  "transit_port": null,
  "pod": "NHAVA SHEVA",
  "carrier": "ONE",
  "vessel": "YM UNICORN",
  "voyage": "075W",
  "etd": "2025-05-15",
  "eta": "2025-06-10",
  "cargo_description": "SPARE PARTS OF WATERJET LOOMS",
  "hs_code": "84484290",
  "marks": "N/M",
  "pieces": "150 CTNS",
  "gross_weight": "3500.00 KGS",
  "volume": "22.5 CBM",
  "is_dangerous": false,
  "un_number": null,
  "dangerous_class": null,
  "containers": [
    { "type": "20GP", "quantity": 1 }
  ],
  "freight_terms": "PREPAID",
  "reference_number": "BK2025051500123",
  "confidence": "high",
  "low_confidence_fields": []
}
```

---

## 字段详细说明

### 发货人（Shipper）

| 字段 | 类型 | 说明 |
|------|------|------|
| `shipper_name` | string | 发货人公司名称，对应托书 Shipper / 托运人 标签。**注意**：托书右上角的货代公司名不是发货人，不要混入此字段 |
| `shipper_address` | string | 发货人详细地址，通常包含电话、邮箱等联系信息，原样保留 |

### 收货人（Consignee）

| 字段 | 类型 | 说明 |
|------|------|------|
| `consignee_name` | string | 收货人公司名称 |
| `consignee_address` | string | 收货人详细地址 |

### 通知人（Notify Party）

| 字段 | 类型 | 说明 |
|------|------|------|
| `notify_name` | string | 通知人名称。常见值：`SAME AS CONSIGNEE`（与收货人相同）|
| `notify_address` | string \| null | 通知人地址。若与收货人相同通常填 null |

### 港口与航线

| 字段 | 类型 | 说明 |
|------|------|------|
| `pol` | string | 起运港（Port of Loading），如 `SHANGHAI`、`NINGBO`、`SHENZHEN` |
| `transit_port` | string \| null | 中转港（Transshipment Port），直达航线为 null |
| `pod` | string | 目的港（Port of Discharge），如 `NHAVA SHEVA`、`SINGAPORE`、`ROTTERDAM` |

### 船期信息

| 字段 | 类型 | 说明 |
|------|------|------|
| `carrier` | string \| null | 船公司名称，如 `ONE`、`MSC`、`COSCO`、`MAERSK`、`CMA CGM`、`EVERGREEN` |
| `vessel` | string \| null | 船名，如 `YM UNICORN`、`COSCO SHIPPING ARIES` |
| `voyage` | string \| null | 航次号，如 `075W`、`2024E` |
| `etd` | string \| null | 预计开船日期，格式 `YYYY-MM-DD`。客户尚未确认船期时为 null |
| `eta` | string \| null | 预计到港日期，格式 `YYYY-MM-DD`。客户尚未确认船期时为 null |

> 💡 `vessel`、`voyage`、`etd`、`eta` 经常为 null —— 客户发来托书时往往还未确认具体船期，这是正常现象，不代表提取失败。

### 货物信息

| 字段 | 类型 | 说明 |
|------|------|------|
| `cargo_description` | string | 货物描述，原样保留，不翻译。支持中英文混排 |
| `hs_code` | string \| null | 海关 HS 编码（Harmonized System Code）。多品类时用分号分隔，如 `84484290; 44199090` |
| `marks` | string \| null | 唛头（Marks & Numbers），常见值 `N/M`（无唛头）|
| `pieces` | string \| null | 件数，含单位，如 `150 CTNS`、`698 PKGS`、`14 PALLETS` |
| `gross_weight` | string \| null | 毛重，含单位，如 `3500.00 KGS`、`12,250 KGS` |
| `volume` | string \| null | 体积，含单位，如 `22.5 CBM`、`68 CBM` |

### 危险品信息

| 字段 | 类型 | 说明 |
|------|------|------|
| `is_dangerous` | boolean | 是否为危险品，默认 `false` |
| `un_number` | string \| null | 危险品 UN 编号，如 `UN1263`。非危险品为 null |
| `dangerous_class` | string \| null | 危险品分类，如 `Class 3`（易燃液体）、`Class 8`（腐蚀品）。非危险品为 null |

### 箱型箱量

```json
"containers": [
  { "type": "20GP", "quantity": 1 },
  { "type": "40HQ", "quantity": 2 }
]
```

| 字段 | 说明 |
|------|------|
| `type` | 箱型。常见值：`20GP`（20尺普柜）、`40GP`（40尺普柜）、`40HQ`（40尺高柜）、`45HQ`（45尺高柜）、`20RF`（20尺冷箱）、`40RF`（40尺冷箱） |
| `quantity` | 箱量，整数 |

> 支持多箱型混装，如 `1×20GP + 2×40HQ` 会输出两个元素的数组。

### 运费与参考号

| 字段 | 类型 | 说明 |
|------|------|------|
| `freight_terms` | string \| null | 运费条款。常见值：`PREPAID`（预付）、`COLLECT`（到付）、`AS ARRANGED` |
| `reference_number` | string \| null | 客户参考号或订舱号，原样保留，不修改任何字符 |

### 置信度

| 字段 | 类型 | 说明 |
|------|------|------|
| `confidence` | string | 整体置信度：`high` / `medium` / `low` |
| `low_confidence_fields` | array | 不确定的字段名列表，建议人工复核 |

---

## 置信度规则

| 级别 | 判断标准 | 建议操作 |
|------|---------|---------|
| `high` | 6 个核心字段（shipper_name / consignee_name / pol / pod / cargo_description / containers）全部提取成功 | 可直接入系统 |
| `medium` | 核心字段大部分提取成功，少量次要字段（如 vessel/etd）缺失 | 确认低置信度字段后入系统 |
| `low` | 核心字段多个缺失，或文档质量差（模糊扫描件、非标格式） | 建议人工重新核对原件 |

---

## 日期格式规范

所有日期统一转换为 `YYYY-MM-DD`：

| 原始格式 | 转换结果 |
|---------|---------|
| `25 APR 2025` | `2025-04-25` |
| `25/04/2025` | `2025-04-25` |
| `APR.25.2025` | `2025-04-25` |
| `2025.04.25` | `2025-04-25` |
| `25-APR-25` | `2025-04-25` |

---

## 特殊情况处理

| 情况 | 处理方式 |
|------|---------|
| 字段在托书中未填写 | 输出 `null` |
| 通知人与收货人相同 | `notify_name` 输出 `SAME AS CONSIGNEE`，`notify_address` 输出 `null` |
| 多品类货物 | `cargo_description` 用分号或换行拼接，`hs_code` 同样用分号分隔 |
| 危险品 | `is_dangerous` 为 `true`，填写 `un_number` 和 `dangerous_class` |
| 文件不是托书 | `confidence` 输出 `invalid`，脚本报错退出 |
| 多箱型混装 | `containers` 数组包含多个元素 |
