---
name: song-cover-en
version: 2.0.0
description: 把一首中文歌做成英文翻唱成品：抓歌词 → 可唱英文填词 → RMVPE 提真实旋律 → 神经歌声合成（SoulX-Singer）→ 频谱匹配/颤音后处理 → 混音 → ComfyUI 配图 + 律动背景 + 逐词歌词视频。Use when the user wants an English cover of a Chinese song, a singable translation of lyrics, sung vocals from text, a lyric video with a reactive audio background, or asks for 英文翻唱 / 中文歌翻英文 / AI 唱歌 / 歌词视频 / 频谱背景视频.
metadata:
  openclaw:
    emoji: 🎤
    os: [win32, linux, darwin]
    requires:
      bins: [python, ffmpeg]
---

# Chinese-to-English Song Cover (v2)

把中文歌做成英文翻唱：抓歌词 → 可唱英文填词 → RMVPE 提真实旋律 → SoulX-Singer 神经歌声合成 → 频谱匹配/颤音后处理 → 混音 → ComfyUI 配图 + 律动背景 + 逐词歌词视频。

> **这是一次个人尝试，不是生产级方案。** 完整的踩坑记录、8 轮迭代、耗时/Token/工具统计和已知缺陷都写在
> [`RELEASE_NOTES.md`](RELEASE_NOTES.md) 里。音色仍与真人演唱有差距，欢迎来一起调——
> 尤其缺的是「保留原唱音色只换歌词」的方案、更好的频谱补偿和更地道的英文填词。

## 前置条件

- **GPU**: NVIDIA ≥ 6GB VRAM（SoulX-Singer fp16 约 1.4GB，可与 ComfyUI 共存）
- **Python**: 3.12，且装好 torch + CUDA（推荐直接用 ComfyUI 的 venv）。其余依赖放
  `$SONG_COVER_HOME/libs/`：librosa, soundfile, numpy, scipy, soxr, cmudict, pyloudnorm,
  imageio-ffmpeg, onnxruntime, transformers **4.41.x**, omegaconf, einops, pypinyin, requests
  - transformers 必须 4.41.x（SoulX 的 `LlamaConfig(0,256,1024,1,1)` 用位置参数，5.x 不兼容）
  - torchaudio 手写 shim 在 `libs/torchaudio/`（SoulX 只用 4 个 API）
- **模型权重**（约 3.3GB，需自行下载，仓库不附带）：
  - SoulX-Singer 代码 → `cache/soulx_src/SoulX-Singer-main/`，权重 → `cache/soulx/model.pt` + `config.yaml`
  - RMVPE → `cache/rmvpe/rmvpe.onnx`（362MB）
  - Whisper-base → `cache/whisper-base/`（ASR 质检，需 16kHz 输入）
  - UVR MDX-Net → `cache/UVR-MDX-NET-Voc_FT.onnx`
- **ComfyUI**（可选，只做配图）: `http://127.0.0.1:8188`，**只支持 1152x648 或 1024x576**，1344x768 会 VAE 解码失败
- **ffmpeg**: 优先用 `imageio_ffmpeg.get_ffmpeg_exe()`，找不到时退回 `PATH` 里的 `ffmpeg`

### 路径约定（可移植）

所有运行期文件都在一个根目录下，脚本里没有任何作者机器路径：

```
$SONG_COVER_HOME/            # 默认 ~/.song-cover-en，也可指向旧目录
├── libs/                    # python 依赖（会插到 sys.path）
├── cache/                   # 模型权重、下载缓存
├── runs/<song>/NN/          # 每首歌每一步的产物
└── workspace/               # 临时文件
```

| 环境变量 | 作用 | 默认 |
|---|---|---|
| `SONG_COVER_HOME` | 总根目录 | `~/.song-cover-en` |
| `SONG_COVER_LIBS` / `_CACHE` / `_RUNS` | 单独覆盖某个子目录 | `<HOME>/libs` 等 |
| `SONG_COVER_REF_HUMAN` | 频谱匹配用的真人英文干声 | `<HOME>/smoke_out/_ref_human.wav` |
| `SONG_COVER_FONT_EN` / `_EN_R` / `_CN` | 视频字体（Windows 自带 Georgia/微软雅黑，其他系统会自动找 DejaVu/Noto） | 自动探测 |

`scripts/_env.py` 负责解析这些路径，其余脚本都从它 import。

## 快速开始

```bash
# 1) 抓歌词 + 下载原曲/伴奏，并对齐到同一条时间线
python scripts/01_lyrics.py --run-dir "$SONG_COVER_HOME/runs/mysong" --song-id <网易云ID>
python scripts/02_audio.py  --run-dir "$SONG_COVER_HOME/runs/mysong" --orig-bv BV... --inst-bv BV...

# 2) 人声分离 + 提旋律
python scripts/03_separate.py --run-dir .../mysong
python scripts/04_melody.py   --run-dir .../mysong

# 3) 按 assets/en_lyrics.json 的格式写好英文词，再对齐、合成、后处理
python scripts/05_align.py    --run-dir .../mysong
python scripts/06_svs.py      --run-dir .../mysong --seed 42 --chunk-s 22
python scripts/spectral_match.py --run-dir .../mysong --ref "$SONG_COVER_REF_HUMAN"
python scripts/add_vibrato.py --run-dir .../mysong
python scripts/mix_song.py    --run-dir .../mysong --vocal-over 1.5

# 4) 配图 + 成片（需要本地 ComfyUI）
python scripts/07_art.py      --out .../mysong/07/art
python scripts/08_video.py    --run-dir .../mysong
```

## 管线

```
01_lyrics.py → 02_audio.py → 03_separate.py → 04_melody.py
  ↓ (人工/LLM 写英文歌词)
05_align.py → 06_svs.py → spectral_match.py → add_vibrato.py → mix_song.py
  ↓
07_art.py (ComfyUI 配图) → 08_video.py (成片)
```

每步输出到 `<run-dir>/NN/`。

## 各步骤关键要点

### 01_lyrics.py — 抓歌词
- `--song-id <网易云ID>`（不是 `--id`）
- **LRC 时间戳不可靠**（逐行抖动 ±6s），后续对齐不能信 `next_t`

### 02_audio.py — 下载伴奏与原曲
- 必须 `$env:PYTHONIOENCODING='utf-8'`
- 输出 22050Hz 单声道；两条音轨用 chroma 互相关求出偏移，再补静音对齐到同一条时间线

### 03_separate.py — 人声分离
- UVR MDX-Net ONNX，设计采样率 **44100Hz**
- **坑**: 喂 22050Hz 会把内容当低八度处理，人声被带限到约 1kHz

### 04_melody.py — RMVPE 音高提取
- **前端标定**: `ln`（自然对数）+ `htk=True` + `norm='slaney'`，`CONF_TH=0.10`
  - 错误前端（如 dB 变换）会让 confidence 崩塌
- 去颤音: `detrend_vibrato(midi, fps, win_s=0.20)`
- 吸收碎片: `absorb_shards(notes, min_sung=0.12)`（短音符并入邻音符，绝不丢弃）

### 05_align.py — DP 单调对齐
- `align_lines_to_notes(notes, need)` 动态规划，行边界严格连续不漂移
- `need[i]` = max(汉字数, 英文音节数)
- `build_segment` 构造 SoulX 元数据，`word_start` 由 `word_id` 推导
- prompt 选音区匹配句（音符中位音高与全曲中位最近者）

### 06_svs.py — SoulX-Singer 歌声合成
- **`--seed 42`**（必须！扩散从随机噪声起步）
- `--chunk-s 22`（分块渲染，代价超线性增长）
- **不加 `--auto-shift`**（逐段移调不同量，与原调失调）
- `torch.manual_seed(a.seed + ci)` 在每次 `model.infer` 前

### spectral_match.py — 频谱匹配（消除"机器音"）
- 零相位 LTAS 匹配到真人参考
- `--strength 1.0 --max-boost 18`：mid(1-3kHz) 从 10%→27.6%（真人 39.8%）
- 参考干声用 `SONG_COVER_REF_HUMAN` 或 `--ref` 指定，没有参考就不要跑这一步

### add_vibrato.py — 颤音增强
- 分数延迟颤音，`--rate 5.4 --depth 20 --onset 0.18 --fade 0.22`

### mix_song.py — 混音
- `--vocal-over 1.5`，`limit()` 软限幅（不像 tanh 弯曲波形）

### 07_art.py — ComfyUI 配图
- 9 场景，**1152x648**（1344x768 会 VAE 解码失败）
- 需要同目录下的 `comfy_client.py` 和一个跑着 Z-Image-Turbo 的 ComfyUI

### 08_video.py — 歌词视频
- 场景映射用 `SCENE_BY_TEXT` 按歌词原文（不能用行号，副歌重复会错位）
- 歌词时间用真实拟合词时间（不用 LRC 时间戳）
- 逐词高亮用 `word_start` 标志

## 质检（qa_sing.py）
- **RMVPE 假设 16kHz 输入**，必须 `soxr.resample(y, sr, 16000)`（否则音高偏低 7.02 半音）
- 音符落点: `median |err|` < 0.2 st，`corr` > 0.95
- ASR 词召回 > 80%

## 已知限制
- 音色非 100% 原唱（声码器 1-3kHz 只有真人约 1/8，频谱匹配后约 2/3）
- SoulX-Singer SVC 模式只换音色不换发音，不能"保留原唱只换歌词"
- 颤音深度约为真人的 60%
- 模型权重、ComfyUI 都不在包里，第一次跑要先自己搭环境

## 开发记录与致谢

- 开发时间：2026-11-06 22:35 → 2026-11-07 13:00，约 **14.5 小时**
- **8 轮重大迭代**（v1 CPU/WORLD → v2 SoulX-Singer → 频谱匹配 → 固定 seed）
- 累计约 **3 亿 tokens**（约 ¥100 API 费用，模型 `deepseek-v4.1-flash`），工具调用：PowerShell 100+、Python 50+、ComfyUI 9
- 完整记录见 [`RELEASE_NOTES.md`](RELEASE_NOTES.md)：踩坑清单、每轮指标、诚实声明与求助方向

**这只是一次尝试，个人能力有限。** 希望有更多大佬加入调试完善：音色克隆、频谱补偿、
更地道的英文填词、更精确的音符-音节映射。demo 成品在 [`demo/`](demo/)。

## 详细参考
- `references/pipeline-v2.md` — 管线技术文档与踩坑记录
- `references/model-contracts.md` — SoulX/RMVPE/Whisper 模型契约
- `references/lyrics-guide.md` — 英文填词规则与文化处理
- `scripts/probe_*.py`、`scripts/diag_*.py` — 开发期探针/诊断脚本，参数按需传，留作复现实验
