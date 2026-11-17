---
name: tuneviva-scan-sheet-music
description: Guide a user through recognising printed sheet music from photos or a PDF in TuneViva, reviewing the notation and opening the result for practice. Use for browser-based sheet music recognition, not audio transcription.
---

# Recognise sheet music in TuneViva

Open https://tuneviva.com/recognize. Recognition runs in the user's browser; there is no public recognition API. This skill describes the browser workflow, not an image-processing service an agent can call. If browser interaction is unavailable, give the user the link and the relevant steps rather than claiming to process their image.

## Choose the source

Use a clear, evenly lit photo of printed notation with complete staves, minimal perspective distortion and no fingers or dark borders over the music. Choose one PDF or several photos with the “Choose photos or PDF” control, or drop them into the upload area. “Take photo” is available on supported mobile devices; camera behavior depends on the browser. The current limits are 50 MB per file, 100 MB total and 100 pages per PDF.

Selecting files starts recognition automatically. The first run downloads the recognition engine and models; leave the tab open while it processes. Sheet images are processed locally rather than uploaded for recognition. Do not send the user's score to an unrelated service as part of this workflow.

For an existing `.xml`, `.musicxml` or `.mxl` score, skip recognition: open https://tuneviva.com/learn/ and choose “Open MusicXML”.

## Review the result

Compare the recognised notation with the original, especially clefs, key and time signatures, accidentals, rhythms and staff grouping. Review any measures the page flags. Optical recognition can make mistakes; a completed scan is not proof of an accurate transcription. Play the result to help spot errors, but do not describe playback as an independent accuracy check.

If the result is poor, suggest a better crop or clearer photo. Avoid repeatedly processing the same input without a change. If notation still needs correction, download MusicXML and edit it in a notation editor; TuneViva does not expose a server-side editing API.

## Practise or save

Use the result's “Practise” action to open the recognised score. This uses temporary browser-session storage. Keep the same tab/session; the resulting local practice URL is not a public share link and will not reproduce the score on another device.

Use “More” to download MusicXML or PDF when the user wants to keep the result. MusicXML preserves editable notation. Retain the original source for comparison and its attribution/licensing information.

In practice, the user can tap highlighted piano keys, use a compatible MIDI instrument or enable the microphone. Device access requires the user's permission. Microphone matching is experimental; do not promise precise feedback for every instrument or recording environment.
