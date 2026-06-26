#!/usr/bin/env python3
"""
Qwen3-TTS 语音合成脚本
用法: python synthesize.py "要合成的文字" output.wav [speaker] [language] [model_path] [device]

示例:
  python synthesize.py "你好世界" output.wav
  python synthesize.py "Hello world" output.wav aiden English
  python synthesize.py "こんにちは" output.wav bella Japanese ./my-model cuda
"""
import sys
import os
import soundfile as sf

# 默认配置（可通过环境变量覆盖）
DEFAULT_MODEL_PATH = os.environ.get(
    "QWEN_TTS_MODEL_PATH",
    "./Qwen3-TTS-12Hz-1.7B-CustomVoice"
)
DEFAULT_DEVICE = os.environ.get(
    "QWEN_TTS_DEVICE",
    "mps"  # Apple Silicon: mps | NVIDIA: cuda | 通用: cpu
)

SPEAKERS = ["aiden", "bella", "chelsie", "ethan", "freya", "george", "holly", "iris", "james"]
LANGUAGES = ["Chinese", "English", "Japanese"]


def synthesize(text, output_path, speaker="aiden", language="Chinese",
               model_path=DEFAULT_MODEL_PATH, device=DEFAULT_DEVICE):
    from qwen_tts.inference.qwen3_tts_model import Qwen3TTSModel

    if speaker not in SPEAKERS:
        print(f"警告: 未知音色 '{speaker}'，使用默认值 'aiden'")
        print(f"可用音色: {', '.join(SPEAKERS)}")
        speaker = "aiden"

    print(f"加载模型: {model_path} (device={device})")
    model = Qwen3TTSModel.from_pretrained(model_path, device_map=device)

    print(f"合成中 [{speaker}/{language}]: {text[:50]}{'...' if len(text) > 50 else ''}")
    wavs, sample_rate = model.generate_custom_voice(
        text=text,
        speaker=speaker,
        language=language
    )

    sf.write(output_path, wavs[0], sample_rate)
    print(f"✓ 完成: {output_path}  ({sample_rate}Hz, {len(wavs[0])/sample_rate:.1f}s)")
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        print(f"可用音色: {', '.join(SPEAKERS)}")
        sys.exit(1)

    text       = sys.argv[1]
    output     = sys.argv[2]
    speaker    = sys.argv[3] if len(sys.argv) > 3 else "aiden"
    language   = sys.argv[4] if len(sys.argv) > 4 else "Chinese"
    model_path = sys.argv[5] if len(sys.argv) > 5 else DEFAULT_MODEL_PATH
    device     = sys.argv[6] if len(sys.argv) > 6 else DEFAULT_DEVICE

    synthesize(text, output, speaker, language, model_path, device)
