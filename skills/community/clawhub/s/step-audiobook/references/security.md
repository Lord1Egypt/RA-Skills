# 安全与外部访问

语言切换：当前为中文｜[English companion](./security.en.md)

这份文档用于帮助用户、审查者和程序调用方快速判断 `audiobook` 会访问什么、读取什么，以及哪些动作可能产生费用。

## 运行时依赖

`audiobook` 当前默认声明并实际依赖以下运行时条件：

- 环境变量：`STEP_API_KEY`
- 系统二进制：`ffmpeg`
- 系统二进制：`ffprobe`

这些依赖已经同步写入 `SKILL.md` 的 frontmatter `metadata.openclaw.requires`，用于让 ClawHub / OpenClaw 侧的注册表元数据与文档保持一致。

## 默认外部接口

如果你不手动改 `base_url`，默认外部访问目标只有 Step 相关接口：

- `scripts/sync_voice_library.py`
  - `https://api.stepfun.com/v1/audio/system_voices`
  - `https://api.stepfun.com/v1/chat/completions`
- `scripts/step_tts_client.py` / `scripts/synthesize_tts_requests.py`
  - `https://api.stepfun.com/v1/audio/speech`
- `scripts/clone_selected_voices.py`
  - `https://api.stepfun.com/v1/files`
  - `https://api.stepfun.com/v1/audio/voices`
- `scripts/llm_json.py`（供结构化剧本、选角等 LLM 推理环节使用）
  - 默认：`https://api.stepfun.com/step_plan/v1/chat/completions`

## 哪些情况下会访问非默认 endpoint

以下情况属于“用户显式配置后的定向访问”，不是 skill 的默认行为：

- 你在 `voice-library.yaml` 里改了 `llm.*.base_url`
- 你在某些脚本上显式传了 `--base-url`
- 你在合成脚本上显式传了 `--api-key-env`，要求从别的环境变量名取 key

也就是说：默认配置是 Step endpoint；只有你自己改配置或命令参数时，才会访问你指定的兼容服务。

## 默认读取的环境变量

默认情况下，skill 只要求并读取：

- `STEP_API_KEY`

补充说明：

- `scripts/run_audiobook.py` 和 `scripts/synthesize_tts_requests.py` 支持 `--api-key-env`，允许你显式指定别的环境变量名。
- 这不表示 skill 会自动枚举大量环境变量；它只会读取你指定的那个 key 名。
- 当前文档、模板和默认配置都以 `STEP_API_KEY` 为主。

## 默认读取和上传的文件范围

`audiobook` 默认不会主动扫描整个磁盘，也不会打包上传工作区全部内容。

它主要处理以下几类显式输入：

- 你给它的原始文本文件
- 你放进 `audiobook-library/voices/inbox/` 的待分析参考音频
- `voice-library.yaml` 里登记的 clone 参考音频路径
- 当前故事 run 目录下的中间产物与最终产物

其中真正会上传到 Step 的文件，只有你显式选择执行付费 clone 时，对应的参考音频文件；上传动作发生在 `scripts/clone_selected_voices.py` 中，并且只针对被选中的 `asset_id`。

## 付费动作边界

当前只有真正的音色复刻可能产生费用：

- `scripts/run_audiobook.py` 只会做 clone 预览，不会自动执行正式付费 clone
- `scripts/clone_selected_voices.py --dry-run` 只预览，不调用正式付费接口
- 真正执行 clone 需要同时满足：
  - `voice-library.yaml -> clones.<asset_id>.selected_for_clone = true`
  - 没有传 `--dry-run`
  - 显式传入 `--confirm-paid-action`

如果缺少最后一个确认参数，脚本会直接报错退出，而不是继续调用付费接口。

## 建议的安全测试方式

第一次使用或准备发布前，建议这样验证：

1. 使用测试 key、受限 key，或先准备一枚可随时轮换的 key
2. 先在隔离环境、容器或独立 workspace 跑一遍
3. 先执行 `clone_selected_voices.py --dry-run`，不要直接做正式 clone
4. 检查 `voice-library.yaml` 里是否有你不希望上传或不希望复刻的条目
5. 若曾在不完全信任的环境中测试，测试后轮换 key

## 给审查者的快速结论

如果你正在做一次快速代码审查，可以重点确认下面几点：

- `scripts/common.py`：API key 解析与来源展示是否安全
- `scripts/sync_voice_library.py`：官方音色同步与 `step-audio-r1.1` 分析是否只走预期接口
- `scripts/clone_selected_voices.py`：是否仍然必须 `--confirm-paid-action` 才能正式 clone
- `scripts/step_tts_client.py`：TTS 是否只向预期 TTS endpoint 发请求
- `scripts/run_audiobook.py`：是否仍然只做 clone dry-run 预览
