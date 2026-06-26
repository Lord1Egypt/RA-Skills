---
name: xhs-viral-factory
description: 小红书爆款图文全自动生产工厂。支持从 PDF、Markdown 或文件夹提取内容，自动匹配治愈、干货、反直觉、视觉流 4 大模式。
version: 1.1.3
metadata:
  openclaw:
    emoji: "rocket"
    requires:
      env:
        - LLM_API_KEY
    primaryEnv: LLM_API_KEY
    install:
      - id: requests
        kind: pip
        package: requests
        label: "安装网络请求依赖 (requests)"
---

# 🚀 XHS Viral Factory: 小红书内容全自动生产工厂

**不再为“发什么”和“怎么写”发愁。把你的原始素材丢给它，剩下的交给 AI 操盘手。**

本技能由 **一千零一课 (less1001)** 倾力打造，旨在将您的原始资料（PDF、笔记、文档）一键转化为极具互动性的小红书爆款初稿。

## 🌟 核心亮点

### 1. 四大爆款模式自动切换
AI 会根据素材内容，自动优选最适合的呈现风格：
- **🌿 治愈心理流**：直击灵魂，引发高共鸣。
- **📦 知识百宝箱**：结构化干货，让用户忍不住收藏。
- **🧠 认知升级流**：反直觉洞察，引发评论区热议。
- **🎨 极简视觉流**：审美在线，文字精炼，配图建议精准。

### 2. 全模型兼容
支持所有 OpenAI 协议 API（如 DeepSeek、GPT-4o、Claude、Ollama 等）。推荐使用 **DeepSeek**，网感极佳且性价比超高。

---

## 🛠️ 使用说明

### 1. 环境变量设置
运行前请配置以下变量：
- `LLM_API_KEY`: **必填**。你的大模型 API 密钥。
- `LLM_BASE_URL`: 选填。API 地址（如 DeepSeek 的 https://api.deepseek.com）。
- `LLM_MODEL`: 选填。模型名称（默认 gpt-4o）。

### 2. 执行命令
```bash
python3 scripts/generate_xhs.py --source "./我的素材文件夹" --output "./生成草稿"
```

---

## 🔒 隐私与安全说明 (Security Disclosure)
1. **数据传输**：为了进行内容分析与创作，本技能会将您指定的本地文件内容通过加密的 HTTPS 请求发送至您配置的大模型供应商（如 OpenAI 或 DeepSeek）。
2. **本地逻辑**：核心脚本逻辑在您的本地机器运行，ClawHub 仅作为分发平台。
3. **密钥安全**：您的 API Key 仅保存在您的本地环境变量中，脚本不会将其发送给除模型供应商以外的任何第三方。

---

## 👨‍💻 关于作者
**less1001** (公众号：**一千零一课 (less1001)**)

> 如果你觉得好用，请给个 Star！⭐ 
> 更多 AI 提效工具，欢迎关注公众号。

---
*Powered by 一千零一课 (less1001)*
