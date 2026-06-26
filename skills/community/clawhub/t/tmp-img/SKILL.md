---
name: tmp-img
description: 临时图床上传工具。上传图片到临时图床，默认30天过期，获取公开链接。零配置，开箱即用。当用户说"临时上传"、"上传到临时图床"、"tmp upload" 时触发。
---

# tmp-img - 临时图床

上传图片到 imgland.net 临时图床，固定 30 天过期，零配置开箱即用。

## 触发场景

当用户提到以下需求时触发本技能：

- "临时上传图片" / "临时图床"
- "tmp upload" / "临时上传"
- "上传到临时图床"
- "传到临时图床"

## 使用方式

上传一张图片（默认 30 天过期）：

```bash
bash ~/.claude/skills/tmp-img/scripts/upload.sh ~/Desktop/screenshot.png
```

自定义过期时间：

```bash
bash ~/.claude/skills/tmp-img/scripts/upload.sh ~/photo.png 7d
```

支持的过期时间格式：`1d`、`7d`、`30d` 等。

## 输出

成功后返回 JSON：

```json
{
  "url": "https://api.imgland.net/v1/images/xxx/file",
  "id": "h463m2O1",
  "filename": "screenshot.png",
  "file_size": "377716",
  "expires_at": "2026-05-11T00:04:15.5834277+00:00",
  "delete_url": "https://api.imgland.net/v1/images/h463m2O1/file/uXMJd95M..."
}
```

向用户展示时，重点展示：
1. **图片链接** — url 字段
2. **过期时间** — expires_at 字段（转换为可读日期）
3. 提醒用户这是临时图床，图片会在过期时间后自动删除

## 支持的图片格式

png, jpg, jpeg, gif, webp, bmp

## 依赖

- curl（系统自带）
- jq（JSON 解析，通常系统自带）

## 不做什么

- 不编辑图片（裁剪、压缩等）
- 不提供批量上传
- 不提供图片管理功能
- 不提供删除功能（图片会自动过期）
