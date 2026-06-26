# Error Handling

| Error | Action |
|-------|--------|
| Modal run failed (auth error) | Run `modal setup` to re-authenticate |
| Modal run failed (other) | Paste Modal error output verbatim to user |
| No audio files found in upload | Report "no audio files found" and list which files were skipped |
| Volume put failed (permission) | Verify Modal token is still valid: `modal token new` |
