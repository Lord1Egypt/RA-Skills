---
name: wechat-video-downloader
description: 从微信公众号文章中提取并下载视频。使用场景：用户发送公众号文章链接并要求下载其中的视频，或提到"微信视频下载"、"公众号视频"、"mp.weixin.qq.com 视频"等关键词。自动识别页面中的视频播放器，提取真实视频 URL 并下载到本地。
---

# 微信视频下载器

从微信公众号文章中提取并下载嵌入的视频文件。

## 快速开始

当用户提供微信公众号文章链接时，使用内置脚本下载视频：

```bash
python ~/.openclaw/skills/wechat-video-downloader/scripts/download_wechat_video.py <文章 URL> [输出文件名]
```

## 工作流程

### 1. 识别触发场景

当用户请求包含以下特征时触发此技能：

- 包含 `mp.weixin.qq.com` 的 URL
- 提到"微信视频"、"公众号视频"、"下载视频"等关键词
- 发送公众号文章链接并要求获取其中的视频

### 2. 检查文章是否包含视频

**方法 A：使用浏览器快照（推荐）**

打开文章页面并获取快照，查找视频播放按钮：

```
1. 用 browser.open 打开文章 URL
2. 用 browser.snapshot 获取页面快照（refs="aria"）
3. 查找包含"播放视频"、"play"、"video"的 button 元素
4. 提取按钮的 ref 用于后续点击
```

**方法 B：直接调用脚本**

如果确认文章包含视频，直接运行下载脚本：

```bash
python ~/.openclaw/skills/wechat-video-downloader/scripts/download_wechat_video.py <URL>
```

### 3. 下载视频

脚本自动执行以下步骤：

1. **打开页面** - 使用 browser.open 加载文章
2. **查找视频** - 通过 snapshot 定位播放按钮
3. **触发加载** - 点击播放按钮使视频元素加载
4. **提取 URL** - 通过 JavaScript 获取 `<video>` 元素的 src
5. **下载文件** - 使用 curl 添加正确的 User-Agent 和 Referer 请求头
6. **关闭页面** - 清理浏览器标签页

### 4. 处理常见问题

**问题 1:403 Forbidden**

微信视频链接有时效性和来源验证，必须添加正确的请求头：

```bash
curl -L -o output.mp4 \
  -H "User-Agent: Mozilla/5.0 ..." \
  -H "Referer: https://mp.weixin.qq.com/" \
  "<video_url>"
```

**问题 2：找不到视频元素**

- 确认文章确实包含视频（有些文章只有图片）
- 等待页面完全加载（增加 sleep 时间）
- 检查是否有多个视频，尝试不同的播放按钮 ref

**问题 3：视频链接过期**

视频 URL 包含时效性 token，必须在点击播放后立即提取并下载，不能重复使用旧链接。

## 脚本说明

### 位置
`~/.openclaw/skills/wechat-video-downloader/scripts/download_wechat_video.py`

### 参数
- `article_url`（必需）- 微信公众号文章 URL
- `output_filename`（可选）- 输出文件名，默认使用视频 ID

### 返回值
- 成功：返回 0，视频保存到当前目录
- 失败：返回 1，打印错误信息

### 依赖
- Python 3.6+
- OpenClaw CLI（browser 命令）
- curl

## 示例

### 示例 1：基本下载

用户：下载这个公众号文章里的视频 https://mp.weixin.qq.com/s/xxx

```bash
python ~/.openclaw/skills/wechat-video-downloader/scripts/download_wechat_video.py https://mp.weixin.qq.com/s/xxx
```

### 示例 2：指定文件名

用户：把视频保存为"教学视频.mp4"

```bash
python ~/.openclaw/skills/wechat-video-downloader/scripts/download_wechat_video.py https://mp.weixin.qq.com/s/xxx 教学视频.mp4
```

### 示例 3：手动流程（脚本失败时）

如果脚本无法自动处理，手动执行：

```
1. browser.open targetUrl=<文章 URL>
2. browser.snapshot refs="aria" → 找到播放按钮 ref
3. browser.act request='{"kind":"click","ref":"e88"}'
4. sleep 3
5. browser.act request='{"kind":"evaluate","fn":"()=>document.querySelector(\"video\").src"}'
6. 用 curl 下载提取的 URL
7. browser.close 关闭页面
```

## 注意事项

1. **视频时效性** - 提取的 URL 包含认证 token，必须在短时间内使用
2. **网络速度** - 视频文件通常较大（100MB-1GB），下载需要时间
3. **存储空间** - 确保工作目录有足够空间
4. **版权尊重** - 仅下载用于个人学习或已获授权的内容

## 支持的视频类型

- ✅ 微信公众号内置视频播放器（mpvideo.qpic.cn）
- ✅ 腾讯视频嵌入（v.qq.com）
- ⚠️ 第三方平台视频（可能需要额外处理）

## 故障排查

| 问题 | 可能原因 | 解决方案 |
|------|----------|----------|
| 403 Forbidden | 缺少 Referer 头 | 确保 curl 添加 `-H "Referer: https://mp.weixin.qq.com/"` |
| 找不到视频 | 页面未完全加载 | 增加点击前的等待时间 |
| 文件为空 | URL 过期 | 重新打开页面，立即提取并下载 |
| 脚本无响应 | 浏览器未启动 | 先运行 `openclaw browser start` |
