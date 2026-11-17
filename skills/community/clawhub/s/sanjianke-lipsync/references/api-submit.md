# 提交任务 · submit

> a7w 插件 `lipsync` 的接口 `submit` · 平台官方文档

---

`POST /api/v1/apps/lipsync/submit`

## 提交任务

`POST /api/v1/apps/lipsync/submit`

数字人对口型任务，提供数字人视频 URL、驱动音频 URL 和可选的数字人模型标识。xiaojiayu1.0 须配置弹性部署策略；xiaojiayu2.0/3.0 会先自动创建数字人，创建完成后提交视频生成任务。

返回示例：`{ "task_id": 123, "status": "pending" }`

## 参数（平台 schema 原文）

```json
{
  "fps": {
    "type": "string",
    "required": false,
    "description": "可选帧率参数。"
  },
  "mode": {
    "type": "string",
    "default": "async_query",
    "required": false,
    "description": "任务模式，默认 async_query"
  },
  "model": {
    "type": "string",
    "default": "xiaojiayu1.0",
    "required": false,
    "description": "数字人模型标识，支持 xiaojiayu1.0、xiaojiayu2.0、xiaojiayu3.0；亦可使用简写 1.0、2.0、3.0。xiaojiayu1.0 需配置弹性部署策略；2.0 和 3.0 会自动创建数字人后生成视频。"
  },
  "audio_url": {
    "type": "string",
    "example": "https://example.com/speech.wav",
    "required": true,
    "description": "输入音频文件 URL（驱动口型的语音）"
  },
  "video_url": {
    "type": "string",
    "example": "https://example.com/avatar_video.mp4",
    "required": true,
    "description": "输入视频文件 URL（数字人原始视频）"
  },
  "video_params": {
    "type": "object",
    "required": false,
    "description": "视频生成可选参数对象。"
  }
}
```

## 计费

- 结算口径：以站内计费为准
- 标准价：`fixed_price=0.1000` / `input_price=0.000000`
- 租户价：`tenant_fixed_points=0.00` / `tenant_points_per_1k_input=0.0000`
