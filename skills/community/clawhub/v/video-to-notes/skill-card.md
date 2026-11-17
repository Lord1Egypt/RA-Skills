## Description:

Converts user-provided local or online videos into transcripts and structured study notes using media extraction, Whisper transcription, and agent-generated Markdown note templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yll-kb](https://clawhub.ai/user/yll-kb)

### License/Terms of Use:

MIT-0

## Use Case:

Students, self-directed learners, developers, and professionals use this skill to turn lectures, tutorials, talks, meetings, and documentaries into structured study notes. Agents can transcribe up to a small batch of videos, segment the transcript, and produce review-oriented Markdown with summaries, diagrams, key points, and quick-reference tables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Videos, transcripts, and notes may contain sensitive personal, meeting, course, or business information.

Mitigation: Process only videos the user explicitly provides, tell the user where transcripts and notes will be saved, and remind them to review or delete generated files when privacy matters.

Risk: Online video download can implicate platform rules, copyright, or access restrictions.

Mitigation: Download online videos only after user approval, ask the user to confirm they have rights to use the content, and fall back to a local file when a platform blocks download.

Risk: Installing transcription and media dependencies can increase supply-chain exposure.

Mitigation: Show missing dependencies and full install commands before installation, wait for explicit user approval, and recommend virtual environments with pinned dependency versions for stronger control.

Risk: Transcription and summarization can miss words, mishear technical terms, or over-compress important details.

Mitigation: Use language hints and higher-accuracy Whisper models for important content, keep timestamped transcript output, and ask the user to review generated notes before relying on them.

## Reference(s):

- [Workflow Reference](references/workflow.md)
- [Note Templates](references/note-templates.md)
- [ClawHub Skill Page](https://clawhub.ai/yll-kb/skills/video-to-notes)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown notes plus timestamped transcript text and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create transcript text files beside the source video or in a selected output directory; temporary audio files are removed after transcription.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
