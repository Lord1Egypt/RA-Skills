## Description:

Turn YouTube videos into dependable markdown transcripts and polished summaries, using manual captions, auto-captions, or local Whisper fallback when caption coverage is missing or inconsistent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arthurli202602-commits](https://clawhub.ai/user/arthurli202602-commits)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and operators use this skill to turn one or more YouTube videos, including private or caption-poor videos, into reusable transcript and summary artifacts for analysis, documentation, and batch research workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private-video cookie support can expose account credentials.

Mitigation: Use cookie support only when necessary, prefer an explicit cookies.txt file over browser extraction, and handle cookie files as credentials.

Risk: Transcript text and video metadata may be sent to the configured OpenClaw model.

Mitigation: Avoid confidential private videos unless that data path is approved, or use an approved local or controlled model configuration.

Risk: Untrusted video metadata can be forwarded back into agent sessions and logs.

Mitigation: Disable or patch automatic progress forwarding in sensitive sessions and redact session identifiers from logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/arthurli202602-commits/skills/youtube-anycaption-summarizer)
- [Source homepage](https://github.com/arthurli202602-commits/youtube-anycaption-summarizer)
- [Detailed workflow](references/detailed-workflow.md)
- [Batch input format](references/batch-input-format.md)
- [Batch end-to-end behavior](references/batch-end-to-end-behavior.md)
- [Summary template](references/summary-template.md)
- [Session output template](references/session-output-template.md)
- [Default Whisper model download](https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-medium.bin)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown files plus session-ready markdown or JSON status blocks with shell commands for workflow execution]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates per-video raw transcript and polished summary files; batch mode reports successful outputs and failed-video reasons.]

## Skill Version(s):

1.1.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
