---
name: tts-qwen3
version: 1.0.0
description: "Qwen3-TTS 本地语音合成。支持音色克隆、声音设计、多角色对话。琪琪OPC首选TTS，失败回退到 tts-cosyvoice (Edge TTS)。"
metadata:
  openclaw:
    emoji: 🎤
    priority: high
    category: audio
    tags: [tts, qwen3, voice-clone, voice-design, qiqi-opc]
---

# Qwen3-TTS 本地语音合成

> 基于 Qwen3-TTS 1.7B 模型，支持音色克隆 + 声音设计 + 多角色对话。
> **琪琪OPC 首选 TTS**，失败时回退到 tts-cosyvoice (Edge TTS)。

## 优先级

```
Qwen3-TTS（本地GPU，音色克隆+设计）→ Edge TTS（tts-cosyvoice，云端回退）
```

## 琪琪OPC 音色库

6 个角色音色，通过 ComfyUI API 调用：

| 角色 | 音色名 | 方式 | 说明 | 用途 |
|------|--------|------|------|------|
| 🐰 琪琪 | qiqi_clone | 克隆 | ref_audio=qiqi_voice_v3.wav | 琪琪对话 |
| 📖 旁白 | narrator_teacher | VoiceDesign | seed=100, 温暖女声 | 叙事 |
| 👦 男孩 | boy_child | VoiceDesign | seed=200, 活泼8岁 | 儿童男角 |
| 👧 女孩 | girl_child | VoiceDesign | seed=300, 甜美7岁 | 儿童女角 |
| 👨 大人男 | adult_male | VoiceDesign | seed=400, 沉稳 | 成年男角 |
| 👩 大人女 | adult_female | VoiceDesign | seed=500, 优雅 | 成年女角 |

## 脚本

### 单角色 TTS

```bash
python3 {baseDir}/scripts/qwen_tts.py \
  --text "你好，我是琪琪" \
  --voice qiqi_clone \
  --output /tmp/output.wav
```

### 多角色对话 TTS

```bash
python3 {baseDir}/scripts/qwen_tts_dialogue.py \
  --script "琪琪:你好呀！\n旁白:琪琪开心地笑了。" \
  --output /tmp/dialogue.wav \
  --srt /tmp/dialogue.srt
```

### 选项

| 选项 | 默认 | 说明 |
|------|------|------|
| `--text` | (必需) | 要合成的文本 |
| `--voice` | narrator_teacher | 音色名（见音色库） |
| `--output` | /tmp/qwen_tts_output.wav | 输出文件路径 |
| `--language` | Chinese | 语言 |
| `--model` | 1.7B | 模型大小 (0.6B/1.7B) |
| `--attention` | sdpa | 注意力机制 |
| `--fallback-edge` | true | 失败时回退到 Edge TTS |

## 对话脚本格式

```
角色名: 台词内容
角色名: 台词内容
```

角色名映射到音色库中的音色。`旁白` 映射到 `narrator_teacher`。

## 依赖

- ComfyUI 运行中（localhost:8188）
- ComfyUI-Qwen-TTS 插件已安装
- Qwen3-TTS 模型已下载（~/ComfyUI/models/qwen-tts/）
- comfyui-venv Python 环境

## 回退策略

当 Qwen3-TTS 不可用时（ComfyUI 未启动 / GPU 显存不足 / 生成失败），
自动回退到 Edge TTS (tts-cosyvoice)：
- 琪琪 → zh-CN-XiaoyiNeural
- 旁白 → zh-CN-XiaoxiaoNeural
- 男孩 → zh-CN-YunxiNeural
- 女孩 → zh-CN-XiaoyiNeural
- 大人男 → zh-CN-YunjianNeural
- 大人女 → zh-CN-XiaoxiaoNeural

---

*版本: v1.0 | 琪琪OPC 首选 TTS | 基于 Qwen3-TTS + ComfyUI*
