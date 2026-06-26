# Zhipu AI ASR Skill

Automatic Speech Recognition (ASR) using Zhipu AI (BigModel) GLM-ASR model. Transcribe Chinese audio files to text with high accuracy.

## Features

- 🎤 **Multiple Audio Formats**: WAV, MP3, OGG, M4A, AAC, FLAC, WMA
- 🇨🇳 **Chinese Language Support**: Optimized for Mandarin Chinese
- 📝 **Context Prompts**: Improve accuracy with previous transcription context
- 🔥 **Hotwords**: Custom vocabulary for specific terms (names, jargon, etc.)
- ⚡ **Fast Processing**: Real-time or faster transcription speed
- 🔄 **Auto Format Conversion**: Automatically converts unsupported formats to MP3

## Requirements

- `jq` - JSON processor
- `ffmpeg` - Audio format conversion
- `ZHIPU_API_KEY` environment variable

## Quick Start

```bash
# Install dependencies (if needed)
sudo apt-get install jq ffmpeg

# Set your API key
export ZHIPU_API_KEY="your-key-here"

# Transcribe an audio file
bash scripts/speech_to_text.sh recording.wav

# With context and hotwords
bash scripts/speech_to_text.sh recording.wav "previous context" "term1,term2,term3"
```

## File Constraints

- **Max file size**: 25 MB
- **Max duration**: 30 seconds
- **Supported formats**: WAV (recommended), MP3
- **Other formats**: Auto-converted to MP3

## Use Cases

- 🎙️ Meeting transcription
- 📚 Lecture recording
- 💼 Voice memos
- 🎞️ Video subtitle generation
- 📞 Call recording transcription

## Author

franklu0819-lang

## License

MIT
