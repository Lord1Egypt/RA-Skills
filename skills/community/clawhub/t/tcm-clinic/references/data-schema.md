# 中医诊所数据表结构参考

本文档定义了 tcm-clinic Skill 中所有 Excel 数据表的字段规范。所有数据存储在 `clinic_data/` 目录下，每个模块对应一个独立的 `.xlsx` 文件。

## 通用约定

- **ID 格式**：各表的主键 ID 格式为 `{模块前缀}{YYYYMMDD}{3位序号}`，例如 `P20260402001`
- **日期格式**：统一使用 `YYYY-MM-DD`，日期时间使用 `YYYY-MM-DD HH:MM`
- **金额格式**：保留两位小数，单位为人民币（元）
- **状态枚举**：见各表备注列的允许值说明
- **空值处理**：字符串类型空值为空字符串 `""`，数值类型空值为 `0`

---

## 1. 患者信息表 (`patients.xlsx`)

文件路径：`clinic_data/patients.xlsx`
工作表名：`patients`

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| patient_id | string | 是 | 患者唯一标识，格式 `P{YYYYMMDD}{3位序号}` |
| name | string | 是 | 患者姓名 |
| gender | string | 是 | 性别：男/女 |
| birth_date | string | 否 | 出生日期，格式 `YYYY-MM-DD` |
| age | int | 否 | 年龄（根据出生日期自动计算，也可手动填写） |
| phone | string | 否 | 联系电话 |
| address | string | 否 | 居住地址 |
| constitution_type | string | 否 | 体质分型：平和质/气虚质/阳虚质/阴虚质/痰湿质/湿热质/血瘀质/气郁质/特禀质 |
| allergies | string | 否 | 过敏史，多项用逗号分隔 |
| chronic_diseases | string | 否 | 慢性病史，多项用逗号分隔 |
| notes | string | 否 | 备注 |
| created_date | string | 是 | 建档日期，格式 `YYYY-MM-DD` |
| last_visit_date | string | 否 | 最近就诊日期，格式 `YYYY-MM-DD` |

**索引字段**：patient_id（主键）、name、phone

---

## 2. 病历记录表 (`medical_records.xlsx`)

文件路径：`clinic_data/medical_records.xlsx`
工作表名：`records`

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| record_id | string | 是 | 记录唯一标识，格式 `R{YYYYMMDD}{3位序号}` |
| patient_id | string | 是 | 关联患者 ID |
| patient_name | string | 是 | 患者姓名（冗余字段，便于查询） |
| visit_date | string | 是 | 就诊日期，格式 `YYYY-MM-DD` |
| chief_complaint | string | 是 | 主诉 |
| tongue_condition | string | 否 | 舌诊：舌色、舌形、舌苔等描述 |
| pulse_condition | string | 否 | 脉诊：脉象描述（如浮脉、沉脉、滑脉等） |
| observation | string | 否 | 望诊记录（面色、神态、体型等） |
| listening_smelling | string | 否 | 闻诊记录（声音、气味等） |
| inquiry | string | 否 | 问诊记录（寒热、出汗、饮食、睡眠、二便等） |
| diagnosis | string | 是 | 诊断（中医病名/证型） |
| prescription | string | 否 | 处方内容（方名或药物组成及剂量） |
| advice | string | 否 | 医嘱（忌口、起居、复诊建议等） |
| visit_count | int | 否 | 该患者累计就诊次数 |
| notes | string | 否 | 备注 |

**索引字段**：record_id（主键）、patient_id、patient_name、visit_date

---

## 3. 中药库存表 (`herbs_inventory.xlsx`)

文件路径：`clinic_data/herbs_inventory.xlsx`
工作表名：`herbs`

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| herb_id | string | 是 | 药材唯一标识，格式 `H{3位序号}` |
| name | string | 是 | 药材名称（如黄芪、当归、白芍等） |
| pinyin | string | 否 | 拼音名（便于检索） |
| specification | string | 否 | 规格描述（如统货、切片、饮片等） |
| stock_quantity | float | 是 | 当前库存量 |
| unit | string | 是 | 单位：g/kg/包/瓶 |
| purchase_price | float | 否 | 进货价（元） |
| retail_price | float | 否 | 零售价（元） |
| supplier | string | 否 | 供应商名称 |
| expiry_date | string | 否 | 保质期截止日期，格式 `YYYY-MM-DD` |
| entry_date | string | 否 | 入库日期，格式 `YYYY-MM-DD` |
| minimum_stock | float | 否 | 最低库存警戒线（低于此值发出补货提醒） |
| category | string | 否 | 分类：补气药/补血药/补阴药/补阳药/清热药/解表药/理气药/活血药/祛湿药/其他 |
| notes | string | 否 | 备注 |

**索引字段**：herb_id（主键）、name、pinyin

---

## 4. 预约排班表 (`appointments.xlsx`)

文件路径：`clinic_data/appointments.xlsx`
工作表名：`appointments`

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| appointment_id | string | 是 | 预约唯一标识，格式 `A{YYYYMMDD}{3位序号}` |
| patient_id | string | 是 | 关联患者 ID |
| patient_name | string | 是 | 患者姓名 |
| appointment_date | string | 是 | 预约日期，格式 `YYYY-MM-DD` |
| time_slot | string | 是 | 预约时段：上午/下午/晚上 或自定义时段 |
| status | string | 是 | 状态：待诊/已诊/取消/未到 |
| purpose | string | 否 | 就诊目的（复诊/新症/调方/体检等） |
| queue_number | int | 否 | 当日排队序号 |
| notes | string | 否 | 备注 |

**索引字段**：appointment_id（主键）、patient_id、appointment_date、status

---

## 5. 财务记录表 (`finances.xlsx`)

文件路径：`clinic_data/finances.xlsx`
工作表名：`finances`

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| finance_id | string | 是 | 记录唯一标识，格式 `F{YYYYMMDD}{3位序号}` |
| record_id | string | 否 | 关联病历记录 ID（如有） |
| patient_id | string | 是 | 关联患者 ID |
| patient_name | string | 是 | 患者姓名 |
| date | string | 是 | 日期，格式 `YYYY-MM-DD` |
| type | string | 是 | 费用类型：挂号费/药费/针灸费/其他 |
| amount | float | 是 | 金额（元），保留两位小数 |
| payment_method | string | 否 | 支付方式：现金/微信/支付宝/医保/其他 |
| notes | string | 否 | 备注 |

**索引字段**：finance_id（主键）、patient_id、date、type

### 统计维度

财务统计支持以下聚合维度：
- **按日**：指定日期范围内的每日收入汇总（按 type 分列）
- **按月**：指定月份的月度收入汇总（按 type 分列）
- **按类型**：各费用类型的占比分析
- **按患者**：指定患者的就诊费用汇总
