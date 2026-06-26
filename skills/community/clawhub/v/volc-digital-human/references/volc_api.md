# 火山引擎数字人 API 参考

## 凭证配置

用户需要自行配置火山引擎 AK/SK，见上级目录 SKILL.md 中的配置说明。

**Region**: cn-north-1
**Service**: cv
**Endpoint**: https://visual.volcengineapi.com

## SDK 用法

```python
from volcengine.visual.VisualService import VisualService

service = VisualService()
service.set_ak(YOUR_AK)  # 替换为你的 AK
service.set_sk(YOUR_SK)  # 替换为你的 SK

# 提交任务
body = {"req_key": "...", "image_url": "..."}
resp = service.cv_submit_task(body)
task_id = resp['data']['task_id']

# 查询结果（轮询）
import json, time
for i in range(60):
    time.sleep(5)
    raw = service.json("CVGetResult", {}, json.dumps({"req_key": "...", "task_id": task_id}))
    result = json.loads(raw)
    if result['data']['status'] == 'done':
        break
```

## Step 1: 创建形象

**API**: `CVSubmitTask` + `CVGetResult`

**req_key**: `realman_avatar_picture_create_role`

**Body**:
```json
{
  "req_key": "realman_avatar_picture_create_role",
  "image_url": "https://..."  // 公开可访问的图片URL
}
```

**返回**:
```json
{
  "code": 10000,
  "data": {
    "task_id": "17333543019195298862"
  }
}
```

**查询返回** (status=done时):
```json
{
  "data": {
    "status": "done",
    "resp_data": "{\"resource_id\": \"57884593-68ce-4293-be72-cb9ef60d1bcf\", ...}"
  }
}
```

**注意**: 建议用闭口照片，开口的照片会被警告但仍可使用

---

## Step 2: TTS 配音

**工具**: `edge-tts` (微软免费TTS，已在服务器安装)

```bash
edge-tts --voice zh-CN-XiaoxiaoNeural --text "对白内容" --write-media output.mp3
```

**可选音色**:
- `zh-CN-XiaoxiaoNeural` - 女声，自然（推荐）
- `zh-CN-YunxiNeural` - 男声，阳光
- `zh-CN-YunxiaNeural` - 男声，可爱
- `zh-CN-XiaoyiNeural` - 女声，活泼

**音频上传**: `https://uguu.se/upload` (免费公开托管)

---

## Step 3: 视频合成

**API**: `CVSubmitTask` + `CVGetResult`

**req_key**: `realman_avatar_picture_v2`

**Body**:
```json
{
  "req_key": "realman_avatar_picture_v2",
  "resource_id": "57884593-68ce-4293-be72-cb9ef60d1bcf",
  "audio_url": "https://..."  // 公开可访问的音频URL (mp3)
}
```

**返回**:
```json
{
  "code": 10000,
  "data": {
    "task_id": "866562558524147465"
  }
}
```

**查询返回** (status=done时):
```json
{
  "data": {
    "status": "done",
    "resp_data": "{\"preview_url\": [\"https://...mp4?...\"]}"
  }
}
```

**视频URL有效期**: 约1小时，需尽快下载

**生成时间**: 通常30秒~3分钟（视音频长度）

---

## 常见错误码

| code | message | 解决方案 |
|------|---------|---------|
| 50207 | Image Decode Error | 图片格式不支持，换jpg/png格式 |
| 50430 | API Concurrent Limit | 等1-5分钟再试 |
| 403 | Access Denied | 权限不足，检查RAM用户授权 |
| 401 | InvalidAccessKey | AK/SK错误 |
