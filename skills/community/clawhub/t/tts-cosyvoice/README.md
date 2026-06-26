# TTS/ASR 语音模型部署指南

## 当前部署状态

| 组件 | 方案 | 状态 | 说明 |
|------|------|------|------|
| **TTS** | Edge TTS | ✅ 已部署 | 微软免费云端 TTS，无需 API Key |
| **ASR** | Whisper | ⏳ 待装 | pip install openai-whisper 依赖较多，国内网络慢 |

## TTS — Edge TTS

### 优势
- **零依赖**：只需 `edge-tts` Python 包（已装好）
- **免费**：无需 API Key，使用 Microsoft Edge 内置 TTS
- **高质量**：Neural 级别语音，中文自然度顶级
- **多语言**：50+ 语言，100+ 音色
- **轻量**：纯 Python，不占显存

### 中文推荐音色
| 音色 | 性别 | 风格 |
|------|------|------|
| `zh-CN-XiaoxiaoNeural` | 女 | 温暖自然（默认） |
| `zh-CN-YunxiNeural` | 男 | 年轻 casual |
| `zh-CN-YunyangNeural` | 男 | 新闻播报 |
| `zh-CN-XiaoyiNeural` | 女 | 可爱年轻 |

### 使用示例
```bash
~/.openclaw/plugin-skills/tts-cosyvoice/scripts/tts.py \
  --text "你好，我是Nova" \
  --output /tmp/hello.mp3
```

### 备选：CosyVoice（本地 TTS）
如果需要完全离线的 TTS：
```bash
pip install cosyvoice
# 从 ModelScope 下载模型
python -c "
from modelscope.hub.snapshot_download import snapshot_download
snapshot_download('iic/CosyVoice-300M-SFT', local_dir='./cosyvoice-models/sft')
"
```

## ASR — Whisper

### 当前状态
- `pip install openai-whisper` 依赖较多（torch_complex, kaldiio, librosa 等）
- 国内网络下载较慢
- 模型权重首次使用自动下载（base ~150MB）

### 安装（网络恢复后执行）
```bash
pip install openai-whisper
# 测试
python -c "import whisper; model = whisper.load_model('base'); print('OK')"
```

### 使用示例
```bash
~/.openclaw/plugin-skills/asr-funasr/scripts/asr.py \
  --input meeting.mp3 \
  --language zh \
  --model base
```

### 备选：FunASR SenseVoice（更快更准的中文 ASR）
如果 Whisper 安装困难：
```bash
pip install funasr modelscope
# 从 ModelScope 下载模型
python -c "
from funasr import AutoModel
model = AutoModel(model='iic/SenseVoiceSmall', trust_remote_code=True, device='cuda:0')
result = model.generate(input='test.wav')
print(result)
"
```

## 显存预算

| 场景 | ComfyUI | TTS | ASR | 总计 |
|------|---------|-----|-----|------|
| 图片生成 | 14GB | 0 | 0 | 14GB ✅ |
| 视频生成 | 13GB | 0 | 0 | 13GB ✅ |
| TTS | 0 | 0（云端） | 0 | 0 ✅ |
| ASR | 0 | 0 | 1-2GB | 1-2GB ✅ |
| TTS+ASR+ComfyUI | 13GB | 0 | 2GB | 15GB ✅ |

**Edge TTS 不占显存**（云端 API），ASR 仅 1-2GB（base 模型）。

## 与 keynote-video 集成

keynote-video 技能流程：
```
PPT → 内容理解（LLM）→ 讲稿生成 → TTS 语音合成 → 视频合成 → 音画合并
                                          ↑ Edge TTS
```

## OpenClaw 技能

| 技能 | 位置 | 功能 |
|------|------|------|
| tts-cosyvoice | ~/.openclaw/plugin-skills/tts-cosyvoice/ | 文字转语音 |
| asr-funasr | ~/.openclaw/plugin-skills/asr-funasr/ | 语音转文字 |
