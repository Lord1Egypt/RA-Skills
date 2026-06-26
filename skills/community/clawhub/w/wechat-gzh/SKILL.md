---
name: wechat-gzh
description: "微信公众号管理 skill。支持获取 Access Token、永久素材管理、发布能力（发布草稿、查询发布状态、获取已发布列表、删除发布文章）。触发词：微信公众号、wechat gzh、发布图文、素材管理。"
permissions:
  - type: context_reading
    purpose: "读取微信公众号配置和凭证"
    data_access: "Workspace files and environment variables"
  - type: api_calls
    purpose: "调用微信公众号 API"
    data_access: "WeChat Official Account API (api.weixin.qq.com)"
---

# WeChat GZH - 微信公众号管理

微信公众号 API 封装，支持素材管理和发布能力。

## 功能列表

### 1. 凭证管理
- `get_stable_access_token` - 获取稳定版 Access Token

### 2. 素材管理
- `add_material` - 上传永久素材（图片/视频/语音/缩略图）
- `get_material` - 获取永久素材

### 3. 发布能力
- `add_draft` - 新建草稿
- `get_draft` - 获取草稿列表
- `delete_draft` - 删除草稿
- `submit_publish` - 发布草稿
- `get_publish_status` - 发布状态查询
- `get_published_articles` - 获取已发布图文信息
- `get_published_list` - 获取已发布的消息列表
- `delete_publish` - 删除发布文章

## 配置

首次使用需要配置 AppID 和 AppSecret：

```bash
# 创建配置文件
cat > ~/.wechat_gzh_config.json << EOF
{
  "appid": "your_appid_here",
  "secret": "your_appsecret_here"
}
EOF

# 设置权限
chmod 600 ~/.wechat_gzh_config.json
```

## 使用方法

### Python API

```python
from scripts.wechat_gzh import WeChatGZH

# 初始化
wechat = WeChatGZH()

# 获取 Access Token
token = wechat.get_stable_access_token()

# 上传永久素材
result = wechat.add_material("/path/to/image.jpg", "image")
print(f"Media ID: {result['media_id']}")

# 上传视频素材
result = wechat.add_material(
    "/path/to/video.mp4",
    "video",
    video_info={"title": "我的视频", "introduction": "视频描述"}
)

# 获取已发布列表
articles = wechat.get_published_list(offset=0, count=10)

# 发布草稿
result = wechat.submit_publish(media_id="xxx")
```

### 命令行

```bash
# 获取 Access Token
python scripts/wechat_gzh.py get-token

# 上传永久素材
python scripts/wechat_gzh.py upload-material -f /path/to/image.jpg -t image
python scripts/wechat_gzh.py upload-material -f /path/to/video.mp4 -t video --title "视频标题"

# 获取已发布列表
python scripts/wechat_gzh.py list-published --offset 0 --count 10

# 发布草稿
python scripts/wechat_gzh.py publish --media-id xxx

# 查询发布状态
python scripts/wechat_gzh.py status --publish-id xxx
```

## API 端点

### 凭证
- **获取 Stable Access Token**: `POST https://api.weixin.qq.com/cgi-bin/stable_token`

### 素材
- **上传永久素材**: `POST https://api.weixin.qq.com/cgi-bin/material/add_material`
- **获取永久素材**: `POST https://api.weixin.qq.com/cgi-bin/material/get_material`

### 发布
- **新建草稿**: `POST https://api.weixin.qq.com/cgi-bin/draft/add`
- **获取草稿列表**: `POST https://api.weixin.qq.com/cgi-bin/draft/batchget`
- **删除草稿**: `POST https://api.weixin.qq.com/cgi-bin/draft/delete`
- **发布草稿**: `POST https://api.weixin.qq.com/cgi-bin/freepublish/submit`
- **发布状态查询**: `POST https://api.weixin.qq.com/cgi-bin/freepublish/get`
- **获取已发布图文信息**: `POST https://api.weixin.qq.com/cgi-bin/freepublish/getarticle`
- **获取已发布的消息列表**: `POST https://api.weixin.qq.com/cgi-bin/freepublish/batchget`
- **删除发布文章**: `POST https://api.weixin.qq.com/cgi-bin/freepublish/delete`

## 注意事项

1. **Access Token 缓存**: Token 有效期 7200 秒，建议缓存复用
2. **调用频率**: 每分钟限制 1 万次，每天 50 万次
3. **强制刷新**: 每天限用 20 次，需间隔 30 秒
4. **IP 白名单**: 需要在公众号后台配置服务器 IP 白名单
5. **权限要求**: 部分接口需要认证服务号

## 错误处理

常见错误码：
- `40001`: invalid credential - access_token 无效
- `40007`: invalid media_id - 无效的媒体 ID
- `48001`: api unauthorized - 接口未授权

完整错误码参考：https://developers.weixin.qq.com/doc/oplatform/developers/errCode/errCode.html

## 示例场景

### 发布一篇图文

```python
# 1. 准备图文素材（需要先上传）
# 2. 创建草稿
draft = wechat.add_draft(articles=[{
    "title": "标题",
    "content": "正文内容",
    "thumb_media_id": "封面图 media_id"
}])

# 3. 发布草稿
result = wechat.submit_publish(media_id=draft['media_id'])

# 4. 查询发布状态
status = wechat.get_publish_status(publish_id=result['publish_id'])
```

## 参考文档

- [获取稳定版接口调用凭据](https://developers.weixin.qq.com/doc/subscription/api/base/api_getstableaccesstoken.html)
- [获取永久素材](https://developers.weixin.qq.com/doc/subscription/api/material/permanent/api_getmaterial.html)
- [发布能力](https://developers.weixin.qq.com/doc/subscription/api/public/api_freepublish_batchget.html)
