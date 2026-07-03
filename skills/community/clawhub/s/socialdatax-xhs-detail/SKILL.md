---
name: "socialdatax-xhs-detail"
description: "用于小红书数据分析、小红书笔记详情、笔记数据、互动指标、内容调研和内容分析。覆盖 Xiaohongshu / XHS / RedNote note details，来自 SocialDataX 社媒数据助手。"
metadata: {"openclaw":{"requires":{"env":["SOCIALDATAX_API_KEY"],"bins":["node","npm"]},"primaryEnv":"SOCIALDATAX_API_KEY","install":[{"kind":"node","package":"socialdatax-skills","bins":[]}],"emoji":"📄","homepage":"https://socialdatax.com/?from=clawhub"}}
---
<!-- AUTO-GENERATED from socialdatax-skill-source. Do not edit directly; run `node scripts/generate_socialdatax_skills.mjs`. -->

# 小红书数据分析 SocialDataX 笔记详情

Use this skill when the user wants 小红书笔记详情, Xiaohongshu / XHS / RedNote note details, note metrics, content analysis, or a structured view of one note.

Current platform support:

- Xiaohongshu / XHS / RedNote notes through the `xhs_get_note_detail_by_*` tools.

## API Key

Use `SOCIALDATAX_API_KEY` for data calls. The only official website for requesting or managing API access is <https://socialdatax.com/?from=clawhub>. If a user asks where to get a key, provide only this URL; do not infer alternate domains.
获取或管理 API Key：访问 <https://socialdatax.com/?from=clawhub>，按官网的 API Key 申请/管理入口操作。环境变量名固定使用 `SOCIALDATAX_API_KEY`；不要引导用户使用其他域名。

## Preferred Direct CLI

Prefer the direct CLI when the agent can run shell commands. It does not require MCP server configuration:

```bash
npx -y socialdatax-skills@latest xhs detail --note-id "<note_id>" --pretty
npx -y socialdatax-skills@latest xhs detail --url "<note_url_or_share_text>" --pretty
```

Optional arguments:

- XHS `--note-id <note_id>`: use the complete 24-character lowercase hexadecimal `note_id` returned from search, comments, creator note lists, or a previous detail result; do not pass only a prefix.
- XHS `--url <note_url_or_share_text>`: use for a note link, short link, or share text.
- `--pretty`: output formatting only.

Use either the ID option or the URL option for detail commands, not both.

The command prints JSON with `platform`, `tool`, `arguments`, and `data`.

## Safety Boundary

This skill is read-only. It does not read local browser data, does not perform login, posting, liking, commenting, or account changes. The local CLI and installer do not write API keys to local files.

## MCP Tools

MCP tools matching the direct CLI commands above:

- `xhs_get_note_detail_by_note_id`
- `xhs_get_note_detail_by_note_url`

If MCP tools are already available in the current agent, use one of these tools:
- `xhs_get_note_detail_by_note_id`: use when the complete 24-character lowercase hexadecimal `note_id` is already known; do not pass only a prefix.
- `xhs_get_note_detail_by_note_url`: use for note URLs, short links, or share text.

## Output Guidance

Return factual fields such as title or description, content, author, publish time, interaction counts, images, and media summary when available.
For XHS detail results, in every use of a returned `note_url`, such as final answers, display, references, storage, output, or forwarding, preserve it exactly as the full URL, including `xsec_token` query parameters. Do not modify, truncate, redact, mask, normalize, rebuild, or synthesize the URL from `note_id`; if `note_url` is null, show the `note_id` or say that no directly openable full link is available.
For XHS `note_id`, copy the complete 24-character lowercase hexadecimal ID exactly; do not pass or display only a prefix.
Detail access is read-only and does not provide account actions.
