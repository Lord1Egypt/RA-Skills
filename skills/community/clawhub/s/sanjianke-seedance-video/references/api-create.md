# 创建任务 · create

> a7w 插件 `seedance` 的接口 `create` · 平台官方文档

---

`POST /api/v1/apps/seedance/create`

## Seedance 2.0 创建任务

`POST /api/v1/apps/seedance/create`

异步任务：提交后返回 `task_id`，可通过 `GET /api/v1/tasks/{task_id}` 或 `GET /api/v1/tasks/{task_id}` 查询进度与结果。

### 模型名称与使用场景

请求体中的 `model` 只能使用下表的公开模型名称。模型类型、名称和适用场景一一对应：

| 模型类型 | 模型名称 | 描述 |
|---|---|---|
| Seedance 2.0 标准版 | `seedance-2-text-2-video` | 输入内容不包含视频，适合文生视频、图生视频、首尾帧生成 |
| Seedance 2.0 标准版 | `seedance-2-video-2-video` | 输入内容包含视频，适合视频编辑、视频延长、视频参考 |
| Seedance 2.0 快速版 | `seedance-2-fast-text-2-video` | 输入内容不包含视频，优先生成速度 |
| Seedance 2.0 快速版 | `seedance-2-fast-video-2-video` | 输入内容包含视频，优先生成速度 |

除上述 4 个公开模型名称外，不需要填写其他模型名称。

### 计费

按输出 `total_tokens` 与定价矩阵结算。实际扣点 = 输出 `total_tokens` ÷ 1,000,000 × 当前档位点数单价（点数/百万 tokens）。
不同分辨率 × 是否含视频输入 单价不同；创建任务时预扣可为 0，完成后按矩阵扣点。

## 参数（平台 schema 原文）

```json
{
  "seed": {
    "type": "integer",
    "description": "随机种子，可复现结果（若上游支持）"
  },
  "draft": {
    "type": "boolean",
    "description": "是否草稿模式（若上游支持）"
  },
  "model": {
    "type": "string",
    "example": "seedance-2-text-2-video",
    "options": "seedance-2-text-2-video / seedance-2-video-2-video / seedance-2-fast-text-2-video / seedance-2-fast-video-2-video",
    "description": "公开模型名称。请从模型名称与使用场景表中选择一个名称。"
  },
  "ratio": {
    "type": "string",
    "default": "adaptive",
    "example": "16:9",
    "options": "16:9 / 4:3 / 1:1 / 3:4 / 9:16 / 21:9 / adaptive",
    "description": "画面宽高比。adaptive 表示由模型根据输入自动选择"
  },
  "tools": {
    "type": "array",
    "example": [
      {
        "type": "web_search"
      }
    ],
    "description": "可选工具（仅文生视频支持 web_search 联网搜索）"
  },
  "frames": {
    "type": "integer",
    "description": "帧数相关参数（若上游支持）"
  },
  "content": {
    "type": "array",
    "example": [
      {
        "text": "一只金毛犬在海边奔跑，夕阳西下",
        "type": "text"
      }
    ],
    "children": {
      "role": {
        "type": "string",
        "description": "条件必填。图片首尾帧：first_frame / last_frame；参考图：reference_image；参考视频：reference_video；参考音频：reference_audio"
      },
      "text": {
        "type": "string",
        "description": "文本提示词（type=text 时必填）"
      },
      "type": {
        "type": "string",
        "options": "text / image_url / video_url / audio_url",
        "required": "1",
        "description": "内容类型"
      },
      "audio_url": {
        "type": "object",
        "description": "音频对象，格式 {\"url\": \"音频地址\"}"
      },
      "image_url": {
        "type": "object",
        "description": "图片对象，格式 {\"url\": \"图片地址\"}"
      },
      "video_url": {
        "type": "object",
        "description": "视频对象，格式 {\"url\": \"视频地址\"}"
      }
    },
    "examples": {
      "文生视频": [
        {
          "text": "一只金毛犬在海边奔跑",
          "type": "text"
        }
      ],
      "图生视频-首帧": [
        {
          "role": "first_frame",
          "type": "image_url",
          "image_url": {
            "url": "https://example.com/pic1.jpg"
          }
        },
        {
          "text": "让画面动起来",
          "type": "text"
        }
      ],
      "图生视频-首尾帧": [
        {
          "role": "first_frame",
          "type": "image_url",
          "image_url": {
            "url": "首帧图片地址"
          }
        },
        {
          "role": "last_frame",
          "type": "image_url",
          "image_url": {
            "url": "尾帧图片地址"
          }
        },
        {
          "text": "平滑过渡",
          "type": "text"
        }
      ],
      "多模态参考生视频": [
        {
          "role": "reference_image",
          "type": "image_url",
          "image_url": {
            "url": "参考图1"
          }
        },
        {
          "role": "reference_video",
          "type": "video_url",
          "video_url": {
            "url": "参考视频1"
          }
        },
        {
          "role": "reference_audio",
          "type": "audio_url",
          "audio_url": {
            "url": "参考音频1"
          }
        },
        {
          "text": "场景描述",
          "type": "text"
        }
      ]
    },
    "description": "多模态输入列表：支持 文本 + 图片 + 视频 + 音频 的任意组合。图片最多 9 张、视频最多 3 个、音频最多 3 段，且不可单独传音频。含 video_url 时按「含视频输入」档位计费。"
  },
  "duration": {
    "type": "integer",
    "default": "5",
    "example": "5",
    "description": "生成视频时长（秒）。取值 4~15，或 -1 由模型自动决定"
  },
  "watermark": {
    "type": "boolean",
    "default": "",
    "example": "",
    "description": "是否在视频右下角添加水印"
  },
  "resolution": {
    "type": "string",
    "default": "720p",
    "example": "720p",
    "options": "480p / 720p / 1080p",
    "description": "输出分辨率"
  },
  "callback_url": {
    "type": "string",
    "example": "https://your-domain.com/webhook/seedance",
    "description": "异步任务完成/失败时的回调地址"
  },
  "camera_fixed": {
    "type": "boolean",
    "description": "是否固定机位（若上游支持）"
  },
  "service_tier": {
    "type": "string",
    "description": "服务档位（若上游支持）"
  },
  "generate_audio": {
    "type": "boolean",
    "default": "1",
    "example": "1",
    "description": "是否生成与画面同步的音频"
  }
}
```

## 计费

- 结算口径：免费
- 标准价：`fixed_price=0.0000` / `input_price=0.000000`
- 租户价：`tenant_fixed_points=0.00` / `tenant_points_per_1k_input=0.0000`
- 分档：`480p`=3000/5000，`720p`=3200/5500，`1080p`=3500/6000
