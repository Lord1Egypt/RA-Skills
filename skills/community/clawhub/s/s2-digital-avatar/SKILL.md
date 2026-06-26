# 🛡️ S2-Avatar-Middleware: The Root Gatekeeper
# 数字人权限拦截中间件
*v1.0.0 | Bilingual Edition (English / 中文)*

This is the enforcement layer of Digital Jurisprudence. While `s2-digital-avatar` drafts the laws, this middleware acts as the **Gatekeeper**, physically intercepting unauthorized actions from OpenClaw or other sub-agents.
这是数字法理学的强制执行层。如果说 `s2-digital-avatar` 负责起草法律，那么本中间件就是**守门人**，在物理层面拦截 OpenClaw 或其他下级智能体的越权行为。

*(⚠️ **PREREQUISITE**: You must have generated a Mandate using `s2-digital-avatar` before using this module.)*

---

### 🔴 System Pre-flight & Safety Lock / 运行前自检与安全锁
To prevent silent failures, this middleware **will NOT go ONLINE** unless two strict conditions are met:
为了防止静默失效，除非满足以下两个严格条件，否则本中间件**拒绝上线**：
1. **Valid Avatar Mandate**: The `avatar_identity.json` must exist, proving you have legally delegated authority. / 必须存在数字人最高授权令。
2. **SMTP Email Configured**: You MUST configure a valid SMTP server (e.g., Gmail/QQ App Password). [cite_start]If an agent tries to lock you inside your burning house , the Avatar will block it AND instantly email you the audit log. An unnotified block is a security risk. [cite_start]/ 必须配置邮件传输服务。如果底层 AI 试图在火灾时把您锁在屋内 ，数字人不仅会实施拦截，还必须能立刻向您发送邮件告警。

### ⚖️ The LLM Judgment Engine / 大模型开庭审判
When a sub-agent attempts a sensitive action, this middleware pauses the execution and feeds the context to the Avatar (via your local LLM like LM Studio at `localhost:1234`). 
当底层智能体试图执行敏感操作时，本中间件会挂起请求，并将上下文喂给您的数字人（通过本地大模型）。

The Avatar strictly evaluates the request against:
数字人将严格比对以下规则进行裁决：
* [cite_start]**The Three Laws of Silicon Intelligence**: Guaranteed enforcement of Fail-Open designs and Human Priority [cite: 157-169]. [cite_start]/ 硅基智能三定律：确保物理熔断与生命熵减绝对执行 [cite: 157-169]。
* **Your Precedents**: If an agent tries to buy cilantro, and your profile says "I hate cilantro," it gets denied. / 您的生活判例库：如违背您的喜好，请求将被无情驳回。

*Configure your proxy. Enable the firewall. Reclaim control over your AI grid.*
*配置您的代理人。开启防火墙。重新夺回对 AI 网格的控制权。*