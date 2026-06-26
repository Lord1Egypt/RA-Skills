# 提示词反推 API

## 接口

```
POST /open/api/v1/resource/aigc/generation
```

---

## 图片反推提示词

上传一张图片，AI 反推出描述这张图片的提示词。可以把这个提示词用于「生成图片」，得到风格相似的作品。

### 请求示例

```json
{
  "type": "image_prompt_extraction",
  "url": "https://example.com/sample.jpg"
}
```

### 参数说明

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| type | string | 是 | 固定填 `image_prompt_extraction` |
| url | string | 是 | 参考图片 URL（必须是可公开访问的图片链接） |

### 轮询结果

```json
{
  "code": 200,
  "data": [{
    "opsId": 111222333,
    "status": "COMPLETED",
    "failReason": null,
    "content": [
      {
        "prompt": "一位穿着汉服的年轻女子，站在古建筑前，逆光拍摄，氛围感强，柔和的自然光线"
      }
    ]
  }]
}
```

从 `content` 中提取提示词文本（通常在 `prompt` 字段），可以直接用它做 prompt 生成图片。

---

## 视频反推脚本

上传一个视频，AI 分析视频内容，输出视频脚本（包含每个场景的画面描述、时间轴、旁白等）。

### 请求示例

```json
{
  "type": "video_script_extraction",
  "url": "https://example.com/sample.mp4"
}
```

### 参数说明

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| type | string | 是 | 固定填 `video_script_extraction` |
| url | string | 是 | 参考视频 URL（必须是可公开访问的视频链接，文件需大于 100MB） |

### 轮询结果

```json
{
  "code": 200,
  "data": [{
    "opsId": 444555666,
    "status": "COMPLETED",
    "failReason": null,
    "content": [
      {
        "segment": "场景1",
        "timeRange": "0-5秒",
        "description": "城市街景，车流穿梭",
        "narration": "在这个快节奏的城市里..."
      },
      {
        "segment": "场景2",
        "timeRange": "5-15秒",
        "description": "咖啡馆内景，暖色调",
        "narration": "偶尔也需要放慢脚步..."
      }
    ]
  }]
}
```

从 `content` 获取结构化脚本内容，每个元素包含 `segment`、`timeRange`、`description`、`narration` 等字段。

---

## 轮询方式

两种反推任务都使用相同的轮询接口：

```
POST /open/api/v1/resource/aigc/task/status
```

传入任务 ID 列表：

```json
[任务ID]
```
