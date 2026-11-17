---
name: shipinhao-upload
description: 使用 EasyPost 自动填充或发布微信视频号（Channels）短视频。Use when 用户需要向微信视频号发布短视频。
license: MIT-0
slug: easypost-shipinhao-upload
displayName: 微信视频号自动发布 (EasyPost)
version: 1.0.0
summary: 基于真实 Chrome 会话的微信视频号短视频自动发布，内置 16 字纯文本短标题强校验。
---

# 微信视频号自动填充与发布 Skill

通过 EasyPost 驱动当前 Chrome 浏览器已登录的微信视频号助手（`channels.weixin.qq.com`）执行自动上传与填充。

## 平台硬性规格限制（⚠️ 严格注意）

- **内容形态**：仅支持 `shortVideo`（短视频）；
- **短标题规则**：
  - **最大长度**：严格不得超过 **16 个字符**；
  - **字符集限制**：**仅允许中文汉字、英文字母、数字和空格**；
  - **严禁包含标点符号**（如逗号、句号、感叹号、破折号）、Emoji 或特殊符号。包含标点将被 CLI 本地校验拒绝（不会静默吞掉报错）；
- **动态描述**：可包含详细说明与 `#话题` 标签；
- **封面**：支持 9:16 竖版封面（`cover`）。

---

## 示例

```bash
printf '%s\n' '{
  "type": "shortVideo",
  "platforms": ["shipinhao"],
  "data": {
    "title": "晨间自律三个习惯",
    "content": "每天坚持做好这三件事，轻松提升精力与专注力 #个人成长 #生活习惯 #自律"
  },
  "assets": [
    {
      "path": "/absolute/path/to/video.mp4",
      "role": "media"
    },
    {
      "path": "/absolute/path/to/vertical_cover.jpg",
      "role": "cover"
    }
  ]
}' | easypost fill
```
