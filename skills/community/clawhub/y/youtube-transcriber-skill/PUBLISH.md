# 发布到 ClawHub 指南

## 🎯 为什么要发布？

发布后用户可以：
- ✅ 在 OpenClaw 中直接安装：`/openclaw install youtube-transcribe`
- ✅ 在 ClawHub 市场搜索到
- ✅ 自动安装依赖
- ✅ 版本管理和更新

---

## 📦 发布步骤

### 1. 安装 ClawHub CLI

```bash
npm install -g clawhub
```

### 2. 登录 ClawHub

```bash
clawhub login
```

会打开浏览器让你登录 GitHub 账号。

### 3. 准备发布

确保你的仓库包含：
- ✅ `package.json`（已包含）
- ✅ `README.md`（已包含）
- ✅ `LICENSE`（建议添加 MIT License）

### 4. 发布

```bash
cd /tmp/Youtube-Transcriber-Skill
clawhub publish
```

### 5. 验证

访问 ClawHub 市场：
https://clawhub.com/search?q=youtube-transcribe

---

## 📝 配置 clawhub.json

创建 `clawhub.json` 配置文件：

```json
{
  "name": "youtube-transcribe",
  "version": "1.0.0",
  "description": "自动转录 YouTube 视频，生成带时间戳的文字稿",
  "author": "Alex Bloomberg",
  "repository": "BODYsuperman/Youtube-Transcriber-Skill",
  "license": "MIT",
  "keywords": ["youtube", "transcribe", "whisper", "ai", "subtitle"],
  "requirements": {
    "python": ">=3.8.0",
    "packages": ["yt-dlp", "faster-whisper"]
  },
  "usage": {
    "openclaw": "/youtube-transcribe <URL>",
    "npx": "npx github:BODYsuperman/Youtube-Transcriber-Skill <URL>",
    "python": "python3 transcribe.py <URL>"
  }
}
```

---

## 🚀 发布后用户使用

### OpenClaw 用户

```bash
# 安装
/openclaw install youtube-transcribe

# 使用
/youtube-transcribe "https://youtube.com/watch?v=VIDEO_ID"
```

### NPX 用户

```bash
npx github:BODYsuperman/Youtube-Transcriber-Skill "URL"
```

### Python 用户

```bash
git clone https://github.com/BODYsuperman/Youtube-Transcriber-Skill.git
cd Youtube-Transcriber-Skill
pip3 install -r requirements.txt
python3 transcribe.py "URL"
```

---

## 📊 版本更新

```bash
# 修改代码后
git add .
git commit -m "feat: 新功能描述"
git tag v1.0.1
git push origin main --tags

# 更新 ClawHub 包
clawhub publish --patch  # 或 --minor, --major
```

---

## 🔗 相关链接

- **ClawHub:** https://clawhub.com
- **文档:** https://docs.clawhub.com
- **你的仓库:** https://github.com/BODYsuperman/Youtube-Transcriber-Skill

---

**发布后记得更新 README 中的安装说明！** 🎉
