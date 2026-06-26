# ScreeningTracker Schema

妇科癌症筛查追踪的完整数据结构定义。

## 字段速查

### 核心字段

| 字段 | 类型 | 说明 |
|-----|------|-----|
| `cervical_cancer` | object | 宫颈癌筛查记录 |
| `tumor_markers` | object | 肿瘤标志物 |
| `abnormal_result_followup` | array | 异常结果随访 |
| `upcoming_appointments` | array | 即将到来的预约 |

## cervical_cancer 对象

### HPV检测字段

| 字段 | 类型 | 说明 |
|-----|------|-----|
| `last_hpv` | string | 最后HPV检测日期 |
| `hpv_result` | enum | negative/positive/not_done |
| `hpv_type` | array | HPV型别数组 |
| `hpv_risk_level` | enum | none/low/moderate/high/very_high |

### TCT检测字段

| 字段 | 类型 | 说明 |
|-----|------|-----|
| `last_tct` | string | 最后TCT检测日期 |
| `tct_result` | enum | NILM/ASC-US/ASC-H/LSIL/HSIL/AGC/Cancer/not_done |
| `tct_result_full` | string | 完整结果描述 |
| `tct_bethesda_category` | string | Bethesda分类 |

### 筛查策略字段

| 字段 | 类型 | 说明 |
|-----|------|-----|
| `screening_strategy` | enum | tct_only/co-testing/hpv_primary |
| `screening_interval` | string | 筛查间隔 |
| `next_screening` | string | 下次筛查日期 |
| `next_screening_type` | string | 下次筛查类型 |

### TCT结果分类（Bethesda系统）

| 结果 | 英文缩写 | 风险 |
|-----|---------|------|
| 阴性 | NILM | 正常 |
| 非典型鳞状细胞，意义不明确 | ASC-US | 低 |
| 非典型鳞状细胞，不除外高级别 | ASC-H | 中-高 |
| 低度鳞状上皮内病变 | LSIL | 低-中 |
| 高度鳞状上皮内病变 | HSIL | 高 |
| 非典型腺细胞 | AGC | 中-高 |
| 癌症 | Cancer | 极高 |

## tumor_markers 对象

### CA125（卵巢癌、子宫内膜癌）

| 字段 | 类型 | 说明 |
|-----|------|-----|
| `current_value` | number | 当前值 |
| `reference_range` | string | 参考值（"<35"） |
| `unit` | string | "U/mL" |
| `last_checked` | string | 最后检测日期 |
| `classification` | enum | normal/elevated/significantly_elevated |
| `trend` | enum | stable/rising/falling |
| `history` | array | 历史记录 |

### CA125分类标准

| 数值 | 分类 | 意义 |
|-----|------|------|
| <35 | normal | 无明显异常 |
| 35-65 | elevated | 轻度升高 |
| 65-100 | elevated | 明显升高 |
| >100 | significantly_elevated | 显著升高 |

### CA19-9（卵巢癌、子宫内膜癌）

| 数值 | 分类 | 意义 |
|-----|------|------|
| <37 | normal | 无明显异常 |
| 37-74 | elevated | 轻度升高 |
| 74-100 | elevated | 明显升高 |
| >100 | significantly_elevated | 显著升高 |

### CEA（子宫内膜癌）

| 数值 | 分类 | 意义 |
|-----|------|------|
| <5 | normal | 非吸烟者正常 |
| 5-10 | elevated | 吸烟者正常/非吸烟者升高 |
| >10 | elevated | 明显升高 |

### AFP（卵黄囊瘤）

| 数值 | 分类 | 意义 |
|-----|------|------|
| <10 | normal | 无明显异常 |
| >=10 | elevated | 需要评估 |

## abnormal_result_followup 数组项

| 字段 | 类型 | 说明 |
|-----|------|-----|
| `result_id` | string | 结果记录ID |
| `initial_result.type` | string | 初始结果类型 |
| `initial_result.hpv_type` | string | HPV型别 |
| `follow_up.type` | string | 随访方式 |
| `follow_up.result` | string | 随访结果 |
| `status` | enum | pending/in_progress/resolved/treated/lost_to_followup |

## 数据存储

- 位置: `data/screening-tracker.json`
