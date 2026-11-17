# references/ai-seo.md — AI 搜索优化（AEO/GEO）深度清单（geo 子流程用）

> 目标：让内容被 AI 引擎（ChatGPT/Perplexity/Claude/Copilot/豆包/文小言）与 Google AI Overviews 引用。
> 核心事实：AI Overviews 出现于约 45% 搜索、最高减少 58% 点击；优化内容被 AI 引用率高 ~3 倍。
> 品牌经第三方来源被引用的概率是自有域名的 **6.5 倍**（2026 最值得吃的流量红利）。
> 要点提炼自 marketingskills `ai-seo` v2.4.0（2026-09 对照原文核查）。

> 🌐 语言 / Language：本清单是**内容规范**而非语言约束；默认中文，用户用英文或其他语言提问时就用该语言输出（答案语言跟随用户）。
> This checklist is a content spec, not a language mandate — answer in the user's language.

## 1. AI 搜索工作原理（平台差异）

| 平台 | 工作方式 | 选源倾向 |
|------|---------|---------|
| Google AI Overviews | 摘要排名靠前的页面 | 与传统排名强相关 |
| ChatGPT（联网） | 搜索网页 + 引用来源 | 来源范围比只看排名更广 |
| Perplexity | 始终带链接引用 | 权威、新鲜、结构良好的内容 |
| Gemini | Google AI 助手 | Google 索引 + Knowledge Graph |
| Copilot | Bing 系 | Bing 索引 + 权威源 |
| Claude | Brave Search（启用时） | 训练数据 + Brave 结果 |

**关键认知**：传统 SEO 让你"排名"，AI SEO 让你"**被引用**"——结构良好的页面即使排第 2-3 页也可能被 AI 引用（选源看质量/结构/相关性，不只看排名）。

### Google 官方立场（AI Overviews）
- ✅ 无需特殊标记/文件；AI 功能根植于核心搜索排名系统
- ✅ people-first 内容 + 语义 HTML 即最优
- ❌ **不为 AI 单独写内容**（scaled content abuse 整站风险）
- ❌ 不 chunk/拆内容喂 AI
- ❌ 无 AI 专属 Search Console 报告——用标准指标衡量

### 非 Google AI 引擎（ChatGPT/Perplexity/Claude/Copilot）
- 奖励**可抽取结构**：独立答案段落（40-60 词）、FAQ、对比表、定义块、步骤块、pros/cons、统计块
- 解析 `llms.txt` / `llms-full.txt`、结构化定价页等机器可读文件
- **第三方引用权重大**（Reddit/维基/评测站 > 自站排名页）
- 带 schema 的内容在非 Google AI 引擎可见度高 30-40%

### 国内 AI（豆包/文小言/Kimi/百度 AI 搜索）
- 无 llms.txt 标准支持，但吃清晰结构 + 权威第三方 + 百度收录

**默认策略**："为人写作、为清晰组织"——两边通吃。Google 吃 people-first，其他 AI 吃结构，两者不冲突。

## 2. 量化证据（Princeton GEO 研究，KDD 2024，Perplexity 实测）

9 种优化方法的可见度提升排名：

| 方法 | 提升 | 怎么用 |
|------|:----:|--------|
| 引用来源 | **+40%** | 关键论断加权威链接 |
| 加统计数字 | +37% | 具体数字 + 来源 + 日期 |
| 加引述 | +30% | 专家原话 + 姓名头衔 |
| 权威语气 | +25% | 展示专业度 |
| 提升清晰度 | +20% | 简化复杂概念 |
| 技术术语 | +18% | 领域词汇 |
| 独特词汇 | +15% | 用词多样性 |
| 流畅度优化 | +15-30% | 可读性（流畅度+统计 = 最大组合） |
| ~~关键词堆砌~~ | **-10%** | **主动伤害 AI 可见度** |

低排名站点受益更大（引用来源最高 +115%）。

**被引用 ≠ 被推荐**：被引用 = 内容被 consult；被推荐 = 进买家候选名单（靠全网共识：评测/论坛/分析师/媒体）。自我推销式"最佳 X 榜单"可能反噬——某 B2B 研究中 69% 的自我推销 listicle 引用出现在**推荐竞争对手**的回答里。布局要克制真实。

**最易被引用的内容类型**：对比文章 ~33% / 权威指南 ~15% / 原创研究数据 ~12% / best-of 列表 ~10% / 产品页 ~10% / 教程 ~8%。低质：无结构泛博客、营销废话薄页、gated 内容、无日期无署名、纯 PDF。

## 3. AI bot 访问检查（robots.txt）

AI bot User-agent 完整名单：
- `GPTBot` + `ChatGPT-User`（OpenAI/ChatGPT）
- `OAI-SearchBot`（ChatGPT 搜索）
- `PerplexityBot`（Perplexity）
- `ClaudeBot` + `anthropic-ai`（Anthropic/Claude）
- `Google-Extended`（Gemini/AI Overviews 训练；**不管 Google 搜索**）
- `Bingbot`（Copilot 底层）
- `CCBot`（Common Crawl，**纯训练爬虫**）
- 国内：`Bytespider`（字节）、`Baiduspider`（百度）

检查方法：
1. 读 robots.txt：以上 UA 是否有 `Disallow`
2. 判定：
   - 显式放行 → ✅
   - 屏蔽搜索型 bot（GPTBot/PerplexityBot/ClaudeBot/Google-Extended/Bingbot）→ 🟠（该平台无法引用你）
   - 屏蔽训练型 bot（CCBot）→ ✅ 可接受的折中（防训练但不丢引用）
   - 未提及（默认放行）→ ✅ 但建议显式声明
3. ⚠️ 反坑：确认 robots.txt 是真实文件（fallback 陷阱见 technical-seo.md）

推荐模板（放行 AI bot，可屏蔽 CCBot）：
```txt
User-agent: *
Allow: /

User-agent: GPTBot
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: anthropic-ai
Allow: /

User-agent: Google-Extended
Allow: /

# 防训练但保留引用（可选折中）
# User-agent: CCBot
# Disallow: /

Sitemap: https://<canonical-host>/sitemap.xml
```

## 4. llms.txt / llms-full.txt（AI 可读站点地图）

格式（https://llmstxt.org）：
```txt
# <站点名>

> <一句话站点说明：这是什么、给谁、核心价值>

## 关于本站
- 类型/定位：…
- 主要受众：…
- 内容语言：…

## 核心页面
- [页面标题](https://<host>/path)：一句话说明该页价值
- [关于](https://<host>/about)：作者/团队介绍

## 内容政策（可选）
- 允许 AI 引用本站内容，引用请注明来源
```

规范要点：
- 每行一个链接条目，`- [标题](URL)：说明`，说明一句话讲清页面价值（AI 拿它做路由判断）
- 核心页面 10-30 条足够；`llms-full.txt` 放全量
- ⚠️ 反坑：静态托管 fallback 会返回 HTML——部署后必须验证 content-type 是 text/plain
- 站点结构大改时同步更新

## 5. /pricing.md — AI 代理可读定价（v2.4 新增重点）

AI 代理正在替用户"采购"：评估工具时若定价锁在 JS 渲染页或"联系销售"墙后，代理会跳过你推荐竞争对手。
- 在站点根放 `/pricing.md` 或 `/pricing.txt`：纯 Markdown 结构化定价，任何 LLM 可直接解析
- 格式：分级列出 价格/额度上限/功能/链接，单位统一（月付/年付、per-seat/flat）
- 原则：具体额度阈值（不是只有功能名）、保持更新（过期定价比没有更糟）、从 sitemap 和定价页链过去
- 同类思想：robots.txt（给爬虫）、llms.txt（给 AI 上下文）、AGENTS.md（给代理能力）——pricing.md 给"采购代理"

## 6. 内容可抽取性检查（AI 引用工程）

对关键页逐项过：
- [ ] **首段定义句**：开头 40-60 词内"X 是…"说清实体（AI 抽取答案第一候选）
- [ ] **独立答案块**：每 H2 段首直接给答案再展开（不要铺垫三段）
- [ ] **FAQ 区块**：3-8 个自然语言问答，页面可见 + FAQPage schema
- [ ] **对比表**：选型/交易内容用真 `<table>`（AI 解析表格强于散文）
- [ ] **定义块**：术语首次出现给一句话定义（`<dfn>` 或加粗）
- [ ] **来源引用**：数据/统计带链接 + 日期（+40% 可见度）
- [ ] **更新时间**：6 个月内更新过；"最后更新: 日期"显眼展示
- [ ] **语义 HTML**：`<main>/<nav>/<article>/<button>` + 标题层级 + alt（AI 代理走 accessibility tree）
- [ ] **无 JS 墙**：核心内容不藏在 4 个框架加载后才渲染的 JS 后（代理看到空白页 = 不存在）
- [ ] **可见定价/规格/联系信息**：公开可索引页，不 gated

判定：首段无定义句 → 🟠（最大损失点）；无 FAQ/表格 → 🟡；其余单项缺失 → 🟡。

## 7. 第三方引用布局（隐藏权重）

AI 引用排序 ≈ 权威第三方提及 > 站内自证（6.5x）。策略：
1. 内容值得被引：独家数据/实测结论/开源项目（被引根因）
2. 主动布局：开源 README、Product Hunt、评测站、维基类、行业 roundup、社区高赞回答（知乎/SO/Reddit）、YouTube 教程（AI 读视频的文字层：transcript/字幕/章节/简介）
3. 站内互引：官网 ↔ 博客 ↔ 店铺同品牌互链（品牌实体一致性）
4. 监控：见下节

## 8. AI 可见度监控

**DIY 月度检查（无工具）**：
1. 挑 10-20 个核心查询（"什么是 X"/"最佳 X 用于 Y"/"品牌 vs 竞品"/"如何…"/"X 定价"）
2. 逐个跑 ChatGPT / Perplexity / Google AI Overviews
3. 记录：自己被引用吗？谁被引用？哪个页面？
4. 表格追踪月度变化

**第三方工具**（可选）：Otterly AI / Peec AI / ZipTie / LLMrefs（AI 引用追踪）。GSC 无 AI 专属报告——Google 侧仍用标准 Performance/Coverage/CWV 报告。

## 9. 红线（Google 政策 + 实操）

- ❌ 不为 AI 单独造内容 / 拆 chunk 喂 AI（scaled content abuse）
- ❌ 页面塞对用户隐藏的"AI 抽取专用段落"（cloaking 变体）
- ❌ 批量低质 AI 页冲量；伪造引用；刷 Reddit/维基
- ❌ 想被引用却屏蔽 AI bot（自相矛盾）
- ⚠️ 屏蔽/放行 AI bot 是商业决策：内容站放行；怕训练可只屏蔽 CCBot 这类纯训练爬虫
- ⚠️ llms.txt 不放不存在的页面/链接

## 10. geo 输出模板

```markdown
# <域名> AI 搜索优化方案
## AI bot 现状：<robots.txt 检查结果> → <修改>
## llms.txt：<现状> → <生成/更新>
## 关键页可抽取性：逐页清单（首段/FAQ/表格/来源/更新）
## 第三方引用布局：<目标清单 + 动作>
## 优先级：P0（llms.txt + robots）/ P1（首段与 FAQ 改造）/ P2（第三方布局）
```
