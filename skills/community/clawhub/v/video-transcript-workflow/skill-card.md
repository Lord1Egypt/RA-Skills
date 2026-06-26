## Description: <br>
Transcribes video or audio with faster-whisper, cleans and annotates the transcript, extracts key quotes, and drafts platform-specific Markdown for Zhihu, WeChat, and Xiaohongshu. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[artminding](https://clawhub.ai/user/artminding) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and content creators use this skill to turn Chinese video or audio recordings into timestamped transcripts, polished drafts, and platform-specific posts for publication review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local transcripts and generated drafts may contain confidential, regulated, unreleased, or personal information from recordings. <br>
Mitigation: Use the skill only with recordings appropriate to store locally, and review generated transcript and Markdown files before sharing or publishing. <br>
Risk: Automatic web enrichment and saved preferences can expose sensitive context or persist preferences unexpectedly. <br>
Mitigation: For sensitive recordings, tell the agent to skip web enrichment and avoid saving preferences to MEMORY.md. <br>
Risk: Automatic corrections, summaries, and platform drafts may be inaccurate or change the speaker's intended meaning. <br>
Mitigation: Review low-confidence names, terms, numbers, correction notes, and final publication drafts before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/artminding/video-transcript-workflow) <br>
- [OpenAI Whisper project](https://github.com/openai/whisper) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, shell commands, guidance] <br>
**Output Format:** [TXT transcripts and Markdown drafts, with inline shell commands for local transcription scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes transcript and draft files beside the source media; outputs can include timestamped segments, correction notes, key quotes, and platform-specific publication drafts.] <br>

## Skill Version(s): <br>
2.2.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
