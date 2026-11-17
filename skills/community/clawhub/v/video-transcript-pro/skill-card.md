## Description:

Automatically transcribes video and audio, refines transcripts, and generates publishing drafts for Zhihu, WeChat, and Xiaohongshu.

This skill is ready for commercial/non-commercial use.

## Publisher:

[artminding](https://clawhub.ai/user/artminding)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, marketers, and agents working with Chinese-language audio or video use this skill to create timestamped transcripts, edited transcripts, and platform-ready publishing drafts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may automatically enrich content through web search and persist user preferences without clear opt-in or deletion controls.

Mitigation: Use with non-sensitive media, disable web enrichment and MEMORY.md preference storage for sensitive work, and review generated notes before reuse.

Risk: Local audio and video inputs can be summarized into transcript and progress files that may contain confidential content.

Mitigation: Run the skill in an isolated workspace, treat generated files as sensitive, and delete transcripts and progress files when they are no longer needed.

Risk: The transcription workflow depends on local Python packages and a reviewed faster-whisper installation.

Mitigation: Install dependencies in an isolated environment with pinned, reviewed package versions before processing production content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/artminding/skills/video-transcript-pro)
- [Whisper open-source project](https://github.com/openai/whisper)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance, files]

**Output Format:** [Timestamped text transcripts and Markdown publishing drafts with inline command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write transcript, edited transcript, platform draft, partial progress, and preference memory files in the working environment.]

## Skill Version(s):

2.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
