---
name: openclaw-astro-blog
description: automate publishing posts for the user's astro koharu blog on the same server. use when the user asks to publish, draft, generate, classify, tag, or build markdown blog posts for /www/wwwroot/www.wanziyoo.com, especially requests like 发布博客, 写一篇博客, 生成博客文章, 自动打标签, ai 分类, or opencalw/openclaw blog posting.
---

# OpenClaw Astro Blog

## Purpose

Use this skill to help publish Markdown posts for the Astro Koharu blog located at `/www/wwwroot/www.wanziyoo.com`.

This skill defines the blog directory, frontmatter format, AI tagging/classification rules, safe file-operation limits, and build workflow.

## Required reference

Before creating or modifying a post, read `references/blog-publish-rules.md` and follow it strictly.

## Workflow

1. Parse the user's request into title, body, draft intent, optional tags, optional category, and optional cover.
2. If the user did not provide tags, generate 2 to 5 concise tags using the rules in the reference file.
3. If the user did not provide a category, choose one category using the classification rules in the reference file.
4. Generate a lowercase English slug for the Markdown filename.
5. Create the Markdown file only under `/www/wwwroot/www.wanziyoo.com/src/content/blog/` or a subfolder below it.
6. Do not overwrite an existing file. If the target filename exists, append a date or numeric suffix.
7. Write complete YAML frontmatter and Markdown body.
8. Run `cd /www/wwwroot/www.wanziyoo.com && pnpm build` after creating formal posts.
9. If the build fails, report the error and do not restart services or perform extra deployment actions.
10. Return the title, file path, category, tags, build result, and publish status.

## Safety limits

Do not read, print, modify, or move secrets such as `.env`, private keys, tokens, database passwords, or server credentials.

Do not delete existing posts, theme source code, configuration files, `node_modules`, or system files unless the user explicitly asks and the operation is clearly safe.

Only run commands needed for this workflow. The default allowed command is:

```bash
cd /www/wwwroot/www.wanziyoo.com && pnpm build
```

## Output format

After a publish attempt, respond in Chinese using this structure:

```text
文章标题：...
文件路径：...
自动分类：...
自动标签：...
构建结果：成功/失败
是否发布成功：是/否
```
