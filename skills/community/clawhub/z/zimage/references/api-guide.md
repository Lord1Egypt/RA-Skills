# z-image API Guide

## Endpoint

- URL: https://agent.mathmind.cn/minimalist/api/tywx/zImage
- Method: POST
- Headers:
  - x-api-key: required
  - Content-Type: application/json

## Request Body

- prompt: string, required
- size: string, optional, format WIDTH*HEIGHT

默认值：`1024*1536`

总像素范围限制：

- 最小：`512*512`
- 最大：`2048*2048`

推荐范围：

- 建议总像素在 `1024*1024` 到 `1536*1536` 之间

## 比例到 size 的推荐映射

### 1024 档

- 1:1 -> 1024*1024
- 2:3 -> 832*1248
- 3:2 -> 1248*832
- 3:4 -> 864*1152
- 4:3 -> 1152*864
- 7:9 -> 896*1152
- 9:7 -> 1152*896
- 9:16 -> 720*1280
- 9:21 -> 576*1344
- 16:9 -> 1280*720
- 21:9 -> 1344*576

### 1280 档

- 1:1 -> 1280*1280
- 2:3 -> 1024*1536
- 3:2 -> 1536*1024
- 3:4 -> 1104*1472
- 4:3 -> 1472*1104
- 7:9 -> 1120*1440
- 9:7 -> 1440*1120
- 9:16 -> 864*1536
- 9:21 -> 720*1680
- 16:9 -> 1536*864
- 21:9 -> 1680*720

### 1536 档

- 1:1 -> 1536*1536
- 2:3 -> 1248*1872
- 3:2 -> 1872*1248
- 3:4 -> 1296*1728
- 4:3 -> 1728*1296
- 7:9 -> 1344*1728
- 9:7 -> 1728*1344
- 9:16 -> 1152*2048
- 9:21 -> 864*2016
- 16:9 -> 2048*1152
- 21:9 -> 2016*864

## cURL Example

```bash
curl --location 'https://agent.mathmind.cn/minimalist/api/tywx/zImage' \
--header 'x-api-key: <YOUR_X_API_KEY>' \
--header 'Content-Type: application/json' \
--data '{
  "prompt": "Elegant Christmas tree decorated with gold and white ornaments, glowing lights, and a soft gradient background",
  "size": "1024*1536"
}'
```

## Common Error Hints

- 401/403: invalid or missing x-api-key
- 429: rate limited, retry later
- 5xx: service unavailable, retry with same payload