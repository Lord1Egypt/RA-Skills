# references/technical-seo.md — 技术 SEO 深度清单（audit 子流程用）

> 按「检查清单 → 判定标准 → 修复方法 → 验证方式」组织。分级：🔴 阻断索引/访问 / 🟠 明显扣分 / 🟡 优化项。
> 反坑条目（实战踩过）以 ⚠️ 标注。
> 要点提炼自 marketingskills `seo-audit` v2.0.1（2026-09 对照原文核查）。

> 🌐 语言 / Language：本清单是**内容规范**而非语言约束；默认中文，用户用英文或其他语言提问时就用该语言输出（答案语言跟随用户）。
> This checklist is a content spec, not a language mandate — answer in the user's language.

## 0. 探测工具与抓取姿势

| 目标 | 工具 | 说明 |
|------|------|------|
| 响应头/状态码/跳转 | `curl -sI -o /dev/null -w "%{http_code} %{redirect_url}" <url>` 或 Node fetch redirect:'manual' | 看 301/302 目标 |
| robots.txt / sitemap 真实性 | 抓文本 + 检查 content-type | ⚠️ 静态托管/SPA 对任意路径返回 200 + HTML fallback，会误判"文件存在" |
| 首页/页面标签 | 浏览器渲染（能跑 JS） | schema、SPA 内容必须浏览器 |
| DNS | `nslookup <domain>` / 公共 DNS 查询 | 查裸域 A 记录是否存在 |
| CWV | PageSpeed Insights https://pagespeed.web.dev | 移动端优先，需真实浏览器 |

⚠️ **robots.txt / sitemap fallback 陷阱（实测反坑）**：Next.js 静态导出、Vercel/Netlify、某些 CDN 对不存在的路径返回 200 + 站点 HTML。判定真实文件：`content-type` 含 `text/plain` / `application/xml` 且首字符非 `<html`/`<!DOCTYPE`。否则视为"文件不存在"→ 🔴。

⚠️ **静态抓取测不到 JS 注入的 schema**：判定"无 schema"前必须浏览器渲染复核（见 schema.md）。

⚠️ **抓取环境 ≠ 站点问题**：被墙/证书/超时先换工具复核，别急着下"站点挂了"结论。

## 1. 可爬性与索引

### robots.txt
检查：
- `GET https://<host>/robots.txt` 返回真实文本（见上反坑）
- 无 `Disallow: /` 全站屏蔽（除非有意）
- 重要路径（/、/blog、/products 等）未被意外 Disallow
- 有 `Sitemap: <绝对URL>` 行
- AI bot 策略显式：GPTBot / PerplexityBot / ClaudeBot / Google-Extended / Bingbot 未被屏蔽（geo 子流程详查）

判定：
- 文件不存在/HTML fallback → 🔴（爬虫只能靠猜，新页收录慢）
- 屏蔽重要页 → 🔴
- 无 Sitemap 行 → 🟠

修复（按技术栈）：
- Next.js：`app/robots.ts` 或 `public/robots.txt`（静态导出必须 public/）
- Halo：主题设置或插件；确认输出真实文本而非走页面路由
- 静态站：站点根放 `robots.txt`（确认部署平台不 rewrite 到 404 页）

验证：重新 GET，确认 content-type 与内容；GSC → 抓取测试。

### XML sitemap
检查：
- 位置：`/sitemap.xml`、`/sitemap_index.xml` 或 robots.txt 声明位置
- ⚠️ 同上 fallback 反坑：必须真实 XML（content-type xml、首字符 `<?xml`）
- 只含 canonical 可索引 URL（无 http 版本、无参数页、无 noindex 页）
- 无 4xx/5xx 死链（抽查 10% 或脚本全查）
- 已提交 GSC / 百度站长平台
- 有 lastmod 且随内容更新

判定：缺失/假文件 → 🔴；含死链/非 canonical URL → 🟠；无 lastmod → 🟡。

修复：
- Next.js：`app/sitemap.ts` 动态生成（自动带 lastmod），或静态导出时构建脚本生成
- Halo：SEO 插件自动生成；确认 URL 前缀与 canonical 版本一致
- 静态站：构建时生成 sitemap.xml（脚本遍历页面输出），部署前确认可访问

验证：GET 确认 XML 有效；GSC 提交后看"已发现/已抓取"；用 sitemap 校验器（如 https://www.xml-sitemaps.com/validate-xml-sitemap.html）。

### Canonical 与版本归一
检查：
- 首页与代表页有自引用 canonical：`<link rel="canonical" href="https://<canonical-host><path>">`
- http/https 只留一个：http 应 301 → https（⚠️ 实测反坑：三站 http/https 都 200 并存 → 重复内容权重分散）
- www/裸域只留一个，另一个 301
- 尾斜杠策略统一（`/about` vs `/about/`）
- 无 canonical 链/环（A→B→A）

判定：
- 无 canonical + http/https 并存 → 🔴（重复内容判定风险最高）
- 仅缺 canonical → 🟠
- 尾斜杠不一致 → 🟡

修复：
- Next.js：`next-seo` 或 metadata `alternates.canonical`；中间件统一重定向
- Halo：主题输出 canonical；服务器层（Tengine/Nginx/CDN）配 http→https 301 + 裸域→www 301
- 静态站：每页 <head> 手写/构建注入；托管平台配强制 HTTPS 跳转

验证：`curl -sI http://<host>/` 看 301 Location；页面源码确认 canonical 存在且为 https 规范版本。

### 裸域 / 子域可达性（实测反坑）
检查：`https://example.com`（不带 www）能否访问；DNS 是否有 A/AAAA 记录。
判定：裸域无 A 记录（NS 存在但无 A）→ 🔴。用户手输裸域打不开、外链若用裸域全失效、品牌流量流失。
修复：DNS 控制台加裸域 A 记录指向与 www 相同 CDN/IP；配 301 归一（裸域 → www 或反向，二选一）。
验证：nslookup + 浏览器访问裸域确认 301 到规范版本。

### 索引状态
检查：
- `site:<domain>` 在 Google/百度抽查收录量级
- noindex meta/X-Robots-Tag 是否误用在重要页（分页、筛选页、后台页用 noindex 是正常的，落地页/文章页误用是事故）
- 重定向链（>3 跳）/环；软 404（返回 200 的"页面不存在"页）；死链
- GSC 覆盖率报告：排除原因（404/软404/noindex/重复）

判定：重要页 noindex → 🔴；软 404 成片 → 🟠；少量死链 → 🟡。
修复：移除误用 noindex；软 404 改为真 404/410；死链 301 到相关页或删 sitemap 条目。
验证：GSC 覆盖率两周内观察排除数下降；抽查改后页面 headers。

### 站点架构
检查：重要页面距首页点击 ≤3；无孤儿页（无任何内链指向）；导航/面包屑完整；内链都用 canonical 版本 URL。
判定：核心页埋太深/孤儿页 → 🟠；内链指向 http 或带参数版本 → 🟠（权重不集中）。
修复：首页/主导航加核心入口；正文自然内链；面包屑 BreadcrumbList schema。
验证：人工按导航走一遍；Screaming Frog 类工具跑全站（可选）。

### Crawl Budget（大站专用，>10 万页才重点考虑）
检查：参数化 URL 是否失控；分面导航（faceted navigation）是否正确处理（noindex 或参数规则）；无限滚动是否有分页 fallback；URL 中无 session ID。
判定：参数页吞噬抓取配额 → 🟠（小站基本不用管，标注即可）。
修复：GSC 参数处理规则；分面页 noindex/canonical 到代表页；无限滚动内容配分页链接。

## 2. 技术基础

### Core Web Vitals（⚠️ 需浏览器实测，静态抓取测不了）
判定标准（移动端）：
- LCP < 2.5s（>4s 🔴）
- INP < 200ms（>500ms 🔴）
- CLS < 0.1（>0.25 🔴）
修复：
- LCP：压缩/转 WebP-AVIF 图片、preload LCP 资源、消除渲染阻塞 JS/CSS、CDN 加速 TTFB
- INP：减主线程长任务、懒加载非关键 JS、避免复杂布局 thrash
- CLS：图片/广告/嵌入预留尺寸、font-display: swap、避免顶部插入内容
验证：PageSpeed Insights 复测；CrUX 数据（有流量后）；GSC Core Web Vitals 报告。

### 速度因素（CWV 之外）
检查：TTFB（服务器响应）；图片格式/尺寸/压缩；JS 执行量；CSS 交付方式；缓存头；CDN 使用；字体加载（font-display: swap）。
工具：PageSpeed Insights / WebPageTest / Chrome DevTools / GSC CWV 报告。

### 移动友好
检查：响应式（非独立 m. 站）；viewport meta；无横向滚动；可点击元素尺寸（tap target）；移动端内容与桌面一致（移动优先索引）。
判定：独立 m. 站 → 🟠；无 viewport → 🔴（移动渲染异常）。

### HTTPS / 混合内容 / HSTS
检查：证书有效期；https 页是否引 http 资源（混合内容，浏览器会拦截）；有无 HSTS 头；SSL Labs 评分。
判定：证书过期/无效 → 🔴；混合内容 → 🟠（部分资源被拦）；无 HSTS → 🟡。
修复：全站资源改 https/协议相对；CDN 层加 HSTS 头（`Strict-Transport-Security: max-age=31536000`）。
验证：浏览器无混合内容警告；`curl -sI` 看 HSTS 头。

### URL 结构
检查：可读（含关键词）；小写+连字符；无查询参数承载内容（`?id=123`）；无会话 ID/跟踪参数污染（用 canonical + 参数处理规则）。
判定：参数页被索引 → 🟠；URL 含大写/下划线/中文 → 🟡。
修复：重写 URL 并 301；GSC 参数处理规则；canonical 指向干净版本。
验证：抽查索引中 URL 形态；301 后 site: 查询。

## 2.5 国际 SEO / 多语言（站点服务多语言/多地区时启用）

⚠️ 三站当前为单语中文站，此节仅在站点出现多语言版本时执行；错误配置会压制整个语言版本索引。

### Hreflang
三种等价放置：HTML `<link>`（head）/ HTTP `Link` 头 / XML sitemap `<xhtml:link>`。多法并用必须一致，冲突会导致该语言对被丢弃。
检查：
- 每页 hreflang 集合**包含自引用**（漏自引用 = 全部 hreflang 被忽略）
- **互惠**：A 指向 B，B 必须指回 A（单向 = 该对被丢弃）
- 合法代码：ISO 639-1 语言 + 可选 ISO 3166-1 地区（`en`、`en-GB`；❌ 永远不写 `en-UK`）
- `x-default` 存在，指向默认页（语言选择器或默认语言）
- 所有目标 URL 返回 200、可索引、与 canonical 一致
- 无重复语言-地区码指向不同 URL
- Bing 补充：`<html lang>` + `<meta http-equiv="content-language">`（Bing 把 hreflang 当弱信号）
- 规模化：≥10 语言优先 sitemap 方式（<xhtml:link> 不占 5 万 URL 上限，但注意 50MB 文件限制）；hreflang 只加在真正收到错误语言流量的页，不必每页

### 多语言 canonical（反模式）
- 每个语言页自引用 canonical（`/en/page` canonical 到自身）
- ❌ 跨语言 canonical（法语指到英语）→ 整个非 canonical 语言版本被压制
- canonical URL 必须出现在 hreflang 集合里（不在 = hreflang 全部被忽略）
- canonical 与 hreflang 冲突时 canonical 优先
- canonical/hreflang/sitemap 三者协议域名必须一致（全 https + 同域变体）
- 分页语言页：每页自引用 canonical（❌ 第 2+ 页 canonical 到第 1 页）

### 多语言 sitemap 与 URL 结构
- `<urlset>` 带 `xmlns:xhtml`；每个 `<url>` 含所有语言（含自身）的 `<xhtml:link>`；含 x-default；URL 全绝对
- ⚠️ Next.js 坑：`alternates.languages` **不会**自动为 `<loc>` 加自引用 `<xhtml:link>`，必须手动加当前语言
- URL 结构推荐：子目录（`/en/`、`/zh/`）> 子域/ccTLD > ❌ URL 参数（`?lang=en`）
- 所有语言页加语言前缀（URL 隐藏语言会让 Google 无法区分版本）；根 URL 用 x-default（重定向或直接服务默认语言）
- ❌ IP/Accept-Language 内容协商（Googlebot 从美国 IP 无 Accept-Language 头，会被绕晕）
- GSC International Targeting 报告已废弃；地理定向靠 hreflang + 内容信号 + 链接模式

### 多语言内容质量
- AI 翻译本身不算 spam（Google 2025 立场），但**规模化低质翻译**会触发 scaled content abuse
- 全部内容翻译（title/desc/标题/正文），只翻模板壳子 = 制造重复内容
- 薄语言页会拖累整站 helpful content 信号——不能做出真有用的语言页就别做
- 检查 GSC "Duplicate, Google chose different canonical"

## 3. 页面级（快速抽样，深查走 page/on-page.md）
抽查首页 + 3-5 代表页：title 唯一性、description 唯一性、H1 数量（🟠 常见 12 个 H1 / 0 个 H1，见 on-page.md）、canonical、正文长度与关键词覆盖。

## 3.5 分站点类型常见问题（按站点类型定向排查）

| 站点类型 | 重点排查 |
|---------|---------|
| SaaS/产品官网 | 产品页内容薄；博客与产品页脱节；缺对比/替代页；feature 页无内容；缺术语表/教育内容 |
| 电商/知识店铺 | 分类页内容薄；商品描述重复；缺 Product schema；分面导航制造重复；缺货页处理不当 |
| 博客/内容站 | 旧内容未刷新；关键词自相残杀（cannibalization）；无主题聚类；内链差；缺作者页 |
| 多语言站 | 见 2.5 节 hreflang/canonical 全套 |
| 本地商家 | NAP（名称/地址/电话）不一致；缺 LocalBusiness schema；GBP 未优化；缺位置页；无本地内容 |

## 4-5. 内容质量与权威（深查走 content-quality.md）
抽样标记：作者/来源/更新日期是否存在（E-E-A-T）；外链反链概览（可用第三方工具或让用户提供 Ahrefs/SEMrush 截图）。

## audit 报告模板（五要素：每条问题 = Issue/Impact/Evidence/Fix/Priority）

```markdown
# <域名> SEO 审计报告（日期）
## 执行摘要
- 整体健康度评估（一句话）
- Top 3-5 优先问题
- 快速胜利项（低投入高回报）

## 🔴 高危（阻断索引/访问）
1. **Issue 问题**：<一句话描述>
   - Impact 影响：<High/Medium/Low + 为什么>
   - Evidence 证据：<实测：状态码/抓取结果/文件内容>
   - Fix 修复：<具体方法，按技术栈>
   - Verify 验证：<怎么确认修好>
## 🟠 中危（明显扣分）
## 🟡 优化项 / AI 红利
## ✅ 做得好
## 待人工实测（浏览器项）
- CWV：PageSpeed Insights 链接
- JS 注入 schema：浏览器复核
## 修复优先级行动计划
1. Critical（阻断索引/排名的必修项）
2. High-impact（高影响改进）
3. Quick wins（低投入立即收益）
4. Long-term（长期建议）
```

## 免费/付费工具清单

免费：Google Search Console（必备）、PageSpeed Insights、Rich Results Test（schema 验证，**渲染 JS**）、Mobile-Friendly Test、Schema Validator、Bing Webmaster Tools。
付费（如有）：Screaming Frog（渲染 JS）、Ahrefs/Semrush、Sitebulb、ContentKing。
