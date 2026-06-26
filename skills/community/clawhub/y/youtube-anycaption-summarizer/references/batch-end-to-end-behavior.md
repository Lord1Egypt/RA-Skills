# Batch End-to-End Behavior

Use this reference when handling multiple YouTube URLs in one request and the user expects fully finished outputs, not just extracted transcripts.

## Goal
For batch mode, process each video to completion when possible:
1. extract transcript artifacts
2. backfill language if needed
3. write the final polished summary
4. run completion/finalization
5. capture the final result block

## Processing model
- For multi-video runs, first create a plain-text batch file and invoke `run_youtube_batch_end_to_end.py --batch-file <path>`.
- Process videos sequentially.
- Treat each video as an independent unit of work.
- Prefer finishing one video completely before moving to the next.
- Do not block the whole batch on one failing video.

## Retry policy
- If a video fails at any phase, record the failure reason and continue with the next video.
- After the first pass, retry failed videos.
- Maximum attempts per video: 3 total.
- If a video still fails after 3 attempts, mark it as failed and include the final failure reason in the batch result.

## Required successful item fields
Every successful item in the final batch result must include:
- title
- video_id
- raw_transcript
- summary
- summary_language
- transcript_source
- postprocess_complete
- end_to_end_total_seconds
- attempts
- session_report

## Required failed item fields
Every failed item in the final batch result must include:
- url
- video_id if known
- attempts
- phase
- error

## Final batch result contract
Return a final machine-readable result containing:
- queue_mode
- count
- success_count
- failure_count
- results (successful items)
- failures (failed items)

## Notes
- The low-level workflow script may still create placeholder summaries as an intermediate step.
- Batch end-to-end completion is only achieved when the placeholder is overwritten and completion succeeds for that video.
- If a completion report exists, use its `end_to_end_total_seconds` for the successful item.