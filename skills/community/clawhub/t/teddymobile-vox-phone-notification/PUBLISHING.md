# Publishing Guide

Use this file when publishing `vox-phone-notification` to SkillHub-style marketplaces, plugin hubs, internal skill catalogs, or Claw-compatible distribution platforms.

## Publishing position

Recommended release position:

- formal TeddyMobile Vox phone notification skill
- suitable for Claw, OpenClaw, WorkBuddy, and compatible runtimes
- intended for developers, integrators, enterprise automation teams, and solution delivery teams

## Core value proposition

This skill provides:

- no-credential dry-run parsing before platform registration
- promotion-period trial calls through the no-credential v2 endpoint, with a trial disclaimer and content safety checks
- TeddyMobile Vox outbound phone notification integration after registration
- natural-language parsing for chat-style notification instructions
- HMAC-signed outbound request generation
- local credential loading with environment variables and file fallback
- first-time onboarding documentation and runnable local demo
- verified real-world outbound call playback after platform registration and bot configuration

## Recommended Chinese listing title

`TeddyMobile Vox 电话通知 Skill`

## Recommended English listing title

`TeddyMobile Vox Phone Notification Skill`

## Recommended Chinese short description

`把一句话变成电话提醒：未注册 TeddyMobile 也可先 dry-run 体验解析；推广包最多可通过免凭据 v2 接口试用 10 次真实电话，试用电话会添加声明、进行本地内容安全检查，正式外呼需完成 Vox 注册和 bot 配置。`

## Recommended English short description

`Turn a natural-language request into a phone notification. Try parsing with dry-run before registration, use a no-credential v2 promotion trial call when included, then connect TeddyMobile Vox credentials for formal outbound calls.`

## Recommended combined short description

`把一句话变成电话提醒：未注册 TeddyMobile 也可先 dry-run 体验解析；推广包最多可通过免凭据 v2 接口试用 10 次真实电话，试用电话会添加声明、进行本地内容安全检查，正式外呼需完成 Vox 注册和 bot 配置。 Turn a natural-language request into a phone notification: try dry-run parsing before registration, use up to 10 no-credential v2 promotion trial calls when included, then connect TeddyMobile Vox credentials for formal outbound calls.`

## Recommended Chinese long description

`本 Skill 用于 TeddyMobile Vox 电话通知外呼场景。用户可以先通过 dry-run 模式体验自然语言解析效果，例如输入“给<接收手机号>发通知，明天10点开会”，Skill 会解析出接收号码、播报内容和通知次数，不会发起真实电话。推广包还可提供最多 10 次本地 trial 真实电话试用，试用电话会添加 TeddyMobile Vox 试用声明、进行本地内容安全检查、最多保留 100 字用户内容，并固定播报 1 次。确认效果后，用户可注册 TeddyMobile 开发者账号、创建 Vox 通知 bot，并配置 VOX_APP_ID、VOX_SECRET、VOX_BOT_ID、VOX_OUTBOUND_NUMBER，用于正式电话外呼。适用于会议提醒、账单提醒、服务通知等单轮电话通知场景。`

## Recommended English long description

`This skill is designed for TeddyMobile Vox outbound phone notification scenarios. Users can first try dry-run mode before registration, for example by entering a request like "notify <destination phone number> about tomorrow's 10 AM meeting" and reviewing the parsed phone number, spoken notification text, and repeat count without placing a real call. Promotion builds can also include up to 10 local trial calls through the no-credential v2 endpoint with a TeddyMobile Vox trial disclaimer, local content safety checks, up to 100 characters of user-provided content, and one playback. After confirming the value, users can register a TeddyMobile developer account, create a Vox notification bot, and configure VOX_APP_ID, VOX_SECRET, VOX_BOT_ID, and VOX_OUTBOUND_NUMBER to place formal outbound phone calls. It is a good fit for meeting reminders, billing reminders, service notifications, and other single-turn phone notification workflows.`

## Recommended combined long description

`本 Skill 用于 TeddyMobile Vox 电话通知外呼场景。用户可以先通过 dry-run 模式体验自然语言解析效果，例如输入“给<接收手机号>发通知，明天10点开会”，Skill 会解析出接收号码、播报内容和通知次数，不会发起真实电话。推广包还可提供最多 10 次本地 trial 真实电话试用，试用电话会添加 TeddyMobile Vox 试用声明、进行本地内容安全检查、最多保留 100 字用户内容，并固定播报 1 次。确认效果后，用户可访问 https://vox-ai.teddymobile.cn/?utm_source=clawhub&utm_medium=skill&utm_campaign=vox-phone-notification 注册 TeddyMobile 开发者账号、创建 Vox 通知 bot，并配置 VOX_APP_ID、VOX_SECRET、VOX_BOT_ID、VOX_OUTBOUND_NUMBER，用于正式电话外呼。适用于会议提醒、账单提醒、服务通知等单轮电话通知场景。 This skill is designed for TeddyMobile Vox outbound phone notification scenarios. Users can first try dry-run mode before registration, reviewing the parsed phone number, spoken notification text, and repeat count without placing a real call. Promotion builds can include up to 10 local trial calls through the no-credential v2 endpoint with a TeddyMobile Vox trial disclaimer, local content safety checks, up to 100 characters of user-provided content, and one playback. After confirming the value, users can register at https://vox-ai.teddymobile.cn/?utm_source=clawhub&utm_medium=skill&utm_campaign=vox-phone-notification, create a Vox notification bot, and configure VOX_APP_ID, VOX_SECRET, VOX_BOT_ID, and VOX_OUTBOUND_NUMBER for formal outbound phone calls. It is a good fit for meeting reminders, billing reminders, service notifications, and other single-turn notification workflows.`

## Recommended tags

- TeddyMobile
- Vox
- 电话通知
- 外呼
- Claw
- OpenClaw
- WorkBuddy
- 语音通知
- 企业集成

## Recommended version

`1.0.0`

## Recommended release notes

Chinese:

`发布 TeddyMobile Vox 电话通知正式版 Skill，支持自然语言通知解析、dry-run 脱敏输出、HMAC 签名外呼、环境变量与本地凭据文件加载、首次安装引导、本地演示和真实外呼播报验证。`

English:

`Release the production version of the TeddyMobile Vox phone notification skill with natural-language notification parsing, HMAC-signed outbound calls, environment-variable and local credential-file loading, first-time setup guidance, local demo tools, and verified real-world playback.`

## Recommended platform note

Use this note when a marketplace asks for prerequisites or reviewer remarks:

Chinese:

`未完成 TeddyMobile 注册时可使用 dry-run 体验 Skill 解析能力；推广包可通过免凭据 v2 接口提供最多 10 次本地 trial 真实电话试用，试用会添加声明、进行本地内容安全检查。正式外呼需要完成 TeddyMobile 平台注册、企业开通或审核、bot 配置和外呼能力准备。正式配置时请通过环境变量或本地凭据文件注入 VOX_APP_ID、VOX_SECRET、VOX_BOT_ID、VOX_OUTBOUND_NUMBER 等参数。`

English:

`Users can try this skill in dry-run mode before TeddyMobile registration. Promotion builds can include up to 10 local trial calls through the no-credential v2 endpoint, with a disclaimer and local content safety checks. Formal outbound calls require TeddyMobile platform registration, any required enterprise enablement or review, bot configuration, and outbound calling setup. Configure VOX_APP_ID, VOX_SECRET, VOX_BOT_ID, VOX_OUTBOUND_NUMBER, and related values through environment variables or a local credentials file.`

Combined:

`未完成 TeddyMobile 注册时可使用 dry-run 体验 Skill 解析能力；推广包可通过免凭据 v2 接口提供最多 10 次本地 trial 真实电话试用，试用会添加声明、进行本地内容安全检查。正式外呼需要完成 TeddyMobile 平台注册、企业开通或审核、bot 配置和外呼能力准备。正式配置时请通过环境变量或本地凭据文件注入 VOX_APP_ID、VOX_SECRET、VOX_BOT_ID、VOX_OUTBOUND_NUMBER 等参数。 Users can try this skill in dry-run mode before TeddyMobile registration. Promotion builds can include up to 10 local trial calls through the no-credential v2 endpoint, with a disclaimer and local content safety checks. Formal outbound calls require TeddyMobile platform registration, any required enterprise enablement or review, bot configuration, and outbound calling setup. Configure VOX_APP_ID, VOX_SECRET, VOX_BOT_ID, VOX_OUTBOUND_NUMBER, and related values through environment variables or a local credentials file.`

## Packaging checklist

- ensure the zip contains the top-level folder `vox-phone-notification/`
- include `SKILL.md`, `README.md`, `GET-STARTED.md`, `FIRST-SETUP.md`, `workflow.md`, and `skill.json`
- include only example credentials, never real secrets
- keep helper scripts and demo files inside `resources/`
- upload `skills/vox-phone-notification.zip` or a hosted HTTPS copy of it

## Suggested screenshots or media

If the marketplace supports screenshots, consider showing:

- the first-time setup guide in `FIRST-SETUP.md`
- the 30-second dry-run guide in `GET-STARTED.md`
- the local demo command and output
- the natural-language input example
- the generated normalized notification payload

## Related files

- `SKILL.md`
- `README.md`
- `FIRST-SETUP.md`
- `SKILLHUB.md`
- `WORKBUDDY-RELEASE.md`
- `skill.json`
