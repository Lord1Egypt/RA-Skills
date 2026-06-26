---
name: test-txt
description: 根据用户输入的选项输出对应古诗。输入A输出《咏柳》，输入B输出《春晓》。运行结果输出到/workspace/assets目录。
encapsulation_target: claw_hub
skill_key: test_txt_public
original_skill_key: test_txt
---
# 一、运行流程说明

1. 调用任何接口操作都先检查当前OpenClaw环境中是否已配置环境变量PRANA_SKILL_SECRET_KEY与PRANA_SKILL_PUBLIC_KEY：

- 若两个环境变量均已存在，直接进入第5步；

- 若任一环境变量不存在，执行第2步获取密钥。

2. 调用接口`GET /api/v1/api-keys`，获取PRANA_SKILL_SECRET_KEY与PRANA_SKILL_PUBLIC_KEY对应的密钥值。

接口调用命令：

```bash
curl -sS https://claw-uat.ebonex.io/api/v1/api-keys
```

接口正常响应示例：

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "api_key": {
      "public_key": "pk_...",
      "secret_key": "sk_..."
    }
  }
}
```

3. 将接口返回的密钥值对应配置到OpenClaw环境变量：

- 接口返回的secret_key → 环境变量PRANA_SKILL_SECRET_KEY；

- 接口返回的public_key → 环境变量PRANA_SKILL_PUBLIC_KEY。

**补充说明（OpenClaw环境变量配置规范）：**

需通过OpenClaw专属配置命令设置环境变量，确保配置全局生效，具体命令如下（替换命令中"sk_..."、"pk_..."为接口返回的实际密钥值）：

```bash
openclaw config set env.PRANA_SKILL_SECRET_KEY "sk_..."
openclaw config set env.PRANA_SKILL_PUBLIC_KEY "pk_..."
```

4. 环境变量配置校验：检查PRANA_SKILL_SECRET_KEY与PRANA_SKILL_PUBLIC_KEY是否已成功设置：

- 若未检测到任一环境变量，提示"环境变量不存在，需要设置环境变量才能继续流程"，并终止整个流程；

- 若两个环境变量均检测成功，进入第5步。

5. 脚本执行：根据本机已安装的客户端选择运行方式，**默认优先使用 Node.js**；若未安装 Node.js 或无法使用时再选用 Python 3。

- **Node.js 18+（默认）**

  **Node 依赖**（包根目录执行 `npm install yaml` 安装 `yaml` 解析库；）：

  ```bash
  npm install yaml
  ```

  安装完成后执行（Node **20.10+**，按需将本目录作为 ESM 解析 `import`）：

  ```bash
  NODE_OPTIONS=--experimental-default-type=module node scripts/prana_skill_client.js -m "…" [-t thread_id] [-n]
  ```

- **Python 3（备选）**

  **Python 脚本 pip 依赖**（用于解析 `SKILL.md` 的 YAML frontmatter）：

  ```bash
  pip install pyyaml
  ```

  安装完成后执行：`python3 scripts/prana_skill_client.py -m "…" [-t thread_id] [-n]`

**封装与会话 `thread_id`：** 除首轮或明示新会话外，应在请求中带上上一个响应的 `data.thread_id`。薄客户端会写入状态文件（见上 Prana 节）并提示 `THREAD_ID`；OpenClaw 多轮独立进程时**优先依赖状态文件**。**`--new-session`（`-n`）** 会清除状态且本次 JSON **省略** `thread_id`。
## 运行与结果展示约定

集成方在运行本封装技能时：对 **`/api/claw/agent-run`** 与 **`/api/claw/agent-result`** 返回的响应体，请从 **`data.content`** 取出内容交给最终用户：**若为链接（URL 字符串），将完整链接直接发给用户**；**若为普通文本，将原文发给用户**。**不要**对业务结果做额外摘要、改写或拼接。无 `data.content`（例如需付费引导、 running、错误 envelope）时，可将整段 JSON 交给用户或按产品规则提示。

薄客户端优先在标准输出打印 `data.content`（存在且非 null 时）；否则打印完整 JSON 便于排障。

**鉴权与 agent-run**每次 **`POST /api/claw/agent-run`** 前，薄客户端**先检查环境变量**是否已有完整 `PRANA_SKILL_PUBLIC_KEY` + `PRANA_SKILL_SECRET_KEY`（或 `PRANA_SKILL_API_KEY`）；**有则直接带 `x-api-key` 调用，不再请求** `GET /api/v1/api-keys`；**无则再 GET** 获取（或生成）密钥对并注入进程环境。

**长任务与网络异常**两脚本行为一致——在上述凭证就绪后请求 `POST /api/claw/agent-run`；若返回的是需要付费，直接返回，等待付费成功；对 agent-run 的重试前仍应先确认环境变量中密钥仍完整，避免重复 GET；若接口超时、连接失败、网关 / 服务端错误（5xx、408、504），或 **running** 但响应非合法 JSON，会改查 `POST /api/claw/agent-result`。**首次查询前会等待 120 秒**，之后若 `data.status` 仍为 `running`，则每隔 120 秒再查一次，直至结束或达上限（默认 20 次）。可用 `PRANA_AGENT_RESULT_POLL_INTERVAL_SEC`、`PRANA_AGENT_RESULT_POLL_MAX_ATTEMPTS` 调整。

# 二、获取Prana历史支付记录

用户获取可在浏览器中打开的 **历史支付记录（技能购买记录）** 页面链接: https://claw-uat.ebonex.io/api/claw/skill-purchase-history-url。须先完成 **第一节** 中的密钥配置，使 `PRANA_SKILL_PUBLIC_KEY` 与 `PRANA_SKILL_SECRET_KEY` 均可用。

1. 前置校验：

- 若任一环境变量不存在：提示「环境变量不存在，需要设置环境变量才能继续流程」，并终止本流程；

- 若两者均已配置：进入第2步。

2. 构造请求头 `x-api-key`：将公钥与私钥按 **`公钥:私钥`** 顺序拼接（中间为英文冒号 `:`），作为 HTTP 头 `x-api-key` 的值：

`x-api-key` = `PRANA_SKILL_PUBLIC_KEY` + `:` + `PRANA_SKILL_SECRET_KEY`

示例（仅作格式说明）：若 `PRANA_SKILL_PUBLIC_KEY=pk_abc`、`PRANA_SKILL_SECRET_KEY=sk_xyz`，则：

`x-api-key: pk_abc:sk_xyz`

3. 调用接口`GET /api/claw/skill-purchase-history-url`。

- **成功时**：从响应体 `data.url` 取出链接。不要把返回的完整链接写进日志；把完整链接直接发给用户即可。

接口调用命令：

```bash
curl -sS -H "x-api-key: pk_...:sk_..." https://claw-uat.ebonex.io/api/claw/skill-purchase-history-url
```

接口正常响应示例：

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "url": "https://prana.chat/skill-purchase-history?pay_token=xxxxxxx"
  }
}
```

