# Transcription Guide

## How It Works

This transcription skill uses the OpenAI Whisper API endpoint running locally at `http://192.168.0.11:8080/v1`. The endpoint handles:

- **Audio extraction** from video files (ffmpeg)
- **Language auto-detection** or explicit language specification
- **High-quality transcription** using whisper-small model
- **Timestamp extraction** for word-level timing

## File Processing Flow

```
User sends file → Skill detects type → Extract audio if video → Send to Whisper API → Return transcript
```

## Best Practices

1. **Clear audio**: Minimize background noise for better results
2. **Language hint**: If auto-detection fails, specify the language code (e.g., `--language es`)
3. **File size**: Keep files under 25MB for best performance
4. **Batch processing**: Send files one at a time or use the batch flag

## Common Use Cases

- **Meeting recordings**: "Transcribe this meeting"
- **Video content**: "Extract audio from this video"
- **Language learning**: "Transcribe with timestamps for practice"
- **Content creation**: Get text from audio for captions/summaries

## Troubleshooting

- **Endpoint unreachable**: Check that the Whisper service is running on `192.168.0.11`
- **Poor transcription quality**: Try specifying the language explicitly
- **Video not working**: Ensure ffmpeg is installed (handled automatically)

---

For technical details, see the Python scripts in `scripts/`.