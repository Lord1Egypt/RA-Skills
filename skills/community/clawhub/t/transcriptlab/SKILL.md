---
name: transcriptlab
description: Use when the user wants a YouTube transcript, a transcript of an audio or video file, caption languages for a video, a search inside a transcript, their TranscriptLab credit balance, or to revisit a transcript they pulled before.
---

# TranscriptLab

The TranscriptLab tools fetch YouTube captions and transcribe audio or video with speech-to-text.
Results land in the user's TranscriptLab library and are metered in credits.

## Route the request

| The user gives you | Call |
| --- | --- |
| a YouTube link or video ID | `transcriptlab_get_transcript` |
| an audio or video file attached to the conversation | `transcriptlab_transcribe_file` |
| a direct link to a media file (.mp3, .mp4, .webm, and similar) | `transcriptlab_transcribe_media_url` |
| a question about which subtitle languages exist | `transcriptlab_discover_captions` |
| a phrase to find inside a transcript already delivered | `transcriptlab_search_transcript` |
| a request to reopen or list earlier transcripts | `transcriptlab_list_transcripts` |
| a question about their plan, credits, or usage | `transcriptlab_get_usage` |
| a file to download, a download link, or "save it as SRT/VTT/TXT" | `transcriptlab_export_link` |
| no link or file yet, or several links at once | `transcriptlab_open` (if the host renders MCP App views) or ask for the link |

`transcriptlab_get_transcript` may answer with a pending job: check it with
`transcriptlab_get_job_status` and read it with `transcriptlab_retrieve_transcript` once done.
`transcriptlab_transcribe_file` and `transcriptlab_transcribe_media_url` return an id to poll with
`transcriptlab_get_speech_transcript` — a few seconds between tries, stop after about ten.

When the user wants the transcript as a file, call `transcriptlab_export_link` and give them the
returned URL as a link, saying it expires in 10 minutes. This host cannot start a download by
itself, so the link is how the file reaches them; it needs a signed-in connection and fails with an
explicit message if the connection used an API key instead.

The view tools (`transcriptlab_open`, `transcriptlab_open_audio`) render an interactive launcher in
hosts that support MCP App resources; elsewhere the core tools do the same work. App-facing tools —
`transcriptlab_mentions`, `transcriptlab_begin_audio_upload`,
`transcriptlab_start_audio_transcription`, `transcriptlab_read_audio_transcript`,
`transcriptlab_submit_batch`, `transcriptlab_list_job_items` — belong to those views; never call
them.

## How to behave

- Answer with the transcript. Never invent text, a title, a timestamp, or a caption language. If a
  tool returns nothing, say so in one sentence and offer the next option.
- Talk about their content, not the plumbing. Do not name tools, describe the connection or the
  transcription engine, or explain views. Do not offer install, setup, or troubleshooting detail
  unless something has actually failed.
- Poll quietly. Wait between checks, back off, and stop after about ten tries; then report that the
  job is still running. Do not narrate each attempt.
- Mention that a first transcript may use a credit only when it affects their choice. Otherwise stay
  quiet about it.
- Captions are not transcription. If a YouTube video has no captions, say so plainly and offer
  speech-to-text when they can attach the file or give a direct media link. Never imply the audio
  was transcribed when it was not.

## If something fails

- An authentication error or reconnect prompt: ask them to reconnect the connector once, then
  retry. This plugin authenticates over OAuth; the consent flow on transcriptlab.dev completes in
  one click for signed-in users.
- Out of credits, or the monthly caption-discovery limit: state the limit and stop. Do not retry.
- A job that never finishes: give the job id and its last status instead of continuing to poll.
