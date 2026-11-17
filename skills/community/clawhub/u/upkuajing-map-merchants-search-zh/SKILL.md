---
name: upkuajing-map-merchants-search-zh
description: 依托 Google‑Maps 商业数据库挖掘海外本地企业、线下门店和服务商。可按照所在区域、行业分类、商家评分筛选精准目标客户，助力外贸销售团队完成海外市场布局和线下渠道获客。
metadata: {"version":"1.0.6","homepage":"https://www.upkuajing.com","clawdbot":{"emoji":"📍","requires":{"bins":["python"],"env":["UPKUAJING_API_KEY"]},"primaryEnv":"UPKUAJING_API_KEY"}}
---

# 跨境魔方地图商户搜索

使用跨境魔方开放平台API查询商户信息。本技能提供基于地图的商户搜索，支持两种搜索模式：区域搜索和附近搜索。

## 概述

本技能通过以下方式访问跨境魔方的地图商户数据库：
- **商户搜索** (`merchants_search.py`)：按关键词和地理位置搜索商户
- **地理列表** (`geography_list.py`)：获取国家/州省/城市列表用于构建位置参数

## 运行脚本

### 环境配置

1. **检查 Python**：`python --version`
2. **安装依赖**：`pip install -r requirements.txt`

脚本目录：`scripts/*.py`
运行示例：`python scripts/*.py`

**重要**：始终使用直接脚本调用，如 `python scripts/merchants_search.py`。**不要使用** shell 复合命令如 `cd scripts && python merchants_search.py`。

## 两个主要API

### 商户搜索 (`merchants_search.py`)

按关键词和地理区域搜索商户。

**参数**：见 [商户搜索API](references/merchants-search-api.md)

**两种搜索模式**：
- **区域搜索**：按国家/州省/城市、关键词和筛选条件搜索
- **附近搜索**：使用 `geoDistance` 按经纬度坐标和半径搜索

**示例**：
```bash
# 国家搜索 - 查找巴西的餐厅
python scripts/merchants_search.py \
  --params '{"keywords":["restaurant"],"countryCodes":["BR"]}' \
  --query_count 100

# 多国家搜索并筛选有电话的 - 查找美国或中国有电话的餐厅
python scripts/merchants_search.py \
  --params '{"keywords":["restaurant"],"countryCodes":["US","CN"],"existPhone":true}' \
  --query_count 50

# 行业筛选 - 查找泰国的汽车经销商
python scripts/merchants_search.py \
  --params '{"keywords":["car dealer"],"countryCodes":["TH"],"industries":["Cars"]}' \
  --query_count 100

# 附近搜索 - 查找某点5公里范围内的酒店
python scripts/merchants_search.py \
  --params '{"keywords":["hotel"],"geoDistance":{"location":{"lat":31.1104643,"lon":29.7602221},"distance":"5km"}}'

# 省份/城市筛选 - 查找特定省份/城市的餐厅
python scripts/merchants_search.py \
  --params '{"keywords":["restaurant"],"provinceIds":["2277"],"cityIds":["19975"]}' \
  --query_count 50

# 店铺名称筛选 - 按名称查找店铺
python scripts/merchants_search.py \
  --params '{"companyNames":["car care"],"countryCodes":["TH"]}' \
  --query_count 100

# 多条件组合搜索 - 组合多个筛选条件
python scripts/merchants_search.py \
  --params '{"keywords":["restaurant"],"countryCodes":["US"],"provinceIds":["1447"],"industries":["Cars"],"existPhone":true}' \
  --query_count 50
```

**任务恢复**：使用 `--task_id` 恢复中断的大规模查询：
```bash
python scripts/merchants_search.py --task_id 'your-task-id-here' --query_count 2000
```

### 地理列表 (`geography_list.py`)

获取地理层级数据用于构建搜索参数。

**示例**：
```bash
# 获取国家列表
python scripts/geography_list.py --type country

# 获取某个国家的州省列表
python scripts/geography_list.py --type province --country_id 1

# 获取某个国家的城市列表
python scripts/geography_list.py --type city --country_id 1
```

## API密钥与跨境魔方账号

- **API密钥**：存储在 `~/.upkuajing/.env` 文件中，变量名为 `UPKUAJING_API_KEY`
- **首先检查**：如果未设置，提示用户提供或前往 [跨境魔方开放平台](https://developer.upkuajing.com/) 申请

### **API密钥未设置**
首先检查 `~/.upkuajing/.env` 文件中是否有 UPKUAJING_API_KEY；
如果 UPKUAJING_API_KEY 未设置，提示用户选择：
1. 用户已有密钥：用户自行添加（手动添加到 ~/.upkuajing/.env 文件）
2. 用户没有密钥：引导用户前往 [跨境魔方开放平台](https://developer.upkuajing.com/) 申请
等待用户选择；

### **账户充值**
当API返回余额不足时，解释并引导用户充值：
1. 创建充值订单 (`auth.py --new_rec_order`)
2. 根据订单响应，发送支付页面链接给用户，引导用户打开链接支付，用户确认支付成功后继续

### **获取账户信息**
获取UPKUAJING_API_KEY对应账户信息的脚本：`auth.py --account_info`

## API密钥与跨境魔方账号

- 新申请的API密钥：需要在 [跨境魔方开放平台](https://developer.upkuajing.com/) 注册登录后绑定账户

### **上报Skill调用异常**
当API调用失败或返回异常数据（服务端错误、超时、响应格式错误等）时，先用自然语言向用户解释异常情况，并询问是否需要上报给平台追踪；用户确认后才执行上报：
```bash
python scripts/error_report.py --params '{"requestPath":"/agent/map/search","requestId":"f47ac10b58cc4372a5670e02b2c3d479","context":"商户搜索查询失败，服务端异常"}'
```
- **不要上报正常业务情况**（余额不足、API密钥无效、参数错误等），按各自原有流程处理
- 异常上报不产生查询费用
- **参数说明**：参见 [异常上报API](references/skill-error-report-api.md)

## 费用

**商户搜索API调用收费**，不同接口计费方式不同。
**最新价格**：用户可访问 [详细价格说明](https://www.upkuajing.com/web/openapi/price.html)
或者使用：`python scripts/auth.py --price_info`（返回接口完整定价）

### 商户搜索计费规则

按**调用次数**计费，每次返回最多100条记录：
- 调用次数：`ceil(query_count / 100)` 次
- **只要 query_count > 100，执行前必须：**
  1. 告知用户预计调用次数
  2. 停止，等待用户在独立消息中明确确认后，再执行脚本

### 地理列表计费规则

**免费使用** — 国家/省/市列表查询不收取任何费用。

### 费用确认原则

**任何产生费用的操作必须先告知用户并等待明确确认，不得在通知的同一消息中执行。**

## 工作流程

### 决策指南

| 用户意图 | 使用API |
|---------|---------|
| "按国家/区域查找商户" | 商户搜索 (countryCodes) |
| "按省份/城市查找商户" | 商户搜索 (provinceIds, cityIds) |
| "在某个位置附近查找商户" | 商户搜索 (geoDistance) |
| "按行业或联系方式筛选" | 商户搜索 (industries, existPhone, existWebsite) |
| "按店铺名称查找" | 商户搜索 (companyNames) |
| "获取国家/州省/城市数据" | 地理列表 |

### 搜索流程

1. **区域搜索**：先使用地理列表获取国家/州省/城市ID
2. **构建搜索参数**：将关键词与地理过滤器结合
3. **执行搜索**：使用相应参数运行 merchants_search.py
4. **处理大规模查询**：使用 task_id 恢复中断的搜索

## 错误处理

- **API密钥无效/不存在**：检查 `~/.upkuajing/.env` 文件中的 `UPKUAJING_API_KEY`
- **余额不足**：引导用户充值
- **参数无效**：必须首先查看 references/ 目录中对应的API文档，从文档中获取正确的参数名和格式，不要猜测
- **Skill调用异常/响应异常**：先友好告知用户，经用户确认后用 `python scripts/error_report.py` 上报给平台（参见 [上报Skill调用异常](#上报skill调用异常)）

### API 文档参考

- 异常上报：查看 [references/skill-error-report-api.md](references/skill-error-report-api.md)

## 最佳实践

### 选择正确的搜索模式

1. **理解用户意图**：
   - 按国家/区域查找商户？ → 使用**国家搜索 (countryCodes)**
   - 按省份/城市查找商户？ → 使用**省份/城市搜索 (provinceIds, cityIds)**
   - 在某个位置附近查找商户？ → 使用**附近搜索 (geoDistance)**
   - 按行业或联系方式筛选？ → 使用 **industries, existPhone, existWebsite**
   - 按店铺名称查找？ → 使用 **companyNames**

2. **查看API文档**：
   - **执行搜索前，必须先查看对应的 API 参考文档**
   - 商户搜索：查看 [references/merchants-search-api.md](references/merchants-search-api.md)
   - 地理列表：查看 references/ 目录下对应文件
   - 不要猜测参数名称，从文档中获取准确的参数名称和格式

### 基于位置的搜索

1. **国家搜索覆盖大面积区域**：使用 `countryCodes` 配合关键词
2. **附近搜索精确定位**：使用 `geoDistance` 配合位置和距离

### 参数指南

- **关键词**：使用英文关键词以获得更好的结果
- **筛选条件**：使用 `existPhone=true` 或 `existWebsite=true` 按联系方式可用性筛选
- **行业筛选**：使用 `industries` 按商业类型筛选
- **省份/城市筛选**：使用 `provinceIds` 和 `cityIds` 按特定省份或城市筛选
- **店铺名称筛选**：使用 `companyNames` 按店铺名称筛选
- **附近搜索**：distance 格式如 "5km"，建议范围 1-10km
- **搜索数量会影响接口的响应时间**，大量查询时注意设置合理的 query_count

### 处理结果

1. **大数量查询时注意文件大小**：jsonl 文件可能较大
2. **使用 task_id 恢复中断的查询**：避免重复调用和费用浪费

## 注意事项

- 国家代码使用 ISO 3166-1 alpha-2 格式（如 CN、US、BR）
- 文件路径在所有平台上使用正斜杠
- **不要猜测参数名**，从文档中获取准确的参数名和格式
- **禁止输出技术参数格式**：不要在回复中展示代码样式的参数，应将其转换为自然语言
- **不要估算或猜测每次调用的费用** — 使用 `python scripts/auth.py --price_info` 获取准确定价信息

## 相关技能

其他您可能会用到的跨境魔方技能：

- linkedin-person-search — 领英找人
- global-company-person-search — 全球企业库找人
- linkedin-company-search — 领英找公司
- global-company-search — 全球企业库找公司
- global-company-shareholder — 全球企业库股东查询
- global-company-employee — 全球企业库员工查询
- global-company-person-colleague — 全球企业库同事查询
- global-company-person-alumni — 全球企业库校友查询
- global-company-person-experience — 全球企业库工作经历查询
- global-company-person-education — 全球企业库教育经历查询
- global-company-person-school-detail — 全球企业库学校详情查询
- upkuajing-global-company-people-search — 全球企业与人员搜索
- upkuajing-customs-trade-company-search — 海关贸易企业搜索
- upkuajing-email-tool — 发送邮件和管理邮件任务
- upkuajing-sms-tool — 发送短信和管理短信任务
- upkuajing-contact-info-validity-check — 联系方式有效性检测
- phone-validity-check — 电话号码有效性检测
- email-validity-check — 邮箱地址有效性检测
- domain-validity-check — 域名有效性检测