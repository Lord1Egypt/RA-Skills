---
name: upkuajing-sms-tool-zh
description: 对接全球通信运营商发送批量跨境短信，实时查看每条短信的发送状态，助力外贸从业者开展海外营销推广、订单物流通知以及客户精细化触达。
metadata: {"version":"1.0.4","homepage":"https://www.upkuajing.com","clawdbot":{"emoji":"📱","requires":{"bins":["python"],"env":["UPKUAJING_API_KEY"]},"primaryEnv":"UPKUAJING_API_KEY"}}
---

# 跨境魔方短信工具

使用跨境魔方开放平台API发送短信和跟踪短信任务状态。

## 概述

本技能通过三个脚本提供对跨境魔方短信服务的访问：
- **短信发送** (`sms_send.py`): 向手机号发送短信
- **短信任务列表** (`sms_task_list.py`): 查看短信任务列表，支持时间范围筛选
- **短信任务明细** (`sms_task_record_list.py`): 查看特定任务的详细记录

## 脚本运行

### 环境准备

1. **检查 Python**：`python --version`
2. **安装依赖**：`pip install -r requirements.txt`

脚本目录：`scripts/*.py`
运行示例：`python scripts/*.py`

**重要**：始终使用直接脚本调用，如 `python scripts/sms_send.py`。**不要使用** shell 复合命令如 `cd scripts && python sms_send.py`。

## 三个主要API

### 短信发送 (`sms_send.py`)

向手机号发送短信。

**参数**：查看参数说明 [短信发送](references/sms-send-api.md)

**示例**：
```bash
# 发送简单短信
python scripts/sms_send.py \
  --content "这是短信内容" \
  --phones '["13800138000"]'

# 双向模式发送（支持接收回复）
python scripts/sms_send.py \
  --content "这是短信内容" \
  --phones '["13800138000"]' \
  --channel_type 1

# 发送多个手机号
python scripts/sms_send.py \
  --content "这是短信内容" \
  --phones '["13800138000","13800138001"]'
```

### 短信任务列表 (`sms_task_list.py`)

查看短信任务列表，支持可选的时间范围筛选。

**参数**：查看参数说明 [短信任务列表](references/sms-task-list-api.md)

**示例**：
```bash
# 获取任务列表（第一页，10条）
python scripts/sms_task_list.py --page_no 1 --page_size 10

# 按时间范围筛选
python scripts/sms_task_list.py \
  --start_time 1775812273 \
  --end_time 1775900000 \
  --page_no 1 \
  --page_size 10

# 按状态筛选（0-待发送 1-发送中 2-发送完成）
python scripts/sms_task_list.py --status 2 --page_no 1 --page_size 10
```

### 短信任务明细 (`sms_task_record_list.py`)

查看特定短信任务的详细记录。

**参数**：查看参数说明 [短信任务明细](references/sms-task-record-list-api.md)

**示例**：
```bash
# 获取任务ID为1496的明细
python scripts/sms_task_record_list.py --task_id 1496 --page_no 1 --page_size 10

# 按时间和状态筛选
python scripts/sms_task_record_list.py \
  --task_id 1496 \
  --start_time 1775812273 \
  --end_time 1775900000 \
  --status 2 \
  --page_no 1 \
  --page_size 10
```

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

### **上报Skill调用异常**
当API调用失败或返回异常数据（服务端错误、超时、响应格式错误等）时，先用自然语言向用户解释异常情况，并询问是否需要上报给平台追踪；用户确认后才执行上报：
```bash
python scripts/error_report.py --params '{"requestPath":"/agent/sms/send","requestId":"f47ac10b58cc4372a5670e02b2c3d479","context":"短信发送失败，服务端异常"}'
```
- **不要上报正常业务情况**（余额不足、API密钥无效、参数错误等），按各自原有流程处理
- 异常上报不产生查询费用
- **参数说明**：参见 [异常上报API](references/skill-error-report-api.md)

## 费用

**短信发送API调用会产生费用**，不同接口计费方式不同。

**最新价格**：用户可访问 [详细价格说明](https://www.upkuajing.com/web/openapi/price.html)
或者使用：`python scripts/auth.py --price_info`（返回接口完整定价）

### 短信发送计费规则

**短信发送收费** — 每次发送请求根据手机号数量计费。

### 任务列表与明细计费规则

**免费** — 任务列表和任务明细查询不收取费用。

### 费用确认原则

**任何会产生费用的操作，都必须先告知、等待用户明确确认，不得在告知的同一条消息中直接执行。**

## 工作流程

### 决策指南

| 用户意图 | 使用API |
|-------------|---------|
| "发送一条短信" | 短信发送 |
| "查看我的短信任务" | 短信任务列表 |
| "查看短信投递状态" | 短信任务明细 |
| "查找某个时间范围的任务" | 短信任务列表（带 start_time/end_time） |

### 短信发送流程

1. **准备短信内容**：内容、手机号列表
2. **执行发送**：使用 sms_send.py 及相应参数
3. **获取响应**：API 同步返回任务结果

### 任务查看流程

1. **查看任务列表**：使用 sms_task_list.py，可选时间筛选
2. **获取任务ID**：从任务列表响应中获取
3. **查看任务明细**：使用 sms_task_record_list.py 及 task_id

## 错误处理

- **API密钥无效/不存在**：检查 `~/.upkuajing/.env` 文件中的 `UPKUAJING_API_KEY`
- **余额不足**：引导用户充值
- **参数无效**：**必须先查看 references/ 目录下的对应 API 文档**，从文档中获取正确的参数名称和格式，不要猜测
- **Skill调用异常/响应异常**：先友好告知用户，经用户确认后用 `python scripts/error_report.py` 上报给平台（参见 [上报Skill调用异常](#上报skill调用异常)）

### API 文档参考

- 短信发送：查看 [references/sms-send-api.md](references/sms-send-api.md)
- 短信任务列表：查看 [references/sms-task-list-api.md](references/sms-task-list-api.md)
- 短信任务明细：查看 [references/sms-task-record-list-api.md](references/sms-task-record-list-api.md)
- 异常上报：查看 [references/skill-error-report-api.md](references/skill-error-report-api.md)

## 注意事项

- 文件路径在所有平台上都使用正斜杠
- **不要猜测参数名称**，从文档中获取准确的参数名称和格式
- **禁止输出技术参数格式**：不要在回复中展示代码样式的参数，应将其转换为自然语言
- **不要估算或猜测费用** — 使用 `python scripts/auth.py --price_info` 获取准确定价信息
- **短信发送是同步提交**：API 提交后立即返回响应，但短信服务器会异步处理；响应中 `status` 字段表示发送状态（1-发送中 2-发送成功 3-失败 4-部分成功）

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
- upkuajing-map-merchants-search — 基于地图的商家搜索
- upkuajing-contact-info-validity-check — 联系方式有效性检测
- phone-validity-check — 电话号码有效性检测
- email-validity-check — 邮箱地址有效性检测
- domain-validity-check — 域名有效性检测