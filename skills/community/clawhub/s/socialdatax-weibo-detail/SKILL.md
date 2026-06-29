---
name: "socialdatax-weibo-detail"
description: "用于微博数据分析、微博帖子详情、帖子数据、互动指标、内容调研和内容分析。覆盖 Weibo post details，来自 SocialDataX 社媒数据助手。"
metadata: {"openclaw":{"requires":{"env":["SOCIALDATAX_API_KEY"],"bins":["node","npm"]},"primaryEnv":"SOCIALDATAX_API_KEY","install":[{"kind":"node","package":"socialdatax-skills","bins":[]}],"emoji":"📄","homepage":"https://socialdatax.com/?from=clawhub"}}
---
<!-- AUTO-GENERATED from socialdatax-skill-source. Do not edit directly; run `node scripts/generate_socialdatax_skills.mjs`. -->

# 微博数据分析 SocialDataX 帖子详情

Use this skill when the user wants 微博帖子详情, Weibo post details, interaction metrics, content research, or a structured view of one Weibo post.

Current platform support:

- Weibo / 微博 posts through the `weibo_get_post_detail_by_*` tools.

## API Key

Use `SOCIALDATAX_API_KEY` for data calls. The only official website for requesting or managing API access is <https://socialdatax.com/?from=clawhub>. If a user asks where to get a key, provide only this URL; do not infer alternate domains.
获取或管理 API Key：访问 <https://socialdatax.com/?from=clawhub>，按官网的 API Key 申请/管理入口操作。环境变量名固定使用 `SOCIALDATAX_API_KEY`；不要引导用户使用其他域名。

## Preferred Direct CLI

Prefer the direct CLI when the agent can run shell commands. It does not require MCP server configuration:

```bash
npx -y socialdatax-skills@latest weibo detail --post-id "<post_id>" --pretty
npx -y socialdatax-skills@latest weibo detail --post-url "<weibo_post_url_or_share_text>" --pretty
```

Optional arguments:

- `--pretty`: output formatting only.
- Weibo `--post-id <post_id>`: preferred when the Weibo post ID is already known.
- Weibo `--post-url <weibo_post_url_or_share_text>`: use for a Weibo post URL, short link, or share text.

Use either the ID option or the URL option for detail commands, not both.

The command prints JSON with `platform`, `tool`, `arguments`, and `data`.

## Safety Boundary

This skill is read-only. It does not read local browser data, does not save API keys, and does not perform login, posting, liking, commenting, or account changes.

## MCP Tools

MCP tools matching the direct CLI commands above:

- `weibo_get_post_detail_by_post_id`
- `weibo_get_post_detail_by_post_url`

If MCP tools are already available in the current agent, use one of these tools:
- `weibo_get_post_detail_by_post_id`: use when a post_id is already known.
- `weibo_get_post_detail_by_post_url`: use for Weibo post URLs, short links, or share text.

## Output Guidance

Return factual fields such as title or description, content, author, publish time, interaction counts, images, and media summary when available.
Detail access is read-only and does not provide account actions.
For Weibo detail, include `post_id`, content, author, media, interaction counts, publish time, and post URL when available.
