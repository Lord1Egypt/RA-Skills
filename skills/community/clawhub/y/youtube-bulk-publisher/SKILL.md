# YouTube 批量发布器

YouTube 批量视频发布工具，支持自动上传、元数据设置、缩略图上传等功能。

## 功能特性

- **批量视频上传**：支持多个视频文件的自动化上传
- **元数据管理**：自定义标题、描述、标签、分类和隐私设置
- **缩略图支持**：可为每个视频上传自定义缩略图
- **OAuth 2.0 认证**：安全的 Google API 认证流程
- **进度监控**：实时显示上传进度
- **状态查询**：可查询已上传视频的状态信息

## 使用方法

### 1. 准备凭证

在技能目录下创建 `credentials` 文件夹，并放入 YouTube OAuth 2.0 凭证文件：
- `youtube_credentials.json` - Google Cloud Console 下载的 OAuth 2.0 客户端凭证

### 2. 命令行使用

```bash
python youtube_publisher.py \
  --video /path/to/video.mp4 \
  --title "视频标题" \
  --description "视频描述" \
  --tags "标签1,标签2,标签3" \
  --privacy unlisted \
  --category 22 \
  --thumbnail /path/to/thumbnail.jpg
```

### 3. 编程接口

```python
from youtube_publisher import YouTubePublisher

# 初始化发布器
publisher = YouTubePublisher()

# 上传视频
result = publisher.upload_video(
    video_path="/path/to/video.mp4",
    title="视频标题",
    description="视频描述",
    tags=["标签1", "标签2"],
    category_id="22",
    privacy_status="unlisted",
    thumbnail_path="/path/to/thumbnail.jpg"
)

if result['success']:
    print(f"上传成功: {result['video_url']}")
else:
    print(f"上传失败: {result['error']}")
```

## 参数说明

### 视频参数
- `video_path`: 视频文件路径（必需）
- `title`: 视频标题（必需）
- `description`: 视频描述（可选）
- `tags`: 标签列表（可选）
- `category_id`: 分类 ID（默认 22=人物博客）
- `privacy_status`: 隐私状态（public/unlisted/private，默认 unlisted）
- `thumbnail_path`: 缩略图路径（可选）

### 返回结果
成功时返回：
```json
{
  "success": true,
  "video_id": "视频ID",
  "video_url": "https://www.youtube.com/watch?v=视频ID",
  "title": "视频标题"
}
```

失败时返回：
```json
{
  "success": false,
  "error": "错误信息"
}
```

## 依赖要求

- Python 3.7+
- google-api-python-client
- google-auth-httplib2
- google-auth-oauthlib

## 注意事项

1. 首次使用需要完成 OAuth 2.0 授权流程
2. 确保 YouTube Data API v3 已启用
3. 视频文件格式建议使用 MP4
4. 缩略图格式建议使用 JPG，尺寸至少 1280x720 像素