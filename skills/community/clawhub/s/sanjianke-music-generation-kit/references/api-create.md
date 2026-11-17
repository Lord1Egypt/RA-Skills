# 创建音乐任务 · create

> a7w 插件 `music_generation` 的接口 `create` · 平台官方文档

---

`POST /api/v1/apps/music_generation/create`

# 音乐生成 · 创建音乐任务

提交音乐生成、续写、翻唱、分轨或混音任务，返回平台任务 ID。

## 基本信息

| 字段 | 内容 |
| --- | --- |
| 应用编码 | `music_generation` |
| API 编码 | `create` |
| 请求方式 | `POST` |
| 请求路径 | `/api/v1/apps/music_generation/create` |
| 调用模式 | 异步 |
| 计费方式 | 按 `type` 对应固定规格计费 |

## 鉴权

```http
Authorization: Bearer <YOUR_API_KEY>
Content-Type: application/json
```

## type 价格对照

请求 `create` 接口时，`type` 字段决定具体创作动作和计费规格。

| type 参数值 | 规格说明 | 价格 |
| --- | --- | --- |
| `generate` | 生成音乐 | 65 点/次 |
| `extend` | 续写音乐 | 65 点/次 |
| `upload_extend` | 上传音频续写 | 65 点/次 |
| `upload_cover` | 上传音频翻唱 | 65 点/次 |
| `concat` | 拼接音频 | 14 点/次 |
| `cover` | 风格翻唱 | 65 点/次 |
| `artist_consistency` | 歌手风格生成 | 65 点/次 |
| `artist_consistency_vox` | 歌手风格人声生成 | 65 点/次 |
| `stems` | 基础分轨 | 65 点/次 |
| `all_stems` | 完整分轨 | 230 点/次 |
| `replace_section` | 替换片段 | 90 点/次 |
| `underpainting` | 添加伴奏 | 65 点/次 |
| `overpainting` | 添加人声 | 65 点/次 |
| `remaster` | 音质增强 | 65 点/次 |
| `mashup` | 混音融合 | 65 点/次 |
| `samples` | 添加采样 | 65 点/次 |
| `inspo` | 参考灵感生成 | 65 点/次 |

## 业务参数

| 参数 | 类型 | 必填 | 默认值 | 可选值 / 范围 | 示例 | 说明 |
| --- | --- | --- | --- | --- | --- | --- |
| `type` | string | 否 | `generate` | `generate` / `extend` / `upload_extend` / `upload_cover` / `concat` / `cover` / `artist_consistency` / `artist_consistency_vox` / `stems` / `all_stems` / `replace_section` / `underpainting` / `overpainting` / `remaster` / `mashup` / `samples` / `inspo` | `generate` | 操作类型。generate 根据提示生成音乐；extend 基于已有音频续写；concat 拼接音频片段；cover 参考既有曲风重新演绎；upload_cover 对上传音频进行风格翻唱；upload_extend 续写上传音频；artist_consistency 按指定歌手风格生成；artist_consistency_vox 使用人声模式按歌手风格生成；stems 分离人声和伴奏；all_stems 分离人声、鼓、贝斯和其他乐器；replace_section 替换指定时间段；underpainting 为人声添加伴奏；overpainting 为伴奏添加人声；samples 在指定时间段添加采样；remaster 增强音质；mashup 混合多首歌曲；inspo 基于 1 到 4 段参考音频生成灵感作品。 |
| `prompt` | string | 否 | - | - | `A warm synth-pop song about city nights` | 生成音乐的提示词。灵感模式下不超过 500 个字符；自定义歌词模式请优先使用 lyric 和 style。 |
| `lyric` | string | 否 | - | - | - | 自定义模式下使用的歌词。常规模型最多 3000 字符，高质量模型最多 5000 字符。 |
| `style` | string | 否 | - | - | `dream pop, warm synth, mellow vocal` | 音乐风格描述。常规模型最多 200 字符，高质量模型最多 1000 字符。 |
| `title` | string | 否 | - | - | `Neon Night` | 自定义模式下的歌曲标题。常规模型最多 80 字符，高质量模型最多 100 字符。 |
| `custom` | boolean | 否 | - | - | - | 是否启用自定义模式。请使用 JSON boolean；平台也兼容 true/false、1/0、yes/no、on/off 字符串。为 true 时按歌词和风格生成；为 false 时按提示词生成。 |
| `instrumental` | boolean | 否 | - | - | - | 纯伴奏模式。请使用 JSON boolean；平台也兼容 true/false、1/0、yes/no、on/off 字符串。开启后将忽略歌词内容。 |
| `lyric_prompt` | string | 否 | - | - | - | 自动生成歌词的提示词，仅在 custom 为 true 且 lyric 为空时生效。 |
| `audio_id` | string | 否 | - | - | - | 已有音频 ID。extend、concat 等基于已有音频的操作需要填写。 |
| `audio_urls` | array | 否 | - | - | `["https:\/\/example.com\/ref.mp3"]` | 参考音频 URL 列表。inspo 类型要求 1 到 4 个可公开访问的音频地址。 |
| `persona_id` | string | 否 | - | - | - | 歌手或声音风格 ID，用于让生成歌曲采用指定风格。 |
| `continue_at` | number | 否 | - | - | - | 从已有音频的指定秒数位置继续生成。例如 213.5 表示从 3 分 33.5 秒处续写。 |
| `vocal_gender` | string | 否 | - | `m` / `f` | - | 人声性别偏好，m 表示男声，f 表示女声。该参数用于提高目标音色概率，但不保证严格符合。 |
| `style_negative` | string | 否 | - | - | - | 不希望出现在音乐中的风格描述。 |
| `style_influence` | number | 否 | - | - | - | 风格影响强度，范围 0 到 1；数值越高越贴近填写的风格，仅在自定义模式下生效。 |
| `weirdness` | number | 否 | - | - | - | 创意实验强度，范围 0 到 1；数值越高结果越开放，仅在自定义模式下生效。 |
| `audio_weight` | number | 否 | - | - | - | 参考音频权重，范围 0 到 1；数值越高越依赖参考音频，主要用于翻唱类操作。 |
| `variation_category` | string | 否 | - | `high` / `normal` / `subtle` | - | 变化强度，可选 high、normal、subtle。 |
| `mashup_audio_ids` | array | 否 | - | - | - | 用于混合的音频 ID 列表。mashup 类型需要填写。 |
| `replace_section_start` | number | 否 | - | - | - | replace_section 类型中需要替换片段的开始时间，单位秒。 |
| `replace_section_end` | number | 否 | - | - | - | replace_section 类型中需要替换片段的结束时间，单位秒。 |
| `underpainting_start` | number | 否 | - | - | - | 添加伴奏的开始时间，单位秒，默认 0。 |
| `underpainting_end` | number | 否 | - | - | - | 添加伴奏的结束时间，单位秒，需小于歌曲总时长。 |
| `overpainting_start` | number | 否 | - | - | - | 添加人声的开始时间，单位秒，默认 0。 |
| `overpainting_end` | number | 否 | - | - | - | 添加人声的结束时间，单位秒，需小于歌曲总时长。 |
| `samples_start` | number | 否 | - | - | - | 添加采样的开始时间，单位秒，默认 0。 |
| `samples_end` | number | 否 | - | - | - | 添加采样的结束时间，单位秒，需小于歌曲总时长。 |
| `callback_url` | string | 否 | - | - | - | 任务完成或失败时由平台主动通知的 HTTPS 地址。 |

## 响应说明

提交成功后返回平台 `task_id`。请使用本应用查询接口或统一任务查询接口获取最终结果；如果请求传入 `callback_url`，平台会在任务终态时主动通知。

### 提交成功示例

```json
{
    "code": 1,
    "msg": "success",
    "data": {
        "task_id": "task_xxxxxxxxxxxx",
        "status": "processing",
        "app": "music_generation",
        "api": "create",
        "frozen_points": 65,
        "actual_points": 0,
        "created_at": "2026-07-06T14:32:35Z"
    }
}
```

### 查询完成示例

```json
{
    "code": 1,
    "msg": "success",
    "data": {
        "result": {
            "task_id": "task_xxxxxxxxxxxx",
            "status": "completed",
            "audio_url": "https://example.com/music/audio.mp3",
            "title": "Morning API",
            "data": [
                {
                    "id": "audio_xxxxxxxxxxxx",
                    "title": "Morning API",
                    "lyric": "[Verse]\nClean lines, clean run",
                    "style": "bright synth pop",
                    "duration": 20.5,
                    "audio_url": "https://example.com/music/audio.mp3"
                }
            ]
        },
        "usage": {
            "points_cost": 65,
            "actual_points": 65
        }
    }
}
```

### 失败示例

```json
{
    "code": 0,
    "msg": "任务处理失败，请稍后重试",
    "data": null
}
```

## 参数（平台 schema 原文）

```json
{
  "type": {
    "enum": [
      "generate",
      "extend",
      "upload_extend",
      "upload_cover",
      "concat",
      "cover",
      "artist_consistency",
      "artist_consistency_vox",
      "stems",
      "all_stems",
      "replace_section",
      "underpainting",
      "overpainting",
      "remaster",
      "mashup",
      "samples",
      "inspo"
    ],
    "type": "string",
    "default": "generate",
    "example": "generate",
    "options": "generate / extend / upload_extend / upload_cover / concat / cover / artist_consistency / artist_consistency_vox / stems / all_stems / replace_section / underpainting / overpainting / remaster / mashup / samples / inspo",
    "description": "操作类型。generate 根据提示生成音乐；extend 基于已有音频续写；concat 拼接音频片段；cover 参考既有曲风重新演绎；upload_cover 对上传音频进行风格翻唱；upload_extend 续写上传音频；artist_consistency 按指定歌手风格生成；artist_consistency_vox 使用人声模式按歌手风格生成；stems 分离人声和伴奏；all_stems 分离人声、鼓、贝斯和其他乐器；replace_section 替换指定时间段；underpainting 为人声添加伴奏；overpainting 为伴奏添加人声；samples 在指定时间段添加采样；remaster 增强音质；mashup 混合多首歌曲；inspo 基于 1 到 4 段参考音频生成灵感作品。"
  },
  "lyric": {
    "type": "string",
    "description": "自定义模式下使用的歌词。常规模型最多 3000 字符，高质量模型最多 5000 字符。"
  },
  "style": {
    "type": "string",
    "example": "dream pop, warm synth, mellow vocal",
    "description": "音乐风格描述。常规模型最多 200 字符，高质量模型最多 1000 字符。"
  },
  "title": {
    "type": "string",
    "example": "Neon Night",
    "description": "自定义模式下的歌曲标题。常规模型最多 80 字符，高质量模型最多 100 字符。"
  },
  "custom": {
    "type": "boolean",
    "description": "是否启用自定义模式。请使用 JSON boolean；平台也兼容 true/false、1/0、yes/no、on/off 字符串。为 true 时按歌词和风格生成；为 false 时按提示词生成。"
  },
  "prompt": {
    "type": "string",
    "example": "A warm synth-pop song about city nights",
    "description": "生成音乐的提示词。灵感模式下不超过 500 个字符；自定义歌词模式请优先使用 lyric 和 style。"
  },
  "audio_id": {
    "type": "string",
    "description": "已有音频 ID。extend、concat 等基于已有音频的操作需要填写。"
  },
  "weirdness": {
    "type": "number",
    "maximum": 1,
    "minimum": 0,
    "description": "创意实验强度，范围 0 到 1；数值越高结果越开放，仅在自定义模式下生效。"
  },
  "audio_urls": {
    "type": "array",
    "items": {
      "type": "string"
    },
    "example": [
      "https://example.com/ref.mp3"
    ],
    "description": "参考音频 URL 列表。inspo 类型要求 1 到 4 个可公开访问的音频地址。"
  },
  "persona_id": {
    "type": "string",
    "description": "歌手或声音风格 ID，用于让生成歌曲采用指定风格。"
  },
  "continue_at": {
    "type": "number",
    "description": "从已有音频的指定秒数位置继续生成。例如 213.5 表示从 3 分 33.5 秒处续写。"
  },
  "samples_end": {
    "type": "number",
    "description": "添加采样的结束时间，单位秒，需小于歌曲总时长。"
  },
  "audio_weight": {
    "type": "number",
    "maximum": 1,
    "minimum": 0,
    "description": "参考音频权重，范围 0 到 1；数值越高越依赖参考音频，主要用于翻唱类操作。"
  },
  "callback_url": {
    "type": "string",
    "description": "任务完成或失败时由平台主动通知的 HTTPS 地址。"
  },
  "instrumental": {
    "type": "boolean",
    "description": "纯伴奏模式。请使用 JSON boolean；平台也兼容 true/false、1/0、yes/no、on/off 字符串。开启后将忽略歌词内容。"
  },
  "lyric_prompt": {
    "type": "string",
    "description": "自动生成歌词的提示词，仅在 custom 为 true 且 lyric 为空时生效。"
  },
  "vocal_gender": {
    "enum": [
      "m",
      "f"
    ],
    "type": "string",
    "options": "m / f",
    "description": "人声性别偏好，m 表示男声，f 表示女声。该参数用于提高目标音色概率，但不保证严格符合。"
  },
  "samples_start": {
    "type": "number",
    "description": "添加采样的开始时间，单位秒，默认 0。"
  },
  "style_negative": {
    "type": "string",
    "description": "不希望出现在音乐中的风格描述。"
  },
  "style_influence": {
    "type": "number",
    "maximum": 1,
    "minimum": 0,
    "description": "风格影响强度，范围 0 到 1；数值越高越贴近填写的风格，仅在自定义模式下生效。"
  },
  "mashup_audio_ids": {
    "type": "array",
    "items": {
      "type": "string"
    },
    "description": "用于混合的音频 ID 列表。mashup 类型需要填写。"
  },
  "overpainting_end": {
    "type": "number",
    "description": "添加人声的结束时间，单位秒，需小于歌曲总时长。"
  },
  "underpainting_end": {
    "type": "number",
    "description": "添加伴奏的结束时间，单位秒，需小于歌曲总时长。"
  },
  "overpainting_start": {
    "type": "number",
    "description": "添加人声的开始时间，单位秒，默认 0。"
  },
  "variation_category": {
    "enum": [
      "high",
      "normal",
      "subtle"
    ],
    "type": "string",
    "options": "high / normal / subtle",
    "description": "变化强度，可选 high、normal、subtle。"
  },
  "replace_section_end": {
    "type": "number",
    "description": "replace_section 类型中需要替换片段的结束时间，单位秒。"
  },
  "underpainting_start": {
    "type": "number",
    "description": "添加伴奏的开始时间，单位秒，默认 0。"
  },
  "replace_section_start": {
    "type": "number",
    "description": "replace_section 类型中需要替换片段的开始时间，单位秒。"
  }
}
```

## 计费

- 结算口径：按次固定价 65 点（租户价）
- 标准价：`fixed_price=65.0000` / `input_price=0.000000`
- 租户价：`tenant_fixed_points=65.00` / `tenant_points_per_1k_input=0.0000`
