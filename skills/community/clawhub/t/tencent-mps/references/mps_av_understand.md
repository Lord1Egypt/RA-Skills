# 大模型音视频理解参数与示例 — `mps_av_understand.py`

**功能**：大模型音视频内容理解，支持视频画面理解、语音识别、对比分析等。
> **核心机制**：通过 `AiAnalysisTask.Definition=33` + `ExtendedParameter(mvc.mode + mvc.prompt)` 控制。
> `--mode` 和 `--prompt` 是最重要的两个参数，**强烈建议每次调用都明确填写**。

## 参数说明

| 参数 | 说明 |
|------|------|
| `--local-file` | 本地文件路径，自动上传到 COS 后处理（与 `--cos-input-*` 互斥）|
| `--url` | 音视频 URL（HTTP/HTTPS），与 `--task-id` 互斥 |
| `--cos-input-key` | COS 输入文件的 Key（如 `/input/video.mp4`，推荐使用）|
| `--cos-input-bucket` | 输入文件所在 COS Bucket 名称（默认使用环境变量）|
| `--cos-input-region` | 输入文件所在 COS Region（如 `ap-guangzhou`）|
| `--task-id` | 直接查询已有任务结果，跳过创建 |
| `--mode` | **必填**。理解模式：`video`（理解视频画面内容，默认）/ `audio`（仅处理音频，视频会自动提取音频）|
| `--prompt` | **必填**。大模型提示词，决定理解侧重点和输出格式（如"请对视频进行语音识别"）|
| `--extend-url` | 对比两段音视时，第二段对比音视频 URL（用于对比分析，最多 1 条）|
| `--definition` | AiAnalysisTask 模板 ID（默认 `33`，即预设视频理解模板）|
| `--no-wait` | 异步模式：只提交任务，不等待结果 |
| `--json` | 以 JSON 格式输出结果 |
| `--output-dir` | 将结果 JSON 保存到指定目录 |
| `--verbose` / `-v` | 显示详细日志信息 |
| `--region` | 处理地域（优先读取 `TENCENTCLOUD_API_REGION` 环境变量，默认 `ap-guangzhou`） |
| `--dry-run` | 只打印参数预览，不调用 API |

## 强制规则

- `--mode` 和 `--prompt` **必填**，禁止省略：
  - `--mode video`：理解视频画面内容
  - `--mode audio`：仅处理音频（视频会自动提取音频）
  - `--prompt`：控制大模型理解侧重点，缺失时结果可能为空

## 示例命令

```bash
# 理解视频内容（--mode video + 提示词）
python scripts/mps_av_understand.py \
    --url https://example.com/video.mp4 \
    --mode video \
    --prompt "请分析这个视频的主要内容、场景和关键信息"

# 音频模式：语音识别（视频自动提取音频）
python scripts/mps_av_understand.py \
    --url https://example.com/video.mp4 \
    --mode audio \
    --prompt "请对这段音频进行语音识别，输出完整文字内容"

# 纯音频文件
python scripts/mps_av_understand.py \
    --url https://example.com/audio.mp3 \
    --mode audio \
    --prompt "请识别这段音频的内容并输出文字"

# 对比分析（两段音视频）
python scripts/mps_av_understand.py \
    --url https://example.com/standard.mp4 \
    --extend-url https://example.com/user.mp4 \
    --mode audio \
    --prompt "请对比这两段音频，分析差异，给出专业评价"

# COS 对象输入
python scripts/mps_av_understand.py \
    --cos-input-key /input/my-video.mp4 \
    --mode video \
    --prompt "总结视频的核心内容"

# 异步模式：只提交任务
python scripts/mps_av_understand.py \
    --url https://example.com/video.mp4 \
    --mode video --prompt "分析视频内容" --no-wait

# 查询已有任务结果
python scripts/mps_av_understand.py --task-id 2600011633-WorkflowTask-80108cc3380155d98b2e3573a48a

# 将结果保存到本地目录
python scripts/mps_av_understand.py \
    --url https://example.com/video.mp4 \
    --mode video --prompt "分析内容" --output-dir /output/
```

