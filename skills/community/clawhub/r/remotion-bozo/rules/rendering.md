# 渲染配置

Remotion 视频渲染的完整配置和命令。

## CLI 渲染命令

### 基础渲染

```bash
# 使用全局 remotion 命令
remotion render src/index.tsx MyVideo out/video.mp4

# 使用 npx
npx remotion render src/index.tsx MyVideo out/video.mp4

# 使用 npm script
npm run render
```

### 高级选项

```bash
# 指定编解码器
remotion render src/index.tsx MyVideo out/video.mp4 --codec=vp9

# 指定质量
remotion render src/index.tsx MyVideo out/video.mp4 --quality=90

# 指定比特率
remotion render src/index.tsx MyVideo out/video.mp4 --video-bitrate=5000k

# 并发渲染
remotion render src/index.tsx MyVideo out/video.mp4 --concurrency=8

# 传递参数
remotion render src/index.tsx MyVideo out/video.mp4 --props='{"title":"Hello"}'

# 渲染部分帧
remotion render src/index.tsx MyVideo out/video.mp4 --frames=0-300

# 静音渲染
remotion render src/index.tsx MyVideo out/video.mp4 --mute
```

## 编解码器选项

### H.264（默认）

```bash
--codec=h264
# 或
--codec=h264-mkv

# 优点：兼容性最好，所有设备都支持
# 缺点：文件较大
```

### H.265/HEVC

```bash
--codec=h265

# 优点：压缩效率高，文件小
# 缺点：编码慢，兼容性稍差
```

### VP9

```bash
--codec=vp9

# 优点：开源，压缩效率高
# 缺点：兼容性一般
```

### ProRes

```bash
--codec=prores

# 优点：高质量，适合后期
# 缺点：文件很大
```

## 音频配置

```bash
# 仅渲染音频
remotion render src/index.tsx MyAudio out/audio.mp3 --audio-only

# 指定音频编解码器
remotion render src/index.tsx MyVideo out/video.mp4 --audio-codec=aac

# 静音渲染
remotion render src/index.tsx MyVideo out/video.mp4 --mute
```

## 图片序列渲染

```bash
# 渲染为 PNG 序列
remotion render src/index.tsx MyVideo out/frame_%04d.png --image-sequence

# 渲染为 JPEG 序列
remotion render src/index.tsx MyVideo out/frame_%04d.jpg --image-sequence

# 渲染为 GIF
remotion render src/index.tsx MyVideo out/video.gif --codec=gif
```

## Lambda 云端渲染

### 配置

```bash
# 安装 Lambda 客户端
npm install -D @remotion/lambda

# 设置 AWS 凭证
export AWS_REGION="us-east-1"
export AWS_ACCESS_KEY_ID="your-key"
export AWS_SECRET_ACCESS_KEY="your-secret"
```

### 渲染命令

```bash
# 渲染到 Lambda
remotion lambda src/index.tsx MyVideo --function-name=remotion-render

# 指定输出
remotion lambda src/index.tsx MyVideo --function-name=remotion-render --out-dir=s3://my-bucket/output

# 传入参数
remotion lambda src/index.tsx MyVideo --function-name=remotion-render --props='{"title":"Hello"}'
```

### Lambda 部署

```bash
# 部署 Lambda 函数
remotion lambda functions deploy --function-name=remotion-render

# 查看状态
remotion lambda functions status

# 删除函数
remotion lambda functions rm --function-name=remotion-render
```

## 性能优化

### 并发设置

```bash
# 根据 CPU 核心数调整
remotion render src/index.tsx MyVideo out/video.mp4 --concurrency=4
```

推荐并发数：
- 4 核 CPU: 4-6
- 8 核 CPU: 8-12
- 16 核 CPU: 16-24

### 缓存设置

```bash
# 启用缓存（默认）
remotion render src/index.tsx MyVideo out/video.mp4 --cache

# 禁用缓存
remotion render src/index.tsx MyVideo out/video.mp4 --no-cache
```

### 预览编译

```bash
# 预览渲染但不保存
remotion render src/index.tsx MyVideo out/video.mp4 --dry-run
```

## 输出格式

### MP4（推荐）

```bash
remotion render src/index.tsx MyVideo out/video.mp4
```

### WebM

```bash
remotion render src/index.tsx MyVideo out/video.webm --codec=vp9 --audio-codec=opus
```

### MOV

```bash
remotion render src/index.tsx MyVideo out/video.mov --codec=prores
```

## 渲染配置示例

### 高质量设置

```bash
remotion render src/index.tsx MyVideo out/video.mp4 \
  --quality=95 \
  --video-bitrate=10000k \
  --audio-bitrate=320k
```

### 快速预览

```bash
remotion render src/index.tsx MyVideo out/video.mp4 \
  --quality=70 \
  --concurrency=8
```

### 社交媒体优化

```bash
# Instagram/TikTok (9:16)
remotion render src/index.tsx MyVideo out/video.mp4 \
  --width=1080 --height=1920

# YouTube (16:9)
remotion render src/index.tsx MyVideo out/video.mp4 \
  --width=1920 --height=1080

# Twitter (1:1)
remotion render src/index.tsx MyVideo out/video.mp4 \
  --width=1080 --height=1080
```

## 常见问题

### 渲染很慢

1. 检查并发数设置
2. 减少复杂动画
3. 降低输出质量
4. 使用更快的编解码器

### 内存不足

```bash
# 限制并发
remotion render src/index.tsx MyVideo out/video.mp4 --concurrency=2
```

### 视频卡顿

```bash
# 增加帧率
remotion render src/index.tsx MyVideo out/video.mp4 --fps=60
```
