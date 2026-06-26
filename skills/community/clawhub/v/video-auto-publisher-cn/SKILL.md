---
name: video-auto-publisher-cn
description: 自动发布视频到中国三大平台（B站、抖音、小红书）
version: 1.0.0
author: HankHuang
tags: [video, automation, publishing, bilibili, douyin, xiaohongshu]
---

# video-auto-publisher-cn

自动将视频发布到中国三大主流平台：B站（Bilibili）、抖音（Douyin）、小红书（Xiaohongshu）。

## 功能特性

- ✅ 完全自动化发布到三个平台
- ✅ 自动上传视频文件
- ✅ 自动填写标题、描述、标签
- ✅ Cookie 持久化，保持登录状态
- ✅ 智能成功检测
- ✅ 详细日志记录

## 使用方法

### 基础用法

```bash
/video-auto-publisher-cn
```

这将自动发布最新的视频到三个平台。

### 指定视频文件

```bash
/video-auto-publisher-cn --video path/to/video.mp4
```

### 指定平台

```bash
/video-auto-publisher-cn --platforms bilibili,douyin
```

### 自定义标题和描述

```bash
/video-auto-publisher-cn --title "我的视频标题" --description "视频描述内容"
```

## 前置要求

1. **Python 环境**: Python 3.8+
2. **依赖安装**:
   ```bash
   pip install playwright
   python -m playwright install chromium
   ```
3. **首次登录**: 需要先登录各平台保存 cookies

## 参数说明

- `--video`: 视频文件路径（可选，默认使用最新视频）
- `--title`: 视频标题（可选，默认自动生成）
- `--description`: 视频描述（可选，默认自动生成）
- `--tags`: 标签列表，逗号分隔（可选）
- `--platforms`: 目标平台，逗号分隔（可选，默认全部）
- `--headless`: 是否使用无头模式（可选，默认 false）

## 示例

### 发布到所有平台
```bash
/video-auto-publisher-cn
```

### 只发布到 B站 和抖音
```bash
/video-auto-publisher-cn --platforms bilibili,douyin
```

### 指定完整信息
```bash
/video-auto-publisher-cn \
  --video my_video.mp4 \
  --title "精彩视频" \
  --description "这是一个很棒的视频" \
  --tags "娱乐,搞笑,日常"
```

## 注意事项

1. **Cookies 有效期**: Cookies 通常 7-14 天过期，需要重新登录
2. **视频格式**: 支持 MP4、MOV、MKV 等常见格式
3. **视频大小**:
   - B站: 16GB 以内
   - 抖音: 根据平台限制
   - 小红书: 根据平台限制
4. **网络要求**: 需要稳定的网络连接

## 故障排查

### Cookies 过期
```bash
# 重新登录保存 cookies
python login_platforms.py
```

### 查看日志
```bash
# 日志保存在 logs/ 目录
cat logs/publish_*.log
```

## 技术细节

- **浏览器自动化**: Playwright
- **反检测**: 非 headless 模式 + 真实用户行为模拟
- **成功检测**: 多重验证机制（URL、关键词、元素）
- **错误处理**: 完善的异常捕获和日志记录

## 更新日志

### v1.0.0 (2026-03-19)
- ✅ 初始版本
- ✅ 支持 B站、抖音、小红书
- ✅ 完全自动化发布
- ✅ Cookie 持久化
- ✅ 详细日志记录
