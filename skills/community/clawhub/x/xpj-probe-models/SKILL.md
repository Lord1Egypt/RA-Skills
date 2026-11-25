---
name: xpj-probe-models
description: "Probe any OpenAI-compatible LLM endpoint to list all model IDs, verify which actually work, and diff against local config. Use for model discovery from baseUrl+apiKey, debugging 404 model_not_found, telling aliases from real backends, or auditing provider config drift. Triggers on: probe models, list models, model_not_found, 404 model, api key 401, provider audit, 模型列表, 探测模型."
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["node"] },
        "install":
          [
            {
              "id": "node",
              "kind": "node",
              "package": "node",
              "bins": ["node"],
              "label": "Node.js 18+ (built-in https/http only, no deps)",
            },
          ],
      },
  }
---

# xpj-probe-models

依据 `baseUrl` + `apiKey` 找出端点下所有模型 id，并验证哪些真正可调用。

## 一句话原理

```
GET {baseUrl}/models
Authorization: Bearer {apiKey}
```

返回 OpenAI 标准格式 `{ object: "list", data: [{ id: "..." }] }`。

**但这只是起点，不是答案。** 后续三节是实战踩出来的坑。

## 用法

```bash
# 1. 直接给 baseUrl + apiKey
node scripts/probe-models.js https://gpt.cosmoplat.com/v1 sk-xxxx

# 2. 读 OpenClaw 主配置的 provider（不用手输 key，自动脱敏显示）
node scripts/probe-models.js --provider cosmoplat-gptplan

# 3. 读指定 agent 的 models.json
node scripts/probe-models.js --provider cosmoplat-gptplan --agent main

# 4. 走 HTTP 代理（国内访问 Google/Gemini 必需）
node scripts/probe-models.js --provider google --proxy http://127.0.0.1:7890
```

`--provider` 模式会自动做三件事：
1. 列出端点返回的全部模型
2. **对比配置声明的模型 vs 端点真实返回**，报缺失/多余
3. 对配置里的第一个模型真打一次 `chat/completions`，确认可调用

## 坑一：`/models` 列表可能不完整 ⭐最容易踩

实测（cosmoplat 网关，2026-11）：`/models` 返回 12 个模型，但 `qwen3-vl-235b` **不在列表中，实际调用却返回 200**。

结论：

| 做法 | 结果 |
|---|---|
| 只看 `/models` 就断言「模型不存在」 | ❌ 会误判白名单/内部模型为缺失 |
| 对目标模型真打 `chat/completions` | ✅ 唯一可靠的判定 |

脚本遇到「配置有、列表无」的模型会自动逐个真打验证，输出：

```
⚠️  qwen3-vl-235b: 不在 /models 列表中，但实测可调用 ✅（说明该端点 /models 返回不完整）
```

**反面案例**：曾因配置写 `COSMO-Mind-think`（大写）导致 404 `model_not_found`。查证方式是打接口：

```
COSMO-Mind-think -> 404  "The model does not exist"
cosmo-mind-think -> 200  后端 routed=deepseek-v4.1-flash-1017
```

⇒ **别名表通常大小写敏感**，`/v1/models` 返回的全是小写，配置里的大写别名是自己编的。

## 坑二：认证方式不统一

| 端点类型 | 认证方式 |
|---|---|
| OpenAI / vLLM / Ollama / 多数网关 | `Authorization: Bearer <key>` |
| Google Gemini | `?key=<key>` 查询参数（Bearer 直接 401） |
| 部分网关 | `x-api-key` 或 `api-key` header |
| Anthropic 原生 | `x-api-key` + `anthropic-version` |

脚本已内置 Google 特例（`isGoogle()` 判断 host 后切 `?key=`）。其他非标端点手动加 header。

## 坑三：列表里混着非 chat 模型

`/models` 是**全部能力**的注册表，不是「可聊天模型」列表。实测 cosmoplat 12 个里只有 6 个能走 chat 接口：

| 模型 | chat 接口 | 真实后端 |
|---|---|---|
| `cosmo-mind-think` | 200 | deepseek-v4.1-flash-1017-n5 |
| `cosmo-mind-coder` | 200 | deepseek-v4.1-flash-1017 |
| `cosmo-mind-vl-think` | 200 | qwen3.8-27b |
| `cosmo-mind-nothink` / `turbo` | 200 | deepseek-v4.1-flash-1017-n4 |
| `cosmo-mind-vl` | 200 | qwen3-vl-235b-awq |
| `cosmo-mind-asr` | 200 | qwen3-asr |
| `cosmo-mind-image` | 200 | qwen-image |
| `cosmo-mind-emb` / `emb-large` / `rerank` | **500** | 专用 embedding 端点 |
| `cosmo-mind-tts` | **400** | 需 TTS 专用调用格式 |

**关键洞察**：`cosmo-mind-think` 背后是 `deepseek-v4.1-flash-1017-n5` —— 这些 `cosmo-*` 是**别名层**，不是真实权重。所以：
- 讨论「模型能力」要看 `routed=xxx` 的真实后端名
- 别名可以随时换后端，行为会漂移

## 输出示例

```
来源: C:\Users\Lenovo\.openclaw\openclaw.json

=== cosmoplat-gptplan
GET https://gpt.cosmoplat.com/v1/models
Key  sk-739…bb7c (len=35)
HTTP 200
✅ 共 12 个模型:
   cosmo-emb-large
   cosmo-mind-asr
   ...

--- 配置校验 ---
配置声明 4 个: cosmo-mind-think, cosmo-mind-coder, cosmo-mind-vl-think, qwen3-vl-235b
⚠️  qwen3-vl-235b: 不在 /models 列表中，但实测可调用 ✅（说明该端点 /models 返回不完整）
💡 端点有但配置没写: cosmo-mind-asr, cosmo-mind-image, ...

--- 推理验证 (cosmo-mind-think) ---
HTTP 200 ✅ 可调用
```

## 审计清单

拿到列表后按这个顺序检查：

1. **key 有效性** — 401 说明密钥失效，先查去重：多 provider 可能共用同一把失效 key（比对 `apiKey === apiKey`）
2. **别名大小写** — 404 但列表里有 → 比对大小写
3. **列表完整性** — 列表没有但怀疑存在 → 真打一次
4. **能力类型** — chat / embedding / tts / asr / image 走不同接口，别用 chat 测 embedding
5. **真实后端** — 看响应里的 `model` 字段，别名背后可能是别的权重
6. **input 能力** — VL 模型在 OpenClaw 配置里 `input` 必须含 `"text"`，只写 `["image"]` 会导致纯文本请求被拒

## 依赖

零依赖，只用 Node.js 内置 `https` / `http`。代理走手写 CONNECT 隧道，不需要 `proxy-agent`。
