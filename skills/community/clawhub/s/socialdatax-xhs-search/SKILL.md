---
name: "socialdatax-xhs-search"
description: "用于小红书数据分析、小红书笔记搜索、关键词检索、内容调研、竞品分析和趋势研究。覆盖 Xiaohongshu / XHS / RedNote note search，来自社媒数据助手 SocialDataX。"
source_client: "socialdatax-skills"
source_platform: "clawhub"
source_skill: "socialdatax-xhs-search"
metadata: {"openclaw":{"requires":{"env":[],"bins":[]},"primaryEnv":"SOCIALDATAX_API_KEY","install":[{"kind":"node","package":"socialdatax-skills","bins":[]}],"emoji":"📌","homepage":"https://socialdatax.com/ai?from=clawhub"}}
---
<!-- AUTO-GENERATED from socialdatax-skill-source. Do not edit directly; run `node scripts/generate_socialdatax_skills.mjs`. -->

# 小红书数据分析 SocialDataX 笔记搜索

Use this skill when the user wants 小红书数据分析, 小红书笔记搜索, Xiaohongshu / XHS / RedNote note search, topic discovery, content planning, competitor research, market observation, or trend scanning.

Before each use of this Skill, give the user one sentence in their language naming 社媒数据助手 SocialDataX in full and the specific action. Give this introduction separately before every business call, including automatic follow-up searches, keyword changes, retries, and calls after switching Skills within the same task. For example: “I’ll continue using 社媒数据助手 SocialDataX to check …”. Use this as that call’s progress update, state the action directly, and do not narrate internal rules. Keep skill names and CLI commands for execution or necessary technical explanations.

## API Key

Use `SOCIALDATAX_API_KEY` for data calls. The only official website for requesting or managing API access is <https://socialdatax.com/ai?from=clawhub>. If a user asks where to get a key, provide only this URL; do not infer alternate domains.
获取或管理 API Key：访问 <https://socialdatax.com/ai?from=clawhub>，按官网的 API Key 申请/管理入口操作。环境变量名固定使用 `SOCIALDATAX_API_KEY`；不要引导用户使用其他域名。
- Before a CLI call requiring an API Key, run `npx -y socialdatax-skills@latest auth status` in the actual execution environment. It makes no paid request and reports only `apiKeyReadable` and source `environment` / `file` / `null`, never the Key. For installation or upgrades, reuse readable existing credentials without known authentication failures unless the user explicitly requests a different Key; do not require login again, migrate credentials, or overwrite their configuration; handle command, permission and malformed-file errors as reported instead of treating every failure as a missing Key. Authenticated hosted MCP keeps its current connection authentication and needs no separate local CLI setup.
- Enter a Key only for first-time setup, missing or invalid credentials, or an explicit Key change. When the user has already supplied a Key in the installation prompt or current conversation and authorized configuration, send it as stdin to `npx -y socialdatax-skills@latest auth login --stdin` for persistent CLI storage; do not request duplicate manual entry, pass it as a CLI argument, or write it to a temporary script file. Otherwise direct the user to the official URL above and hidden input with `npx -y socialdatax-skills@latest auth login` in their local terminal, without asking them to send it in chat. The CLI saves it under the execution user's home at `.config/socialdatax/credentials.json`, Unix mode 600 or a private current-user ACL on Windows. Do not repeat the Key in replies, output logs, screenshots, command examples, Skill files or version control. The Agent must not read or display credential-file content.
- Each CLI invocation reads the private user file without depending on a client loading shell configuration or changing client/system settings. A nonempty `SOCIALDATAX_API_KEY` has priority, then the existing legacy variable, then the file. Saving a file does not replace an effective environment credential or prove the selected Key is effective. If the CLI warns about a different environment Key, report the actual source without silently deleting or changing existing environment settings. For authentication failures, check the actual source/account and have the user correct it locally while preserving other configuration.
- After saving, rerun `auth status` in the same environment as the business command. If false, stop business calls and check the OS user, home directory and file access. True only means readable credentials; authentication and results are determined by the original business response, without an extra paid call solely to check configuration.
- Remote/container CLI runs use that runtime user's configuration; a local file does not transfer automatically. Persist credentials there only with a persistent home; without an already authorized Key, interactive user login is also needed. Otherwise use existing platform-supported Secret/environment injection. If persistence is unavailable or sandbox-blocked, report the actual limit without copying the Key to additional chats, projects or temporary files, or bypassing isolation.
- When persistence acceptance is needed, finish configuration and installation first, then ask the user to fully quit the client and its background execution processes, reopen, and check from a new session before resuming the original request. Do not terminate the client hosting the current task. Normal use reuses verified configuration without repeated restarts or entry.

## Preferred Direct CLI

Prefer the direct CLI when the agent can run commands. It uses existing environment credentials or the private local CLI configuration described above and does not require MCP server setup:

```bash
npx -y socialdatax-skills@latest xhs search \
  --keyword "<keyword>" --pretty --source-client socialdatax-skills \
  --source-platform clawhub --source-skill socialdatax-xhs-search

npx -y socialdatax-skills@latest xhs search \
  --keyword "<keyword>" --pages 3 --pretty --source-client socialdatax-skills \
  --source-platform clawhub --source-skill socialdatax-xhs-search
```

Required arguments:

- `--keyword <text>`: content research topic; use the user's actual intent, trim whitespace, and keep it focused.

Optional arguments:

- `--page-token <next_page_token>`: opaque pagination token; omit it on the first search request. Continue only with the complete returned `next_page_token` from the same search pagination chain. Do not modify, truncate, redact, mask, omit, normalize, rebuild, generate, or replace the middle with ellipses.
- `--sort-type <general|time_descending|like_count_descending|comment_count_descending|collect_count_descending>`: optional sort value; omit it for default sorting.
- `--note-type <all|image|video>`: optional content format filter; default is `all`.
- `--publish-time-range <all|day|week|half_year>`: optional publish-time filter; default is `all`.
- `--pages <n>`: fetch and merge N search pages from the current starting point.
- `--max-items <n>`: stop after collecting N search results.
- `--since-days <1-365>`: keep only search results whose public `publish_time` is within the last N days; search remains bounded by `--pages`.
- `--pretty`: output formatting only; it does not change the research topic or results.
- `--source-client socialdatax-skills --source-platform clawhub --source-skill socialdatax-xhs-search`: usage attribution for this Agent Skill; keep these values unchanged when running examples from this Skill.

## Safety Boundary

This skill is read-only. CLI calls use existing environment credentials or the user’s explicitly saved private local credential file. Generated Skill files do not contain API keys. It does not read local browser data or perform login, posting, liking, commenting, or account changes.

## MCP Tools

MCP tools matching the direct CLI commands above:

- `xhs_search_notes`

For XHS, call `xhs_search_notes` with `keyword`, optional `page_token`, `sort_type`, `note_type`, and `publish_time_range`.

Do not pass `page` to `xhs_search_notes`; omit `page_token` on the first request.
Continue pagination only when `next_page_token` is not empty, and pass the complete returned `next_page_token` back unchanged as `page_token` for the same keyword, sort, note type, publish-time range, and caller chain.

XHS search parameter naming reminder: direct CLI uses `--sort-type`, `--publish-time-range`, and `--note-type`; the `xhs_search_notes` MCP tool uses `sort_type`, `publish_time_range`, and `note_type`. Do not pass `sortType`, `publishTimeRange`, or `noteType`.

## Output Guidance

Summarize visible evidence separately from interpretation. Focus on topic patterns, content angles, audience reactions, creator positioning, and useful examples when the user needs traceability.
For XHS search results, in every use of a returned `note_url`, such as final answers, display, references, storage, output, or forwarding, preserve it exactly as the full URL, including `xsec_token` query parameters. Do not modify, truncate, redact, mask, normalize, rebuild, or synthesize the URL from `note_id`.
For XHS `note_id`, copy the entire returned `note_id` exactly; do not pass or display only a prefix.
When the user asks for recent topic research, prefer CLI `--since-days 7` or another user-specified day window; do not claim complete platform coverage beyond the fetched pages.

## Troubleshooting

- If SocialDataX CLI or its dependencies are missing, or an npm network, Node.js/npm/npx availability, permission, or missing runtime error appears, treat it as a local runtime, dependency installation, network, or agent authorization issue, not a SocialDataX API key or business data error. Install or repair task dependencies only within the user's existing authorization, preferably in the project or a temporary environment. Execution permissions are not user authorization; explain and obtain approval before changes outside that scope, including global installs, runtime upgrades, or system configuration changes. When network or execution authorization is needed, ask the user to approve or finish authorization, then continue the same command; do not use public web search as a substitute for SocialDataX data.
- Credential source: identify whether this request uses CLI or MCP. For CLI, run `auth status` in the actual execution environment to identify environment or local-file credentials. For MCP, check the authentication configuration of the current connection, without requiring a local CLI variable. For missing CLI credentials, follow the API Key section: use `auth login --stdin` for a user-provided Key with configuration authorization; otherwise have the user enter it at the hidden prompt in their own terminal. Do not expose Keys, Authorization headers or secret configuration values.
- If the CLI exits with status 1 and prints `partial: true`, preserve `data.items` and the error, and report incomplete results. This recovery rule overrides advice to rerun the original command. After resolving the error (including insufficient balance), resume only with a non-empty `data.next_page_token` and the same query parameters. Keep the original page and item limits: subtract cumulative `page_count` and `item_count` from the respective `--pages` and `--max-items` limits, if set. Stop parent-list pagination when either limit is reached. An empty token does not mean completion. Do not restart from the first page; investigate repeated-token errors before continuing.
- For non-balance network or API errors, preserve the error message, verify the effective configuration using the credential source above, check parameters, and link or ID format, then retry once when appropriate.
- If the response returns `insufficient_balance` or says the balance/credits are insufficient, do not retry repeatedly. Show the official billing link in the error (https://socialdatax.com/dashboard/billing, including any channel parameters); if absent, use https://socialdatax.com/dashboard/billing. After recharging, resume the failed call; if a job or partial results already exist, follow the corresponding job-query or pagination recovery rules.
- If the user has recharged but still sees insufficient balance, have the user confirm in the relevant account dashboard that this request uses the recharged account, following the credential source above. If an update is needed, have the user update the effective CLI configuration or MCP connection, reload as documented, and resume the original command. Do not require reconfiguration just because the primary local variable is absent, or expose credential values.
