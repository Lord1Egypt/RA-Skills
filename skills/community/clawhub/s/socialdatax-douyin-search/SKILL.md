---
name: "socialdatax-douyin-search"
description: "用于抖音数据分析、抖音热榜、抖音作品搜索、图文搜索、关键词检索、内容调研、竞品分析和趋势研究。覆盖 Douyin hot search and work search，来自 SocialDataX 社媒数据助手。"
source_client: "socialdatax-skills"
source_platform: "clawhub"
source_skill: "socialdatax-douyin-search"
metadata: {"openclaw":{"requires":{"env":[],"bins":[]},"primaryEnv":"SOCIALDATAX_API_KEY","install":[{"kind":"node","package":"socialdatax-skills@0.2.71","bins":[]}],"emoji":"🔥","homepage":"https://socialdatax.com/ai?from=clawhub"}}
---
<!-- AUTO-GENERATED from socialdatax-skill-source. Do not edit directly; run `node scripts/generate_socialdatax_skills.mjs`. -->

# 抖音数据分析 SocialDataX 作品搜索

Use this skill when the user wants 抖音数据分析, 抖音热榜, Douyin work search, image/text post search, keyword discovery, content research, competitor analysis, or trend scanning.

Current platform support:

- Douyin / 抖音 hot-search through `douyin_get_hot_search_list`.
- Douyin / 抖音 works, including video and image/text posts, through `douyin_search_videos`.

## API Key

Use `SOCIALDATAX_API_KEY` for data calls. The only official website for requesting or managing API access is <https://socialdatax.com/ai?from=clawhub>. If a user asks where to get a key, provide only this URL; do not infer alternate domains.
获取或管理 API Key：访问 <https://socialdatax.com/ai?from=clawhub>，按官网的 API Key 申请/管理入口操作。环境变量名固定使用 `SOCIALDATAX_API_KEY`；不要引导用户使用其他域名。
- Before a CLI call requiring an API Key, run `npx -y socialdatax-skills@0.2.71 auth status` in the actual execution environment. It makes no paid request and reports only `apiKeyReadable` and source `environment` / `file` / `null`, never the Key. For installation or upgrades, reuse readable existing credentials without known authentication failures unless the user explicitly requests a different Key; do not require login again, migrate credentials, or overwrite their configuration; handle command, permission and malformed-file errors as reported instead of treating every failure as a missing Key. Authenticated hosted MCP keeps its current connection authentication and needs no separate local CLI setup.
- Enter a Key only for first-time setup, missing or invalid credentials, or an explicit Key change. When the user has already supplied a Key in the installation prompt or current conversation and authorized configuration, send it as stdin to `npx -y socialdatax-skills@0.2.71 auth login --stdin` for persistent CLI storage; do not request duplicate manual entry, pass it as a CLI argument, or write it to a temporary script file. Otherwise direct the user to the official URL above and hidden input with `npx -y socialdatax-skills@0.2.71 auth login` in their local terminal, without asking them to send it in chat. The CLI saves it under the execution user's home at `.config/socialdatax/credentials.json`, Unix mode 600 or a private current-user ACL on Windows. Do not repeat the Key in replies, output logs, screenshots, command examples, Skill files or version control. The Agent must not read or display credential-file content.
- Each CLI invocation reads the private user file without depending on a client loading shell configuration or changing client/system settings. A nonempty `SOCIALDATAX_API_KEY` has priority, then the existing legacy variable, then the file. Saving a file does not replace an effective environment credential or prove the selected Key is effective. If the CLI warns about a different environment Key, report the actual source without silently deleting or changing existing environment settings. For authentication failures, check the actual source/account and have the user correct it locally while preserving other configuration.
- After saving, rerun `auth status` in the same environment as the business command. If false, stop business calls and check the OS user, home directory and file access. True only means readable credentials; authentication and results are determined by the original business response, without an extra paid call solely to check configuration.
- Remote/container CLI runs use that runtime user's configuration; a local file does not transfer automatically. Persist credentials there only with a persistent home; without an already authorized Key, interactive user login is also needed. Otherwise use existing platform-supported Secret/environment injection. If persistence is unavailable or sandbox-blocked, report the actual limit without copying the Key to additional chats, projects or temporary files, or bypassing isolation.
- When persistence acceptance is needed, finish configuration and installation first, then ask the user to fully quit the client and its background execution processes, reopen, and check from a new session before resuming the original request. Do not terminate the client hosting the current task. Normal use reuses verified configuration without repeated restarts or entry.

## Preferred Direct CLI

Prefer the direct CLI when the agent can run shell commands. It does not require MCP server configuration:

```bash
npx -y socialdatax-skills@0.2.71 douyin hot-search \
  --pretty --source-client socialdatax-skills --source-platform clawhub \
  --source-skill socialdatax-douyin-search

npx -y socialdatax-skills@0.2.71 douyin search \
  --keyword "<keyword>" --pretty --source-client socialdatax-skills \
  --source-platform clawhub --source-skill socialdatax-douyin-search

npx -y socialdatax-skills@0.2.71 douyin search \
  --keyword "<keyword>" --pages 3 --pretty --source-client socialdatax-skills \
  --source-platform clawhub --source-skill socialdatax-douyin-search

npx -y socialdatax-skills@0.2.71 douyin user-search \
  --keyword "<keyword>" --pretty --source-client socialdatax-skills \
  --source-platform clawhub --source-skill socialdatax-douyin-search
```

Required arguments:

- Douyin `hot-search`: no required arguments.
- Douyin `search --keyword <text>`: required only when using `douyin search`; use the user's actual intent, trim whitespace, and keep it focused.

Optional arguments:

- `--pretty`: output formatting only.
- Douyin `--page-token <next_page_token>`: opaque pagination token; omit it on the first search request. Continue only with the complete returned `next_page_token` from the same search pagination chain. Do not modify, truncate, redact, mask, omit, normalize, rebuild, generate, or replace the middle with ellipses.
- Douyin `--sort-type <general|time_descending|like_count_descending>`: optional sort value; omit it for the default sort.
- Douyin `--publish-time-range <all|day|week|half_year>`: optional publish-time filter; omit it for no publish-time filter.
- Douyin `--duration-range <all|under_1_minute|one_to_five_minutes|over_5_minutes>`: optional duration filter; omit it for no duration filter.
- Douyin `--content-type <all|video|image>`: optional content type filter; omit it for all content types.
- Douyin `--pages <n>`: fetch and merge N search pages from the current starting point; continue with returned `next_page_token`.
- `--max-items <n>`: stop after collecting N search results.
- `--source-client socialdatax-skills --source-platform clawhub --source-skill socialdatax-douyin-search`: usage attribution for this Agent Skill; keep these values unchanged when running examples from this Skill.

Use `douyin hot-search` for the current Douyin main hot-search list. Do not ask the user for `--keyword` for this command.
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

## Safety Boundary

This skill is read-only. CLI calls use existing environment credentials or the user’s explicitly saved private local credential file. Generated Skill files do not contain API keys. It does not read local browser data or perform login, posting, liking, commenting, or account changes.

## MCP Tools

MCP tools matching the direct CLI commands above:

- `douyin_get_hot_search_list`
- `douyin_search_videos`
- `douyin_search_users`

If MCP tools are already available in the current agent, use one of these tools:
- `douyin_get_hot_search_list`: use for the current Douyin main hot search list.
- `douyin_search_videos`: use for Douyin keyword search with optional semantic filters.
- `douyin_search_users`: use when the user wants to discover Douyin creator or account candidates by name, keyword, niche, or public Douyin ID.

Do not pass `page` to `douyin_search_videos`; omit `page_token` on the first request. Continue Douyin pagination only when `next_page_token` is not empty. Pass the complete returned `next_page_token` back unchanged as `page_token` for the same keyword and filter chain. Do not stop only because one page has empty `items`.

## Output Guidance

Summarize hot-search items as observed ranking signals. Keep the current hot-search list separate from keyword search results when both are used.
Summarize visible evidence separately from interpretation. Include useful content IDs, URLs, titles or descriptions, authors, counts, and publish time when the user needs traceability.
For Douyin search results, include `content_type` when the user needs traceability.
For Douyin image/text search results, use returned `images` and treat `video.media_type="audio"` as an audio player resource rather than a video post.

## Troubleshooting

- Credential source: identify whether this request uses CLI or MCP. For CLI, run `auth status` in the actual execution environment to identify environment or local-file credentials. For MCP, check the authentication configuration of the current connection, without requiring a local CLI variable. If configuration is missing, follow the API Key section for user-entered hidden local login. Do not expose Keys, Authorization headers or secret configuration values.

- If an SDK/dependency, npm network, Node.js/npm/npx availability, permission, or missing runtime error appears, treat it as a local runtime, dependency installation, network, or agent authorization issue, not a SocialDataX API key or business data error. Install or repair task dependencies only within the user's existing authorization, preferably in the project or a temporary environment. Execution permissions are not user authorization; explain and obtain approval before changes outside that scope, including global installs, runtime upgrades, or system configuration changes. When network or execution authorization is needed, ask the user to approve or finish authorization, then continue the same command; do not use public web search as a substitute for SocialDataX data.
- If the CLI exits with status 1 and prints `partial: true`, preserve `data.items` and the error, and report incomplete results. This recovery rule overrides advice to rerun the original command. After resolving the error (including insufficient balance), resume only with a non-empty `data.next_page_token` and the same query parameters. Keep the original page and item limits: subtract cumulative `page_count` and `item_count` from the respective `--pages` and `--max-items` limits, if set. Stop parent-list pagination when either limit is reached. An empty token does not mean completion. Do not restart from the first page; investigate repeated-token errors before continuing.
- For non-balance network or API errors, preserve the error message, check the effective credential source above, parameters, and link or ID format, then retry once when appropriate.
- If the response returns `insufficient_balance` or says the balance/credits are insufficient, do not retry repeatedly. Show the official billing link in the error (https://socialdatax.com/dashboard/billing, including any channel parameters); if absent, use https://socialdatax.com/dashboard/billing. After recharging, resume the failed call; if a job or partial results already exist, follow the corresponding job-query or pagination recovery rules.
- If the user has recharged but still sees insufficient balance, have the user confirm in the relevant account dashboard that this request uses the recharged account, following the credential source above. If an update is needed, have the user update the effective CLI configuration or MCP connection, reload as documented, and resume the original command. Do not require reconfiguration just because the primary local variable is absent, or expose credential values.
