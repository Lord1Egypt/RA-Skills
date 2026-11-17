## Description:

Transcribes tables and event logs from video by matching cells to visible row boundaries and checking results against source frames.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ciklopentan](https://clawhub.ai/user/ciklopentan)

### License/Terms of Use:

MIT-0

## Use Case:

Engineers and analysts transcribe tables from recorded SCADA screens and device logs, preserve source-frame evidence, and compare visible event records across videos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided videos may expose sensitive industrial or account information.

Mitigation: Process authorized media locally and use external OCR services only with explicit permission.

Risk: Blurred, clipped, or overlapping rows can produce incorrect transcriptions or misleading comparisons.

Mitigation: Review cells against source frames, mark uncertainty, and limit comparisons to the visible interval.

## Reference(s):

- [Video Table Transcriber GPT release](https://clawhub.ai/ciklopentan/skills/video-table-transcriber-gpt)
- [Geometry and verifiable data](references/geometry-and-data.md)
- [Review and comparison](references/review-and-comparison.md)
- [Method sources](references/method-sources.md)
- [Tesseract image quality guidance](https://tesseract-ocr.github.io/tessdoc/ImproveQuality.html)
- [OpenCV line-detection tutorial](https://docs.opencv.org/4.x/dd/dd7/tutorial_morph_lines_detection.html)
- [FFmpeg documentation](https://ffmpeg.org/ffmpeg.html)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Guidance]

**Output Format:** [Markdown tables and structured JSON evidence records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Source-frame references, field review statuses, and explicit uncertainty for unreadable content.]

## Skill Version(s):

1.0.0 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
