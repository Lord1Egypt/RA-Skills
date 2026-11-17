# 提交任务 · submit

> a7w 插件 `image_human` 的接口 `submit` · 平台官方文档

---

`POST /api/v1/apps/image_human/submit`

## 提交任务

`POST /api/v1/apps/image_human/submit`

全驱动数字人任务，提供人物图片、驱动音频、可选用户提示词和生成模式。mode 支持 fast、standard、2k、4k；resolution 仅作为兼容别名；submit 按输入音频时长计费。

返回示例：`{ "task_id": 123, "status": "pending" }`

## 参数（平台 schema 原文）

```json
{
  "mode": {
    "enum": [
      "fast",
      "standard",
      "2k",
      "4k"
    ],
    "type": "string",
    "default": "standard",
    "required": false,
    "description": "生成模式/清晰度档位：fast 快速模式，standard 标准模式，2k 高清模式，4k 超清模式"
  },
  "prompt": {
    "type": "string",
    "default": "人物说话自然，面对镜头，肢体语言自然，人物清晰可鉴。",
    "example": "人物说话自然，面对镜头，肢体语言自然，人物清晰可鉴。",
    "required": false,
    "description": "用户提示词；未传时使用默认提示词"
  },
  "duration": {
    "type": "number",
    "required": false,
    "description": "输入音频时长，单位秒；未传时平台从 ref_file_url 探测"
  },
  "file_url": {
    "type": "string",
    "example": "https://example.com/person.png",
    "required": true,
    "description": "输入图片 URL"
  },
  "resolution": {
    "enum": [
      "2k",
      "4k"
    ],
    "type": "string",
    "required": false,
    "description": "兼容字段；传 2k 或 4k 时等同于 mode=2k 或 mode=4k。新接入建议直接使用 mode"
  },
  "ref_file_url": {
    "type": "string",
    "example": "https://example.com/audio.wav",
    "required": true,
    "description": "输入音频 URL，用于驱动数字人；平台按该音频时长计费"
  }
}
```

## 能力限制（平台字段原文）

| 字段 | 值 | 含义 |
|---|---|---|
| `max_reference_images` | **1** | 参考图**最多 1 张** |
| `max_reference_audios` | 0 | 不接受参考音频列表 |
| `max_reference_videos` | 0 | 不接受参考视频 |
| `default_params` | `{"mode": "standard"}` | 不传 `mode` 时按 `standard` 计费 |
| `call_type` | 2 | 异步：返回 `task_id`，需轮询 |

## 计费

**这个接口按输入音频的时长计费，单价随 `mode` 档位变化。**

平台给出的 `pricing_matrix`（点/秒，1 元 = 100 点）：

```json
{
  "fast":     { "with_video": 1.5, "without_video": 1.5 },
  "standard": { "with_video": 2,   "without_video": 2   },
  "2k":       { "with_video": 4,   "without_video": 4   },
  "4k":       { "with_video": 8,   "without_video": 8   }
}
```

| `mode` | 点/秒 | 元/秒 | 60 秒 | 120 秒 |
|---|---|---|---|---|
| `fast` | 1.5 | 0.015 | 90 点 / 0.90 元 | 180 点 / 1.80 元 |
| `standard` | 2 | 0.02 | 120 点 / 1.20 元 | 240 点 / 2.40 元 |
| `2k` | 4 | 0.04 | 240 点 / 2.40 元 | 480 点 / 4.80 元 |
| `4k` | 8 | 0.08 | 480 点 / 4.80 元 | 960 点 / 9.60 元 |

**计算公式**：`费用（点） = 音频时长（秒） × 该档单价`

其它价格字段（原样保留，供对账）：

- 标准价：`fixed_price=0.0000` / `input_price=2.000000`
- 租户价：`tenant_fixed_points=0.00` / `tenant_points_per_1k_input=2.0000`
- `billing_type = 5`

> `input_price = 2.0` 是**基础参考价**（对应 `standard` 档）。
> 实际扣费取 `pricing_matrix` 里对应档位的值；平台还有智能路由
> （`smart_route`，取值 `on` / `auto` / `off`），主线路故障时会降级到其它线路，
> **最终按实际成功线路的计费规则结算**，所以以账号实际扣费为准。

