# SkillHub Publishing Notes

Use this file when publishing `vox-phone-notification` to `https://skillhub.cn`.

## Recommended listing position

Publish this skill as a formal TeddyMobile Vox notification skill for developers, solution teams, and advanced operators who have completed TeddyMobile platform onboarding.

Recommended positioning:

- TeddyMobile Vox phone notification skill
- no-credential dry-run experience before platform registration
- promotion-period trial calls through the no-credential v2 endpoint, with a disclaimer and content safety checks
- Claw / OpenClaw / WorkBuddy outbound call notification integration
- validated outbound playback after TeddyMobile platform registration and bot configuration

## What is verified

- skill package structure is complete
- no-credential dry-run parsing is available before registration
- promotion trial mode supports local content safety checks and local usage counter
- natural-language parsing helper works
- TeddyMobile HMAC signing works
- outbound request submission succeeds
- request body includes `extra.notification.text` when `notificationText` is provided
- live outbound calls have been tested successfully with audible playback

## Release prerequisite

Dry-run use does not require TeddyMobile platform registration. Promotion packages can include up to 10 local trial calls through the no-credential v2 endpoint, with a trial disclaimer and local content safety checks. Successful formal outbound calling requires the operator to complete TeddyMobile platform registration, bot configuration, and outbound capability setup before using the skill in production.

Possible platform-side requirements:

- notification bot type must be enabled for the chosen `botid`
- direct playback from `extra.notification.text` must be supported
- callback/SSE mode may still be required for some bot configurations

## Recommended listing title

`TeddyMobile Vox 电话通知 Skill`

## Recommended short description

`把一句话变成电话提醒：未注册 TeddyMobile 也可先 dry-run 体验解析；推广包最多可通过免凭据 v2 接口试用 10 次真实电话，试用电话会添加声明、进行本地内容安全检查，正式外呼需完成 Vox 注册和 bot 配置。 Turn one sentence into a phone notification: try dry-run parsing before TeddyMobile registration, use up to 10 promotion trial calls when included, and complete Vox registration and bot setup for formal outbound calls.`

## Recommended long description

`本 Skill 用于 TeddyMobile Vox 电话通知外呼场景。用户可以先通过 dry-run 模式体验自然语言解析效果，例如输入“给<接收手机号>发通知，明天10点开会”，Skill 会解析出接收号码、播报内容和通知次数，不会发起真实电话。推广包还可提供最多 10 次本地 trial 真实电话试用，试用电话会添加 TeddyMobile Vox 试用声明、进行本地内容安全检查、最多保留 100 字用户内容，并固定播报 1 次。确认效果后，用户可访问 https://vox-ai.teddymobile.cn/?utm_source=clawhub&utm_medium=skill&utm_campaign=vox-phone-notification 注册 TeddyMobile 开发者账号、创建 Vox 通知 bot，并配置 VOX_APP_ID、VOX_SECRET、VOX_BOT_ID、VOX_OUTBOUND_NUMBER，用于正式电话外呼。适用于会议提醒、账单提醒、服务通知等单轮电话通知场景。 This skill is designed for TeddyMobile Vox outbound phone notification scenarios. Users can first try dry-run mode before registration, reviewing the parsed phone number, spoken notification text, and repeat count without placing a real call. Promotion builds can include up to 10 local trial calls through the no-credential v2 endpoint with a TeddyMobile Vox trial disclaimer, local content safety checks, up to 100 characters of user-provided content, and one playback. After confirming the value, users can register at https://vox-ai.teddymobile.cn/?utm_source=clawhub&utm_medium=skill&utm_campaign=vox-phone-notification, create a Vox notification bot, and configure VOX_APP_ID, VOX_SECRET, VOX_BOT_ID, and VOX_OUTBOUND_NUMBER for formal outbound phone calls. It is a good fit for meeting reminders, billing reminders, service notifications, and other single-turn notification workflows.`

## Recommended tags

- TeddyMobile
- Vox
- 电话通知
- Claw
- WorkBuddy
- OpenClaw
- 语音通知
- 商用发布

## Recommended usage note

State clearly in the listing: `用户可先 dry-run 体验解析；推广包可通过免凭据 v2 接口提供最多 10 次真实电话试用，试用电话会添加声明、进行本地内容安全检查；正式外呼需要完成 TeddyMobile 平台注册和 Vox bot 配置。本 Skill 适合开发者、解决方案工程师或需要将 TeddyMobile Vox 集成到自有运行时的高级用户。 Users can try dry-run parsing first; promotion builds can provide up to 10 real trial calls through the no-credential v2 endpoint with a disclaimer and local content safety checks; formal outbound calls require TeddyMobile platform registration and Vox bot configuration. This skill is intended for developers, solution engineers, or advanced users integrating TeddyMobile Vox into their own runtime.`

## Recommended credential note

Add a short note in the listing or reviewer remarks explaining the credential model:

- this skill supports environment variables first: `VOX_APP_ID`, `VOX_SECRET`, `VOX_BOT_ID`, `VOX_OUTBOUND_NUMBER`
- it also supports local fallback from `~/.teddymobile/credentials.json`
- `VOX_CREDENTIALS_FILE` can override the default local credential file path
- real secrets are not bundled in the uploaded zip; only an example credential file is included

Suggested Chinese wording:

`本 Skill 采用环境变量优先、本地凭据文件兜底的配置方式。支持通过 VOX_APP_ID、VOX_SECRET、VOX_BOT_ID、VOX_OUTBOUND_NUMBER 直接注入配置；也支持从 ~/.teddymobile/credentials.json 读取本地凭据，并可通过 VOX_CREDENTIALS_FILE 自定义凭据文件路径。上传包中仅包含示例凭据文件，不包含任何真实密钥。`

## Suggested upload artifact

Upload the packaged zip file:

`skills/vox-phone-notification.zip`
