---
name: xiaohongshu-upload
description: 使用 EasyPost 自动填充或发布小红书创作者中心的图文笔记与短视频。Use when 用户需要向小红书发布图文或短视频。
license: MIT-0
slug: easypost-xiaohongshu-upload
displayName: 小红书自动发布 (EasyPost)
version: 1.0.0
summary: 基于真实 Chrome 浏览器会话的小红书图文与短视频零风控自动发布。
---

# 小红书自动填充与发布 Skill

使用 EasyPost 通过创作者日常已登录的 Chrome 浏览器无感填充或发布小红书内容，免配置 Cookie，避免 CDP 探针风控。

## 平台规格限制与最佳实践

- **内容形态**：
  - `imageText`：图文笔记（1~18 张图片，推荐 3:4 比例）；
  - `shortVideo`：短视频（推荐 9:16 竖版）。
- **字段限制**：
  - **标题**：最大 20 个字（超过会被平台截断或拒绝）；
  - **正文**：最多 1000 字，支持 `#话题` 格式；
  - **封面**：短视频建议提供竖版封面，对应 `role: "cover"`。

---

## 工作流程

1. **核验参数**：确保标题不超过 20 字，提取前 3~5 个核心标签；
2. **生成任务配置**；
3. **优先执行 `easypost fill`**（将图片与标题文案填入小红书创作后台，让用户人工在浏览器中微调并点击发布）；
4. 若用户显式要求自动提交，附加 `--yes` 执行 `easypost publish`。

---

## 示例

### 发布图文笔记
```bash
printf '%s\n' '{
  "type": "imageText",
  "platforms": ["xiaohongshu"],
  "data": {
    "title": "极简桌面好物推荐",
    "content": "近期淘到的几款提升办公幸福感的小物件，尤其是这个磁吸支架... #桌面搭配 #好物推荐 #生产力工具",
    "tags": ["桌面搭配", "好物推荐"]
  },
  "assets": [
    {
      "path": "/absolute/path/to/desktop1.jpg",
      "role": "media"
    },
    {
      "path": "/absolute/path/to/desktop2.jpg",
      "role": "media"
    }
  ]
}' | easypost fill
```

### 发布短视频
```bash
printf '%s\n' '{
  "type": "shortVideo",
  "platforms": ["xiaohongshu"],
  "data": {
    "title": "3分钟学会高效剪辑",
    "content": "新手剪辑避免踩坑的几个技巧，建议收藏！#剪辑教程 #创作日常"
  },
  "assets": [
    {
      "path": "/absolute/path/to/video.mp4",
      "role": "media"
    },
    {
      "path": "/absolute/path/to/cover_vertical.jpg",
      "role": "cover"
    }
  ]
}' | easypost fill
```
