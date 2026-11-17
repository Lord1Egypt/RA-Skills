---
slug: suno-cn-music
displayName: Suno.cn AI 音乐助手
display_name: Suno.cn AI 音乐助手
display_name_en: Suno.cn AI Music Assistant
description_zh: Suno.cn AI 音乐创作助手，支持 AI 作曲写歌、文字生成歌曲、歌词生成、参考音频翻唱与续写、添加人声或伴奏、纯音乐与 BGM 生成、人声及音轨分离、音频降噪裁剪合并、音质提升、WAV 转换、音频转 MIDI、MIDI 转乐谱 PDF，以及作品和积分查询。首次使用通过网页确认三天授权，无需手填 API Key；部分功能消耗账户积分。
description_en: Suno.cn AI music and song generator for AI agents. Create songs from text or lyrics, write lyrics, make instrumental music and background music (BGM), cover or extend reference audio, and add vocals, accompaniment or stems. Supports vocal and stem separation, audio denoising, trimming, merging, quality enhancement, WAV conversion, audio-to-MIDI, MIDI-to-PDF sheet music, and music library and credit queries. Uses three-day web authorization without manual API key entry. Some operations consume account credits.
summary: Suno.cn AI 音乐创作助手：文字生成歌曲、AI 作曲写歌、歌词生成、参考音频翻唱与续写、纯音乐和伴奏生成、人声分离、音频降噪、MIDI 与乐谱转换。支持 Agent 网页授权接入。
homepage: https://www.suno.cn
tags: [AI音乐, AI作曲, AI写歌, 歌词生成, AI翻唱, 歌曲续写, BGM, 伴奏生成, 人声分离, 音频处理, MIDI, Suno]
name: suno-cn-music
description: Suno.cn AI 音乐助手（AI Music Generator / Song Generator）。当用户需要 AI 作曲、AI 写歌、文字生成音乐、歌词生成歌曲、自动作词、参考音频翻唱（Cover）、歌曲续写（Extend）、添加人声或伴奏、添加音轨、生成纯音乐、制作短视频 BGM 或播客背景音乐时使用；也适用于人声伴奏分离、音轨分离（Stem Separation）、音频裁剪合并、音频降噪、音质提升、音频转 MIDI、MIDI 转乐谱 PDF、WAV 转换、作品查询和积分查询。首次使用通过网页确认三天授权，无需手填 API Key；部分功能消耗账户积分。所有网络请求必须通过随 Skill 提供的 helper 发起。
version: 2.3.1
---

# Suno.cn AI 音乐助手

本 Skill 使用网页明确批准的独立授权，不要求用户复制 API Key。新版授权自批准起固定有效三天，使用不会续期；旧授权以服务端显示的实际期限为准。执行网络请求时只能调用 `scripts/suno-client.mjs`，不要使用 curl、MCP JSON-RPC、浏览器脚本或自行拼接 Authorization。

## 功能与适用场景

Suno.cn AI 音乐助手将音乐创作和音频处理接入支持 Skill 的 Agent，通过自然语言描述需求，再由 helper 调用平台能力。

- **AI 作曲与歌曲生成**：根据文字描述或自定义歌词生成歌曲，支持歌曲名称、音乐风格及纯音乐模式。适合写歌、歌词配曲、短视频配乐、播客背景音乐、游戏 BGM 和广告配乐等创作需求。
- **AI 作词与歌词生成**：根据主题、风格和灵感生成歌词，也可查询已生成歌曲的歌词。
- **参考音频创作**：上传参考音频并等待准备完成后，进行翻唱（Cover）、续写（Extend）、添加人声、添加伴奏或添加音轨。
- **人声与音轨分离**：分离人声、伴奏或音轨（Stem Separation），用于后续音频编辑。
- **音频编辑与格式转换**：音频降噪、裁剪、合并、音质提升、WAV 转换、音频转 MIDI、MIDI 转乐谱 PDF。
- **作品与账户管理**：查询生成进度、最近作品、歌词、账户积分及会员状态。

### 用户可能这样表达

- “帮我写一首温暖的民谣，先生成歌词，再生成歌曲。”
- “给短视频做一段轻快的纯音乐 BGM，不要人声。”
- “用我上传的参考音频翻唱，或者从指定位置续写这首歌。”
- “给这段伴奏添加人声，或者给这段人声添加伴奏。”
- “把人声和伴奏分离，再裁剪音频、去除噪声。”
- “把音乐转成 MIDI，再将 MIDI 转为乐谱 PDF。”
- “查看我的积分、最近生成的歌曲和当前任务进度。”

具体模型、输入格式、可用参数和处理结果以服务端接口为准。需要 Suno.cn 账号，部分操作消耗积分；这些创作场景不代表对生成效果或作品商用权利作出承诺。

## 安装与完整性边界

- 宿主 Agent 可以根据自身官方机制决定安装目录、重新加载方式和启用步骤。
- 必须完整保留 Skill 目录名称 `suno-cn-music` 以及 `SKILL.md`、`INSTALL.md`、`references/`、`scripts/` 和安装脚本。
- 不得改写、生成替代版本或删除 `SKILL.md`、`references/api.md`、`scripts/suno-client.mjs`；登录、购买、任务重试、API 路径和凭证保护规则均不得修改。
- 若宿主无法确定安装目录，应先询问用户，不得猜测路径。安装细则见 [INSTALL.md](INSTALL.md)。

## 安全规则

- 不读取、展示、复述或记录 Skill Key、网站 Token、`SUNO_CN_API_KEY` 的值。
- 不输出 helper 的凭证文件内容；不要要求用户打开 `~/.suno-cn/credentials.json`。
- 不把凭证放入命令行参数、对话、日志、URL query 或生成文件。
- 错误排查只使用 helper 返回的脱敏结构，不追加请求头或原始响应转储。
- `SUNO_CN_API_KEY` 仅由 helper 作为旧版本兼容回退读取，不主动要求用户配置。

## 调用方式

在本 Skill 根目录执行：

```bash
node scripts/suno-client.mjs <command> [...args]
```

所有命令都输出 JSON。只根据 JSON 的 `status`、`error`、`message` 和 `action` 决定下一步。

## 首次授权与重新授权

1. 首次业务请求前执行 `auth status`。
2. 若不是 `authorized`，执行 `auth start`。
3. 把返回的 `action.url` 作为可点击链接提供给用户，并请用户在网页完成登录和授权。
4. 用户确认完成后执行 `auth complete`。只有返回 `authorized` 才重试原业务请求。
5. 若业务请求返回 `authorization_required`，按相同步骤重新授权，不要猜测凭证问题。
6. 若用户要求退出授权，执行 `auth logout`。该命令会先撤销服务端授权，再清除本地凭证；不要手工删除或打印凭证。

```bash
node scripts/suno-client.mjs auth status
node scripts/suno-client.mjs auth start
node scripts/suno-client.mjs auth complete
node scripts/suno-client.mjs auth logout
```

授权链接短时有效。`denied` 表示用户拒绝，`expired` 表示链接过期；这两种情况都要重新执行 `auth start`。

`auth complete [seconds]` 会阻塞等待网页批准，默认等待 180 秒，最大 600 秒。等待超时不表示三天授权到期；可执行 `auth status` 确认状态。pending 链接默认 600 秒，其倒计时不会因维护或重新加载而重置。

新版授权不受网页刷新、关闭或普通退出登录影响。要撤销音乐助手访问，请执行 `auth logout` 或在网站的授权管理中撤销；已接受任务继续执行。`authorization_paused`、`internal_credential_invalid`、`upstream_authorization_failed`、`authorization_record_invalid`、`permission_service_unavailable` 是服务异常，保留当前凭证并稍后重试查询，不要求用户反复授权，也不自动重放收费操作。`account_unavailable` 应按账号不可用处理；只有明确的 `permission_context_invalid` 才要求用户重新确认授权范围。

## 账户与积分

```bash
node scripts/suno-client.mjs account
```

当业务响应为 `insufficient_credits` 时，helper 会把待恢复操作保存到本机 `~/.suno-cn/pending-operation.json`，文件权限为 `0600`，其中不包含 Skill Key、Token 或请求头。向用户说明积分不足，并原样提供 `action.url`；该链接已包含 `source=skill`，不得删除、覆盖或替换来源参数。

用户表示购买完成后，先执行：

```bash
node scripts/suno-client.mjs purchase status
```

此命令只刷新账户信息并返回待操作摘要，不会自动重放收费请求。必须把余额和待恢复操作告诉用户并再次确认；得到明确同意后，才执行返回提示中的 `purchase retry <operation_id>`。该命令最多提交一次。若返回 `result_unknown` 或 `operation_state_unknown`，必须先查询任务列表确认是否已提交，禁止直接重试。无需恢复时可执行 `purchase clear`。

## 业务请求

通用 JSON 请求：

```bash
node scripts/suno-client.mjs request GET /mcp/api/task/任务编号
node scripts/suno-client.mjs request POST /mcp/api/generate '{"prompt":"轻快的城市流行歌曲","mv":"chirp-fenix"}'
```

只允许 `/mcp/api/` 路径和 GET/POST 方法。参数、状态轮询、模型枚举和完整端点见 [references/api.md](references/api.md)。

上传本地参考音频：

```bash
node scripts/suno-client.mjs upload-reference ./demo.mp3 cover "歌曲名称"
```

`operation` 只能是 `extend`、`add_vocals`、`add_instrumental`、`cover`、`add_stem`。提交后必须继续查询 `/mcp/api/upload/{serial_no}`，直到成功或失败。

上传音频处理文件：

```bash
node scripts/suno-client.mjs upload-tool ./demo.mp3
```

后续音频工具优先使用返回的 `path`，不要重复上传。

## 任务处理

- 创建类接口返回任务编号不代表任务成功，必须按 API 参考轮询。
- 任何收费操作都不得在购买后自动重放；先用 `purchase status` 查余额，再取得用户明确确认。
- 等待时间优先使用接口支持的 `wait` 参数，单次不超过 60 秒。
- 失败时向用户展示服务端返回的业务原因；不要把失败描述为成功或继续无期限轮询。
- 返回音频、MIDI、WAV 或 PDF 链接时，直接提供给用户。
- 不确定字段时先读取 `references/api.md`，不要发明接口、字段或模型名。

## 版本

当前 Skill 版本：`2.3.1`。可执行以下命令检查服务端版本：

```bash
node scripts/suno-client.mjs version
```
