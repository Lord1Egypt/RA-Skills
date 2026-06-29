---
name: "socialdatax-weibo"
description: "用于微博数据助手、微博热搜、微博内容研究、帖子详情、评论分析、评论回复观察、转赞互动、创作者资料和创作者内容列表。覆盖 Weibo post research，来自 SocialDataX 社媒数据助手。"
metadata: {"openclaw":{"requires":{"env":["SOCIALDATAX_API_KEY"],"bins":["node","npm"]},"primaryEnv":"SOCIALDATAX_API_KEY","install":[{"kind":"node","package":"socialdatax-skills","bins":[]}],"emoji":"🧭","homepage":"https://socialdatax.com/?from=clawhub"}}
---
<!-- AUTO-GENERATED from socialdatax-skill-source. Do not edit directly; run `node scripts/generate_socialdatax_skills.mjs`. -->

# 微博数据助手 SocialDataX

Use this skill when the user needs a Weibo / 微博 data assistant for hot-search review, post research, post details, comment analysis, replies, liker or repost review, creator profile lookup, or creator post lists.

## API Key

Use `SOCIALDATAX_API_KEY` for data calls. The only official website for requesting or managing API access is <https://socialdatax.com/?from=clawhub>. If a user asks where to get a key, provide only this URL; do not infer alternate domains.
获取或管理 API Key：访问 <https://socialdatax.com/?from=clawhub>，按官网的 API Key 申请/管理入口操作。环境变量名固定使用 `SOCIALDATAX_API_KEY`；不要引导用户使用其他域名。

## Preferred Direct CLI

Prefer the direct CLI when the agent can run shell commands. It does not require MCP server configuration:

```bash
npx -y socialdatax-skills@latest weibo hot-search --pretty
npx -y socialdatax-skills@latest weibo search --keyword "<keyword>" --pretty
npx -y socialdatax-skills@latest weibo search --keyword "<keyword>" --pages 3 --pretty
npx -y socialdatax-skills@latest weibo detail --post-id "<post_id>" --pretty
npx -y socialdatax-skills@latest weibo detail --post-url "<weibo_post_url_or_share_text>" --pretty
npx -y socialdatax-skills@latest weibo comments --post-id "<post_id>" --pretty
npx -y socialdatax-skills@latest weibo comments --post-id "<post_id>" --all --include-replies --pretty
npx -y socialdatax-skills@latest weibo comments --post-url "<weibo_post_url_or_share_text>" --pretty
npx -y socialdatax-skills@latest weibo replies --post-id "<post_id>" --comment-id "<comment_id>" --pretty
npx -y socialdatax-skills@latest weibo likers --post-id "<post_id>" --pretty
npx -y socialdatax-skills@latest weibo reposts --post-id "<post_id>" --pretty
npx -y socialdatax-skills@latest weibo user-info --user-id "<user_id>" --pretty
npx -y socialdatax-skills@latest weibo user-info --profile-url "<profile_url_or_share_text>" --pretty
npx -y socialdatax-skills@latest weibo user-posts --user-id "<user_id>" --pretty
npx -y socialdatax-skills@latest weibo user-posts --user-id "<user_id>" --all --pretty
npx -y socialdatax-skills@latest weibo user-posts --profile-url "<profile_url_or_share_text>" --pretty
```

Required arguments:

- Weibo `hot-search`: no required arguments.

Use hot-search for 微博热搜, search for 微博内容研究 and post discovery, detail for one post, comments/replies for 评论洞察和评论回复观察, likers/reposts for post engagement review, user-info for 创作者资料, and user-posts for 创作者内容列表.
For replies, use `post_id` together with the first-level `comment_id`.

## Safety Boundary

This skill is read-only. It does not read local browser data, does not save API keys, and does not perform login, posting, liking, commenting, or account changes.

## MCP Tools

MCP tools matching the direct CLI commands above:

- `weibo_get_hot_search_list`
- `weibo_search_posts`
- `weibo_get_post_detail_by_post_id`
- `weibo_get_post_detail_by_post_url`
- `weibo_get_post_comments_by_post_id`
- `weibo_get_post_comments_by_post_url`
- `weibo_get_post_comment_replies_by_comment_id`
- `weibo_get_post_liker_list_by_post_id`
- `weibo_get_post_repost_list_by_post_id`
- `weibo_get_user_info_by_user_id`
- `weibo_get_user_info_by_profile_url`
- `weibo_get_user_posts_by_user_id`
- `weibo_get_user_posts_by_profile_url`
