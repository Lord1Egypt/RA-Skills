# Video Summarizer

🎬 将 B 站/YouTube/小红书/抖音视频转换为结构化 Notion 总结

**版本**: 1.0.12  
**发布**: 2026-05-06  
**许可**: MIT

---

## ⚡ 5 分钟快速开始

### 第一步：安装依赖

```bash
# 系统依赖（最低版本：ffmpeg >= 6.1, yt-dlp >= 2026.03.17）
brew install ffmpeg yt-dlp  # macOS
apt install ffmpeg yt-dlp   # Ubuntu/Debian

# 验证版本
ffmpeg -version    # 应 >= 6.1
yt-dlp --version   # 应 >= 2026.03.17

# Python 依赖
pip3 install requests oss2 python-dotenv
```

### 第二步：配置 API Keys

编辑 `~/.openclaw/.env`：

```bash
# 必需 - 阿里云 OSS 图床
ALIYUN_OSS_AK=your_access_key_id
ALIYUN_OSS_SK=your_access_key_secret
ALIYUN_OSS_BUCKET_ID=your_bucket_name
ALIYUN_OSS_ENDPOINT=oss-cn-shanghai.aliyuncs.com

# 必需 - AI 分析
DASHSCOPE_API_KEY=your_dashscope_api_key

# 可选 - Notion 自动推送（单个数据库）
NOTION_API_KEY=your_notion_api_key
NOTION_VIDEO_SUMMARY_DATABASE_ID=your_database_id

# 可选 - 语音转录加速（Groq API）
# 国内需代理访问，未配置时自动使用本地 Faster-Whisper
# 不配置此项不影响使用
GROQ_API_KEY=your_groq_api_key
```

### 第三步：处理视频

```bash
cd ~/.openclaw/skills/video-summarizer/scripts

# 基础用法
./video-summarize.sh "视频 URL"

# 指定输出目录
./video-summarize.sh "视频 URL" /tmp/output

# 自动推送到 Notion
./video-summarize.sh "视频 URL" --push

# 查看详细日志
./video-summarize.sh "视频 URL" --verbose
```

### 第四步：查看结果

```bash
# 输出目录结构
<output_dir>/
├── summary.md              # 📝 最终总结
├── ai_result.json          # 🧠 AI 分析原始结果
├── screenshot_urls.txt     # 🔗 截图链接
├── metadata.json           # 📊 视频元数据
├── transcript.txt          # 📄 纯文本字幕
├── screenshots/            # 📸 截图原图
└── *.log                   # 📋 日志文件

# 查看总结
cat output/summary.md
```

---

## 🎯 平台支持

| 平台 | 字幕 | 语音转录 | Cookies | 说明 |
|------|------|----------|---------|------|
| **Bilibili** | ✅ 官方 | ✅ | 推荐 | 扫码登录获取字幕 |
| **YouTube** | ✅ 自动 | ✅ | ❌ | 需网络可达 |
| **小红书** | ❌ | ✅ | ❌ | 依赖语音转录 |
| **抖音** | ❌ | ✅ | ❌ | 专用下载器 |

---

## 📚 详细文档

- **[SKILL.md](SKILL.md)** - 完整技能文档（平台配置、架构说明、故障排查）
- **[CHANGELOG.md](CHANGELOG.md)** - 版本历史

---

## 🔧 常用命令

```bash
# 检查配置
./check-config.sh

# B 站扫码登录（仅 B 站需要）
./bili-login.sh

# 保留视频文件
./video-summarize.sh "URL" --keep-video

# 从中断恢复
./video-summarize.sh "URL" --resume
```

---

## 📋 命令行选项

| 选项 | 说明 | 默认 |
|------|------|------|
| `--verbose`, `-v` | 详细日志 | 关闭 |
| `--keep-video` | 保留视频/音频 | 清理 |
| `--push` | 自动推送 Notion | 手动 |
| `--resume` | 断点续跑 | 从头开始 |

---

## ❓ 常见问题

### 截图显示 404

OSS 路径不匹配，重新上传截图：

```bash
python3 upload-to-oss.py auto /tmp/output
```

### 转录失败

检查 GPU 或 API Key：

```bash
# 检查 GPU
nvidia-smi

# 检查 API Key
echo $GROQ_API_KEY
```

### Notion 推送失败

更新 API Key：

```bash
# 编辑 ~/.openclaw/.env
NOTION_API_KEY=your_new_key
```

---

**项目地址**: https://github.com/AjayHao/video-summarizer  
**问题反馈**: https://github.com/AjayHao/video-summarizer/issues
