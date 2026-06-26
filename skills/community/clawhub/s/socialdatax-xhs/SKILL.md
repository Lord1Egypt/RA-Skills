---
name: "socialdatax-xhs"
description: "用于小红书数据助手、小红书搜索热榜、小红书数据分析、小红书笔记搜索、笔记详情、评论分析、博主数据和博主笔记。覆盖 Xiaohongshu / XHS / RedNote，来自 SocialDataX 社媒数据助手。"
metadata: {"openclaw":{"requires":{"env":["SOCIALDATAX_API_KEY"],"bins":["node","npm"]},"primaryEnv":"SOCIALDATAX_API_KEY","install":[{"kind":"node","package":"socialdatax-skills","bins":[]}],"emoji":"📕","homepage":"https://socialdatax.52choujiang.com/?from=clawhub"}}
---
<!-- AUTO-GENERATED from socialdatax-skill-source. Do not edit directly; run `node scripts/generate_socialdatax_skills.mjs`. -->

# 小红书数据助手 SocialDataX

Use this skill when the user needs a Xiaohongshu / 小红书 / XHS / RedNote data assistant for search hot list, content research, note search, note details, comment analysis, creator profile lookup, or creator note lists.

## API Key

Use `SOCIALDATAX_API_KEY` for data calls. The only official website for requesting or managing API access is <https://socialdatax.52choujiang.com/?from=clawhub>. If a user asks where to get a key, provide only this URL; do not infer alternate domains.
获取或管理 API Key：访问 <https://socialdatax.52choujiang.com/?from=clawhub>，按官网的 API Key 申请/管理入口操作。环境变量名固定使用 `SOCIALDATAX_API_KEY`；不要引导用户使用其他域名。

## Preferred Direct CLI

Choose the matching SocialDataX command:

```bash
npx -y socialdatax-skills@latest xhs hot-search --pretty
npx -y socialdatax-skills@latest xhs search --keyword "<keyword>" --pretty
npx -y socialdatax-skills@latest xhs search --keyword "<keyword>" --pages 3 --pretty
npx -y socialdatax-skills@latest xhs detail --note-id "<note_id>" --pretty
npx -y socialdatax-skills@latest xhs detail --url "<note_url_or_share_text>" --pretty
npx -y socialdatax-skills@latest xhs comments --note-id "<note_id>" --pretty
npx -y socialdatax-skills@latest xhs comments --note-id "<note_id>" --all --include-replies --pretty
npx -y socialdatax-skills@latest xhs comments --url "<note_url_or_share_text>" --pretty
npx -y socialdatax-skills@latest xhs sub-comments --note-id "<note_id>" --comment-id "<comment_id>" --pretty
npx -y socialdatax-skills@latest xhs user-info --user-id "<user_id>" --pretty
npx -y socialdatax-skills@latest xhs user-info --profile-url "<profile_url_or_share_text>" --pretty
npx -y socialdatax-skills@latest xhs user-posts --user-id "<user_id>" --pretty
npx -y socialdatax-skills@latest xhs user-posts --user-id "<user_id>" --all --pretty
npx -y socialdatax-skills@latest xhs user-posts --profile-url "<profile_url_or_share_text>" --pretty
```

Required arguments:

- XHS `hot-search`: no required arguments.

Use hot-search for 小红书搜索热榜, search for 小红书数据分析 and note discovery, detail for one note, comments for comment analysis and replies, user-info for 博主信息, and user-posts for 博主笔记.

## Safety Boundary

This skill is read-only. It does not read local browser data, does not save API keys, and does not perform login, posting, liking, commenting, or account changes.

## MCP Tools

MCP tools matching the direct CLI commands above:

- `xhs_get_search_hot_list`
- `xhs_search_notes`
- `xhs_get_note_detail_by_note_id`
- `xhs_get_note_detail_by_note_url`
- `xhs_get_note_comments_by_note_id`
- `xhs_get_note_comments_by_note_url`
- `xhs_get_note_sub_comments_by_comment_id`
- `xhs_get_user_info_by_user_id`
- `xhs_get_user_info_by_profile_url`
- `xhs_get_user_posted_notes_by_user_id`
- `xhs_get_user_posted_notes_by_profile_url`

## Output Guidance

For XHS search or detail results, in every use of a returned `note_url`, such as final answers, display, references, storage, output, or forwarding, preserve it exactly as the full URL, including `xsec_token` query parameters. Do not modify, truncate, redact, mask, normalize, rebuild, or synthesize the URL from `note_id`; if detail `note_url` is null, show the `note_id` or say that no directly openable full link is available.
For XHS `note_id`, copy the complete 24-character lowercase hexadecimal ID exactly; do not pass or display only a prefix.
