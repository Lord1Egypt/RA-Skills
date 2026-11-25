# StepOneAI GEO Check (`stepone-geo-check`)

> **Zero-dependency, zero-LLM-cost open-source GEO & AI Search Readiness Auditor.**
> 免费开源的「官网 AI 搜索体检」工具——纯代码 3~5 秒真实探测任意官网在 **豆包、DeepSeek、通义千问、腾讯元宝、ChatGPT、Claude、Perplexity、Bing、Google** 中的 AI 可读性与引用友好度。

🌐 **在线可视化雷达图版（免费体验）**：[https://www.steponeai.com/geo-check](https://www.steponeai.com/geo-check)
🏛️ **由 [基智 GEO · 北京基智科技有限公司 (StepOneAI)](https://www.steponeai.com/) 开源维护**（A 股上市公司彩讯股份 `300634.SZ` 旗下全资企业）

---

## ✨ 为什么需要 GEO Check？

传统 SEO 排第一的官网，在豆包、DeepSeek、ChatGPT 里往往完全不被推荐，最常见 4 大隐形硬伤：
1. `robots.txt` 误封了 `Bytespider`（豆包）、`OAI-SearchBot` / `GPTBot`（ChatGPT）或 `YisouSpider`（夸克/千问）；
2. 缺失 `/llms.txt` 与 `/llms-full.txt` 机器可读知识清单；
3. 前端纯 SPA 渲染导致无 JS 首屏只有几十个字，AI 爬虫进去看到一片空白；
4. 缺少 `Organization`、`FAQPage`、`Product` JSON-LD 与原生 HTML `<table>` 参数对比表。

`stepone-geo-check` **100% 纯代码实测、0 大模型 Token 消耗、内置严格 SSRF 安全防护**，覆盖 **6 大维度 × 38 项可验证指标**，并自动生成专属修复代码包。

---

## 🚀 快速开始 (CLI)

```bash
# 一行命令体检任意官网
npx stepone-geo-check https://www.steponeai.com

# 输出结构化 JSON（适合 CI/CD 或 Agent 集成）
npx stepone-geo-check https://www.steponeai.com --json

# 导出本地炫酷可视化 HTML 报告
npx stepone-geo-check https://www.steponeai.com --html report.html

# 自动生成定制修复文件 (llms.txt / robots.txt / schema-jsonld.html)
npx stepone-geo-check https://www.steponeai.com --fix-out ./geo-fixes
```

---

## 🤖 在 OpenClaw / 腾讯 WorkBuddy / MCP 中使用

### 1. OpenClaw / WorkBuddy Skill
本仓库根目录自带标准 [`SKILL.md`](./SKILL.md)，可直接作为技能导入 **OpenClaw（小龙虾）** 与 **腾讯 WorkBuddy**：
```bash
openclaw skills install stepone-geo-check
```

### 2. MCP Server（Cursor / Claude Desktop / Windsurf / WorkBuddy）
在你的 MCP 配置文件中加入：
```json
{
  "mcpServers": {
    "stepone-geo-check": {
      "command": "npx",
      "args": ["-y", "-p", "stepone-geo-check", "stepone-geo-check-mcp"]
    }
  }
}
```
即可直接让 AI 调用 `check_website_geo` 工具体检任意官网并自动生成整改代码。

---

## 📊 6 大维度 × 38 项评估体系

| 维度 | 满分 | 核心实测项 |
| :--- | :---: | :--- |
| **01 · AI 爬虫准入** | 20 | `/robots.txt`、豆包 `Bytespider`、ChatGPT `OAI-SearchBot`/`GPTBot`、`DeepSeek`、`ClaudeBot`、`PerplexityBot`、百度/夸克/必应/Google、`noindex`/`noai` |
| **02 · AI 知识清单** | 20 | `/llms.txt`、`/llms-full.txt`、`/sitemap.xml`、`<link rel="alternate" type="text/markdown">` / `/content.json`、`Sitemap:` 宣言 |
| **03 · SSR 首屏可读** | 20 | 无 JS 有效正文密度、空壳 SPA 判定、HTML 纯文本信噪比、TTFB 响应速度、HTTPS 安全传输 |
| **04 · 结构化 Schema** | 20 | 合法 JSON-LD、`Organization + sameAs`、`FAQPage / Product`、原生 HTML `<table>` 对比表、Canonical & OpenGraph |
| **05 · 语义引用层级** | 10 | `<title>`、`<meta description>`、唯一 `<h1>` + `<h2>/<h3>` 目录骨架、图片 `alt` 多模态覆盖率 |
| **06 · 权威信任信号** | 10 | 企业法定主体与 ICP 备案、问答决策型标题、官方商务联系锚点 |

---

## 🏢 关于基智 GEO

官网结构化体检是 GEO（生成式引擎优化）的第一步。如需进一步系统化提升品牌在豆包、DeepSeek、通义千问与腾讯元宝中的可见度与引用率，欢迎了解：
- **基智 GEO 企业版与渠道商 OEM 独立域名贴牌平台**：[https://geo.steponeai.com](https://geo.steponeai.com)
- **StepOne Voice 全渠道 AI 智能客服与老客唤醒**：[https://www.steponeai.com/voice](https://www.steponeai.com/voice)
- **AI 电话助理 Skill（腾讯 WorkBuddy / OpenClaw）**：[https://www.steponeai.com/workbuddy](https://www.steponeai.com/workbuddy)

## License
MIT © 2026 北京基智科技有限公司 (StepOneAI)
