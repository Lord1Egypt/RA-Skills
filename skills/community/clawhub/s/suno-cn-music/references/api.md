# Suno.cn MCP REST API

所有请求由 `scripts/suno-client.mjs` 发起。基础地址默认是 `https://mcp.suno.cn`，可通过 `SUNO_CN_MCP_URL` 覆盖测试环境。helper 会自动处理网页独立授权和旧版环境变量兼容。新版批准后固定有效 72 小时，以 `authorized_at`、`expires_at` 为准，使用不会续期。

## 通用响应

- HTTP 401 且 `error=authorization_required`：重新执行 `auth start`，网页授权后执行 `auth complete`。
- HTTP 402 且 `error_type=insufficient_credits`：展示 `action.url` 购买入口，链接必须保留 `source=skill`；helper 会保存一个不含凭证的待恢复操作。
- HTTP 429：按提示稍后重试，不要并发轰炸接口。
- HTTP 502/503：服务异常；依据 `error_type` 和 `reauthorize=false` 保留授权，不轮换 Key，不自动重放收费请求。
- HTTP 403 且 `error_type=account_unavailable`：账号当前不可用，不能通过反复授权解决。
- HTTP 409 且 `error_type=permission_context_invalid`：当前团队或权限与批准范围不一致，需重新进行网页确认。
- 任务响应中的 `status`：`0` 排队、`1` 处理中、`2` 成功、`3` 失败。

## 账户

`GET /mcp/api/user`：昵称、积分和会员状态。

退出授权使用 `auth logout`。helper 会调用 `DELETE /mcp/auth/binding` 立即撤销当前 Skill Key 对应的服务端授权，成功后再清除本地凭证；网络失败时会保留凭证以便重试。

购买完成后的恢复命令：

- `purchase status`：刷新账户信息并返回待恢复操作摘要，不提交任务。
- `purchase retry <operation_id>`：仅在用户明确确认后重放一次。
- `purchase clear`：放弃并清除待恢复操作。

`result_unknown` / `operation_state_unknown` 表示网络中断时无法确认是否已提交，必须先查询任务列表，禁止直接重试。

## 音乐生成

`POST /mcp/api/generate`

主要字段：

- `prompt`：AI 描述或自定义歌词。
- `mv`：默认 `chirp-fenix`。可用 `chirp-fenix`、`chirp-crow`、`chirp-bluejay`、`chirp-auk`、`chirp-auk-turbo`、`chirp-v4`、`chirp-v3-5`。
- `title`、`tags`、`custom_mode`、`instrumental`。
- `duration`：仅符合模型和模式要求时传，10-360 秒整数。
- 参考音频创作：`reference_operation`、`continue_serial_no`、`continue_at`、`stem_control_tags`、`vocal_gender`。

参考音频的 `reference_operation` 只能是 `extend`、`add_vocals`、`add_instrumental`、`cover`、`add_stem`。先上传并等待成功，再把返回的参考任务编号放入 `continue_serial_no`。

`GET /mcp/api/task/{serial_no}?wait=0`：查询一个或多个音乐任务，多个编号以逗号分隔。

`GET /mcp/api/music?page=1&page_size=10`：最近生成的音乐；`page_size` 最大 20。

`GET /mcp/api/lyrics/{serial_no}`：获取任务歌词。

`POST /mcp/api/extend`：续写已有歌曲。字段为 `serial_no`、`continue_at`、`mv`。

`POST /mcp/api/gen-lyrics`：生成歌词。字段为 `title`、`style`、`inspiration`，其中 `inspiration` 必填。

## 参考音频上传

使用 helper：

```bash
node scripts/suno-client.mjs upload-reference <mp3文件> <operation> [title] [mode]
```

对应 `POST /mcp/api/upload` multipart 表单，字段为 `file`、`operation`、`title`、`mode`。

`GET /mcp/api/upload/{serial_no}?wait=45`：查询处理状态。只有成功响应中的参考任务编号才可用于生成。

## 格式与音频工具

- `GET /mcp/api/midi/{serial_no}?wait=45`：提取 MIDI。
- `GET /mcp/api/wav/{serial_no}?wait=45`：转换 WAV。
- `POST /mcp/api/improve`：提升音质。
- `POST /mcp/api/tool/{action}`：音频处理或转谱。

音频工具的 `action` 包括：

- `separate`：分离音轨，字段 `path` / `serial_no` / `audio_url`、`type`、`model`。
- `crop-audio`：裁剪，另需 `start`、`end`，可传 `output_format`。
- `denoise`：降噪，可传 `output_format`。
- `merge`：合并，使用 `paths` / `serial_nos` / `audio_urls`，多个值以逗号分隔。
- `music-to-midi`：音频转 MIDI。
- `midi-to-sheet`：MIDI 转乐谱 PDF，字段 `path` 或 `midi_url`。

`wait` 是以上工具接口的 URL 查询参数，不是 JSON 请求体字段，例如 `?wait=45`；单次最大 60 秒。

本地文件先执行：

```bash
node scripts/suno-client.mjs upload-tool <音频或MIDI文件>
```

对应 `POST /mcp/api/tool/upload`。后续工具优先传返回的 `path`。

## 调用示例

```bash
node scripts/suno-client.mjs request POST /mcp/api/generate '{"prompt":"温暖的民谣，木吉他和女声","mv":"chirp-fenix"}'
node scripts/suno-client.mjs request GET '/mcp/api/task/123456?wait=45'
node scripts/suno-client.mjs request POST '/mcp/api/tool/crop-audio?wait=45' '{"path":"upload/path.mp3","start":10,"end":40,"output_format":"mp3"}'
```
