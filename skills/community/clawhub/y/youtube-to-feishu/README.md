# 🎵 YouTube to Feishu

OpenClaw 技能 - 自动下载 YouTube 视频音频并上传到飞书云盘，然后发送给用户。

## 功能

- 📹 **YouTube 下载** - 使用 yt-dlp 提取音频
- 🎵 **MP3 转换** - 自动转换为 192K MP3 格式
- ☁️ **飞书云盘** - 上传到用户飞书云盘
- 📬 **即时推送** - 发送交互式卡片到飞书对话
- 🧹 **自动清理** - 清理临时文件（保留最近下载）

## 安装

### 1. 依赖安装

```bash
# 安装 yt-dlp
pip install yt-dlp

# 确认 Python 3.8+
python --version
```

### 2. 技能安装

技能已放置在：
```
~/.openclaw/workspace/skills/youtube-to-feishu/
```

### 3. 飞书授权

需要以下飞书权限：
- `feishu_drive_file` - 云盘文件上传
- `feishu_im_user_message` - 发送消息

## 使用方法

### 在 OpenClaw 对话中

直接发送 YouTube 链接：

```
下载这个 YouTube 音频到飞书：https://www.youtube.com/watch?v=dyJUscv7b9g
```

或

```
把这个视频转 MP3 存到飞书：https://youtu.be/VIDEO_ID
```

### 命令行使用

```bash
# 完整流程（需要 OpenClaw 环境）
python youtube_to_feishu_complete.py --url <YouTube_URL> --user-id <FEISHU_OPEN_ID>

# 仅下载（测试）
python youtube_upload.py --url <YouTube_URL>

# Dry run（不实际上传）
python youtube_to_feishu_complete.py --url <URL> --dry-run
```

## 工作流程

```
1. 解析 YouTube URL
   ↓
2. 获取视频信息（标题、时长、ID）
   ↓
3. 下载音频（yt-dlp，MP3 192K）
   ↓
4. 上传到飞书云盘（feishu_drive_file）
   ↓
5. 发送交互式卡片到飞书（feishu_im_user_message）
   ↓
6. 清理临时文件（保留最近下载）
```

## 输出示例

### 下载进度

```
[1/4] Extracting video info...
  📹 Title: AI 就业冲击：7030 岗位受影响...
  🆔 Video ID: dyJUscv7b9g
  ⏱️ Duration: 840s

[2/4] Downloading audio...
  ✅ Downloaded: youtube_audio_dyJUscv7b9g.mp3 (17.5 MB)

[3/4] Uploading to Feishu cloud...
  ☁️  File token: NxSYbtSpeoTAgJxHOW4cpcOxned

[4/4] Sending to your Feishu chat...
  ✅ Done!
```

### 飞书卡片消息

```
┌─────────────────────────────────────┐
│  🎵 YouTube 音频已准备好             │
├─────────────────────────────────────┤
│  YouTube 视频转音频                  │
│                                     │
│  📁 文件：youtube_audio.mp3         │
│  📊 大小：17.5 MB                   │
│  ⏱️ 时长：约 14 分钟                 │
│                                     │
│  AI 就业冲击：7030 岗位受影响         │
│                                     │
│  [📥 点击下载音频] [📄 查看详情]    │
└─────────────────────────────────────┘
```

## 配置

| 环境变量 | 说明 | 默认值 |
|---------|------|--------|
| `FEISHU_USER_ID` | 用户飞书 open_id | 从上下文获取 |
| `TEMP_DIR` | 临时下载目录 | `./temp` |

## 限制

- **文件大小**：最大 100MB（飞书限制）
- **支持格式**：仅音频（MP3）
- **视频来源**：仅支持 YouTube
- **需要授权**：飞书云盘 + IM 权限

## 故障排除

### 下载失败

```bash
# 更新 yt-dlp
pip install -U yt-dlp

# 检查网络连接
ping youtube.com
```

### 上传失败

- 确认飞书授权完成
- 检查文件大小（<100MB）
- 确认云盘空间充足

### 发送失败

- 确认用户 open_id 正确
- 检查应用权限（im:message.send_as_user）

## 文件结构

```
youtube-to-feishu/
├── SKILL.md                      # 技能定义
├── index.js                      # 工具注册
├── youtube_upload.py             # 下载脚本
├── youtube_to_feishu_complete.py # 完整流程脚本
├── README.md                     # 本文档
└── requirements.txt              # Python 依赖
```

## 依赖

- **yt-dlp** >= 2024.0.0
- **Python** >= 3.8
- **OpenClaw** >= 2026.0.0
- **Feishu OAuth** - 云盘 + IM 权限

## 版本历史

- **1.0.0** (2026-03-19) - 初始版本
  - YouTube 音频下载
  - 飞书云盘上传
  - 交互式卡片发送
  - 自动清理

## License

MIT

---

*Created for OpenClaw | 🎵 Enjoy your YouTube audio on Feishu!*