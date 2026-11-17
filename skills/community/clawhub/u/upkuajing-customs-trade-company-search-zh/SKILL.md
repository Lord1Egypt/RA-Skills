---
name: upkuajing-customs-trade-company-search-zh
description: 调取真实可靠的全球海关进出口记录，挖掘各行各业的进口商、出口商与采购商；可依托产品品类及原产国筛选目标企业、海外采购客户和优质供应商，助力外贸人员精准开发全球合作伙伴。
metadata: {"version":"1.0.11","homepage":"https://www.upkuajing.com","clawdbot":{"emoji":"🏢","requires":{"bins":["python"],"env":["UPKUAJING_API_KEY"]},"primaryEnv":"UPKUAJING_API_KEY"}}
---

# 跨境魔方海关贸易公司搜索

使用跨境魔方开放平台API通过海关贸易数据搜索公司。本技能采用**数据驱动方式**：通过分析贸易记录和交易模式来查找公司。

## 概述

本技能通过四个脚本提供对跨境魔方海关贸易数据API的访问：两种搜索方式（贸易列表、公司列表）和两个增强接口（公司详情、联系信息）; 
通过`auth.py`脚本提供 API密钥生成、充值；

## 脚本运行

### 环境准备

1. **检查 Python**：`python --version`
2. **安装依赖**：`pip install -r requirements.txt`

脚本目录：`scripts/*.py`
运行示例：`python scripts/*.py`

**重要**：始终使用直接脚本调用，如 `python scripts/trade_list_search.py`。**不要使用** shell 复合命令如 `cd scripts && python trade_list_search.py`。

### 两种搜索方式

**贸易列表搜索** (`trade_list_search.py`)
- **返回粒度**：每条贸易订单为一行记录
- **适用场景**：关心的是"发生了什么交易"
- **示例**：
   - "显示A公司采购LED的所有订单"
   - "找进/出口到美国的大豆贸易记录"
   - "查看某段时间内的具体交易明细"
- **参数**：查看参数说明 [贸易列表](references/trade-list-api.md)


**公司列表搜索** (`company_list_search.py`)
- **返回粒度**：对贸易订单按公司聚合后，每家公司为一行
- **适用场景**：关心的是"有哪些公司"
- **示例**：
  - "找采购过LED的公司有哪些"
  - "找与中国有电子产品进出口往来的美国公司"
  - "找有中美贸易往来的公司"（物流行业客户开发）
- **参数**：查看参数说明 [公司列表](references/company-list-api.md)


### 两个增强功能

在获取到贸易列表或公司列表后，如有必要，可通过以下接口对结果中的公司ID进行信息增强：
**公司详情** (`company_get_details.py --companyIds *`)
- 获取公司信息（不包括联系方式）
- **参数**：`--companyIds` 公司ID列表（空格分隔），一次最多20个
- **API业务参数**：[公司详情](references/company-detail-api.md)

**联系信息** (`company_get_contact.py --companyIds *`)
- 获取联系方式详情 邮箱、电话、社交媒体、网站
- **参数**：`--companyIds` 公司ID列表（空格分隔），一次最多20个
- **API业务参数**：[获取联系方式](references/contact-fetch-api.md)

## API密钥与充值
使用此技能需要API密钥。API密钥保存在 `~/.upkuajing/.env` 文件中：
```bash
cat ~/.upkuajing/.env
```
**文件内容示例**：
```
UPKUAJING_API_KEY=your_api_key_here
```
### **未设置API密钥**
请先检查 `~/.upkuajing/.env` 文件是否有 UPKUAJING_API_KEY;
如果未设置 UPKUAJING_API_KEY API密钥，请提示并让用户选择：
1. 用户有，由用户提供(手动添加到 ~/.upkuajing/.env 文件)
2. 用户没有，你可使用接口进行申请（`auth.py --new_key`），申请到新密钥后，会自动保存到 ~/.upkuajing/.env
等待用户选择；

### **账户充值**
如果调用接口响应账户余额不足时，需说明并引导用户进行账户充值：
1. 创建充值订单（`auth.py --new_rec_order`）
2. 根据订单响应，发送支付页面URL给用户，引导用户打开地址付款，付款成功后告诉你；

### **获取账户信息**
可通过此脚本，获取UPKUAJING_API_KEY对应的账户信息 `auth.py --account_info`
  
## API密钥与跨境魔方账号
- 新申请的API密钥：在[跨境魔方开放平台](https://developer.upkuajing.com/)注册、登录后进行账号绑定

### **上报Skill调用异常**
当API调用失败或返回异常数据（服务端错误、超时、响应格式错误等）时，先用自然语言向用户解释异常情况，并询问是否需要上报给平台追踪；用户确认后才执行上报：
```bash
python scripts/error_report.py --params '{"requestPath":"/agent/customs/company/list","requestId":"f47ac10b58cc4372a5670e02b2c3d479","context":"海关贸易公司搜索查询失败，服务端异常"}'
```
- **不要上报正常业务情况**（余额不足、API密钥无效、参数错误等），按各自原有流程处理
- 异常上报不产生查询费用
- **参数说明**：参见 [异常上报API](references/skill-error-report-api.md)

## 费用

**所有API调用都会产生费用**，不同接口计费方式不同。
**最新价格**：用户可访问 [详细价格说明](https://www.upkuajing.com/web/openapi/price.html)
或者使用：`python scripts/auth.py --price_info`（返回接口完整定价）

### 列表搜索计费规则

按**调用次数**计费，每次返回最多20条记录：
- 调用次数：`ceil(query_count / 20)` 次
- **只要 query_count > 20，执行前必须：**
  1. 告知用户预计调用次数
  2. 停止，等待用户在独立消息中明确确认后，再执行脚本

### 增强接口计费规则

按**传入的ID数量**计费，每次最多可以传入20个ID：
- 传入1个ID = 计费1次
- 传入20个ID = 计费20次（单次上限）
- **批量获取前必须：**
  1. 告知用户传入ID数量及对应费用次数
  2. 停止，等待用户在独立消息中明确确认后，再执行脚本

### 费用确认原则

**任何会产生费用的操作，都必须先告知、等待用户明确确认，不得在告知的同一条消息中直接执行。**


## 工作流程
根据用户意图选择合适的API

### 决策指南

| 用户意图 | 使用API |
|-------------|---------|
| "分析贸易模式/订单数据" | 贸易列表 |
| "找采购XXX的公司" | 公司列表 |
| "找XXX的供应商，有邮箱" | 公司列表 existEmail=1 |
| "获取公司详细信息" | 公司详情 |
| "获取联系方式" | 联系信息 |

## 使用示例

### 场景1: 小量查询 — 贸易数据分析

**用户请求**："显示2024年出口到美国的LED灯具贸易数据"
```bash
python scripts/trade_list_search.py \
  --params '{"products": ["LED lights"], "buyerCountryCodes": ["US"], "dateStart": 1704067200000, "dateEnd": 1735689599999}' \
  --query_count 20
```

如需进一步获取供应商详情（支持批量查询）：
```bash
python scripts/company_get_details.py --companyIds 123456 789012 ...
```

### 场景 2: 大量查询 — 大数据集分析

**用户请求**："分析2024年的100条大豆贸易数据"
**执行前**告知用户：ceil(100/20) = 5 次API调用，确认后再执行；
```bash
python scripts/trade_list_search.py --params '{"products": ["soybean"], "dateStart": 1704067200000, "dateEnd": 1735689599999}' --query_count 100
```

### 场景 3: 超大量查询 - 需要多次调用脚本

**用户请求**："找从中国进口电子产品的2000家公司，要有邮箱"
**执行前**告知用户：ceil(2000/20) = 100 次API调用，确认后再执行；
```bash
python scripts/company_list_search.py --params '{"companyType": 2, "sellerCountryCodes": ["CN"], "existEmail": 1}' --query_count 1000
```
**执行结束**：脚本响应 {"task_id":"a1b2-c3d4", "file_url": "xxxxx", ……}
**继续执行，追加数据**：指定task_id，让脚本从上次的cursor处继续查询并追加到文件
```bash
python scripts/company_list_search.py --task_id 'a1b2-c3d4' --query_count 1000
```

## 错误处理

- **API密钥无效/不存在**：检查 `~/.upkuajing/.env` 文件中的 `UPKUAJING_API_KEY`
- **余额不足**：根据**账户充值**步骤，引导用户充值
- **参数无效**：**必须先查看 references/ 目录下的对应 API 文档**，检查参数名称和格式，不要猜测
- **Skill调用异常/响应异常**：先友好告知用户，经用户确认后用 `python scripts/error_report.py` 上报给平台（参见 [上报Skill调用异常](#上报skill调用异常)）

### API 文档参考

- 异常上报：查看 [references/skill-error-report-api.md](references/skill-error-report-api.md)

## 最佳实践

### 选择正确的方法

1. **理解用户意图**：
   - 分析贸易数据？ → 使用**贸易列表搜索**
   - 寻找客户/合作伙伴？ → 使用**公司列表搜索**

2. **查看API文档**：
   - **执行列表查询前，必须先查看对应的 API 参考文档**
   - 贸易列表：查看 [references/trade-list-api.md](references/trade-list-api.md)
   - 公司列表：查看 [references/company-list-api.md](references/company-list-api.md)

3. **识别参数条件**：
   - 设定日期范围
   - HS编码通常比产品名称 筛选效果更精准
   - 通过筛选特定国家来减少噪音
   - 使用ISO国家代码：CN、US、JP等
   - 使用筛选条件查找有联系信息的公司

### 处理结果

3. **谨慎处理jsonl文件**：对数据量大的查询，注意文件大小

4. **逐步丰富信息**：仅在需要时调用详情/联系接口
   - 两个列表接口返回的公司ID都可以用于两个详情接口
   - 如果用户只需要少数公司，不要为所有公司获取详情

## 注意事项
- 所有时间戳均为毫秒级
- 国家代码使用ISO 3166-1 alpha-2格式（例如：CN、US、JP）
- 文件路径在所有平台上都使用正斜杠
- 产品名称、行业名称需要使用**英文**
- 搜索数量会影响接口的响应时间，建议设置 timeout:120
- **禁止输出技术参数格式**：不要在回复中展示代码样式的参数，应将其转换为自然语言
- **不要估算或猜测每次调用的费用** — 使用 `python scripts/auth.py --price_info` 获取准确定价信息
- **不要**猜测参数名称，从文档中获取准确的参数名称和格式

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
- upkuajing-email-tool — 发送邮件和管理邮件任务
- upkuajing-map-merchants-search — 基于地图的商家搜索
- upkuajing-sms-tool — 发送短信和管理短信任务
- upkuajing-contact-info-validity-check — 联系方式有效性检测
- phone-validity-check — 电话号码有效性检测
- email-validity-check — 邮箱地址有效性检测
- domain-validity-check — 域名有效性检测