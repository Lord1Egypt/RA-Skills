---
name: "socialdatax-zhihu"
description: "用于知乎数据助手、知乎热榜、内容搜索、回答文章视频详情、评论分析、创作者资料和文章列表。覆盖 Zhihu content research，来自 SocialDataX 社媒数据助手。"
source_client: "socialdatax-skills"
source_platform: "clawhub"
source_skill: "socialdatax-zhihu"
metadata: {"openclaw":{"requires":{"env":[],"bins":[]},"primaryEnv":"SOCIALDATAX_API_KEY","install":[{"kind":"node","package":"socialdatax-skills","bins":[]}],"emoji":"💡","homepage":"https://socialdatax.com/ai?from=clawhub"}}
---
<!-- AUTO-GENERATED from socialdatax-skill-source. Do not edit directly; run `node scripts/generate_socialdatax_skills.mjs`. -->

# 知乎数据助手 SocialDataX

Use this skill when the user needs a Zhihu / 知乎 data assistant for hot-list review, answer, article, or video research, content details, comments, creator profiles, or creator article lists.

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

Prefer the direct CLI when the agent can run shell commands. It does not require MCP server configuration:

```bash
npx -y socialdatax-skills@latest zhihu hot-list \
  --pretty --source-client socialdatax-skills --source-platform clawhub \
  --source-skill socialdatax-zhihu

npx -y socialdatax-skills@latest zhihu search \
  --keyword "<keyword>" --pretty --source-client socialdatax-skills \
  --source-platform clawhub --source-skill socialdatax-zhihu

npx -y socialdatax-skills@latest zhihu search \
  --keyword "<keyword>" --pages 3 --pretty --source-client socialdatax-skills \
  --source-platform clawhub --source-skill socialdatax-zhihu

npx -y socialdatax-skills@latest zhihu detail \
  --content-url "<zhihu_content_url_or_share_text>" --pretty \
  --source-client socialdatax-skills --source-platform clawhub \
  --source-skill socialdatax-zhihu

npx -y socialdatax-skills@latest zhihu comments \
  --content-url "<zhihu_content_url_or_share_text>" --pretty \
  --source-client socialdatax-skills --source-platform clawhub \
  --source-skill socialdatax-zhihu

npx -y socialdatax-skills@latest zhihu replies \
  --content-url "<zhihu_content_url_or_share_text>" --comment-id "<comment_id>" \
  --pretty --source-client socialdatax-skills --source-platform clawhub \
  --source-skill socialdatax-zhihu

npx -y socialdatax-skills@latest zhihu user-info \
  --profile-url "<profile_url_or_share_text>" --pretty \
  --source-client socialdatax-skills --source-platform clawhub \
  --source-skill socialdatax-zhihu

npx -y socialdatax-skills@latest zhihu user-posts \
  --profile-url "<profile_url_or_share_text>" --pretty \
  --source-client socialdatax-skills --source-platform clawhub \
  --source-skill socialdatax-zhihu

npx -y socialdatax-skills@latest zhihu user-posts \
  --profile-url "<profile_url_or_share_text>" --all --pretty \
  --source-client socialdatax-skills --source-platform clawhub \
  --source-skill socialdatax-zhihu
```

Required arguments:

- Zhihu `hot-list`: no required arguments.

Optional arguments:

- `--source-client socialdatax-skills --source-platform clawhub --source-skill socialdatax-zhihu`: usage attribution for this Agent Skill; keep these values unchanged when running examples from this Skill.

Use hot-list for 知乎热榜, search for question, answer, article, and video research, detail for one content URL, comments/replies for discussion analysis, user-info for creator profiles, and user-posts for creator article lists.
For replies, use the Zhihu content URL together with the first-level `comment_id`.

## Safety Boundary

This skill is read-only. CLI calls use existing environment credentials or the user’s explicitly saved private local credential file. Generated Skill files do not contain API keys. It does not read local browser data or perform login, posting, liking, commenting, or account changes.

## MCP Tools

MCP tools matching the direct CLI commands above:

- `zhihu_get_hot_list`
- `zhihu_search_content`
- `zhihu_get_content_detail_by_url`
- `zhihu_get_content_comments_by_url`
- `zhihu_get_comment_replies_by_url`
- `zhihu_get_user_info_by_profile_url`
- `zhihu_get_user_posted_articles_by_profile_url`

## Troubleshooting

- Credential source: identify whether this request uses CLI or MCP. For CLI, run `auth status` in the actual execution environment to identify environment or local-file credentials. For MCP, check the authentication configuration of the current connection, without requiring a local CLI variable. If configuration is missing, follow the API Key section for user-entered hidden local login. Do not expose Keys, Authorization headers or secret configuration values.

- If an SDK/dependency, npm network, Node.js/npm/npx availability, permission, or missing runtime error appears, treat it as a local runtime, dependency installation, network, or agent authorization issue, not a SocialDataX API key or business data error. Install or repair task dependencies only within the user's existing authorization, preferably in the project or a temporary environment. Execution permissions are not user authorization; explain and obtain approval before changes outside that scope, including global installs, runtime upgrades, or system configuration changes. When network or execution authorization is needed, ask the user to approve or finish authorization, then continue the same command; do not use public web search as a substitute for SocialDataX data.
- If the CLI exits with status 1 and prints `partial: true`, preserve `data.items` and the error, and report incomplete results. This recovery rule overrides advice to rerun the original command. After resolving the error (including insufficient balance), resume only with a non-empty `data.next_page_token` and the same query parameters. Keep the original page and item limits: subtract cumulative `page_count` and `item_count` from the respective `--pages` and `--max-items` limits, if set. Stop parent-list pagination when either limit is reached. An empty token does not mean completion. Do not restart from the first page; investigate repeated-token errors before continuing.
- For non-balance network or API errors, preserve the error message, check the effective credential source above, parameters, and link or ID format, then retry once when appropriate.
- If the response returns `insufficient_balance` or says the balance/credits are insufficient, do not retry repeatedly. Show the official billing link in the error (https://socialdatax.com/dashboard/billing, including any channel parameters); if absent, use https://socialdatax.com/dashboard/billing. After recharging, resume the failed call; if a job or partial results already exist, follow the corresponding job-query or pagination recovery rules.
- If the user has recharged but still sees insufficient balance, have the user confirm in the relevant account dashboard that this request uses the recharged account, following the credential source above. If an update is needed, have the user update the effective CLI configuration or MCP connection, reload as documented, and resume the original command. Do not require reconfiguration just because the primary local variable is absent, or expose credential values.
