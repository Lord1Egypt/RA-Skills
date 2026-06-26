# Content Engine / 内容引擎

> Cross-platform content creation and distribution tool — the FIRST WeChat Official Account integration on ClawHub!
>
> 跨平台内容创作与分发工具 — ClawHub 首个支持微信公众号集成的内容引擎！

---

## Features / 功能亮点

- **Multi-platform Distribution / 多平台分发** — Write once, publish everywhere: Twitter, LinkedIn, WeChat Official Account, Blog (Hugo/Jekyll/Hexo), Medium
- **WeChat OA Integration / 微信公众号集成** — The FIRST skill on ClawHub to support WeChat Official Account publishing, including article formatting, author cards, and rich text
- **Smart Adaptation / 智能适配** — Automatically adapts content to each platform's format, character limits, and best practices
- **Self-Learning Engine / 自学习引擎** — Learn from content performance to continuously improve: topic suggestions, optimal posting times, engagement analysis
- **Obsidian Integration / Obsidian 集成** — Import drafts directly from your Obsidian vault, bidirectional sync, wikilinks and tags conversion
- **AI Image Prompter / AI 配图助手** — Generate AI image prompts (Midjourney/DALL-E/SD style) for your content, with platform-specific sizing and SEO alt text
- **Content Calendar / 内容日历** — Plan, schedule, and visualize your content pipeline with Mermaid Gantt charts
- **Performance Metrics / 数据指标** — Collect and compare engagement metrics across all platforms with learning-based insights
- **Markdown Native / Markdown 原生** — Create content in Markdown, import/export with YAML frontmatter support
- **Local Data / 本地数据** — All data stored locally, nothing leaves your environment

---

## Version Comparison / 版本对比

| Feature / 功能 | Free / 免费版 | Paid / 付费版 ¥99/月 |
|------|:------:|:------------:|
| Content limit / 内容上限 | 20 | 500 |
| Platforms / 平台数 | 2 | 5 (all / 全部) |
| Create & Edit / 创建编辑 | ✅ | ✅ |
| Basic Adaptation / 基础适配 | ✅ | ✅ |
| Markdown Import/Export / 导入导出 | ✅ | ✅ |
| AI Image Prompts / AI 配图提示词 | ✅ | ✅ |
| Obsidian Import / Obsidian 导入 | ✅ | ✅ |
| Auto Publish / 自动发布 | ❌ | ✅ |
| WeChat OA / 微信公众号 | ❌ | ✅ |
| Batch Adapt / 批量适配 | ❌ | ✅ |
| Scheduled Publish / 定时发布 | ❌ | ✅ |
| Metrics Collection / 指标采集 | ❌ | ✅ |
| Self-Learning Engine / 自学习引擎 | ❌ | ✅ |
| Learning Insights / 学习洞察 | ❌ | ✅ |
| Obsidian Bidirectional Sync / 双向同步 | ❌ | ✅ |
| Content Calendar / 内容日历 | ❌ | ✅ |
| Mermaid Charts / 可视化图表 | ❌ | ✅ |

---

## Quick Start / 快速开始

### 1. Install / 安装

Search `content-engine` on ClawHub and install, or use CLI:

在 ClawHub 搜索 `content-engine` 并安装，或使用命令行：

```bash
openclaw skill install content-engine
```

### 2. Configure Platforms / 配置平台

Set environment variables for the platforms you want to use:

配置你要使用的平台环境变量：

```bash
# Twitter
export CE_TWITTER_BEARER_TOKEN="your-bearer-token"

# LinkedIn
export CE_LINKEDIN_ACCESS_TOKEN="your-access-token"

# WeChat Official Account / 微信公众号
export CE_WECHAT_APPID="your-appid"
export CE_WECHAT_SECRET="your-appsecret"

# Medium
export CE_MEDIUM_TOKEN="your-integration-token"

# Blog (Hugo/Jekyll/Hexo)
export CE_BLOG_TYPE="hugo"
export CE_BLOG_PATH="/path/to/your/blog"

# Obsidian Vault / Obsidian 笔记库
export CE_OBSIDIAN_VAULT_PATH="~/MyVault"

# Subscription / 订阅等级
export CE_SUBSCRIPTION_TIER="paid"
```

### 3. Create & Publish / 创建并发布

```bash
# Create content / 创建内容
/content-engine create "My Article Title" --platforms twitter,linkedin,wechat

# Adapt to platforms / 适配到各平台
/content-engine adapt CT... --platform twitter

# Preview before publishing / 发布前预览
/content-engine preview CT... --platform wechat

# Publish / 发布
/content-engine publish CT... --platform twitter
```

### 4. Track Performance / 追踪表现

```bash
# Collect metrics / 采集指标
/content-engine metrics CT...

# View content calendar / 查看内容日历
/content-engine calendar week
```

---

## Example / 使用示例

### Content Creation Workflow / 内容创作工作流

```
User: 帮我创建一篇关于 AI 编程助手的文章，发布到 Twitter 和微信公众号

Agent: 好的，我来帮你创建内容...
       [创建内容，生成 Twitter thread 和微信公众号 HTML 文章]
       [展示各平台预览]
       [获得确认后发布]

User: 查看这篇文章在各平台的表现

Agent: 正在采集指标数据...
       Twitter: 128 点赞, 45 转发, 12 回复, 5,230 曝光
       微信公众号: 2,340 阅读, 89 分享, 156 收藏
       [生成对比图表]
```

---

## Supported Platforms / 支持的平台

| Platform / 平台 | Format / 格式 | Key Feature / 核心特性 |
|------|------|------|
| Twitter / X | Thread (280 chars/tweet) | Auto-split, hashtags, CJK char counting |
| LinkedIn | Professional post (3000 chars) | Professional tone, structured format |
| WeChat OA / 微信公众号 | HTML article | Rich text, author card, image refs |
| Blog | Markdown + frontmatter | Hugo, Jekyll, Hexo support |
| Medium | Markdown | Medium-compatible format, 5 tags |

---

## FAQ / 常见问题

### Q1: Is this really the first WeChat integration on ClawHub? / 这真的是 ClawHub 首个微信集成吗？

Yes! content-engine is the first OpenClaw skill to support WeChat Official Account API integration, enabling direct article publishing from the CLI.

是的！content-engine 是首个支持微信公众号 API 集成的 OpenClaw Skill，可以直接从命令行发布文章到公众号。

### Q2: Do I need all platform tokens configured? / 需要配置所有平台的 Token 吗？

No. Only configure the platforms you plan to use. Content creation and adaptation work without any tokens — tokens are only needed for publishing.

不需要。只配置你计划使用的平台即可。内容创建和适配不需要任何 Token — Token 仅在发布时需要。

### Q3: Is my data uploaded to the cloud? / 数据会上传到云端吗？

No. All content data is stored locally in `~/.openclaw-bdi/content-engine/`. API calls are made directly from your machine to each platform.

不会。所有内容数据存储在本地 `~/.openclaw-bdi/content-engine/`。API 调用从你的机器直接发送到各平台。

### Q4: How does the Chinese character counting work for Twitter? / Twitter 的中文字符计数怎么算？

Twitter counts CJK characters as 2 character positions. content-engine automatically handles this when splitting content into threads.

Twitter 将中日韩字符计为 2 个字符位。content-engine 在拆分 thread 时会自动处理这个规则。

### Q5: Can I use the free version for WeChat? / 免费版能用微信公众号吗？

WeChat Official Account integration is a paid feature. Free users can create and adapt content, but publishing to WeChat requires the paid tier (¥99/month).

微信公众号集成是付费功能。免费用户可以创建和适配内容，但发布到微信需要付费版（¥99/月）。

### Q6: What blog engines are supported? / 支持哪些博客引擎？

Hugo, Jekyll, and Hexo. Set `CE_BLOG_TYPE` to your engine type, and `CE_BLOG_PATH` to your blog project root. content-engine generates properly formatted Markdown with the correct frontmatter.

支持 Hugo、Jekyll 和 Hexo。设置 `CE_BLOG_TYPE` 为你的引擎类型，`CE_BLOG_PATH` 为博客项目根目录。content-engine 会生成正确格式的 Markdown 和 frontmatter。

---

## Technical Support / 技术支持

- **Docs / 文档**: See `references/` directory for platform specs and WeChat guide
- **Issues / 问题反馈**: Submit on ClawHub skill page
- **Community / 社区讨论**: Join `#content-engine` channel on ClawHub
- **Email / 邮件**: skill-support@clawhub.dev

---

*content-engine v1.1.0 | Compatible with OpenClaw 0.5+ | First WeChat OA integration on ClawHub*
