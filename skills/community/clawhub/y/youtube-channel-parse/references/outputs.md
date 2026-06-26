# Outputs

Write outputs under a directory named from `output_prefix`.

Use clear subdirectories for inventories, filtered datasets, transcripts, and reports.

## Recommended Structure

```text
output/<output_prefix>/
  inventory/
  filtered/
  transcripts/
  reports/
```

## Inventory Outputs

Write channel inventories as:

- `inventory/<output_prefix>_channel.json`
- `inventory/<output_prefix>_channel.md` when the user wants a human-readable channel inventory

## Filtered Dataset Outputs

Write filtered datasets as:

- `filtered/<output_prefix>_videos.json`
- `filtered/<output_prefix>_videos.transcripts.json` for the transcript-enriched intermediate dataset
- `filtered/<output_prefix>_videos.final.json` for the final filtered dataset after transcript-aware report processing
- `filtered/<output_prefix>_videos.csv`
- `filtered/<output_prefix>_videos.md` when the user wants a human-readable list or notes

## Transcript Outputs

Write one transcript file per video:

- `transcripts/<video_id>.txt`

Add per-video markdown notes when requested:

- `transcripts/<video_id>.md`

## Report Outputs

Write synthesized findings as markdown:

- `reports/<output_prefix>_report.md`

Write filtered-set notes as markdown when the task calls for them:

- `reports/<output_prefix>_notes.md`
