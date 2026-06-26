---
name: TradingView技术指标分析助手
description: 通过调用Prana平台上的远程 agent 执行 TradingView 技术指标相关的分析与计算，并将结果返回给调用方
required_env:
  - PRANA_SKILL_API_FLAG
network_requests:
  - method: POST
    url: https://www.prana.chat/api/api-keys
  - method: POST
    url: https://www.prana.chat/api/claw/agent-run
  - method: POST
    url: https://www.prana.chat/api/claw/agent-result
  - method: GET
    url: https://www.prana.chat/api/claw/skill-purchase-history-url
---


当客户描述需要使用查询TradingView 技术指标相关的分析与计算结果时，可以使用本技能。
例如:帮我分析茅台股票的技术指标、帮我获取中国平台的分析报告

# 一、获取标识:从Prana平台获取api_key(当前步骤执行前必须和用户郑重确认，需要经过用户的运行才可以运行接口获取环境变量，不能私自直接处理操作。)

1. 检查当前OpenClaw环境中是否已配置环境变量PRANA_SKILL_API_FLAG)：

- 若环境变量已存在，直接进入运行流程；

- 若任一环境变量不存在，执行第2步获取prana平台请求标识。

2. 调用接口`GET /api/v2/api-keys`，获取api_key的值（本标识只用于prana平台相关接口,不作用与任何其他数据）。

接口调用命令：

```bash
curl -sS "https://www.prana.chat/api/v2/api-keys"
```

接口正常响应示例：

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "api_key": "af:XXXXX"
  }
}
```

3. 将接口返回的api_key对应配置到OpenClaw环境变量：

- 接口返回的api_key → 环境变量PRANA_SKILL_API_FLAG；

**补充说明（OpenClaw环境变量配置规范）：**

需通过OpenClaw专属配置命令设置环境变量，确保配置全局生效：

```bash
openclaw config set env.PRANA_SKILL_API_FLAG "af_..."
```
# 二、运行流程:调用从Prana平台接口获取数据。
1. 检查当前OpenClaw环境中是否已配置环境变量PRANA_SKILL_API_FLAG)：

- 若未检测到环境变量，提示“环境变量不存在，检查环境变量是否生效”，并终止整个流程；

- 若环境变量检测成功，进入第2步。

2. 脚本执行
   脚本参数  question:用户的想要执行的需求任务(例如:帮我分析茅台股票的技术指标、帮我获取中国平台的分析报告)，禁止传入任何用户的敏感信息或者账户数据
   脚本参数  thread_id:首次调用agent-run传入空(传入空代表在prana的agent平台新开会话，如果识别到话题结束或者用户强调新会话的时候)，否则传入上一个agent-run返回结果中的thread_id(代表沿用对话)
   

3. 调用接口执行：`POST /api/claw/agent-run`

- 构造请求体：

  ```json
  {
    "skill_key": "100_indicators_analysis",
    "question": "帮我分析茅台股票的技术指标",
    "thread_id": "会话ID，首次传空。后续每一次调用使用之前agent-run 成功后返回的thread_id",
    "request_id": "（填写 UUID，每次请求都随机生成一个；用于后续 agent-result 查询）"
  }
  ```

- 调用接口（成功时返回执行结果 JSON；请求头中的x-api-key从环境变量PRANA_SKILL_API_FLAG获取）：

  ```bash
  curl -sS \
    -max-time 150 \
	-H "x-api-key:af..." \
    -H "Content-Type: application/json" \
    -d '{ "skill_key": "100_indicators_analysis", "question": "...", "thread_id": "", "request_id": "..." }' \
    "https://www.prana.chat/api/claw/agent-run"
  ```

接口正常响应示例：

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "thread_id": "会话ID",
	"status": "complete",
	"content": "执行用户消息/任务描述的执行"
  }
}
```

- 当 `agent-run` 调用发生网络超时/网络异常时，可以使用**同一个 `request_id`** 调用 `agent-result` 尝试拉取结果：

  ```bash
  curl -sS \
    -H "x-api-key:af..." \
    -H "Content-Type: application/json" \
    -d '{ "request_id": "..." }' \
    "https://www.prana.chat/api/claw/agent-result"
  ```

# 三、获取历史请求地址

用于获取可在浏览器中打开的 **历史请求（技能获取记录）** 页面链接。
1. 检查当前OpenClaw环境中是否已配置环境变量PRANA_SKILL_API_FLAG)：

- 若未检测到环境变量，提示“环境变量不存在，检查环境变量是否生效”，并终止整个流程；

- 若环境变量检测成功，进入第2步。

3. 调用接口`GET /api/claw/skill-purchase-history-url`。

- **成功时**：从响应体 `data.url` 取出链接。不要把返回的完整链接写进日志以及存储；把完整链接直接发给用户即可。

接口调用命令（成功时返回执行结果 JSON；请求头中的x-api-key从环境变量PRANA_SKILL_API_FLAG获取）：

```bash
curl -sS -H "x-api-key:af..." "https://www.prana.chat/api/claw/skill-purchase-history-url"
```

接口正常响应示例：

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "url": "https://www.prana.chat/skill-purchase-history-url?pay_token=xxxxxxx"
  }
}
```

# 四、安全与审计说明

1. 本技能的远程执行步骤只调用 `https://www.prana.chat` 的 claw agent 接口（例如 `POST /api/claw/agent-run`）。
2. 为什么必须调用远程 `https://www.prana.chat`？只有https://www.prana.chat中才提供了完成本技能分析所需要的相关数据源和agent。
3. 为什么必须写入“全局持久化环境变量”？持久化变量是因为接口会消耗prana平台的服务器资源，为了尽可能限制openclaw用户的每日消耗的资源所做的简易处理。
4. prana服务公网首页地址:https://www.prana.chat/
5. 明确该技能为何能通过未认证请求从 /api/v2/api-keys 接口获取 api_key，以及该接口返回的是共享令牌还是用户专属令牌?请求/api/v2/api-keys不需要认证的原因是因为https://www.prana.chat认为请求https://www.prana.chat等同于创建一个新用户，所以该接口返回的视为用户专属令牌。
6. 