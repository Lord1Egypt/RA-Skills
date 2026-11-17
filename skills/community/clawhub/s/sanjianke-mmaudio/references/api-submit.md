# 提交任务 · submit

> a7w 插件 `mmaudio` 的接口 `submit` · 平台官方文档

---

`POST /api/v1/apps/mmaudio/submit`

## 提交弹性任务

`POST /api/v1/apps/mmaudio/submit`

音效生成、视频配音任务，提供视频 URL、可选 duration 视频时长和可选 prompt 音频生成提示词，平台将自动生成匹配的音频配音。可选提供参考音频 URL。

返回示例：`{ "task_id": 123, "status": "pending" }`（task_id 为弹性任务主键）

## 参数（平台 schema 原文）

```json
{
  "mode": {
    "type": "string",
    "default": "async_query",
    "required": false,
    "description": "任务模式，默认 async_query"
  },
  "prompt": {
    "type": "string",
    "example": "Generate natural cinematic sound effects and ambience for this video.",
    "required": false,
    "description": "音频生成提示词，用于描述期望的音效、环境声或配乐风格；未传时使用系统默认提示词"
  },
  "duration": {
    "type": "number",
    "example": 15.695,
    "required": false,
    "description": "输入视频时长，单位秒；未传时平台从 input_url 探测"
  },
  "audio_url": {
    "type": "string",
    "example": "https://example.com/reference_audio.wav",
    "required": false,
    "description": "可选的输入音频 URL，用于参考配音风格"
  },
  "input_url": {
    "type": "string",
    "example": "https://example.com/silent_video.mp4",
    "required": true,
    "description": "输入视频文件 URL"
  }
}
```

## 计费

- 结算口径：按次固定价 0.1 点（租户价）
- 标准价：`fixed_price=0.1000` / `input_price=0.000000`
- 租户价：`tenant_fixed_points=0.10` / `tenant_points_per_1k_input=0.0000`
