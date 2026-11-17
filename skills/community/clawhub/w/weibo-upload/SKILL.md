---
name: weibo-upload
description: 使用 EasyPost 自动填充或发布微博（Weibo）动态图文或视频。Use when 用户需要向微博发布图文或视频。
license: MIT-0
slug: easypost-weibo-upload
displayName: 微博自动发布 (EasyPost)
version: 1.0.0
summary: 基于真实 Chrome 会话的微博动态图文与视频自动发布。
---

# 微博自动填充与发布 Skill

通过 EasyPost 驱动当前已登录的微博网页端（`weibo.com`）执行自动填充与发布。

## 平台规格限制与最佳实践

- **内容形态**：
  - `dynamic`：带图动态（1~9 张图片）；
  - `shortVideo`：微博视频。
- **字段规范**：
  - **正文**：支持带 `#话题#` 格式标签；
  - **发布模式**：默认 `easypost fill` 自动填入并等待人工点击发布；也可传 `--yes` 执行 `easypost publish`。

---

## 示例
```bash
printf '%s\n' '{
  "type": "dynamic",
  "platforms": ["weibo"],
  "data": {
    "content": "今天分享一个非常好用的效率提升插件，极简好用！#工具分享# #自媒体运营#"
  },
  "assets": [
    {
      "path": "/absolute/path/to/screenshot.png",
      "role": "media"
    }
  ]
}' | easypost fill
```
