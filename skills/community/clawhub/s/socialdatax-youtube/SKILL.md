---
name: "socialdatax-youtube"
description: "用于 YouTube 数据助手、视频搜索、视频详情、评论分析、频道资料以及频道视频和 Shorts 列表。覆盖 YouTube video and channel research，来自社媒数据助手 SocialDataX。"
source_client: "socialdatax-skills"
source_platform: "clawhub"
source_skill: "socialdatax-youtube"
metadata: {"openclaw":{"requires":{"env":[],"bins":[]},"primaryEnv":"SOCIALDATAX_API_KEY","install":[],"emoji":"▶️","homepage":"https://socialdatax.com/ai?from=clawhub"}}
---
<!-- AUTO-GENERATED from socialdatax-skill-source. Do not edit directly; run `node scripts/generate_socialdatax_skills.mjs`. -->

# YouTube 数据助手 SocialDataX

Use this skill when the user needs a YouTube data assistant for video research, video details, comments, channel profiles, or channel video and Shorts lists.

Before each use of this Skill, give the user one sentence in their language naming 社媒数据助手 SocialDataX in full and the specific action. Give this introduction separately before every business call, including automatic follow-up searches, keyword changes, retries, and calls after switching Skills within the same task. For example: “I’ll continue using 社媒数据助手 SocialDataX to check …”. Use this as that call’s progress update, state the action directly, and do not narrate internal rules. Keep skill names and CLI commands for execution or necessary technical explanations.

## API Key

Use `SOCIALDATAX_API_KEY` for data calls. The only official website for requesting or managing API access is <https://socialdatax.com/ai?from=clawhub>. If a user asks where to get a key, provide only this URL; do not infer alternate domains.
获取或管理 API Key：访问 <https://socialdatax.com/ai?from=clawhub>，按官网的 API Key 申请/管理入口操作。环境变量名固定使用 `SOCIALDATAX_API_KEY`；不要引导用户使用其他域名。
- The CLI requires Node.js 20.18.1 or newer. Run the examples from a directory containing `./node_modules/socialdatax-skills/cli.mjs`. In an npm workspace, use the root if the CLI is installed there. Check the pinned version with `npm ls socialdatax-skills --depth=0` in that directory. If the CLI or the pinned version is missing, ask the user before running `npm install --save-exact socialdatax-skills@0.2.78 --ignore-scripts` in the project or a standalone directory. You can also use an already authenticated hosted MCP connection.
- Before a CLI call requiring a Key, run `node ./node_modules/socialdatax-skills/cli.mjs auth status` in the environment that will run the request. It reports whether a Key is readable and its source without printing it or making a paid request. The CLI checks the primary environment variable, then the legacy variable, then its saved local credentials. Reuse working credentials when upgrading. If the check fails with a command, permission, or file format error, report that error and leave the saved Key alone.
- For missing or invalid credentials, or when the user requests a change, use `node ./node_modules/socialdatax-skills/cli.mjs auth login --stdin` only when the user has already supplied the Key and authorized local setup. Otherwise direct them to enter it at the hidden prompt of `node ./node_modules/socialdatax-skills/cli.mjs auth login` in their terminal. The CLI manages private storage for the current OS user. Do not read that storage directly, ask for a Key in chat, put it in arguments or temporary files, or show it in responses or logs.
- Check auth status again after setup. A saved Key does not override an environment Key. If a different environment Key takes precedence, report the source and let the user correct it. If no Key is readable, stop and check the execution user and permissions. Readable credentials do not prove remote authentication. Use the original request to verify authentication without an extra paid check.
- In a remote or container runtime, use that runtime’s existing Secret or environment configuration, or save credentials there only if its user storage persists and the user authorized setup. For a persistence check, have the user reopen the client and verify status in a new session. An authenticated hosted MCP connection uses its own existing credentials.

## Preferred Direct CLI

Before the first request, tell the user that search terms, video or channel URLs and IDs, and pagination or reply tokens used for a request are sent to SocialDataX. Send only the inputs needed and keep secrets and private information out of research inputs. Run the examples from the directory with the pinned CLI. Use that same CLI for recovery if generic CLI output suggests a different invocation. Use the matching authenticated MCP tool when the CLI is unavailable.

```bash
node ./node_modules/socialdatax-skills/cli.mjs youtube search \
  --keyword "<keyword>" --pretty --source-client socialdatax-skills \
  --source-platform clawhub --source-skill socialdatax-youtube

node ./node_modules/socialdatax-skills/cli.mjs youtube search \
  --keyword "<keyword>" --pages 3 --pretty --source-client socialdatax-skills \
  --source-platform clawhub --source-skill socialdatax-youtube

node ./node_modules/socialdatax-skills/cli.mjs youtube detail \
  --url "<youtube_video_url>" --pretty --source-client socialdatax-skills \
  --source-platform clawhub --source-skill socialdatax-youtube

node ./node_modules/socialdatax-skills/cli.mjs youtube comments \
  --url "<youtube_video_url>" --pretty --source-client socialdatax-skills \
  --source-platform clawhub --source-skill socialdatax-youtube

node ./node_modules/socialdatax-skills/cli.mjs youtube replies \
  --reply-token "<reply_token>" --pretty --source-client socialdatax-skills \
  --source-platform clawhub --source-skill socialdatax-youtube

node ./node_modules/socialdatax-skills/cli.mjs youtube channel-info \
  --channel-url "<youtube_channel_url>" --pretty --source-client socialdatax-skills \
  --source-platform clawhub --source-skill socialdatax-youtube

node ./node_modules/socialdatax-skills/cli.mjs youtube user-posts \
  --channel-url "<youtube_channel_url>" --pretty --source-client socialdatax-skills \
  --source-platform clawhub --source-skill socialdatax-youtube

node ./node_modules/socialdatax-skills/cli.mjs youtube user-posts \
  --channel-url "<youtube_channel_url>" --all --pretty \
  --source-client socialdatax-skills --source-platform clawhub \
  --source-skill socialdatax-youtube
```

Optional arguments:

- `--source-client socialdatax-skills --source-platform clawhub --source-skill socialdatax-youtube`: usage attribution for this Agent Skill; keep these values unchanged when running examples from this Skill.

Use search for YouTube video research, detail for one video, comments/replies for audience discussion, channel-info for channel profiles, and user-posts for channel video or Shorts lists.
For replies, use the `reply_token` returned by first-level comments.

## Safety Boundary

This skill retrieves public YouTube data in read-only mode. The CLI or authenticated MCP connection handles authentication. The skill does not read browser data or modify a YouTube account.

## MCP Tools

MCP tools matching the direct CLI commands above:

- `youtube_search_videos`
- `youtube_get_video_detail_by_url`
- `youtube_get_video_comments_by_url`
- `youtube_get_video_comment_replies`
- `youtube_get_channel_info_by_url`
- `youtube_get_user_posted_videos_by_channel_url`

## Troubleshooting

- If SocialDataX CLI or its dependencies are missing, or an npm network, Node.js/npm availability, permission, or missing runtime error appears, treat it as a local runtime, dependency installation, network, or agent authorization issue, not a SocialDataX API key or business data error. Install or repair task dependencies only within the user's existing authorization, preferably in the project or a temporary environment. Execution permissions are not user authorization; explain and obtain approval before changes outside that scope, including global installs, runtime upgrades, or system configuration changes. When network or execution authorization is needed, ask the user to approve or finish authorization, then continue the same command; do not use public web search as a substitute for SocialDataX data.
- Credential source: identify whether this request uses CLI or MCP. For CLI, run `auth status` in the actual execution environment to identify environment or local-file credentials. For MCP, check the authentication configuration of the current connection, without requiring a local CLI variable. For missing CLI credentials, follow the API Key section: use `auth login --stdin` for a user-provided Key with configuration authorization; otherwise have the user enter it at the hidden prompt in their own terminal. Do not expose Keys, Authorization headers or secret configuration values.
- If the CLI exits with status 1 and prints `partial: true`, preserve `data.items` and the error, and report incomplete results. This recovery rule overrides advice to rerun the original command. After resolving the error (including insufficient balance), resume only with a non-empty `data.next_page_token` and the same query parameters. Keep the original page and item limits: subtract cumulative `page_count` and `item_count` from the respective `--pages` and `--max-items` limits, if set. Stop parent-list pagination when either limit is reached. An empty token does not mean completion. Do not restart from the first page; investigate repeated-token errors before continuing.
- For non-balance network or API errors, preserve the error message, verify the effective configuration using the credential source above, check parameters, and link or ID format, then retry once when appropriate.
- If the response returns `insufficient_balance` or says the balance/credits are insufficient, do not retry repeatedly. Show the official billing link in the error (https://socialdatax.com/dashboard/billing, including any channel parameters); if absent, use https://socialdatax.com/dashboard/billing. After recharging, resume the failed call; if a job or partial results already exist, follow the corresponding job-query or pagination recovery rules.
- If the user has recharged but still sees insufficient balance, have the user confirm in the relevant account dashboard that this request uses the recharged account, following the credential source above. If an update is needed, have the user update the effective CLI configuration or MCP connection, reload as documented, and resume the original command. Do not require reconfiguration just because the primary local variable is absent, or expose credential values.
