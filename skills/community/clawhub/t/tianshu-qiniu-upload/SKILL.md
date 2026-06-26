---
name: tianshu-qiniu-upload
description: >
  将本地文件（图片、HTML 等）上传到七牛云存储，返回可在线访问的 URL。
  Use when: 用户需要把生成的图片、HTML 页面或任意文件上传到云端以便分享链接；用户说「上传到七牛」「生成图片并上传」「把这个 HTML 上传到网上」。
  NOT for: 上传到其他云存储（如 S3、OSS）；仅生成文件不分享链接。
metadata:
  openclaw:
    primaryEnv: QINIU_ACCESS_KEY
    requires:
      env:
        - QINIU_ACCESS_KEY
        - QINIU_SECRET_KEY
        - QINIU_BUCKET
        - QINIU_DOMAIN
---

# 七牛上传 Skill

将文件上传到七牛云，返回公开访问 URL。

## When to Run

- 用户说「上传到七牛」「把这个文件上传」「生成图片并上传到网上」
- AI 生成了图片或 HTML，用户需要可分享的在线链接
- 用户提供本地文件路径，要求获取在线访问地址

## 前置配置

在 `~/.openclaw/openclaw.json` 的 `skills.entries.tianshu-qiniu-upload` 中配置环境变量，或在系统环境变量中设置：

- `QINIU_ACCESS_KEY` - 七牛 Access Key
- `QINIU_SECRET_KEY` - 七牛 Secret Key
- `QINIU_BUCKET` - 存储空间名
- `QINIU_DOMAIN` - 公开访问域名，如 `https://your-bucket.qiniucdn.com`
- `QINIU_PREFIX` - 存储路径前缀，默认 `uploads`

## Workflow

1. 确认要上传的文件路径存在（图片、HTML 或其他文件）
2. 执行上传脚本：
   ```
   node ~/.openclaw/skills/tianshu-qiniu-upload/scripts/upload.js <文件路径>
   ```
   或使用绝对路径调用
3. 脚本会输出上传后的完整 URL，格式为 `{QINIU_DOMAIN}/{QINIU_PREFIX}/{随机文件名}`
4. 将 URL 返回给用户，用户即可在线访问

## 使用示例

- 用户：「帮我生成一个简单的 HTML 页面，然后上传到七牛」
  1. 用 write 工具创建 HTML 文件到 /tmp/xxx.html
  2. 执行 `node .../upload.js /tmp/xxx.html`
  3. 返回 URL 给用户

- 用户：「把这张图片上传到网上」
  1. 确认图片路径（用户可能已提供或 AI 已生成）
  2. 执行 upload.js
  3. 返回 URL

## Output

始终输出上传后的完整 URL，便于用户直接复制访问。
