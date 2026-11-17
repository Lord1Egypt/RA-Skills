## Description:

Create short-form vertical video packages, preview reels, narrated reels, and AI-video workflows from ideas, articles, updates, or source material.

This skill is ready for commercial/non-commercial use.

## Publisher:

[normandmickey](https://clawhub.ai/user/normandmickey)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, social media teams, and developers use Reelsmith to turn topics or source material into short-form reel packages with hooks, scripts, scene plans, captions, and optional preview, narration, or AI-video generation steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local preview helpers execute ffmpeg and may overwrite caller-selected output files.

Mitigation: Review commands before execution, choose output paths deliberately, and avoid reusing filenames for files that must be preserved.

Risk: Optional narration and AI-video helpers send prompt or narration text to third-party services.

Mitigation: Do not submit confidential or sensitive source material unless the receiving service is acceptable for the use case.

Risk: Repeated preview generation can leave temporary Reelsmith directories on disk.

Mitigation: Periodically clean old Reelsmith temporary directories after generating many previews.

## Reference(s):

- [Reelsmith ClawHub Skill Page](https://clawhub.ai/normandmickey/skills/reelsmith)
- [LTX Text-to-Video API](https://api.ltx.video/v1/text-to-video)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown with optional inline bash commands and generated MP4 or MP3 files from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional helper scripts use OPENAI_API_KEY, LTX_API_KEY, local ffmpeg execution, and caller-selected output paths.]

## Skill Version(s):

0.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
