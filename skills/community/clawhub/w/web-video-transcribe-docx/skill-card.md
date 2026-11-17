## Description:

Offline-first workflow for turning Chinese web page video or audio into text and Word deliverables.

This skill is ready for commercial/non-commercial use.

## Publisher:

[c-narcissus](https://clawhub.ai/user/c-narcissus)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content-processing agents use this skill to extract user-supplied or locally available Chinese web and media audio, run local ASR, preserve raw transcripts, and export TXT or DOCX deliverables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bootstrap workflow installs unpinned runtime packages.

Mitigation: Use an isolated virtual environment and pin, review, or mirror dependencies before installation in sensitive environments.

Risk: The ASR model can be downloaded and extracted from a remote release without strong integrity checks.

Mitigation: Prefer a preverified local model directory, or verify the downloaded archive before allowing extraction and transcription.

Risk: The media extraction workflow can preserve reusable media URLs and Referer or Origin context in media_info.json.

Mitigation: Treat media_info.json as private, restrict sharing, and redact or delete it when it is no longer needed.

Risk: The skill can download user-supplied or page-extracted media URLs.

Mitigation: Use it only for URLs the user supplied or that the extractor captured from the target page, and do not use it to bypass DRM, login walls, geo-restrictions, cookies, or credential requirements.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/c-narcissus/skills/web-video-transcribe-docx)
- [Workflow](references/workflow.md)
- [Cleanup Guidelines](references/cleanup-guidelines.md)
- [sherpa-onnx ASR model releases](https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands; generated local TXT, DOCX, JSON manifest, and downloaded media files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves raw transcript files separately from cleaned or chapterized reading copies.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter metadata reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
