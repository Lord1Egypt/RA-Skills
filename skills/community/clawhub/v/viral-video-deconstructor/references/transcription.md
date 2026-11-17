# 视频/音频转文字（ASR）流程

> 转录是**事实性步骤**：识别结果可能有误，改写前务必让用户核对关键数据、人名、引语。环境缺依赖时**明确告知，不要假装已转录**。

## 一、首选：平台内建字幕/转录（最稳）
- **YouTube**：视频页"…→ 显示文稿/转录"直接复制；或用 `youtube-transcript-api`（需联网）。
- **B站**：播放器"字幕"开关，CC 字幕可复制。
- **抖音/快手/视频号/小红书**：App 内"字幕/歌词"或创作者后台导出；无公开 API 时请用户手动复制文案。
- 链接类输入：优先让用户粘贴平台字幕/文案，比本地 ASR 更准。

## 二、次选：本地音视频 ASR（用户给了文件且环境可用）
前置依赖（**先查后跑**）：
1. **ffmpeg**：抽音频用。`command -v ffmpeg` 查；无则下载静态包或让用户先转成 wav/mp3。
2. **ASR 引擎**：`openai-whisper`（本地，需 PyTorch + 模型下载）或平台/云 ASR。
3. **模型下载源**：HuggingFace 直连在本环境不通，必须设 `HF_ENDPOINT=https://hf-mirror.com`（镜像）再跑，否则模型下载失败。

> ⚠️ 注意：ffmpeg 与 whisper 是**环境依赖**，**不打包进 Skill 文件夹**，也不会随 `dist/*.zip` 一起分发。换机器需重新安装。

### 已就绪环境（已装依赖的机器，可复用）
- ffmpeg：装在 `~/.workbuddy/tools/ffmpeg/ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe`（Windows，gh-proxy 下载的 BtbN 静态包；Linux/macOS 对应 `bin/ffmpeg`）。
  - 调用需把该 bin 目录加入 PATH（Windows 例：`export PATH="$PATH:$HOME/.workbuddy/tools/ffmpeg/ffmpeg-master-latest-win64-gpl/bin"`）。
- whisper：装在「运行本脚本的 Python」对应的 venv 里（`pip install openai-whisper`，含 torch CPU）。small 模型已缓存，无需重下。
- 新环境仍按"前置依赖"从头装；已装环境可直接复用上面路径。

### 一键安装（换机 / 新环境）
运行一次安装器即可补齐依赖，**自动下载 ffmpeg（gh-proxy 镜像）、pip 安装 whisper、写标记文件**：
- 该安装器已被 `transcribe.py` 内置调用——**直接跑 `transcribe.py` 即可，缺依赖时它会自动触发安装**，无需手动先跑本步。本步仅用于想提前装好或排错时。
```bash
# 用 WorkBuddy 托管 Python 运行
python scripts/setup_transcribe.py
```
- 幂等：ffmpeg / whisper 已存在则跳过下载，只补标记与自检。
- 跨平台：自动识别 win32 / linux / darwin，下载对应 BtbN 静态包。

### 转录命令（已固化镜像与 ffmpeg 路径）
```bash
# 自动走 hf-mirror 镜像下载模型，自动把 ffmpeg 加入 PATH
python scripts/transcribe.py <视频/音频文件> --model small --lang zh --out transcribe_out
```
- 产物：`<out>` 目录下生成 .srt / .txt / .vtt / .json（output_format=all），交给 Skill 阶段 1。
- 模型首次运行自动下载（已固化 `HF_ENDPOINT=https://hf-mirror.com`）；本机已缓存则秒过。
- 手动等价命令（仅参考，推荐用上面的脚本）：
```bash
# 抽音频
ffmpeg -i input.mp4 -vn -ar 16000 -ac 1 output.wav
# whisper 识别（需 pip install openai-whisper）
whisper output.wav --model base --language zh
```

## 三、转录后处理
- 去口头禅、补全标点、按句断行，输出可编辑文稿。
- 标注「识别置信度未知」，关键信息请用户复核。
- 把转录稿作为阶段 1 的 `text` 输入继续拆解。
