# HTTP 请求示例

```bash
API_ROOT="${AI_SKILLS_API_URL:-https://ai-skills.open-idea.net}/api/v1"

curl --fail-with-body "$API_ROOT/spark-media/image" \
  -H "Authorization: Bearer ${AI_SKILLS_API_KEY:-$SPARK_MEDIA_API_KEY}" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: image-uuid-001" \
  -d '{"prompt":"雪山下的藏式村庄，电影感光线","width":1024,"height":1024,"count":1}'
```

```bash
curl --fail-with-body "$API_ROOT/spark-media/video" \
  -H "Authorization: Bearer ${AI_SKILLS_API_KEY:-$SPARK_MEDIA_API_KEY}" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: video-uuid-001" \
  -d '{"prompt":"云层缓慢掠过雪山","duration":5,"resolution":"720p","ratio":"16:9","watermark":false}'
```

创建返回 HTTP 202 后：

```bash
curl --fail-with-body "$API_ROOT/spark-media/video/TASK_ID" \
  -H "Authorization: Bearer ${AI_SKILLS_API_KEY:-$SPARK_MEDIA_API_KEY}"
```

图生图和图生视频将完整的 `data:image/png;base64,...` 放进 JSON 的 `image` 单值或 `images` 数组，两者二选一；不要使用 multipart。图生图 `images` 接受 1–5 张，图生视频接受 1–9 张，单张解码最大 5 MB，总计最大 20 MB。按数组顺序在提示词中引用“图 1、图 2”；所有参考图共同参与同一次创作。

多图请求体示意（占位内容需替换成真实本地图片的完整 data URL，不要直接发送省略号）：

```json
{"prompt":"保留图 1 商品，使用图 2 背景","images":["data:image/png;base64,...","data:image/jpeg;base64,..."]}
```

生产中使用 UUID 等真正唯一的幂等键；同一次请求重试需保持全部图片内容和顺序一致，避免重复生成和扣费。

创建响应的计费头是 `X-AI-Skills-Billing-Currency`、
`X-AI-Skills-Billing-Charged`、`X-AI-Skills-Billing-Balance`。
