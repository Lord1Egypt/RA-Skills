# WeChat MP Publisher

OpenClaw Skill for publishing articles to WeChat Official Account (微信公众号文章自动发布工具)

## Description

This skill enables AI agents to publish articles to WeChat Official Accounts using the WeChat MP API. It supports:

- AccessToken management with automatic caching and refresh
- Media upload (images, thumbnails, videos)
- Article draft creation and management
- Publishing articles to followers
- Querying publish status and drafts

## Tools

### wechat-mp-publish

Publish a WeChat Official Account article (发布微信公众号文章)

**Parameters:**
- `title` (string, required): Article title (文章标题)
- `content` (string, required): Article content in HTML format (正文内容，支持 HTML)
- `cover_media_id` (string, required): Cover image media_id obtained from upload (封面图片素材 ID)
- `author` (string, optional): Author name (作者名)
- `digest` (string, optional): Article summary/abstract (文章摘要)
- `content_source_url` (string, optional): Original source URL (原文链接)
- `publish` (boolean, optional): Whether to publish immediately (default: true). Set to false to save as draft. (是否立即发布，false 则保存为草稿)

**Returns:**
```json
{
  "success": true,
  "message": "文章已创建并提交发布",
  "data": {
    "media_id": "draft media id",
    "publish_id": "publish task id"
  }
}
```

**Example:**
```yaml
tool: wechat-mp-publish
params:
  title: "我的第一篇文章"
  content: "<p>这是一篇测试文章</p>"
  cover_media_id: "MEDIA_ID_FROM_UPLOAD"
  author: "张三"
  publish: true
```

---

### wechat-mp-upload-media

Upload media file to WeChat server (上传素材到微信服务器)

**Parameters:**
- `file_path` (string, required): Local file path to upload (本地文件路径)
- `type` (string, optional): Media type - `image`, `thumb`, `voice`, `video` (default: `image`) (素材类型)

**Returns:**
```json
{
  "success": true,
  "message": "素材上传成功",
  "data": {
    "media_id": "uploaded media id",
    "type": "image",
    "created_at": 1234567890
  }
}
```

**Example:**
```yaml
tool: wechat-mp-upload-media
params:
  file_path: "/path/to/image.jpg"
  type: "image"
```

---

### wechat-mp-upload-cover

Upload cover image (shortcut for thumb type upload) (上传封面图片)

**Parameters:**
- `file_path` (string, required): Local file path to cover image (封面图片路径)

**Returns:**
```json
{
  "success": true,
  "message": "封面上传成功",
  "data": {
    "media_id": "cover media id"
  }
}
```

**Example:**
```yaml
tool: wechat-mp-upload-cover
params:
  file_path: "/path/to/cover.jpg"
```

---

### wechat-mp-query-drafts

Query draft list (查询草稿列表)

**Parameters:**
- `offset` (number, optional): Pagination offset (default: 0) (分页偏移量)
- `count` (number, optional): Items per page, max 20 (default: 10) (每页数量)

**Returns:**
```json
{
  "success": true,
  "message": "获取草稿列表成功，共 5 条",
  "data": {
    "total_count": 5,
    "item_count": 5,
    "items": [...]
  }
}
```

---

### wechat-mp-query-publish-status

Query publish status by publish_id (查询发布状态)

**Parameters:**
- `publish_id` (string, required): Publish task ID returned from publish (发布任务 ID)

**Returns:**
```json
{
  "success": true,
  "message": "发布状态: 成功",
  "data": {
    "publish_id": "PUBLISH_ID",
    "publish_status": 0,
    "status_text": "成功",
    "article_id": "ARTICLE_ID",
    "article_detail": {...}
  }
}
```

**Status codes:**
- 0: Success (成功)
- 1: Publishing (发布中)
- 2: Original content review failed (原创审核失败)
- 3: Failed (失败)

---

### wechat-mp-delete-draft

Delete a draft by media_id (删除草稿)

**Parameters:**
- `media_id` (string, required): Draft media_id to delete (草稿素材 ID)

**Returns:**
```json
{
  "success": true,
  "message": "草稿删除成功"
}
```

## Configuration

Create a configuration file at `~/.openclaw/config/wechat-mp.json`:

```json
{
  "app_id": "your-wechat-app-id",
  "app_secret": "your-wechat-app-secret",
  "default_author": "默认作者名",
  "access_token_cache_file": "~/.openclaw/.wechat_mp_token.json"
}
```

Or use environment variables:
```bash
export WECHAT_MP_APP_ID="your-app-id"
export WECHAT_MP_APP_SECRET="your-app-secret"
export WECHAT_MP_DEFAULT_AUTHOR="默认作者"
export WECHAT_MP_TOKEN_CACHE="~/.openclaw/.wechat_mp_token.json"
```

## Prerequisites

1. WeChat Official Account (Service Account/认证服务号) with API access
2. IP whitelist configured in WeChat MP Admin Portal
3. Node.js >= 18

## Installation

```bash
cd /Users/zhizi/.openclaw/workspace/agents/dev-team/projects/active/wechat-mp-publisher
npm install
npm run build
```

## Usage Example

### Complete workflow

```typescript
// 1. Upload cover image
const coverResult = await wechatMpUploadCover({
  file_path: "/path/to/cover.jpg"
});

// 2. Publish article
const publishResult = await wechatMpPublish({
  title: "我的文章标题",
  content: "<p>文章内容</p>",
  cover_media_id: coverResult.data.media_id,
  author: "作者名",
  publish: true
});

// 3. Check publish status
const status = await wechatMpQueryPublishStatus({
  publish_id: publishResult.data.publish_id
});
```

## Project Structure

```
wechat-mp-publisher/
├── SKILL.md                    # This file
├── README.md                   # Project documentation
├── package.json                # Dependencies
├── tsconfig.json               # TypeScript config
├── src/
│   ├── index.ts               # Main entry & OpenClaw tools
│   ├── auth.ts                # AccessToken management
│   ├── media.ts               # Media upload
│   ├── article.ts             # Article management
│   └── types.ts               # TypeScript types
├── scripts/                    # CLI scripts (optional)
└── tests/                      # Test files
```

## Error Handling

All tools return a standardized response:

```typescript
{
  success: boolean;    // Operation success status
  message: string;     // Human-readable message
  data?: any;          // Response data on success
}
```

On failure, `success` will be `false` and `message` contains the error description.

## API Reference

Based on WeChat Official Account API:
- https://developers.weixin.qq.com/doc/offiaccount/en/Getting_Started/Overview.html

## License

MIT
