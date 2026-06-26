# Error Handling

| Error | Action |
|-------|--------|
| Modal run failed (auth error) | Run `modal setup` to re-authenticate |
| Modal run failed (other) | Paste Modal error output verbatim to user |
| No audio files found in upload | Report "no audio files found" and list which files were skipped |
| Volume put failed (permission) | Verify Modal token is still valid: `modal token new` |
| Model download failed (HF) | Set `HF_TOKEN` environment variable for higher rate limits. Run `export HF_TOKEN=your_token` before modal run |
| Model not found (local cache miss) | Run with `--model tiny` first to download smaller model, or ensure volume is mounted correctly |
