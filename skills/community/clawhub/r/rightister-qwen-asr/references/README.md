# qwen-asr 参考资料

## 仓库 & 文档

- GitHub: [https://github.com/antirez/qwen-asr](https://github.com/antirez/qwen-asr)
- 模型: [Qwen3-ASR-0.6B](https://huggingface.co/antirez/qwen3-asr-0.6b) / [Qwen3-ASR-1.7B](https://huggingface.co/antirez/qwen3-asr-1.7b)

## 编译 & 依赖

### macOS (Apple Silicon / Intel)
```bash
make blas
```
自动链接 `-framework Accelerate`（OpenBLAS 替代方案：`make blas BLAS=-L/opt/homebrew/opt/openblas/lib -I/opt/homebrew/opt/openblas/include`）

### Linux (OpenBLAS)
```bash
# Ubuntu/Debian
sudo apt install libopenblas-dev

make blas BLAS=-lopenblas
```

## 模型格式

- 格式：`safetensors`（PyTorch 原生，兼容 C loader）
- 目录结构：
  ```
  qwen3-asr-0.6b/
  ├── config.json          # 模型配置 (vocab_size, hidden_dim, etc.)
  ├── model.safetensors    # 权重文件 (~1.7GB)
  └── vocab.json           # 分词表
  ```

## 音频规范

- 采样率：16000 Hz
- 声道：1 (mono)
- 位深：16-bit PCM
- 格式：WAV (RIFF)

## 使用命令

```bash
./qwen_asr -d <model_dir> -i <input.wav> [-t <threads>] [-S <seg_sec>] [-W <sil_sec>]
```

| 参数 | 含义 | 默认 |
|------|------|------|
| `-d` | 模型目录 | 必填 |
| `-i` | 输入 WAV | 必填 |
| `-t` | 线程数 | `sysconf(_SC_NPROCESSORS_ONLN)` |
| `-S` | 分段长度 (秒) | `0` (全音频) |
| `-W` | 切段静音阈值 (秒) | `0.5` |

## FFmpeg 预处理范例

```bash
# 非 WAV → 16kHz/mono/WAV
ffmpeg -y -i input.mp3 -ar 16000 -ac 1 -f wav output.wav

# 检查音频规格
ffprobe -v error -select_streams a:0 -show_entries stream=sample_rate,channels,codec_name -of default=nw=1 input.wav
```

## 性能参考 (Apple M2)

| 模型 | 推理时间 (3.6s 音频) | 内存峰值 |
|------|---------------------|----------|
| qwen3-asr-0.6b | ~1.2s | ~2.1GB |
| qwen3-asr-1.7b | ~2.8s | ~4.8GB |
