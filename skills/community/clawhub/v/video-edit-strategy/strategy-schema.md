# 剪辑策略 JSON Schema

本文档定义 `video-edit-strategy` 输出的完整 JSON 结构。下游 skill 依赖此格式解析和执行。

## 顶层结构

```json
{
  "project": { ... },
  "materials": [ ... ],
  "timeline": [ ... ],
  "audio": { ... },
  "text_overlays": [ ... ],
  "execution_plan": [ ... ]
}
```

---

## 1. project（项目元信息）

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `name` | string | 是 | 项目名称 |
| `platform` | enum | 是 | 目标平台 |
| `aspect_ratio` | enum | 是 | 画面比例 |
| `resolution` | object | 是 | 输出分辨率 |
| `resolution.width` | int | 是 | 宽度像素 |
| `resolution.height` | int | 是 | 高度像素 |
| `fps` | int | 是 | 输出帧率，默认 30 |
| `target_duration` | float | 是 | 目标总时长（秒） |
| `style` | enum | 是 | 剪辑风格 |
| `output_path` | string | 是 | 最终输出文件路径 |

**枚举值：**

- `platform`: `"douyin"` | `"kuaishou"` | `"xiaohongshu"` | `"youtube_shorts"` | `"instagram_reels"` | `"bilibili"` | `"general"`
- `aspect_ratio`: `"9:16"` | `"16:9"` | `"1:1"` | `"4:3"` | `"21:9"`
- `style`: `"fast_pace"` | `"narrative"` | `"ambient"` | `"vlog"` | `"montage"`

**分辨率速查：**

| 比例 | 分辨率 |
|------|--------|
| 9:16 | 1080x1920 |
| 16:9 | 1920x1080 |
| 1:1 | 1080x1080 |
| 4:3 | 1440x1080 |

---

## 2. materials（素材清单）

数组，每个元素描述一个输入素材。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `id` | string | 是 | 素材唯一标识，如 `"m1"`, `"m2"` |
| `type` | enum | 是 | `"video"` / `"image"` / `"audio"` |
| `path` | string | 是 | 文件绝对路径 |
| `duration` | float | 视频/音频必填 | 时长（秒），由 ffprobe 获取 |
| `width` | int | 视频/图片必填 | 像素宽度 |
| `height` | int | 视频/图片必填 | 像素高度 |
| `codec` | string | 否 | 编码格式，如 `"h264"`, `"aac"` |
| `fps` | float | 视频时填 | 原始帧率 |
| `has_audio` | bool | 视频时填 | 是否包含音频轨道 |

---

## 3. timeline（时间线编排）

数组，按播放顺序排列。每个元素是一个镜头/场景。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `scene_id` | string | 是 | 场景标识，如 `"s1"`, `"s2"` |
| `segment` | enum | 是 | 所属段落 |
| `material_ref` | string | 是 | 引用 `materials[].id` |
| `source_in` | string | 是 | 源素材起始时间 `HH:MM:SS.mmm` |
| `source_out` | string | 是 | 源素材结束时间 `HH:MM:SS.mmm` |
| `timeline_start` | string | 是 | 在输出时间线上的起始位置 |
| `duration` | float | 是 | 在输出中的持续时长（秒），计入变速 |
| `speed` | float | 否 | 播放速度倍率，默认 `1.0` |
| `transition_in` | object | 否 | 入场转场 |
| `transition_out` | object | 否 | 出场转场 |
| `filters` | array | 否 | 应用的滤镜列表 |
| `description` | string | 否 | 该镜头的内容描述（便于理解） |

**segment 枚举：** `"hook"` | `"content"` | `"buildup"` | `"climax"` | `"ending"`

### transition 对象

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `type` | enum | 是 | 转场类型 |
| `duration` | float | 是 | 转场时长（秒），通常 0.3–1.0 |

**type 枚举（对应 FFmpeg xfade）：**
- `"cut"` — 硬切（无 xfade）
- `"fade"` — 淡入淡出
- `"fadewhite"` — 闪白过渡
- `"fadeblack"` — 闪黑过渡
- `"dissolve"` — 交叉溶解
- `"wipeleft"` — 向左擦除
- `"wiperight"` — 向右擦除
- `"wipeup"` — 向上擦除
- `"wipedown"` — 向下擦除
- `"slideleft"` — 向左滑动
- `"slideright"` — 向右滑动
- `"smoothleft"` — 平滑左移
- `"smoothright"` — 平滑右移

### filter 对象

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `name` | string | 是 | 滤镜名称 |
| `params` | object | 否 | 滤镜参数键值对 |

常用滤镜：
- `"brightness"` — `{ "value": 0.05 }` 范围 -1.0 ~ 1.0
- `"contrast"` — `{ "value": 1.2 }` 范围 0 ~ 2.0
- `"saturation"` — `{ "value": 1.3 }` 范围 0 ~ 3.0
- `"blur"` — `{ "sigma": 2 }`
- `"sharpen"` — `{ "amount": 1.5 }`
- `"colorbalance"` — `{ "rs": 0.1, "gs": -0.1, "bs": 0.05 }`
- `"vignette"` — `{ "angle": 0.5 }`
- `"crop_to_ratio"` — `{ "ratio": "9:16" }` 裁切适配目标比例

---

## 4. audio（音频编排）

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `bgm` | object | 否 | 背景音乐配置 |
| `original_audio` | object | 否 | 原声处理 |
| `voiceover` | object | 否 | 配音处理 |

### bgm 对象

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `material_ref` | string | 是 | 引用 `materials[].id` |
| `volume` | float | 是 | 音量倍率 0.0–1.0 |
| `fade_in` | float | 否 | 淡入时长（秒），默认 0.5 |
| `fade_out` | float | 否 | 淡出时长（秒），默认 2.0 |
| `start_offset` | float | 否 | BGM 起始偏移（秒），用于跳过前奏 |
| `loop` | bool | 否 | 是否循环以覆盖视频时长 |

### original_audio 对象

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `keep` | bool | 是 | 是否保留原声 |
| `volume` | float | 否 | 原声音量倍率，默认 0.25（有 BGM 时） |

### voiceover 对象

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `material_ref` | string | 是 | 引用 `materials[].id` |
| `volume` | float | 是 | 音量倍率 0.0–1.0 |
| `timeline_start` | string | 否 | 在时间线上的起始位置 |

---

## 5. text_overlays（文字叠加）

数组，每个元素是一条文字叠加。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `text` | string | 是 | 显示文字内容 |
| `timeline_start` | string | 是 | 出现时间 `HH:MM:SS.mmm` |
| `timeline_end` | string | 是 | 消失时间 `HH:MM:SS.mmm` |
| `position` | enum | 是 | 位置 |
| `font_size` | int | 否 | 字号，默认 48 |
| `font_color` | string | 否 | 颜色，默认 `"white"` |
| `bg_color` | string | 否 | 文字背景色，默认 `null`（无背景） |
| `bg_opacity` | float | 否 | 背景透明度 0.0–1.0 |

**position 枚举：**
- `"top_center"` — 顶部居中
- `"center"` — 画面正中
- `"bottom_center"` — 底部居中（常用于字幕）
- `"top_left"` / `"top_right"` — 角落位置
- `"bottom_left"` / `"bottom_right"` — 角落位置

---

## 6. execution_plan（执行计划）

数组，按执行顺序排列。每个元素是一个可执行步骤。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `step` | int | 是 | 步骤序号，从 1 开始 |
| `action` | enum | 是 | 操作类型 |
| `description` | string | 是 | 操作简述 |
| `inputs` | array | 是 | 输入文件路径列表（可引用前序步骤的 output） |
| `output` | string | 是 | 输出文件路径 |
| `params` | object | 否 | 操作参数 |
| `skill_ref` | string | 是 | 执行该步骤的 skill 名称 |

**action 枚举：**

| action | skill_ref | 用途 |
|--------|-----------|------|
| `probe` | `shell` | ffprobe 获取素材信息 |
| `cut` | `ffmpeg-cli` | 裁剪视频片段 |
| `speed` | `ffmpeg-cli` | 变速处理 |
| `merge` | `ffmpeg-cli` | 合并多个片段 |
| `convert` | `ffmpeg-cli` | 格式转换 |
| `extract_frame` | `video-frames` | 提取关键帧 |
| `add_text` | `ffmpeg-video-editor` | 添加文字叠加 |
| `add_audio` | `ffmpeg-video-editor` | 混合音频 |
| `filter` | `ffmpeg-video-editor` | 应用滤镜/调色 |
| `xfade` | `ffmpeg-video-editor` | 应用转场效果 |
| `scale` | `ffmpeg-video-editor` | 缩放/裁切适配分辨率 |

### params 示例

**cut:**
```json
{ "start": "00:00:05.000", "end": "00:00:08.500" }
```

**speed:**
```json
{ "rate": 1.5 }
```

**xfade:**
```json
{ "transition": "dissolve", "duration": 0.5, "offset": 7.5 }
```

**add_text:**
```json
{
  "text": "跟我学做菜",
  "position": "bottom_center",
  "font_size": 48,
  "font_color": "white",
  "start": "00:00:00.000",
  "end": "00:00:03.000"
}
```

**add_audio:**
```json
{
  "mode": "mix",
  "volume_main": 0.25,
  "volume_overlay": 0.8,
  "fade_in": 0.5,
  "fade_out": 2.0
}
```

**scale:**
```json
{ "width": 1080, "height": 1920, "method": "pad" }
```

`method` 取值：`"pad"`（加黑边）| `"crop"`（裁切）| `"stretch"`（拉伸）

---

## 字段引用规则

- `material_ref` 引用 `materials[].id`（如 `"m1"`）
- `execution_plan[].inputs` 可使用前序步骤的 `output` 路径
- 中间产物路径统一使用 `/tmp/ve_strategy/` 前缀
- 最终输出路径写入 `project.output_path`
