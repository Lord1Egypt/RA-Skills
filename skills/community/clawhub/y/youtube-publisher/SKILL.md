---
name: youtube-publisher
description: "YouTube 视频自动上传工具。支持视频上传、设置标题/描述/标签/缩略图、管理频道和播放列表。基于 YouTube Data API v3 + OAuth 2.0。"
metadata:
  {
    "openclaw":
      {
        "emoji": "🎬",
      },
  }
---

# youtube-publisher

**YouTube 视频自动上传与管理工具**

基于 YouTube Data API v3 + OAuth 2.0，支持从命令行自动上传视频到 YouTube。

## 架构

```
本地 Mac (Python)
    ↓ OAuth 2.0 认证
Google YouTube Data API v3
    ↓ 断点续传上传
YouTube 频道
```

## 功能

- ✅ 视频上传（支持大文件断点续传，10MB 分块）
- ✅ 设置标题、描述、标签、分类
- ✅ 隐私状态控制（private / public / unlisted）
- ✅ 自定义缩略图
- ✅ 添加到播放列表
- ✅ 频道信息查询
- ✅ 已上传视频列表
- ✅ OAuth 2.0 自动刷新 Token

## 快速开始

### 第一步：Google Cloud Console 配置

**⚠️ 这一步必须手动完成，只需做一次。**

1. 打开 [Google Cloud Console](https://console.cloud.google.com)
2. 创建新项目（或选择已有项目）
3. **启用 API：**
   - 搜索 "YouTube Data API v3" → 点击 "启用"
4. **创建 OAuth 凭证：**
   - 左侧菜单 → "API 和服务" → "凭据"
   - "创建凭据" → "OAuth 客户端 ID"
   - 应用类型选 **"桌面应用"**
   - 名称随意（如 "OpenClaw YouTube"）
   - 下载 JSON 文件
5. **保存凭证文件：**
   ```bash
   mv ~/Downloads/client_secret_*.json ~/.openclaw/workspace/skills/youtube-publisher/client_secret.json
   ```

> **注意：** 如果项目处于"测试"状态，需要在 OAuth 同意屏幕 → 测试用户 中添加你的 Google 邮箱。

### 第二步：安装依赖

```bash
pip3 install google-api-python-client google-auth-oauthlib google-auth-httplib2
```

### 第三步：首次授权

```bash
python3 {baseDir}/scripts/youtube_upload.py auth
```

浏览器会自动打开 Google 授权页面，登录并授权后，Token 自动保存到本地。后续使用无需再授权。

### 第四步：上传视频

```bash
# 基本上传（默认 private）
python3 {baseDir}/scripts/youtube_upload.py upload video.mp4 \
  --title "视频标题" \
  --description "视频描述" \
  --tags AI OpenClaw 自动化

# 公开发布 + 设置缩略图
python3 {baseDir}/scripts/youtube_upload.py upload video.mp4 \
  --title "OpenClaw 实战教程" \
  --description "详细教程..." \
  --tags AI OpenClaw 教程 \
  --privacy public \
  --thumbnail cover.png \
  --category 28

# 上传并添加到播放列表
python3 {baseDir}/scripts/youtube_upload.py upload video.mp4 \
  --title "系列教程 #1" \
  --playlist PLxxxxxx
```

## 其他命令

```bash
# 查看频道信息
python3 {baseDir}/scripts/youtube_upload.py channels

# 列出最近上传的视频
python3 {baseDir}/scripts/youtube_upload.py list
python3 {baseDir}/scripts/youtube_upload.py list -n 20

# 列出播放列表
python3 {baseDir}/scripts/youtube_upload.py playlists
```

## 在 OpenClaw 中使用

直接对 Agent 说：

```
"帮我把 ~/Videos/demo.mp4 上传到 YouTube，标题是 xxx，标签加上 AI 和教程"
```

Agent 会自动调用上传脚本完成发布。

## 视频分类 ID 参考

| 分类 | ID | 分类 | ID |
|------|-----|------|-----|
| 电影/动画 | 1 | 游戏 | 20 |
| 汽车/交通 | 2 | 博客/Vlog | 22 |
| 音乐 | 10 | 喜剧 | 23 |
| 宠物/动物 | 15 | 娱乐 | 24 |
| 体育 | 17 | 新闻 | 25 |
| 短片 | 18 | 时尚 | 26 |
| 旅游/活动 | 19 | **教育** | **27** |
| | | **科技** | **28** |

## 隐私状态

- `private` — 仅自己可见（默认，推荐先用此状态检查后再公开）
- `unlisted` — 不公开列出，有链接可访问
- `public` — 公开发布

## 故障排查

### 1. "client_secret.json 找不到"
请按照"第一步"从 Google Cloud Console 下载 OAuth 凭证文件。

### 2. "Access blocked: This app's request is invalid"
OAuth 同意屏幕未配置。在 Google Cloud Console → OAuth 同意屏幕 → 设置。

### 3. "The user has exceeded the number of videos they may upload"
YouTube API 有每日上传配额限制（通常约 6 个视频/天）。

### 4. "缩略图设置失败"
自定义缩略图需要频道已通过电话号码验证。

### 5. Token 过期
脚本会自动刷新 Token。如果持续失败，删除 `token.json` 重新授权：
```bash
rm ~/.openclaw/workspace/skills/youtube-publisher/token.json
python3 {baseDir}/scripts/youtube_upload.py auth
```

## 文件结构

```
youtube-publisher/
├── SKILL.md              # 本文档
├── client_secret.json    # Google OAuth 凭证（需自行配置）
├── token.json            # 自动生成的访问令牌
└── scripts/
    └── youtube_upload.py  # 上传脚本
```

## 参考资料

- [YouTube Data API v3](https://developers.google.com/youtube/v3)
- [Google Cloud Console](https://console.cloud.google.com)
- [OAuth 2.0 配置指南](https://developers.google.com/youtube/v3/guides/auth/installed-apps)
- [视频上传 API](https://developers.google.com/youtube/v3/docs/videos/insert)
- [API 配额说明](https://developers.google.com/youtube/v3/determine_quota_cost)
