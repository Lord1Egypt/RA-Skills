# 新闻体视频 · news_mixcut

> a7w 插件 `smart_clip` 的接口 `news_mixcut` · 平台官方文档

---

`POST /api/v1/apps/smart_clip/news_mixcut`

# 智能剪辑 · 新闻体视频

提交新闻体视频任务。如未传 `processRules.videoDuration`，平台会探测素材媒体时长用于计费；无法获取有效输入媒体时长时会拒绝提交。

## 基本信息

| 字段 | 内容 |
| --- | --- |
| 应用编码 | `smart_clip` |
| API 编码 | `news_mixcut` |
| 请求方式 | `POST` |
| 请求路径 | `/api/v1/apps/smart_clip/news_mixcut` |
| 调用模式 | 异步 |
| 计费方式 | 按输入媒体时长计费 |

## 请求参数

| 参数 | 类型 | 必填 | 默认值 | 可选值 / 范围 | 说明 |
| --- | --- | --- | --- | --- | --- |
| `styleId` | string | 是 | - | - | 视频模板ID |
| `title` | string | 是 | - | 3-1800字符 | 标题 |
| `materials` | array | 是 | - | image / video | 素材，每项包含 type、fileUrl、soundSwitch；平台会探测素材媒体时长用于计费 |
| `introduceCard` | object | 否 | - | - | 身份栏信息，包含 name、description |
| `packRules` | object | 否 | - | - | 包装规则：仅用于控制标题、素材、字幕、关键词、背景音乐等是否参与模板效果包装 |
| `processRules.watermarkShow` | boolean | 否 | false | true / false | 是否添加“AI生成”字样水印 |
| `processRules.videoDuration` | integer | 否 | - | 5-300 | 视频时长，单位秒，默认跟随素材资源时长 |
| `processRules.metadata` | object | 否 | - | - | 元水印数据，仅支持写入一组数据，且value值需为字符串 |
| `processRules.materialComposition` | string | 否 | random | random / order | 素材组合方式 |
| `processRules.firstFrameCover` | object | 否 | - | - | 首帧封面配置 |
| `structLayers` | array | 否 | - | - | 需要修改的图层数据 |
| `callbackUrl` | string | 否 | - | HTTPS URL | 结果通知回调地址，由平台在任务完成或失败后通知 |

### processRules

| 字段 | 类型 | 必填 | 默认值 | 可选值 / 范围 | 说明 |
| --- | --- | --- | --- | --- | --- |
| `watermarkShow` | boolean | 否 | `false` | true / false | 是否添加“AI生成”字样水印 |
| `videoDuration` | integer | 否 | 跟随素材资源时长 | `5-300` | 视频时长，单位：秒 |
| `metadata` | object | 否 | - | - | 元水印数据，仅支持写入一组数据，且 value 值需为字符串 |
| `materialComposition` | string | 否 | `random` | `random` / `order` | 素材组合方式，random 随机，order 顺序 |
| `firstFrameCover` | object | 否 | - | - | 首帧封面配置 |

## 重要规则

- 素材 `materials[].fileUrl`、背景音乐 `packRules.backgroundMusic.audioUrl`、AI 封面的 `resultImageUrl` 地址不能重名，重名会导致渲染异常。
- `packRules` 仅用于控制标题、字幕、素材、背景音乐、关键词等图层是否参与效果包装，不能控制对应图层的显示/隐藏。
- 如果期望生成的视频不显示标题，请不要设置标题值。
- `callbackUrl` 作为平台任务通知地址保存，任务完成或失败后由平台发起通知。
- 如无法解析有效输入媒体时长，本次请求会被拒绝，不使用默认时长。

## 通用对象字段

### subtitle[]

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `startMs` | integer | 是 | 时间戳开始，单位 ms |
| `endMs` | integer | 是 | 时间戳结束，单位 ms，最大支持 310000ms |
| `text` | string | 是 | 文本，只支持单字符级别 |

### materials[]

| 字段 | 类型 | 必填 | 可选值 / 默认值 | 说明 |
| --- | --- | --- | --- | --- |
| `type` | string | 是 | `image` / `video` | 素材类型 |
| `fileUrl` | string | 是 | - | 素材url |
| `soundSwitch` | boolean | 否 | `false` | 当素材为视频时原声开关，素材混剪和新闻体视频支持 |

### introduceCard

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `name` | string | 否 | 名称 |
| `description` | string | 否 | 描述 |

### packRules

| 字段 | 类型 | 必填 | 默认值 | 说明 |
| --- | --- | --- | --- | --- |
| `headerSwitch` | boolean | 否 | - | 标题包装开关 |
| `materialSwitch` | boolean | 否 | - | 素材包装开关 |
| `subtitleSwitch` | boolean | 否 | - | 字幕包装开关 |
| `keywordSwitch` | boolean | 否 | - | 关键词包装开关 |
| `backgroundMusic` | object | 否 | - | 背景音乐设置 |
| `backgroundMusic.audioSwitch` | boolean | 否 | - | 音乐开关 |
| `backgroundMusic.audioUrl` | string | 否 | - | 音频url，模板内置背景音乐和传递audioUrl，优先使用audioUrl |
| `backgroundMusic.volume` | number | 否 | `0.3` | 音量，保留一位小数，范围 0-1 |

### processRules.firstFrameCover

| 字段 | 类型 | 必填 | 默认值 | 说明 |
| --- | --- | --- | --- | --- |
| `coverSwitch` | boolean | 否 | `false` | 封面开关 |
| `templateId` | string | 否 | - | 模版ID，如果未设置则系统匹配 |
| `imageUrl` | string | 否 | - | 图片地址，用于生成AI封面图的底图，`imageUrl` 和 `resultImageUrl` 二选一必填 |
| `resultImageUrl` | string | 否 | - | 图片生成接口的结果图片地址或其他封面图片地址；传了此值将直接运用作为视频首桢封面，优先级更高 |

### structLayers[]

| 字段 | 类型 | 必填 | 可选值 | 说明 |
| --- | --- | --- | --- | --- |
| `markCode` | string | 是 | `headerLayer` / `subtitleLayer` / `ipLayer` / `backgroundLayer` / `figureLayer` | 图层，对应模板详情接口返回的图层数据 |
| `show` | boolean | 否 | - | 是否显示，不设置时默认跟随模板；`backgroundLayer`、`figureLayer` 不支持设置，默认显示 |
| `showMode` | string | 否 | `always` / `customize` | 显示模式，`markCode=headerLayer` 时生效，不设置时默认跟随模板 |
| `showTime` | number | 条件必填 | 大于 0 | 显示时长，`markCode=headerLayer` 且 `showMode=customize` 时生效且必填，保留 3 位小数 |
| `layer.transform.position` | integer[] | 否 | - | 锚点定位，对应模板详情 `transform.position` |
| `layer.uri` | string | 否 | - | 背景图片资源链接，仅 `backgroundLayer` 生效 |

## 素材与媒体要求

- 输入视频格式：mp4、mov；视频编码 h264、HEVC(h265)；帧率 10-60fps，推荐 25；单边分辨率小于 2000px。
- 真人口播 `videoUrl` 时长小于 5 分钟，文件大小小于 500MB，视频中的音频需要能够语音转文本。
- 素材总量限制：单张图片计算为 2 秒，单个视频素材不能超过 60 秒，所有素材总时长不能超过 5 分钟。
- 素材图片格式支持 jpg、png、webp 静态图，单边分辨率小于 2000px。
- 素材视频格式支持 mp4、mov，单个视频小于 500MB，单边分辨率小于 2000px。
- 背景音乐格式支持 mp3、wav、m4a，文件大小不超过 120MB，时长不超过 5 分钟。
- 首帧封面 `imageUrl`、`resultImageUrl` 格式支持 jpg/jpeg、png，文件大小不超过 10MB，单边分辨率小于 2000px。

## 请求示例

```json
{
  "styleId": "68aebb91b8619ed6f4168f40",
  "title": "聊AI行业",
  "materials": [
    {"type": "image", "fileUrl": "https://example.com/a.jpg", "soundSwitch": false},
    {"type": "video", "fileUrl": "https://example.com/b.mp4", "soundSwitch": false}
  ],
  "introduceCard": {
    "name": "廖志勇",
    "description": "AI行业领军人物"
  },
  "packRules": {
    "headerSwitch": true,
    "materialSwitch": true,
    "subtitleSwitch": true,
    "keywordSwitch": true,
    "backgroundMusic": {
      "audioSwitch": true,
      "audioUrl": "https://example.com/bg.mp3",
      "volume": 1
    }
  },
  "processRules": {
    "materialComposition": "random",
    "watermarkShow": true,
    "videoDuration": 30,
    "metadata": {
      "AIGC": "{"Label":"1","ContentProducer":"AI服务提供者的名称或统一社会信用代码等","ProduceID":"XXXXXXXXXXXXXXXXXXX"}"
    }
  },
  "structLayers": [
    {
      "markCode": "headerLayer",
      "show": true,
      "showMode": "customize",
      "showTime": 2,
      "layer": {"transform": {"position": [0, 0, 0]}}
    }
  ],
  "callbackUrl": "https://example.com/hook"
}
```

## 成功响应

```json
{
  "code": 1,
  "msg": "success",
  "data": {
    "task_id": "task_xxxxxxxxxxxx",
    "status": "processing",
    "app": "smart_clip",
    "api": "news_mixcut"
  }
}
```

## 响应字段

| 字段 | 类型 | 必返 | 说明 |
| --- | --- | --- | --- |
| `task_id` | string | 是 | 平台任务 ID |
| `status` | string | 是 | 平台任务状态，提交后通常为 `processing` 或 `queued` |
| `app` | string | 是 | 应用编码，固定为 `smart_clip` |
| `api` | string | 是 | API 编码 |

## 任务结果

任务完成后，平台任务查询结果中的 `result` 通常包含：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `video_url` | string | 视频url地址，视频生成类任务返回 |
| `cover_url` | string | 视频封面url地址 |
| `duration` | number | 生成的视频或音频时长，单位：秒 |
| `data` | object | 完整结果数据 |

任务失败时返回错误码和错误描述。

## 参数（平台 schema 原文）

```json
{
  "title": {
    "type": "string",
    "example": "聊AI行业",
    "maxLength": 1800,
    "minLength": 3,
    "description": "标题"
  },
  "styleId": {
    "type": "string",
    "example": "68aebb91b8619ed6f4168f40",
    "description": "视频模板ID"
  },
  "materials": {
    "type": "array",
    "items": {
      "type": "object",
      "required": [
        "type",
        "fileUrl"
      ],
      "properties": {
        "type": {
          "enum": [
            "image",
            "video"
          ],
          "type": "string",
          "options": "image / video",
          "description": "素材类型"
        },
        "fileUrl": {
          "type": "string",
          "description": "素材url"
        },
        "soundSwitch": {
          "type": "boolean",
          "default": false,
          "description": "当素材为视频时原声开关"
        }
      }
    },
    "description": "素材"
  },
  "packRules": {
    "type": "object",
    "description": "包装规则：仅用于控制标题、素材、字幕等是否参与模版的效果包装，无特殊要求不建议设置。"
  },
  "callbackUrl": {
    "type": "string",
    "example": "https://example.com/hook",
    "description": "结果通知回调地址"
  },
  "processRules": {
    "type": "object",
    "properties": {
      "metadata": {
        "type": "object",
        "description": "元水印数据，仅支持写入一组数据，且value值需为字符串，详情见产品介绍/元数据-AI 显式标识和隐式标识说明"
      },
      "videoDuration": {
        "type": "integer",
        "example": 30,
        "maximum": 300,
        "minimum": 5,
        "description": "视频时长 单位：秒，默认：跟随素材资源时长"
      },
      "watermarkShow": {
        "type": "boolean",
        "default": false,
        "description": "是否添加“AI生成”字样水印"
      },
      "firstFrameCover": {
        "type": "object",
        "description": "首帧封面配置"
      },
      "materialComposition": {
        "enum": [
          "random",
          "order"
        ],
        "type": "string",
        "default": "random",
        "options": "random / order",
        "description": "素材组合方式"
      }
    },
    "description": "处理规则"
  },
  "structLayers": {
    "type": "array",
    "description": "需要修改的图层数据"
  },
  "introduceCard": {
    "type": "object",
    "properties": {
      "name": {
        "type": "string",
        "description": "名称"
      },
      "description": {
        "type": "string",
        "description": "描述"
      }
    },
    "description": "身份栏信息，含义详见常见问题库"
  }
}
```

## 计费

- 结算口径：免费
- 标准价：`fixed_price=0.0000` / `input_price=0.000000`
- 租户价：`tenant_fixed_points=0.00` / `tenant_points_per_1k_input=0.0000`
- 分档：`720p`=0.2，`1080p`=0.3
