# 获取抖音视频详情

获取抖音视频的详细信息。

## 使用说明

用户需要提供以下参数（通过 $ARGUMENTS 传入或交互式询问）：

- `aweme_id` 或 `share_text`（二选一必填）
  - `aweme_id`: 抖音视频的 aweme_id（视频ID）
  - `share_text`: 视频分享文本/链接

## 执行步骤

1. 从 $ARGUMENTS 中解析参数。如果参数不完整，向用户询问缺失的必填参数。
2. 读取 API Key：优先从环境变量 `XS_API_KEY` 获取，如果未设置则向用户询问。
3. 使用 curl 调用接口：

```bash
curl -s --location 'https://api.xsdata.top/api/v1/goa/douyin/fetch-video-detail' \
--header 'x-api-key: <api_key>' \
--header 'Content-Type: application/json' \
--data '{
  "aweme_id": "<aweme_id>",
  "share_text": "<share_text>"
}'
```

4. 解析返回的 JSON，提取关键字段并以清晰的形式呈现给用户：
   - `aweme_id`（视频ID）
   - `desc`（视频描述/标题）
   - `create_time`（发布时间，转换为可读日期）
   - `author.nickname`（作者昵称）、`author.uid`（作者ID）
   - `statistics`：
     - `digg_count`（点赞数）
     - `comment_count`（评论数）
     - `share_count`（分享数）
     - `play_count`（播放数）
     - `collect_count`（收藏数）
   - `video.play_addr`（视频播放地址）
   - `video.cover`（视频封面）
   - `video.duration`（视频时长，转换为 分:秒 格式）
   - `music.title`（背景音乐名称）
   - `music.author`（背景音乐作者）
   - `share_info`（分享信息）
   - `text_extra`（话题标签列表）
   - `video_tag`（视频标签）

5. 如果 `success` 为 false，展示错误信息给用户。

## 注意事项

- 该接口消耗 API 积分，请提醒用户
- `aweme_id` 和 `share_text` 至少填写一个
- 可以接受用户直接粘贴抖音视频的分享链接作为 `share_text`
- 返回数据可能非常庞大，只展示用户关心的核心字段
