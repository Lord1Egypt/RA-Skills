---
name: voxcpm
description: VoxCPM2 — Tokenizer-Free TTS model guide. Covers installation, Python/CLI API (TTS/Voice Design/Controllable Cloning/Ultimate Cloning/Streaming), vLLM-Omni deployment, fine-tuning (SFT/LoRA). Use when synthesizing speech, multilingual TTS, voice cloning/design.
---

# VoxCPM2 — Tokenizer-Free Multilingual TTS

A tokenizer-free TTS from OpenBMB based on a diffusion autoregressive architecture. **2B** parameters, trained on 2M+ hours, **30 languages**, 48kHz output, built on MiniCPM-4.

Architecture: `LocEnc → TSLM → RALM → LocDiT`, AudioVAE V2 asymmetric 16kHz→48kHz.

## Installation

```bash
pip install voxcpm  # Python ≥3.10, PyTorch ≥2.5, CUDA ≥12
model = VoxCPM.from_pretrained("openbmb/VoxCPM2", device="auto")  # cuda→mps→cpu
# torch.compile issues: optimize=False; HF mirror: export HF_ENDPOINT=https://hf-mirror.com
```

## Models

| | V2 (2B) | 1.5 (0.8B) | 0.5B |
|--|:--:|:--:|:--:|
| Sample Rate | 48kHz | 44.1kHz | 16kHz |
| Languages | 30 | 2(zh/en) | 2(zh/en) |
| Voice Design | ✅ | — | — |
| VRAM/RTF | ~8GB/~0.30 | ~6GB/~0.15 | ~5GB/~0.17 |

30 languages: Chinese, English, Japanese, Korean, French, German, Spanish, Italian, Russian, Arabic, Hindi, Thai, Vietnamese, Turkish, Dutch, Finnish, Norwegian, Swedish, Danish, Polish, Portuguese, Greek, Hebrew, Indonesian, Malay, Burmese, Khmer, Lao, Swahili, Tagalog + 9 Chinese dialects (Sichuan, Cantonese, Wu, Northeastern, Henan, Shaanxi, Shandong, Tianjin, Minnan)

## Python API

```python
from voxcpm import VoxCPM; import soundfile as sf
model = VoxCPM.from_pretrained("openbmb/VoxCPM2", load_denoiser=False)

# Basic TTS
sf.write("out.wav", model.generate("Hello!", cfg_value=2.0, inference_timesteps=10), model.tts_model.sample_rate)

# Voice Design (text description → voice, no reference audio needed)
wav = model.generate("(A young woman, gentle voice)Hello!")

# Controllable Cloning (reference audio + style control)
wav = model.generate("Hello.", reference_wav_path="voice.wav")
wav = model.generate("(faster, cheerful)Hi.", reference_wav_path="voice.wav")

# Ultimate Cloning (reference audio + transcript for full detail reproduction)
wav = model.generate("Text.", prompt_wav_path="ref.wav", prompt_text="transcript", reference_wav_path="ref.wav")

# Streaming
import numpy as np
wav = np.concatenate([c for c in model.generate_streaming("Streaming!")])
```

`generate()` params: `text`(required) `reference_wav_path` `prompt_wav_path` `prompt_text` `cfg_value=2.0`(1-3) `inference_timesteps=10`(4-30) `normalize=False` `denoise=False` `retry_badcase=True`

## CLI

```bash
voxcpm design --text "Hello" --control "Young female warm voice" --output out.wav --device auto
voxcpm clone --text "Hi" --reference-audio voice.wav --prompt-audio ref.wav --prompt-text "txt" --output out.wav
voxcpm batch --input examples/input.txt --output-dir outs
```

## Web Demo

```bash
git clone https://github.com/OpenBMB/VoxCPM.git && cd VoxCPM && pip install -e .
python app.py --port 8808 --device auto
```

## Deployment

### vLLM-Omni (recommended, OpenAI-compatible)
```bash
uv pip install vllm==0.19.0 --torch-backend=auto
git clone https://github.com/vllm-project/vllm-omni.git && cd vllm-omni && uv pip install -e .
vllm serve openbmb/VoxCPM2 --omni --port 8000
curl http://localhost:8000/v1/audio/speech -H "Content-Type:application/json" -d '{"model":"openbmb/VoxCPM2","input":"Hello!","voice":"default"}' --output out.wav
```
Nano-vLLM: `pip install nano-vllm-voxcpm` (RTF ~0.13 vs standard ~0.30)

## Fine-tuning

```bash
# LoRA (recommended)
python scripts/train_voxcpm_finetune.py --config_path conf/voxcpm_v2/voxcpm_finetune_lora.yaml
# Full fine-tuning
python scripts/train_voxcpm_finetune.py --config_path conf/voxcpm_v2/voxcpm_finetune_all.yaml
# WebUI
python lora_ft_webui.py  # http://localhost:7860
```

Data format JSONL: `{"audio":"path","text":"transcript","ref_audio":"path"}` (recommend 30-50% samples with ref_audio). LoRA params `r=32` `alpha=16`, hot-swappable (`load_lora`/`unload_lora`/`set_lora_enabled`). Adapt to a speaker with as little as 5-10 minutes of audio.

## License

Apache 2.0 — free for commercial use