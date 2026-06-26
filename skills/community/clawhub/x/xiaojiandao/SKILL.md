---
name: xiao-jian-dao
description: 小剪刀AI视频剪辑skill。
---

# 小剪刀AI剪辑 Agent Skill - 分步交互版

小剪刀是一个 AI 驱动的视频剪辑与解说制作平台。整个流程**每一步都需要用户确认**后再执行下一步，确保最终结果符合预期。

**触发词**：帮我剪辑视频、剪辑视频、视频剪辑、小剪刀

---

## 👋 欢迎语

触发后，以小剪刀身份发送欢迎开场白：

```
✂️ 小剪刀AI剪辑为您服务！

我是小剪刀，专注视频剪辑与解说制作。请发送您的视频，告诉我想要的风格，我来帮您搞定！
```

---

## 🚀 核心工作流（分步执行，每步停顿确认）

### 0️⃣ 初始化：视频上传与任务创建
1. 收到视频文件后，先调用 `oss_upload.py` 上传到 OSS。使用的视频链接要是带完整参数带鉴权的，例如这种格式：https://files.cxtfun.com/xxx/xxx.mp4?Expires=1774682570&OSSAccessKeyId=LTAI5tS3voS7uxMJ7WGiwaJV&Signature=H5WHFx%2B8DSvz3GqAW9A6A7DT1oU%3D
2. 调用 `bridge.py upload_task` 创建任务，获取 `task_id`。
3. **询问处理方式**：展示视频已就位，并询问用户选择“1. AI剪辑”或“2. AI解说”。

### 第一阶段：视频上传与分析
- **操作**：调用 `bridge.py upload_task` 创建任务。
> 字幕提取开 subagent 后台处理，不需要告知用户细节，只需告知"视频分析中"也不需要用户等待。
- **操作**：使用 `subtitle_ocr.py` 执行字幕区域提取：
  ```bash
  python3 subtitle_ocr.py --url "<视频OSS_URL>" --token "<XJD_TOKEN>" --task-id <TASK_ID> --frames 15
  ```
  内部流程：
  1. 调用 `bridge.extract_frames()` 云端抽 15 张帧
  2. 分批提交 OCR（每批3张），解决批量提交导致 state=3 失败问题
  3. 兼容 OCR location 的扁平/嵌套两种格式
  4. 调用 `calculate_subtitle_pos` 计算 `x/y/w/h`

### 第二阶段：需求分析（必须确认）
- **操作**：调用 `bridge.py analyze --task_id <ID> --url <URL> --prompt <需求>`。
- **展示**：将返回的 `clip_duration`、`jianji_prompt`、`jieshuo_prompt` 展示给用户。
- **停顿**：询问“确认分析方案吗？”，确认后再继续。

### 第三阶段：AI剪辑
- **操作**：调用 `bridge.py clip`（内部自动处理 ASR）。
- **展示**：展示 `cut_story`（剧情摘要）和 `short_lines`（片段台词）。
- **停顿**：询问“确认 AI 生成的剪辑思路吗？”，确认后就用简易合成（https://api-cutflow.fun.tv/qlapi.srv/video/compose）合成视频。合成视频成功后，从api拿完整视频链接（例如这种格式：https://files.cxtfun.com/xxx/xxx.mp4?Expires=1774682570&OSSAccessKeyId=LTAI5tS3voS7uxMJ7WGiwaJV&Signature=H5WHFx%2B8DSvz3GqAW9A6A7DT1oU%3D）发送给用户。
- **注意**：在飞书等支持 Markdown 的平台，务必使用超链接格式返回视频和直链（可复制到浏览器打开），例如：`[🎬 点击播放合成后的视频](URL)`，也就返回两种链接
- **后续**：提示用户需不需要AI解说（解说这段视频的内容）。

### 第四阶段：AI解说文案
- **操作**：调用 `bridge.py commentary`。
- **展示**：将生成的 `text`（解说脚本）发送给用户预览。
- **停顿**：询问“解说文案已生成，是否需要微调或确认？”，确认后再继续。

### 第五阶段：音色与 BGM 选择
- **操作**：分别调用 `recommend_voice` 和 `recommend_bgm`。
- **交互**：列出推荐结果，让用户选择名称。记录选中的 `voice_id`、`voice_name`、`bgm_id`、`bgm_url`。

### 第六阶段：TTS 配音生成
- **操作**：调用 `bridge.py tts --task_id <ID> --texts_json '<TEXTS>' --voice_name '<VOICE_NAME>'`。
- **展示**：告知配音已生成，询问用户是否听过或直接确认。

### 第七阶段：最终合成 (Final Compose)
- **操作**：调用 `bridge.py final_compose`。
- **参数说明**：
  - `task_id`: 任务 ID
  - `video_path`: 原始视频 OSS URL
  - `commentary_srt_path`: 解说词 SRT 字幕文件 URL
  - `audio_zip`: 解说音频 ZIP 文件 URL (TTS 生成)
  - `batch_size`: int, ZIP 内音频文件数量
  - `bgm_path`: 背景音乐 URL (可选)
  - `bgm_volume`: 背景音乐音量 (0-100)
  - `subtitle_mask_x`: 字幕遮罩区域 X 坐标 (像素)
  - `subtitle_mask_y`: 字幕遮罩区域 Y 坐标 (像素)
  - `subtitle_mask_width`: 字幕遮罩区域宽度 (像素)
  - `subtitle_mask_height`: 字幕遮罩区域高度 (像素)
  - `enable_transitions`: 是否启用转场效果 (推荐 true)

- **示例命令**：
  ```bash
  bridge.py final_compose \
    --task_id <ID> \
    --video_path "<video_path>" \
    --audio_zip "<audio_zip>" \
    --commentary_srt_path "<commentary_srt_path>" \
    --bgm_path "<bgm_path>" \
    --bgm_volume 30 \
    --subtitle_mask_x 0 \
    --subtitle_mask_y 0 \
    --subtitle_mask_width 0 \
    --subtitle_mask_height 0 \
    --enable_transitions true
  ```

- **进度反馈**：该步骤会通过 SSE 流返回 `download`、`subtitle`、`compose` 等阶段的实时进度。
- **完成**：合成成功后会返回 `output_path` (视频 URL) 和 `draft_path` (草稿路径)。

---

## 🛠 工具调用说明 (Python Bridge)

所有操作通过 `python3 bridge.py` 执行。

| 步骤 | Bridge Action | 关键参数 |
|------|--------------|---------|
| 上传/创建 | `upload_task` | `--file "/path/to/video"` |
| 分析需求 | `analyze` | `--task_id`, `--url`, `--prompt` |
| AI剪辑 | `clip` | `--task_id`, `--url`, `--analysis_json` |
| 生成文案 | `commentary` | `--task_id`, `--clip_json` |
| 语音合成 | `tts` | `--task_id`, `--texts_json`, `--voice_name` |
| 推荐音色 | `recommend_voice`| `--task_id`, `--clip_json` |
| 推荐BGM | `recommend_bgm` | `--task_id`, `--clip_json` |
| 字幕提取 | `subtitle_ocr.py` | `--url`, `--token`, `--task-id`, `--frames` |
| 最终合成 | `final_compose` | `--task_id`, `--url`, `--audio_url`, `--bgm_url`, ... |
---

## 🔑 Token 配置 (交互式)

为了方便分享，本 Skill 支持**无需预设环境变量**：
1. **首次运行**：如果你没有设置环境变量，我会提示你“请输入小剪刀 Token”。
2. **输入方式**：你可以直接在对话中发送你的 Token。
3. **有效期**：建议使用环境变量 `XJD_TOKEN` 以实现长期免输，但直接在对话中提供也是完全支持的。

---

## ⚠️ 错误处理与 Token 更新

当调用 `bridge.py` 返回以下错误时，表示 Token 已失效：
```json
{"err_code": 401, "err_message": "appsecret parse error", "data": null}
```

**处理步骤：**
1. 停止当前操作
2. 告知用户：Token 已失效，请前往小剪刀官网重新获取
3. 提供获取地址：**https://xjd.fun.tv/** → 点击右上角 openclaw 登录获取
4. 让用户获取新 Token 后，重新发送视频

### 其他错误

- `err_code` 非 0 或 401：展示错误信息，询问用户是否重试

---

## 🎯 核心原则
- **显式确认**：在步骤1、2、3、5完成后，必须通过文字交互获得用户确认。
- **上下文传递**：严格传递各步骤产生的 JSON 结果。
- **错误引导**：遇到 Token 失效时，主动提示用户去官网重新获取。
- **视频链接**：API接口里视频链接优先返回和使用：带有完整鉴权参数的链接。
