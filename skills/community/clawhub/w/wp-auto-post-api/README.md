# WordPress SEO Publisher

通过 WordPress REST API 发布 SEO 优化文章，自动设置 [RankMath](https://rankmath.com/) Free 版 meta fields（SEO 标题、描述、焦点关键词）。

Publish SEO-optimized articles to WordPress via REST API, with automatic [RankMath](https://rankmath.com/) Free meta field support (SEO title, description, focus keyword).

---

- **零依赖 / Zero dependencies** — 仅使用 Python 3 标准库 / uses only Python 3 standard library
- **RankMath 集成 / RankMath integration** — 通过 API 设置 SEO 标题、meta 描述、焦点关键词 / sets SEO title, meta description, and focus keyword via API
- **标签管理 / Tag management** — 自动创建不存在的标签 / auto-creates tags that don't exist yet
- **Agent 友好 / Agent-friendly** — 结构化 JSON 输出，便于下游自动化 / structured JSON output for downstream automation

> 🌐 **For English-speaking users**: The [`SKILL.md`](SKILL.md) file (agent workflow instructions) is written in Chinese. You can ask your AI agent to translate it to English before use.
>
> 🌐 **英语用户提示**：[`SKILL.md`](SKILL.md)（Agent 工作流指令）以中文编写。你可以让你的 AI Agent 将其翻译为英文后使用。

## 快速开始 / Quick Start

### 前置条件 / Prerequisites

- Python 3.6+
- 已启用 HTTPS 的 WordPress 站点 / A WordPress site with HTTPS enabled
- 已安装并激活 [RankMath SEO](https://rankmath.com/) Free 插件 / [RankMath SEO](https://rankmath.com/) Free plugin installed and activated

### 步骤 1：克隆仓库 / Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/wp-seo-publisher.git
```

### 步骤 2：配置 WordPress（一次性设置）/ Step 2: Configure WordPress (One-Time Setup)

你需要在 WordPress 后台完成 **3 个手动步骤**：

You need to perform **3 manual steps** in your WordPress admin panel:

#### 2a. 创建 Application Password / Create an Application Password

1. 进入 **Users → Profile** / Go to **Users → Profile**
2. 下滑到 **Application Passwords** / Scroll down to **Application Passwords**
3. 输入名称（如 `seo-publisher`），点击 **Add New Application Password** / Enter a name (e.g. `seo-publisher`) and click **Add New Application Password**
4. **立即复制生成的密码** — 之后不会再显示 / **Copy the generated password immediately** — it won't be shown again
5. 密码格式形如：`xxxx xxxx xxxx xxxx xxxx xxxx` / The password format looks like: `xxxx xxxx xxxx xxxx xxxx xxxx`

#### 2b. 为 REST API 注册 RankMath Meta Keys / Register RankMath Meta Keys for REST API

默认情况下 RankMath 的 meta 字段不会通过 REST API 暴露，你需要手动注册：

By default, RankMath meta fields are not exposed via the REST API. You need to register them:

1. 进入 **Appearance → Theme File Editor**（建议使用子主题）/ Go to **Appearance → Theme File Editor** (use a child theme if available)
2. 打开当前激活主题的 `functions.php` / Open your active theme's `functions.php`
3. 将 [`docs/wordpress-setup.php`](docs/wordpress-setup.php) 中的内容粘贴到文件末尾 / Paste the contents of [`docs/wordpress-setup.php`](docs/wordpress-setup.php) at the end of the file
4. 点击 **Update File** / Click **Update File**

> **替代方案 / Alternative**：使用 [Code Snippets](https://wordpress.org/plugins/code-snippets/) 插件来管理此代码，无需直接修改主题文件。/ Use the [Code Snippets](https://wordpress.org/plugins/code-snippets/) plugin to add this code without editing theme files directly.

#### 2c. 查找分类 ID / Find Your Category ID

1. 进入 **Posts → Categories** / Go to **Posts → Categories**
2. 鼠标悬停在目标分类上（如 "Articles"）/ Hover over the category you want to use (e.g. "Articles")
3. 查看浏览器状态栏中的 URL，找到 `tag_ID=XX` / Look at the URL in your browser's status bar — find `tag_ID=XX`
4. 记下这个数字，填入 `.env` 文件 / Note down this number for your `.env` file

### 步骤 3：配置环境变量 / Step 3: Configure Environment Variables

```bash
cp .env.example .env
```

用你的实际信息编辑 `.env` / Edit `.env` with your actual values:

```env
WP_SITE_URL=https://your-domain.com
WP_USERNAME=your_wordpress_username
WP_APP_PASSWORD=xxxx xxxx xxxx xxxx xxxx xxxx
WP_CATEGORY_ID=5
```

> 详见 [`.env.example`](.env.example) 中每个变量的说明。/ See [`.env.example`](.env.example) for detailed descriptions of each variable.

### 步骤 4：用草稿测试 / Step 4: Test with a Draft Post

加载环境变量并发布一篇测试草稿：

Load environment variables and publish a test draft:

```bash
export $(cat .env | grep "^WP_" | xargs)

python3 scripts/publish_wp_article.py '{
  "title": "Test Article — Please Delete",
  "content": "<h2>Hello World</h2><p>This is a test post from wp-seo-publisher.</p>",
  "excerpt": "A test article to verify the publishing pipeline.",
  "slug": "test-wp-seo-publisher",
  "focus_keyword": "test article",
  "status": "draft"
}'
```

成功后你会看到 / If successful, you'll see:

```
✅ Article published successfully!
  Post ID:        123
  URL:            https://your-domain.com/test-wp-seo-publisher/
  Status:         draft
  Focus Keyword:  test article
```

前往 WordPress 后台 → **Posts** 确认草稿已出现且 RankMath SEO 数据正确，然后删除它。

Go to your WordPress admin → **Posts** to verify the draft appears with correct RankMath SEO data, then delete it.

## 使用方法 / Usage

### JSON 参数 / JSON Parameters

| 字段 / Field | 类型 / Type | 必填 / Required | 说明 / Description |
|-------|------|----------|-------------|
| `title` | String | ✅ | 文章标题（含关键词，50-60 字符）/ Article title (include keyword, 50-60 chars) |
| `content` | String | ✅ | HTML 正文（使用 H2/H3 结构）/ HTML body (use H2/H3 structure for SEO) |
| `excerpt` | String | 推荐 / Recommended | 摘要，也用作默认 meta description / Summary, also used as default meta description |
| `slug` | String | 推荐 / Recommended | SEO 友好 URL（小写、连字符分隔）/ SEO-friendly URL (lowercase, hyphen-separated) |
| `focus_keyword` | String | 推荐 / Recommended | RankMath 焦点关键词 / RankMath focus keyword for content scoring |
| `seo_title` | String | 否 / Optional | 自定义 SEO 标题（默认用 title）/ Custom SEO title (defaults to `title`) |
| `seo_description` | String | 否 / Optional | 自定义 meta description（默认用 excerpt）/ Custom meta description (defaults to `excerpt`) |
| `tags` | Array | 否 / Optional | 标签名称列表（自动创建不存在的标签）/ Tag name strings (auto-created if not exist) |
| `category_id` | Number | 否 / Optional | 分类 ID（默认用 `.env` 中的值）/ Category ID (defaults to `WP_CATEGORY_ID`) |
| `status` | String | 否 / Optional | `publish` 或 `draft`（默认 `draft`）/ `publish` or `draft` (default: `draft`) |

### 通过 API 设置的 RankMath Meta 字段 / RankMath Meta Fields Set via API

| Meta Key | 来源 / Source | 用途 / Purpose |
|----------|--------|---------|
| `rank_math_title` | `seo_title` 或 `title` | 搜索结果中显示的标题 / Title shown in search results |
| `rank_math_description` | `seo_description` 或 `excerpt` | 搜索结果中显示的描述 / Description shown in search results |
| `rank_math_focus_keyword` | `focus_keyword` | RankMath 内容评分焦点关键词 / Focus keyword for RankMath content scoring |

### 完整示例 / Full Example

```bash
export $(cat .env | grep "^WP_" | xargs)

python3 scripts/publish_wp_article.py '{
  "title": "Top 5 Benefits of Renting Robots for Corporate Events",
  "content": "<h2>Why More Companies Are Choosing Robot Rental</h2><p>In today'\''s competitive event landscape...</p>",
  "excerpt": "Discover the top 5 reasons why renting robots saves money and impresses guests.",
  "slug": "benefits-renting-robots-corporate-events",
  "focus_keyword": "renting robots for corporate events",
  "seo_title": "Top 5 Benefits of Renting Robots for Corporate Events",
  "seo_description": "Discover the top 5 reasons why renting robots saves money and impresses guests.",
  "tags": ["robot rental", "corporate events", "service robots"],
  "status": "draft"
}'
```

## 作为 OpenClaw Skill 使用 / Using as an OpenClaw Skill

本仓库可作为 [OpenClaw](https://github.com/openclaw/openclaw) Agent Skill 安装：

This repository can be installed as an [OpenClaw](https://github.com/openclaw/openclaw) agent skill:

1. 克隆到工作区 skills 目录 / Clone into your workspace skills directory:
   ```bash
   cd ~/.openclaw/workspace-marketing/skills
   git clone https://github.com/YOUR_USERNAME/wp-seo-publisher.git
   ```

2. 在工作区根目录配置 `.env` / Configure `.env` in your workspace root:
   ```bash
   cp skills/wp-seo-publisher/.env.example ~/.openclaw/workspace-marketing/.env
   # 编辑 .env 填入你的实际凭据 / Edit .env with your actual credentials
   ```

3. Agent 将遵循 [`SKILL.md`](SKILL.md) 中定义的工作流。/ The agent will follow the workflow defined in [`SKILL.md`](SKILL.md).

## 注意事项 / Notes

- **首次使用请用 `"status": "draft"` 测试** — 在 WordPress 后台确认 RankMath 数据正确 / **Always test with `"status": "draft"` first** to verify RankMath data in WordPress admin
- **必须启用 HTTPS** — Application Password 在 HTTP 下不安全 / **HTTPS is required** — Application Passwords are not secure over plain HTTP
- 每篇文章的 `slug` 必须唯一，避免 URL 冲突 / Each article's `slug` must be unique to avoid URL conflicts
- `focus_keyword` 会直接影响 RankMath 的内容评分 / `focus_keyword` directly affects RankMath's content scoring in the WordPress editor
