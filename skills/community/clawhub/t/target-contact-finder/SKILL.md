---
name: crm-customer-import
description: CRM 客户画像搜索与批量导入技能。只要用户提到以下任意一项就必须使用此技能：找客户、搜客户、搜索客户、客户画像、潜在客户、目标客户、客户列表、录入CRM、导入客户、批量导入、添加客户、找一批xx客户、xx地区的客户、xx行业的客户、酒店客户、酒旅客户、OTA客户、旅行社客户、商旅客户、分销客户、批发客户、TMC、DMC、bedbank、wholesaler、B2B客户。即使用户没有明确说"CRM"或"画像"，只要意图是寻找、筛选、导入潜在客户，都要立即使用此技能。
metadata.openclaw: {"emoji": "🔍", "primaryEnv": "user_key.txt"}
---

# CRM 客户画像搜索与批量导入

通过结构化条件搜索酒旅行业与 B2B 场景的潜在客户，确认后批量导入 CRM。

## API

**Base URL:** `http://39.108.114.224:9059`

所有接口的请求体中均需包含 `user_key` 字段。

### 接口列表

| 功能 | Method | Path |
|------|--------|------|
| 搜索客户画像 | POST | `/skill/search_customer_profile` |
| 批量导入客户 | POST | `/skill/batch_import_customer` |

### 调用方式

```bash
# 搜索客户画像
curl -s -X POST -H "Content-Type: application/json" \
  "http://39.108.114.224:9059/skill/search_customer_profile" \
  -d '{
    "user_key": "<user_key>",
    "q_keywords": "hotel hospitality resort",
    "organization_locations": ["Japan"],
    "person_titles": ["Business Development", "Partnership Manager"],
    "person_seniorities": ["manager", "director", "head"],
    "contact_email_status": ["verified", "likely to engage"],
    "per_page": 10,
    "page": 1
  }'

# 批量导入客户
curl -s -X POST -H "Content-Type: application/json" \
  "http://39.108.114.224:9059/skill/batch_import_customer" \
  -d '{
    "user_key": "<user_key>",
    "customers": [
      {
        "name": "Hilton Tokyo",
        "contact_name": "John Smith",
        "contact_email": "john@hiltontokyo.com",
        "contact_phone": "80012345",
        "contact_phone_prefix": "+81",
        "country_code": "JP",
        "address": "Tokyo, Japan",
        "remark": "Business Development | Hospitality"
      }
    ]
  }'
```

### 响应格式

成功响应：
```json
{
  "ok": true,
  "data": { ... }
}
```

失败响应：
```json
{
  "ok": false,
  "error": "错误描述"
}
```

`search_customer_profile` 成功时 `data` 字段：
```json
{
  "total_entries": 120,
  "credits_consumed": 5,
  "customers": [
    {
      "name": "公司名",
      "contact_name": "联系人",
      "contact_email": "email@example.com",
      "contact_phone": "12345678",
      "contact_phone_prefix": "+81",
      "country_code": "JP",
      "address": "Tokyo, Japan",
      "remark": "Title | Industry"
    }
  ]
}
```

`batch_import_customer` 成功时 `data` 字段：
```json
{
  "success_count": 8,
  "fail_count": 2,
  "fail_details": [
    {"name": "公司名", "email": "xxx@example.com", "reason": "联系邮箱已存在"}
  ]
}
```

---

## 核心流程

```text
1. 用户描述目标客户
2. 你将自然语言拆解为 Apollo 可识别的结构化参数
3. 调用 /skill/search_customer_profile
4. 展示结果并询问是否导入
5. 用户确认后调用 /skill/batch_import_customer
```

## 业务背景（重要）

本公司是 **酒旅行业 B2B 服务商**，核心目标客户主要包括：

- 酒店：hotel, resort, hospitality group, serviced apartment
- 旅游：travel, tourism, tour operator, travel agency
- OTA / 分销：OTA, online travel agency, wholesaler, bedbank, distribution
- 商旅：business travel, corporate travel, TMC
- 地接 / 目的地服务：DMC, destination management

目标联系人优先是：

- 商务合作负责人：Business Development, Partnership, Commercial
- 采购 / 签约负责人：Procurement, Contracting, Sourcing, Supplier
- 酒店收益 / 渠道负责人：Revenue, Distribution, Ecommerce
- 高层决策人：Founder, Owner, CEO, GM, VP, Head, Director

## Setup

调用任何接口前，必须先完成用户身份验证。

### Step 1 - User Key

1. 读取 `{baseDir}/user_key.txt`
2. 如果文件不存在或为空，不要调用任何接口，告知用户：
   > "在开始之前，需要先验证你的身份。请前往 https://aauth-170125614655.asia-northeast1.run.app/dashboard 用 Google 账号登录，复制你的 `user_key`（格式：`uk_xxxxxxxx`），然后告诉我。"
3. 如果文件存在且有内容，将其值作为所有请求体中的 `user_key`
4. 如果任意接口返回 HTTP 401 或响应体 `{"ok": false, "error": "unauthorized: ..."}` ，删除 `{baseDir}/user_key.txt` 并重新执行第 2 步

---

## 接口参数说明

### /skill/search_customer_profile

| 参数 | 类型 | 说明 |
|------|------|------|
| user_key | string | 从 `{baseDir}/user_key.txt` 读取 |
| q_keywords | string | 英文关键词，多个词用空格分隔 |
| person_titles | string[] | 联系人岗位 |
| person_locations | string[] | 联系人所在地区 |
| organization_locations | string[] | 公司所在地区，优先使用 |
| person_seniorities | string[] | 联系人层级 |
| contact_email_status | string[] | 邮箱状态 |
| organization_num_employees_ranges | string[] | 公司人数范围 |
| revenue_range_min | int | 最低营收（美元） |
| revenue_range_max | int | 最高营收（美元） |
| per_page | int | 每页数量 |
| page | int | 页码，从 1 开始 |

### /skill/batch_import_customer

| 参数 | 类型 | 说明 |
|------|------|------|
| user_key | string | 从 `{baseDir}/user_key.txt` 读取 |
| customers | CustomerItem[] | 要导入的客户列表 |

CustomerItem 字段：

| 字段 | 类型 | 说明 |
|------|------|------|
| name | string | 客户或公司名称（必填） |
| contact_name | string | 联系人姓名（必填） |
| contact_email | string | 联系人邮箱（必填） |
| contact_phone | string | 联系人电话（必填） |
| contact_phone_prefix | string | 电话区号，如 +81 |
| country_code | string | 国家编码，如 JP |
| address | string | 地址 |
| remark | string | 备注或画像描述 |

---

## Apollo 搜索原则（非常重要）

Apollo 这一套接口本质是 **按人搜索**，不是按一句画像描述直接找公司。

正确思路是：

1. 先定义 **公司画像**
2. 再定义 **联系人画像**
3. 最后再补邮箱状态、规模、营收等过滤条件

也就是说，你在构造参数时要优先关注：

- `q_keywords`：行业和业务模式关键词
- `organization_locations`：公司所在区域
- `person_titles`：联系人岗位
- `person_seniorities`：联系人层级

不要把用户原话整句塞给 Apollo。
特别是 `q_keywords`：

- 必须转成英文关键词
- 要短、准、可检索
- 不要传中文
- 不要传长句
- 不要只写一个空泛词如 `B2B`

## 参数解析指南（必须遵守）

### 1. 先判断搜索意图属于哪一类

优先把用户需求归到下面某个业务场景：

- 酒店 / 酒店集团
- OTA / 在线旅游平台
- 旅行社 / tour operator
- 分销 / 批发 / wholesaler / bedbank
- 商旅 / corporate travel / TMC
- 地接 / DMC

如果用户没有明确说行业，默认按 **酒旅 B2B 潜客** 搜索。

### 2. q_keywords 规则

推荐映射：

| 用户表达 | q_keywords |
|----------|-----------|
| 酒店客户 | `hotel hospitality resort` |
| 酒店集团 | `hotel hospitality group` |
| OTA 客户 | `ota online travel agency` |
| 旅行社 | `travel agency tour operator` |
| 酒旅分销 / 批发 | `hotel wholesale travel distribution bedbank` |
| 商旅客户 | `business travel corporate travel tmc` |
| 地接 / DMC | `destination management dmc inbound travel` |
| 酒旅 B2B 客户 | `hotel travel hospitality b2b` |
| 未明确行业 | `hotel travel hospitality b2b` |

### 3. 地区规则

默认优先用 `organization_locations`，因为我们通常要找"公司在哪个市场"的客户。

常用地区映射：

| 用户表达 | 参数 | 值 |
|----------|------|-----|
| 日本客户 | organization_locations | `["Japan"]` |
| 东京客户 | organization_locations | `["Tokyo"]` |
| 东南亚客户 | organization_locations | `["Singapore", "Thailand", "Vietnam", "Indonesia", "Malaysia", "Philippines"]` |
| 欧洲客户 | organization_locations | `["United Kingdom", "Germany", "France", "Spain", "Italy", "Netherlands"]` |
| 中东客户 | organization_locations | `["United Arab Emirates", "Saudi Arabia", "Qatar"]` |
| 香港客户 | organization_locations | `["Hong Kong"]` |

### 4. person_titles 规则

推荐映射：

| 用户表达 | person_titles |
|----------|---------------|
| 商务合作负责人 | `["Business Development", "Business Development Manager", "Partnership Manager", "Head of Partnerships", "Commercial Director"]` |
| 采购负责人 | `["Procurement Manager", "Purchasing Manager", "Sourcing Manager", "Buyer"]` |
| 签约负责人 | `["Contracting Manager", "Supplier Manager", "Market Manager"]` |
| 酒店渠道 / 收益负责人 | `["Revenue Manager", "Distribution Manager", "Ecommerce Manager"]` |
| 老板 / 决策人 | `["CEO", "Founder", "Owner", "General Manager", "Managing Director"]` |
| 未指定联系人角色 | 可以不填 titles，但要补 seniorities |

### 5. person_seniorities 规则

- 未指定角色时，默认：`["manager", "director", "head", "vp"]`
- 明确找老板 / 决策人：`["owner", "founder", "c_suite"]`
- 明确找中层执行负责人：`["manager", "director", "head"]`
- 结果太少时，可以放宽到：`["manager", "director", "head", "vp", "c_suite"]`

### 6. contact_email_status 规则

默认使用：`["verified", "likely to engage"]`

只有在用户明确要求"邮箱质量更高"时，才收紧为：`["verified"]`

### 7. 公司规模 / 营收规则

| 用户表达 | 参数 | 值 |
|----------|------|-----|
| 大公司 | organization_num_employees_ranges | `["500,10000"]` |
| 中型公司 | organization_num_employees_ranges | `["50,500"]` |
| 中小企业 | organization_num_employees_ranges | `["10,500"]` |
| 年营收超过 100 万美元 | revenue_range_min | `1000000` |

### 8. 数量规则

- 默认 `per_page=10`
- 用户说"找 5 个"时用 `5`
- 不要默认传大于 10 的 `per_page`

---

## 搜索策略（非常重要）

### 第一轮：先保证命中

- 用行业词 + 业务模式词生成 `q_keywords`
- 用 `organization_locations` 限定区域
- `person_seniorities` 先不要太严
- `contact_email_status` 默认用 `["verified", "likely to engage"]`

### 第二轮：结果太少时自动放宽

如果第一轮结果为 0，或明显太少（少于 3 条），按下面顺序放宽并重新调用：

1. 放宽 `person_seniorities`
2. 去掉 `person_titles`，只保留行业词和地区
3. 保留核心行业词，减少过细的业务模式词
4. 如用户区域太窄，可放宽到更大的国家/区域级别

---

## 使用指南

### 步骤 1：理解并解析

收到用户需求后，先完成解析：行业类别、区域、联系人角色、联系人层级、公司规模，然后转成 Apollo 参数。

### 步骤 2：调用搜索并展示结果

调用 `/skill/search_customer_profile` 后，用下面格式回答：

```text
根据您的需求，我使用以下条件搜索：
- 关键词：{q_keywords}
- 公司地区：{organization_locations}
- 联系人岗位：{person_titles}
- 联系人层级：{person_seniorities}

共找到 {total_entries} 条匹配记录，本次获取 {count} 条：

1. {name}
   联系人：{contact_name}
   职位/备注：{remark}
   邮箱：{contact_email}
   电话：{contact_phone_prefix} {contact_phone}
   地区：{country_code}
   地址：{address}

是否要将这些客户录入 CRM 系统？也可以输入"下一页"查看更多。
```

### 步骤 3：确认导入

当用户回复"是""好的""导入""录入""确认"等肯定词时，调用 `/skill/batch_import_customer`。

### 步骤 4：导入反馈

```text
导入完成！成功 {success_count} 条，失败 {fail_count} 条。
如有失败，列出失败明细和原因。
```

---

## 场景模板

### 模板 1：找日本酒店合作负责人

```json
{
  "q_keywords": "hotel hospitality resort",
  "organization_locations": ["Japan"],
  "person_titles": ["Business Development", "Partnership Manager", "Commercial Director", "Revenue Manager", "Distribution Manager"],
  "person_seniorities": ["manager", "director", "head", "vp"],
  "contact_email_status": ["verified", "likely to engage"],
  "per_page": 10
}
```

### 模板 2：找东南亚酒店分销 / 批发客户

```json
{
  "q_keywords": "hotel wholesale travel distribution bedbank",
  "organization_locations": ["Singapore", "Thailand", "Vietnam", "Indonesia", "Malaysia", "Philippines"],
  "person_titles": ["Contracting Manager", "Supplier Manager", "Market Manager", "Business Development Manager"],
  "person_seniorities": ["manager", "director", "head"],
  "contact_email_status": ["verified", "likely to engage"],
  "per_page": 10
}
```

### 模板 3：找欧洲商旅 / TMC 客户

```json
{
  "q_keywords": "business travel corporate travel tmc",
  "organization_locations": ["United Kingdom", "Germany", "France", "Spain", "Italy", "Netherlands"],
  "person_titles": ["Head of Partnerships", "Commercial Director", "Business Development Director"],
  "person_seniorities": ["director", "head", "vp"],
  "contact_email_status": ["verified", "likely to engage"],
  "per_page": 10
}
```

---

## 注意事项

1. 接口返回 HTTP 401 或 `ok: false` 且 error 包含 `unauthorized` 时，删除 `{baseDir}/user_key.txt` 并重新引导用户获取 user_key
2. `q_keywords` 必须是英文关键词，不是中文句子
3. 默认优先使用 `organization_locations`，不是 `person_locations`
4. 默认邮箱状态建议使用 `["verified", "likely to engage"]`
5. 每次默认最多取 10 条，更多结果通过翻页获取
6. 导入时邮箱、联系人、电话、公司名是关键字段
