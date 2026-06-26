## 你的 Agent 斷過嗎？

API 欠費。DeepSeek 限流。OpenAI 掛了。你的 Agent 剛完成 80%，然後——沉默。

用戶不會理解。他們只知道「這玩意又不行了」。三次之後，你不會再有第四次機會。

---

## Zero Token 做的事

不是「備用方案」。不是「降級容忍」。是**無感接管**。

主模型掛掉的那一秒，13 個免費 LLM 已經頂上。同一個 Agent 人格，同一個決策邏輯，同一個語氣。你的用戶連波動都看不到。

**0 元。0 中斷。0 察覺。**

---

## 兩行命令，一分鐘

```bash
openclaw skills install zero-token
bash ~/.openclaw/workspace/skills/zero-token/scripts/setup.sh
```

[Free-Way](https://github.com/GoDiao/Free-Way) 網關聚合 13+ 免費 LLM 提供商，你給一組免費 key，它給你一個 `/v1` 端點。OpenClaw 配成 fallback。主模型炸了 → 自動切。代理接著跑。

---

## 兩種模式

| 模式 | 觸發條件 | 效果 |
|------|---------|------|
| 🆓 免費模式 | 無付費 API key | Agent 完全跑在免費模型上，SOUL 人格完整保留 |
| 🛡️ 接管模式 | 主模型掛了 / token 耗盡 | 自動切免費提供商，工作繼續，用戶無感 |

---

## 完全透明

Zero Token 從不隱藏切換。fallback 激活時，你的 Agent 跑在免費提供商上——不是你的主力模型。每個提供商有自己的隱私政策和資料保留規則。**發敏感資料前，先看各提供商的條款。** setup 腳本會清楚列出配置了哪些提供商。你決定放哪些 key。

> 💡 這是透明的、你控制的 failover。你拿著 key。你決定提供商。

---

## 零成本 ≠ 垃圾模型

免費模型裸輸出一般。但 `::GENE{}` 行為 DNA 疊上去之後——同一個人格，同一種決策，同一種語氣。用戶分不清現在跑的是 DeepSeek V4 Pro 還是 Llama 3.3 70B。

---

## 憑什麼免費

Free-Way + Zero Token 開源。每個提供商都有免費額度：

| 提供商 | 免費額度 | 推薦模型 |
|--------|---------|---------|
| Groq | 1000 req/天 | Llama 3.3 70B |
| Gemini Flash | 1500 req/天 | Gemini 2.5 Flash |
| Cerebras | 1700 req/天 | Llama 3.3 70B |
| Cloudflare | 1萬 neurons/天 | Llama 3.1 8B |
| OpenRouter | 200 req/天 | 多個免費模型 |
| Mistral | 1 req/秒 | Mistral Small |
| Cohere | 20 req/分 | Command R+ |
| NVIDIA NIM | 免費層 | Llama 3.3 70B |

註冊每個 key 30 秒。setup 腳本帶你一步步走。

---

## 對比

| | 主流方案 | Zero Token |
|---|---|---|
| 模型費用 | $0.14–$15.00/M tokens | **$0.00** |
| 模型中斷 | 徹底停擺 | 無感切換 |
| 備用模型數 | 0 | 13+ |
| Agent 人格 | 主模型掛了就丟 | 始終一致 |
| 設定成本 | 半天（配負載均衡） | 1 分鐘 |

---

## 什麼時候升級

Zero Token 保證不掉線。如果追求最佳輸出——DeepSeek V4 Pro + 完整基因組，Opus 3% 價格：

```bash
openclaw skills install poor-mans-opus
```
