# qwen-asr — 离线中文语音识别（纯 C 实现）

使用 [antirez/qwen-asr](https://github.com/antirez/qwen-asr) 的 `qwen3-asr-0.6b` 模型进行中文语音转文字，**无 Python/GIL/FFmpeg 依赖**，适合边缘部署。

---

## 依赖

| 平台 | 依赖项 | 说明 |
|------|--------|------|
| macOS | Accelerate.framework | 系统自带，自动链接 |
| Linux | OpenBLAS 或 Intel MKL | 需手动安装 |

---

## 典型用法

```bash
# 转写音频（自动预处理为 16kHz/mono/WAV）
.skill qwen-asr --audio /path/to/audio.wav

# 指定模型（small=0.6B, large=1.7B）
.skill qwen-asr --audio /path/to/audio.wav --model large

# 指定线程数
.skill qwen-asr --audio /path/to/audio.wav --threads 4
```

---

## 输出

```text
[中文] 现在已经可以用了吗？
```

支持中/英文混读（模型训练语料含双语）。

---

## 模型大小

| 模型 | 大小 | 推荐场景 |
|------|------|----------|
| `qwen3-asr-0.6b` | ~1.7GB | 推荐：低延迟、边缘设备 |
| `qwen3-asr-1.7b` | ~4.5GB | 高精度（需 ≥4GB 内存） |

---

## 注意事项

- 音频必须为 **16kHz/mono/16-bit PCM WAV**（脚本会自动转换非合规音频）
- 首次运行会下载模型（~1.7GB），后续无需重复下载
- 仅支持 `.ogg`/`.mp3`/`.wav`→`.wav` 预处理（FFmpeg 内置支持）
- 推理为**纯离线**，无需网络（模型下载阶段除外）

---

## 作者

- GitHub: [@antirez](https://github.com/antirez)
- 技能封装: OpenClaw Agent

---

## 许可

MIT（qwen-asr）+ 阿里云 Qwen3 ASR Model License
