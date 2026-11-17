## Description:

Downloads videos from supported platforms, transcribes local audio, and can combine transcript text with extracted video frames for visual understanding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kk-kingkong](https://clawhub.ai/user/kk-kingkong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to download or process video URLs, generate transcripts, query transcript segments, and produce combined audio-visual summaries for supported platforms and local video files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad URL triggers can cause video URLs, transcripts, and extracted frames to be processed before the user has clearly confirmed the data flow.

Mitigation: Use the skill only with videos intended for processing, avoid private or tokenized URLs, and add an explicit consent step before remote processing.

Risk: Remote services may receive video data or derived transcript and frame content without clear provider and retention details.

Mitigation: Document all processing providers and retention behavior, and prefer isolated execution with pinned dependencies or a verified release.

Risk: Referenced implementation files or dependencies may be missing, unpinned, or change independently of the skill text.

Mitigation: Ship or pin referenced implementation files and dependencies before deployment, then review and scan the release before installation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kk-kingkong/skills/video-download-transcribe)
- [openclaw-media](https://github.com/openclaw/openclaw-media)
- [Playwright npm mirror](https://npmmirror.com/mirrors/playwright)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, JSON examples, and transcript or analysis text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return transcript identifiers for long-running background transcription and may produce timestamped transcript segments or combined text-and-frame analysis.]

## Skill Version(s):

3.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
