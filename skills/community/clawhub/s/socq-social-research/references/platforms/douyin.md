# Douyin

Generated from SocQ Capability Registry schema `v1-9a87cca161f6`. Read this file when the request targets Douyin.

## Endpoint selection

| Endpoint | Use for | Input choice | Standard schema | Cost |
| --- | --- | --- | --- | --- |
| [`douyin/live-room-detail`](https://docs.socq.ai/api-manual/douyin/live-room-detail) | Collect public Douyin live room details. | room_id | `live-room@1.0` | 0.1 credits/request |
| [`douyin/product-data`](https://docs.socq.ai/api-manual/douyin/product-data) | Collect one page of public Douyin live room products. | author_id, room_id | `product@1.0` | 0.1 credits/request |
| [`douyin/user-profile`](https://docs.socq.ai/api-manual/douyin/user-profile) | Collect a public Douyin profile. | one of: url; user_id | `account@1.0` | 0.1 credits/request |
| [`douyin/user-videos`](https://docs.socq.ai/api-manual/douyin/user-videos) | Collect one page of public Douyin user videos. | one of: url; user_id | `reel-video@1.0` | 0.1 credits/request |
| [`douyin/video-comments`](https://docs.socq.ai/api-manual/douyin/video-comments) | Collect one page of public Douyin video comments. | url | `comment@1.0` | 0.1 credits/request |
| [`douyin/video-detail`](https://docs.socq.ai/api-manual/douyin/video-detail) | Collect public Douyin video details. | url | `reel-video@1.0` | 0.1 credits/request |
| [`douyin/video-search`](https://docs.socq.ai/api-manual/douyin/video-search) | Search public Douyin videos. | query | `reel-video@1.0` | 0.1 credits/request |

## Validated examples

### `douyin/live-room-detail`

Typed MCP tool: `socq_douyin_live_room_detail`

```json
{
  "room_id": "7462723839303093032"
}
```

### `douyin/product-data`

Typed MCP tool: `socq_douyin_product_data`

```json
{
  "room_id": "7356742011975715619",
  "author_id": "2207432981615527",
  "results_limit": 3
}
```

### `douyin/user-profile`

Typed MCP tool: `socq_douyin_user_profile`

```json
{
  "user_id": "MS4wLjABAAAAW9FWcqS7RdQAWPd2AA5fL_ilmqsIFUCQ_Iym6Yh9_cUa6ZRqVLjVQSUjlHrfXY1Y"
}
```

### `douyin/user-videos`

Typed MCP tool: `socq_douyin_user_videos`

```json
{
  "user_id": "MS4wLjABAAAANXSltcLCzDGmdNFI2Q_QixVTr67NiYzjKOIP5s03CAE",
  "results_limit": 3
}
```

### `douyin/video-comments`

Typed MCP tool: `socq_douyin_video_comments`

```json
{
  "url": "https://www.douyin.com/video/7448118827402972455",
  "results_limit": 3
}
```

### `douyin/video-detail`

Typed MCP tool: `socq_douyin_video_detail`

```json
{
  "url": "https://www.douyin.com/video/7448118827402972455"
}
```

### `douyin/video-search`

Typed MCP tool: `socq_douyin_video_search`

```json
{
  "query": "人工智能"
}
```
