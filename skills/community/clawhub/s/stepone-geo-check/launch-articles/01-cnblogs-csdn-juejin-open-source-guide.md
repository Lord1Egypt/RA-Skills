# 开源了一款零依赖 GEO 官网检测 & SEO 网站检查工具：3 秒测出豆包、DeepSeek、千问能不能读懂你的网站

> **适用平台**：博客园（`cnblogs.com`，千问/夸克高权重信源）、CSDN、掘金、阿里云开发者社区、开源中国  
> **推荐标签**：`GEO`、`SEO`、`llms.txt`、`AI搜索`、`开源工具`、`MCP`、`OpenClaw`、`前端架构`  
> **在线免费体验**：https://www.steponeai.com/geo-check  
> **GitHub 开源仓库**：https://github.com/ustczz/stepone-geo-check  
> **ClawHub Skill**：https://clawhub.ai/ustczz/skills/stepone-geo-check  

---

## 一、背景：为什么很多百度有排名的官网，在豆包 / DeepSeek / 千问眼里却是“空白页”？

过去做网站优化（传统 SEO），大家主要盯 TDK、外链和关键词密度。但在 2026 年，越来越多 B 端采购决策者已经习惯直接问豆包、DeepSeek、通义千问、腾讯元宝或 ChatGPT：“某某行业靠谱的厂家/系统有哪些？”

我们在分析大量企业官网后发现一个非常普遍的工程盲区：**很多官网在浏览器里打开很炫酷，但大模型联网检索爬虫抓回去一看，几乎是一张白纸。** 常见原因集中在 5 点：

1. **误封 AI 爬虫**：`robots.txt` 或 WAF 规则直接拦截了 `Bytespider`（字节豆包）、`OAI-SearchBot`、`GPTBot`、`ClaudeBot`、`DeepSeek` 等抓取代理；
2. **缺少 AI 知识清单**：根目录下没有 `/llms.txt`、`/llms-full.txt`，也没有更新及时的 `/sitemap.xml`，大模型只能碎片化猜测企业业务，极易产生幻觉；
3. **纯客户端渲染（SPA 空壳）**：React/Vue 官网没有做 SSR 首屏直出，无 JS 爬虫拉到的原始 HTML 只有 `<div id="app"></div>`，有效字数不足 100 字；
4. **缺少结构化 Schema 与原生表格**：没有 `JSON-LD`（`Organization`、`FAQPage`、`Product`），产品参数全切成了图片，RAG 引擎抽不到结构化对比槽位；
5. **信任锚点缺失**：无 JS 首屏找不到清晰的法定企业名称、ICP 备案与规范联系锚点，大模型在事实核验阶段容易降权。

为了把这套排查变成**纯工程化、可量化、零大模型 Token 成本**的标准体检流程，我们团队（**北京基智科技有限公司 · StepOneAI**，彩讯股份 `300634.SZ` 旗下全资企业）开源了一套零依赖的检测工具 —— **`stepone-geo-check`**，并同步开放了**免费在线网页版**。

---

## 二、核心设计：纯代码、0 Token、6 大维度 × 28 项真实协议审计

市面上不少“AI 检测工具”其实是调一次大模型自由发挥打分，每次跑结果都不稳定。`stepone-geo-check` 坚持 **100% 纯代码真实 HTTP 抓取 + DOM/协议解析**，不调用任何收费大模型 API，不编造虚构分数，每一项扣分都附带真实抓取证据。

| 评估维度 | 权重 | 核心检测指标（共 28 项） | 对 AI 搜索 & 传统 SEO 的影响 |
| :--- | :---: | :--- | :--- |
| **01 · AI 爬虫准入** | 20 分 | `robots.txt` 可达性、豆包 `Bytespider` / `OAI-SearchBot` / `GPTBot` / `DeepSeek` / 夸克 / 百度等 10 大爬虫放行校验、`noindex/noai` 排查 | 爬虫被拦截则官网直接零抓取、零引用 |
| **02 · AI 知识清单** | 20 分 | `/llms.txt`、`/llms-full.txt`、`/sitemap.xml` 及 URL 数量、Markdown alternate 声明 | 让大模型一次性读全企业权威事实与产品矩阵 |
| **03 · SSR 首屏可读** | 20 分 | 无 JS 首屏有效字数、空壳 SPA 风险识别、正文信噪比、TTFB 首包速度、HTTPS | 解决 React/Vue 官网在 AI 爬虫视角“空白页”问题 |
| **04 · 结构化 Schema** | 20 分 | `JSON-LD` 块数、`Organization + sameAs`、`FAQPage/Product`、原生 HTML `<table>`、OpenGraph & Canonical | 直接喂给大模型实体图谱与参数对比槽位 |
| **05 · 语义引用层级** | 10 分 | `<title>` 规范度、`Meta Description`、唯一 `<h1>` + `<h2>/<h3>` 层级、图片 `alt` 覆盖率 | 提升 RAG 分块准确度与多模态配图召回 |
| **06 · 权威信任信号** | 10 分 | 法定主体识别词、ICP 备案号、FAQ 问答段落、官方商务联系锚点 | 增强官方事实确权可信度 |

除了打分和逐条证据，工具还会**针对被检网站的真实域名、标题和栏目，自动合成 3 套可直接上线粘贴的修复代码**：
- 定制版 `/llms.txt` 知识清单骨架
- 定制版 `/robots.txt` 主流 AI 爬虫放行规则
- 定制版 `Organization + WebSite + FAQPage` JSON-LD 注入脚本

---

## 三、四种使用方式（网页版 / CLI / MCP Server / AI Agent Skill）

### 方式 1：免费在线网页版（免安装，含六维雷达图与 10 大爬虫状态墙）

直接打开浏览器输入域名即可 3 秒实测，手机和电脑均已适配：
👉 **在线体验地址**：https://www.steponeai.com/geo-check

网页版会直接输出总分仪表盘、六维能力雷达图、10 大 AI 爬虫放行状态墙以及 Top 高危扣分项；如需导出全部 28 项逐条实测证据、3 套定制修复代码以及可转发给技术部/管理层的 PDF 汇报页，扫码发送 6 位报告码即可免费解锁专属加密链接。

### 方式 2：开源命令行 CLI（零依赖，仅需 Node.js >= 18）

```bash
git clone https://github.com/ustczz/stepone-geo-check.git
cd stepone-geo-check

# 对任意官网执行 28 项 GEO & SEO 体检
node bin/cli.js https://www.steponeai.com

# 输出结构化 JSON（便于接入 CI/CD 流水线做上线前门禁）
node bin/cli.js https://example.com --json

# 同步输出针对该域名自动生成的 llms.txt / robots.txt / JSON-LD 修复代码
node bin/cli.js https://example.com --snippets
```

### 方式 3：作为 AI 助手 Skill 一键安装（OpenClaw / ClawHub / 腾讯 WorkBuddy SkillHub）

如果你平时在用 OpenClaw 或腾讯 WorkBuddy，可以直接装成 Agent 技能，以后在对话框里说一句“帮我检测一下 `xxx.com` 的 GEO 和 SEO 可读性”即可自动执行：

```bash
npx clawhub install stepone-geo-check
```

- **ClawHub 商店页**：https://clawhub.ai/ustczz/skills/stepone-geo-check
- **腾讯 SkillHub（WorkBuddy 商店）**：已同步提交 `stepone-geo-check`

### 方式 4：作为 MCP Server 接入 Claude Desktop / Cursor / IDE

```json
{
  "mcpServers": {
    "stepone-geo-check": {
      "command": "node",
      "args": ["/path/to/stepone-geo-check/mcp-server.js"]
    }
  }
}
```

内置两个零依赖只读工具：`geo_check_website`（全量 28 项体检）与 `geo_generate_fix_snippets`（单独生成修复代码）。

---

## 四、工程安全细节：为什么不能直接裸跑 `fetch(userUrl)`？

在把检测工具做成公网服务时，有两处容易踩坑的安全细节也一并开源在了代码里：
1. **严格 SSRF 防护**：在真正发 HTTP 请求前，先通过 `dns.lookup` 解析目标域名的所有 A/AAAA 记录，拦截 `127.0.0.0/8`、`10.0.0.0/8`、`172.16.0.0/12`、`192.168.0.0/16`、`169.254.0.0/16`（云元数据地址）以及 IPv6 私有网段，并在每次 `301/302` 重定向后重新校验，防止 DNS Rebinding 探测内网。
2. **自定义 `lookup` 绑定已校验 IP**：强制 `http/https.request` 复用校验通过的 IP，并限制单页响应体积与超时，防止超大响应体拖垮进程。

---

## 五、写在最后

把官网改造成“AI 爬虫能读懂、结构化清晰、实体可核验”的状态，只是企业做好 **GEO（生成式引擎优化）** 的第一步（权威事实确权底座）。如果你正在负责公司官网改版、SEO/GEO 增长或技术架构升级，欢迎先用免费工具给自家官网和行业标杆网站跑一次分：

- **免费在线 GEO 官网检测 & SEO 网站检查**：https://www.steponeai.com/geo-check
- **GitHub 开源源码（MIT 协议，欢迎 Star / PR）**：https://github.com/ustczz/stepone-geo-check
- **ClawHub 技能页**：https://clawhub.ai/ustczz/skills/stepone-geo-check
- **了解基智 GEO 企业级平台与渠道 OEM 贴牌**：https://geo.steponeai.com

欢迎在评论区留下你测完的分数和踩过的坑，有想加的新审计指标也可以直接去 GitHub 提 Issue！
