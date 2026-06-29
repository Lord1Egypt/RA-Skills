# 一个网站为什么 SEO 跑分高 —— 深度分析 + 生产站实测（案例脱敏）

> 案例来源已脱敏，下文以 `example.com`（生产域）/ `staging.example.com`（预发域）/「该工程仓」指代一个真实生产站点。所有方法论与实测结构均为真实数据，仅隐去品牌与域名。

---

## 一句话结论

跑分高不是靠某个插件或事后优化，而是**把 SEO/性能/可访问性的底线变成了"构建时强制门禁"**：10 条规则任一不达标，`build` 直接失败、根本部署不出去。再叠一层别人很少做的 **GEO（让 AI 助手能爬、能引用、能推荐）**。规则前置到 CI、人无法绕过 → 每个上线页面天然合规。

这份报告把这套机制拆开讲清楚，并附上用本工具包对**一个生产站**跑出来的实测结果作为佐证。

---

## 一、根因：三层叠加

### 第 1 层 —— 构建期 10 道硬门禁（跑分高的主因）
工程仓的 `scripts/audit-*.mjs`，由一个 `run-audits.mjs` 在 build 末尾串行执行，**fail-fast**（第一条挂就停、exit 1、build 红）。它们不是 lint 建议，是硬约束：

| 门禁脚本 | 强制内容（精确阈值） | 对应 SEO/CWV 价值 |
|---|---|---|
| `audit-h1` | 每页 `<h1>` 恰好 1 个 | 主题信号唯一、不稀释 |
| `audit-viewport` | viewport meta 必含 `width=device-width` + `initial-scale=1` | 移动优先索引 |
| `audit-semantic` | 每页必有 `<main>`+`<nav>`+`<footer>` | 可访问性 + 内容/外壳区分 |
| `audit-routes` | path 全小写 / 尾斜杠 / ≤3 级 / ≤256B；desc 20–240；canonical host=部署域 | 防重复内容、爬取预算集中、canonical 不发错域 |
| `audit-baseline` | 任一 `font-size < 10px` 即 fail；正文建议 14px | 可读性 + 可访问性 |
| `audit-images` | 每张 `<img>` 有 width/height/alt；非 hero `loading=lazy`；hero `fetchpriority=high`；单张产物 ≤500KB | 防 CLS、压 LCP、图片 SEO |
| `audit-size` | 单页 HTML + 同页 CSS + JS ≤500KB | 传输体积 → LCP/INP、爬取效率 |
| `audit-inline` | 无 inline 可执行 `<script>`（仅放行 ld+json/json/importmap）、无 `on*=` | 支撑严格 CSP `script-src 'self'`、JS 外链可缓存可 defer |
| `audit-external` | HTML/CSS 里不许有跨域 `<link>/<script>/<img>/url()/@import`（白名单空） | 自托管 → 去三方握手、满足 CSP、去隐私依赖 |
| `audit-admin-isolation` | admin bundle 不许泄漏进主站公开 HTML/JS/CSS | 后台不污染主站 SEO 面 |

补：`codemod-nofollow.mjs`（build 后给所有跨 host `<a>` 加 `rel="nofollow noopener"`）。

**关键设计点（值得复用到任何项目）：**
- **canonical 是构建期烤进 HTML 的，不是运行期算的。** 用 `PUBLIC_SITE_ORIGIN` 环境变量在 build 时注入：`build:dev` → staging 域、`build:prod` → 生产域。一份产物绑一个域，**禁止同一份 dist 部署到两个域**（否则 canonical 发错域 = 灾难）。运行时（如 CDN Worker）的变量**不会**进静态构建，不能拿来做 canonical。
- **`audit-images` 查的是 `dist/` 里压缩后的产物字节**，不是 `src/` 源图——保证用户实际下载的就是 ≤500KB。
- **Astro 要显式 `vite.build.assetsInlineLimit: 0`**，否则它默认把小 `<script>` inline 进 HTML，和严格 CSP 撞车、也被 audit-inline 拦。

### 第 2 层 —— 结构化数据（嵌套 @graph）
SEO 库构造、JSON-LD 组件渲染：全站注入 **Organization + WebSite**，按路由加 Article/Product/FAQPage，面包屑自动出 **BreadcrumbList**。全部用嵌套 `@graph` + 稳定 `@id`（`/#organization`、`/#website`）互相引用，绝对 URL 与 canonical 同源构建。这是「让机器（Google 富结果 + LLM）可靠抽取实体与事实」的核心杠杆。

`Organization.knowsAbout` 列了若干主题—— 直接影响 LLM 认为"这个品牌是关于什么的、什么场景该推荐它"。

### 第 3 层 —— GEO / AI 可见性（招牌、和别人拉开差距的部分）
边缘 Worker 的 SEO 层：
- **robots**：生产环境对主流 AI 爬虫**显式 `Allow: /`**（OpenAI 的 GPTBot/OAI-SearchBot/ChatGPT-User、Anthropic 的 ClaudeBot/Claude-User/Claude-SearchBot、Perplexity、Google-Extended…），只 Disallow `/admin/`、`/api/admin/`。逻辑是"靠 AI 可见性吃饭，当然要让 AI 爬虫进来"。
- **llms.txt**：动态生成 `/llms.txt`——给 LLM 的分区站点地图（Start here / Concepts / Research / Industry guides），从路由表生成、排除法务页和纯表单页。
- **sitemap + noindex**：sitemap 与 robots 共用同一份 `NOINDEX_PATHS` 单一可信源，避免漂移。
- **indexnow-ping**：部署后 POST 所有 URL 到 IndexNow，让 Bing/Copilot 即时收录。

**生产实战教训（已写进工具 references）：** 某 staging 域开了 CDN 平台的 "Managed robots / AI Crawl Control"，它在 Worker 输出**之前**注入一段把 GPTBot/ClaudeBot 等全 `Disallow` 的规则——直接架空"欢迎 AI 爬虫"策略。两条铁律：①生产域**永远别开**这开关；②调 robots **只在生产域验证**（staging 显示的是平台注入版）。

---

## 二、生产站实测（用本工具包跑一个真实生产站）

### 构建产物审计 `audit-seo.mjs --dir dist`
```
scanned: 39 html · 3 css · 86 images
errors: 0   warnings: 45   heuristic score: 78/100
```
- **0 错误** —— 39 个页面全过 12 门禁。
- 45 个警告几乎全是 title/description「偏长」——这是**故意为 GEO 写长**的实体丰富标题，属软警告、非问题。

### 线上审计 `audit-live.mjs https://www.example.com`
```
[geo]   ✓ AI 爬虫放行：GPTBot, OAI-SearchBot, ChatGPT-User, ClaudeBot, Claude-User,
              Claude-SearchBot, PerplexityBot, Perplexity-User, Google-Extended,
              GoogleOther, CCBot, Bytespider, Amazonbot, Applebot-Extended  （14 个）
        ✓ llms.txt 在线（AI 可读站点地图）
[robots]✓ 默认爬虫策略：allowed    ✓ 声明了 Sitemap
[sitemap]✓ 34 个 URL（含 <lastmod>）
[jsonld]✓ JSON-LD @types：Organization, WebSite, FAQPage, WebPage, Service,
              OfferCatalog, Product, SoftwareApplication ×4
[headers]✓ HSTS    ✓ Vary: User-Agent    ✓ Cache-Control
[canonical]✓ 首页有 canonical
errors: 0   warnings: 0
```

线上 **0 错误 0 警告**：AI 爬虫全放行、llms.txt 在线、首页 ship 完整嵌套 @graph、安全/缓存头齐全。这就是"GEO 做到位"的样板。

---

## 三、可迁移到任何项目的 7 条精华

1. **把 SEO 底线变成 build 门禁**，别靠人记、别靠事后查——CI 红是最强约束。
2. **canonical 构建期烤入、一份产物绑一个域**，绝不运行期算、绝不跨域复用。
3. **图片预算查产物字节**：每张 ≤500KB + 现代格式 + 尺寸属性 + 懒加载，hero 单独 `fetchpriority=high`。
4. **严格 CSP `script-src 'self'`**：JS 全外链、删 inline script / `on*=`、字体资源全自托管。
5. **结构化数据用嵌套 @graph + 稳定 @id**，全站 Organization+WebSite 打底，`knowsAbout` 写准。
6. **GEO 三件套**：robots 显式放行 AI 爬虫 + `llms.txt` + 部署 ping IndexNow。
7. **robots 只信生产域**：警惕平台层注入的 Managed robots 静默屏蔽 AI。

> 想直接动手：用 `../scripts/audit-seo.mjs` 和 `audit-live.mjs` 对你的站跑一遍，对照 `../references/hard-gates.md` 逐条修。
