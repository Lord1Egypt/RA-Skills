# Batch Input Format

Use a plain text file with one YouTube URL per line.

This is the required input format for multi-video runs. If you have more than one URL, create this batch file first, then invoke the batch runner with `--batch-file`. Do not pass multiple positional URLs directly to `run_youtube_batch_end_to_end.py`.

Example:

```text
https://www.youtube.com/watch?v=RX-fQTW2To8
https://www.youtube.com/watch?v=657wlbtrzG8
```

Canonical invocation:

```bash
python3 scripts/run_youtube_batch_end_to_end.py --batch-file ./youtube-urls.txt
```

## Rules
- Ignore blank lines.
- Ignore lines starting with `#`.
- Process URLs sequentially in file order.
- Create one dedicated subfolder per video under the chosen parent output folder.
- Treat each item as an independent workflow run with its own transcript, summary placeholder, and cleanup step.

## Per-item workflow in batch mode
For each URL, the main workflow should:
1. fetch metadata
2. derive sanitized output paths
3. try subtitle-first extraction
4. fall back to media download + Whisper transcription when needed
5. write the raw transcript markdown
6. write the summary placeholder markdown
7. clean intermediates unless explicitly told to keep them

After deterministic processing, summarize each item sequentially and run the finalizer script for each finished summary.

## Failure handling
- By default, a failure stops the batch.
- With `--continue-on-error`, record the failure and continue with later URLs.
- Report both successes and failures clearly at the end.
