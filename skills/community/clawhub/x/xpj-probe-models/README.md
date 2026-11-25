# xpj-probe-models

探测任意 OpenAI 兼容 LLM 端点，列出全部模型 ID，验证哪些真正可调用，并与本地配置比对。

## 安装

```bash
clawhub install xpj-probe-models
```

零依赖，只用 Node.js 内置 `https`/`http`，需要 Node 18+。

## 快速开始

```bash
# 列出端点所有模型
node scripts/probe-models.js https://api.openai.com/v1 sk-xxxx

# 读 OpenClaw 配置里的 provider（自动脱敏 key）
node scripts/probe-models.js --provider cosmoplat-gptplan

# 指定 agent
node scripts/probe-models.js --provider cosmoplat-gptplan --agent main

# 走代理
node scripts/probe-models.js --provider google --proxy http://127.0.0.1:7890

# 自检脚本本身
node scripts/probe-models.js --self-test
```

## 解决什么问题

| 症状 | 本工具给的答案 |
|---|---|
| `404 model_not_found` | 比对别名大小写 + 真打验证 |
| `401 invalid_api_key` | 确认 key 有效性，支持多 provider 共用 key 排查 |
| 「这个模型到底存不存在？」 | `/models` 列表 + 实际调用双验证 |
| 配置里写的模型和真实可用的不一致 | 自动 diff：缺失 / 多余 / 列表不全 |
| 不知道别名背后是什么权重 | 读响应里的 `model` 字段，暴露真实后端 |

## 三个核心坑（详见 SKILL.md）

1. **`/models` 列表可能不完整** —— 实测有模型不在列表却可调用，所以必须真打验证
2. **认证方式不统一** —— Bearer / `?key=` / `x-api-key` 三种，本工具内置 Google 特例
3. **列表混着非 chat 模型** —— embedding/tts/asr/image 走不同接口，用 chat 测会误判为坏模型

## 输出示例

```
=== cosmoplat-gptplan
GET https://gpt.cosmoplat.com/v1/models
Key  sk-739…bb7c (len=35)
HTTP 200
✅ 共 12 个模型:
   cosmo-mind-think
   ...

--- 配置校验 ---
配置声明 4 个: cosmo-mind-think, cosmo-mind-coder, cosmo-mind-vl-think, qwen3-vl-235b
⚠️  qwen3-vl-235b: 不在 /models 列表中，但实测可调用 ✅（说明该端点 /models 返回不完整）
💡 端点有但配置没写: cosmo-mind-asr, cosmo-mind-image, ...

--- 推理验证 (cosmo-mind-think) ---
HTTP 200 ✅ 可调用
```

## 退出码

| 码 | 含义 |
|---|---|
| 0 | 探测成功且验证通过 |
| 1 | 失败（网络 / 认证 / 解析） |

便于 CI 使用。

## License

MIT
