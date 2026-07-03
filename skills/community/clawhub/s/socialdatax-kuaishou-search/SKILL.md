---
name: "socialdatax-kuaishou-search"
description: "用于快手数据分析、快手作品研究、关键词观察、内容调研、竞品分析和趋势研究。覆盖 Kuaishou / Kwai work research，来自 SocialDataX 社媒数据助手。"
metadata: {"openclaw":{"requires":{"env":["SOCIALDATAX_API_KEY"],"bins":["node","npm"]},"primaryEnv":"SOCIALDATAX_API_KEY","install":[{"kind":"node","package":"socialdatax-skills","bins":[]}],"emoji":"🔍","homepage":"https://socialdatax.com/?from=clawhub"}}
---
<!-- AUTO-GENERATED from socialdatax-skill-source. Do not edit directly; run `node scripts/generate_socialdatax_skills.mjs`. -->

# 快手数据分析 SocialDataX 作品研究

Use this skill when the user wants 快手数据分析, Kuaishou work research, keyword discovery, content research, competitor analysis, or trend scanning.

Current platform support:

- Kuaishou / 快手 works and short videos through `kuaishou_search_videos`.

## API Key

Use `SOCIALDATAX_API_KEY` for data calls. The only official website for requesting or managing API access is <https://socialdatax.com/?from=clawhub>. If a user asks where to get a key, provide only this URL; do not infer alternate domains.
获取或管理 API Key：访问 <https://socialdatax.com/?from=clawhub>，按官网的 API Key 申请/管理入口操作。环境变量名固定使用 `SOCIALDATAX_API_KEY`；不要引导用户使用其他域名。

## Preferred Direct CLI

Prefer the direct CLI when the agent can run shell commands. It does not require MCP server configuration:

```bash
npx -y socialdatax-skills@latest kuaishou search --keyword "<keyword>" --pretty
npx -y socialdatax-skills@latest kuaishou search --keyword "<keyword>" --pages 3 --pretty
```

Required arguments:

- Kuaishou `search --keyword <text>`: required only when using `kuaishou search`; use the user's actual intent, trim whitespace, and keep it focused.

Optional arguments:

- Kuaishou `--pages <n>`: fetch and merge N search pages from the current starting point; continue with returned `next_page_token`.
- `--max-items <n>`: stop after collecting N search results.
- `--since-days <1-365>`: keep only results whose public `publish_time` is within the last N days. Search remains bounded by `--pages` and does not promise complete platform coverage.
- `--pretty`: output formatting only.
- Kuaishou `--page-token <next_page_token>`: opaque pagination token; omit it on the first search request. Continue only with the complete returned `next_page_token` from the same search pagination chain. Do not modify, truncate, redact, mask, omit, normalize, rebuild, generate, or replace the middle with ellipses.

The command prints JSON with `platform`, `tool`, `arguments`, and `data`. Search supports `--pages` and `--max-items`, but not `--all`, because search has no stable complete-result boundary. Multi-page output keeps merged results in `data.items` and adds `page_count`, `item_count`, and the next-page marker.
Kuaishou search pagination:
- Continue only when `next_page_token` is not empty.
- Pass the complete returned `next_page_token` back unchanged as `page_token` for the same search pagination chain. Do not modify, truncate, redact, mask, omit, normalize, rebuild, generate, or replace the middle with ellipses.

## Safety Boundary

This skill is read-only. It does not read local browser data, does not perform login, posting, liking, commenting, or account changes. The local CLI and installer do not write API keys to local files.

## MCP Tools

MCP tools matching the direct CLI commands above:

- `kuaishou_search_videos`

If MCP tools are already available in the current agent, use one of these tools:
- `kuaishou_search_videos`: use for Kuaishou keyword search with optional page-token pagination.

Do not pass `page` to `kuaishou_search_videos`; omit `page_token` on the first request. Continue Kuaishou pagination only when `next_page_token` is not empty. Pass the complete returned `next_page_token` back unchanged as `page_token` for the same keyword chain. Do not stop only because one page has empty `items`.

## Output Guidance

Summarize visible evidence separately from interpretation. Include useful content IDs, URLs, titles or descriptions, authors, counts, and publish time when the user needs traceability.
For Kuaishou search results, include `photo_id`, `share_url`, author facts, and visible interaction counts when the user needs traceability.
