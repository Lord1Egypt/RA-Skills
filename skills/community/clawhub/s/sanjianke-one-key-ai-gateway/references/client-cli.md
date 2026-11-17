# `client.py` 命令行手册

零依赖（只用 Python 标准库）。**不内嵌任何密钥**，只从 `~/.a7w/config.json` 或环境变量 `A7W_API_KEY` 读；只把请求发往 `api.a7w.cn`。

```bash
python3 scripts/client.py <命令> [参数]
```

## 全局参数

| 参数 | 说明 |
|---|---|
| `--key sk-xxx` | 临时覆盖 API Key（优先级最高） |
| `--host https://...` | 覆盖服务地址（默认 `https://api.a7w.cn`，便于指向自建/测试网关） |

优先级：`--key` > `A7W_API_KEY` > `~/.a7w/config.json`。

## 命令一览

| 命令 | 作用 | 对应接口 |
|---|---|---|
| `login --key sk-xxx` | 验证并保存 Key 到本机（权限 600） | 探测应用列表端点 |
| `whoami` | 验证当前 Key，列出可用应用 | 同上 |
| `models [--filter 词]` | 列出可调用模型 | 候选端点探测 |
| `chat --model <名> --prompt "..."` | 调用模型网关 | `POST /api/v1/chat/completions` |
| `openai-env` | 打印 OpenAI SDK 接入参数（base_url / 示例代码） | 无请求 |
| `balance` | 查点数余额（实测可用，返回**裸对象**） | `GET /api/v1/user/balance` |
| `pricing [--filter 词]` | 查**计费规则表**（全局 markup + 少量特例，非逐接口价目表） | `GET /api/v1/pricing` |
| `apps [--brief]` | 列出全部应用 | `GET /api/v1/apps` |
| `schema <app>` | 某应用的接口、参数、必填项与真实价 | `GET /api/v1/apps/{app}` |
| `call <app> <api>` | 调用应用接口（异步自动轮询） | `POST /api/v1/apps/{app}/{api}` |
| `task <task_id>` | 查单个异步任务 | `GET /api/v1/tasks/{task_id}` |
| `tasks` | 列出最近任务（**上游忽略 `page_size`**，翻页用 `--page-no`） | `GET /api/v1/tasks?page_no=&page_size=` |
| `dump --out <文件>` | 导出全部应用 schema 到一个 JSON，便于离线检索 | 遍历应用列表 + 详情 |

## 配置类

```bash
# 首次配置（会用真实接口验证 Key，不是假装成功）
python3 scripts/client.py login --key sk-你的key

# 确认现在用的是哪个 Key、能调哪些应用
python3 scripts/client.py whoami
```

`whoami` 输出的是 `key_prefix`（前 10 位 + 省略号），**不会回显完整 Key**。

## 模型网关

```bash
# 列出全部模型 / 按关键词过滤
python3 scripts/client.py models
python3 scripts/client.py models --filter qwen

# 一次性对话
python3 scripts/client.py chat --model DeepSeek-V4-Flash --prompt "你好"
python3 scripts/client.py chat --model DeepSeek-V4-Flash \
    --system "你只输出 JSON" --prompt "给 3 个字段名" \
    --max-tokens 256 --temperature 0.2

# 流式（直接打印文本增量，便于管道处理）
python3 scripts/client.py chat --model DeepSeek-V4-Flash --prompt "讲个笑话" --stream

# 拿到 OpenAI SDK 的接法
python3 scripts/client.py openai-env
```

| 子参数 | 说明 |
|---|---|
| `--model` | **必填**。模型名用 `models` 查，不要猜 |
| `--prompt` / `--system` | 用户消息 / system 消息 |
| `--max-tokens` | 最大生成 tokens（控成本主旋钮） |
| `--temperature` | 采样温度 |
| `--stream` | 流式输出，直接打印文本 |
| `--timeout` | 请求超时秒数 |

> ⚠️ **实测：`--max-tokens` 太小会让 `content` 变成 `null`。** 推理模型会先把 token 花在思维链上：`max_tokens=8` 时返回 `content: null` + `finish_reason: "length"`；调到 200 才正常返回正文。
> 客户端的 `chat` 已把思维链单列为 `reasoning` 字段，并在「正文为空且 `length`」时给出 `hint`。注意思维链字段名在不同线路上分别是 `reasoning` 和 `reasoning_content`，客户端两个都取。

## 应用任务

```bash
# 看清单（--brief 只要代码与名称）
python3 scripts/client.py apps --brief

# 看某应用的接口、参数、必填与真实价
python3 scripts/client.py schema voice_tts

# 提交（同步接口直接返回结果，异步接口自动轮询到终态）
python3 scripts/client.py call voice_tts tts --param text="你好世界"

# 只提交不等结果
python3 scripts/client.py call voice_tts tts_async --json-file body.json --no-wait

# 查任务
python3 scripts/client.py task tsk_xxxxxxxx
python3 scripts/client.py tasks --page-size 50
```

### 三种传参方式（只能选一种）

| 方式 | 用法 | 什么时候用 |
|---|---|---|
| `--param k=v` | `--param text=你好 --param n=3` | 参数少、扁平。值按 JSON 解析（`n=3` → 数字） |
| `--json-file f.json` | `--json-file body.json` | **复杂/嵌套参数首选**，最稳 |
| `--json '{...}'` | `--json '{"text":"你好"}'` | 临时用；**PowerShell/CMD 会吃掉内部双引号** |

> 在 Windows 上遇到 `JSON 解析失败` 基本都是第三种方式导致的。换 `--json-file` 立刻好。
> 也支持 `--json -` 从标准输入读。

### 轮询控制

| 子参数 | 默认 | 说明 |
|---|---|---|
| `--no-wait` | 关 | 提交后立刻返回 `task_id` |
| `--interval` | 6 秒 | 轮询间隔 |
| `--timeout` | 1800 秒 | 轮询上限；超时**不代表任务失败** |

## 退出码

写脚本时按退出码分支，比解析文本可靠：

| 码 | 含义 | 怎么办 |
|---|---|---|
| `0` | 成功 | — |
| `2` | 用法/配置错误（缺 Key、传参方式冲突、JSON 非法） | 看 stderr 提示 |
| `3` | 网络错误（到不了 `api.a7w.cn`） | 查内网/代理/防火墙 |
| `4` | HTTP/业务错误（401、403、404、400…） | 看 stderr 的「含义 → 下一步」 |
| `5` | 点数不足（402） | 先分清账号没钱还是 Key 额度满 |
| `6` | 异步任务终态为失败 | 看返回里的 `error` |
| `7` | 轮询超时 | 用 `task <task_id>` 继续查，**别急着重提** |

## 输出约定

- **stdout**：纯 JSON（`ensure_ascii=False`，可直接管道给 Agent 或其他程序）
- **stderr**：人类可读的进度与错误解释
- 流式模式下 `chat --stream` 的正文直接走 stdout，完成信息走 stderr

所以这样用是安全的：

```bash
python3 scripts/client.py models > models.json
python3 scripts/client.py call voice_tts tts --param text="你好" > result.json
```

## 设计取舍（为什么有些命令会「试探」）

`models` / `balance` / `apps` 会**按候选端点顺序探测**，而不是硬编一个地址。原因：官方文档给出的路径与实测可用路径未必一致，且不同账号开放情况可能不同。

因此这些命令的返回里带 `endpoint`（实际通了哪个）和 `attempts`（每个候选的真实 HTTP 状态）——**失败时你能看到是路径不对、还是账号没开、还是网络不通**，而不是一句「失败了」。

探测的判定标准是「HTTP 200 **且** 不是业务错误信封」，并且**允许裸对象**：因为 `balance`、`pricing` 这两个端点直接返回 `{...}`，没有 `code/msg/data` 外壳，用「有没有 data 字段」判断会把它们误判为不可用。

## 实测核验记录

以下命令已在**真实网络 + 真实 Key** 下端到端跑通（2026-09-24）：

| 命令 | 结果 |
|---|---|
| `whoami` | 退出码 0，识别出 **21 个应用** |
| `models --filter image` | 退出码 0，从 75 个模型中筛出 10 个 |
| `apps --brief` | 退出码 0，21 条 |
| `schema voice_tts` | 退出码 0，6 个接口含 `code`/`method`/`call_type`/参数/价格 |
| `schema flashvsr` | 退出码 0，2 个接口 |
| `balance` | 退出码 0，`points` 正常取值（裸对象端点） |
| `pricing` | 退出码 0，返回 6 条规则 |
| `tasks --page-size 2` | 退出码 0，实际返回 20 条（上游忽略 `page_size`） |
| `openai-env` | 退出码 0 |
| `call voice_tts __不存在的接口__` | 退出码 **4**，正确识别 `code:0` 业务错误 |
| `chat --model DeepSeek-V4-Flash` | 退出码 0，`max_tokens=200` 时返回 `content:"ok"` |

> 唯一**未**做端到端验证的是 `call` 的**成功路径**——它会真实创建计费任务（异步任务提交即冻结）。错误路径已验证。
