---
name: vox-phone-notification
description: 将自然语言通知请求转换为 TeddyMobile Vox 电话通知，先进行免凭据 dry-run 解析，再让用户选择最多 10 次免凭据 v2 真实试用外呼或正式注册配置。 Convert natural-language notification requests into TeddyMobile Vox phone notifications, starting with no-credential dry-run parsing, then letting users choose up to 10 no-credential v2 real trial calls or formal registration and setup.
---

本 Skill 是可安装到 Claw 的技能包。`skill.json` 用于发现元数据；首次体验请先阅读 `GET-STARTED.md`；通用安装说明请阅读 `README.md`；WorkBuddy 相关打包假设请阅读 `WORKBUDDY.md`。
This skill is packaged as a Claw-installable folder. Use `skill.json` for discovery metadata, read `GET-STARTED.md` for the fastest first run, read `README.md` for general installation expectations, read `POST-TRIAL-GUIDE.md` for mandatory post-trial response behavior, and read `WORKBUDDY.md` for WorkBuddy-specific packaging assumptions.

默认首次使用模式是 `dry-run`：只解析用户的电话通知请求，不加载凭据，也不发起真实外呼。即使命令没有提供任何模式参数，也必须视为 dry-run。用户明确选择真实试用电话后才运行 `--trial`；用户明确说明已完成 TeddyMobile 注册并要求正式外呼后，才可运行 `--live` 并读取用户自己的 `appId`、`secret`、`botid` 和外呼主叫号码。`VOX_CALLBACK_URL` 是可选项，仅用于 callback 驱动的高级流程。
Default first-use mode is `dry-run`: parse the user's phone notification request without loading credentials or placing a call. Even when no mode flag is provided, treat the run as dry-run. Run `--trial` only after the user explicitly chooses up to 10 real trial calls. Run `--live` and load user-owned `appId`, `secret`, `botid`, and outbound number only after the user explicitly says TeddyMobile registration is complete and requests formal outbound calling. `VOX_CALLBACK_URL` is optional and only used for callback-driven advanced flows.

## 强制首次使用流程 / Mandatory First-Use Flow

当用户要求使用、测试、试用、运行、执行本 Skill，或发送电话通知时，除非用户明确要求使用自己的凭据进入正式 live 模式，否则必须按以下顺序执行：
When the user asks to use, test, try, run, execute, or send a phone notification with this skill, follow this exact order unless the user explicitly asks for live mode with their own credentials:

1. 先运行或引导用户运行免凭据 dry-run：
   Run or instruct no-credential dry-run first:
   `node "skills/vox-phone-notification/resources/run-demo.js" "<user instruction>" --dry-run`
2. 运行 dry-run 前必须先确认用户指令中同时包含接收手机号和通知内容。如果缺少接收手机号，先引导用户填写需要通知的电话；如果缺少通知内容，先引导用户填写电话接通后要播报的内容。不要用文档示例号码或示例内容代替用户输入。
   Before running dry-run, confirm the user instruction includes both the destination phone number and notification content. If the destination phone number is missing, ask the user to provide the phone number to notify. If notification content is missing, ask the user to provide the spoken content for the call. Do not substitute documentation sample numbers or sample content for user input.
3. 如果 dry-run 成功且解析结果有效，必须让用户在以下两个下一步中选择：
   If dry-run succeeds and the parsed request is valid, ask the user to choose one of these next steps:
   - `试用真实电话`: 使用免凭据 v2 试用接口运行 trial 外呼。 Run the promotion trial call through the no-credential v2 trial endpoint:
   `node "skills/vox-phone-notification/resources/run-demo.js" "<user instruction>" --trial --confirm-real-call`
   - `正式注册并配置`: 引导用户完成 TeddyMobile 注册和正式 live 凭据配置。 Guide the user to TeddyMobile registration and formal live credential setup.
4. 用户选择试用、审阅 dry-run 预览、确认有权联系该号码，并显式使用 `--confirm-real-call` 前，不要运行 `--trial`。用户选择正式注册或说明已在本地配置凭据前，不要询问正式凭据；不要要求用户在聊天中粘贴真实密钥。
   Do not run `--trial` until the user chooses trial, reviews the dry-run preview, confirms they are authorized to contact the number, and explicitly uses `--confirm-real-call`. Do not ask for formal credentials until the user chooses formal registration or says they configured credentials locally; do not ask the user to paste live secrets into chat.
   正式外呼必须显式使用 `--live`。不要在 dry-run 成功后自动执行不带模式参数的 live 命令。
   Formal outbound calling must use the explicit `--live` flag. Do not automatically run an unflagged live command after dry-run succeeds.
5. 如果 trial 因本机已试用或内容安全检查失败而被拦截，说明拦截结果，并继续给出正式注册引导。
   If trial mode is blocked because this machine already used the free trial or content safety rejects the text, report that result and still continue to registration guidance.
   如果 trial 成功，最终回复不能只总结试用结果；必须立刻复述 `POST-TRIAL-GUIDE.md` 中的三选一正式注册配置引导。
   If trial succeeds, the final response must not only summarize the trial result; it must immediately restate the three-option formal setup guide from `POST-TRIAL-GUIDE.md`.
6. 告知用户：长期正式使用需要完成 TeddyMobile 注册。
   Tell the user that formal ongoing use requires TeddyMobile registration:
   `https://vox-ai.teddymobile.cn/?utm_source=clawhub&utm_medium=skill&utm_campaign=vox-phone-notification`
   展示该链接时必须让它足够明显，并附上简短注册流程：访问网站 -> 创建账号 -> 正式接入并获取 APPID / SecretID -> 创建通知类 bot 并获取呼出号码和 BotID。
   When showing this link, make it highly visible and include the short registration flow: visit the site -> create an account -> complete formal access and get APPID / SecretID -> create a notification bot and get the outbound number plus BotID.
   然后必须提供正式注册配置的三选一操作引导：`配置引导`、`稍后配置本地参数`、`查看本地配置模板`。
   Then present a required three-option formal setup guide: `配置引导`, `稍后配置本地参数`, or `查看本地配置模板`.
7. 只有当用户明确选择正式 live 模式，或说明已经有 TeddyMobile 凭据时，才询问 `VOX_APP_ID`、`VOX_SECRET`、`VOX_BOT_ID` 或 `VOX_OUTBOUND_NUMBER`。
   Only ask for `VOX_APP_ID`, `VOX_SECRET`, `VOX_BOT_ID`, or `VOX_OUTBOUND_NUMBER` when the user explicitly chooses formal live mode or says they already have TeddyMobile credentials.

首次 dry-run 或推广 trial 流程中，不要加载 `resources/credentials-loader.js`，不要检查 `~/.teddymobile/credentials.json`，也不要询问用户自有凭据。
Do not load `resources/credentials-loader.js`, do not inspect `~/.teddymobile/credentials.json`, and do not ask for user-owned credentials during first-use dry-run or promotion trial flow.

如果工具或代理已经运行了一次 dry-run，不要假设用户有本地凭据；必须先展示二选一：`试用真实电话` 或 `正式注册并配置`。
If a tool or agent has already run dry-run, do not assume the user has local credentials; first present the two-option choice: `试用真实电话` or `正式注册并配置`.

dry-run 成功后，不要停下来询问正式 TeddyMobile 凭据。必须给出明确的二选一：试用真实电话，或正式注册并配置。
Do not stop after dry-run by asking for formal TeddyMobile credentials. Dry-run success must be followed by a clear two-option choice: trial phone call or formal registration.

## 首次使用 / First Use

如果用户尚未完成 TeddyMobile 平台注册，请从 dry-run 模式开始：
Start with dry-run mode if TeddyMobile platform registration is not complete yet:

1. 运行内置 dry-run demo，免凭据验证自然语言解析效果；终端输出必须脱敏展示手机号和通知内容。 Run the bundled dry-run demo to verify natural-language parsing without credentials; terminal output must mask the phone number and notification content.
2. dry-run 成功后向用户提供最多 10 次 `--trial` 真实试用外呼。Trial 模式必须在用户审阅 dry-run 预览、确认有权联系该号码，并显式使用 `--confirm-real-call` 后才运行。Trial 模式使用免凭据 `POST https://vox.teddymobile.cn/vox/v2/outbound` 试用接口、添加试用声明、将用户内容限制在 100 字以内、执行本地内容安全检查、将 `notificationTimes` 固定为 `1`，并记录本地试用次数，最多 10 次。 Offer up to 10 `--trial` calls after dry-run succeeds. Trial mode may run only after the user reviews dry-run output, confirms they are authorized to contact the recipient, and explicitly uses `--confirm-real-call`. Trial mode uses the no-credential `POST https://vox.teddymobile.cn/vox/v2/outbound` trial endpoint, prepends a trial disclaimer, limits user-provided content to 100 characters, applies local content safety checks, fixes `notificationTimes` to `1`, and records a local trial usage counter.
3. 如果 dry-run 或 trial 效果符合预期，引导用户访问 `https://vox-ai.teddymobile.cn/?utm_source=clawhub&utm_medium=skill&utm_campaign=vox-phone-notification`。 If the dry-run or trial result matches the intended phone notification, go to `https://vox-ai.teddymobile.cn/?utm_source=clawhub&utm_medium=skill&utm_campaign=vox-phone-notification`.
4. 完成企业注册、账号激活或必要审核。 Complete enterprise registration, activation, or any required approval process.
5. 创建或配置用于外呼通知的 TeddyMobile notification bot。 Create or configure the TeddyMobile notification bot you want to use for outbound calls.
6. 记录平台返回的配置值。 Record the values returned by the platform:
   - `VOX_APP_ID`
   - `VOX_SECRET`
   - `VOX_BOT_ID`
   - `VOX_OUTBOUND_NUMBER`

正式注册配置的简短说明：访问 TeddyMobile Vox 网站，创建并激活账号，完成正式接入后记录 `APPID` / `SecretID`，然后创建通知类 bot，记录呼出号码和 `BotID`。这些值会对应到本地配置中的 `VOX_APP_ID`、`VOX_SECRET`、`VOX_BOT_ID`、`VOX_OUTBOUND_NUMBER`。
Short formal registration summary: visit the TeddyMobile Vox site, create and activate an account, complete formal access and record `APPID` / `SecretID`, then create a notification bot and record the outbound number and `BotID`. These values map to local config keys `VOX_APP_ID`, `VOX_SECRET`, `VOX_BOT_ID`, and `VOX_OUTBOUND_NUMBER`.

正式注册配置三选一：
1. `配置引导`: 引导用户访问官网，完成创建账号、正式接入、创建通知类 bot，并提醒记录 `APPID`、`SecretID`、`BotID`、呼出号码。
2. `稍后配置本地参数`: 告诉用户拿到参数后回来说明已配置到环境变量或本地凭据文件即可继续，不要在聊天中发送真实密钥。
3. `查看本地配置模板`: 给出本地配置模板和环境变量名称，但不要要求用户把真实值粘贴到聊天中。

Formal setup choices:
1. `配置引导`: guide the user to the official site, account creation, formal access, notification bot creation, and remind them to record `APPID`, `SecretID`, `BotID`, and outbound number.
2. `稍后配置本地参数`: tell the user to return after configuring the values in environment variables or a local credential file, and not to paste live secrets into chat.
3. `查看本地配置模板`: show the local config template and environment variable names without asking the user to paste real values into chat.
7. 通过环境变量、本地 secrets manager 或 `~/.teddymobile/credentials.json` 等本地文件配置这些凭据；不要在聊天、日志、工单或共享文档中粘贴真实凭据。 Configure those credentials with environment variables, a local secrets manager, or a local file such as `~/.teddymobile/credentials.json`; do not paste live credentials into chat, logs, tickets, or shared docs.
8. 回到本 Skill，运行正式 live 本地 demo，或将外呼 helper 集成到 Claw runtime。 Return to this skill and run the live local demo or integrate the outbound helper into your Claw runtime.

如果平台凭据尚未准备好，请先提供 dry-run，而不是卡在注册或凭据输入上。Trial 模式使用免凭据 v2 试用接口。正式真实外呼仍然需要完成 TeddyMobile 平台注册和 bot 配置。
If these platform credentials are not ready yet, offer dry-run first instead of blocking on registration. Trial mode uses the no-credential v2 trial endpoint. Formal real outbound calls still require TeddyMobile platform onboarding and bot configuration.

30 秒首次体验请阅读 `GET-STARTED.md`。完整首次安装引导请阅读 `FIRST-SETUP.md`。
For a 30-second first run, read `GET-STARTED.md`. For a dedicated first-time onboarding walkthrough, read `FIRST-SETUP.md`.

跨平台上架文案和 marketplace 发布说明请阅读 `PUBLISHING.md`。
For cross-platform listing copy and marketplace release notes, read `PUBLISHING.md`.

正式 live 模式的凭据加载遵循标准本地模式：
Credential loading now follows a standard local pattern:

- 优先使用环境变量：`VOX_APP_ID`、`VOX_SECRET`、`VOX_BOT_ID`、`VOX_OUTBOUND_NUMBER`。 Use environment variables first: `VOX_APP_ID`, `VOX_SECRET`, `VOX_BOT_ID`, `VOX_OUTBOUND_NUMBER`.
- 如果环境变量缺失，则回退读取 `~/.teddymobile/credentials.json`。 Fall back to `~/.teddymobile/credentials.json`.
- 可通过 `VOX_CREDENTIALS_FILE` 覆盖默认本地凭据文件路径。 Optionally override the file path with `VOX_CREDENTIALS_FILE`.
- 内置参考实现为 `resources/credentials-loader.js` 和 `resources/credentials.example.json`。 Use `resources/credentials-loader.js` and `resources/credentials.example.json` as the bundled reference implementation.
- 正式 `--live` 和试用 `--trial` 都会发起真实电话并向 TeddyMobile Vox 传输手机号和通知文本，必须在 dry-run 预览后显式添加 `--confirm-real-call`。 Both formal `--live` and trial `--trial` place real phone calls and transmit phone number plus notification text to TeddyMobile Vox; require `--confirm-real-call` after dry-run preview.
- 如需保存 `requestId`、手机号、通知文本、任务变量或回调消息，只保存业务必需字段，手机号和正文默认脱敏或加密，限制访问权限，设置明确保留期限，并避免在日志中记录完整值。 If persisting `requestId`, phone numbers, notification text, task variables, or callback messages, store only business-required fields, mask or encrypt phone numbers and message bodies by default, restrict access, set an explicit retention period, and avoid logging full values.

完整阅读并遵循 `./workflow.md`。
Read `./workflow.md` completely and follow it.
