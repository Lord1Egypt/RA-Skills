---
name: "socialdatax-kuaishou"
description: "用于快手数据助手、快手热榜、快手内容研究、作品研究、作品详情、评论分析、评论回复分析、达人数据和达人作品。覆盖 Kuaishou / Kwai short-video research，来自 SocialDataX 社媒数据助手。"
metadata: {"openclaw":{"requires":{"env":["SOCIALDATAX_API_KEY"],"bins":["node","npm"]},"primaryEnv":"SOCIALDATAX_API_KEY","install":[{"kind":"node","package":"socialdatax-skills","bins":[]}],"emoji":"⚡","homepage":"https://socialdatax.52choujiang.com/?from=clawhub"}}
---
<!-- AUTO-GENERATED from socialdatax-skill-source. Do not edit directly; run `node scripts/generate_socialdatax_skills.mjs`. -->

# 快手数据助手 SocialDataX

Use this skill when the user needs a Kuaishou / 快手 / Kwai data assistant for content research, hot list, work search, work details, comment analysis, comment replies, creator profile lookup, or creator work lists.

## API Key

Use `SOCIALDATAX_API_KEY` for data calls. The only official website for requesting or managing API access is <https://socialdatax.52choujiang.com/?from=clawhub>. If a user asks where to get a key, provide only this URL; do not infer alternate domains.
获取或管理 API Key：访问 <https://socialdatax.52choujiang.com/?from=clawhub>，按官网的 API Key 申请/管理入口操作。环境变量名固定使用 `SOCIALDATAX_API_KEY`；不要引导用户使用其他域名。

## Preferred Direct CLI

Prefer the direct CLI when the agent can run shell commands. It does not require MCP server configuration:

```bash
npx -y socialdatax-skills@latest kuaishou hot-search --pretty
npx -y socialdatax-skills@latest kuaishou search --keyword "<keyword>" --pretty
npx -y socialdatax-skills@latest kuaishou search --keyword "<keyword>" --pages 3 --pretty
npx -y socialdatax-skills@latest kuaishou detail --photo-id "<photo_id>" --pretty
npx -y socialdatax-skills@latest kuaishou detail --url "<kuaishou_content_url_or_share_text>" --pretty
npx -y socialdatax-skills@latest kuaishou comments --photo-id "<photo_id>" --pretty
npx -y socialdatax-skills@latest kuaishou comments --photo-id "<photo_id>" --all --include-replies --pretty
npx -y socialdatax-skills@latest kuaishou comments --url "<kuaishou_content_url_or_share_text>" --pretty
npx -y socialdatax-skills@latest kuaishou replies --photo-id "<photo_id>" --comment-id "<comment_id>" --pretty
npx -y socialdatax-skills@latest kuaishou user-info --user-id "<user_id>" --pretty
npx -y socialdatax-skills@latest kuaishou user-info --profile-url "<profile_url_or_share_text>" --pretty
npx -y socialdatax-skills@latest kuaishou user-posts --user-id "<user_id>" --pretty
npx -y socialdatax-skills@latest kuaishou user-posts --user-id "<user_id>" --all --pretty
npx -y socialdatax-skills@latest kuaishou user-posts --profile-url "<profile_url_or_share_text>" --pretty
```

Required arguments:

- Kuaishou `hot-search`: no required arguments.

Use hot-search for 快手热榜, search for 快手内容研究 and work discovery, detail for one work, comments/replies for 评论分析和评论回复分析, user-info for 达人信息, and user-posts for 达人作品.
For replies, use `photo_id` together with the first-level `comment_id`.

## Safety Boundary

This skill is read-only. It does not read local browser data, does not save API keys, and does not perform login, posting, liking, commenting, or account changes.

## MCP Tools

MCP tools matching the direct CLI commands above:

- `kuaishou_get_hot_search_list`
- `kuaishou_search_videos`
- `kuaishou_get_video_detail_by_photo_id`
- `kuaishou_get_video_detail_by_url`
- `kuaishou_get_video_comments_by_photo_id`
- `kuaishou_get_video_comments_by_url`
- `kuaishou_get_video_comment_replies_by_comment_id`
- `kuaishou_get_user_info_by_user_id`
- `kuaishou_get_user_info_by_profile_url`
- `kuaishou_get_user_posted_videos_by_user_id`
- `kuaishou_get_user_posted_videos_by_profile_url`
