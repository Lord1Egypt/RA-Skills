---
name: Tender Quick Search Engine - Biaozhaozhao
description: 招投标快捷检索引擎-标找找，当用户需要快速查询特定关键词的招标或中标公告时调用，优先调用基础搜索工具提取项目名称、金额和链接，输出精简直接的列表。
metadata: { "openclaw": {"requires": {"env":["ZLBX_API_KEY"]},"primaryEnv": "ZLBX_API_KEY"}}
---
# 招投标快捷检索引擎 - 标找找

## API 概览

**基础 URL**: `https://mcp-server.zhiliaobiaoxun.com/api_v2/{工具名}`

**调用方式**: POST 请求，Headers: `X-API-Key: 你的API_KEY`, `Content-Type: application/json`

**API Key 配置**:
- 通过环境变量 `ZLBX_API_KEY` 获取 [推荐]
- 申请地址：https://ai.zhiliaobiaoxun.com

现在注册赠送200次免费调用额度，助您快速体验平台功能！

**⚠️ 安全提示**：
- 切勿在代码中硬编码 API Key

## 工具分类（15个工具）

| 类别 | 工具名 | 功能 |
|------|--------|------|
| **标讯搜索** | `search_bids` | 常规搜索，按关键词、地区、金额、时间等检索 |
| | `query_bids_advanced` | 高级搜索，支持关键词分组、排除词、复杂逻辑 |
| | `get_bid_detail` | 获取单条标讯完整详情及正文 |
| | `search_expiring_projects` | 查询即将到期的周期性项目（商机预测） |
| **企业分析** | `get_company_profile` | 公司基础工商信息、行业、招中标次数 |
| | `get_company_business_keywords` | 从中标记录提炼公司主营业务关键词 |
| | `get_company_partners` | 查询公司合作客户和供应商 |
| | `get_company_contacts` | 查询公司项目联系人信息 |
| | `find_competitors` | 基于投标重叠度分析竞争对手 |
| | `find_potential_bidders` | 推荐历史参与同类项目的潜在供应商 |
| **市场分析** | `get_top_purchasers` | 按关键词查询Top采购单位 |
| | `get_top_suppliers` | 按关键词查询Top中标单位 |
| | `get_top_brands` | 按产品/品类查询Top中标品牌及型号 |
| | `aggregate_bids_advanced` | 多维度聚合统计（月/季/年/省份/行业/品牌等） |
| | `get_price_trends` | 查询品牌+型号的历史中标单价记录 |

---

# 核心概念

## match_modes 匹配模式

多个工具共用的匹配模式参数，控制关键词匹配的字段范围。

| 值 | 含义 | 使用场景 |
|---|------|---------|
| `sm` | 标的物/产品名称 | 搜索具体产品 |
| `title` | 公告标题 | 在标题中搜索 |
| `brand` | 品牌名 | 搜索特定品牌 |
| `fulltext` | 全文检索 | 全面搜索 |
| `caller` | 招标方/采购单位 | 搜索招标公司，当用户需要查询xx公司招标/采购时使用 |
| `winner` | 中标方/供应商 | 搜索中标公司，当用户需要查询xx公司中标时使用 |
| `tender` | 投标方 | 搜索投标方 |
| `winner_tender` | 中标方或投标方（两者都搜） | 搜索参与方 |

### 示例

```json
{
  "keywords": ["服务器"],
  "match_modes": ["sm", "title"]
}
```
仅在标的物和标题中搜索"服务器"。

```json
{
  "keywords": ["阿里云计算有限公司"],
  "match_modes": ["winner", "tender"]
}
```
**重点案例：** 查询“阿里云计算有限公司”投标和中标的项目。

```json
{
  "keywords": ["阿里云计算有限公司"],
  "match_modes": ["caller"]
}
```
**重点案例：** 查询“阿里云计算有限公司”招标的项目。

```json
{
  "keywords": ["阿里云"],
  "match_modes": ["winner"],
  "keyword_groups": [
    {
      "keywords": ["云存储", "云服务器", "云数据库"],
      "match_modes": ["sm", "title"]
    }
  ]
}
```
**重点案例：**查询阿里云中标的云存储、云服务器、云数据库相关的项目。[注意：keyword_groups筛选项需要高级搜索接口（query_bids_advanced）]

```json
{
  "keywords": ["生产许可证"],
  "match_modes": ["fulltext"]
}
```
查询投标资质中需要生产许可证的项目【由于资质：生产许可证不是标准字段，所以需要使用全文查询】。


## bid_process 公告阶段

标讯的生命周期阶段，用于筛选不同阶段的公告。

| 值 | 阶段 | 说明 |
|---|------|------|
| 1 | 采购意向 | 早期需求预告 |
| 2 | 预招标 | 招标前准备 |
| 4 | 招标 | 正式招标公告 |
| 5 | 变更 | 变更公告 |
| 6 | 中标候选人 | 中标候选人公示 |
| 7 | 中标结果 | 中标结果公告 |
| 8 | 合同 | 合同公示 |
| 9 | 验收 | 验收公告 |
| 10 | 废标 | 废标公告 |

**默认返回**：`[1, 2, 4, 7, 8]`（主要阶段）

### 示例

```json
{
  "bid_process": [7, 8]
}
```
仅返回中标结果和合同公告。

## 响应字段通用说明
所有工具统一返回结构：

```json
{
  "success": true,
  "data": { /* 实际数据 */ },
  "error": null,
  "meta": {
    "cost_units": 1,
    "execution_time_ms": 156
  }
}
```

### 标讯核心字段

| 字段 | 说明 |
|------|------|
| `bid_id` | 标讯ID |
| `title` | 公告标题 |
| `bid_type` | 招标/中标 |
| `bid_process` | 阶段 |
| `pub_time` | 发布时间 |
| `money` | 金额（元） |
| `money_wan` | 金额（万元） |
| `caller_name` | 采购方 |
| `winner_names` | 中标方列表 |
| `sm_names` | 标的物列表 |
| `url` | 详情链接 |
| `province` | 省份 |
| `city` | 城市 |

## 分页参数

所有列表类接口支持分页：

| 参数 | 说明 | 默认值 | 限制 |
|------|------|--------|------|
| `page` | 页码 | 1 | ≥1 |
| `page_size` | 每页数量 | 20 | 1~50 |

---

# 搜索类工具详解

## 1. search_bids - 常规搜索

按关键词、地区、金额、时间等条件检索招/中标公告。

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `keywords` | list[str] | 是 | 搜索关键词，如 `["大模型", "人工智能"]` |
| `match_modes` | list[str] | 否 | 匹配模式，默认 `["all"]` |
| `bid_type` | str | 否 | 公告类型：`招标`/`中标`/`全部`，默认 `全部` |
| `bid_process` | list[int] | 否 | 公告阶段，默认 `[1,2,4,7,8]` |
| `begin_date` | str | 否 | 开始日期 `YYYY-MM-DD` |
| `end_date` | str | 否 | 结束日期 `YYYY-MM-DD` |
| `provinces` | list[str] | 否 | 省份列表 |
| `cities` | list[str] | 否 | 城市列表 |
| `counties` | list[str] | 否 | 区县列表 |
| `min_amount` | float | 否 | 最低金额（元） |
| `max_amount` | float | 否 | 最高金额（元） |
| `page` | int | 否 | 页码，默认 1 |
| `page_size` | int | 否 | 每页数量，默认 20 |

### 响应结构

```json
{
  "success": true,
  "data": {
    "total": 150,
    "items": [
      {
        "bid_id": 12345678,
        "title": "XX市智慧城市建设项目",
        "bid_type": "招标",
        "pub_time": "2025-01-15",
        "money": 5000000,
        "money_wan": 500,
        "caller_name": "XX市人民政府",
        "winner_names": [],
        "sm_names": ["智慧城市平台", "数据中心建设"],
        "url": "https://www.zhiliaobiaoxun.com/content/12345678/b1"
      }
    ]
  }
}
```

### 使用示例

**场景1：搜索北京地区AI相关招标**
```bash
POST /api_v2/search_bids
{
  "keywords": ["人工智能", "AI"],
  "bid_type": "招标",
  "provinces": ["北京"],
  "begin_date": "2025-01-01"
}
```
---

## 2. query_bids_advanced - 高级搜索

- 所有常规搜索的参数都支持
- 支持关键词分组、排除词、复杂逻辑组合。

### 请求参数（扩展参数）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `keyword_groups` | list[dict] | 否 | 关键词组，实现分组匹配 |
| `exclude_keywords` | list[str] | 否 | 排除关键词 |
| `sort_field` | str | 否 | 排序字段，默认 `pub_time` |
| `sort_order` | str | 否 | 排序方向 `asc`/`desc`，默认 `desc` |

### 使用示例

**场景1：搜索服务器或大模型，排除运维和耗材**

```bash
POST /api_v2/query_bids_advanced
{
  "keywords": ["服务器", "大模型"],
  "exclude_keywords": ["运维", "耗材"],
  "bid_type": 2
}
```

**场景2：复合查询 - 广东深圳地区，搜索财产/资产关键词，标题包含"险"**

```bash
POST /api_v2/query_bids_advanced
{
  "keywords": ["财产", "资产"],
  "keyword_groups": [
    {
      "keywords": ["险"], 
      "match_modes": ["title"]
    }
  ],
  "provinces": ["广东"],
  "cities": ["深圳"],
  "bid_type": 1
}
```

---

## 3. get_bid_detail - 获取标讯详情

根据 `bid_id` / `uniq_key` / `URL` 获取单条标讯完整详情及正文。

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `bid_id` | int | 否* | 标讯ID（优先使用） |
| `bid_type` | int | 否 | 公告类型 1:招标 2:中标 |
| `bid_url` | str | 否* | 知了标讯公告链接 |
| `uniq_key` | str | 否* | 公告唯一标识 |

*三者至少填一个*

### 响应结构（扩展字段）

除基础标讯字段外，还包含：

| 字段 | 说明 |
|------|------|
| `county` | 区县 |
| `agency_name` | 代理机构 |
| `source` | 信息来源 |
| `service_end_date` | 服务截止日期 |
| `fulltext` | 公告原文 |

### 使用示例

**场景1：根据ID获取详情**

```bash
POST /api_v2/get_bid_detail
{
  "bid_id": 12345678
}
```

**场景2：根据URL获取详情**

```bash
POST /api_v2/get_bid_detail
{
  "bid_url": "https://www.zhiliaobiaoxun.com/content/1234567890/b1"
}
```

---

## 4. search_expiring_projects - 查询临期项目

查询即将到期的周期性项目，用于商机预测和续期机会挖掘。

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `keywords` | list[str] | 是 | 产品/服务关键词 |
| `begin_date` | str | 否 | 到期开始日期，默认今天 |
| `end_date` | str | 否 | 到期结束日期，默认今天起90天后 |
| `provinces` | list[str] | 否 | 省份列表 |
| `cities` | list[str] | 否 | 城市列表 |
| `counties` | list[str] | 否 | 区县列表 |
| `min_amount` | float | 否 | 最低金额 |
| `company_type` | list[str] | 否 | 招标公司类型，如 `["学校", "医院"]` |
| `page` | int | 否 | 页码，默认 1 |
| `page_size` | int | 否 | 每页数量，默认 20 |

### 响应结构（扩展字段）

| 字段 | 说明 |
|------|------|
| `days_until_expiry` | 距离到期天数 |
| `service_end_date` | 服务截止日期 |

### 使用示例

**场景1：查找医疗体检服务即将到期的项目**

```bash
POST /api_v2/search_expiring_projects
{
  "keywords": ["职工体检"],
  "provinces": ["北京"]
}
```

**场景2：查找90天内到期的物业管理项目**

```bash
POST /api_v2/search_expiring_projects
{
  "keywords": ["物业管理"],
  "end_date": "2026-07-01" # 当前时间90天后
}
```

---

# 公司类工具详解

## 1. get_company_profile - 公司画像

获取公司基础工商信息、行业、招中标次数等画像数据。

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `company` | str \| int | 否* | 公司名称（全称或简称）或公司ID |
| `company_url` | str | 否* | 知了标讯公司详情页链接 |

*两者至少填一个*

### 响应结构

```json
{
  "success": true,
  "data": {
    "id": 1234567890,
    "fullname": "华为技术有限公司",
    "name": "华为",
    "org_base_type": "企业",
    "industry": "通信设备制造",
    "industry_l1": "制造业",
    "industry_l2": "计算机、通信和其他电子设备制造业",
    "province": "广东",
    "city": "深圳",
    "county": "龙岗区",
    "capital": "10000万人民币",
    "size": "大型企业",
    "business_status": "在营",
    "caller_count": 1500,
    "winner_count": 3200,
    "taxpayer_number": "91XXXXXXXXXXXX",
    "establishment_date": "1987-09-15",
    "business_scope": "程控交换机、传输设备...",
    "url": "https://www.zhiliaobiaoxun.com/company/1234567890"
  }
}
```

### 使用示例

**场景1：查询华为公司画像**

```bash
POST /api_v2/get_company_profile
{
  "company": "华为技术有限公司"
}
```

**场景2：根据URL查询公司画像**

```bash
POST /api_v2/get_company_profile
{
  "company_url": "https://www.zhiliaobiaoxun.com/company/1234567890"
}
```

---

## 2. get_company_business_keywords - 主营业务关键词

从中标记录提炼公司主营业务关键词。

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `company` | str \| int | 否* | 公司名称或ID |
| `company_url` | str | 否* | 知了标讯公司详情页链接 |
| `begin_date` | str | 否 | 统计开始日期 |
| `end_date` | str | 否 | 统计结束日期 |
| `provinces` | list[str] | 否 | 省份列表 |
| `cities` | list[str] | 否 | 城市列表 |
| `limit` | int | 否 | 返回数量，默认10，最大50 |

### 响应结构

```json
{
  "success": true,
  "data": {
    "company_name": "华为技术有限公司",
    "company_id": 1234567890,
    "total_keywords": 50,
    "keywords": [
      {"keyword": "服务器", "count": 150, "amount": 50000000},
      {"keyword": "交换机", "count": 120, "amount": 30000000},
      {"keyword": "5G设备", "count": 80, "amount": 40000000}
    ]
  }
}
```

### 使用示例

**场景1：分析科大讯飞的主营业务**

```bash
POST /api_v2/get_company_business_keywords
{
  "company": "科大讯飞股份有限公司",
  "begin_date": "2024-01-01"
}
```

---

## 3. get_company_partners - 合作客户与供应商

查询公司的合作客户（采购方）和供应商（分包方），分析上下游关系。

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `company` | str \| int | 否* | 公司名称或ID |
| `company_url` | str | 否* | 知了标讯公司详情页链接 |
| `partner_type` | str | 是 | 合作方类型：`客户`/`供应商`/`全部` |
| `begin_date` | str | 否 | 统计开始日期 |
| `end_date` | str | 否 | 统计结束日期 |
| `provinces` | list[str] | 否 | 省份列表 |
| `cities` | list[str] | 否 | 城市列表 |
| `keywords` | list[str] | 否 | 产品关键词过滤 |
| `min_amount` | float | 否 | 最低合作金额 |
| `limit` | int | 否 | 返回数量，默认20，最大100 |

### 响应结构

```json
{
  "success": true,
  "data": {
    "company": "华为技术有限公司",
    "partner_type": "全部",
    "total": 500,
    "partners": [
      {
        "company_name": "中国移动通信集团",
        "company_id": 9876543210,
        "cooperation_count": 50,
        "cooperation_amount": 500000000,
        "cooperation_amount_wan": 50000,
        "last_cooperation_time": "2025-01-10",
        "products": ["5G基站", "核心网设备"]
      }
    ]
  }
}
```

### 使用示例

**场景1：查看科大讯飞的主要客户和供应商**

```bash
POST /api_v2/get_company_partners
{
  "company": "科大讯飞股份有限公司",
  "partner_type": "全部"
}
```

**场景2：查看某公司在教育行业的客户**

```bash
POST /api_v2/get_company_partners
{
  "company": "某公司名称",
  "partner_type": "客户",
  "keywords": ["教育", "学校"]
}
```

---

## 4. find_competitors - 竞争对手分析

基于投标重叠度分析竞争对手列表。

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `company` | str \| int | 否* | 公司名称或ID |
| `company_url` | str | 否* | 知了标讯公司详情页链接 |
| `limit` | int | 否 | 返回数量，默认10，最大50 |

### 响应结构

```json
{
  "success": true,
  "data": {
    "company_name": "目标公司",
    "company_id": 1234567890,
    "total_projects": 1000,
    "total_competitors": 50,
    "competitors": [
      {
        "company_name": "竞争对手A",
        "company_id": 1111111111,
        "co_bid_count": 80,
        "latest_co_bid_time": "2025-01-05",
        "top_co_bid_products": [
          {"product": "服务器", "count": 30}
        ],
        "top_co_bid_callers": [
          {"caller": "中国移动", "count": 20}
        ],
        "top_co_bid_provinces": [
          {"province": "北京", "count": 25}
        ]
      }
    ]
  }
}
```

### 使用示例

**场景1：查找一起投过标的竞争对手**

```bash
POST /api_v2/find_competitors
{
  "company": "公司名称",
  "limit": 20
}
```

---

## 5. get_company_contacts - 公司项目联系人

查询公司的项目联系人信息，包括招标联系人和中标联系人。

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `company` | str \| int | 否* | 公司名称（全称或简称）或公司ID |
| `company_url` | str | 否* | 知了标讯公司详情页链接 |
| `keywords` | list[str] | 否 | 筛选关键词，如 `["呼吸机", "监护仪"]` |
| `match_modes` | list[str] | 否 | 搜索范围，默认 `["sm","title"]`，可选：`sm`(标的物) `title`(标题) `brand`(品牌) `caller`(招标方) `winner`(中标方) |
| `begin_date` | str | 否 | 筛选开始日期 `YYYY-MM-DD` |
| `end_date` | str | 否 | 筛选截止日期 `YYYY-MM-DD` |
| `role` | int | 否 | 联系人类型：`1`=招标联系人，`2`=中标联系人，`0`=全部（先招标后中标补充），默认 `0` |
| `limit` | int | 否 | 返回联系人数量，默认5，最大20 |

### 响应结构

```json
{
  "success": true,
  "data": {
    "total": 50,
    "contacts": [
      {
        "phone": "138****1234",
        "name": "张先生",
        "bid_count": 10,
        "last_pub_time": "2025-01-10",
        "last_bid_url": "https://www.zhiliaobiaoxun.com/content/1234567890/b1"
      }
    ]
  }
}
```

### 使用示例

**场景1：查询某公司的所有项目联系人**

```bash
POST /api_v2/get_company_contacts
{
  "company": "公司名称"
}
```

**场景2：查询某公司在医疗设备项目中的中标联系人**

```bash
POST /api_v2/get_company_contacts
{
  "company": "公司名称",
  "keywords": ["呼吸机", "监护仪"],
  "role": 2
}
```

**场景3：查询某公司近期项目的招标联系人**

```bash
POST /api_v2/get_company_contacts
{
  "company": "公司名称",
  "begin_date": "2024-01-01",
  "role": 1
}
```

---

## 6. find_potential_bidders - 推荐潜在供应商

针对一个招标项目，推荐历史上参与同类项目较多的潜在供应商。

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `bid_id` | int | 否* | 标讯ID（优先使用） |
| `bid_type` | str | 否 | 公告类型 `招标`/`中标` |
| `bid_url` | str | 否* | 知了标讯公告链接 |
| `uniq_key` | str | 否* | 公告唯一标识 |
| `project_title` | str | 否 | 项目标题 |
| `limit` | int | 否 | 返回数量，默认10，最大50 |

*三者至少填一个*

### 响应结构

```json
{
  "success": true,
  "data": {
    "project_title": "XX市智慧城市建设项目",
    "project_bid_id": 12345678,
    "project_bid_type": 1,
    "caller_name": "XX市人民政府",
    "province": "广东",
    "city": "深圳",
    "sm_names": ["智慧城市平台", "数据中心"],
    "total": 50,
    "bidders": [
      {
        "company_name": "潜在供应商A",
        "company_id": 2222222222,
        "source": "历史中标",
        "caller_history_count": 10,
        "caller_history_amount": 5000000,
        "region_win_count": 5,
        "region_win_amount": 2000000,
        "last_cooperation_time": "2024-11-15",
        "latest_win_time": "2024-12-01",
        "matched_products": ["智慧城市平台", "数据中心"],
        "main_customers": ["深圳市政府", "广州市政府"]
      }
    ]
  }
}
```

### 使用示例

**场景1：投标前评估，查看类似项目的历史供应商**

```bash
POST /api_v2/find_potential_bidders
{
  "bid_url": "https://www.zhiliaobiaoxun.com/content/1234567890/b1"
}
```

**场景2：根据项目标题推荐供应商**

```bash
POST /api_v2/find_potential_bidders
{
  "project_title": "某市智慧城市建设项目",
  "limit": 20
}
```

---

# 市场分析类工具详解

## 1. get_top_purchasers - Top采购单位

按关键词查询Top采购单位（精准获客、市场调研）。

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `keywords` | list[str] | 是 | 业务关键词，如 `["大模型", "人工智能"]` |
| `match_modes` | list[str] | 否 | 匹配模式，默认 `["all"]` |
| `begin_date` | str | 否 | 统计开始日期 |
| `end_date` | str | 否 | 统计结束日期 |
| `provinces` | list[str] | 否 | 省份列表 |
| `cities` | list[str] | 否 | 城市列表 |
| `exclude_keywords` | list[str] | 否 | 排除关键词，如 `['维修', '耗材']` |
| `min_amount` | float | 否 | 最低金额 |
| `max_amount` | float | 否 | 最高金额 |
| `limit` | int | 否 | 返回数量，默认20，最大100 |
| `sort_field` | str | 否 | 排序字段：`count`/`amount`/`pub_time`，默认 `count` |

### 响应结构

```json
{
  "success": true,
  "data": {
    "total": 100,
    "items": [
      {
        "company_name": "XX市人民政府",
        "company_id": 1234567890,
        "purchase_count": 50,
        "total_amount": 100000000,
        "total_amount_wan": 10000,
        "latest_purchase_time": "2025-01-10",
        "top_winners": [
          {"winner": "华为技术有限公司", "count": 10}
        ],
        "company_url": "https://www.zhiliaobiaoxun.com/company/1234567890"
      }
    ]
  }
}
```

### 使用示例

**场景1：分析大语言模型市场，谁在买**

```bash
POST /api_v2/get_top_purchasers
{
  "keywords": ["大语言模型"],
  "begin_date": "2025-01-01"
}
```

**场景2：查找北京地区AI采购大户**

```bash
POST /api_v2/get_top_purchasers
{
  "keywords": ["人工智能", "AI"],
  "provinces": ["北京"],
  "min_amount": 1000000,
  "sort_field": "amount"
}
```

---

## 2. get_top_suppliers - Top中标单位

按关键词查询Top中标单位（渠道扩展、竞对分析）。

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `keywords` | list[str] | 是 | 业务关键词 |
| `match_modes` | list[str] | 否 | 匹配模式，默认 `["all"]` |
| `begin_date` | str | 否 | 统计开始日期 |
| `end_date` | str | 否 | 统计结束日期 |
| `provinces` | list[str] | 否 | 省份列表 |
| `cities` | list[str] | 否 | 城市列表 |
| `exclude_keywords` | list[str] | 否 | 排除关键词 |
| `min_amount` | float | 否 | 最低金额 |
| `max_amount` | float | 否 | 最高金额 |
| `limit` | int | 否 | 返回数量，默认20，最大100 |
| `sort_field` | str | 否 | 排序字段：`count`/`amount`/`pub_time`，默认 `count` |

### 响应结构

```json
{
  "success": true,
  "data": {
    "total": 100,
    "items": [
      {
        "company_name": "华为技术有限公司",
        "company_id": 1234567890,
        "win_count": 100,
        "total_amount": 500000000,
        "total_amount_wan": 50000,
        "latest_win_time": "2025-01-10",
        "top_provinces": [
          {"province": "北京", "count": 30, "amount": 150000000}
        ],
        "top_cities": [
          {"city": "深圳", "count": 20, "amount": 100000000}
        ],
        "top_callers": [
          {"caller": "中国移动", "count": 15}
        ],
        "company_url": "https://www.zhiliaobiaoxun.com/company/1234567890"
      }
    ]
  }
}
```

### 使用示例

**场景1：分析大语言模型市场，谁在中标**

```bash
POST /api_v2/get_top_suppliers
{
  "keywords": ["大语言模型"],
  "begin_date": "2025-01-01"
}
```

**场景2：查找服务器Top供应商**

```bash
POST /api_v2/get_top_suppliers
{
  "keywords": ["服务器"],
  "exclude_keywords": ["维修", "维保"],
  "sort_field": "amount"
}
```

---

## 3. get_top_brands - Top中标品牌

按产品/品类查询Top中标品牌及型号。

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `product` | str | 是 | 产品名称，如 `"呼吸机"`, `"服务器"` |
| `exclude_keywords` | list[str] | 否 | 排除关键词，如 `['维修', '耗材']` |
| `min_price` | float | 否 | 最低价格 |
| `max_price` | float | 否 | 最高价格 |
| `begin_date` | str | 否 | 统计开始日期 |
| `end_date` | str | 否 | 统计结束日期 |
| `provinces` | list[str] | 否 | 省份列表 |
| `cities` | list[str] | 否 | 城市列表 |
| `counties` | list[str] | 否 | 区县列表 |
| `limit` | int | 否 | 返回品牌数量，默认10，最大50 |

### 响应结构

```json
{
  "success": true,
  "data": {
    "product": "呼吸机",
    "total": 20,
    "brands": [
      {
        "brand": "迈瑞",
        "brand_id": 1001,
        "win_count": 500,
        "total_amount": 100000000,
        "total_amount_wan": 10000,
        "total_count": 2000,
        "avg_price": 50000,
        "avg_price_wan": 5,
        "top_models": ["SV300", " BeneVision T1"],
        "last_win_time": "2025-01-10"
      }
    ]
  }
}
```

### 使用示例

**场景1：查询呼吸机Top品牌**

```bash
POST /api_v2/get_top_brands
{
  "product": "呼吸机",
  "exclude_keywords": ["维修", "耗材"]
}
```

**场景2：查询服务器品牌市场占有率**

```bash
POST /api_v2/get_top_brands
{
  "product": "服务器",
  "begin_date": "2024-01-01",
  "limit": 20
}
```

---

## 4. aggregate_bids_advanced - 多维度聚合统计

按月/季/年/省份/城市/行业/品牌等维度进行招中标数据统计分析。

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `filters` | object | 否 | 筛选条件（与搜索工具类似） |
| `filters.keywords` | list[str] | 否 | 关键词 |
| `filters.match_modes` | list[str] | 否 | 匹配模式 |
| `filters.keyword_groups` | list[dict] | 否 | 关键词组 |
| `filters.exclude_keywords` | list[str] | 否 | 排除关键词 |
| `filters.bid_type` | int | 否 | 1=招标 2=中标 |
| `filters.begin_date` | str | 否 | 开始日期 |
| `filters.end_date` | str | 否 | 结束日期 |
| `filters.provinces` | list[str] | 否 | 省份列表 |
| `filters.cities` | list[str] | 否 | 城市列表 |
| `filters.min_money` | float | 否 | 最低金额 |
| `filters.max_money` | float | 否 | 最高金额 |
| `group_by` | list[str] | 是 | 聚合维度 |
| `metrics` | list[str] | 否 | 统计指标，默认 `["count", "sum_amount"]` |
| `compare_with` | str | 否 | 对比类型：`yoy`=同比 `qoq`=环比 |
| `compare_period` | str | 否 | 对比周期 |

### group_by 可选值

| 值 | 说明 |
|---|------|
| `month` | 按月统计 |
| `quarter` | 按季度统计 |
| `year` | 按年统计 |
| `province` | 按省份统计 |
| `city` | 按城市统计 |
| `industry` | 采购行业 |
| `brand` | 品牌 |
| `company_type` | 招标公司类型 |
| `bid_method` | 采购方式 |

### 响应结构

```json
{
  "success": true,
  "data": {
    "total_count": 1000,
    "total_amount": 5000000000,
    "total_amount_wan": 500000,
    "buckets": [
      {
        "key": "2025-01",
        "count": 100,
        "sum_amount": 500000000,
        "sum_amount_wan": 50000,
        "avg_amount": 5000000,
        "yoy_count": 10.5,
        "yoy_amount": 15.3
      }
    ],
    "group_by": ["month"]
  }
}
```

### 使用示例

**场景1：按月统计大语言模型项目**

```bash
POST /api_v2/aggregate_bids_advanced
{
  "filters": {
    "keywords": ["大语言模型"],
    "begin_date": "2024-01-01"
  },
  "group_by": ["month"]
}
```

**场景2：按省份和城市统计服务器市场**

```bash
POST /api_v2/aggregate_bids_advanced
{
  "filters": {
    "keywords": ["服务器"],
    "begin_date": "2024-01-01"
  },
  "group_by": ["province", "city"]
}
```

**场景3：同比分析AI项目趋势**

```bash
POST /api_v2/aggregate_bids_advanced
{
  "filters": {
    "keywords": ["人工智能", "AI"],
    "bid_type": 2
  },
  "group_by": ["month"],
  "compare_with": "yoy"
}
```

---

## 5. get_price_trends - 品牌型号价格查询

查询品牌+型号的历史中标单价记录（采购寻源、价格参考）。

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `brand` | str | 是 | 品牌名称，如 `"联想"`, `"迈瑞"` |
| `model` | str | 否 | 型号 |
| `product` | str | 否 | 产品类别 |
| `exclude_keywords` | list[str] | 否 | 排除关键词 |
| `min_price` | float | 否 | 最低价格 |
| `max_price` | float | 否 | 最高价格 |
| `begin_date` | str | 否 | 统计开始日期 |
| `end_date` | str | 否 | 统计结束日期 |
| `provinces` | list[str] | 否 | 省份列表 |
| `cities` | list[str] | 否 | 城市列表 |
| `counties` | list[str] | 否 | 区县列表 |
| `limit` | int | 否 | 返回记录数量，默认20，最大200 |

### 响应结构

```json
{
  "success": true,
  "data": {
    "brand": "迈瑞",
    "model": "SV300",
    "total": 50,
    "price_stats": {
      "min": 30000,
      "max": 80000,
      "avg": 50000,
      "median": 48000
    },
    "records": [
      {
        "bid_id": 12345678,
        "bid_type": 2,
        "title": "XX医院医疗设备采购项目",
        "sm_name": "呼吸机",
        "brand": "迈瑞",
        "model": "SV300",
        "sku_price": 50000,
        "sku_count": 5,
        "sku_total_money": 250000,
        "caller_name": "XX市人民医院",
        "pub_time": "2025-01-10",
        "province": "广东",
        "city": "深圳",
        "winner_names": ["XX医疗器械公司"],
        "url": "https://www.zhiliaobiaoxun.com/content/12345678/b1"
      }
    ]
  }
}
```

### 使用示例

**场景1：查询迈瑞SV300呼吸机历史中标价格**

```bash
POST /api_v2/get_price_trends
{
  "brand": "迈瑞",
  "model": "SV300",
  "product": "呼吸机",
  "exclude_keywords": ["耗材", "维修", "维保"]
}
```

**场景2：查询某品牌服务器价格区间**

```bash
POST /api_v2/get_price_trends
{
  "brand": "联想",
  "product": "服务器",
  "begin_date": "2024-01-01",
  "limit": 50
}
```

---

# 使用场景示例

本文档提供7个典型使用场景的完整调用示例，涵盖标讯搜索、企业分析、市场研究等常见需求。

---

## 场景一：公司深度分析（互联网增强）

**用户需求**：帮我深度分析一下科大讯飞，包括业务布局、竞争优势、最新动态

**分析思路**：
1. 获取公司基础画像和主营业务（标讯数据）
2. 分析竞争对手（标讯数据）
3. 搜索公司官网获取最新动态
4. 查找行业新闻了解市场地位
5. 综合分析生成报告

**标讯数据调用**：

```bash
# 步骤1：获取公司画像
POST https://mcp-server.zhiliaobiaoxun.com/api_v2/get_company_profile
{
  "company": "科大讯飞股份有限公司"
}

# 步骤2：获取主营业务关键词
POST https://mcp-server.zhiliaobiaoxun.com/api_v2/get_company_business_keywords
{
  "company": "科大讯飞股份有限公司",
  "begin_date": "2024-01-01"
}

# 步骤3：分析竞争对手
POST https://mcp-server.zhiliaobiaoxun.com/api_v2/find_competitors
{
  "company": "科大讯飞股份有限公司"
}
```

**互联网信息补充**：使用 WebSearch 搜索公司官网、最新动态、行业政策等

---

## 场景二：市场趋势与价格分析（互联网增强）

**用户需求**：分析服务器市场2025年发展趋势及价格区间

**标讯数据调用**：

```bash
# 按月统计服务器中标趋势
POST https://mcp-server.zhiliaobiaoxun.com/api_v2/aggregate_bids_advanced
{
  "filters": {
    "keywords": ["服务器"],
    "bid_type": 2,
    "begin_date": "2024-01-01"
  },
  "group_by": ["month", "province"],
  "compare_with": "yoy"
}

# 获取Top品牌及价格区间
POST https://mcp-server.zhiliaobiaoxun.com/api_v2/get_top_brands
{
  "product": "服务器",
  "begin_date": "2024-01-01"
}

# 查询特定品牌价格走势
POST https://mcp-server.zhiliaobiaoxun.com/api_v2/get_price_trends
{
  "brand": "联想",
  "product": "服务器",
  "exclude_keywords": ["维修", "维保", "耗材"]
}
```

---

## 场景三：产业链分析（互联网增强）

**用户需求**：分析新能源汽车充电桩产业链

**标讯数据调用**：

```bash
# 获取充电桩Top供应商
POST https://mcp-server.zhiliaobiaoxun.com/api_v2/get_top_suppliers
{
  "keywords": ["充电桩", "充电设施"],
  "begin_date": "2024-01-01",
  "limit": 50
}

# 获取Top采购方
POST https://mcp-server.zhiliaobiaoxun.com/api_v2/get_top_purchasers
{
  "keywords": ["充电桩", "充电设施"],
  "begin_date": "2024-01-01",
  "limit": 50
}

# 分析某供应商的合作伙伴（上下游关系）
POST https://mcp-server.zhiliaobiaoxun.com/api_v2/get_company_partners
{
  "company": "特来电新能源有限公司",
  "partner_type": "全部"
}
```

---

## 场景四：寻找商机（临期项目续期）

**用户需求**：找一些医疗体检服务即将到期的项目

**调用示例**：

```bash
POST https://mcp-server.zhiliaobiaoxun.com/api_v2/search_expiring_projects
{
  "keywords": ["职工体检"],
  "provinces": ["北京"]
}
```

**响应分析要点**：
- `days_until_expiry`：距离到期天数，越小越紧急
- `service_end_date`：服务截止日期
- `caller_name`：潜在续约客户
- `money`：历史项目金额，可参考报价

---

## 场景五：竞对分析

**用户需求**：找找跟我们公司一起投过标的竞争对手

**调用示例**：

```bash
POST https://mcp-server.zhiliaobiaoxun.com/api_v2/find_competitors
{
  "company": "公司名称",
  "limit": 20
}
```

**响应分析要点**：
- `co_bid_count`：共同投标次数，越大竞争越激烈
- `top_co_bid_products`：竞争产品领域
- `top_co_bid_callers`：共同争夺的客户
- `top_co_bid_provinces`：竞争活跃地区

---

## 场景六：投标前评估潜在供应商

**用户需求**：这个项目我要不要参与？看看历史上参与过类似项目的供应商

**调用示例**：

```bash
POST https://mcp-server.zhiliaobiaoxun.com/api_v2/find_potential_bidders
{
  "bid_url": "https://www.zhiliaobiaoxun.com/content/xxxxxx/b1"
}
```

**响应分析要点**：
- `caller_history_count`：与该采购方的历史合作次数
- `region_win_count`：在该地区的中标次数
- `matched_products`：匹配的产品领域
- `main_customers`：主要客户资源

---

## 场景七：市场分析（获客+竞对）

**用户需求**：帮我分析大语言模型市场，谁在买，谁在中标

**标讯数据调用**：

```bash
# 步骤1：找Top采购方
POST https://mcp-server.zhiliaobiaoxun.com/api_v2/get_top_purchasers
{
  "keywords": ["大语言模型"],
  "begin_date": "2025-01-01"
}

# 步骤2：找Top供应商
POST https://mcp-server.zhiliaobiaoxun.com/api_v2/get_top_suppliers
{
  "keywords": ["大语言模型"],
  "begin_date": "2025-01-01"
}

# 步骤3：趋势分析
POST https://mcp-server.zhiliaobiaoxun.com/api_v2/aggregate_bids_advanced
{
  "filters": {
    "keywords": ["大语言模型"],
    "begin_date": "2025-01-01"
  },
  "group_by": ["month", "province"]
}
```

---

## 场景八：高级搜索技巧

**排除干扰词 + 复合条件**：

```bash
# 场景A：排除运维和耗材
POST https://mcp-server.zhiliaobiaoxun.com/api_v2/query_bids_advanced
{
  "keywords": ["服务器", "大模型"],
  "exclude_keywords": ["运维", "耗材"],
  "provinces": ["北京"],
  "bid_type": 2
}

# 场景B：keyword_groups实现AND逻辑
POST https://mcp-server.zhiliaobiaoxun.com/api_v2/search_bids
{
  "keywords": ["财产", "资产"],
  "keyword_groups": [
    {"keywords": ["险"], "match_modes": ["title"]}
  ],
  "provinces": ["广东"],
  "cities": ["深圳"],
  "bid_type": 1
}
```

---

## Python 调用示例

```python
import requests

url = "https://mcp-server.zhiliaobiaoxun.com/api_v2/search_bids"
headers = {
    "X-API-Key": api_key,
    "Content-Type": "application/json"
}
payload = {
    "keywords": ["智慧城市"],
    "bid_type": "全部",
    "provinces": ["北京"],
    "begin_date": "2025-01-01",
    "page": 1,
    "page_size": 20
}

response = requests.post(url, json=payload, headers=headers)
data = response.json()
print(data)
```

---

# 错误处理与FAQ

## API 错误码

| 错误码 | 说明 | 处理方式 |
|------|------|---------|
| AUTHENTICATION_FAILED | API Key 无效、缺失或无权访问 | 检查 API Key 配置，确认Key正确有效 |
| INSUFFICIENT_BALANCE / QUOTA_EXCEEDED | 账户余额或可用次数不足 | 充值后重试 |
| RATE_LIMITED | 触发频率限制 | 降低请求频率，稍后重试 |
| INVALID_REQUEST | 请求参数不合法或缺少必填项 | 检查请求参数类型和取值范围 |
| INTERNAL_ERROR | 服务内部错误 | 稍后重试或联系技术支持 |
| TOOL_EXECUTION_ERROR | 工具执行失败（下游或业务逻辑异常） | 检查请求参数或联系技术支持 |


## 使用 FAQ

### Q1: company 参数应该传什么？

A: 支持以下三种方式：
1. **公司全称**：`"华为技术有限公司"`
2. **公司简称**：`"华为"`
3. **公司ID**：`1234567890`（整数）

**优先级**：公司ID > 公司全称 > 公司简称

### Q4: 如何按金额筛选？响应中的金额字段有什么区别？

A: **金额筛选**：不同工具使用不同参数名

| 工具 | 金额参数 | 单位 |
|------|---------|------|
| search_bids | `min_amount`, `max_amount` | 元 |
| query_bids_advanced | `min_money`, `max_money` | 元 |
| get_top_brands | `min_price`, `max_price` | 元 |

**响应字段**：
| 字段 | 单位 | 说明 |
|------|------|------|
| `money` | 元 | 原始金额 |
| `money_wan` | 万元 | 转换后的金额，方便展示 |

### Q7: 如何排除特定关键词？

A: 使用 `exclude_keywords` 参数：

```json
{
  "keywords": ["服务器"],
  "exclude_keywords": ["维修", "耗材", "维保"]
}
```

### Q8: 如何进行复合条件搜索？

A: 使用 `keyword_groups` 参数实现 AND 逻辑：

```json
{
  "keywords": ["服务器"],
  "keyword_groups": [
    {"keywords": ["华为"], "match_modes": ["winner"]},
    {"keywords": ["北京"], "match_modes": ["caller"]}
  ]
}
```

这表示：搜索服务器相关项目，且中标方是华为，且采购方在北京。

---

## 使用场景速查

| 场景 | 使用工具 | 互联网增强 |
|------|---------|-----------|
| 公司深度分析 | `get_company_profile` + `get_company_business_keywords` + `find_competitors` | ✅ 官网、新闻、政策 |
| 市场趋势与价格分析 | `aggregate_bids_advanced` + `get_top_brands` + `get_price_trends` | ✅ 行业报告、技术趋势 |
| 产业链分析 | `get_top_suppliers` + `get_top_purchasers` + `get_company_partners` | ✅ 产业链信息 |
| 寻找商机（临期项目续期） | `search_expiring_projects` | - |
| 竞对分析 | `find_competitors` | ✅ 行业新闻 |
| 投标前评估潜在供应商 | `find_potential_bidders` | - |
| 市场分析（获客+竞对） | `get_top_purchasers` + `get_top_suppliers` + `aggregate_bids_advanced` | ✅ 市场报告 |
| 高级搜索技巧 | `query_bids_advanced` + `keyword_groups` | - |

**说明**：标记 ✅ 的场景建议结合互联网信息进行增强分析。

---

# 互联网增强分析

对于分析类、趋势分析或深度研究需求，本技能可结合标讯数据与最新互联网信息，提供更全面的分析结果。

## 触发判断规则

当用户需求满足以下**任一条件**时，可启用互联网增强分析：

| 触发条件 | 示例关键词/描述 |
|---------|----------------|
| **趋势分析类** | 趋势、前景、预测、发展方向、未来走向 |
| **深度分析类** | 深度分析、全面分析、综合分析、调研 |
| **竞争格局类** | 竞争格局、市场地位、行业排名、市场份额 |
| **战略类** | 战略、战略方向、业务布局、发展策略 |
| **产业链类** | 产业链、上下游、供应链、生态链 |
| **政策影响类** | 政策影响、行业政策、监管变化、政策支持 |

## 执行流程

```
用户需求输入
    ↓
判断是否需要互联网增强？
    ├─ 是 → 标讯API获取数据 + WebSearch补充信息 → 综合分析报告
    └─ 否 → 标讯API获取数据 → 基础分析结果
```

## 数据优先级原则

1. **标讯数据为主**：历史中标记录、项目金额、合作关系等客观数据
2. **互联网信息为辅**：用于背景补充、趋势验证、动态更新
3. **信息源优先级**：公司官网 > 可靠媒体 > 政策网站 > 一般新闻

## 适用场景

当用户需求包含以下关键词时，可主动引入互联网信息：
- 趋势分析、市场分析、行业分析
- 竞争分析、竞对研究
- 公司深度分析、公司调研
- 政策影响、行业前景
- 产业链分析、供应链研究
- 市场规模、市场预测

## 分析增强流程

```
标讯数据
    ↓
初步分析 ← → 互联网信息补充
    ↓              ↓
                - 搜索公司官网
                - 查找行业新闻
                - 获取政策文件
                - 产业链信息
    ↓
综合分析报告
```
---

# 用户引导与增值服务

## 回答后引导

在完成用户查询后，应主动引导用户进行进一步探索或使用增值服务。

### 引导话术模板

**基础引导**：
```
以上是查询结果。您还可以：
- 查看相关公司的合作伙伴和竞争对手分析
- 分析该领域的市场趋势和Top品牌
- 查询临期项目寻找商机
```

**深度分析引导**：
```
如需更深入的分析，我还可以帮您：
- 产业链上下游分析
- 竞争对手深度画像
- 价格趋势与采购寻源
- 市场规模与趋势预测
```

---

## 完整 API 文档

https://ai.zhiliaobiaoxun.com/docs/api/

