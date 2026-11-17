---
name: upkuajing-global-company-people-search-zh
description: 搜索全球企业信息、个人信息，用于全球贸易、跨境出口、海外采购商的线索开发。帮助出口贸易商、采购商、服务商、代理商及销售团队通过搜索，得到企业决策人信息、企业高管信息；寻找供应商，并加速海外客户获取。本产品提供企业注册信息、背景资料以及联系方式（邮箱、电话、WhatsApp）。适用于海外客户开发、企业背调、人才搜索等场景。
metadata: {"version":"1.0.10","homepage":"https://www.upkuajing.com","clawdbot":{"emoji":"🏢","requires":{"bins":["python"],"env":["UPKUAJING_API_KEY"]},"primaryEnv":"UPKUAJING_API_KEY"}}
---

# 跨境魔方企业与人物搜索

使用跨境魔方开放平台API查询企业工商信息和人物数据。本技能采用**实体驱动方式**：通过公司属性（产品、行业、规模）和人物属性（职位、学校、经历）直接查找目标实体。

## 概述

本技能通过五个脚本提供对跨境魔方全球企业库和人物数据的访问：两种列表搜索（公司、人物）和三个增强接口（公司详情、人物详情、联系方式）。
通过`auth.py`脚本提供 API密钥生成、充值；

## 脚本运行

### 环境准备

1. **检查 Python**：`python --version`
2. **安装依赖**：`pip install -r requirements.txt`

脚本目录：`scripts/*.py`
运行示例：`python scripts/*.py`

**重要**：始终使用直接脚本调用，如 `python scripts/company_list_search.py`。**不要使用** shell 复合命令如 `cd scripts && python company_list_search.py`。

### 两种搜索方式

**公司列表搜索** (`company_list_search.py`)
- **返回粒度**：每家公司为一行记录
- **适用场景**：关心的是"有哪些公司"
- **示例**：
   - "找生产LED灯的厂家"
   - "找员工规模100-500人的科技公司"
- **参数**：查看参数说明 [公司列表](references/company-list-api.md)

**人物列表搜索** (`human_list_search.py`)
- **返回粒度**：每个人物为一行记录
- **适用场景**：关心的是"有哪些人"
- **示例**：
  - "找XXXX的CTO"
  - "找XXX中国区的销售总监"
- **参数**：查看参数说明 [人物列表](references/human-list-api.md)

### 三个增强接口

在获取到公司或人物列表后，如有必要，可通过以下接口获取信息增强；

**公司详情** (`company_details.py --pids *`)
- 获取公司工商信息（不包括联系方式）
- **参数**：`--pids` 公司ID列表（空格分隔，从列表搜索获取），一次最多20个

**人物详情** (`human_details.py --hids *`)
- 获取人物详细信息（教育经历、工作履历等）
- **参数**：`--hids` 人物ID列表（空格分隔，从列表搜索获取），一次最多20个

**联系方式** (`get_contact.py --bus_type * --bus_ids *`)
- 获取联系方式（邮箱、电话、WhatsApp、社媒、网站）
- **参数**：
  - `--bus_type`: 1=公司，2=人物
  - `--bus_ids`: 公司ID或人物ID 列表（空格分隔，从列表搜索获取），一次最多20个

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
python scripts/error_report.py --params '{"requestPath":"/agent/search/company/list","requestId":"f47ac10b58cc4372a5670e02b2c3d479","context":"企业与人搜索查询失败，服务端异常"}'
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
根据用户意图选择合适的API。

### 决策指南

| 用户意图 | 使用API |
|-------------|---------|
| "找生产XXX的公司" | 公司列表 |
| "找有邮箱/电话的公司" | 公司列表 existEmail=1/existPhone=1 |
| "找XX公司的CEO/CTO" | 人物列表 |
| "找采购XXX的客户" | 公司列表 |
| "获取人物履历" | 人物详情 |
| "获取公司联系方式" | 联系方式 bus_type=1 |

## 使用示例

### 场景1: 小量查询 — 搜索公司

**用户请求**："找生产LED灯的中国厂家"
```bash
python scripts/company_list_search.py \
  --params '{"products": ["LED lights"], "countryCodes": ["CN"], "existEmail": 1}' \
  --query_count 20
```

### 场景2: 搜索人物

**用户请求**："找XXXX的CTO"
```bash
python scripts/human_list_search.py \
  --params '{"companyNames": ["XXXX"], "titleRoles": ["CTO"]}' \
  --query_count 20
```

### 场景3: 大量查询 — 需要多次调用脚本

**用户请求**："找1000家有邮箱的美国电子产品进口商"
**执行前**告知用户：ceil(1000/20) = 50 次API调用，确认后再执行。
```bash
python scripts/company_list_search.py --params '{"products": ["electronics"], "countryCodes": ["US"], "existEmail": 1}' --query_count 1000
```
**执行结束**：脚本响应 {"task_id":"a1b2-c3d4", "file_url": "xxxxx", ……}
**继续执行，追加数据**：指定task_id，让脚本从上次的cursor处继续查询并追加到文件
```bash
python scripts/company_list_search.py --task_id 'task-id-here' --query_count 2000
```

## 错误处理

- **API密钥无效/不存在**：检查 `~/.upkuajing/.env` 文件中的 `UPKUAJING_API_KEY`
- **余额不足**：引导用户充值
- **参数无效**：**必须先查看 references/ 目录下的对应 API 文档**，从文档中获取正确的参数名称和格式，不要猜测
- **Skill调用异常/响应异常**：先友好告知用户，经用户确认后用 `python scripts/error_report.py` 上报给平台（参见 [上报Skill调用异常](#上报skill调用异常)）

### API 文档参考

- 异常上报：查看 [references/skill-error-report-api.md](references/skill-error-report-api.md)

## 最佳实践

### 选择正确的方法

1. **理解用户意图**：
   - 找公司？ → 使用**公司列表搜索**
   - 找人？ → 使用**人物列表搜索**

2. **查看API文档**：
   - **执行列表查询前，必须先查看对应的 API 参考文档**
   - 公司列表：查看 [references/company-list-api.md](references/company-list-api.md)
   - 人物列表：查看 [references/human-list-api.md](references/human-list-api.md)
   - 不要猜测参数名称，从文档中获取准确的参数名称和格式

3. **优化查询参数**：
   - 使用 `products` 参数精确筛选产品，需翻译为英文
   - 使用 `existEmail=1` 或 `existPhone=1` 筛选有联系方式的实体
   - 使用 `countryCodes` 限定国家范围

### 处理结果

3. **谨慎处理jsonl文件**：对数据量大的查询，注意文件大小
4. **逐步丰富信息**：仅在需要时调用详情/联系接口
   - 两个列表接口返回的公司ID都可以用于两个详情接口
   - 如果用户只需要少数公司，不要为所有公司获取详情

## 注意事项
- 人物搜索用 hids，公司搜索用 pids，注意区分
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
- upkuajing-customs-trade-company-search — 海关贸易企业搜索
- upkuajing-email-tool — 发送邮件和管理邮件任务
- upkuajing-map-merchants-search — 基于地图的商家搜索
- upkuajing-sms-tool — 发送短信和管理短信任务
- upkuajing-contact-info-validity-check — 联系方式有效性检测
- phone-validity-check — 电话号码有效性检测
- email-validity-check — 邮箱地址有效性检测
- domain-validity-check — 域名有效性检测