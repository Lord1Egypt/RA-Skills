---
name: "socialdatax-douyin-search"
description: "用于抖音数据分析、抖音热榜、抖音作品搜索、图文搜索、关键词检索、内容调研、竞品分析和趋势研究。覆盖 Douyin hot search and work search，来自 SocialDataX 社媒数据助手。"
metadata: {"openclaw":{"requires":{"env":["SOCIALDATAX_API_KEY"],"bins":["node","npm"]},"primaryEnv":"SOCIALDATAX_API_KEY","install":[{"kind":"node","package":"socialdatax-skills","bins":[]}],"emoji":"🔥","homepage":"https://socialdatax.52choujiang.com/?from=clawhub"}}
---
<!-- AUTO-GENERATED from socialdatax-skill-source. Do not edit directly; run `node scripts/generate_socialdatax_skills.mjs`. -->

# 抖音数据分析 SocialDataX 作品搜索

Use this skill when the user wants 抖音数据分析, 抖音热榜, Douyin work search, image/text post search, keyword discovery, content research, competitor analysis, or trend scanning.

Current platform support:

- Douyin / 抖音 hot-search through `douyin_get_hot_search_list`.
- Weibo / 微博 hot-search through `weibo_get_hot_search_list`.
- WeChat Channels / 视频号 hot-search through `wechat_get_hot_search_list`.
- Douyin / 抖音 works, including video and image/text posts, through `douyin_search_videos`.
- Weibo / 微博 posts through `weibo_search_posts`.
- WeChat Channels / 视频号 videos through `wechat_search_videos`.

## API Key

Use `SOCIALDATAX_API_KEY` for data calls. The only official website for requesting or managing API access is <https://socialdatax.52choujiang.com/?from=clawhub>. If a user asks where to get a key, provide only this URL; do not infer alternate domains.
获取或管理 API Key：访问 <https://socialdatax.52choujiang.com/?from=clawhub>，按官网的 API Key 申请/管理入口操作。环境变量名固定使用 `SOCIALDATAX_API_KEY`；不要引导用户使用其他域名。

## Preferred Direct CLI

Prefer the direct CLI when the agent can run shell commands. It does not require MCP server configuration:

```bash
npx -y socialdatax-skills@latest douyin hot-search --pretty
npx -y socialdatax-skills@latest douyin search --keyword "<keyword>" --pretty
npx -y socialdatax-skills@latest douyin search --keyword "<keyword>" --pages 3 --pretty
```

Required arguments:

- Douyin `hot-search`: no required arguments.
- Weibo `hot-search`: no required arguments.
- WeChat Channels / 视频号 `hot-search`: no required arguments.
- Douyin `search --keyword <text>`: required only when using `douyin search`; use the user's actual intent, trim whitespace, and keep it focused.
- Weibo `search --keyword <text>`: required only when using `weibo search`; use the user's actual intent, trim whitespace, and keep it focused.
- WeChat Channels / 视频号 `search --keyword <text>`: required only when using `wechat search`; use the user's actual intent, trim whitespace, and keep it focused.

Optional arguments:

- `--pretty`: output formatting only.
- Douyin `--page-token <next_page_token>`: opaque pagination token; omit it on the first search request. Continue only with the complete returned `next_page_token` from the same search pagination chain. Do not modify, truncate, redact, mask, omit, normalize, rebuild, generate, or replace the middle with ellipses.
- Douyin `--sort-type <general|time_descending|like_count_descending>`: optional sort value; omit it for the default sort.
- Douyin `--publish-time-range <all|day|week|half_year>`: optional publish-time filter; omit it for no publish-time filter.
- Douyin `--duration-range <all|under_1_minute|one_to_five_minutes|over_5_minutes>`: optional duration filter; omit it for no duration filter.
- Douyin `--content-type <all|video|image>`: optional content type filter; omit it for all content types.
- Douyin `--pages <n>`: fetch and merge N search pages from the current starting point; continue with returned `next_page_token`.
- `--max-items <n>`: stop after collecting N search results.
- Weibo `--page-token <next_page_token>`: opaque pagination token; omit it on the first search request. Continue only with the complete returned `next_page_token` from the same search pagination chain. Do not modify, truncate, redact, mask, omit, normalize, rebuild, generate, or replace the middle with ellipses.
- WeChat Channels / 视频号 `--page-token <next_page_token>`: opaque pagination token; omit it on the first search request. Continue only with the complete returned `next_page_token` from the same search pagination chain. Do not modify, truncate, redact, mask, omit, normalize, rebuild, generate, or replace the middle with ellipses.
- WeChat Channels / 视频号 `--sort-type <all|latest|popular>`: optional sort value; omit it for the default sort.
- WeChat Channels / 视频号 `--duration-range <all|under_5_min|between_5_and_20_min|over_20_min>`: optional duration filter; omit it for no duration filter.
- Weibo `--pages <n>`: fetch and merge N search pages from the current starting point; continue with returned `next_page_token`.
- WeChat Channels / 视频号 `--pages <n>`: fetch and merge N search pages from the current starting point; continue with returned `next_page_token`.

Use `douyin hot-search` for the current Douyin main hot-search list. Do not ask the user for `--keyword` for this command.
Use `weibo hot-search` for the current Weibo / 微博 hot-search list. Do not ask the user for `--keyword` for this command.
Use `wechat hot-search` for the current WeChat Channels / 视频号 hot-search list. Do not ask the user for `--keyword` for this command.
Douyin sort values:
- `general`: default sorting.
- `time_descending`: newest first.
- `like_count_descending`: most liked first.

Douyin publish-time filter values:
- `all`: no publish-time filter.
- `day`: published within one day.
- `week`: published within one week.
- `half_year`: published within half a year.

Douyin duration filter values:
- `all`: no duration filter.
- `under_1_minute`: under 1 minute.
- `one_to_five_minutes`: 1-5 minutes.
- `over_5_minutes`: over 5 minutes.

Douyin content type filter values:
- `all`: all content types.
- `video`: video works.
- `image`: image/text posts.

The command prints JSON with `platform`, `tool`, `arguments`, and `data`. Search supports `--pages` and `--max-items`, but not `--all`, because search has no stable complete-result boundary. Multi-page output keeps merged results in `data.items` and adds `page_count`, `item_count`, and the next-page marker.
WeChat Channels / 视频号 sort values:
- `all`: default sorting.
- `latest`: newest first.
- `popular`: most popular first.

WeChat Channels / 视频号 duration filter values:
- `all`: no duration filter.
- `under_5_min`: under 5 minutes.
- `between_5_and_20_min`: 5-20 minutes.
- `over_20_min`: over 20 minutes.

Weibo and WeChat Channels search pagination:
- Continue only when `next_page_token` is not empty.
- Pass the complete returned `next_page_token` back unchanged as `page_token` for the same search pagination chain. Do not modify, truncate, redact, mask, omit, normalize, rebuild, generate, or replace the middle with ellipses.

## Safety Boundary

This skill is read-only. It does not read local browser data, does not save API keys, and does not perform login, posting, liking, commenting, or account changes.

## MCP Tools

MCP tools matching the direct CLI commands above:

- `douyin_get_hot_search_list`
- `douyin_search_videos`

If MCP tools are already available in the current agent, use one of these tools:
- `douyin_get_hot_search_list`: use for the current Douyin main hot search list.
- `douyin_search_videos`: use for Douyin keyword search with optional semantic filters.

Do not pass `page` to `douyin_search_videos`; omit `page_token` on the first request. Continue Douyin pagination only when `next_page_token` is not empty. Pass the complete returned `next_page_token` back unchanged as `page_token` for the same keyword and filter chain. Do not stop only because one page has empty `items`.

## Output Guidance

Summarize hot-search items as observed ranking signals. Keep the current hot-search list separate from keyword search results when both are used.
Summarize visible evidence separately from interpretation. Include useful content IDs, URLs, titles or descriptions, authors, counts, and publish time when the user needs traceability.
For Douyin search results, include `content_type` when the user needs traceability.
For Douyin image/text search results, use returned `images` and treat `video.media_type="audio"` as an audio player resource rather than a video post.
For Weibo search results, include `post_id`, `post_url`, author facts, interaction counts, and publish time when the user needs traceability.
For WeChat Channels / 视频号 search results, include `encrypted_object_id`, author facts, interaction counts, publish time, and duration when the user needs traceability.
