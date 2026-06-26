# 字幕识别与字幕位置计算

通过火山OCR识别视频画面中的文字，确定字幕出现位置。

## 整体流程

```
视频 → 抽帧 → 上传到 OSS → 火山OCR识别 → 字幕位置精确计算
```

## 接口一：字幕识别（火山OCR）

### 提交OCR识别

```
POST /api/aipkg/submit/volcano.ocr
```

### 查询OCR识别结果

```
POST /api/aipkg/query/volcano.ocr.result
```

### 请求参数（提交）

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `task_id` | int | ✅ | server_task_id |
| `data_type` | string | ✅ | 固定 `url`（图片地址模式） |
| `scene` | string | ✅ | 固定 `general` |
| `data_list` | array | ✅ | 图片URL列表 |

### 图片获取流程

```
视频 → ffprobe获取(时长/宽高) → ffmpeg均匀抽帧(n张) → 上传到OSS → 获得公网URL
```

**上传接口**（明文，不走加密通道）：
```
POST {upload_base_url}/bk.srv/upload
Content-Type: multipart/form-data
Form-data: files=图片文件, usage=seven_day_temp_img
```
> `upload_base_url` 由服务端提供（与主 API `https://biyi.cxtfun.com` 同域或为独立 CDN）。

**上传响应**（从 `data[0].url` 取公网可访问URL）：
```json
{
  "err_code": -1,
  "data": {
    "list": [
      {"url": "https://cdn.example.com/frame_0001.jpg"}
    ]
  }
}
```

### 异步轮询

- **client_id**：从提交响应 `data.client_id` 获取（注意不是 task_id）
- **轮询接口**：POST `/api/aipkg/query/volcano.ocr.result`，body `{"client_id": "xxx"}`
- **建议超时**：300秒
- **轮询间隔**：5秒

### OCR查询响应（state=2 成功）

```json
{
  "err_code": -1,
  "state": 2,
  "data": {
    "state": 2,
    "results": [
      {
        "frame_num": 0,
        "general_result": [
          {
            "content": "字幕文字1",
            "confidence": 0.95,
            "location": [[x1,y1], [x2,y1], [x2,y2], [x1,y2]]
          }
        ]
      }
    ]
  }
}
```

### OCR结果解析

```python
def parse_ocr_boxes(results):
    boxes = []
    for frame_num, item in enumerate(results):
        for text_info in item.get("general_result", []):
            content = text_info.get("content", "").strip()
            conf = float(text_info.get("confidence", 0))
            loc = text_info.get("location", [])
            if content and conf >= 0.5 and len(loc) >= 4:
                x1, y1 = loc[0]
                x2, y2 = loc[2]
                boxes.append({
                    "frame_num": frame_num,
                    "text": content,
                    "x1": x1, "y1": y1, "x2": x2, "y2": y2,
                    "cy": (y1+y2)//2,
                    "conf": conf
                })
    return boxes
```

---

## 接口二：字幕位置精确计算

基于 OCR 识别结果，用聚类算法精确计算字幕区域。

### 接口

```
POST /api/aipkg/calc/subtitle.pos.by.ocr
```

### 请求参数

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `results` | array | ✅ | OCR 轮询结果的 `results` 数组 |
| `video_width` | int | ✅ | 视频宽度（像素） |
| `video_height` | int | ✅ | 视频高度（像素） |

### 响应

```json
{
  "err_code": -1,
  "data": {
    "x": 100,
    "y": 900,
    "w": 760,
    "h": 80
  }
}
```

返回字段：`x`, `y` 为左上角坐标，`w`, `h` 为宽高（像素）。

## 字幕位置本地粗估（无服务端时）

如果精确计算接口不可用，可用本地粗估：

```python
def rough_subtitle_bbox(boxes, video_width, video_height):
    # 取画面下半区（center_y >= 45%）的高置信度框
    threshold_y = video_height * 0.45
    bottom = [b for b in boxes if b["cy"] >= threshold_y]
    use = bottom if len(bottom) >= 2 else boxes
    x1 = min(b["x1"] for b in use)
    y1 = min(b["y1"] for b in use)
    x2 = max(b["x2"] for b in use)
    y2 = max(b["y2"] for b in use)
    return {
        "x": max(0, min(x1, video_width-1)),
        "y": max(0, min(y1, video_height-1)),
        "w": max(1, x2 - x1),
        "h": max(1, y2 - y1)
    }
```

## 注意事项

- **必须先完成 OCR 识别，再计算字幕位置**（两步骤顺序不能颠倒）
- 图片**必须是公网可访问的 URL**，火山侧能拉取
- 抽帧建议数量：**15帧**，覆盖整个视频时长
- 字幕区域计算需要**视频宽高**，用于坐标归一化
- `usage=seven_day_temp_img` 确保图片有7天有效期
