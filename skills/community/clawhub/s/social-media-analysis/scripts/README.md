# 社交媒体下载脚本使用说明

本目录包含用于下载抖音和小红书媒体文件的脚本。

---

## 📕 小红书脚本

### 1. `parse-xiaohongshu.js` - 通用解析脚本（推荐）

**功能**：自动判断帖子类型（图集/视频）并下载

**用法**：
```bash
node parse-xiaohongshu.js <URL> <输出目录> [--cookie <COOKIE_STRING>]
```

**示例**：
```bash
# 图集下载
node parse-xiaohongshu.js "https://www.xiaohongshu.com/explore/69ba4a870000000028009ac0" ./output

# 视频下载（需要 Cookie）
node parse-xiaohongshu.js "https://www.xiaohongshu.com/explore/69b8f9360000000021039d96" ./output \
  --cookie "unread=xxx; id_token=xxx; web_session=xxx"
```

**输出**：
- **图集**：`./output/images/image-01.webp`, `image-02.webp`...
- **视频**：`./output/video.mp4`

---

### 2. `download-xiaohongshu-album.js` - 图集专用脚本

**功能**：专门用于下载小红书图集（图片轮播）

**用法**：
```bash
node download-xiaohongshu-album.js <URL> <输出目录> [--cookie <COOKIE_STRING>]
```

**示例**：
```bash
node download-xiaohongshu-album.js "https://www.xiaohongshu.com/explore/69ba4a870000000028009ac0" ./images \
  --cookie "unread=xxx; id_token=xxx"
```

**输出**：`./images/image-01.webp`, `image-02.webp`...

---

### 3. `download-xiaohongshu-video.sh` - 视频下载脚本

**功能**：使用 yt-dlp 下载小红书视频，支持抽帧

**用法**：
```bash
./download-xiaohongshu-video.sh <URL> <输出目录> [--cookie <COOKIE_STRING>]
```

**示例**：
```bash
chmod +x download-xiaohongshu-video.sh

./download-xiaohongshu-video.sh "https://www.xiaohongshu.com/explore/69b8f9360000000021039d96" ./output \
  --cookie "unread=xxx; id_token=xxx"
```

**输出**：
- `./output/video.mp4`
- （可选）`./output/frame_001.jpg`, `frame_002.jpg`...（抽帧）

---

## 🎵 抖音脚本

### 1. `extract-douyin-images.js` - 图集下载

**功能**：下载抖音图集（图片轮播）+ 音频

**用法**：
```bash
node extract-douyin-images.js <URL> <输出目录>
```

**示例**：
```bash
node extract-douyin-images.js "https://www.douyin.com/share/video/7618120092425065587" ./output
```

**输出**：
- `./output/images/image-01.webp`, `image-02.webp`...
- `./output/audio.mp3`（背景音乐）

---

### 2. `parse-douyin-video.js` - 视频下载

**功能**：下载抖音视频（无需 Cookie）

**用法**：
```bash
node parse-douyin-video.js <URL> <输出路径>
```

**示例**：
```bash
node parse-douyin-video.js "https://www.douyin.com/share/video/7618122368540801019" ./output/video.mp4
```

**输出**：`./output/video.mp4`

---

## 🔑 Cookie 获取方法

### 小红书 Cookie

1. 浏览器打开 [小红书网页版](https://www.xiaohongshu.com) 并登录
2. 按 F12 打开开发者工具
3. 切换到 **Network** 标签
4. 刷新页面，点击任意请求
5. 复制 **Request Headers** 中的 `Cookie` 值
6. 粘贴到脚本的 `--cookie` 参数中

**Cookie 格式示例**：
```
unread={"ub":"xxx","ue":"xxx","uc":22}; id_token=VjEAxxx; web_session=0400xxx; ...
```

### Cookie 有效期

- 小红书 Cookie 通常有效期为 **7-30 天**
- 如下载失败提示 403/401，说明 Cookie 已过期，需重新获取
- 建议定期更新 Cookie

---

## 🛠️ 前置依赖

### Node.js 脚本
```bash
# 检查 Node.js 是否安装
node --version

# 无需额外安装依赖，使用内置模块
```

### Shell 脚本
```bash
# 安装 yt-dlp（视频下载）
brew install yt-dlp

# 安装 ffmpeg（视频抽帧）
brew install ffmpeg

# 赋予执行权限
chmod +x download-xiaohongshu-video.sh
```

---

## 📋 工作流程

### 小红书帖子处理流程

```
1. 判断类型
   │
   ├─ 图集 → download-xiaohongshu-album.js → images/
   │
   └─ 视频 → download-xiaohongshu-video.sh → video.mp4 → ffmpeg 抽帧 → frames/
```

### 抖音帖子处理流程

```
1. 先尝试图集下载
   │
   ├─ 找到图片 → extract-douyin-images.js → images/ + audio.mp3
   │
   └─ 未找到图片 → parse-douyin-video.js → video.mp4 → ffmpeg 抽帧 → frames/
```

---

## ⚠️ 常见问题

### 1. "未找到 imageList"
- **原因**：Cookie 过期或无效
- **解决**：重新获取 Cookie，使用 `--cookie` 参数

### 2. "No video formats found"
- **原因**：帖子是图集类型，不是视频
- **解决**：使用 `download-xiaohongshu-album.js` 脚本

### 3. "ffmpeg 抽帧失败：Output file does not contain any stream"
- **原因**：图集被误判为视频（图集只有音频，没有视频流）
- **解决**：先用图集脚本判断类型，图集不需要抽帧

### 4. 图片下载后无法打开
- **原因**：图片 URL 有时效性
- **解决**：尽快下载，不要延迟

---

## 📁 目录结构

```
scripts/
├── README.md                          # 本文件
├── parse-xiaohongshu.js              # 小红书通用解析（推荐）
├── download-xiaohongshu-album.js     # 小红书图集专用
├── download-xiaohongshu-video.sh     # 小红书视频下载
├── extract-douyin-images.js          # 抖音图集下载
└── parse-douyin-video.js             # 抖音视频下载
```

---

## 📝 使用技巧

1. **优先使用通用脚本**：`parse-xiaohongshu.js` 会自动判断类型
2. **Cookie 管理**：将常用 Cookie 保存为环境变量 `XHS_COOKIE`
3. **批量处理**：编写循环脚本批量调用这些脚本
4. **输出目录**：建议按记录 ID 组织输出，如 `record-107/images/`

---

## 🔗 相关文档

- 主 Skill 文档：`../SKILL.md`
- 飞书多维表格 API：https://open.feishu.cn/document/ukTMukTMukTM/uADO1UjLwgjB14CN
- yt-dlp 文档：https://github.com/yt-dlp/yt-dlp
