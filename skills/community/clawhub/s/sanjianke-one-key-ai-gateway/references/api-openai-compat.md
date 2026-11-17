# 模型网关：OpenAI 兼容层

## 1. 端点与鉴权

```
Base URL : https://api.a7w.cn/api/v1
Chat     : POST https://api.a7w.cn/api/v1/chat/completions
Header   : Authorization: Bearer <你的 API Key>
           Content-Type: application/json
```

**与 OpenAI 官方接口的差别只有 base_url 和 model 名。** 换模型不需要换 Key、不需要重新签名、不需要重新对账。

## 2. 最小请求

```bash
curl https://api.a7w.cn/api/v1/chat/completions \
  -H "Authorization: Bearer $A7W_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "DeepSeek-V4-Flash",
    "messages": [{"role": "user", "content": "你好"}]
  }'
```

用本 Skill 的客户端（免去 shell 引号问题）：

```bash
python3 scripts/client.py chat --model DeepSeek-V4-Flash --prompt "你好"
python3 scripts/client.py chat --model DeepSeek-V4-Flash \
    --system "你是一个只输出 JSON 的助手" --prompt "给我 3 个字段名"
```

## 3. 模型发现（**先查再猜**）

模型名**不要猜**，也不要抄别人的。上下架很频繁——站内宣传 87+、宣传页写 89+，而**实测 `GET /api/v1/models` 返回 75 个**，这些数字都会变。

```bash
python3 scripts/client.py models                      # 全部
python3 scripts/client.py models --filter deepseek    # 按关键词
python3 scripts/client.py models --filter video
```

`models` 会**按候选顺序探测**端点，并在结果里告诉你 `endpoint` 实际用的是哪个：

```json
{ "ok": true, "endpoint": "/api/v1/models", "count": 88, "models": ["..."] }
```

候选顺序（文档口径与实测口径未必一致，所以按序试）：

1. `/api/v1/models` —— OpenAI 风格的通用路径。**实测可用**，返回 75 个模型，字段含 `model_code`、`model_name`、`call_type_desc`、`vendor_name`、`supports_vision`、`supports_reasoning`
2. `/api/user_center/modelList?page_no=1` —— 官方开发文档给出的模型列表路径。**实测也可用**，但**耗时约 39 秒**（比 `/api/v1/models` 慢一个数量级），非必要不用

若两个都不通，返回里会列出每个候选的实际 HTTP 状态，便于判断是「路径不对」还是「这个账号没开」。

## 4. Python SDK 接入

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://api.a7w.cn/api/v1",
    api_key="sk-你的key",
)

resp = client.chat.completions.create(
    model="DeepSeek-V4-Flash",
    messages=[{"role": "user", "content": "你好"}],
)
print(resp.choices[0].message.content)
```

流式：

```python
stream = client.chat.completions.create(
    model="DeepSeek-V4-Flash",
    messages=[{"role": "user", "content": "写一段 200 字的产品介绍"}],
    stream=True,
)
for chunk in stream:
    delta = chunk.choices[0].delta.content or ""
    print(delta, end="", flush=True)
```

## 5. Node SDK 接入

```javascript
import OpenAI from "openai";

const client = new OpenAI({
  baseURL: "https://api.a7w.cn/api/v1",
  apiKey: process.env.A7W_API_KEY,
});

const r = await client.chat.completions.create({
  model: "DeepSeek-V4-Flash",
  messages: [{ role: "user", content: "你好" }],
});
console.log(r.choices[0].message.content);
```

不想手抄这几段就让它打印出来：

```bash
python3 scripts/client.py openai-env
```

## 6. 常用参数

| 参数 | 类型 | 说明 |
|---|---|---|
| `model` | string | **必填**。以 `models` 的结果为准 |
| `messages` | array | **必填**。`[{role, content}]`，role 取 `system` / `user` / `assistant` |
| `temperature` | number | 采样温度，越高越发散 |
| `max_tokens` | integer | 最大生成 tokens，**同时是控成本的主要旋钮** |
| `stream` | boolean | 流式返回（SSE） |
| `top_p` | number | 核采样 |

CLI 对应：

```bash
python3 scripts/client.py chat --model <名> --prompt "..." \
    --max-tokens 512 --temperature 0.3
```

## 7. 流式（SSE）

`stream: true` 时返回 `text/event-stream`，逐行 `data: {...}`，以 `data: [DONE]` 结束。取增量文本的路径是 `choices[0].delta.content`（注意**不是** `message.content`）。

```bash
python3 scripts/client.py chat --model DeepSeek-V4-Flash --prompt "讲个笑话" --stream
```

流式模式下客户端**直接打印文本**（便于管道处理），不进 JSON 包装；是否输出完成的信息走 stderr。

## 8. 响应结构

非流式响应与 OpenAI 一致：

```json
{
  "id": "chatcmpl-xxx",
  "model": "DeepSeek-V4-Flash",
  "choices": [
    { "index": 0,
      "message": { "role": "assistant", "content": "..." },
      "finish_reason": "stop" }
  ],
  "usage": { "prompt_tokens": 12, "completion_tokens": 34, "total_tokens": 46 }
}
```

客户端会把 `content`、`finish_reason`、`usage` 提到顶层，同时保留完整 `raw`：

```json
{ "ok": true, "model": "...", "content": "...", "finish_reason": "stop",
  "usage": { "total_tokens": 46 }, "raw": { } }
```

如果网关在 OpenAI 结构外又包了一层 `{code,msg,data}`，客户端会自动拆包后再找 `choices`；两者都认不出来时，会把原始响应放进 `raw` 返回给你，不会静默丢数据。

## 9. 推理模型的坑（实测）

部分模型（如 `DeepSeek-V4-Flash`）是**推理模型**：会先花 token 产出思维链，再给正文。

实测两种情况：

| `max_tokens` | 结果 |
|---|---|
| `8` | `content` 为 **`null`**，`finish_reason: "length"`（token 全被 reasoning 吃掉） |
| `200` | `content: "ok"`，`finish_reason: "stop"`，`usage.completion_tokens_details.reasoning_tokens = 16` |

所以：

- **`content` 可能是 `null`**，代码里必须容错，不要假定它是字符串。
- 看到 `finish_reason: "length"` 且正文为空，**先把 `max_tokens` 调大**，不是接口坏了。
- 思维链字段名**在不同线路上不一致**——实测分别出现过 `message.reasoning` 和 `message.reasoning_content`，两个都取一下。客户端的 `chat` 会把思维链输出为 `reasoning` 字段，并在正文为空且 `length` 时给出 `hint`。

另外两点实测细节：

- **模型名会被规范化**：请求 `DeepSeek-V4-Flash`，响应 `model` 返回 `deepseek-v4-flash`（小写）。别拿响应的 `model` 去做精确匹配。
- **模型清单的字段是 `model_code` / `model_name`**（不是 `model`）。实测 75 个模型，`call_type_desc` 只有「同步 / 异步」两类。

## 10. 与「应用任务」的边界

| | 模型网关 | 应用任务 |
|---|---|---|
| 路径 | `/api/v1/chat/completions` | `/api/v1/apps/{app}/{api}` |
| 入参 | `messages` 数组 | 业务参数（`text` / `image_url` …） |
| 返回 | `choices` 同步返回 | 多为 `task_id` 异步 |
| 典型用途 | 对话、写作、分类、抽取、代码 | 出图、出视频、配音、数字人、音乐 |

**别拿 `messages` 去调应用**，也别指望模型网关返回 `task_id`。选错入口的报错通常是 400 `invalid_request` 或 404 `not_found`。

## 11. 计费与排错

- 文本生成按**点数 / 百万 tokens** 计，**输出分档**。控成本先压 `max_tokens`。
- 预算一律按**实收价**（`tenant_*`）算，别按公示标准价——两者可能差很多。详见 `api-billing-errors.md`。
- 报 402 先分清是账号没钱（`insufficient_points`）还是 Key 额度满（`key_quota_exceeded`）。
- 报 403 `permission_denied` 说明这个 Key 没有该模型的权限，跟余额无关。
