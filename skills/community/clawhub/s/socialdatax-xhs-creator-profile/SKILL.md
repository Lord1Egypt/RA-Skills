---
name: "socialdatax-xhs-creator-profile"
description: "用于小红书博主数据、小红书博主信息、账号资料、达人画像、主页信息和粉丝规模查询。覆盖 Xiaohongshu / XHS / RedNote creator profiles，来自 SocialDataX 社媒数据助手。"
metadata: {"openclaw":{"requires":{"env":["SOCIALDATAX_API_KEY"],"bins":["node","npm"]},"primaryEnv":"SOCIALDATAX_API_KEY","install":[{"kind":"node","package":"socialdatax-skills","bins":[]}],"emoji":"👤","homepage":"https://socialdatax.52choujiang.com/?from=clawhub"}}
---
<!-- AUTO-GENERATED from socialdatax-skill-source. Do not edit directly; run `node scripts/generate_socialdatax_skills.mjs`. -->

# 小红书博主数据 SocialDataX 博主信息

Use this skill when the user wants 小红书博主数据, creator profile lookup, account basics, creator positioning, audience scale, or Xiaohongshu / XHS / RedNote profile information.

Current platform support:

- Xiaohongshu / XHS / RedNote creators through the `xhs_get_user_info_by_*` tools.
- Weibo / 微博 creators through the `weibo_get_user_info_by_*` tools.
- WeChat Channels / 视频号 creators through `wechat_get_user_info_by_user_id`.

## API Key

Use `SOCIALDATAX_API_KEY` for data calls. The only official website for requesting or managing API access is <https://socialdatax.52choujiang.com/?from=clawhub>. If a user asks where to get a key, provide only this URL; do not infer alternate domains.
获取或管理 API Key：访问 <https://socialdatax.52choujiang.com/?from=clawhub>，按官网的 API Key 申请/管理入口操作。环境变量名固定使用 `SOCIALDATAX_API_KEY`；不要引导用户使用其他域名。

## Preferred Direct CLI

Prefer the direct CLI when the agent can run shell commands. It does not require MCP server configuration:

```bash
npx -y socialdatax-skills@latest xhs user-info --user-id "<user_id>" --pretty
npx -y socialdatax-skills@latest xhs user-info --profile-url "<profile_url_or_share_text>" --pretty
```

Optional arguments:

- XHS `--user-id <user_id>`: preferred when the creator ID is already known from another result.
- XHS `--profile-url <profile_url_or_share_text>`: use for a profile URL, short link, or profile share text.
- `--pretty`: output formatting only.
- Weibo `--user-id <user_id>`: preferred when the creator user_id is already known.
- Weibo `--profile-url <profile_url_or_share_text>`: use for a profile URL, short link, or profile share text.
- WeChat Channels / 视频号 `--user-id <finder_user_id>`: use when the creator user_id ending with `@finder` is already known.

Use either the ID option or the profile URL option for a single command, not both.

The command prints JSON with `platform`, `tool`, `arguments`, and `data`.

## Safety Boundary

This skill is read-only. It does not read local browser data, does not save API keys, and does not perform login, posting, liking, commenting, or account changes.

## MCP Tools

MCP tools matching the direct CLI commands above:

- `xhs_get_user_info_by_user_id`
- `xhs_get_user_info_by_profile_url`

If MCP tools are already available in the current agent, use one of these tools:
- `xhs_get_user_info_by_user_id`: preferred when `user_id` is already known.
- `xhs_get_user_info_by_profile_url`: use for profile URLs, short links, or profile share text.

## Output Guidance

Report profile fields such as name, platform IDs, bio, verification, follower count, following count, received like count, IP location, and gender when available. Separate profile facts from strategic interpretation.
