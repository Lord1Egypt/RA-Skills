# SEO / GEO 体检 + 优化工具包

> 一套**可执行的网站 SEO + GEO（AI 可见性）审计工具**，从 example.com 官网"跑分高"的工程硬约束里提炼而成。
> 给团队任何人用：可以当 Claude skill 调用，也可以纯命令行独立跑（只需 Node，零依赖、零安装）。

跑分高不是玄学——参考生产站的构建流水线里挂了 10 个**硬门禁**，任何一条不达标就 **build 失败**，逼着每个页面都满足 SEO/性能/可访问性底线；再叠一层 **GEO（让 ChatGPT / Claude / Perplexity / Gemini 能爬、能引、能推荐你）**。这个包把那套规则抽象成框架无关的工具，能对任意网站跑一遍、报问题、给修法。

实测：用本包审 example.com 生产站 → **构建产物 0 错误、线上 0 错误 0 警告**（14 个 AI 爬虫全放行、llms.txt 在线、JSON-LD 是 Organization+WebSite+Product+… 的嵌套 @graph）。

---

## 文件夹结构

```
seo-audit/                 ← 这个目录本身就是 seo-audit skill（可直接拷进 ~/.claude/skills/）
├── SKILL.md               ← skill 说明 + 4 步工作流 + 12 门禁速查
├── README.md              ← 你正在看的这份（上手入口）
├── scripts/
│   ├── audit-seo.mjs      ← 扫「构建产物目录」：12 项硬门禁
│   └── audit-live.mjs     ← 扫「线上 origin」：robots/AI 爬虫 / sitemap / llms.txt / JSON-LD / 安全头
├── references/
│   ├── hard-gates.md          ← 12 门禁：精确阈值 + 为什么 + 通用修法 + Astro/CF 参考实现
│   ├── structured-data.md     ← JSON-LD（@graph 嵌套）配方：Org/WebSite/面包屑/Article/Product/FAQ
│   ├── geo-ai-visibility.md   ← GEO 招牌层：AI 爬虫精确 UA 白名单 / llms.txt / knowsAbout / IndexNow
│   └── lcp-playbook.md        ← LCP 实战手册：参考站移动端 7.5s → 1.5s 的全部实测杠杆 + CLS 护栏 + CI 锁定
└── analysis/
    └── case-study-build-time-seo-gates.md   ← 深度分析：跑分高的根因 + 生产站实测结果
```

---

## 用法一：命令行独立跑（推荐给开发同事，不需要 Claude）

前置：**Node ≥ 18**（自带 `fetch`）。无需 `npm install`，两个脚本零外部依赖。

### 1) 审计构建产物（本地 / CI 都行）
先把站点 build 出来，拿到产物目录（Astro `dist/`、Next `out/`、Hugo `public/`、Jekyll `_site/`、或任意一堆 HTML），然后：

```bash
node scripts/audit-seo.mjs --dir <构建产物目录>

# 可选参数：
#   --strict          把 warning 也当 error（CI 模式，有问题 exit 1）
#   --json            输出 JSON（便于程序消费）
#   --max-page-kb 500 单页 HTML+CSS+JS 预算（默认 500KB）
#   --max-img-kb 500  单张图片预算（默认 500KB）
```

输出里 `✗` = ERROR（真伤排名 / 卡爬虫 / 拖垮 Core Web Vitals，优先修），`⚠` = WARN（最佳实践没达到）。末尾有个粗略 score 当仪表盘看，不是 Lighthouse 分。

### 2) 审计线上站（GEO 那层只能在线上看）
```bash
node scripts/audit-live.mjs https://www.example.com
```
查：robots.txt 对各 AI 爬虫是放行还是拦截、有没有 sitemap、有没有 `llms.txt`、首页实际 ship 了哪些 JSON-LD `@type`、HSTS / Vary / Cache-Control。

> ⚠️ **robots 一定在「生产 origin」验证**：Cloudflare 等平台的 "Managed robots / AI Crawl Control" 会在你的源站之前注入自己的 robots，可能把 AI 爬虫静默 `Disallow`，而且 staging 域显示的往往是注入版不是你真正 ship 的版本。

### 接进 CI（可选）
```bash
# 在 build 之后加一步，回归就让流水线红：
node scripts/audit-seo.mjs --dir dist --strict
```

---

## 用法二：作为 Claude / Cursor 的 skill

把这个目录整个拷进自己的技能目录：

```bash
cp -R . ~/.claude/skills/seo-audit
```

之后在 Claude Code / Desktop / Cursor 里直接说：
- "审计一下这个站的 SEO" / "帮我把 SEO 分提上去"
- "让我的站能被 AI / ChatGPT 发现" / "加 llms.txt" / "修 robots 放行 AI 爬虫"
- "加结构化数据 / JSON-LD" / "配 sitemap / canonical / Open Graph"

它会自动定位构建产物、跑审计、按严重度报问题、对照 `references/` 给修法、改完再跑一遍确认。

---

## 12 门禁速查

| # | 门禁 | 底线 |
|---|---|---|
| 1 | `<h1>` 唯一 | 每页恰好 1 个 |
| 2 | viewport meta | `width=device-width, initial-scale=1` |
| 3 | 语义地标 | `<main>` + `<nav>` + `<footer>` |
| 4 | title + description | 都要有（长度为软警告，GEO 可故意写长） |
| 5 | canonical | 绝对 URL，host=部署域，**构建期**烤入（非运行时） |
| 6 | Open Graph | `og:title` + `og:image` |
| 7 | 图片 | 每张有 width/height/alt；非 hero `lazy`；hero `fetchpriority=high`；单张 ≤500KB |
| 8 | 无 inline 可执行 script / 无 `on*=` | 走严格 CSP `script-src 'self'` |
| 9 | 无外链资源 | 字体/图/CSS/JS 全自托管 |
| 10 | 单页文本预算 | HTML+同页 CSS+JS ≤500KB（图片单独算） |
| 11 | 结构化数据 | 全站 Organization + WebSite，按页加 Article/Product/FAQ |
| 12 | URL 规范 | 全小写 / 尾斜杠 / ≤3 级 / 单一路由源 |

**GEO 层**：robots 显式放行主流 AI 爬虫 + ship `llms.txt` + `Organization.knowsAbout` 写清楚做什么 + 部署后 ping IndexNow。详见 `references/geo-ai-visibility.md`。

**性能层（LCP / Core Web Vitals）**：门禁全过但站还是慢？看 `references/lcp-playbook.md` —— 参考站移动端 LCP 7.5s → 1.5s 的实测杠杆，按影响排序：消灭 render-blocking CSS → 关键 CSS 拆分 → 字体 preload 纪律（无用 preload 反而占满关键路径）→ 延后首屏非 LCP 重 DOM → hero 图 eager + fetchpriority → 三方 JS 推迟到 idle/首次交互。核心方法论：先找到**真正的 LCP 元素**（常常是文字不是图），用 DevTools 实测节流（别信 Lantern 模拟值），每改一步都量一次，最后用 Lighthouse CI 门禁 + 单页 JS 字节预算把战果锁死。

逐条「精确阈值 + 为什么 + 怎么修」看 `references/hard-gates.md`；想看跑分高的根因和实测看 `analysis/case-study-build-time-seo-gates.md`。

---

## 原则

- 别为了让审计过而放宽阈值——**修页面，不是改门禁**。
- SEO 活在「渲染后的 HTML」里：审构建产物 / 线上页，不是审源码模板。
- 修的时候改源（模板 / 布局 / 配置），别改构建产物（会被重新生成覆盖）。
- 脚本用保守正则提取信号、不跑完整 DOM：**全绿是强证据，不是形式化保证**。
