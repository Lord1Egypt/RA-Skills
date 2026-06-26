# 获取抖音视频统计数据（含播放数）

获取抖音视频的统计数据，包括播放数。

**特别说明**：抖音大多数接口已经不再返回作品的播放数，只能通过此接口获取。

## 可获取的统计数据

- `digg_count`：点赞数
- `download_count`：下载数
- `play_count`：播放数
- `share_count`：分享数

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
curl -s --location 'https://api.xsdata.top/api/v1/goa/douyin/fetch-video-statistics' \
--header 'x-api-key: <api_key>' \
--header 'Content-Type: application/json' \
--data '{
  "aweme_id": "<aweme_id>",
  "share_text": "<share_text>"
}'
```

4. 解析返回的 JSON，提取统计数据并以清晰的形式呈现给用户：
   - 👍 点赞数（digg_count）
   - ⬇️ 下载数（download_count）
   - ▶️ 播放数（play_count）
   - 🔗 分享数（share_count）

5. 如果 `success` 为 false，展示错误信息给用户。

## 注意事项

- 该接口消耗 API 积分，请提醒用户
- `aweme_id` 和 `share_text` 至少填写一个
- 可以接受用户直接粘贴抖音视频的分享链接作为 `share_text`
- 这是唯一能获取播放数的接口，其他接口的播放数字段通常为 0 或不返回
