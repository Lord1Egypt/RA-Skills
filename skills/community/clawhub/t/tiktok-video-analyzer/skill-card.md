## Description:

Analyze videos from TikTok, YouTube, Instagram, Twitter/X, and other supported sites by downloading audio, transcribing it locally, and answering questions about the content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[holl4ndtv](https://clawhub.ai/user/holl4ndtv)

### License/Terms of Use:


## Use Case:

OpenClaw users and developers use this skill to turn social and video URLs into local transcripts and concise answers, including summaries, extracted teaching points, hooks, and follow-up questions against saved transcripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may download online media and model files, then store transcripts locally in ways users may not expect.

Mitigation: Run it only after review in a dedicated environment and avoid sensitive videos unless local storage behavior is acceptable.

Risk: Unsafe save and ID handling could affect local transcript files or commands when used with untrusted videos or local files.

Mitigation: Fix the save workflow, validate transcript IDs and paths, and review generated commands before execution.

Risk: System-level dependency installation can modify the user's Python environment.

Mitigation: Install dependencies in a virtual environment, container, or other isolated runtime instead of system Python.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/holl4ndtv/skills/tiktok-video-analyzer)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown answers with inline shell commands and optional JSON transcript data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May download online media, create local transcript files, and reuse cached transcripts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
