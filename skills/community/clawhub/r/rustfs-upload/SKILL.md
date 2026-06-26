---
name: rustfs-upload
description: 上传图片/文件到 RustFS 对象存储，返回公开访问链接。当用户说"上传到 rustfs"、"rustfs 图床"、"用 rc 上传"时触发。
---

# rustfs-upload - RustFS 图床上传

使用 `rc` 命令行工具上传文件到 RustFS（或兼容 S3 的对象存储），并返回拼接后的公开访问 URL。

## 前置环境变量

在调用本技能前，请确保以下环境变量已正确设置：

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `RUSTFS_ENDPOINT` | RustFS 服务地址 | `http://127.0.0.1:9000` |
| `RUSTFS_ACCESS_KEY` | Access Key | `your-access-key` |
| `RUSTFS_SECRET_KEY` | Secret Key | `your-secret-key` |
| `RUSTFS_BUCKET` | 目标存储桶名称 | `my-bucket` |
| `RUSTFS_PUBLIC_DOMAIN` | 公开访问域名（用于拼接 URL） | `http://127.0.0.1:9001` |

若未设置，脚本会尝试从默认配置文件中读取（`~/.config/rc/config.toml`）。

## 触发场景

- "上传到 rustfs"
- "rustfs 图床上传这张图"
- "用 rc 传一下这个文件"
- "rc upload"

## 使用方式

```bash
bash ~/.openclaw/skills/rustfs-upload/scripts/upload.sh /path/to/image.png
```

## 输出

成功后返回 JSON：

```json
{
  "url": "http://127.0.0.1:9001/my-bucket/filename.png",
  "bucket": "my-bucket",
  "object": "filename.png",
  "size": "377716",
  "endpoint": "http://127.0.0.1:9000"
}
```

## 依赖
- rc —— RustFS 命令行客户端

- jq —— JSON 解析工具（可选，用于格式化输出）

## 不做什么

- 不编辑图片（裁剪、压缩等）
- 不提供批量上传
- 不提供图片管理功能
- 不提供删除功能（图片会自动过期）