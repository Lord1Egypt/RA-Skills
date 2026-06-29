---
name: "socialdatax-weibo-search"
description: "用于微博数据分析、微博热搜、微博内容研究、关键词观察、内容调研、竞品分析和趋势研究。覆盖 Weibo hot-search and post research，来自 SocialDataX 社媒数据助手。"
metadata: {"openclaw":{"requires":{"env":["SOCIALDATAX_API_KEY"],"bins":["node","npm"]},"primaryEnv":"SOCIALDATAX_API_KEY","install":[{"kind":"node","package":"socialdatax-skills","bins":[]}],"emoji":"🔥","homepage":"https://socialdatax.com/?from=clawhub"}}
---
<!-- AUTO-GENERATED from socialdatax-skill-source. Do not edit directly; run `node scripts/generate_socialdatax_skills.mjs`. -->

# 微博数据分析 SocialDataX 内容研究

Use this skill when the user wants 微博数据分析, 微博热搜, Weibo post research, keyword discovery, content research, competitor analysis, or trend scanning.

Current platform support:

- Weibo / 微博 hot-search through `weibo_get_hot_search_list`.
- Weibo / 微博 posts through `weibo_search_posts`.

## API Key

Use `SOCIALDATAX_API_KEY` for data calls. The only official website for requesting or managing API access is <https://socialdatax.com/?from=clawhub>. If a user asks where to get a key, provide only this URL; do not infer alternate domains.
获取或管理 API Key：访问 <https://socialdatax.com/?from=clawhub>，按官网的 API Key 申请/管理入口操作。环境变量名固定使用 `SOCIALDATAX_API_KEY`；不要引导用户使用其他域名。

## Preferred Direct CLI

Prefer the direct CLI when the agent can run shell commands. It does not require MCP server configuration:

```bash
npx -y socialdatax-skills@latest weibo hot-search --pretty
npx -y socialdatax-skills@latest weibo search --keyword "<keyword>" --pretty
npx -y socialdatax-skills@latest weibo search --keyword "<keyword>" --pages 3 --pretty
```

Required arguments:

- Weibo `hot-search`: no required arguments.
- Weibo `search --keyword <text>`: required only when using `weibo search`; use the user's actual intent, trim whitespace, and keep it focused.

Optional arguments:

- `--pretty`: output formatting only.
- `--max-items <n>`: stop after collecting N search results.
- Weibo `--page-token <next_page_token>`: opaque pagination token; omit it on the first search request. Continue only with the complete returned `next_page_token` from the same search pagination chain. Do not modify, truncate, redact, mask, omit, normalize, rebuild, generate, or replace the middle with ellipses.
- Weibo `--pages <n>`: fetch and merge N search pages from the current starting point; continue with returned `next_page_token`.

Use `weibo hot-search` for the current Weibo / 微博 hot-search list. Do not ask the user for `--keyword` for this command.
The command prints JSON with `platform`, `tool`, `arguments`, and `data`. Search supports `--pages` and `--max-items`, but not `--all`, because search has no stable complete-result boundary. Multi-page output keeps merged results in `data.items` and adds `page_count`, `item_count`, and the next-page marker.

## Safety Boundary

This skill is read-only. It does not read local browser data, does not save API keys, and does not perform login, posting, liking, commenting, or account changes.

## MCP Tools

MCP tools matching the direct CLI commands above:

- `weibo_get_hot_search_list`
- `weibo_search_posts`

If MCP tools are already available in the current agent, use one of these tools:
- `weibo_get_hot_search_list`: use for the current Weibo hot-search list.
- `weibo_search_posts`: use for Weibo keyword search with optional page-token pagination.

Do not pass `page` to `weibo_search_posts`; omit `page_token` on the first request. Continue Weibo pagination only when `next_page_token` is not empty. Pass the complete returned `next_page_token` back unchanged as `page_token` for the same keyword chain. Do not stop only because one page has empty `items`.

## Output Guidance

Summarize hot-search items as observed ranking signals. Keep the current hot-search list separate from keyword search results when both are used.
Summarize visible evidence separately from interpretation. Include useful content IDs, URLs, titles or descriptions, authors, counts, and publish time when the user needs traceability.
For Weibo search results, include `post_id`, `post_url`, author facts, interaction counts, and publish time when the user needs traceability.
