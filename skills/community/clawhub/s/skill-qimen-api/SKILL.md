---
name: skill-qimen-api
description:
  en: Official Xiaoqi Intelligent Calculation API for BaZi and Qi Men Dun Jia. This service requires XIAOQIZHISUAN_API_KEY credential for authentication. 
  zh: 小奇智算官方API，提供八字、奇门遁甲测算服务，需配置XIAOQIZHISUAN_API_KEY密钥鉴权。
metadata:
  claw:
    emoji: ☯️
    homepage: https://www.xiaoqizhisuan.cn
    provider: 小奇智算
    privacyPolicy: https://www.xiaoqizhisuan.cn/privacy.html
    termsOfService: https://www.xiaoqizhisuan.cn/terms.html
    requiredEnvVars:
      - XIAOQIZHISUAN_API_KEY
    requiredCredentials:
      - type: apiKey
        name: XIAOQIZHISUAN_API_KEY
        description: Official API key for authentication with xiaoqizhisuan.cn MCP service
    billing:
        model: pay_per_call
        requires_user_confirmation: true
        per_session_spend_cap: ¥2
        max_retries_per_call: 1

---
# 小奇智算 API 能力 | Xiaoqi Intelligent Calculation API Skill

GET APIKEY：https://www.xiaoqizhisuan.cn/account.html

GET HELP: https://www.xiaoqizhisuan.cn/help.html

## 可用工具 | Available Tools
### 1. bazi_dayun - 八字大运查询 | BaZi Great Fortune Query
```
价格 | Price: ¥0.2 / time / 次
参数 | Parameters:
 year (integer, 必填) 出生年（公历）
 month (integer, 必填) 出生月
 day (integer, 必填) 出生日
 hour (integer, 必填) 出生时（0-23）
 xingbie (string, 必填) 性别（"男" / "女"）

返回 | Return:
 success, cost, balance, bazi, dayun, error

```
实测结果 | real test： https://www.xiaoqizhisuan.cn/examples/example_1_bazi_dayun.html


### 2. qimen_paipan - 奇门排盘（JSON 数据）| Qi Men Chart Generation (JSON Data)
```
价格 | Price: ¥0.5 / time / 次
参数 | Parameters:
 year (integer, 必填) 年
 month (integer, 必填) 月
 day (integer, 必填) 日
 hour (integer, 必填) 时（0-23）
 minute (integer, 选填, 默认0) 分
 number (integer, 选填, 默认1) 排盘方法（1=拆补法, 2=置润法）

返回 | Return:
 success, cost, balance, data, error

```
实测结果 | real test： https://www.xiaoqizhisuan.cn/examples/example_2_qimen_paipan.html


### 3. qimen_paipan_image - 奇门排盘+HTML网页图 | Qi Men Chart Generation + HTML Webpage Chart
```
参数 | Parameters:
 year (integer, 必填) 年
 month (integer, 必填) 月
 day (integer, 必填) 日
 hour (integer, 必填) 时（0-23）
 minute (integer, 选填, 默认0)
 number (integer, 选填, 默认1)

返回 | Return:
 success, cost, balance, data, html_url, error

```
实测结果 | real test： https://www.xiaoqizhisuan.cn/examples/example_3_qimen_paipan_image.html


### 4. qimen_jiepan - 即时盘解析准备 | Immediate Chart Analysis Preparation
```
价格 | Price: ¥1.0 / time / 次
参数 | Parameters:
 year, month, day, hour (integer, 必填) 起盘时间
 minute (integer, 选填, 默认0)
 number (integer, 选填, 默认1)
 question (string, 必填)

返回 | Return:
 success, cost, balance, html_url, system_prompt, user_prompt, error

```
实测结果 | real test： https://www.xiaoqizhisuan.cn/examples/example_4_qimen_jiepan.html


### 5. qimen_jiepan_lifetime - 终身盘解析准备 | Lifetime Chart Analysis Preparation
```
价格 | Price: ¥1.2 / time / 次
参数 | Parameters:
 year, month, day, hour (integer, 必填)
 xingbie (string, 必填) 性别（"男"/"女"）
 minute (integer, 选填, 默认0)
 number (integer, 选填, 默认1)
 question (string, 必填)

返回 | Return:
 success, cost, balance, bazi, dayun, html_url, system_prompt, user_prompt, error

```
实测结果 | real test： https://www.xiaoqizhisuan.cn/examples/example_5_qimen_jiepan_lifetime.html


### 6. qimen_full - 即时局完整解盘 | Complete Immediate Chart Interpretation
```
价格 | Price: ¥1.5 / time / 次
参数 | Parameters:
 year, month, day, hour (integer, 必填)
 minute (integer, 选填, 默认0)
 number (integer, 选填, 默认1)
 question (string, 必填)

返回 | Return:
 success, cost, balance, html_url, system_prompt, user_prompt, jiepan_result, error

```
实测结果 | real test： https://www.xiaoqizhisuan.cn/examples/example_6_qimen_full.html


### 7. qimen_full_lifetime - 终身局完整解盘 | Complete Lifetime Chart Interpretation
```
价格 | Price: ¥2.0 / time / 次
参数 | Parameters:
 year, month, day, hour (integer, 必填)
 xingbie (string, 必填) 性别（"男"/"女"）
 minute (integer, 选填, 默认0)
 number (integer, 选填, 默认1)
 question (string, 必填)

返回 | Return:
 success, cost, balance, bazi, dayun, html_url, system_prompt, user_prompt, jiepan_result, error

```
实测结果 | real test： https://www.xiaoqizhisuan.cn/examples/example_7_qimen_full_lifetime.html


## API 调用方式 | API Integration Methods
### MCP 服务对接 | MCP Server Configuration
OpenClaw / Hermes / mcporter 配置 | Configuration
```json
{
  "mcpServers": {
    "xiaoqi": {
      "type": "streamable-http",
      "url": "https://www.xiaoqizhisuan.cn/mcp",
      "headers": {
        "x-api-key": "${XIAOQIZHISUAN_API_KEY}",
        "Accept": "application/json, text/event-stream"
      }
    }
  }
}
```

Claude Desktop / Cursor / Windsurf 配置 | Configuration
```json
{
  "mcpServers": {
    "xiaoqi": {
      "url": "https://www.xiaoqizhisuan.cn/mcp",
      "headers": {
        "x-api-key": "${XIAOQIZHISUAN_API_KEY}",
        "Accept": "application/json, text/event-stream"
      }
    }
  }
}
```

# 直接 HTTP 调用 | Direct HTTP Request
##通用 Curl 请求示例 | Universal Curl Demo

### 1. 初始化连接 | Initialize Connection
```bash
curl -X POST https://www.xiaoqizhisuan.cn/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "x-api-key: ${XIAOQIZHISUAN_API_KEY}" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
      "protocolVersion": "2025-03-26",
      "capabilities": {},
      "clientInfo": {"name": "my-client", "version": "1.0"}
    }
  }'
```
### 2. 获取工具列表 | Fetch Tool List
```bash
curl -X POST https://www.xiaoqizhisuan.cn/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "x-api-key: ${XIAOQIZHISUAN_API_KEY}" \
  -d '{
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/list",
    "params": {}
  }'
```
### 3. 调用指定工具 | Call Target Tool
```bash
curl -X POST https://www.xiaoqizhisuan.cn/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "x-api-key: ${XIAOQIZHISUAN_API_KEY}" \
  -d '{
    "jsonrpc": "2.0",
    "id": 3,
    "method": "tools/call",
    "params": {
      "name": "bazi_dayun",
      "arguments": {
        "year": 1990, "month": 5, "day": 15, "hour": 8, "xingbie": "男"
      }
    }
  }'
```

## 错误码说明 | Error Code Explanation
- 401: 缺少或无效 API 密钥 | Missing or invalid API Key
- 402: 账户余额不足 | Insufficient account balance
- 403: API 密钥已封禁 | API Key disabled
- 500: 服务端内部异常 | Server internal error

## 注意事项 | Notes
1. EN: This service is driven by data analysis and cognitive science for rational decision reference.
   CN: 本服务基于数据分析与认知科学，仅作理性决策参考。
2. EN: No feudal superstitious content is involved.
   CN: 内容不含封建迷信导向。
3. EN: It is recommended to add a disclaimer when using this service.
   CN: 接入使用时建议补充免责声明。

---
## 服务商声明 | Service Provider Statement
CN: 本技能为【小奇智算】官方自研服务，运营主体、接口计费、隐私规则均公示于官网：
EN: This skill is an official self-developed service of [Xiaoqi Intelligent Calculation]. The operating entity, interface billing, and privacy rules are publicly available on the official website:

官网 | Official Website: https://www.xiaoqizhisuan.cn

隐私政策 | Privacy Policy: https://www.xiaoqizhisuan.cn/privacy.html

服务条款 | Terms of Service: https://www.xiaoqizhisuan.cn/terms.html

CN: 本服务为明码标价按量计费，所有接口价格、扣费规则均文档公示，无隐性收费。
EN: This service uses transparent pay-per-call pricing. All interface prices and deduction rules are publicly documented with no hidden fees.

---

### 关键术语对照（统一规范）
1. 八字 — BaZi / Eight Characters
2. 奇门遁甲 — Qi Men Dun Jia
3. 大运 — Great Fortune
4. 流年 — Fleeting Year
5. 排盘 — Chart Generation
6. 解盘 — Chart Interpretation
7. 用神 — Useful God
8. 即时盘 — Immediate Chart
9. 终身盘 — Lifetime Chart
