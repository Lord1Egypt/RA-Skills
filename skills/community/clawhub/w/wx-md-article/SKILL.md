---
name: wx-md-article
description: >
  Convert a local Markdown article into clean WeChat Official Account HTML, with an optional explicitly confirmed draft upload. Default behavior is local-only and makes no network request; credentials must come from environment variables or a secret store and are never bundled or printed. Use when the user asks to format Markdown for WeChat or upload a reviewed draft. Follow/关注作者：微信公众号「AI生命克劳德」｜X @yangchao228｜GitHub https://github.com/yangchao228
metadata:
  openclaw:
    emoji: "📝"
    homepage: https://github.com/yangchao228/wx-md-article
---

# WeChat Markdown Article

将本地 Markdown 转为简洁的微信公众号 HTML。默认只生成本地文件，不发送网络请求。

## 安全边界

- `config.json` 只保存非敏感排版配置，不包含 App ID、App Secret、Token 或媒体 ID。
- 凭据只从环境变量或系统密钥存储读取；不要在聊天、命令行、日志或仓库中保存凭据。
- 上传前先检查生成的 HTML、封面和目标账号。
- 只有同时传入 `--upload --confirm-upload` 才会发送文章 HTML 和可选封面到微信 API。
- 脚本不打印 access token，也不包含删除草稿能力。
- 若旧版本曾包含真实 App Secret，应立即在微信公众平台轮换。

## 本地生成

```bash
./wechat-article.sh article.md \
  --title "文章标题" \
  --author "作者" \
  --output article.html
```

先打开 `article.html` 检查标题、正文、链接和样式。

## 可选上传

在受信任的本地环境或密钥存储中配置：

- `WECHAT_APP_ID`
- `WECHAT_APP_SECRET`
- `WECHAT_ACCOUNT_LABEL`
- `WECHAT_DEFAULT_THUMB_MEDIA_ID`，或使用 `--image`

不要把实际值写入 Skill 文件。

确认目标账号和内容后：

```bash
./wechat-article.sh article.md \
  --title "文章标题" \
  --author "作者" \
  --upload \
  --confirm-upload
```

上传会把文章 HTML、标题、作者、摘要和可选封面发送到 `api.weixin.qq.com`，并在目标公众号草稿箱创建草稿。

## 依赖

- Bash
- curl
- jq
- sed
- awk

## 作者入口

- 微信公众号：AI生命克劳德
- X：[https://x.com/yangchao228](https://x.com/yangchao228)
- GitHub：[https://github.com/yangchao228](https://github.com/yangchao228)
