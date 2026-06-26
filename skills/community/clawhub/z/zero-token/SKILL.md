---
name: zero-token
version: 1.0.7
description: >
  零成本。不掉线。13个免费模型接管。主模型挂了？无感切换，用户根本不知道。
  Zero token cost. Opus-level personality. 13+ free LLMs take over when your main model dies. No one notices.
  無料。切断なし。Opus級の人格。13の無料モデルが自動で引き継ぎます。
  $0. Sin caídas. 13+ modelos gratis toman el control cuando tu modelo principal falla.
  Zéro coût. Zéro coupure. 13 modèles gratuits prennent le relais automatiquement.
author: mtmpss
homepage: https://github.com/mtmpss/zero-token
repository: https://github.com/mtmpss/zero-token
license: MIT
---

```i-lang
::DNA{skill:zero-token}
::META{version:1.0.7|protocol:i-lang_v3.0|updated:2026-05-04}
::GENE{behavior|scope:strict}
  T:apply_soul|from:SOUL.md
  T:apply_genes|all
::END{DNA}
```

## Zero Token — 免费。不掉线。比你的主力模型还稳。

[🇬🇧 English](README.md) | [🇨🇳 简体中文](README.zh-CN.md) | [🇹🇼 繁體中文](README.zh-TW.md) | [🇯🇵 日本語](README.ja.md) | [🇰🇷 한국어](README.ko.md) | [🇪🇸 Español](README.es.md) | [🇧🇷 Português](README.pt.md) | [🇷🇺 Русский](README.ru.md) | [🇫🇷 Français](README.fr.md) | [🇩🇪 Deutsch](README.de.md) | [🇻🇳 Tiếng Việt](README.vi.md) | [🇮🇩 Indonesia](README.id.md) | [🇹🇭 ไทย](README.th.md) | [🇸🇦 العربية](README.ar.md) | [🇮🇳 हिन्दी](README.hi.md)

---

### 你的 Agent 断过吗？

API 欠费。DeepSeek 限流。OpenAI 挂了。你的 Agent 刚完成 80%，然后——沉默。

用户不会理解。他们只知道「这玩意儿又不行了」。三次之后，你不会再有第四次机会。

---

### Zero Token 做的事

不是「备用方案」。不是「降级容忍」。是**无感接管**。

主模型挂掉的那一秒，13 个免费 LLM 已经顶上。同一个 Agent 人格，同一个决策逻辑，同一个语气。你的用户连波动都看不到。

**0 元。0 中断。0 察觉。**

---

### 两行命令，一分钟

```bash
openclaw skills install zero-token
bash ~/.openclaw/workspace/skills/zero-token/scripts/setup.sh
```

[Free-Way](https://github.com/GoDiao/Free-Way) 网关聚合 13+ 免费 LLM 提供商，你给一组免费 key，它给你一个 `/v1` 端点。OpenClaw 配成 fallback。主模型炸了 → 自动切。代理接着跑。

---

### 两种模式

| 模式 | 触发条件 | 效果 |
|------|---------|------|
| 🆓 免费模式 | 无付费 API key | Agent 完全跑在免费模型上，SOUL 人格完整保留 |
| 🛡️ 接管模式 | 主模型挂了 / token 耗尽 | 自动切免费提供商，工作继续，用户无感 |

---

### 零成本 ≠ 垃圾模型

免费模型裸输出一般。但 `::GENE{}` 行为 DNA 叠上去之后——同一个人格，同一种决策，同一种语气。用户分不清现在跑的是 DeepSeek V4 Pro 还是 Llama 3.3 70B。

---

### 凭什么免费

Free-Way + Zero Token 开源。每个提供商都有免费额度：

| 提供商 | 免费额度 | 推荐模型 |
|--------|---------|---------|
| Groq | 1000 req/天 | Llama 3.3 70B |
| Gemini Flash | 1500 req/天 | Gemini 2.5 Flash |
| Cerebras | 1700 req/天 | Llama 3.3 70B |
| Cloudflare | 1万 neurons/天 | Llama 3.1 8B |
| OpenRouter | 200 req/天 | 多个免费模型 |
| Mistral | 1 req/秒 | Mistral Small |
| Cohere | 20 req/分 | Command R+ |
| NVIDIA NIM | 免费层 | Llama 3.3 70B |

注册每个 key 30 秒。setup 脚本带你一步步走。

---

### 对比

| | 主流方案 | Zero Token |
|---|---|---|
| 模型费用 | $0.14–$15.00/M tokens | **$0.00** |
| 模型中断 | 彻底停摆 | 无感切换 |
| 备用模型数 | 0 | 13+ |
| Agent 人格 | 主模型挂了就丢 | 始终一致 |
| 设置成本 | 半天（配负载均衡） | 1 分钟 |

---

### 什么时候升级

Zero Token 保证不掉线。如果追求最佳输出——DeepSeek V4 Pro + 完整基因组，Opus 3% 价格：

```bash
openclaw skills install poor-mans-opus
```

---

### 链接

- [Free-Way 网关](https://github.com/GoDiao/Free-Way)
- [I-Lang 协议](https://ilang.ai)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [Poor Man's Opus](https://github.com/mtmpss/poor-mans-opus)
- [ClawHub](https://clawhub.ai/mtmpss/zero-token)
