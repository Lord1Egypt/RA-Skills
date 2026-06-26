# 视频最终合成接口文档

baseurl是：https://api-cutflow.fun.tv

## 基本信息

| 项目 | 说明 |
|------|------|
| 路径 | `POST /qlapi.srv/hook/final-compose` |
| 鉴权 | 需要 API 鉴权（APIAuthMid） |
| 请求类型 | `application/json` |
| 响应类型 | `text/event-stream`（SSE 流式） |

## 请求参数

### 必填参数

| 字段 | 类型 | 说明 |
|------|------|------|
| `video_path` | string | 原始视频文件 URL |
| `commentary_srt_path` | string | 解说词 SRT 字幕文件 URL |
| `audio_zip` | string | 解说音频 ZIP 文件 URL（Azure TTS 产出，内含 .mp3 和 .word.json） |
| `batch_size` | int | ZIP 内音频文件数量，必须大于 0 |
| `bgm_path` | string | 背景音乐文件 URL，为空则不添加 BGM |
| `subtitle_mask_x` | int | 字幕遮罩区域 X 坐标（像素） |
| `subtitle_mask_y` | int | 字幕遮罩区域 Y 坐标（像素） |
| `subtitle_mask_width` | int | 字幕遮罩区域宽度（像素） |
| `subtitle_mask_height` | int | 字幕遮罩区域高度（像素） |
| `enable_transitions` | bool | 是否启用转场效果 |

## 请求示例

```json
{
 "task_id": 10001,
 "video_path": "https://example.com/video/raw.mp4",
 "commentary_srt_path": "https://example.com/srt/commentary.srt",
 "audio_zip": "https://example.com/tts/audio_batch.zip",
 "batch_size": 5,
 "bgm_path": "https://example.com/bgm/music.mp3",
 "bgm_volume": 30,
 "canvas_width": 1080,
 "canvas_height": 1920,
 "subtitle_font": "SimHei",
 "subtitle_font_size": 36,
 "subtitle_color": "0xFFFFFFFF",
 "subtitle_outline": true,
 "subtitle_outline_color": "0xFF000000",
 "enable_transitions": true
}
```

## SSE 响应说明

接口返回 SSE（Server-Sent Events）流式响应，每条事件格式为：

```
data: <JSON>\n\n
```

### 事件类型

SSE 流中会推送三种类型的事件：

#### 1. 进度事件

处理过程中推送，用于展示当前步骤和进度。

| 字段 | 类型 | 说明 |
|------|------|------|
| `request_id` | string | 请求唯一标识 |
| `step` | string | 当前步骤 |
| `message` | string | 进度描述信息 |

**step 枚举值：**

| 值 | 说明 |
|----|------|
| `download` | 文件下载阶段（视频、字幕、BGM、音频ZIP） |
| `subtitle` | 字幕生成阶段 |
| `compose` | 视频合成阶段 |

**示例：**

```
data: {"request_id":"","step":"download","message":"正在下载视频文件..."}

data: {"request_id":"","step":"download","message":"正在下载解说词字幕文件..."}

data: {"request_id":"","step":"download","message":"正在下载并解压音频文件..."}

data: {"request_id":"a1b2c3d4","step":"subtitle","message":"开始生成解说字幕"}

data: {"request_id":"a1b2c3d4","step":"compose","message":"开始执行视频合成"}
```

> 注：download 阶段的 `request_id` 为空字符串，因为此时尚未进入 logic 层生成 requestID。

#### 2. 错误事件

任一步骤失败时推送，推送后 SSE 流结束。

| 字段 | 类型 | 说明 |
|------|------|------|
| `err_code` | int | 错误码（400 或 500） |
| `err_message` | string | 错误描述 |

**示例：**

```
data: {"err_code":500,"err_message":"下载视频失败: connection timeout"}
```

#### 3. 完成事件

合成成功并上传 OSS 后推送，推送后 SSE 流结束。

| 字段 | 类型 | 说明 |
|------|------|------|
| `err_code` | int | 固定为 `-1`，表示成功 |
| `err_message` | string | 固定为 `"success"` |
| `data` | object | 合成结果（见下表） |

**data 字段说明：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `success` | bool | 是否成功，固定为 `true` |
| `request_id` | string | 请求唯一标识 |
| `output_path` | string | 合成视频 OSS 签名 URL（有效期 3 天） |
| `draft_path` | string | 草稿目录路径 |

**示例：**

```
data: {"err_code":-1,"err_message":"success","data":{"success":true,"request_id":"a1b2c3d4","output_path":"https://oss.example.com/video/output.mp4?sign=xxx","draft_path":"/tmp/a1b2c3d4/draft_output"}}
```

## 参数校验错误

参数校验失败时直接返回 JSON（非 SSE），HTTP 状态码 200，响应体：

```json
{
 "err_code": 400,
 "err_message": "video_path is required"
}
```

可能的校验错误：

| err_message | 说明 |
|-------------|------|
| `请求参数解析失败: ...` | 请求体 JSON 解析失败 |
| `video_path is required` | 视频 URL 为空 |
| `commentary_srt_path is required` | 解说词字幕 URL 为空 |
| `audio_zip is required` | 音频 ZIP URL 为空 |
| `batch_size must be greater than 0` | ZIP 内文件数量不合法 |

## 处理流程

```
1. 参数校验
2. 创建下载临时目录: {tempDir}/{taskId}/compose/
3. 进入 SSE 流
 ├── [download] 下载视频文件到本地
 ├── [download] 下载解说词 SRT 文件到本地
 ├── [download] 下载 BGM 文件到本地（可选）
 ├── [download] 下载并解压音频 ZIP 到 compose/audios/
 ├── [subtitle] 从 word.json 生成精细字幕（fine_subtitle_srt_path 为空时）
 ├── [compose] 调用 hook-video CLI 执行视频合成
 ├── 上传合成视频到 OSS，生成 3 天有效期签名 URL
 └── 推送完成事件
4. defer 清理下载临时目录
```
