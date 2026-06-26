# Voice Chat Bridge - 设计文档

## 目标
把多渠道语音消息统一桥接成：
**语音输入 → 本地/远程转写 → LLM 对话 → 可选 TTS 回传**

## 当前已完成
- ✅ Sherpa-ONNX（首选）+ Vosk（备份）双引擎 STT
- ✅ 自动 fallback 机制：Sherpa-ONNX 失败时自动切换 Vosk
- ✅ 中英文混合识别优化
- ✅ `transcribe_audio.py` 可处理 `.ogg/opus` 音频
- ✅ 飞书语音样本已验证可转写
- ✅ 支持 Telegram 语音下载与回传
- ✅ Edge TTS 失败自动降级到 `pyttsx3`

## 版本历程

### v1.0 - 最小可用版
- **输入**：手动提供音频文件路径
- **处理**：ffmpeg 转 16k 单声道 wav → vosk 本地模型转写
- **输出**：标准输出文本

### v1.1 - 飞书集成
- 接入飞书语音消息路径
- 自动触发转写
- 输出文字答复

### v1.2 - 完整闭环
- 接入 TTS 工具
- 自动语音回复
- 增加开关：只回文字 / 只回语音 / 双回
- 配置集中化（pydantic + dotenv）
- 提取通用校验与依赖检查（utils）

### v2.3.5 - Sherpa-ONNX 归一化修复（代码同步）
- **修复**：修正 Sherpa-ONNX 样本归一化问题（使用 numpy 缩放到 [-1, 1]）
- **修复**：关闭 use_itn 避免富文本标记干扰
- **修复**：将正确的代码同步到项目源代码目录
- **修复前**：模型听到"静音"，输出 ". ."
- **修复后**：正确识别语音内容

### v2.3.4 - Sherpa-ONNX 归一化修复
- **修复**：修正 Sherpa-ONNX API 调用方式（使用 `from_sense_voice` 类方法）
- **修复**：修正音频处理流程（先转换为 16kHz WAV，再使用 `accept_waveform`）
- **修复**：修正 Sherpa-ONNX 模型名称和下载方式

### v2.3.2 - 双引擎升级（Sherpa-ONNX）
- **新增**：Sherpa-ONNX 引擎（首选，中英文混合识别）
- **新增**：自动 fallback 机制（Sherpa-ONNX 失败时切换 Vosk）
- **新增**：引擎策略配置（sherpa/vosk/auto）
- **优化**：中英文混合识别准确率
- **优化**：内存占用（使用 onnxruntime，约 1GB）
- **兼容**：保持 Vosk 作为备份方案
- **修复**：修正 Sherpa-ONNX 模型名称和下载方式

## 渠道支持现状
| 渠道 | 状态 | 说明 |
|------|------|------|
| Feishu | ✅ 已完成 | 下载/转写/回复/TTS/OGG 输出闭环 |
| Telegram | ✅ 已完成 | Bot API 下载 voice → STT → 模板回复 → TTS → sendVoice 回传 |
| Discord | 🚧 规划中 | |
| WeChat / openclaw-weixin | 🚧 规划中 | |

## STT 引擎对比

### Sherpa-ONNX（首选）
- **优势**：
  - 原生支持中英文混合识别
  - 识别准确率优于 Vosk
  - 轻量级，只依赖 onnxruntime（几十MB）
  - int8 量化模型，内存占用小（600-800MB）
  - 无 CUDA/NVIDIA 依赖，适合 termux 环境
- **劣势**：
  - 需要下载模型文件（~200MB）
  - 首次加载较慢

### Vosk（备份）
- **优势**：
  - 轻量级，模型文件小（~40MB）
  - 纯 Python 实现，部署简单
  - 离线运行，无网络依赖
- **劣势**：
  - 中英文混合识别效果一般
  - 需要语言切换
  - 准确率低于 Sherpa-ONNX

### Fallback 策略
```python
# 策略 1: 仅使用 Sherpa-ONNX
transcribe(audio, engine="sherpa")

# 策略 2: 仅使用 Vosk
transcribe(audio, engine="vosk")

# 策略 3: 自动 fallback（推荐）
transcribe(audio, engine="auto")  # Sherpa-ONNX 失败时自动切换 Vosk
```

## 当前依赖
- `ffmpeg`：音频格式转换
- `sherpa-onnx`：Sherpa-ONNX 引擎（首选）
- `vosk`：Vosk 引擎（备份）
- Python 环境（默认取当前解释器，可由 `VOSK_PYTHON` 覆盖）
- `edge-tts` 可执行文件（默认从 PATH 查找，可由 `EDGE_TTS_BIN` 覆盖）
- `/tmp/sherpa-model/sherpa-onnx-sense-voice-zh-en-ja-ko-small-with-hotwords`（Sherpa-ONNX 模型目录）
- `/tmp/vosk-model/vosk-model-small-cn-0.22`（Vosk 模型目录，可由 `VOSK_MODEL_DIR` 覆盖）

## 配置说明

### 环境变量
| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| `STT_ENGINE` | `sherpa` | STT 引擎策略（sherpa/vosk/auto） |
| `SHERPA_MODEL_DIR` | `/tmp/sherpa-model` | Sherpa-ONNX 模型目录 |
| `SHERPA_MODEL_NAME` | `sherpa-onnx-sense-voice-zh-en-ja-ko-yue-2024-07-17` | Sherpa-ONNX 模型名称 |
| `SHERPA_NUM_THREADS` | `4` | Sherpa-ONNX 线程数 |
| `VOSK_PYTHON` | `sys.executable` | Vosk 使用的 Python 解释器 |
| `VOSK_MODEL_DIR` | `/tmp/vosk-model/vosk-model-small-cn-0.22` | Vosk 模型目录 |
| `EDGE_TTS_BIN` | `edge-tts` | Edge TTS 可执行文件路径 |
| `DEFAULT_VOICE` | `zh-CN-YunxiNeural` | TTS 默认音色 |

## 注意事项
- Sherpa-ONNX 模型需要手动下载（参考 README.md）
- Vosk 模型需要手动下载（参考 README.md）
- 所有处理必须在**当前会话**中执行，**严禁新开子会话**
- termux 环境下，Sherpa-ONNX 使用 CPU 推理（无 GPU 加速）
- 音频格式必须是 16kHz 单声道 WAV（如果不是，用 ffmpeg 转换）
