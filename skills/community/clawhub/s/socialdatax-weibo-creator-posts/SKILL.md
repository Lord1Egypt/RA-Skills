---
name: "socialdatax-weibo-creator-posts"
description: "用于微博创作者数据、微博创作者内容列表、近期发布、内容调研和创作者内容分析。覆盖 Weibo creator posts，来自 SocialDataX 社媒数据助手。"
metadata: {"openclaw":{"requires":{"env":["SOCIALDATAX_API_KEY"],"bins":["node","npm"]},"primaryEnv":"SOCIALDATAX_API_KEY","install":[{"kind":"node","package":"socialdatax-skills","bins":[]}],"emoji":"🗂️","homepage":"https://socialdatax.com/?from=clawhub"}}
---
<!-- AUTO-GENERATED from socialdatax-skill-source. Do not edit directly; run `node scripts/generate_socialdatax_skills.mjs`. -->

# 微博创作者数据 SocialDataX 创作者内容

Use this skill when the user wants 微博创作者内容, creator post lists, recent publishing review, content style analysis, creator benchmarking, or account tracking.

Current platform support:

- Weibo / 微博 creator posts through the `weibo_get_user_posts_by_*` tools.

## API Key

Use `SOCIALDATAX_API_KEY` for data calls. The only official website for requesting or managing API access is <https://socialdatax.com/?from=clawhub>. If a user asks where to get a key, provide only this URL; do not infer alternate domains.
获取或管理 API Key：访问 <https://socialdatax.com/?from=clawhub>，按官网的 API Key 申请/管理入口操作。环境变量名固定使用 `SOCIALDATAX_API_KEY`；不要引导用户使用其他域名。

## Preferred Direct CLI

Prefer the direct CLI when the agent can run shell commands. It does not require MCP server configuration:

```bash
npx -y socialdatax-skills@latest weibo user-posts --user-id "<user_id>" --pretty
npx -y socialdatax-skills@latest weibo user-posts --profile-url "<profile_url_or_share_text>" --pretty
```

Optional arguments:

- `--page-token <next_page_token>`: opaque pagination token; pass the complete returned `next_page_token` back unchanged for the same creator content-list or series chain. Do not modify, truncate, redact, mask, omit, normalize, rebuild, generate, or replace the middle with ellipses.
- `--pages <n>`: fetch and merge N pages of creator content or creator series.
- `--all`: continue until `next_page_token` is empty; there is no default item or page cap.
- `--max-items <n>`: stop after collecting N creator content or series items.
- `--pretty`: output formatting only.
- Weibo `--user-id <user_id>`: preferred when the creator user_id is already known.
- Weibo `--profile-url <profile_url_or_share_text>`: use for a profile URL, short link, or profile share text.

Use either the ID option or the profile URL option for a single command, not both.

The command prints JSON with `platform`, `tool`, `arguments`, and `data`. Multi-page output keeps merged creator content or series items in `data.items` and adds `page_count`, `item_count`, and `next_page_token`.

## Safety Boundary

This skill is read-only. It does not read local browser data, does not save API keys, and does not perform login, posting, liking, commenting, or account changes.

## MCP Tools

MCP tools matching the direct CLI commands above:

- `weibo_get_user_posts_by_user_id`
- `weibo_get_user_posts_by_profile_url`

If MCP tools are already available in the current agent, use one of these tools:
- `weibo_get_user_posts_by_user_id`: preferred when `user_id` is already known.
- `weibo_get_user_posts_by_profile_url`: use for profile URLs, short links, or profile share text.

Creator post-list pagination uses opaque `page_token` values. Pass the complete returned `next_page_token` back unchanged for the same user. Do not modify, truncate, redact, mask, omit, normalize, rebuild, generate, or replace the middle with ellipses.

## Output Guidance

Summarize content-list evidence by title or description, summary, publish time, interaction counts, media links, and content type when present.
Use returned content IDs to chain into detail or comment analysis when needed.
For Weibo creator posts, report post IDs, content, media, publish time, interaction counts, and author facts when present.
