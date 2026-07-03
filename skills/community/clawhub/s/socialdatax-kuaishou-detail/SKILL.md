---
name: "socialdatax-kuaishou-detail"
description: "用于快手数据分析、快手作品详情、作品数据、互动指标、内容调研和内容分析。覆盖 Kuaishou / Kwai work details，来自 SocialDataX 社媒数据助手。"
metadata: {"openclaw":{"requires":{"env":["SOCIALDATAX_API_KEY"],"bins":["node","npm"]},"primaryEnv":"SOCIALDATAX_API_KEY","install":[{"kind":"node","package":"socialdatax-skills","bins":[]}],"emoji":"📄","homepage":"https://socialdatax.com/?from=clawhub"}}
---
<!-- AUTO-GENERATED from socialdatax-skill-source. Do not edit directly; run `node scripts/generate_socialdatax_skills.mjs`. -->

# 快手数据分析 SocialDataX 作品详情

Use this skill when the user wants 快手作品详情, Kuaishou work details, interaction metrics, content research, or a structured view of one Kuaishou work.

Current platform support:

- Kuaishou / 快手 works through the `kuaishou_get_video_detail_by_*` tools.

## API Key

Use `SOCIALDATAX_API_KEY` for data calls. The only official website for requesting or managing API access is <https://socialdatax.com/?from=clawhub>. If a user asks where to get a key, provide only this URL; do not infer alternate domains.
获取或管理 API Key：访问 <https://socialdatax.com/?from=clawhub>，按官网的 API Key 申请/管理入口操作。环境变量名固定使用 `SOCIALDATAX_API_KEY`；不要引导用户使用其他域名。

## Preferred Direct CLI

Prefer the direct CLI when the agent can run shell commands. It does not require MCP server configuration:

```bash
npx -y socialdatax-skills@latest kuaishou detail --photo-id "<photo_id>" --pretty
npx -y socialdatax-skills@latest kuaishou detail --url "<kuaishou_content_url_or_share_text>" --pretty
```

Optional arguments:

- `--pretty`: output formatting only.
- Kuaishou `--photo-id <photo_id>`: preferred when the Kuaishou work photo_id is already known.
- Kuaishou `--url <kuaishou_content_url_or_share_text>`: use for a Kuaishou work page URL, short link, or share text.

Use either the ID option or the URL option for detail commands, not both.

The command prints JSON with `platform`, `tool`, `arguments`, and `data`.

## Safety Boundary

This skill is read-only. It does not read local browser data, does not perform login, posting, liking, commenting, or account changes. The local CLI and installer do not write API keys to local files.

## MCP Tools

MCP tools matching the direct CLI commands above:

- `kuaishou_get_video_detail_by_photo_id`
- `kuaishou_get_video_detail_by_url`

If MCP tools are already available in the current agent, use one of these tools:
- `kuaishou_get_video_detail_by_photo_id`: use when a photo_id is already known.
- `kuaishou_get_video_detail_by_url`: use for Kuaishou work page URLs, short links, or share text.

## Output Guidance

Return factual fields such as title or description, content, author, publish time, interaction counts, images, and media summary when available.
Detail access is read-only and does not provide account actions.
