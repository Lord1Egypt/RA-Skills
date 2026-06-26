---
name: "socialdatax-douyin-comments"
description: "用于抖音评论分析、抖音评论回复、抖音评论洞察、用户反馈、口碑分析、痛点总结和内容讨论分析。覆盖 Douyin comments and comment replies，来自 SocialDataX 社媒数据助手。"
metadata: {"openclaw":{"requires":{"env":["SOCIALDATAX_API_KEY"],"bins":["node","npm"]},"primaryEnv":"SOCIALDATAX_API_KEY","install":[{"kind":"node","package":"socialdatax-skills","bins":[]}],"emoji":"💬","homepage":"https://socialdatax.52choujiang.com/?from=clawhub"}}
---
<!-- AUTO-GENERATED from socialdatax-skill-source. Do not edit directly; run `node scripts/generate_socialdatax_skills.mjs`. -->

# 抖音评论分析 SocialDataX 评论洞察

Use this skill when the user wants 抖音评论分析, Douyin / 抖音 first-level comments, comment replies, audience feedback, sentiment themes, objections, pain points, FAQ extraction, or discussion summaries.

Current platform support:

- Douyin / 抖音 works, including video and image/text posts, through the `douyin_get_video_comments_by_*` and `douyin_get_video_comment_replies_by_comment_id` tools.
- Weibo / 微博 posts through the `weibo_get_post_comments_by_*` and `weibo_get_post_comment_replies_by_comment_id` tools.
- WeChat Channels / 视频号 videos through the `wechat_get_video_comments_by_*` and `wechat_get_video_comment_replies_by_comment_id` tools.

## API Key

Use `SOCIALDATAX_API_KEY` for data calls. The only official website for requesting or managing API access is <https://socialdatax.52choujiang.com/?from=clawhub>. If a user asks where to get a key, provide only this URL; do not infer alternate domains.
获取或管理 API Key：访问 <https://socialdatax.52choujiang.com/?from=clawhub>，按官网的 API Key 申请/管理入口操作。环境变量名固定使用 `SOCIALDATAX_API_KEY`；不要引导用户使用其他域名。

## Preferred Direct CLI

Prefer the direct CLI when the agent can run shell commands. It does not require MCP server configuration:

```bash
npx -y socialdatax-skills@latest douyin comments --aweme-id "<aweme_id>" --pretty
npx -y socialdatax-skills@latest douyin comments --url "<douyin_content_url_or_share_text>" --pretty
npx -y socialdatax-skills@latest douyin replies --aweme-id "<aweme_id>" --comment-id "<comment_id>" --pretty
```

Optional arguments:

- Douyin `--aweme-id <aweme_id>`: preferred when the video ID is already known and should anchor the comment thread.
- `--url <url_or_share_text>`: use for a content page URL, short link, or share text for first-level comments.
- Douyin URL safety: do not pass `video.play_url`; use a Douyin content page URL, short link, or share text instead.
- `--comment-id <comment_id>`: required for reply commands; use the first-level comment ID under the same content item.
- `--page-token <next_page_token>`: opaque pagination token; pass the complete returned `next_page_token` back unchanged for the same content item or comment chain. Do not modify, truncate, redact, mask, omit, normalize, rebuild, generate, or replace the middle with ellipses.
- `--pages <n>`: fetch and merge N pages of first-level comments or replies.
- `--all`: continue first-level comments or replies until `next_page_token` is empty; there is no default item or page cap.
- `--max-items <n>`: stop after collecting N primary comments or replies.
- `--include-replies`: for first-level `comments` commands only, also fetch all second-level replies under each returned first-level comment.
- `--pretty`: output formatting only.
- Weibo `--post-id <post_id>`: preferred when the Weibo post ID is already known and should anchor the comment thread.
- Weibo `--post-url <weibo_post_url_or_share_text>`: use for a Weibo post URL, short link, or share text for first-level comments.
- WeChat Channels / 视频号 `--object-id <object_id>` and `--object-nonce-id <object_nonce_id>`: use together when both values are already known and should anchor the comment thread.
- WeChat Channels / 视频号 `--url <wechat_video_url_or_share_text>`: use for a WeChat Channels video link or share text for first-level comments.

Use either the content ID option or the URL option for first-level comments, not both. For reply commands, use the content ID together with `--comment-id`.

The command prints JSON with `platform`, `tool`, `arguments`, and `data`. Multi-page output keeps merged primary comments in `data.items` and adds `page_count`, `item_count`, and the next-page marker. With `--include-replies`, each first-level comment includes `replies`, `replies_page_count`, and `replies_next_page_token`.

## Safety Boundary

This skill is read-only. It does not read local browser data, does not save API keys, and does not perform login, posting, liking, commenting, or account changes.

## MCP Tools

MCP tools matching the direct CLI commands above:

- `douyin_get_video_comments_by_aweme_id`
- `douyin_get_video_comments_by_url`
- `douyin_get_video_comment_replies_by_comment_id`

If MCP tools are already available in the current agent, use one of these tools:
- `douyin_get_video_comments_by_aweme_id`: use when the aweme_id is known.
- `douyin_get_video_comments_by_url`: use for Douyin content page URLs, short links, or share text; do not pass playback URLs such as `video.play_url`.
- `douyin_get_video_comment_replies_by_comment_id`: use when both aweme_id and first-level comment ID are known; use page_token to continue pagination.

Comment pagination uses opaque `page_token` values. Pass the complete returned `next_page_token` back unchanged for the same content item or first-level comment chain. Do not modify, truncate, redact, mask, omit, normalize, rebuild, generate, or replace the middle with ellipses. Continue only when `next_page_token` is non-empty.

## Output Guidance

Group comments by observed themes before inferring sentiment or demand. Mention whether the result is one page or multiple pages. Empty comments can be a valid successful result.
For Douyin comment media, use `image_urls` for attached pictures. When `sticker` is present, `sticker.static_url` is a static preview when non-empty, and `sticker.animated_url` is the animated resource when non-empty.
For Weibo and WeChat Channels / 视频号 comments, preserve returned content IDs from first-level comments so reply commands can use the same content item and comment chain.
