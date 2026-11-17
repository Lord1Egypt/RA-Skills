---
name: x-upload
description: 使用 EasyPost 自动填充或发布 X (Twitter) 推文动态与短视频。Use when 用户需要向 X (Twitter) 发布推文、图集或视频。
license: MIT-0
slug: easypost-x-upload
displayName: X (Twitter) 自动发布 (EasyPost)
version: 1.0.0
summary: 基于真实 Chrome 会话的 X (Twitter) 动态图文与视频自动发布。
---

# X (Twitter) 自动填充与发布 Skill

通过 EasyPost 驱动当前已登录的 `x.com` 执行自动填充与发布。

## 平台规格限制与最佳实践

- **内容形态**：
  - `dynamic`：动态推文（最多 4 张图片）；
  - `shortVideo`：视频推文。
- **字段规范**：
  - **推文字数**：普通用户单条推文最多 280 字符（Premium 订阅账号除外）；
  - **标签**：支持 `#hashtag`。

---

## 示例
```bash
printf '%s\n' '{
  "type": "dynamic",
  "platforms": ["x"],
  "data": {
    "content": "Excited to share our open-source workflow for cross-platform publishing! Check it out. #buildinpublic #devtools"
  },
  "assets": [
    {
      "path": "/absolute/path/to/product_demo.png",
      "role": "media"
    }
  ]
}' | easypost fill
```
