# 完整搭建指南 + 踩坑记录

这是 2026-03-25 从零搭建这个 skill 的完整经验。下次照着做，不用再踩坑。

## 一、依赖安装

```bash
pip3 install youtube-transcript-api openai --break-system-packages
```

只需要这两个包。不需要 Docker、不需要 RSSHub。

## 二、获取用户的 YouTube 订阅列表

### Google Takeout 导出（推荐）

1. 打开 https://takeout.google.com
2. 点 **取消全选**（把所有勾全去掉）
3. 往下找 **YouTube 和 YouTube Music**，勾上
4. ⚠️ 关键步骤：点旁边的 **「所有 YouTube 数据已包含」** 按钮
5. 弹出窗口里 → **取消全选** → 只勾 **订阅内容**
6. 确定 → 下一步 → 导出一次 → 下载 zip

**踩坑：** 如果跳过第 4、5 步，只会下载一个 `archive_browser.html` 索引页，不含实际 CSV 数据。必须点进去手动只选「订阅内容」。

解压后 CSV 在 `Takeout/YouTube 和 YouTube Music/订阅内容/订阅内容.csv`，格式：
```
频道 ID,频道网址,频道标题
UCSHZKyawb77ixDdsGog4iWA,http://www.youtube.com/channel/UCSHZKyawb77ixDdsGog4iWA,Lex Fridman
```

⚠️ zip 文件名含中文路径，macOS 解压可能报错。用 Python 解压：
```python
import zipfile
z = zipfile.ZipFile('takeout.zip')
for name in z.namelist():
    data = z.read(name)
    print(data.decode('utf-8'))
```

### 手动获取 channel_id

频道页 URL 格式：`youtube.com/channel/UCxxxxxx` → `UCxxxxxx` 就是 channel_id。
或者：频道页 → 查看源码 → 搜索 `channelId`。

## 三、YouTube RSS

**不需要 RSSHub / Docker。** YouTube 自带原生 Atom feed：

```
https://www.youtube.com/feeds/videos.xml?channel_id=UC频道ID
```

直接用这个就能拿到最新视频列表，免费无限制。

**踩坑：** 最早用了 RSSHub 公共实例 `rsshub.app`，返回 403，需要自建。后来发现 YouTube 原生 RSS 完全够用，不需要 RSSHub。

## 四、字幕获取

### 方案一：youtube-transcript-api（推荐）

```python
from youtube_transcript_api import YouTubeTranscriptApi
api = YouTubeTranscriptApi()
segments = api.fetch(video_id, languages=('en',))
text = ' '.join(seg.text for seg in segments)
```

**踩坑 1：API 版本差异**
- 旧版用 `YouTubeTranscriptApi.list_transcripts(video_id)` → 新版报错
- 新版用 `api = YouTubeTranscriptApi()` 然后 `api.fetch(video_id)` 和 `api.list(video_id)`
- 检查方法签名：`import inspect; print(inspect.signature(YouTubeTranscriptApi.fetch))`

**踩坑 2：IP 限流（429 Too Many Requests）**
- 短时间内请求太多次会被 YouTube 封 IP，通常 30-60 分钟恢复
- 正常每天跑一次（13 个频道 = 13 次请求）不会触发
- 测试时用 2 个频道，别用全部 13 个反复跑
- 每个请求间隔 2 秒（`time.sleep(2)`）

**踩坑 3：IP 限流不影响其他用户**
每个用户在自己电脑上跑，用自己的 IP，彼此完全独立。

### 方案二：yt-dlp（备用）

```bash
yt-dlp --write-sub --write-auto-sub --sub-lang en --skip-download --sub-format vtt -o /tmp/sub "https://www.youtube.com/watch?v=VIDEO_ID"
```

同样会受 IP 限流影响，作为 youtube-transcript-api 的备用。

### 不推荐：Supadata API

收费，有免费额度但用完要花钱，不适合做给别人用的 skill。

## 五、AI 摘要生成

通过 OpenClaw Gateway 调用 Claude，不需要单独的 API key：

```python
from openai import OpenAI
client = OpenAI(api_key=gateway_token, base_url="http://localhost:18789/v1")
response = client.chat.completions.create(model="anthropic/claude-sonnet-4-6", ...)
```

Gateway token 和端口从 `~/.openclaw/openclaw.json` 自动读取：
- `gateway.port` → 端口（默认 18789）
- `gateway.auth.token` → token

**摘要 prompt 要点：**
- 返回纯文本，不要 JSON（JSON 格式的引号和花括号容易混进飞书卡片）
- 第一行是中文标题翻译，第二行开始是梗概
- 梗概 150-250 字，点明嘉宾身份 + 2-3 个具体观点

## 六、飞书推送

### 消息格式：互动卡片（interactive）

飞书 post 类型（富文本）格式校验非常严格，容易报 `230001 invalid message content`。
**用互动卡片（msg_type: interactive）代替**，支持 lark_md 渲染 Markdown，效果更好。

```python
card = {
    "config": {"wide_screen_mode": True},
    "header": {
        "title": {"content": "📺 YouTube 每日更新 · 日期 · 共 N 个新视频", "tag": "plain_text"},
        "template": "blue"
    },
    "elements": [
        {"tag": "div", "text": {"tag": "lark_md", "content": "**1. 频道名**\n[标题](链接)\n中文翻译\n\n梗概"}},
        {"tag": "hr"},
        ...
    ]
}
```

### 飞书 API 注意事项

- 获取 tenant_access_token：`POST /auth/v3/tenant_access_token/internal`
- 发消息：`POST /im/v1/messages?receive_id_type=open_id`
- 文本消息有长度限制，长内容用文件附件或卡片
- 上传文件：用 `curl -F` multipart 形式，不能用 urllib

### 获取 user_open_id

飞书开放平台 → 你的 app → 看 bot 收到的消息 → sender 里的 `open_id`（以 `ou_` 开头）。
或者在 OpenClaw 的 inbound metadata 里看 `sender_id`。

## 七、定时任务

```bash
openclaw cron add \
  --name "youtube-daily-digest" \
  --cron "0 11 * * *" \
  --tz "America/New_York" \
  --description "每日 YouTube 播客摘要推送" \
  --message "cd SKILL_DIR && FEISHU_USER_OPEN_ID=用户open_id python3 scripts/digest.py" \
  --session isolated \
  --timeout 600000 \
  --announce \
  --channel feishu
```

- `--session isolated`：不占用主 session
- `--timeout 600000`：10 分钟超时（13 个频道需要时间）
- `--announce --channel feishu`：完成后通知飞书

## 八、常见问题

**Q：报 `No module named youtube_transcript_api`**
A：`pip3 install youtube-transcript-api --break-system-packages`

**Q：字幕全部失败（429 Too Many Requests）**
A：IP 被 YouTube 限流了，等 30-60 分钟恢复。正常每天跑一次不会触发。

**Q：飞书报 `230001 invalid message content`**
A：不要用 `msg_type: post`，改用 `msg_type: interactive`（互动卡片）。

**Q：飞书报 `234008 The app is not the resource sender`**
A：Bot 没有下载用户发送的文件的权限。需要在飞书开放平台开通 `im:resource` 权限并发布新版本。

**Q：摘要里混进了 JSON 字符（花括号、引号）**
A：prompt 里要求返回纯文本，不要 JSON 格式。
