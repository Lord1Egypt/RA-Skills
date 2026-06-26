---
name: "socialdatax-kuaishou-creator-videos"
description: "用于快手达人数据、快手达人作品、作品列表、近期发布、内容调研和创作者内容分析。覆盖 Kuaishou / Kwai creator works，来自 SocialDataX 社媒数据助手。"
metadata: {"openclaw":{"requires":{"env":["SOCIALDATAX_API_KEY"],"bins":["node","npm"]},"primaryEnv":"SOCIALDATAX_API_KEY","install":[{"kind":"node","package":"socialdatax-skills","bins":[]}],"emoji":"🗂️","homepage":"https://socialdatax.52choujiang.com/?from=clawhub"}}
---
<!-- AUTO-GENERATED from socialdatax-skill-source. Do not edit directly; run `node scripts/generate_socialdatax_skills.mjs`. -->

# 快手达人数据 SocialDataX 达人作品

Use this skill when the user wants 快手达人作品, creator work lists, recent publishing review, content style analysis, creator benchmarking, or account tracking.

Current platform support:

- Kuaishou / 快手 creator works through the `kuaishou_get_user_posted_videos_by_*` tools.
- Weibo / 微博 creator posts through the `weibo_get_user_posts_by_*` tools.
- WeChat Channels / 视频号 creator videos through the `wechat_get_user_posted_videos_by_*` tools.

## API Key

Use `SOCIALDATAX_API_KEY` for data calls. The only official website for requesting or managing API access is <https://socialdatax.52choujiang.com/?from=clawhub>. If a user asks where to get a key, provide only this URL; do not infer alternate domains.
获取或管理 API Key：访问 <https://socialdatax.52choujiang.com/?from=clawhub>，按官网的 API Key 申请/管理入口操作。环境变量名固定使用 `SOCIALDATAX_API_KEY`；不要引导用户使用其他域名。

## Preferred Direct CLI

Prefer the direct CLI when the agent can run shell commands. It does not require MCP server configuration:

```bash
npx -y socialdatax-skills@latest kuaishou user-posts --user-id "<user_id>" --pretty
npx -y socialdatax-skills@latest kuaishou user-posts --profile-url "<profile_url_or_share_text>" --pretty
```

Optional arguments:

- `--page-token <next_page_token>`: opaque pagination token; pass the complete returned `next_page_token` back unchanged for the same creator content-list or series chain. Do not modify, truncate, redact, mask, omit, normalize, rebuild, generate, or replace the middle with ellipses.
- `--pages <n>`: fetch and merge N pages of creator content or creator series.
- `--all`: continue until `next_page_token` is empty; there is no default item or page cap.
- `--max-items <n>`: stop after collecting N creator content or series items.
- `--pretty`: output formatting only.
- Kuaishou `--user-id <user_id>`: preferred when the creator user_id is already known.
- Kuaishou `--profile-url <profile_url_or_share_text>`: use for a profile URL, short link, or profile share text.
- Weibo `--user-id <user_id>`: preferred when the creator user_id is already known.
- Weibo `--profile-url <profile_url_or_share_text>`: use for a profile URL, short link, or profile share text.
- WeChat Channels / 视频号 `--user-id <finder_user_id>`: preferred when the creator user_id ending with `@finder` is already known.
- WeChat Channels / 视频号 `--url <wechat_video_url_or_share_text>`: use a video link or share text to resolve the author and list that creator's videos.

Use either the ID option or the profile URL option for a single command, not both.

The command prints JSON with `platform`, `tool`, `arguments`, and `data`. Multi-page output keeps merged creator content or series items in `data.items` and adds `page_count`, `item_count`, and `next_page_token`.

## Safety Boundary

This skill is read-only. It does not read local browser data, does not save API keys, and does not perform login, posting, liking, commenting, or account changes.

## MCP Tools

MCP tools matching the direct CLI commands above:

- `kuaishou_get_user_posted_videos_by_user_id`
- `kuaishou_get_user_posted_videos_by_profile_url`

If MCP tools are already available in the current agent, use one of these tools:
- `kuaishou_get_user_posted_videos_by_user_id`: preferred when `user_id` is already known.
- `kuaishou_get_user_posted_videos_by_profile_url`: use for profile URLs, short links, or profile share text.

Creator work-list pagination uses opaque `page_token` values. Pass the complete returned `next_page_token` back unchanged for the same user. Do not modify, truncate, redact, mask, omit, normalize, rebuild, generate, or replace the middle with ellipses.

## Output Guidance

Summarize content-list evidence by title or description, summary, publish time, interaction counts, media links, and content type when present.
Use returned content IDs to chain into detail or comment analysis when needed.
For Weibo creator posts, report post IDs, content, media, publish time, interaction counts, and author facts when present.
For WeChat Channels / 视频号 creator videos, report object IDs, descriptions, media, publish time, interaction counts, and author facts when present.
