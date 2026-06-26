# Z视介 APP 能力 (zmg-zsj-skill)

提供 Z视介 APP 的核心业务能力，支持直播搜索浏览、短视频综艺内容获取、热门话题榜单、APP 页面跳转、内容发布等功能。

## 能力清单

| 能力分类 | Function | 说明 |
|----------|----------|------|
| 搜索 | `search_hot` | 获取平台热门搜索词榜单 |
| 搜索 | `search_live` | 关键词搜索直播内容 |
| 搜索 | `search_variety` | 关键词搜索综艺内容 |
| 直播 | `get_hot_live_list` | 获取热门直播列表 |
| 直播 | `get_live_detail` | 根据直播 ID 获取详情页地址 |
| 直播 | `watch_live_channel` | 观看电视频道直播（浙江卫视、钱江都市等） |
| 综艺 | `get_variety_list` | 获取热门综艺榜单 |
| 短视频 | `get_short_video_list` | 获取热门短视频榜单 |
| APP | `open_app_page` | 打开 APP 指定页面（返回唤端链接） |
| 创作 | `publish_post` | 发布图文动态 |
| 创作 | `publish_short_video` | 发布短视频 |
| 消息中心 | `get_message_list` | 获取消息列表（@我的/评论回复/点赞） |
| UGC | `get_user_content_list` | 获取用户短视频作品列表 |
| UGC | `get_user_post_list` | 获取用户图文动态作品列表 |
| UGC | `get_user_audio_list` | 获取用户音频作品列表（如KTV录音） |
| UGC | `delete_article` | 删除作品（需先获取作品ID） |


## 使用场景说明

### 搜索场景
- 用户想了解当前热点 → 使用 `search_hot`
  - 无需参数，返回热门搜索词列表
  - 例："最近有什么热搜"、"现在大家在搜什么"
- 用户想找某个直播 → 使用 `search_live` 并传入关键词
  - 例："帮我搜一下周杰伦的直播"、"找一下游戏直播"
- 用户想找某个综艺 → 使用 `search_variety` 并传入关键词
  - 例："帮我搜奔跑吧"、"有没有音乐类的综艺"

### 内容浏览场景
- 用户想看热门直播 → 使用 `get_hot_live_list`
  - 返回当前热门直播列表，包含直播间 ID、标题、副标题和直播观看链接
  - 例："现在有什么直播"、"看看热门直播"
- 用户想进入某个具体直播间 → 使用 `get_live_detail` 并传入 liveId
  - 返回直播详情 H5 页面链接和 APP schema
  - 例：用户从 `get_hot_live_list` 结果中点击某个直播间时调用
- 用户想看电视直播 → 使用 `watch_live_channel` 并传入频道名称
  - 支持频道：浙江卫视、钱江都市、经济生活、教科影视、民生休闲、新闻频道、少儿频道、浙江国际、好易购、之江纪录
  - 返回频道对应的直播 H5 页面链接
  - 例："我想看浙江卫视"、"打开钱江都市"、"看电视"、"看新闻"
  - 不传或匹配不上时默认返回浙江卫视
- 用户想看热门综艺 → 使用 `get_variety_list`
  - 返回热门综艺榜单，每条包含综艺名称和播放页链接
  - 例："有什么综艺可以看"、"推荐一些综艺"、"最近有什么好看的综艺"
- 用户想看热门短视频 → 使用 `get_short_video_list`
  - 返回短视频榜单，每条包含标题和分享页链接
  - 例："看看热门短视频"、"推荐一些短视频"

### APP 交互场景
- 需要引导用户打开 APP 到指定页面 → 使用 `open_app_page` 并传入 schema
  - 返回唤端链接（H5 页面），前端可以超文本链接形式展示，用户点击即可唤起 APP
  - 例："打开APP"、"去APP里看"

### 创作场景
- 用户想发布一条图文动态 → 使用 `publish_post`
  - 必填：title（动态文字内容）
  - 可选：img_array（图片列表，含 pic/height/wide）、tags（标签）、description（描述）
  - 发布成功返回 article_id
  - 例："帮我发一条动态"、"发布一条图文，内容是xxx"
- 用户想发布一条短视频 → 使用 `publish_short_video`
  - 必填：title（标题）、video_url（视频地址）
  - 可选：cover_img（封面图）、width/height（视频尺寸）、play_time（时长 ["时","分","秒"]）、tags（标签）、description（描述）
  - 发布成功返回 article_id
  - 例："帮我发布一个短视频"、"上传视频到Z视介"

### 消息中心场景
- 用户想看谁@了自己 → 使用 `get_message_list` 传入 `msg_type: "mention"`
  - 返回 @我的 消息列表，包含用户名、头像、动态内容
  - 例："看看谁@了我"、"有人@我吗"
- 用户想看评论/回复 → 使用 `get_message_list` 传入 `msg_type: "comment"`
  - 返回评论/回复消息列表，包含评论内容、被评论的动态信息
  - 例："查看评论消息"、"有人评论我吗"
- 用户想看点赞消息 → 使用 `get_message_list` 传入 `msg_type: "like"`
  - 返回点赞消息列表
  - 例："查看点赞"、"谁给我点了赞"

### 作品列表场景
- 用户想看自己的短视频作品 → 使用 `get_user_content_list`
  - 返回短视频作品列表，包含标题、内容、封面、点赞数、评论数、浏览数、作品类型
  - **用户身份由系统自动识别（从授权 token 中提取 uid），调用方不要传 uid、accessUuid 等用户标识参数**
  - 例："看看我的作品"、"查看我的短视频"
- 用户想看自己的图文动态 → 使用 `get_user_post_list`
  - 返回图文动态作品列表
  - **用户身份由系统自动识别，调用方不要传 uid、accessUuid 等用户标识参数**
  - 例："我发过的图文动态"、"查看我的图文"
- 用户想看自己的音频作品 → 使用 `get_user_audio_list`
  - 返回音频作品列表（如KTV录音）
  - **用户身份由系统自动识别，调用方不要传 uid、accessUuid 等用户标识参数**
  - 例："我有哪些音频"、"查看我的KTV录音"

### 作品管理场景
- 用户想删除某个作品 → 使用 `delete_article` 传入 `article_id`
  - **必须先调用 `get_user_content_list`、`get_user_post_list` 或 `get_user_audio_list` 获取作品列表，从中取 `id` 字段作为 article_id**
  - 删除后不可恢复，AI 应在删除前向用户确认
  - 例："删除我的第一条作品"、"把标题为xxx的作品删掉"

## MCP 接入配置

MCP Server 地址（已内置于 skill.json）：

```json
{
  "mcp": {
    "transport": "sse",
    "url": "https://zmg-mcp.cztv.com/sse",
    "auth": {
      "type": "bearer",
      "header": "Authorization",
      "token_prefix": "zmg_",
      "acquire_url": "https://zmg-mcp.cztv.com"
    }
  }
}
```

**客户端配置示例**（将 `<ai_token>` 替换为实际 token）：

```json
{
  "mcpServers": {
    "zmg-zsj-skill": {
      "url": "https://zmg-mcp.cztv.com/sse",
      "headers": {
        "Authorization": "Bearer <ai_token>"
      }
    }
  }
}
```

## 鉴权模型

MCP Server 无状态，不管理用户 session。鉴权通过每次请求携带的 `ai_token` 完成：

- **ai_token 来源**：用户 APP 扫码授权后签发（格式 `zmg_xxxxx`），存 Redis
- **获取方式**：访问 https://zmg-mcp.cztv.com 扫码授权，获取 `ai_token` 后填入客户端配置
- **传递方式**：客户端在 MCP 请求中设置 `Authorization: Bearer <ai_token>`
- **校验方**：NG Gateway 通过 Redis 校验 ai_token 有效性，获取 sessionId 后注入业务请求

## 注意事项

- `channel` 参数为频道名称（如"浙江卫视"），支持模糊匹配，匹配不上时默认返回浙江卫视
- `get_live_detail` 传入直播 ID 即可获取详情页链接
- `open_app_page` 返回的链接可直接用作超链接，用户点击即可唤起 APP
- 发布接口（`publish_post` / `publish_short_video`）需要用户已授权，未授权或授权过期时返回 401
- 调用方无需传入 uid、sessionId 等敏感信息，系统会自动处理

## ⚠️ 授权失效处理协议（最高优先级）

**当任何接口返回 `code: 401` 时，必须立即执行以下流程，不可跳过：**

1. **立即停止当前任务**，不要继续尝试调用任何接口
2. **告诉用户需要扫码授权**，展示以下内容：
   - 提示文字："需要授权才能使用此功能，请用 Z视介 APP 扫描下方二维码授权"
   - **以超链接形式展示授权地址**：[点击扫码授权](https://zmg-mcp.cztv.com)
   - 授权页面地址：`https://zmg-mcp.cztv.com`
3. 用户完成扫码后，将新的 ai_token 更新到 MCP 配置的 `Authorization: Bearer <ai_token>` 中
4. 更新 token 后可重新尝试原请求

**401 响应格式：**

```json
{
  "code": 401,
  "message": "授权已失效，请重新扫码授权",
  "action": "REAUTHORIZE",
  "authorize_url": "https://zmg-mcp.cztv.com"
}
```

**绝对禁止：**
- 收到 401 后告诉用户"我没有权限"或"无法完成"就结束对话 — 必须引导扫码
- 无视 401 直接重试请求
- 只返回错误信息而不提供授权链接
