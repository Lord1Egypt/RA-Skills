# ASR Model Selection Guide

## Available Models

| Model | RAM | Disk | Speed | Quality | Best For |
|-------|-----|------|-------|---------|----------|
| `small` | ~2GB | 461MB | Fast (~1min/6min audio) | Good | Quick tests, low-resource systems |
| `medium` | ~5GB | 1.42GB | Medium (~3-5min) | High | **Recommended default** - best quality/speed ratio |
| `large-v3` | ~10GB | 2.88GB | Slow (~10-20min) | Best | Production quality, needs high RAM |
| `large-v3-turbo` | ~6GB | 1.6GB | Medium-fast | High | Good compromise, smaller than large-v3 |

## Language-Specific Notes

### Chinese (zh)
- `medium`: Good for general Chinese content. Some errors on homophones and financial terms.
- `large-v3`: Best Chinese accuracy, handles accents and domain terminology better.
- Common errors: 同音字混淆 (硬扛→硬钢), 金融术语 (抛压→抛押, 交筹→焦愁), K线术语 (十字星→14星)

### English (en)
- `small`: Sufficient for clear English speech.
- `medium`: Excellent accuracy for most content.

## Memory Constraints

On Windows, `large-v3` may be killed (SIGKILL) on systems with <16GB RAM due to FP32 fallback.
If killed, fall back to `medium` or use `larger-v3-turbo`.

## Future Model Compatibility

The `transcribe.py` script is designed for easy backend extension:
- `faster-whisper`: CTranslate2 backend, more memory efficient
- `whisper.cpp`: Native C++ implementation
- `mlx-whisper`: Apple Silicon optimized
- Cloud APIs: AssemblyAI, iFlytek, Whisper API

To add a new backend, implement a `transcribe_<backend>()` function in transcribe.py
following the same interface (audio_path, model_name, language, output_dir).

## Model Auto-Download

Models are downloaded automatically by openai-whisper on first use.
Cache location:
- Windows: `C:\Users\<user>\.cache\whisper\`
- macOS: `~/Library/Caches/whisper/`
- Linux: `~/.cache/whisper/`