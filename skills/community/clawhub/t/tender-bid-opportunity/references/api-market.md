<!-- request-identity:start -->
**请求身份**：使用已配置的 API Key，并保留本包的 X-Client，携带下列完整身份头；不得沿用其它包的版本或来源。
```text
X-Client: zlbx-bidding/2.5.0
X-Skill-Package: tender-bid-opportunity/1.0.0
X-Skill-Source: clawhub/bailianai
```
<!-- request-identity:end -->

# 市场分析类工具 API 详情

## 目录
- [get_top_purchasers - Top采购单位](#get_top_purchasers)
- [get_top_suppliers - Top中标单位](#get_top_suppliers)
- [get_top_brands - Top中标品牌](#get_top_brands)
- [aggregate_bids_advanced - 多维度聚合统计](#aggregate_bids_advanced)
- [get_price_trends - 品牌型号价格查询](#get_price_trends)

---

## get_top_purchasers - Top采购单位 {#get_top_purchasers}

按关键词查询Top采购单位（精准获客、市场调研）。

### 请求参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `keywords` | list[str] | 必填，业务关键词 |
| `match_modes` | list[str] | 匹配模式，默认 `["all"]` |
| `begin_date` | str | 统计开始日期 |
| `end_date` | str | 统计结束日期 |
| `provinces` | list[str] | 省份列表 |
| `cities` | list[str] | 城市列表 |
| `exclude_keywords` | list[str] | 排除关键词 |
| `min_amount` | float | 最低金额（万元） |
| `max_amount` | float | 最高金额（万元） |
| `limit` | int | 返回数量，默认20，最大100 |
| `sort_field` | str | 排序字段：`count`/`amount`/`pub_time`，默认 `count` |

### 响应结构

```json
{
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
        "top_winners": [{"winner": "华为技术有限公司", "count": 10}],
        "company_url": "https://www.zhiliaobiaoxun.com/company/1234567890"
      }
    ]
  }
}
```

### 示例

**查找北京地区AI采购大户（按金额排序）**：
```json
{
  "keywords": ["人工智能", "AI"],
  "provinces": ["北京"],
  "min_amount": 100,
  "sort_field": "amount"
}
```

---

## get_top_suppliers - Top中标单位 {#get_top_suppliers}

按关键词查询Top中标单位（渠道扩展、竞对分析）。

### 请求参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `keywords` | list[str] | 必填，业务关键词 |
| `match_modes` | list[str] | 匹配模式，默认 `["all"]` |
| `begin_date` | str | 统计开始日期 |
| `end_date` | str | 统计结束日期 |
| `provinces` | list[str] | 省份列表 |
| `cities` | list[str] | 城市列表 |
| `exclude_keywords` | list[str] | 排除关键词 |
| `min_amount` | float | 最低金额（万元） |
| `max_amount` | float | 最高金额（万元） |
| `limit` | int | 返回数量，默认20，最大100 |
| `sort_field` | str | 排序字段：`count`/`amount`/`pub_time`，默认 `count` |

### 响应结构

```json
{
  "data": {
    "total": 100,
    "items": [
      {
        "company_name": "华为技术有限公司",
        "win_count": 100,
        "total_amount": 500000000,
        "total_amount_wan": 50000,
        "latest_win_time": "2025-01-10",
        "top_provinces": [{"province": "北京", "count": 30}],
        "top_callers": [{"caller": "中国移动", "count": 15}],
        "company_url": "https://www.zhiliaobiaoxun.com/company/1234567890"
      }
    ]
  }
}
```

### 示例

**查找服务器Top供应商（按中标金额排序，排除维保）**：
```json
{
  "keywords": ["服务器"],
  "exclude_keywords": ["维修", "维保"],
  "sort_field": "amount"
}
```

---

## get_top_brands - Top中标品牌 {#get_top_brands}

按产品/品类查询Top中标品牌及型号。

### 请求参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `product` | str | 必填，产品名称，如 `"呼吸机"` |
| `exclude_keywords` | list[str] | 排除关键词 |
| `min_price` | float | 最低价格（元） |
| `max_price` | float | 最高价格（元） |
| `begin_date` | str | 统计开始日期 |
| `end_date` | str | 统计结束日期 |
| `provinces` | list[str] | 省份列表 |
| `cities` | list[str] | 城市列表 |
| `counties` | list[str] | 区县列表 |
| `limit` | int | 返回品牌数量，默认10，最大50 |

### 响应结构

```json
{
  "data": {
    "product": "呼吸机",
    "total": 20,
    "brands": [
      {
        "brand": "迈瑞",
        "win_count": 500,
        "total_amount": 100000000,
        "avg_price": 50000,
        "avg_price_wan": 5,
        "top_models": ["SV300", "BeneVision T1"],
        "last_win_time": "2025-01-10"
      }
    ]
  }
}
```

### 示例

**查询服务器品牌市场占有率**：
```json
{
  "product": "服务器",
  "begin_date": "2024-01-01",
  "exclude_keywords": ["维修", "耗材"],
  "limit": 20
}
```

---

## aggregate_bids_advanced - 多维度聚合统计 {#aggregate_bids_advanced}

按月/季/年/省份/城市/行业/品牌等维度进行招中标数据统计分析。

### 请求参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `filters` | object | 筛选条件 |
| `filters.keywords` | list[str] | 关键词 |
| `filters.match_modes` | list[str] | 匹配模式 |
| `filters.keyword_groups` | list[dict] | 关键词组 |
| `filters.exclude_keywords` | list[str] | 排除关键词 |
| `filters.bid_type` | int | 1=招标 2=中标 |
| `filters.begin_date` | str | 开始日期 |
| `filters.end_date` | str | 结束日期 |
| `filters.provinces` | list[str] | 省份列表 |
| `filters.cities` | list[str] | 城市列表 |
| `filters.min_amount` | float | 最低金额（万元） |
| `filters.max_amount` | float | 最高金额（万元） |
| `group_by` | list[str] | **必填**，聚合维度 |
| `metrics` | list[str] | 统计指标，默认 `["count", "sum_amount"]` |
| `compare_with` | str | 对比类型：`yoy`=同比，`qoq`=环比 |

### group_by 可选值

| 值 | 说明 |
|---|------|
| `month` | 按月统计 |
| `quarter` | 按季度统计 |
| `year` | 按年统计 |
| `province` | 按省份统计 |
| `city` | 按城市统计 |
| `industry` | 按采购行业统计 |
| `brand` | 按品牌统计 |
| `company_type` | 按招标公司类型 |
| `bid_method` | 按采购方式 |

### 响应结构

```json
{
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

### 示例

**按月统计大语言模型中标趋势（同比分析）**：
```json
{
  "filters": {
    "keywords": ["大语言模型"],
    "bid_type": 2,
    "begin_date": "2024-01-01"
  },
  "group_by": ["month"],
  "compare_with": "yoy"
}
```

**按省份统计服务器市场**：
```json
{
  "filters": {
    "keywords": ["服务器"],
    "begin_date": "2024-01-01"
  },
  "group_by": ["province"]
}
```

**按品牌统计某产品市场份额**：
```json
{
  "filters": {
    "keywords": ["呼吸机"],
    "bid_type": 2
  },
  "group_by": ["brand"]
}
```

---

## get_price_trends - 品牌型号价格查询 {#get_price_trends}

查询品牌+型号的历史中标单价记录（采购寻源、价格参考）。

### 请求参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `brand` | str | **必填**，品牌名称，如 `"联想"` |
| `model` | str | 型号，如 `"SV300"` |
| `product` | str | 产品类别，如 `"呼吸机"` |
| `exclude_keywords` | list[str] | 排除关键词 |
| `min_price` | float | 最低价格（元） |
| `max_price` | float | 最高价格（元） |
| `begin_date` | str | 统计开始日期 |
| `end_date` | str | 统计结束日期 |
| `provinces` | list[str] | 省份列表 |
| `cities` | list[str] | 城市列表 |
| `counties` | list[str] | 区县列表 |
| `limit` | int | 返回记录数量，默认20，最大200 |

### 响应结构

```json
{
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
        "sm_name": "呼吸机",
        "brand": "迈瑞",
        "model": "SV300",
        "sku_price": 50000,
        "sku_count": 5,
        "sku_total_money": 250000,
        "caller_name": "XX市人民医院",
        "pub_time": "2025-01-10",
        "province": "广东",
        "winner_names": ["XX医疗器械公司"],
        "url": "https://www.zhiliaobiaoxun.com/content/12345678/b1"
      }
    ]
  }
}
```

### 示例

**查询迈瑞SV300呼吸机历史中标价格**：
```json
{
  "brand": "迈瑞",
  "model": "SV300",
  "product": "呼吸机",
  "exclude_keywords": ["耗材", "维修", "维保"]
}
```

**查询某品牌服务器近一年价格区间**：
```json
{
  "brand": "联想",
  "product": "服务器",
  "begin_date": "2025-01-01",
  "limit": 50
}
```

## 金额参数说明

不同工具金额参数名不同：

| 工具 | 金额参数 | 单位 |
|------|---------|------|
| search_bids | `min_amount`, `max_amount` | **万元** |
| query_bids_advanced | `min_amount`, `max_amount` | **万元** |
| search_expiring_projects / search_proposed_projects | `min_amount`, `max_amount` | **万元** |
| get_company_partners | `min_amount` | **万元** |
| aggregate_bids_advanced | `filters.min_amount`, `filters.max_amount` | **万元** |
| get_top_brands / get_price_trends | `min_price`, `max_price` | 元（产品单价，非项目金额） |

响应侧的元口径字段各接口不同名：标讯搜索是 `money`（对应 `money_wan`）、聚合是
`sum_amount` / `total_amount`（对应 `sum_amount_wan`）、Top 类是 `total_amount`
（对应 `total_amount_wan`）、合作伙伴是 `cooperation_amount`（对应 `cooperation_amount_wan`）。

拟建项目（`search_proposed_projects`）与其他工具一致：`money` 是元、`money_wan` 是万元，
另有 `money_format` 可读串。（2026-09-12 之前这里写着「拟建的 money 本身就是万元」，
那是错的，且当时 `min_amount` 筛选因此完全失效，见 ADR-0004。）

<!-- package-identity:start -->
**安装包身份与升级检查**：所有发往知了标讯 API 的请求（包括账户查询）必须额外携带以下两个请求头：
```text
X-Skill-Package: tender-bid-opportunity/1.0.0
X-Skill-Source: clawhub/bailianai
```
这些值是当前安装包的固定身份，复用已有API Key时也要携带；不要用X-Client产品版本替代包版本，不要将Key的注册渠道当作安装来源。
请求鉴权：使用已配置的 API Key，并保留本包的 X-Client。每个会话首次使用本Skill时，在已有凭证可用后先调用免费账户接口 `GET https://mcp-server.zhiliaobiaoxun.com/api_v2/account/balance` 检查升级提醒；该查询不扣积分，不触发购买。
**版本提醒转达**：响应出现 `skill_update_notice` 时，将其中 `message` 原样转达用户；兼容提示只说明检查版本，不能宣称已确认当前包过期。
**展示后确认**：只有将提醒发送到用户可见对话之后，才使用同一凭证和请求头，按 `display_ack` 提交 POST 回执（MCP客户端可调用 `confirm_skill_update_display`）（`notice_id` 和 `displayed: true`）。只读取工具响应、在思考中提过、尚未转达时不得确认。不能在展示后调用接口则不确认，服务端继续保留待提醒状态。回执免费，不扣积分；失败不影响查询结果，不向用户展示技术回执。同一会话同一 `notice_id` 只展示一次。
<!-- package-identity:end -->
