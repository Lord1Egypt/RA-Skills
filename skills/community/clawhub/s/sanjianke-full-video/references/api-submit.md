# 提交任务 · submit

> a7w 插件 `full_video` 的接口 `submit` · 平台官方文档

---

`POST /api/v1/apps/full_video/submit`

## 提交任务

`POST /api/v1/apps/full_video/submit`

全能视频生成任务须传入一条文本内容。输出分辨率支持 480P、768P、1080P、2K 和 4K。首帧和尾帧各最多 1 张；参考图片最多 9 张，参考视频和参考音频各最多 3 个。首尾帧模式不能与参考媒体模式混用；参考媒体模式至少包含 1 张参考图片或 1 个参考视频，不能只传参考音频。时长仅支持 4 到 15 秒整数；768P、1080P、2K 的文本总长度最多 5000 个字符，其他分辨率最多 7000 个字符。

计费：按分辨率 SKU 和生成时长计量；默认前 5 张 reference_image 免费，超出部分每张加 20 点，实际规则以当前应用配置为准。

## 参数（平台 schema 原文）

```json
{
  "model": {
    "type": "string",
    "default": "full-video",
    "example": "full-video",
    "required": false,
    "description": "视频生成模型标识，固定为 full-video。"
  },
  "ratio": {
    "type": "string",
    "default": "16:9",
    "example": "16:9",
    "required": false,
    "description": "视频画幅比例；图生视频可使用 adaptive。"
  },
  "content": {
    "type": "array",
    "required": true,
    "description": "内容列表，须包含文本项；可按模式传入首帧、尾帧或参考媒体。"
  },
  "duration": {
    "type": "integer",
    "default": 4,
    "example": 4,
    "maximum": 15,
    "minimum": 4,
    "required": false,
    "description": "生成时长，单位秒，范围 4 到 15。"
  },
  "resolution": {
    "enum": [
      "480P",
      "768P",
      "1080P",
      "2K",
      "4K"
    ],
    "type": "string",
    "default": "480P",
    "example": "480P",
    "required": false,
    "description": "输出分辨率；不同分辨率对应独立的按秒 SKU，具体售价以当前租户价格配置为准。"
  },
  "aigc_watermark": {
    "type": "boolean",
    "default": false,
    "example": false,
    "required": false,
    "description": "是否添加生成标识。"
  }
}
```

## 计费

- 结算口径：免费
- 标准价：`fixed_price=0.0000` / `input_price=0.000000`
- 租户价：`tenant_fixed_points=0.00` / `tenant_points_per_1k_input=0.0000`
