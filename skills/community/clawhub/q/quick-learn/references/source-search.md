# Authoritative Source Search Strategy / 权威资料搜索策略

> Search queries use English for technical topics (better results), user's language for non-technical topics.

## Search Dimension Priority

### 1. Official Documentation (⭐⭐⭐) / 官方文档
- **Query**: `{topic} documentation site:official-domain` or `{topic} docs`
- **Verify**: URL must be official domain or official GitHub org
- **Recency**: Check doc version, ensure current stable / 检查版本号

### 2. Authoritative Tutorials/Books (⭐⭐⭐) / 权威教程
- **Query**: `{topic} tutorial OR guide OR "getting started" 2024..2026`
- **Priority**: Well-known authors, high-star GitHub repos, reputable platforms
- **Recency**: < 2 years, or explicitly compatible with latest version
- **Authority**: Check author background (official team / renowned developer / professor)

### 3. Well-Known Tech Communities (⭐⭐) / 知名技术社区
- **EN query**: `{topic} in-depth OR deep-dive OR "best practices"`
- **ZH query**: `{topic} 深入 OR 实践 OR 踩坑`
- **Platforms**: freeCodeCamp, MDN, Dev.to, Hacker News, 掘金 (high upvotes), 少数派
- Posts must have clear author, high engagement / 明确作者、高互动

### 4. Community Curated/Roadmap (⭐⭐) / 社区精选
- **Query**: `awesome {topic}` / `{topic} roadmap 2024` / `{topic} learn path`

### 5. Video/Audio (⭐⭐) / 视频音频
- **Query**: `{topic} tutorial video` / `{topic} course playlist`
- Priority: YouTube/Bilibili official channels, well-known creators
- Upload date < 1 year (tech updates fast)

### 6. Papers/Deep Articles (⭐) / 论文深度文章
- **Query**: `{topic} survey OR paper OR review` — advanced users only

## Authority Verification Checklist

- [ ] Credible source: Official / reputable community / 署名专家
- [ ] Publication date: Within 2 years (classics OK with version note) / 2 年内
- [ ] Completeness: Not a snippet, summary, or ad / 不是片段/摘要/广告
- [ ] No outdated info: Check versions, deprecated APIs / 检查版本号、已废弃 API
- [ ] Appropriate format: Article/video/doc/podcast matching user needs

**Verification methods**:
1. Fetch page, check headers (author, date, version) / 抓取页面检查头部信息
2. Official docs: check URL domain (e.g. `react.dev` not random blog) / 检查域名
3. GitHub repos: check last commit time / 检查最后提交时间
4. Tech blogs: check comments for "outdated" warnings / 检查评论区过时提示

## Rejected Sources (Blacklist) / 拒绝来源

- ❌ Unsigned repost/aggregator accounts / 无署名搬运号
- ❌ 3+ years unchanged for fast-iterating tech / 超过 3 年未更新的快速迭代技术
- ❌ Marketing content (selling products/courses) / 营销软文
- ❌ Poor-quality machine translations / 机翻文章
- ❌ Forum posts with zero replies, zero upvotes / 零回复零点赞帖子

## Search Fallback

If a dimension lacks results: expand terms (remove year constraints) → try synonyms → use English terms for authoritative content → lower quality threshold once (max), never recommend clearly outdated content.
