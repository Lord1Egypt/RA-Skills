# 获取抖音用户主页视频列表

获取抖音用户主页发布的视频列表。

## 使用说明

用户需要提供以下参数（通过 $ARGUMENTS 传入或交互式询问）：

- `sec_user_id` 或 `share_text`（二选一必填）
  - `sec_user_id`: 抖音用户的 sec_user_id
  - `share_text`: 用户主页分享文本/链接
- `count`（可选，默认 10）: 每页返回数量
- `max_cursor`（可选，默认 "0"）: 翻页游标，传入上一次返回的 max_cursor 值
- `filter_type`（可选，默认 0）: 过滤类型

## 执行步骤

1. 从 $ARGUMENTS 中解析参数。如果参数不完整，向用户询问缺失的必填参数。
2. 读取 API Key：优先从环境变量 `XS_API_KEY` 获取，如果未设置则向用户询问。
3. 使用 curl 调用接口：

```bash
curl -s --location 'https://api.xsdata.top/api/v1/goa/douyin/fetch-user-video-list' \
--header 'x-api-key: <api_key>' \
--header 'Content-Type: application/json' \
--data '{
  "sec_user_id": "<sec_user_id>",
  "share_text": "<share_text>",
  "count": "<count>",
  "max_cursor": "<max_cursor>",
  "filter_type": 0
}'
```

4. 解析返回的 JSON，提取关键字段并以清晰的表格/列表形式呈现给用户：
   - 每个视频的 `aweme_id`（视频ID）
   - `desc`（视频描述/标题）
   - `create_time`（发布时间，转换为可读日期）
   - `statistics` 中的 `digg_count`（点赞数）、`comment_count`（评论数）、`share_count`（分享数）、`play_count`（播放数）
   - `author.nickname`（作者昵称）
   - 如果返回结果中有 `has_more` 和 `max_cursor`，提示用户可以继续翻页

5. 如果 `success` 为 false，展示错误信息给用户。

## 注意事项

- 该接口消耗 API 积分，请提醒用户
- `sec_user_id` 和 `share_text` 至少填写一个
- 如果返回数据量较大，只展示前几条并询问用户是否需要查看更多
