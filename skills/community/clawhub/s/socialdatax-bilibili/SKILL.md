---
name: "socialdatax-bilibili"
description: "用于 B站数据助手、视频和专栏搜索、内容详情、评论分析、点赞转发观察、UP主资料及视频、专栏和动态列表，并支持按需下载视频到本地。覆盖 Bilibili / 哔哩哔哩，来自 SocialDataX 社媒数据助手。"
source_client: "socialdatax-skills"
source_platform: "clawhub"
source_skill: "socialdatax-bilibili"
metadata: {"openclaw":{"requires":{"env":[],"bins":[]},"primaryEnv":"SOCIALDATAX_API_KEY","install":[{"kind":"node","package":"socialdatax-skills","bins":[]}],"emoji":"📺","homepage":"https://socialdatax.com/ai?from=clawhub"}}
---
<!-- AUTO-GENERATED from socialdatax-skill-source. Do not edit directly; run `node scripts/generate_socialdatax_skills.mjs`. -->

# B站数据助手 SocialDataX

Use this skill when the user needs a Bilibili / 哔哩哔哩 / B站 data assistant for video or article research, content details, comments, reactions, creator profiles, creator videos, articles, dynamics, or explicitly asks to save a Bilibili video locally.

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
npx -y socialdatax-skills@latest bilibili search-videos \
  --keyword "<keyword>" --pretty --source-client socialdatax-skills \
  --source-platform clawhub --source-skill socialdatax-bilibili

npx -y socialdatax-skills@latest bilibili search-articles \
  --keyword "<keyword>" --pretty --source-client socialdatax-skills \
  --source-platform clawhub --source-skill socialdatax-bilibili

npx -y socialdatax-skills@latest bilibili detail \
  --content-id "<content_id>" --pretty --source-client socialdatax-skills \
  --source-platform clawhub --source-skill socialdatax-bilibili

npx -y socialdatax-skills@latest bilibili detail \
  --url "<bilibili_content_url_or_share_text>" --pretty \
  --source-client socialdatax-skills --source-platform clawhub \
  --source-skill socialdatax-bilibili

npx -y socialdatax-skills@latest bilibili comments \
  --content-id "<content_id>" --pretty --source-client socialdatax-skills \
  --source-platform clawhub --source-skill socialdatax-bilibili

npx -y socialdatax-skills@latest bilibili comments \
  --url "<bilibili_content_url_or_share_text>" --pretty \
  --source-client socialdatax-skills --source-platform clawhub \
  --source-skill socialdatax-bilibili

npx -y socialdatax-skills@latest bilibili replies \
  --comment-object-id "<comment_object_id>" \
  --comment-object-type "<comment_object_type_integer>" --comment-id "<comment_id>" \
  --pretty --source-client socialdatax-skills --source-platform clawhub \
  --source-skill socialdatax-bilibili

npx -y socialdatax-skills@latest bilibili reactions \
  --post-id "<post_id>" --pretty --source-client socialdatax-skills \
  --source-platform clawhub --source-skill socialdatax-bilibili

npx -y socialdatax-skills@latest bilibili reactions \
  --url "<bilibili_opus_or_dynamic_url_or_share_text>" --pretty \
  --source-client socialdatax-skills --source-platform clawhub \
  --source-skill socialdatax-bilibili

npx -y socialdatax-skills@latest bilibili user-info \
  --user-id "<user_id>" --pretty --source-client socialdatax-skills \
  --source-platform clawhub --source-skill socialdatax-bilibili

npx -y socialdatax-skills@latest bilibili user-info \
  --profile-url "<profile_url_or_share_text>" --pretty \
  --source-client socialdatax-skills --source-platform clawhub \
  --source-skill socialdatax-bilibili

npx -y socialdatax-skills@latest bilibili user-videos \
  --user-id "<user_id>" --pretty --source-client socialdatax-skills \
  --source-platform clawhub --source-skill socialdatax-bilibili

npx -y socialdatax-skills@latest bilibili user-videos \
  --profile-url "<profile_url_or_share_text>" --pretty \
  --source-client socialdatax-skills --source-platform clawhub \
  --source-skill socialdatax-bilibili

npx -y socialdatax-skills@latest bilibili user-articles \
  --user-id "<user_id>" --pretty --source-client socialdatax-skills \
  --source-platform clawhub --source-skill socialdatax-bilibili

npx -y socialdatax-skills@latest bilibili user-articles \
  --profile-url "<profile_url_or_share_text>" --pretty \
  --source-client socialdatax-skills --source-platform clawhub \
  --source-skill socialdatax-bilibili

npx -y socialdatax-skills@latest bilibili user-dynamics \
  --user-id "<user_id>" --pretty --source-client socialdatax-skills \
  --source-platform clawhub --source-skill socialdatax-bilibili

npx -y socialdatax-skills@latest bilibili user-dynamics \
  --profile-url "<profile_url_or_share_text>" --pretty \
  --source-client socialdatax-skills --source-platform clawhub \
  --source-skill socialdatax-bilibili

npx -y socialdatax-skills@latest bilibili download-media \
  --url "<bilibili_video_url_or_share_text>" --output-dir ./downloads --pretty \
  --source-client socialdatax-skills --source-platform clawhub \
  --source-skill socialdatax-bilibili
```

Optional arguments:

- `--source-client socialdatax-skills --source-platform clawhub --source-skill socialdatax-bilibili`: usage attribution for this Agent Skill; keep these values unchanged when running examples from this Skill.

Use search-videos or search-articles for Bilibili / 哔哩哔哩 / B站 content research, detail for one video, article, or dynamic, comments/replies for discussion analysis, reactions for likes and reposts, user-info for creator profiles, creator list commands for videos, articles, and dynamics, and run download only when the user explicitly asks to save a video locally.
For replies, use the `comment_object_id`, `comment_object_type`, and first-level `comment_id` returned by first-level comments.

## Safety Boundary

SocialDataX requests in this skill are read-only and do not modify social accounts or platform content. CLI calls use existing environment credentials or the user’s explicitly saved private local credential file; generated Skill files do not contain API keys. It does not read local browser data or perform login, posting, liking, commenting, or account changes. The optional `bilibili download` command writes video and audio tracks plus the merged video to the user-selected local output path, uses local `ffmpeg`, and removes temporary tracks unless `--keep-tracks` is set. Online searches, lookups and download-link requests send the necessary keywords, content IDs, URLs or share text to SocialDataX to fulfill the request.

## MCP Tools

MCP tools matching the direct CLI commands above:

- `bilibili_search_videos`
- `bilibili_search_articles`
- `bilibili_get_content_detail_by_id`
- `bilibili_get_content_detail_by_url`
- `bilibili_get_content_comments_by_id`
- `bilibili_get_content_comments_by_url`
- `bilibili_get_content_comment_replies_by_comment_id`
- `bilibili_get_content_likes_and_reposts_by_post_id`
- `bilibili_get_content_likes_and_reposts_by_url`
- `bilibili_get_user_info_by_user_id`
- `bilibili_get_user_info_by_profile_url`
- `bilibili_get_user_posted_videos_by_user_id`
- `bilibili_get_user_posted_videos_by_profile_url`
- `bilibili_get_user_posted_articles_by_user_id`
- `bilibili_get_user_posted_articles_by_profile_url`
- `bilibili_get_user_posted_dynamics_by_user_id`
- `bilibili_get_user_posted_dynamics_by_profile_url`
- `bilibili_get_video_download_links`

## Troubleshooting

- Credential source: identify whether this request uses CLI or MCP. For CLI, run `auth status` in the actual execution environment to identify environment or local-file credentials. For MCP, check the authentication configuration of the current connection, without requiring a local CLI variable. If configuration is missing, follow the API Key section for user-entered hidden local login. Do not expose Keys, Authorization headers or secret configuration values.

- If an SDK/dependency, npm network, Node.js/npm/npx availability, permission, or missing runtime error appears, treat it as a local runtime, dependency installation, network, or agent authorization issue, not a SocialDataX API key or business data error. Install or repair task dependencies only within the user's existing authorization, preferably in the project or a temporary environment. Execution permissions are not user authorization; explain and obtain approval before changes outside that scope, including global installs, runtime upgrades, or system configuration changes. When network or execution authorization is needed, ask the user to approve or finish authorization, then continue the same command; do not use public web search as a substitute for SocialDataX data.
- If the CLI exits with status 1 and prints `partial: true`, preserve `data.items` and the error, and report incomplete results. This recovery rule overrides advice to rerun the original command. After resolving the error (including insufficient balance), resume only with a non-empty `data.next_page_token` and the same query parameters. Keep the original page and item limits: subtract cumulative `page_count` and `item_count` from the respective `--pages` and `--max-items` limits, if set. Stop parent-list pagination when either limit is reached. An empty token does not mean completion. Do not restart from the first page; investigate repeated-token errors before continuing.
- For non-balance network or API errors, preserve the error message, check the effective credential source above, parameters, and link or ID format, then retry once when appropriate.
- If the response returns `insufficient_balance` or says the balance/credits are insufficient, do not retry repeatedly. Show the official billing link in the error (https://socialdatax.com/dashboard/billing, including any channel parameters); if absent, use https://socialdatax.com/dashboard/billing. After recharging, resume the failed call; if a job or partial results already exist, follow the corresponding job-query or pagination recovery rules.
- If the user has recharged but still sees insufficient balance, have the user confirm in the relevant account dashboard that this request uses the recharged account, following the credential source above. If an update is needed, have the user update the effective CLI configuration or MCP connection, reload as documented, and resume the original command. Do not require reconfiguration just because the primary local variable is absent, or expose credential values.
