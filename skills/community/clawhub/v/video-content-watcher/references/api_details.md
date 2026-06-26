# Video Reader - Technical Reference

## Project Structure

```
video-reader/               # MCP project
├── src/
│   ├── __init__.py         # Main entry, VideoReaderMCP class
│   ├── config.py           # Config management (dotenv loading)
│   ├── extractor/
│   │   └── audio_extractor.py  # yt-dlp / ffmpeg audio extraction
│   ├── transcription/
│   │   └── whisper_client.py   # Whisper API or local transcription
│   ├── analyzer/
│   │   └── llm_analyzer.py     # MiniMax / OpenAI LLM analysis
│   └── output/
│       └── report_generator.py # Markdown report generation
├── .env                     # Env vars (gitignored, no real keys)
├── .env.example             # Template for collaborators
├── requirements.txt
└── temp/                    # Audio extraction temp files
```

## API Details

### MiniMax LLM (used for analysis)

- **Endpoint**: `https://api.minimaxi.com/v1` (or custom `LLM_BASE_URL`)
- **Model**: `MiniMax-M2.7` (default), `MiniMax-Text-01` also supported
- **Auth**: Bearer token via `MINIMAX_API_KEY`

### Whisper Transcription

- **Local mode** (default): uses `openai-whisper` package, downloads model (~139MB base)
- **API mode**: uses OpenAI Whisper API, requires `WHISPER_API_KEY`

## Config Priority

1. Constructor arguments (if provided)
2. Environment variables
3. `.env` file (non-sensitive defaults only)
4. Hardcoded defaults in `config.py`

## VideoReaderMCP Methods

```python
# Full pipeline: extract → transcribe → analyze → report
mcp.process_url(video_url)           # Online video
mcp.process_file("/path/to/file.mp4") # Local file

# Partial pipelines
mcp.transcribe_only(source, is_url=True)  # Transcription only
mcp.analyze_text(text)                    # Analyze raw text

# Result dict keys
result = mcp.process_url(url)
result["source_url"]           # Original URL
result["audio_path"]           # Temp audio file path
result["transcription"]        # Raw transcript text
result["transcription_length"] # Character count
result["analysis"]             # LLM raw output (dict)
result["report"]               # Formatted Markdown report
```

## Error Handling

- `WHISPER_API_KEY is required when WHISPER_MODE=api` → set env var or pass to constructor
- `MINIMAX_API_KEY is required` → set env var
- `ffmpeg not found` → install ffmpeg system package
- `No module named 'video_reader_mcp'` → ensure `src/` is in `PYTHONPATH`
