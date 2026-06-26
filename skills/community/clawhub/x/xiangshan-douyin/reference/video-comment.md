# 获取抖音视频一级评论

获取抖音视频的一级评论列表。

## 使用说明

用户需要提供以下参数（通过 $ARGUMENTS 传入或交互式询问）：

- `aweme_id` 或 `share_text`（二选一必填）
  - `aweme_id`: 抖音视频的 aweme_id（视频ID）
  - `share_text`: 视频分享文本/链接
- `count`（可选，默认 10）: 每页返回评论数量
- `cursor`（可选，默认 "0"）: 翻页游标，传入上一次返回的 cursor 值

## 执行步骤

1. 从 $ARGUMENTS 中解析参数。如果参数不完整，向用户询问缺失的必填参数。
2. 读取 API Key：优先从环境变量 `XS_API_KEY` 获取，如果未设置则向用户询问。
3. 使用 curl 调用接口：

```bash
curl -s --location 'https://api.xsdata.top/api/v1/goa/douyin/fetch-video-comment' \
--header 'x-api-key: <api_key>' \
--header 'Content-Type: application/json' \
--data '{
  "aweme_id": "<aweme_id>",
  "share_text": "<share_text>",
  "count": 10,
  "cursor": "0"
}'
```

4. 解析返回的 JSON，提取关键字段并以清晰的表格形式呈现给用户：
   - 每条评论的：
     - `cid`（评论ID）
     - `text`（评论内容）
     - `create_time`（评论时间，转换为可读日期）
     - `digg_count`（点赞数）
     - `reply_comment_total`（回复数）
     - `user.nickname`（评论者昵称）
     - `ip_label`（IP 属地）
     - `is_hot`（是否热门评论）
   - 如果有 `has_more` 和 `cursor`，提示用户可以继续翻页

5. 如果 `success` 为 false，展示错误信息给用户。

## 注意事项

- 该接口消耗 API 积分，请提醒用户
- `aweme_id` 和 `share_text` 至少填写一个
- 可以接受用户直接粘贴抖音视频的分享链接作为 `share_text`
- 评论可能较多，默认展示第一页，询问用户是否需要翻页
- 如果用户需要查看子评论（回复），提醒用户可以使用「获取视频子评论v2」接口
