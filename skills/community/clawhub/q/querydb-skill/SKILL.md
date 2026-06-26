---
name: queryDB-skill
description: 数据库查询 Skill。当用户需要连接 MySQL/PostgreSQL 等数据库执行 SQL 查询、获取测试数据、验证接口返回数据时使用此 Skill。
---

# QueryDB Skill - 数据库查询 & 测试用例生成

## 功能概述

| 模块 | 用途 |
|------|------|
| **DatabaseClient** | 通用数据库连接和查询（MySQL / PostgreSQL） |
| **DbFixture** | db_fixture 模式，为接口测试注入真实数据 |
| **TestCaseGenerator** | 从数据库按场景自动生成接口测试用例 |

---

## 测试环境数据库信息

| 参数 | 值 |
|------|---|
| host | `10.115.96.247` |
| port | `3306` |
| database | `jxindependent0` |
| user | `jxindependent` |
| password | `Xj2zCkLJXTkEJ5j` |
| 购方税号 | `91440606MA4WHN8C8X` |

### 核心表：bw_jms_main1

| 字段 | 说明 |
|------|------|
| `INV_TYPE` | 票种代码（01/31/32/85等，2位字符） |
| `INV_KIND` | 发票代码（税控票/数电纸票，12位） |
| `INV_NUM` | 发票号码（税控票8位，数电纸票8位） |
| `E_INV_NUM` | 数电号码（数电票/数电纸票，20位） |
| `BUYER_TAXNO` | 购方税号 |
| `SELLER_TAXNO` | 销方税号 |
| `SELLER_NAME` | 销方名称 |
| `INV_DATE` | 开票日期（date类型） |
| `CREATE_DATE` | 入库时间（datetime类型） |
| `UPDATE_DATE` | 更新时间（datetime类型） |
| `INV_STATUS` | 发票状态 |
| `RED_LOCK_FLAG` | 红字标识 |
| `INV_DEDU_RESULT` | 认证/合规结果 |
| `IS_COLLECT_ALL` | 是否全量采集 |
| `NOT_DEDUCTIBLE` | 是否不可抵扣 |

---

## 发票类型规则（重要）

查询发票时，根据票种（`INV_TYPE`）决定使用哪个字段作为接口入参：

| 票种大类 | INV_TYPE 代码 | invoiceCode（接口入参） | invoiceNumber（接口入参） |
|---------|-------------|:-------------------:|:--------------------:|
| **数电票** | 31/32/51/59/61/83/84 | ❌ **不传** | `E_INV_NUM`（20位数电号码） |
| **税控票** | 01/03/04/08/10/11/14/15 | `INV_KIND` | `INV_NUM` |
| **数电纸票** | 85/86/87/88 | `INV_KIND` | `INV_NUM` |

---

## 安装依赖

```bash
pip install pymysql          # MySQL
pip install psycopg2-binary  # PostgreSQL（可选）
```

---

## 使用方法

### 1. DatabaseClient - 基本查询

```python
import sys
sys.path.insert(0, r"C:\Users\PC\.workbuddy\skills\queryDB-skill\scripts")
from db_query import DatabaseClient

db = DatabaseClient(
    host="10.115.96.247", port=3306,
    user="jxindependent", password="Xj2zCkLJXTkEJ5j",
    database="jxindependent0", charset="utf8mb4"
)

# 查多条
rows = db.query("SELECT INV_TYPE, INV_NUM, E_INV_NUM FROM bw_jms_main1 LIMIT 5")

# 查单条
row = db.query_one(
    "SELECT INV_TYPE, INV_KIND, INV_NUM, E_INV_NUM, BUYER_TAXNO "
    "FROM bw_jms_main1 WHERE INV_TYPE='31' AND E_INV_NUM IS NOT NULL LIMIT 1"
)

# 计数
total = db.count("SELECT COUNT(*) FROM bw_jms_main1 WHERE INV_TYPE='01'")

db.close()
```

### 2. DbFixture - db_fixture 模式

将真实数据注入到测试用例的 `{{占位符}}` 中：

```python
from db_query import DbFixture

# 查税控票样本
fixture = DbFixture(
    connection={
        "host": "10.115.96.247", "port": 3306,
        "user": "jxindependent", "password": "Xj2zCkLJXTkEJ5j",
        "database": "jxindependent0", "charset": "utf8mb4"
    },
    queries=[
        {
            "name": "tax_invoice",
            "sql": "SELECT INV_KIND, INV_NUM, BUYER_TAXNO FROM bw_jms_main1 "
                   "WHERE INV_TYPE='01' AND INV_NUM IS NOT NULL LIMIT 1",
            "mapping": {
                "invoiceCode":   "INV_KIND",
                "invoiceNumber": "INV_NUM",
                "taxNo":         "BUYER_TAXNO"
            }
        },
        {
            "name": "digital_invoice",
            "sql": "SELECT E_INV_NUM, BUYER_TAXNO FROM bw_jms_main1 "
                   "WHERE INV_TYPE='31' AND E_INV_NUM IS NOT NULL LIMIT 1",
            "mapping": {
                "invoiceNumber": "E_INV_NUM",
                "taxNo":         "BUYER_TAXNO"
            }
        }
    ]
)
data = fixture.get_data()
# 返回: {"invoiceCode": "044031900101", "invoiceNumber": "12345678", "taxNo": "xxx"}
```

### 3. TestCaseGenerator - 自动生成测试用例

支持三种场景模式：

| 模式 | 方法 | 适用场景 |
|------|------|---------|
| `single_row` | `generate_single_row_case()` | 按单条记录字段映射到接口入参 |
| `multi_row_safe` | `generate_multi_row_safe_case()` | 多条记录但 < 500 条时，映射查询条件到入参 |
| `invoice_by_taxno` | `generate_invoice_by_taxno_case()` | 按购方税号查发票，自动加时间范围 |

#### 示例：按票种查各类型发票样本

```python
import sys
sys.path.insert(0, r"C:\Users\PC\.workbuddy\skills\queryDB-skill\scripts")
from db_query import TestCaseGenerator

conn = {
    "host": "10.115.96.247", "port": 3306,
    "user": "jxindependent", "password": "Xj2zCkLJXTkEJ5j",
    "database": "jxindependent0", "charset": "utf8mb4"
}

with TestCaseGenerator(connection=conn, buyer_tax_no="91440606MA4WHN8C8X") as gen:

    # 税控票（01）：invoiceCode=INV_KIND, invoiceNumber=INV_NUM
    case = gen.generate_single_row_case(
        case_id="TC_001",
        case_name="01-增值税专用发票",
        case_group="票种覆盖-税控票",
        sql="SELECT INV_KIND, INV_NUM, BUYER_TAXNO FROM bw_jms_main1 "
            "WHERE INV_TYPE='01' AND INV_KIND IS NOT NULL AND INV_NUM IS NOT NULL LIMIT 1",
        mapping={
            "taxNo":         "BUYER_TAXNO",
            "invoiceCode":   "INV_KIND",
            "invoiceNumber": "INV_NUM",
        },
    )

    # 数电票（31）：invoiceCode 不传，invoiceNumber=E_INV_NUM（20位）
    case = gen.generate_single_row_case(
        case_id="TC_009",
        case_name="31-数电票（增值税专用发票）",
        case_group="票种覆盖-数电票",
        sql="SELECT E_INV_NUM, BUYER_TAXNO FROM bw_jms_main1 "
            "WHERE INV_TYPE='31' AND E_INV_NUM IS NOT NULL "
            "AND BUYER_TAXNO IS NOT NULL LIMIT 1",
        mapping={
            "taxNo":         "BUYER_TAXNO",
            "invoiceNumber": "E_INV_NUM",   # 20位数电号码
            # 注意：不映射 invoiceCode！数电票没有发票代码
        },
    )

    cases = gen.get_cases()
    print("生成 {} 个用例".format(len(cases)))
```

#### 批量生成：generate_from_scenarios

```python
scenarios = [
    {
        "mode": "single_row",
        "case_id": "TC_001",
        "case_name": "01-增值税专用发票",
        "case_group": "票种覆盖-税控票",
        "sql": "SELECT INV_KIND, INV_NUM, BUYER_TAXNO FROM bw_jms_main1 "
               "WHERE INV_TYPE='01' AND INV_KIND IS NOT NULL LIMIT 1",
        "mapping": {"taxNo":"BUYER_TAXNO","invoiceCode":"INV_KIND","invoiceNumber":"INV_NUM"},
    },
    {
        "mode": "multi_row_safe",
        "case_id": "TC_030",
        "case_name": "按票种31筛选发票池",
        "case_group": "枚举参数-发票类型",
        "sql": "SELECT INV_NUM FROM bw_jms_main1 "
               "WHERE BUYER_TAXNO='{{buyer_tax_no}}' AND INV_TYPE='31' "
               "AND CREATE_DATE >= DATE_SUB(NOW(), INTERVAL 90 DAY)",
        "filter_params": {"invoiceType": "31", "pageNum": 1},
        "time_range_days": 90,
        "max_rows": 500,
    },
    {
        "mode": "invoice_by_taxno",
        "case_id": "TC_040",
        "case_name": "按购方税号+销方税号查询",
        "case_group": "精确查询",
        "sql": "SELECT SELLER_TAXNO FROM bw_jms_main1 "
               "WHERE BUYER_TAXNO='{{buyer_tax_no}}' AND SELLER_TAXNO IS NOT NULL LIMIT 1",
        "mapping": {"salesTaxNo": "SELLER_TAXNO"},
        "extra_params": {"pageNum": 1},
        "time_range_days": 90,
    },
]

with TestCaseGenerator(connection=conn, buyer_tax_no="91440606MA4WHN8C8X") as gen:
    cases = gen.generate_from_scenarios(scenarios)
    gen.export_as_json("generated_cases.json")
```

---

## SQL 占位符

- `{{buyer_tax_no}}`：自动替换为初始化时传入的购方税号
- `{{自定义变量}}`：通过 `variables` 参数传入的自定义变量

---

## 生成的用例格式

生成的用例可直接写入 `test_config_xxx.json` 的 `test_cases` 数组：

```json
{
  "id": "TC_001",
  "group": "票种覆盖-税控票",
  "name": "01-增值税专用发票",
  "desc": "从DB查询单条记录，映射字段: taxNo, invoiceCode, invoiceNumber",
  "body": {
    "taxNo": "91440101MA5CLEH08W",
    "invoiceCode": "044031900101",
    "invoiceNumber": "12345678"
  },
  "expect": {
    "success": true
  }
}
```

---

## 注意事项

1. 数电票（31/32/51/59/61/83/84）mapping 中**不要映射 invoiceCode**，对应接口入参也不传此字段
2. `multi_row_safe` 模式会先执行 COUNT 确认数据量，超过 `max_rows`（默认500）则跳过该用例
3. 正向用例入参值必须来自数据库真实数据，确保接口能查到记录
4. 近期时间范围（近3个月）避免数据量超限
5. 建议查询加 `LIMIT 1` 限制（single_row 场景）
