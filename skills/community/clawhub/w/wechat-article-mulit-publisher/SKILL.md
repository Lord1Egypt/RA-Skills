---
name: wechat-article-mulit-publisher
description: 从 Markdown 文件或网页链接提取文章并发布到微信公众号。支持多账号管理、两种排版模板（standard/viral）、自动生成封面图和草稿发布。
---

# WeChat Article Mulit Publisher

## 功能特性

- 多账号支持：通过 `--account` 指定发布到哪个公众号
- 两种排版模板：`standard`（科技风格）和 `viral`（高传播风格）
- 自动生成封面图（无本地图片时）
- 支持 `--dry-run` 预览
- 支持直接发布草稿 `--publish`
- 文章内图片自动上传：自动将文章中的图片上传到微信素材库并替换为微信 CDN URL
- 草稿管理：支持列出草稿列表、删除草稿
- 素材管理：支持单独上传图片到素材库（本地文件或网络 URL）

## 配置

编辑 `config.json`：

```json
{
  "default_account": "your_account",
  "accounts": {
    "your_account": {
      "name": "公众号名称",
      "app_id": "wx...",
      "app_secret": "...",
      "author": "作者",
      "default_template": "standard",
      "topics": ["科技", "AI", "人工智能"]
    },
    "account2": {
      "name": "第二个公众号",
      "app_id": "wx...",
      "app_secret": "...",
      "author": "作者",
      "default_template": "viral",
      "topics": ["汽车", "新能源", "电动车"]
    }
  }
}
```

| 字段                          | 必填 | 说明                               |
| ----------------------------- | ---- | ---------------------------------- |
| `default_account`             | 是   | 默认使用的账号名                   |
| `accounts[].name`             | 是   | 公众号名称（显示用）               |
| `accounts[].app_id`           | 是   | 微信公众号 AppID                   |
| `accounts[].app_secret`       | 是   | 微信公众号 AppSecret               |
| `accounts[].author`           | 否   | 默认作者，可被 `--author` 覆盖     |
| `accounts[].default_template` | 否   | 默认模板，默认 `standard`          |
| `accounts[].topics`           | 否   | 公众号相关领域关键词，用于自动匹配 |

## 安装依赖

```bash
pip install -r scripts/requirements.txt
```

## 使用方法

```bash
# 列出所有已配置的账号
python scripts/publish_wechat.py --list-accounts

# 预览（不调用微信 API）
python scripts/publish_wechat.py <文章.md> --dry-run

# 发布到默认账号
python scripts/publish_wechat.py <文章.md>

# 发布到指定账号
python scripts/publish_wechat.py <文章.md> --account account2

# 直接发布（跳过草稿直接发布）
python scripts/publish_wechat.py <文章.md> --publish --status

# 列出草稿箱
python scripts/publish_wechat.py --list-drafts

# 删除草稿
python scripts/publish_wechat.py --delete-draft <media_id>

# 上传本地图片到素材库
python scripts/publish_wechat.py --upload-material /path/to/image.jpg

# 上传网络图片到素材库
python scripts/publish_wechat.py --upload-material-url https://example.com/image.jpg
```

## 命令行参数

| 参数              | 说明                            |
| ----------------- | ------------------------------- |
| `--account`       | 指定公众号账号（账号标识名）    |
| `--list-accounts` | 列出所有已配置的账号            |
| `--template`      | 覆盖模板：`standard` 或 `viral` |
| `--author`        | 覆盖作者名                      |
| `--cover-image`   | 指定本地封面图路径              |
| `--source-url`    | 覆盖原文链接                    |
| `--dry-run`       | 仅渲染预览，不调用微信 API      |
| `--publish`       | 草稿创建后直接提交发布          |
| `--status`        | 查询发布状态                    |
| `--list-drafts`   | 列出草稿箱中的所有草稿          |
| `--delete-draft`  | 删除指定 media_id 的草稿        |
| `--upload-material` | 上传本地图片到素材库（传入图片路径） |
| `--upload-material-url` | 上传网络图片到素材库（传入图片URL） |

## 输出

成功时返回 JSON：
```json
{
  "success": true,
  "account": "your_account",
  "title": "文章标题",
  "draft_media_id": "...",
  "preview_html": "路径/to-preview.html"
}
```
