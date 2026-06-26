# Astro Koharu Blog Publish Rules

## Project paths

Project root:

```text
/www/wwwroot/www.wanziyoo.com
```

Article directory:

```text
/www/wwwroot/www.wanziyoo.com/src/content/blog/
```

All posts must be created in `src/content/blog/` or a subdirectory below it.

## Allowed operations

Allowed:

- Create new Markdown posts.
- Generate frontmatter.
- Generate Chinese descriptions.
- Generate tags.
- Choose categories.
- Run the production build.

Not allowed:

- Delete existing posts.
- Overwrite existing posts.
- Modify theme source code.
- Modify config files unless the user explicitly asks.
- Read or reveal `.env`, tokens, private keys, passwords, or credentials.
- Modify `node_modules`.
- Execute unrelated system commands.

## Publish triggers

Treat these as publish or draft requests:

```text
发布博客：标题 + 内容
写一篇博客：标题 + 内容
帮我发一篇文章：标题 + 内容
生成博客文章：标题 + 内容
保存草稿：标题 + 内容
```

Extract:

- title
- body
- draft intent
- optional tags
- optional category
- optional cover

## File naming rules

Markdown filenames must be:

- lowercase English
- hyphen-separated
- no spaces
- no Chinese characters
- no special symbols except hyphen
- `.md` extension

Example:

```text
how-to-use-openclaw-to-auto-publish-blog.md
```

For Chinese titles, translate to a short English slug. If translation is uncertain, use pinyin or stable keywords.

If a file exists, never overwrite it. Append a suffix:

```text
how-to-use-openclaw.md
how-to-use-openclaw-20260506.md
how-to-use-openclaw-2.md
```

## Frontmatter

Every post must include:

```yaml
---
title: 文章标题
date: 2026-05-06 12:00:00
description: 文章摘要
tags:
  - 标签1
  - 标签2
categories:
  - 分类
draft: false
---
```

Date format:

```text
YYYY-MM-DD HH:mm:ss
```

Formal posts:

```yaml
draft: false
```

Drafts:

```yaml
draft: true
```

Use draft mode when the user says:

```text
先保存
先不要发布
草稿
待修改
以后再发
```

## Description rules

If the user did not provide `description`, generate one.

Requirements:

- Chinese
- 30 to 80 Chinese characters
- summarize the core article topic
- no marketing exaggeration
- no Markdown syntax

Example:

```yaml
description: 本文介绍如何在 Astro Koharu 博客中接入 OpenClaw，实现 Markdown 文章的自动生成、分类、构建和发布。
```

## AI tag rules

If the user did not provide tags, generate 2 to 5 tags.

Requirements:

- Chinese preferred, but keep product/framework names in English
- short and specific
- each tag should be 2 to 8 Chinese characters when Chinese
- maximum 5 tags
- avoid broad filler tags such as 文章, 内容, 分享, 想法
- avoid duplicate meanings

Recommended tag pool:

```text
Astro
博客
自动化
OpenClaw
服务器
前端
后端
部署
Linux
教程
工具
笔记
生活
随笔
AI
效率
编程
学习
折腾
网站
Nginx
Docker
PM2
宝塔
安全
资源
```

Example:

```yaml
tags:
  - Astro
  - OpenClaw
  - 自动化
  - 博客
```

## AI category rules

If the user did not provide categories, choose one main category.

Default category list:

```text
技术
教程
工具
笔记
生活
随笔
AI
前端
后端
部署
服务器
安全
资源
```

Classification guide:

- Astro, Vue, React, CSS, JavaScript, blog themes -> 前端
- Linux, Nginx, 宝塔, server, PM2, Docker -> 服务器 or 部署
- OpenClaw, ChatGPT, AI tools, automated writing -> AI or 工具
- Step-by-step instructions or configuration guides -> 教程
- Learning records, troubleshooting, knowledge organization -> 笔记
- Daily records or personal reflections -> 生活 or 随笔
- Software links, resource collections, recommendations -> 资源
- Accounts, permissions, secrets, hardening, vulnerabilities -> 安全

Priority:

1. Use the user's explicit category.
2. Use the most relevant category from the article topic.
3. If uncertain, use `笔记`.

Default single category:

```yaml
categories:
  - 教程
```

Multi-level categories are allowed only when useful or explicitly requested:

```yaml
categories:
  - [技术, 前端, Astro]
```

## Body rules

The article body must use Markdown.

Requirements:

- Start content headings at `##`, not `#`.
- Do not repeat the title as an H1 in the body.
- Use clear sections.
- Use lists and code blocks where helpful.
- Technical tutorials must include necessary commands.
- Commands must be fenced code blocks.
- Do not invent nonexistent commands, files, or paths.
- Do not expose private server details.

## Cover rules

If the user did not provide a cover, omit the `cover` field.

If the user provides a cover, use a site-accessible URL path:

Correct:

```yaml
cover: /img/cover/openclaw.webp
```

Incorrect:

```yaml
cover: /www/wwwroot/www.wanziyoo.com/public/img/cover/openclaw.webp
```

## Build rules

After creating a formal post, run:

```bash
cd /www/wwwroot/www.wanziyoo.com && pnpm build
```

If the user is creating multiple posts at once, create all posts first, then run one build.

If build succeeds, report success.

If build fails, report failure and the error. Do not restart services or run extra deployment commands.

## Static deployment notes

This blog is an Astro static site.

- Source Markdown remains in `src/content/blog/`.
- Build output is generated into `dist/`.
- `pnpm build` regenerates static pages.
- Normal builds do not endlessly accumulate old generated pages.
- If Nginx serves `dist/`, a successful build usually does not require a service restart.

Do not remove `dist/` unless the user explicitly asks.

## Final response template

Return:

```text
文章标题：...
文件路径：...
自动分类：...
自动标签：...
构建结果：成功/失败
是否发布成功：是/否
```
