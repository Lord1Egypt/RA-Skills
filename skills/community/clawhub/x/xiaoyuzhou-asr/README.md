# xiaoyuzhou-asr

小宇宙播客本地转录 Skill，适配 Claude Code / OpenClaw。通过兼容的 xyz API 服务获取节目元数据和音频 URL，使用 Qwen3-ASR 在本地完成语音识别，音频不会上传到外部服务。

> **重要前提**：小宇宙搜索、登录、单集详情和音频 URL 获取都依赖正在运行的 [ultrazg/xyz](https://github.com/ultrazg/xyz.git) 兼容 API 服务。默认地址是 `http://localhost:23020`，可用 `XYZ_BASE_URL` 指向其他地址；如果没有安装并启动该服务，小宇宙转录流程无法使用。

## 安装

**方式一** 直接告诉 Claude Code / OpenClaw：

```
安装这个 skill https://github.com/worldwonderer/xiaoyuzhou-asr
```

**方式二** 命令行：

```bash
# Claude Code
cp -r xiaoyuzhou-asr ~/.claude/skills/xiaoyuzhou-asr

# OpenClaw
npx skills add worldwonderer/xiaoyuzhou-asr -y
```

## 使用

安装后对 Claude 说：

- 「转录这集小宇宙播客 https://...」
- 「搜索早咖啡最新一期并转录」
- 「把这个单集 ID 转成文字」

自然语言即可触发，不需要记命令。

也可以直接运行脚本：

```bash
# 检查环境是否就绪
python3 scripts/transcribe_podcast.py --check-env --token YOUR_TOKEN

# 按小宇宙单集链接转录
python3 scripts/transcribe_podcast.py \
  --token YOUR_TOKEN --url "https://www.xiaoyuzhoufm.com/episode/EPISODE_ID" -o output.md

# 按关键词搜索并转录第一个结果
python3 scripts/transcribe_podcast.py \
  --token YOUR_TOKEN --keyword "早咖啡" -o output.md
```

脚本也可以被同目录脚本复用（这不是打包发布的 Python library；推荐直接用 CLI）：

```python
from transcribe_podcast import search_episodes, run_transcription

episodes, _ = search_episodes(token, "早咖啡")
# 所有异常使用 TranscriptionError 体系，不会 sys.exit
```

## Skill 组成

| 文件 | 说明 |
|:-----|:-----|
| `SKILL.md` | Skill 入口，定义触发条件和工作流 |
| `scripts/transcribe_podcast.py` | 全流程脚本：搜索 → 下载 → 转换 → 分割 → 转录 → 输出 |
| `scripts/batch_transcribe.py` | 批量发现并转录播客单集的辅助脚本 |
| `references/xyz-api.md` | xyz API 端点、认证、响应格式参考 |
| `references/qwen3-asr.md` | Qwen3-ASR 模型使用、音频要求、长音频处理参考 |

## 依赖

| 依赖 | 用途 | 安装 |
|:-----|:-----|:-----|
| [ultrazg/xyz](https://github.com/ultrazg/xyz.git) | 小宇宙 API 服务（需 +86 手机号登录） | `git clone` → `go run .` |
| [Qwen3-ASR-0.6B](https://huggingface.co/Qwen/Qwen3-ASR-0.6B) | 语音识别模型（约 1.8GB） | `huggingface_hub.snapshot_download` |
| [qwen3-asr-rs](https://github.com/alan890104/qwen3-asr-rs) | Rust ASR 推理引擎 | `cargo build --release --example local_transcribe` |
| ffmpeg | 音频格式转换 | `brew install ffmpeg` |

详细安装步骤见 [references/qwen3-asr.md](references/qwen3-asr.md)。

## 输出格式

| Format | 参数 | 说明 |
|:-------|:-----|:-----|
| Markdown | `--format markdown`（默认） | 元数据标题 + 转录文本 |
| SRT | `--format srt` | 字幕文件，按分段时间估算句子时间戳 |
| TXT | `--format txt` | 简洁标题 + 转录文本 |
| JSON | `--format json` | 元数据和转录文本 JSON |

## 配置

常用环境变量：

| 变量 | 说明 | 默认值 |
|:-----|:-----|:-------|
| `XYZ_BASE_URL` | xyz API 服务地址 | `http://localhost:23020` |
| `XYZ_ACCESS_TOKEN` | 小宇宙 access token | — |
| `XYZ_REFRESH_TOKEN` | 自动刷新 token 用 | — |
| `XYZ_HTTP_TIMEOUT` | xyz API 请求超时秒数 | `15` |
| `XYZ_DOWNLOAD_TIMEOUT` | 音频下载超时秒数 | `120` |
| `QWEN3_ASR_MODEL_DIR` | Qwen3-ASR 模型目录 | 自动探测 |
| `QWEN3_ASR_BIN` | `local_transcribe` 路径 | 自动探测 |

## 平台支持

| 平台 | GPU 加速 | 备注 |
|:-----|:---------|:-----|
| Apple Silicon (M1/M2/M3/M4) | Metal | 音频超过 3 分钟会挂起，脚本自动分割为 ≤180s 片段 |
| NVIDIA (CUDA) | CUDA | 无时长限制 |

## 转录效果

以下是一期 11 分钟的中文播客（声动早咖啡）的实际转录结果，未经人工修改：

<details>
<summary>展开查看完整转录</summary>

```markdown
# 美军在对伊空袭中使用 AI 工具，泡泡玛特起诉 3D 打印公司拓竹科技

**节目**: 声动早咖啡
**日期**: 2026-03-02
**时长**: 11分14秒
**播放量**: 186,128

---

## 转录文本

用声音碰撞世界，生动活泼。嗨，我是早咖啡的兼职泽林，我们节目组正在寻找新伙伴。如果你对商业世界好奇，也喜欢声音这个媒介，欢迎去单击介绍里点招聘入口看看。那我们接下来就进入今天的节目吧。生动早咖啡与你轻松同步日常生活与商业世界。嗨，各位早上好呀，今天是二零二六年的三月三号，星期二。这里是生动早咖啡，我是来自生动活泼的梦一。美军在军事活动中是如何使用AI工具的？小米为什么不会量产自己的超跑概念车？泡泡玛特为什么起诉了三D打印公司拓竹科技？今天的早咖啡，我们将会为你带来这些问题的答案。海湾地区经济活动遭受冲击。根据路透社三月一号的报道，在美国和以色列对伊朗发动袭击之后，伊朗实施报复性攻击，波及了大部分海湾地区国家。当地的经济活动正在遭遇自新冠疫情以来最严重的冲击...
```

</details>

```markdown
# 美军在对伊空袭中使用 AI 工具，泡泡玛特起诉 3D 打印公司拓竹科技

**节目**: 声动早咖啡
**日期**: 2026-03-02
**时长**: 11分14秒
**播放量**: 186,128

---

## 转录文本

美军在军事活动中是如何使用AI工具的？小米为什么不会量产自己的
超跑概念车？泡泡玛特为什么起诉了三D打印公司拓竹科技？今天的
早咖啡，我们将会为你带来这些问题的答案。海湾地区经济活动遭受
冲击。根据路透社三月一号的报道，在美国和以色列对伊朗发动袭击
之后，伊朗实施报复性攻击，波及了大部分海湾地区国家。当地的经济
活动正在遭遇自新冠疫情以来最严重的冲击，机场被迫关闭，港口停运，
金融市场剧烈震荡...
```

## 致谢

- [ultrazg/xyz](https://github.com/ultrazg/xyz.git) — 感谢该项目提供小宇宙 FM 非官方 API 能力，本 skill 通过运行兼容的 xyz API 服务获取节目元数据和音频 URL
- [qwen3-asr-rs](https://github.com/alan890104/qwen3-asr-rs) — Qwen3 ASR Rust 推理引擎（candle 框架）
