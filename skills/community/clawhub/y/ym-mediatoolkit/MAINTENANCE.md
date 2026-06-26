# YM MediaToolkit 维护手册

本文档面向后续维护者，记录版本发布、测试验证、配置边界和排障流程。

## 发布流程

1. 同步版本号：
   - `SKILL.md` front matter 的 `version`
   - `skill.json` 的 `version`
2. 更新用户文档：
   - 新增 action 时同步更新 `SKILL.md` 和 `skill.json`
   - 新增参数时同步补充默认值、用途和安全限制
   - 变更行为时在 `SKILL.md` 的版本更新段落记录
3. 运行验证：

```bash
python3 -B -m py_compile run.py utils.py intent_parser.py audio_extractor.py frame_extractor.py video_compressor.py asr_engine.py ocr_engine.py subtitle_extractor.py caption_segmenter.py job_manager.py tests/test_release_behaviors.py scripts/smoke_test.py
python3 -m json.tool skill.json
python3 -B -m unittest discover -s tests
python3 scripts/smoke_test.py
```

4. 清理产物：

```bash
find . -type d -name __pycache__ -prune -exec rm -r {} +
find . -name .DS_Store -delete
```

## 当前接口分层

- `chat`：Claw 推荐入口，接收自然语言，解析后调用现有 action。
- `pipeline`：确定性 JSON 流水线入口，适合多步骤、可重复的自动化流程。
- `audio` / `thumbnail` / `compress` / `info` / `audio_info`：底层单步能力。
- `subtitle` / `asr` / `ocr`：字幕识别能力，输出 SRT-like captions JSON。
- `caption_segment`：emlet 字幕二次分句器，处理已有 captions，不重新识别媒体。
- `batch` / `audio_batch`：批量处理入口。
- `/skill/jobs`：HTTP 异步长任务入口，适合压缩、字幕识别、pipeline 等耗时 action。
- `/skill/chat` + `async:"auto"`：Claw 推荐长任务入口，先解析自然语言，再自动提交 job。

维护原则：新体验优先接到 `chat` 或 `pipeline`，媒体处理逻辑继续复用底层 action，避免重复实现 ffmpeg 调用。

## Action 返回协议

所有 action 必须返回 JSON 对象，并保留以下协议字段：

- `status`：`success` / `partial` / `skipped` / `error`
- `code`：稳定机器码，成功为 `ok`
- `reply`：适合聊天展示的中文回复
- `hint`：下一步建议或排障提示

新增 handler 时只需要返回原始业务结果，`run.py` 的 action protocol wrapper 会补齐缺失字段。若底层模块已经返回 `code`，包装层会保留该值。

常用错误码：

| code | 场景 |
|------|------|
| `missing_source` | 缺少 `video_url` / `url` / `source` |
| `source_not_allowed` | 本地路径不在当前工作目录或 `media_roots` 内 |
| `output_exists` | 输出文件已存在且 `overwrite=false` |
| `parse_failed` | `chat` 无法识别自然语言意图 |
| `missing_steps` | `pipeline` 未传 `steps` |
| `missing_captions` | `caption_segment` 未传 `captions` 或 `caption_path` |
| `invalid_action` | 异步任务或 CLI 传入不支持的 action |
| `invalid_params` | HTTP job 的 `params` 不是 JSON object |
| `invalid_async_mode` | HTTP chat 的 `async` 不是 boolean 或 `"auto"` |
| `invalid_wait_timeout` | HTTP chat 的 `wait_timeout_sec` 不是 `0-30` 秒数字 |
| `invalid_job_id` | job id 格式不合法 |
| `job_not_found` | job 文件不存在 |
| `job_interrupted` | 服务重启或进程中断导致未完成 job 失效 |
| `unsupported_action` | action 或 pipeline step 不支持 |
| `invalid_step` | pipeline step 结构不合法 |
| `ffmpeg_failed` | ffmpeg / ffprobe 缺失或执行失败 |
| `missing_asr_dependency` | ASR 依赖缺失 |
| `missing_ocr_dependency` | OCR 依赖缺失 |

## HTTP 异步任务维护

异步任务逻辑在 `job_manager.py`。HTTP 服务启动时会创建单 worker 队列，串行执行提交到 `/skill/jobs` 的 action。

维护规则：

- job 文件存储在 `output/jobs/<job_id>/job.json`。
- job id 使用 32 位十六进制 UUID。
- job 文件必须保留 `job_id`、`action`、`params`、`status`、`code`、`reply`、`hint`、`created_at`、`started_at`、`finished_at`、`result`、`output_paths`、`error`。
- `chat` 提交的 job 会额外写入 `created_by=chat`、`intent`、`source`、`metadata.message`。
- `/skill/jobs` 直接提交的 job 会写入 `created_by=jobs`。
- 当前版本不支持取消任务，不记录进度百分比。
- 服务重启后不恢复未完成任务；旧的 `queued` / `running` 会标记为 `error`，`code=job_interrupted`。
- HTTP 服务启动时会调用 `cleanup_jobs(retention_days=7, max_jobs=200)`，只清理达到保留期或超量的终态 job，不清理 `queued` / `running`。
- 新增 action 时，只要加入 `ACTIONS`，异步任务会自动支持。
- `/skill/jobs` 的 `params` 必须是 JSON object；缺省或 `null` 会按 `{}` 处理，其他类型返回 `invalid_params` 且不创建 job。

## HTTP chat 异步排障

`/skill/chat` 支持 `async` 参数：

- `false` 或不传：保持同步执行，兼容 CLI 和旧 HTTP 调用。
- `true`：解析成功后总是提交 job，不立即执行底层 handler。
- `"auto"`：只把 `audio`、`compress`、`asr`、`ocr`、`subtitle`、`caption_segment`、`batch`、`pipeline` 作为长任务提交；`info`、`audio_info`、`thumbnail` 继续同步。

排查要点：

- `async` 只接受 JSON boolean 或 `"auto"`；字符串 `"true"` / `"false"` 会返回 `invalid_async_mode`。
- `wait_timeout_sec` 只接受 `0-30` 秒数字；非法值会返回 `invalid_wait_timeout`。
- 异步任务排队或运行中返回 HTTP `202`；短等待内已完成时返回 HTTP `200` 和最终 job 结果。
- 如果返回 `parse_failed`，说明自然语言没有解析出 action 或 source，不会创建 job。
- 如果返回 `queued`，让调用方使用 `poll_url` 查询最终 `reply`、`result`、`output_paths`。
- 如果任务完成后 `output_paths` 为空，检查底层 action 是否返回了 `output_path`、`saved_path`、`outputPath` 或 `manifest_path`。重复路径会按首次出现顺序去重。

## media_roots 配置

本地输入默认只允许当前工作目录内的文件。需要处理绝对路径时，必须配置媒体根目录白名单。

请求级配置：

```json
{
  "message": "将 \"D:/AA.MP4\" 提取音频",
  "media_roots": ["D:/"]
}
```

环境变量配置：

```bash
export YM_MEDIA_ROOTS="/Users/me/Videos;/Volumes/Media"
```

规则：

- `media_roots` 优先级高于 `YM_MEDIA_ROOTS`
- 未配置时只允许当前工作目录
- 支持用逗号或分号分隔多个根目录
- URL 仍只允许 `http` / `https`
- 输出路径仍限制在当前工作目录内

## 自然语言解析维护

解析逻辑在 `intent_parser.py`。

当前支持：

- 提取音频：`将 "sample.mp4" 提取音频`
- 提取封面：`给 "sample.mp4" 提取第 3 秒封面`
- 压缩：`压缩 "sample.mp4"`
- 查看信息：`查看 "sample.mp4" 信息`
- JSON pipeline：消息本身是包含 `steps` 的 JSON
- 字幕识别：`识别 "sample.mp4" 的字幕`

新增自然语言规则时需要同时补：

- `tests/test_release_behaviors.py` 的解析测试
- `scripts/smoke_test.py` 的真实链路测试，若会产生文件
- `SKILL.md` 的示例
- `skill.json` 的 action schema 或 examples，若公开接口有变化

## 验证策略

单元测试覆盖轻量行为：

- 输入字段兼容：`video_url` / `url` / `source`
- 本地路径和 `media_roots` 权限
- 默认输出目录和 `overwrite=false`
- pipeline 顺序、跳过、失败继续、manifest
- chat 解析、执行、失败不调用 handler

Smoke test 覆盖真实 ffmpeg 链路：

- 生成 1 秒本地测试视频
- 跑 `info`、`thumbnail`、`audio`、`compress`、`batch`
- 跑 `pipeline`
- 跑 `chat` 的音频、封面、压缩、信息命令
- 跑 `subtitle`；若环境未重新安装依赖，需返回 dependency error；安装完整依赖后验证 captions JSON

## 字幕识别维护

字幕输出统一使用 camelCase 和微秒整数：

```json
{
  "captionTxt": "字幕文本",
  "startTimeUs": 1000000,
  "endTimeUs": 2000000,
  "source": "asr",
  "confidence": 0.92
}
```

字幕识别依赖已进入默认 `requirements.txt`：

```bash
pip install -r requirements.txt
```

维护规则：

- `subtitle` 是推荐入口，`asr` / `ocr` 用于单独调试。
- `mode=fusion` 默认 ASR 为主，OCR 只做高置信文本校正。
- 环境未安装完整依赖时必须返回 JSON error，不能抛未捕获异常。
- 新增字幕准确率策略时，优先补 `subtitle_extractor.py` 的纯函数测试。

## emlet 字幕分句维护

二次分句逻辑在 `caption_segmenter.py`，对已有 captions 做后处理，不调用 ASR/OCR。

默认策略：

- `max_chars=12`
- 强标点优先切分：`。！？!?`
- 弱标点其次：`，、；：,;:`
- 再尝试连接词边界，最后按长度切分
- `protected_terms` 和 `protected_terms_path` 内的词不允许被拆开
- `auto_protect_ascii=true` 时自动保护英文、数字、型号、URL、路径

维护规则：

- 新增分句策略时先补纯函数测试，确保时间轴连续、不重叠、不倒退。
- `caption_segment` 输出继续使用 `captionTxt`、`startTimeUs`、`endTimeUs`。
- pipeline 中 `caption_segment` 如果没有显式传 `caption_path`，会自动使用前面步骤生成的 `.captions.json`。

## 常见问题

`本地输入路径超出允许的 media_roots`

确认文件路径位于当前工作目录，或在请求中传入 `media_roots`。

`输出路径超出工作目录`

输出文件必须写入当前工作目录下，例如 `output/audio/demo.mp3`。

`ffmpeg 错误，返回码: ...`

先确认输入文件可播放，再用 smoke test 验证当前环境的 ffmpeg 是否可用。

`DNS 解析失败` 或 `禁止访问私有/内网 IP`

远程 URL 会做安全校验，不允许内网、回环、链路本地地址或无法验证的目标。

`chat` 没识别出命令

优先使用明确句式：`将 "sample.mp4" 提取音频`、`给 "sample.mp4" 提取第 3 秒封面`、`压缩 "sample.mp4"`。

`缺少 ASR/OCR 依赖`

重新运行 `pip install -r requirements.txt`，确认 `faster-whisper`、`paddlepaddle`、`paddleocr` 已安装。
