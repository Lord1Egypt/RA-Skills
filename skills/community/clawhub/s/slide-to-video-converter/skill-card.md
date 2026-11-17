## Description:

End-to-end pipeline for converting PPT/PPTX/PDF slides with speaker notes into narrated MP4 videos with audio validation, auto-synced subtitles, batch processing, and PPTX support via LibreOffice conversion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hzsunzixiang](https://clawhub.ai/user/hzsunzixiang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use this skill to automate production of narrated slide-based training, lecture, and presentation videos from PPT, PPTX, or PDF inputs plus per-slide speaker notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional HTTP TTS server may expose local file operations or expensive compute work if reachable by untrusted clients.

Mitigation: Bind the service to 127.0.0.1, avoid network exposure without authentication, and review the server before use.

Risk: Online Edge TTS can send presentation narration to an external service.

Mitigation: Use Edge TTS only for content approved for online processing, and use a local TTS mode for confidential presentations.

Risk: Unpinned dependencies and model revisions can make installs less repeatable.

Mitigation: Pin Python dependencies and model revisions before production or regulated use.

## Reference(s):

- [Speaker Notes Script Format](references/script-format.md)
- [ClawHub Skill Page](https://clawhub.ai/hzsunzixiang/skills/slide-to-video-converter)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, configuration notes, and generated video/audio file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces narrated MP4 videos, per-slide media files, subtitles, and logs through local scripts.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
