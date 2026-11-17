# Video Downloader Enhanced

一个面向本地 AI Agent 的视频下载、素材归档与语音转写 Skill，也可以脱离 Agent，直接作为命令行工具运行。

本项目基于 [`kangarooking/kangarooking-skills`](https://github.com/kangarooking/kangarooking-skills) 中的 `video-downloader` 修改和扩展。只要 Agent 能读取项目说明、访问本地文件并运行 Shell / Python 命令，就可以调用这套工作流。不同产品的 Skill 目录、自动发现机制和权限模型并不相同，因此脚本本身是通用的，安装方式需要以各 Agent 的规则为准。

## 功能

输入一个公开视频链接后，本项目可以：

1. 识别视频平台；
2. 获取原始发布标题、正文和话题标签；
3. 下载视频，并在支持的下载路线中验证文件有效性；
4. 使用 FFmpeg 提取音频；
5. 使用本地或云端 ASR 进行语音转写；
6. 生成纯文本转写稿、字幕和结构化元数据。

当前已实现：

- 抖音
- 小红书
- Bilibili
- YouTube

微信视频号链接目前只能识别，尚未实现直接下载。请先通过你有权使用的方式将视频保存到本地，再进行后续处理。

## 输出内容

每个视频会生成一个独立目录，命名格式为：

```text
YY_MM_DD_标题摘要_平台_作者
```

目录中可能包含：

```text
视频文件.mp4
post_caption.txt
audio.wav / audio.m4a / audio.mp3
transcript.txt
transcript.srt
transcript.whisper_cpp.json
transcript.whisper.json
transcript.siliconflow.json
metadata.json
```

- `post_caption.txt`：平台发布标题、正文和话题标签；
- `audio.*`：从视频中提取的音频；
- `transcript.txt`：纯文本语音转写；
- `transcript.srt`：带时间轴的字幕，由 whisper.cpp 或 openai-whisper 后端生成；
- `transcript.*.json`：所用 ASR 后端的结果或运行信息；
- `metadata.json`：平台、作者、链接、时长、分辨率、下载方式和 ASR 状态。

## 主要改进

相较上游 `video-downloader`，本版本主要增加或调整了：

- 支持 whisper.cpp；
- 默认 ASR 优先级为 `whisper.cpp → openai-whisper → SiliconFlow`；
- 通过环境变量配置 whisper.cpp 命令与模型路径；
- 支持 `xhslink.cn` 小红书短链接；
- 小红书匿名 `yt-dlp` 失败后尝试公开媒体直链；
- 将 Chrome Cookie 作为最后一级下载回退；
- 使用 `ffprobe` 校验小红书下载文件是否包含真实视频流；
- 在 `metadata.json` 中记录下载路线、Cookie 使用情况、校验结果和回退错误；
- 使用便于人工管理的输出目录名称。

## 工作原理

```text
视频链接
   ↓
平台 Provider
   ↓
yt-dlp / 平台专用下载路线
   ↓
视频有效性校验
   ↓
FFmpeg 提取音频
   ↓
whisper.cpp / openai-whisper / SiliconFlow
   ↓
视频、发布文案、转写稿、字幕与元数据
```

## 系统要求

- Python 3.10+
- [`yt-dlp`](https://github.com/yt-dlp/yt-dlp)
- [FFmpeg](https://ffmpeg.org/)（包括 `ffmpeg` 和 `ffprobe`）

语音转写至少配置一种后端：

- [whisper.cpp](https://github.com/ggml-org/whisper.cpp)，推荐本地使用；
- [openai-whisper](https://github.com/openai/whisper)，可选本地后端；
- [SiliconFlow](https://siliconflow.cn/) API，可选云端后端。

本项目不会自动安装或升级系统工具。

## 安装

克隆仓库并进入 Skill 目录：

```bash
git clone <repository-url>
cd video-downloader-enhanced
```

作为 Agent Skill 使用时，将整个目录放入目标 Agent 支持的 Skills 目录，或在项目规则中要求 Agent 先读取本仓库的 `SKILL.md`。请查阅你所使用产品的当前文档，不要假设不同 Agent 的安装目录和授权行为完全一致。

也可以不安装为 Skill，直接运行命令行入口：

```bash
python3 scripts/download_video.py --help
```

## whisper.cpp 配置

脚本优先使用 `WHISPER_CPP_BIN` 指定的可执行文件；未设置时，从 `PATH` 查找 `whisper-cli`：

```bash
export WHISPER_CPP_BIN="/path/to/whisper-cli"
export WHISPER_CPP_MODEL="/path/to/ggml-large-v3-turbo.bin"
```

`WHISPER_CPP_MODEL` 必须指向本机已有的 GGML 模型文件。项目不假设任何平台专属默认路径，也不会自动安装软件。请勿把个人绝对路径或模型文件提交到公开仓库。

## 命令行使用

下载并自动选择可用 ASR 后端：

```bash
python3 scripts/download_video.py \
  "https://v.douyin.com/..." \
  --output-dir "./downloads"
```

指定 whisper.cpp：

```bash
python3 scripts/download_video.py \
  "https://v.douyin.com/..." \
  --output-dir "./downloads" \
  --asr whisper_cpp \
  --asr-language Chinese
```

只下载，不提取音频或转写：

```bash
python3 scripts/download_video.py \
  "https://v.douyin.com/..." \
  --output-dir "./downloads" \
  --asr none
```

只获取元数据和发布文案：

```bash
python3 scripts/download_video.py \
  "https://v.douyin.com/..." \
  --output-dir "./downloads" \
  --metadata-only
```

使用 SiliconFlow：

```bash
export SILICONFLOW_API_KEY="your-api-key"

python3 scripts/download_video.py \
  "https://v.douyin.com/..." \
  --output-dir "./downloads" \
  --asr siliconflow \
  --asr-language Chinese
```

API Key 只从环境变量读取。不要将真实密钥写进命令示例、代码、`.env` 或 Git 提交记录。

## 在 AI Agent 中使用

可以直接告诉本地 Agent：

```text
请先阅读 video-downloader-enhanced/SKILL.md，
然后用 scripts/download_video.py 下载并转写这个视频：
<视频链接>
```

推荐在 Agent 的项目规则中提前约定：

- 默认输出目录；
- 是否启用 ASR；
- 默认 ASR 后端和语言；
- whisper.cpp 模型路径；
- 是否允许读取浏览器 Cookie；
- 是否允许安装或升级系统工具。

## Cookie 与隐私

部分平台无法完全匿名下载。对应 Provider 可能在公开路线失败后调用：

```text
yt-dlp --cookies-from-browser chrome
```

这会读取本机 Chrome Cookie；在 macOS 上还可能触发钥匙串授权。项目不会生成 `cookies.txt`，也不会主动将 Cookie 内容写入输出文件，但下载命令本身仍会访问浏览器凭证。

在运行前请确认：

- 你理解并授权本次浏览器 Cookie 访问；
- 不把 Cookie 数据库、`cookies.txt` 或浏览器配置复制进仓库；
- 远程或无人值守环境中设置 `VIDEO_DOWNLOADER_REMOTE=1`，使小红书 Provider 在需要 Cookie 时直接报告；
- 只下载你拥有、获准下载或依法可以保存的内容。

## 发布前安全检查

仓库已提供 `.gitignore`，用于排除：

- 下载的视频、音频、发布文案、转写稿和元数据；
- `.env`、Cookie 导出文件和浏览器 Cookie 数据库；
- `.DS_Store`、`__pycache__`、`*.pyc`；
- `*.bak*` 备份、日志和临时文件。

`.gitignore` 只能阻止未跟踪文件被新增，不能清除已经提交的文件或 Git 历史。发布前仍应检查暂存区与历史记录，并确认没有真实 API Key、Cookie、私人笔记或个人绝对路径。

## 当前限制

- 微信视频号暂不支持直接下载；
- 平台页面结构或 `yt-dlp` 行为变化可能导致 Provider 暂时失效；
- 私密、付费、地区限制或登录后可见内容可能需要额外认证；
- 目前只对小红书下载执行额外的最小文件大小与 `ffprobe` 视频流校验；
- 本 Skill 不包含完整的逐帧视觉理解、OCR 或画面内容分析；
- 下载能力不代表拥有内容版权或再分发权限。

## 致谢与许可

本项目基于 [`kangarooking/kangarooking-skills`](https://github.com/kangarooking/kangarooking-skills) 中的 `video-downloader` 修改和扩展。上游仓库 README 声明：除各 Skill 另有说明外，其原创内容按 MIT License 开源。

本项目按 [MIT License](LICENSE) 发布。详细上游来源和主要修改说明见 [NOTICE](NOTICE)。再发布或修改本项目时，请保留许可证和来源说明。
