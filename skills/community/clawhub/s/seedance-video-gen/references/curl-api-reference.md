# Seedance curl API 参考

> 完整 curl 命令参考。日常使用推荐 Python CLI（`{baseDir}/seedance.py`），此文件仅供调试或 CLI 不可用时参考。

## Base URL

```
https://ark.cn-beijing.volces.com/api/v3
```

## 创建任务

### Mode A: 文生视频

```bash
TASK_RESULT=$(curl -s -X POST "https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ARK_API_KEY" \
  -d '{
    "model": "doubao-seedance-1-5-pro-251215",
    "content": [{"type": "text", "text": "YOUR_PROMPT"}],
    "ratio": "16:9", "duration": 5, "resolution": "720p", "generate_audio": true
  }')
TASK_ID=$(echo "$TASK_RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")
```

### Mode B: 图生视频（首帧）

**URL 图片：**
```bash
curl -s -X POST "https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks" \
  -H "Content-Type: application/json" -H "Authorization: Bearer $ARK_API_KEY" \
  -d '{
    "model": "doubao-seedance-1-5-pro-251215",
    "content": [
      {"type": "text", "text": "YOUR_PROMPT"},
      {"type": "image_url", "image_url": {"url": "IMAGE_URL"}, "role": "first_frame"}
    ],
    "ratio": "adaptive", "duration": 5, "resolution": "720p", "generate_audio": true
  }'
```

**本地图片（base64）：**
```bash
IMG_BASE64=$(base64 < /path/to/image.png | tr -d '\n')
IMG_DATA_URL="data:image/png;base64,${IMG_BASE64}"
# 用 IMG_DATA_URL 替换上面的 IMAGE_URL
```

### Mode C: 首尾帧

```bash
"content": [
  {"type": "text", "text": "YOUR_PROMPT"},
  {"type": "image_url", "image_url": {"url": "FIRST_URL"}, "role": "first_frame"},
  {"type": "image_url", "image_url": {"url": "LAST_URL"}, "role": "last_frame"}
]
```

### Mode D: 参考图（Lite I2V）

```bash
"content": [
  {"type": "text", "text": "[图1]的人物在跳舞"},
  {"type": "image_url", "image_url": {"url": "REF_URL"}, "role": "reference_image"}
]
# model 必须用 doubao-seedance-1-0-lite-i2v-250428
```

## 轮询任务状态

```bash
while true; do
  STATUS_RESULT=$(curl -s -X GET ".../tasks/${TASK_ID}" -H "Authorization: Bearer $ARK_API_KEY")
  STATUS=$(echo "$STATUS_RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin)['status'])")
  [ "$STATUS" = "succeeded" ] && break
  [ "$STATUS" = "failed" ] || [ "$STATUS" = "expired" ] && break
  sleep 15
done
```

## 其他操作

```bash
# 查询任务
curl -s -X GET ".../tasks/${TASK_ID}" -H "Authorization: Bearer $ARK_API_KEY"

# 列表（分页）
curl -s -X GET ".../tasks?page_num=1&page_size=10" -H "Authorization: Bearer $ARK_API_KEY"

# 删除/取消
curl -s -X DELETE ".../tasks/${TASK_ID}" -H "Authorization: Bearer $ARK_API_KEY"
```

## Draft Mode（Seedance 1.5 Pro）

```bash
# 1. 创建草稿（便宜预览）
"draft": true, "resolution": "480p"

# 2. 从草稿生成正式视频
"content": [{"type": "draft_task", "draft_task": {"id": "DRAFT_TASK_ID"}}],
"resolution": "720p"
```

## 连续视频（用尾帧串接）

```bash
# 第一段设置 "return_last_frame": true
# 完成后获取 last_frame_url，作为下一段的 first_frame
```
