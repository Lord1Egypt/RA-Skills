# 标讯搜索类工具 API 详情

## 目录
- [search_bids - 常规搜索](#search_bids)
- [query_bids_advanced - 高级搜索](#query_bids_advanced)
- [get_bid_detail - 标讯详情](#get_bid_detail)
- [search_expiring_projects - 临期项目](#search_expiring_projects)

---

## search_bids - 常规搜索 {#search_bids}

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
| `provinces` | list[str] | 否 | 省份列表，如 `["北京", "广东"]` |
| `cities` | list[str] | 否 | 城市列表 |
| `counties` | list[str] | 否 | 区县列表 |
| `min_amount` | float | 否 | 最低金额（元） |
| `max_amount` | float | 否 | 最高金额（元） |
| `page` | int | 否 | 页码，默认 1 |
| `page_size` | int | 否 | 每页数量，默认 20，最大 50 |

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
        "bid_process": 4,
        "pub_time": "2025-01-15",
        "money": 5000000,
        "money_wan": 500,
        "caller_name": "XX市人民政府",
        "winner_names": [],
        "sm_names": ["智慧城市平台", "数据中心建设"],
        "province": "广东",
        "city": "深圳",
        "url": "https://www.zhiliaobiaoxun.com/content/12345678/b1"
      }
    ]
  }
}
```

### 示例

**北京地区AI相关招标**：
```json
{
  "keywords": ["人工智能", "AI"],
  "bid_type": "招标",
  "provinces": ["北京"],
  "begin_date": "2025-01-01"
}
```

---

## query_bids_advanced - 高级搜索 {#query_bids_advanced}

支持所有 `search_bids` 参数，扩展支持关键词分组、排除词、复杂逻辑。

### 扩展参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `keyword_groups` | list[dict] | 关键词组，每个组与主keywords为AND关系 |
| `exclude_keywords` | list[str] | 排除关键词，匹配任一则排除 |
| `sort_field` | str | 排序字段，默认 `pub_time` |
| `sort_order` | str | 排序方向 `asc`/`desc`，默认 `desc` |

**注意**：`query_bids_advanced` 金额参数名为 `min_money`/`max_money`（不是 min_amount/max_amount）

### keyword_groups 结构

```json
{
  "keywords": ["关键词A", "关键词B"],
  "match_modes": ["sm", "title"]
}
```

### 使用示例

**复合查询 - 广东深圳，财产/资产类险种投保项目**：
```json
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
  "bid_type": "招标"
}
```

**搜索服务器/大模型，排除运维耗材**：
```json
{
  "keywords": ["服务器", "大模型"],
  "exclude_keywords": ["运维", "耗材", "维保"],
  "bid_process": [7, 8]
}
```

**查询A公司和B公司共同参与的项目**：
```json
{
  "keywords": ["华为技术有限公司"],
  "match_modes": ["winner", "tender"],
  "keyword_groups": [
    {
      "keywords": ["中兴通讯"],
      "match_modes": ["winner", "tender"]
    }
  ]
}
```

**查询某公司中标的特定产品**：
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

---

## get_bid_detail - 标讯详情 {#get_bid_detail}

根据 `bid_id`、`bid_url` 或 `uniq_key` 获取单条标讯完整详情及正文（三者至少填一个）。

### 请求参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `bid_id` | int | 标讯ID（优先使用） |
| `bid_url` | str | 知了标讯公告链接 |
| `bid_type` | int | 1=招标 2=中标（可选，加速查询） |

### 扩展响应字段

| 字段 | 说明 |
|------|------|
| `county` | 区县 |
| `agency_name` | 代理机构 |
| `service_end_date` | 服务截止日期 |
| `fulltext` | 公告原文 |

### 示例

```json
// 根据ID获取
{"bid_id": 12345678}

// 根据URL获取
{"bid_url": "https://www.zhiliaobiaoxun.com/content/1234567890/b1"}
```

---

## search_expiring_projects - 临期项目 {#search_expiring_projects}

查询即将到期的周期性项目，用于商机预测和续期机会挖掘。

### 请求参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `keywords` | list[str] | 必填，产品/服务关键词 |
| `begin_date` | str | 到期开始日期，默认今天 |
| `end_date` | str | 到期结束日期，默认今天起90天后 |
| `provinces` | list[str] | 省份列表 |
| `cities` | list[str] | 城市列表 |
| `min_amount` | float | 最低金额（元） |
| `company_type` | list[str] | 招标公司类型，如 `["学校", "医院"]` |
| `page` | int | 页码，默认 1 |
| `page_size` | int | 每页数量，默认 20 |

### 扩展响应字段

| 字段 | 说明 |
|------|------|
| `days_until_expiry` | 距离到期天数（越小越紧急） |
| `service_end_date` | 服务截止日期 |
| `caller_name` | 潜在续约客户 |
| `money` | 历史项目金额，可参考报价 |

### 示例

**北京地区职工体检服务临期项目**：
```json
{
  "keywords": ["职工体检"],
  "provinces": ["北京"]
}
```

**90天内到期的医院物业管理项目**：
```json
{
  "keywords": ["物业管理"],
  "company_type": ["医院"],
  "end_date": "2026-07-28"
}
```
