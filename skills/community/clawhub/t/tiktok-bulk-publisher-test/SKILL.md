# TikTok 批量发布技能

## 功能概述
TikTok批量视频发布技能，实现自动化上传和发布TikTok视频内容。支持以下功能：

- 批量视频上传到TikTok
- 自定义视频标题和描述
- 隐私级别设置（公开、互关好友可见、仅自己可见）
- 评论、合拍、拼接功能控制
- 分片上传大文件（支持10MB+视频）
- 发布状态查询
- OAuth 2.0 授权流程支持

## 技术要求
- 需要 TikTok Content Posting API 权限
- 需要 `video.publish` 和 `user.info.basic` Scope
- 支持 FILE_UPLOAD 和 PULL_FROM_URL 两种上传方式

## 使用方法
### 环境变量配置
```bash
export TIKTOK_CLIENT_KEY="your_client_key"
export TIKTOK_CLIENT_SECRET="your_client_secret"
export TIKTOK_ACCESS_TOKEN="your_access_token"
```

### 命令行使用
```bash
python tiktok_publisher.py --video /path/to/video.mp4 --title "视频标题" --privacy PUBLIC_TO_EVERYONE
```

### Python API 使用
```python
from tiktok_publisher import TikTokPublisher

publisher = TikTokPublisher(client_key, client_secret, access_token)
result = publisher.upload_video(
    video_path="/path/to/video.mp4",
    title="视频标题",
    privacy_level="PUBLIC_TO_EVERYONE",
    disable_comment=False,
    disable_duet=False,
    disable_stitch=False
)

if result['success']:
    print(f"发布成功: {result['video_url']}")
else:
    print(f"发布失败: {result['error']}")
```

## 依赖
- Python 3.7+
- requests
- pathlib

## 注意事项
1. 视频文件大小限制：单个视频不超过500MB
2. 视频格式要求：MP4格式，H.264编码
3. 标题长度限制：不超过2200个字符
4. 需要先完成TikTok开发者账号认证和应用创建
5. 访问令牌有效期为2小时，需要定期刷新

## 错误处理
常见错误代码：
- `missing_scope`: 缺少必要的API权限
- `invalid_token`: 访问令牌无效或过期
- `video_too_large`: 视频文件超过大小限制
- `invalid_video_format`: 视频格式不支持