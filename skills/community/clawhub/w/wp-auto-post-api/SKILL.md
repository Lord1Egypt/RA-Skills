---
name: wp-seo-publisher
description: Publish SEO-optimized articles to WordPress via REST API with RankMath meta fields
env_vars:
  - WP_SITE_URL
  - WP_USERNAME
  - WP_APP_PASSWORD
  - WP_CATEGORY_ID
credentials:
  - type: wordpress_app_password
    description: WordPress Application Password with edit_posts capability. Grants REST API access to create posts and manage tags as the configured user.
---

# WordPress SEO Publisher

通过 WordPress REST API 发布 SEO 优化文章，自动设置 RankMath Free 版 meta fields（SEO 标题、描述、焦点关键词）。

## Requirements

- `python3`（无需额外 pip 依赖，仅使用标准库）
- WordPress 已安装 RankMath SEO Free
- WordPress 已创建 Application Password
- WordPress `functions.php` 中已注册 RankMath meta keys（见下方 WordPress 配置）

## Directory Structure

```
scripts/
├── publish_wp_article.py       # 主发布脚本
docs/
├── wordpress-setup.php         # functions.php 代码片段（需手动添加到 WordPress）
```

## Environment Variables

在 `~/.openclaw/workspace-marketing/.env` 中配置：

```env
WP_SITE_URL=https://你的域名
WP_USERNAME=WordPress用户名
WP_APP_PASSWORD=xxxx xxxx xxxx xxxx xxxx xxxx
WP_CATEGORY_ID=Articles分类的ID
```

## 执行方式

```bash
cd ~/.openclaw/workspace-marketing
export $(cat .env | grep "^WP_" | xargs)
python3 skills/wp-seo-publisher/scripts/publish_wp_article.py '<json_data>'
```

## JSON 参数定义

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `title` | String | ✅ | 文章标题（含关键词，50-60 字符） |
| `content` | String | ✅ | 文章 HTML 正文（使用 H2/H3 结构） |
| `excerpt` | String | 推荐 | 文章摘要，也用作默认 meta description |
| `slug` | String | 推荐 | SEO 友好的 URL（英文、连字符分隔） |
| `focus_keyword` | String | 推荐 | RankMath 焦点关键词 |
| `seo_title` | String | 否 | 自定义 SEO 标题（留空则用 title） |
| `seo_description` | String | 否 | 自定义 meta description（留空则用 excerpt） |
| `tags` | Array | 否 | 标签名称列表（不存在的 tag 会自动创建） |
| `category_id` | Number | 否 | 分类 ID（留空则用 .env 中的默认值） |
| `status` | String | 否 | `publish` 或 `draft`（默认 `draft`） |

## RankMath 免费版自动处理的 SEO 功能

以下功能 RankMath 会根据文章内容**自动处理**，无需通过 API 额外设置：

| 功能 | 说明 |
|------|------|
| XML Sitemap | 新文章自动加入 sitemap，加速搜索引擎收录 |
| Canonical URL | 自动生成，防止重复内容问题 |
| Open Graph Tags | 自动生成 og:title、og:description、og:image |
| Twitter Cards | 自动生成社交分享卡片 |
| Article Schema | 自动添加 Article 结构化数据 |
| Meta Robots | 默认 index, follow |
| Breadcrumbs | 自动生成（需在 RankMath 设置中启用） |

## 通过 API 主动设置的字段（3 个）

| Meta Key | 对应 JSON 字段 | 作用 |
|----------|---------------|------|
| `rank_math_title` | `seo_title` 或 `title` | 搜索结果中显示的标题 |
| `rank_math_description` | `seo_description` 或 `excerpt` | 搜索结果中显示的描述 |
| `rank_math_focus_keyword` | `focus_keyword` | RankMath 内容评分的焦点关键词 |

## AI Agent 发布工作流

> **注意**：
> - 关键词挖掘阶段已独立，必须委托给 `seo-keyword-researcher` Skill 处理。
> - 文章撰写与排版阶段已独立，必须委托给 `seo-content-writer` Skill 处理。
>
> **本 Skill (`wp-seo-publisher`) 仅负责「API 发布」与「日志记录」。**

1. **读取输入 (Input)**：前往目录 `~/.openclaw/workspace-marketing/seo/seo_articles/`，寻找并读取**最新时间戳**且尚未发布的 JSON 文件（例如 `2026-05-06_110000.json`）。
2. **人工确认 (Approval Gate)**：向用户展示即将发布的文章标题、slug 和 status，**必须等待用户明确确认后**才执行发布。如果用户未指定 `status: "publish"`，默认以 `draft` 模式发布。
3. **执行发布 (Execute)**：将该 JSON 文件的内容作为参数，传递给 Python 脚本：
   `python3 skills/wp-seo-publisher/scripts/publish_wp_article.py '<读取到的 JSON 内容>'`
4. **标记与记录 (Clean up)**：
   - **防重复机制**：发布成功后，**必须**将该 JSON 文件重命名，加上 `_published` 后缀（例如执行 `mv 2026-05-06_110000.json 2026-05-06_110000_published.json`）。
   - **更新日志**：将发布成功的结果与 URL 追加写入 `memory/wp-articles-log.md`。此日志**仅用于**本 Skill 的防重复检查和发布审计，不应被其他 Skill 用作数据输入源。

### JSON 组装范例

```json
{
  "title": "Top 5 Benefits of Renting Robots for Corporate Events",
  "content": "<h2>Why More Companies Are Choosing Robot Rental</h2><p>In today's competitive event landscape...</p><h2>1. Cost Efficiency</h2><p>Purchasing a service robot can cost...</p><h2>2. Professional Setup & Support</h2><p>When you rent from a professional provider...</p><h2>3. Cutting-Edge Technology</h2><p>Robot technology evolves rapidly...</p><h2>4. Wow Factor for Guests</h2><p>Nothing captures attention quite like...</p><h2>5. Flexibility and Variety</h2><p>Different events call for different robots...</p><h2>Ready to Elevate Your Next Event?</h2><p>Contact us today for a free consultation and quote. <a href='https://example.com/contact'>Get in touch →</a></p>",
  "excerpt": "Discover the top 5 reasons why renting robots for corporate events saves money, impresses guests, and delivers cutting-edge experiences.",
  "slug": "benefits-renting-robots-corporate-events",
  "focus_keyword": "renting robots for corporate events",
  "seo_title": "Top 5 Benefits of Renting Robots for Corporate Events | Your Company",
  "seo_description": "Discover the top 5 reasons why renting robots for corporate events saves money, impresses guests, and delivers cutting-edge experiences.",
  "tags": ["robot rental", "corporate events", "service robots", "event technology"],
  "status": "draft"
}
```

### 发布记录格式（memory/wp-articles-log.md）

```markdown
## 2026-05-07
- **Title**: Top 5 Benefits of Renting Robots for Corporate Events
- **URL**: https://example.com/benefits-renting-robots-corporate-events/
- **Focus Keyword**: renting robots for corporate events
- **Tags**: robot rental, corporate events, service robots, event technology
- **Status**: published
```

## 主题库（Agent 轮换使用）

1. Robot rental benefits for businesses
2. Industry applications: hospitality
3. Industry applications: retail
4. Industry applications: events & exhibitions
5. Industry applications: healthcare
6. Industry applications: education
7. Event planning with service robots
8. Robot technology trends and innovations
9. FAQ: robot rental process, pricing, setup
10. Cost analysis: buying vs renting robots
11. Customer engagement with robots
12. Future of service robotics in Hong Kong
13. How to choose the right robot for your event
14. Robot safety and insurance considerations
15. Success stories: robots at corporate events

## WordPress 配置（一次性设置）

### 必要步骤

1. **安装 RankMath Free** → Plugins → Add New → 搜索 Rank Math SEO
2. **创建 Application Password** → Users → Profile → Application Passwords
3. **注册 meta keys** → 将 `docs/wordpress-setup.php` 中的代码添加到主题 `functions.php`
4. **记录分类 ID** → Posts → Categories → 找到 Articles 的 ID

## 返回值

成功时输出：
```
✅ Article published successfully!
  Post ID:        123
  URL:            https://example.com/your-article-slug/
  Status:         publish
  Focus Keyword:  your keyword

__RESULT_JSON__:{"success":true,"post_id":123,"url":"...","status":"publish",...}
```

失败时返回非零退出码，并输出错误信息。

## 注意事项

1. 首次使用建议用 `status: "draft"` 测试，在 WordPress 后台确认 RankMath 数据正确
2. 确保 WordPress 启用 HTTPS，否则 Application Password 不安全
3. 文章内容必须有实质价值，不要生成低质量 SEO spam
4. 每篇文章的 slug 必须唯一，避免冲突
5. focus_keyword 应与文章主题一致，这会影响 RankMath 的内容评分
