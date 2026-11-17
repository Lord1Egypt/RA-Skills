# references/schema.md — 结构化数据深度清单（schema 子流程用）

> 检测方法 → 常用类型模板 → 生成落地 → 验证。分级同主文件。
> 要点提炼自 marketingskills `seo-audit` v2.0.1 / `ai-seo` v2.4.0 schema 部分（2026-09 对照原文核查）。

> 🌐 语言 / Language：本清单是**内容规范**而非语言约束；默认中文，用户用英文或其他语言提问时就用该语言输出（答案语言跟随用户）。
> This checklist is a content spec, not a language mandate — answer in the user's language.

## 1. 检测方法（⚠️ 反坑必读）

**错误姿势**：`curl`/`web_fetch` 抓 HTML 后 grep `application/ld+json` → 判"无 schema"。
**为什么错**：多数 CMS/框架（Halo 插件、Next.js 部分方案、GTM）在**客户端 JS 注入** JSON-LD，静态抓取永远漏报。实测三站静态抓 JSON-LD = 0，但浏览器渲染后才算数。

**正确姿势**：
1. 浏览器渲染页面
2. 执行 `document.querySelectorAll('script[type="application/ld+json"]')`
3. 逐个 `JSON.parse`，记录 @type 与关键属性
4. 或直接丢 Google Rich Results Test（https://search.google.com/test/rich-results）→ 输入 URL，它用真实渲染验证

**区分**：GSC 的"增强功能"报告能看 Google 实际识别到的 schema（最权威，但需权限）。

## 2. 常用类型与模板

### Organization（全站，放每页或首页）
```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "小遥AI",
  "url": "https://project.xiaoyaosai.com",
  "logo": "https://project.xiaoyaosai.com/logo.png",
  "sameAs": [
    "https://space.bilibili.com/xxx",
    "https://github.com/dtsola"
  ]
}
```

### WebSite + SearchAction（站内搜索框富媒体）
```json
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "dtsola 的博客",
  "url": "https://www.dtsola.com",
  "potentialAction": {
    "@type": "SearchAction",
    "target": "https://www.dtsola.com/search?q={search_term_string}",
    "query-input": "required name=search_term_string"
  }
}
```

### Article / BlogPosting（文章页，必做）
```json
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "文章标题",
  "description": "meta description",
  "datePublished": "2026-09-01T10:00:00+08:00",
  "dateModified": "2026-09-01T10:00:00+08:00",
  "author": { "@type": "Person", "name": "dtsola", "url": "https://www.dtsola.com/about" },
  "publisher": { "@type": "Organization", "name": "dtsola", "logo": { "@type": "ImageObject", "url": "https://www.dtsola.com/logo.png" } },
  "mainEntityOfPage": "https://www.dtsola.com/post/xxx",
  "image": "https://www.dtsola.com/cover.png"
}
```

### FAQPage（AI 引用 + 精选摘要双红利）
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "小遥Claw 支持哪些模型？",
      "acceptedAnswer": { "@type": "Answer", "text": "支持 Claude、DeepSeek、MiniMax 等主流模型，可在设置中配置 API Key。" }
    }
  ]
}
```
⚠️ FAQ 内容必须与页面可见文本一致（页面要有对应问答区块），隐藏 FAQ 违反政策。

### Product + Offer（电商/知识店铺商品页）
```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "SEO 技能包",
  "image": "https://www.landoo.me/img/seo-skill.png",
  "description": "描述",
  "offers": {
    "@type": "Offer",
    "price": "49.00",
    "priceCurrency": "CNY",
    "availability": "https://schema.org/InStock",
    "url": "https://www.landoo.me/p/seo-skill"
  }
}
```

### BreadcrumbList（面包屑，全站通用）
```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "首页", "item": "https://www.dtsola.com" },
    { "@type": "ListItem", "position": 2, "name": "分类", "item": "https://www.dtsola.com/category/tech" },
    { "@type": "ListItem", "position": 3, "name": "文章" }
  ]
}
```

### Person / HowTo（可选）
- Person：作者页/关于页（author 信号）
- HowTo：教程步骤（注意 Google 2023 起收缩 HowTo 富媒体展示，价值下降，可不优先）

## 3. 生成与落地（按技术栈）

| 技术栈 | 落地方式 |
|--------|---------|
| Next.js App Router | `app/layout.tsx` 加 Organization/WebSite；文章页在 generateMetadata 或页面组件注入 JSON-LD（`<script type="application/ld+json" dangerouslySetInnerHTML>`）；或 next-seo |
| Halo 2.x | 主题模板 `<head>` 注入（主题支持自定义代码则直接加）；或 SEO 插件 |
| 静态站 | 每页 `<head>` 手写；或构建脚本统一注入（改模板一次全站生效） |

⚠️ 落地点选择原则：**能模板化就不手写**（手写 100 页 = 维护灾难）；生成后抽查 3-5 页。

## 4. 验证

> ⚠️ **隐私提醒（外部校验前必读）**：下面第 1、2 项会把**站点 URL 或你粘贴的 schema 代码**
> 发送给第三方（第 1 项 Google、第 2 项 Schema.org）。提交前请：① 告知用户会发给谁、发什么；
> ② 征得同意；③ **不要**提交内网地址、带 token/签名的预览链接、未发布内容或敏感 markup；
> ④ 能本地判定的先本地判定（JSON 能否解析 + 必填字段齐全）。

1. **本地校验（优先，不外发）**：`JSON.parse` 能解析、必填字段（`@context` / `@type` / 关键属性）齐全、类型拼写正确
2. Rich Results Test（https://search.google.com/test/rich-results）：URL 检测可解析类型、报错警告（**会向 Google 提交 URL 或 markup**）
3. Schema.org 校验器（https://validator.schema.org）：贴代码验证语法（**会把粘贴的代码提交给 Schema.org**）
4. 浏览器渲染后 querySelectorAll 确认已注入
5. GSC 增强功能报告（有权限时）：看 Google 实收

判定：无法解析/报错 → 🔴（等于没加还可能有警告）；无富媒体资格类型（纯 Organization 类）→ 🟡（无害但红利有限）。

## 5. 红线

- ❌ 放页面没有的内容（假 Product/假 Review/隐藏 FAQ）→ 违反 Google 结构化数据政策，会被人工处理
- ❌ Review/AggregateRating 放无评价依据的页
- ⚠️ 多类型叠加时 @graph 数组包好，别写坏 JSON（Rich Results Test 能查）
