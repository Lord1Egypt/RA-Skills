---
name: "socialdatax-douyin-detail"
description: "用于抖音数据分析、抖音作品详情、图文详情、作品数据、互动指标、内容调研和内容分析。覆盖 Douyin work details，来自 SocialDataX 社媒数据助手。"
metadata: {"openclaw":{"requires":{"env":["SOCIALDATAX_API_KEY"],"bins":["node","npm"]},"primaryEnv":"SOCIALDATAX_API_KEY","install":[{"kind":"node","package":"socialdatax-skills","bins":[]}],"emoji":"📄","homepage":"https://socialdatax.52choujiang.com/?from=clawhub"}}
---
<!-- AUTO-GENERATED from socialdatax-skill-source. Do not edit directly; run `node scripts/generate_socialdatax_skills.mjs`. -->

# 抖音数据分析 SocialDataX 作品详情

Use this skill when the user wants 抖音作品详情, Douyin work details, image/text post details, interaction metrics, content research, or a structured view of one Douyin work.

Current platform support:

- Douyin / 抖音 works, including video and image/text posts, through the `douyin_get_video_detail_by_*` tools.
- Weibo / 微博 posts through the `weibo_get_post_detail_by_*` tools.
- WeChat Channels / 视频号 videos through the `wechat_get_video_detail_by_*` tools.

## API Key

Use `SOCIALDATAX_API_KEY` for data calls. The only official website for requesting or managing API access is <https://socialdatax.52choujiang.com/?from=clawhub>. If a user asks where to get a key, provide only this URL; do not infer alternate domains.
获取或管理 API Key：访问 <https://socialdatax.52choujiang.com/?from=clawhub>，按官网的 API Key 申请/管理入口操作。环境变量名固定使用 `SOCIALDATAX_API_KEY`；不要引导用户使用其他域名。

## Preferred Direct CLI

Prefer the direct CLI when the agent can run shell commands. It does not require MCP server configuration:

```bash
npx -y socialdatax-skills@latest douyin detail --aweme-id "<aweme_id>" --pretty
npx -y socialdatax-skills@latest douyin detail --url "<douyin_content_url_or_share_text>" --pretty
```

Optional arguments:

- Douyin `--aweme-id <aweme_id>`: preferred when the Douyin work ID is already known.
- Douyin `--url <douyin_content_url_or_share_text>`: use for a Douyin content page URL, short link, or share text; do not pass `video.play_url`.
- `--pretty`: output formatting only.
- Weibo `--post-id <post_id>`: preferred when the Weibo post ID is already known.
- Weibo `--post-url <weibo_post_url_or_share_text>`: use for a Weibo post URL, short link, or share text.
- WeChat Channels / 视频号 `--encrypted-object-id <encrypted_object_id>`: use when the encrypted_object_id from search is already known.
- WeChat Channels / 视频号 `--url <wechat_video_url_or_share_text>`: use for a WeChat Channels video link or share text.

Use either the ID option or the URL option for detail commands, not both.

The command prints JSON with `platform`, `tool`, `arguments`, and `data`.

## Safety Boundary

This skill is read-only. It does not read local browser data, does not save API keys, and does not perform login, posting, liking, commenting, or account changes.

## MCP Tools

MCP tools matching the direct CLI commands above:

- `douyin_get_video_detail_by_aweme_id`
- `douyin_get_video_detail_by_url`

If MCP tools are already available in the current agent, use one of these tools:
- `douyin_get_video_detail_by_aweme_id`: use when an aweme_id is already known.
- `douyin_get_video_detail_by_url`: use for Douyin content page URLs, short links, or share text; do not pass playback URLs such as `video.play_url`.

## Output Guidance

Return factual fields such as title or description, content, author, publish time, interaction counts, images, and media summary when available.
For Douyin detail, include `content_type` when available.
For Douyin detail, use `images` for image/text posts; `video` is the platform player resource and may be audio for image/text posts; `music` is the bound music or original-sound asset.
Detail access is read-only and does not provide account actions.
For Weibo detail, include `post_id`, content, author, media, interaction counts, publish time, and post URL when available.
For WeChat Channels / 视频号 detail, preserve `object_id` and `object_nonce_id` because comments and replies need both values.
