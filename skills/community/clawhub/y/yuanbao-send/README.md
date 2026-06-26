# yuanbao-send

主动向元宝派（Yuanbao Pai）群聊和私聊发送消息和文件，独立于 OpenClaw 插件通道。

## 为什么需要这个

OpenClaw 的 yuanbao 插件通过 WebSocket 收发消息，但只在用户 @bot 时才能回复。
无法从 cron 定时任务、其他 agent session、或后台脚本主动推送消息到群聊或私聊。

本 skill 直接连接 Yuanbao WebSocket 协议，绕过通道限制，实现主动推送（群聊 + 私聊）。

## 前置条件

- Python 3.8+（需包含以下依赖）
- `websocket-client`：`pip install websocket-client`
- `cos-python-sdk-v5`（文件上传需要）：`pip install cos-python-sdk-v5`
- 已在 `~/.openclaw/openclaw.json` 中配置元宝通道（`channels.yuanbao.appKey` + `appSecret`）

> ⚠️ 确保 python3 环境已安装上述依赖，否则文件上传会失败。
> 如系统有多个 Python 版本，可通过修改 send.py 的 shebang 指定。

## 用法

```bash
# 发送群聊文字消息
python3 send.py send <群号> <消息内容>

# 发送私聊文字消息
python3 send.py dm <用户open_id> <消息内容>

# 上传文件并发送（群聊）
python3 send.py upload <群号> <文件路径>

# 上传文件并发送（私聊）
python3 send.py upload-dm <用户open_id> <文件路径>
```

### 示例

```bash
# 群聊文字消息
python3 send.py send 123456789 "任务完成 ✅"

# 私聊文字消息
python3 send.py dm "ou_xxx_open_id" "你好！"

# 群聊上传图片（自动走 TIMImageElem，群内直接预览）
python3 send.py upload 123456789 photo.png

# 私聊上传文件（自动走 TIMFileElem）
python3 send.py upload-dm "ou_xxx_open_id" report.docx
```

### 支持的消息类型

| 命令 | 格式 | 消息类型 |
|------|------|---------|
| `send` / `dm` | 任意文本 | TIMTextElem |
| `upload` / `upload-dm` 图片 | .png .jpg .gif .webp .bmp .heic .tiff .ico | TIMImageElem |
| `upload` / `upload-dm` 文件 | .docx .pptx .xlsx .pdf .txt .zip .wav .mp3 .mp4 .md 等 | TIMFileElem |

> ⚠️ 元宝 Bot 平台仅支持 TIMTextElem、TIMImageElem、TIMFileElem。
> TIMSoundElem 和 TIMVideoFileElem 不支持。音频/视频可通过 TIMFileElem 发送。

### 返回值

```json
{
  "ok": true,
  "code": -1,
  "message": "succ",
  "file": "test.png",
  "type": "TIMImageElem"
}
```

| 字段 | 说明 |
|------|------|
| `ok` | 是否发送成功 |
| `code` | 服务器返回码 |
| `message` | 服务器返回消息 |
| `file` | 文件名（仅 upload） |
| `type` | 消息类型（仅 upload） |

## 工作原理

### 文字消息（群聊 / 私聊）
```
send.py → 签票 → WebSocket → auth-bind → TIMTextElem（send_group / send_c2c）→ 关闭
```

### 文件上传（群聊 / 私聊）
```
send.py → 签票 → /api/resource/genUploadInfo → COS put_object → WebSocket → TIMImageElem / TIMFileElem → 关闭
```

1. **签票**：用 appKey + appSecret 通过 HMAC-SHA256 签名获取临时 token
2. **获取上传凭证**：调用 `/api/resource/genUploadInfo` 获取 COS 临时凭证
3. **COS 上传**：使用 cos-python-sdk-v5 上传文件到腾讯云 COS
4. **发送消息**：通过 WebSocket 发送包含 resourceUrl 的文件消息

## 安全

- 读取本地 `openclaw.json` 中的 `appKey` / `appSecret`
- 不存储、不传输任何凭证到第三方
- 签票请求走 HTTPS

## 限制

- 需要 bot 已加入目标群
- 独立运行，不写入 OpenClaw session 日志
- WebSocket 连接是临时的（每次发送都重新连接）
- 文件大小限制由元宝平台决定（通常 20MB）
- TIMSoundElem / TIMVideoFileElem 不支持
- **⚠️ 与 OpenClaw 插件冲突：** send.py 使用与插件相同的 bot_id 建立 WebSocket 连接，会导致插件现有连接被踢（`code=4014 instanceid conflict`）。插件需等待 health-monitor 重启（约 15 分钟）才能恢复接收消息。建议仅在插件不需要活跃时使用（如 cron 定时推送、后台通知），避免频繁调用。
