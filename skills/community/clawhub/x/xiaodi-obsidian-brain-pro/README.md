# 🧠 Obsidian-Brain-Pro (v1.1.3)

> **拒绝 AI "爹味"润色，记录最真实的生命痕迹。**

---

## 📖 开发者背后的故事

这是一个从电力工地一线、高速公路驾驶座、以及北影管理学院考研笔记中"长"出来的工具。

我是一名在电力行业奔波的极客，也是一名考研党。我发现市面上所有的 AI 笔记工具都有个通病：**喜欢自作聪明**。

我说"颈椎疼，有点烦"，它非要给我整理成"身体健康管理建议"。

我说"思绪混乱"，它非要给我修饰成"逻辑严密的复盘"。

**不，那不是我的生命。** 我的生命是碎片化的、是有情绪的、是有错别字的。

所以我写了 Obsidian-Brain-Pro，配合 OpenClaw，让 AI 闭嘴，让记忆说话。

---

## 🎯 一张图说明问题

![AI 处理对比](comparison.png)

**左边**：Obsidian-Brain-Pro 保持你的原话，只加格式。

**右边**：普通 AI 笔记自作聪明，篡改你的语气。

---

## ✨ 核心黑科技

### 🛡️ 1. "反幻觉"装甲 (v2.0 Prompt)

内置严苛红线规则。AI 只能帮你改错别字、加标题和时间戳，**严禁修改你的语气、美化你的情绪、重构你的逻辑**。

### 🚗 2. 语音输入"纠偏仪"

针对开车、工地等语音转文字场景优化：
- Open Crow → OpenClaw
- 导课 → Docker
- 码云 → Git

即便你在风口浪尖说话，小弟也能听懂你的术语。

### 🔒 3. 隐私脱敏盾牌

自动拦截 API_KEY、Password 等敏感信息，放心推送到 GitHub 私人/公开仓库而不泄密。

### 🔍 4. 本地语义索引 (Powered by Ollama)

无需联网。问它"我最近在焦虑什么？"，它能跨越日期精准提取关联笔记。

---

## 📦 快速开始

### 1. 安装 (OpenClaw 环境)

```bash
npx clawhub@latest install xiaodi-obsidian-brain-pro
```

### 2. 配置路径 ⚠️ 必须修改！

打开 `_meta.json`，修改 `obsidian_path` 为你的真实路径：

```json
"config": {
  "obsidian_path": "~/Obsidian/Daily Notes"  // ❌ 默认值，需修改！
}
```

**不同环境示例**：

| 环境 | 路径示例 |
|------|----------|
| 群晖 NAS | `/volume1/homes/你的用户名/Obsidian/Daily Notes` |
| Linux VPS | `/home/你的用户名/Obsidian/Daily Notes` |
| macOS | `/Users/你的用户名/Obsidian/Daily Notes` |

**注意**：`~` 在容器内会解析成 `/home/node`，不是你的真实用户目录！

### 3. 开始对话

在 WhatsApp 或 Telegram 发送任何碎碎念，小弟会立刻为你封存记忆。

---

## 🤝 商业合作与咨询

如果你也想在 **群晖 NAS** 上部署这套"数字大脑"，或需要电力/能源行业的定制化 AI 方案，欢迎通过 GitHub Issue 或私信联系。

---

## 📜 License

MIT-0 License

---

> **用户说的每一句话都是证据，AI 只能整理格式，不能篡改证据。**