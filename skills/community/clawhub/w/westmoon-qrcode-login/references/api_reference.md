# 西之月扫码登录 API 速查

## 1. 获取登录二维码

- 接口：`GET https://api-x.westmonth.com/umc/miniprogram/qrcode/generate`
- 关键参数：
  - `client_id`
  - `scene=login`
  - `path=p-user/pages/login/index`
  - `envVersion=release`
  - `source=PCLogin`

返回关键字段：

- `data.scan_token`
- `data.wxacode`
- `data.expires_in`
- `data.poll_interval`

说明：

- `scan_token` 是后续轮询依赖的参数
- `wxacode` 是 `data:image/png;base64,...` 格式，需要解码成图片

## 2. 轮询扫码状态

- 接口：`GET https://api-x.westmonth.com/umc/miniprogram/qrcode/poll`
- 参数：
  - `scan_token`
  - `source=xpw`

成功确认后返回关键字段：

- `data.status`
- `data.access_token`
- `data.refresh_token`
- `data.expires_in`
- `data.token_type`

常见状态建议：

- `waiting` / `pending`：继续轮询
- `scanned`：已扫码，等待用户确认
- `confirmed` / `success`：登录成功
- `expired` / `invalid`：二维码失效，需要重新生成

## 3. 校验登录态并读取用户信息

- 接口：`GET https://api-x.westmonth.com/umc/user/user/info`
- Header：`Authorization: Bearer <token>`

规则：

- HTTP 200：token 有效
- HTTP 401：token 无效，需要重新登录

## 本 Skill 的默认行为

- 默认展示二维码后立即返回，不持续占用当前对话
- 默认将 `scan_token` 写入 pending 文件，等待后续 `--continue` 或 `--poll`
- `--blocking` 模式下每 5 秒轮询一次状态接口
- 将二维码落盘到 `~/.westmoon-user-login/qr_codes/`
- 将 token 落盘到 `~/.westmoon-user-login/tokens.json`
- 将待轮询的 `scan_token` 落盘到 `~/.westmoon-user-login/pending_login.json`
