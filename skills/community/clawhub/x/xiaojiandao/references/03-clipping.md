# AI智能剪辑的前置结果

基于原始视频转写文本（long_lines）和分析结果，对视频进行前置结果的分析，得到如何切片。

## 接口

### 提交智能剪辑

```
POST /api/hook/submit/intelligent.slice.engine
```

### 查询智能剪辑结果

```
POST /api/hook/query/intelligent.slice.engine.result
```

**轮询参数**：body 传 `{"task_id": server_task_id}`

> ⚠️ **轮询必须用 POST + body 传参**，不能用 GET + query string！

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `task_id` | int | ✅ | server_task_id |
| `long_lines` | **string** | ✅ | **原始视频转写文本，必须是字符串类型且带时间戳**（**必须是SRT格式**，禁止传纯文本或无时间戳内容） |
| `clip_duration` | string | ✅ | 目标剪辑时长（如 "2分钟"，来自需求分析） |
| `jianji_prompt` | string | ✅ | 剪辑参考提示词（来自需求分析） |
| `jieshuo_prompt` | string | ✅ | 解说参考提示词（来自需求分析） |

## long_lines 获取方式

`long_lines` 是原始视频的完整转写文本，建议通过以下方式获取：

### 方式一：本地视频 ASR（推荐）

```
视频 → ffmpeg抽音频(16kHz mp3) → 上传到 OSS → /api/aipkg/submit/volcano.auc → 轮询 → 返回SRT格式
```

> ⚠️ **重要参数发现**：`volcano.auc` 提交时参数名为 **`file_url`**（不是 `audio_url`）！
> **必须使用完整的带签名参数的 URL**（即 `oss_upload()` 返回的 `url` 字段，**不要**用 `oss_path`）：
> ```python
> api("/api/aipkg/submit/volcano.auc", {"task_id": TASK_ID, "file_url": result["url"]})
> # 其中 result["url"] = "https://files.cxtfun.com/...mp3?Expires=...&OSSAccessKeyId=...&Signature=..."
> # oss_path 只是内部路径，不能用于 API 调用！
> ```

### 方式二：已有字幕文件

直接读取本地 `.srt` 文件内容作为 `long_lines`（`.srt` 文件本身已包含时间戳）。

### 方式三：手动粘贴

用户直接提供转写文本。**⚠️ 注意：手动粘贴的文本必须带有时间戳（SRT格式），否则切片引擎无法正确工作。**

### SRT 格式示例

`long_lines` 传入的内容必须是如下 SRT 格式（包含时间戳信息）：

```
1
00:00:05,000 --> 00:00:10,500
第一个片段的字幕文本

2
00:00:15,000 --> 00:00:25,800
第二个片段的字幕文本
```

**禁止**传入如下无时间戳的纯文本：
```
第一个片段的字幕文本
第二个片段的字幕文本
```

## 异步轮询

1. 提交后获取 `err_code=-1` 即成功
2. 轮询查询接口
3. **建议超时**：300秒（视频较长时）
4. **轮询间隔**：2-3秒

## 轮询响应（state=2 成功）

```json
{
  "err_code": -1,
  "state": 2,
  "data": {
    "state": 2,
    "result": {
      "cut_story": "切片后的剧情主线...",
      "short_lines": "切片后的关键台词/短句..."
    }
  }
}
```

## 返回字段说明

| 字段 | 说明 |
|------|------|
| `cut_story` | 切片后的剧情主线（传给解说脚本/音色推荐/BGM推荐） |
| `short_lines` | 切片后的关键台词（传给解说脚本生成） |

## 注意事项

- `long_lines` **必须是完整转写文本**，由AUC音频提取文字而来
- **⚠️ `long_lines` 必须是字符串类型**：在构造 payload 时，必须使用 `str(long_lines)` 确保转换为字符串，**禁止直接传数字、list 或其他类型**
- **⚠️ `long_lines` 必须带时间戳（SRT格式）**：禁止传入不带时间戳的纯文本，必须使用 `volcano.auc` 返回的 SRT 格式结果
- SRT 格式包含时间戳，AI 可以更好地对齐视频片段
- `jianji_prompt` 和 `jieshuo_prompt` 来自需求分析结果，引导切片朝正确方向进行
- 如果切片未成功（`state != 2`），检查 `long_lines` 格式是否正确（SRT带时间戳）、内容是否足够长、**类型是否为字符串**
