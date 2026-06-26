# 社交媒体分析 Skill - 快速开始指南

## 📦 安装与使用

### 1. 解压 Skill 包

```bash
unzip social-media-analysis-skill-*.zip -d ~/skills/
cd ~/skills/social-media-analysis
```

### 2. 检查依赖

```bash
# Node.js（必需）
node --version  # 需要 v14+

# yt-dlp（小红书视频下载，可选）
brew install yt-dlp

# ffmpeg（视频抽帧，可选）
brew install ffmpeg
```

### 3. 获取 Cookie（小红书必需）

**小红书 Cookie 获取步骤**：

1. 浏览器打开 https://www.xiaohongshu.com 并登录
2. 按 F12 打开开发者工具
3. 切换到 **Network** 标签
4. 刷新页面，点击任意请求
5. 复制 **Request Headers** 中的 `Cookie` 值

**保存 Cookie（可选）**：
```bash
# 方法 1：环境变量（推荐）
export XHS_COOKIE="unread=xxx; id_token=xxx; web_session=xxx"

# 方法 2：Cookie 文件
cat > /tmp/xhs_cookies.txt << 'EOF'
# Netscape HTTP Cookie File
.xiaohongshu.com  TRUE  /  TRUE  0  unread  {"ub":"xxx","ue":"xxx","uc":22}
.xiaohongshu.com  TRUE  /  TRUE  0  id_token  VjEAxxx
.xiaohongshu.com  TRUE  /  TRUE  0  web_session  0400xxx
EOF
```

---

## 🎬 使用示例

### 示例 1：小红书帖子（自动判断类型）

```bash
# 图集或视频都会自动处理
node scripts/parse-xiaohongshu.js \
  "https://www.xiaohongshu.com/explore/69ba4a870000000028009ac0" \
  ./output

# 如果帖子需要 Cookie
node scripts/parse-xiaohongshu.js \
  "URL" \
  ./output \
  --cookie "unread=xxx; id_token=xxx"
```

**输出**：
- 图集：`./output/images/image-01.webp`, `image-02.webp`...
- 视频：`./output/video.mp4`

---

### 示例 2：抖音视频

```bash
# 直接下载视频（无需 Cookie）
node scripts/parse-douyin-video.js \
  "https://www.douyin.com/share/video/7618122368540801019" \
  ./output/video.mp4

# 视频抽帧（每 5 秒一帧）
cd ./output
ffmpeg -i video.mp4 -vf "fps=1/5" -q:v 2 frame_%03d.jpg
```

**输出**：
- `video.mp4`
- `frame_001.jpg`, `frame_002.jpg`...

---

### 示例 3：抖音图集

```bash
# 下载图集 + 音频
node scripts/extract-douyin-images.js \
  "https://www.douyin.com/share/video/7618120092425065587" \
  ./output

# 检查结果
ls -lh ./output/
# 输出：images/ (图片目录), audio.mp3 (背景音乐)
```

**输出**：
- `images/image-01.webp`, `image-02.webp`...
- `audio.mp3`

---

### 示例 4：统一生成“内容解析”（推荐放入批处理）

```bash
node scripts/build-content-analysis.js \
  --title "小爱同学新功能体验" \
  --text "作者对语音识别速度和家居联动进行了测试" \
  --platform "微博" \
  --media-type "视频" \
  --visual "画面出现小米音箱和手机联动控制"
```

输出 JSON 字段：
- `analysis`：100 字以内内容解析（可直接写入飞书“内容解析”）
- `score`：解析置信分（低分建议人工复核）
- `evidence`：解析使用证据（标题/正文/视觉是否参与）

---

## 🔧 脚本选择指南

| 平台 | 类型 | 使用脚本 | 是否需要 Cookie |
|------|------|---------|----------------|
| 小红书 | 未知 | 先用 `yt-dlp` 判断类型 | ✅ 是 |
| 小红书 | 视频 | `yt-dlp` 下载 | ✅ 是 |
| 小红书 | 图集 | `download-xiaohongshu-album.js` | ✅ 是 |
| 抖音 | 未知 | 先尝试 `extract-douyin-images.js` | ❌ 否 |
| 抖音 | 图集 | `extract-douyin-images.js` | ❌ 否 |
| 抖音 | 视频 | `parse-douyin-video.js` | ❌ 否 |

**⚠️ 重要提示**：

小红书类型判断**必须优先使用 yt-dlp**：
```bash
# 正确做法
yt-dlp --dump-json "URL" 2>&1 | grep '"duration"'
# 有 duration → 视频，无 duration → 图集

# ❌ 错误做法
# 不要先用 Node.js 脚本提取 imageList 判断类型
# 可能导致视频被误判为图集（case 180 教训）
```

---

## ⚠️ 常见问题

### Q1: "未找到 imageList"
**原因**：Cookie 过期或无效  
**解决**：重新获取 Cookie，使用 `--cookie` 参数

### Q2: "No video formats found"
**原因**：帖子是图集类型  
**解决**：使用 `download-xiaohongshu-album.js` 脚本

### Q3: "ffmpeg 抽帧失败"
**原因**：图集被误判为视频（图集没有视频流）  
**解决**：先用图集脚本判断类型，图集不需要抽帧

### Q4: Cookie 有效期多久？
**回答**：通常 7-30 天，下载失败时需重新获取

---

## 📁 目录结构

```
social-media-analysis/
├── SKILL.md                          # 完整技能文档
├── scripts/
│   ├── README.md                     # 脚本使用说明
│   ├── QUICKSTART.md                 # 本文件
│   ├── parse-xiaohongshu.js          # 小红书通用解析
│   ├── download-xiaohongshu-album.js # 小红书图集专用
│   ├── download-xiaohongshu-video.sh # 小红书视频下载
│   ├── extract-douyin-images.js      # 抖音图集下载
│   └── parse-douyin-video.js         # 抖音视频下载
└── package.sh                        # 打包脚本
```

---

## 🔗 相关资源

- 完整文档：`../SKILL.md`
- 脚本说明：`README.md`
- 飞书 API 文档：https://open.feishu.cn/document/ukTMukTMukTM/uADO1UjLwgjB14CN

---

## 💡 使用技巧

1. **优先使用通用脚本**：`parse-xiaohongshu.js` 会自动判断类型
2. **Cookie 管理**：将 Cookie 保存为环境变量 `XHS_COOKIE`
3. **输出组织**：按记录 ID 组织输出，如 `record-107/images/`
4. **批量处理**：编写循环脚本批量调用这些脚本

---

**有问题？** 查看 `README.md` 或 `../SKILL.md` 获取更多信息。
