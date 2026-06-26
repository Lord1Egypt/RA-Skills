## Description: <br>
Sync, transcribe, and intelligently organize voice memos, audio/video files, and URLs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ying-wen](https://clawhub.ai/user/ying-wen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users use this skill to process voice memos, recordings, videos, URLs, and transcript files into structured summaries, action items, Apple Notes, Reminders, and local memory records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can collect private recordings, videos, transcripts, and user context into local memory records. <br>
Mitigation: Review configured scan paths before use, especially broad iCloud folders such as Downloads, and keep only intentional input directories enabled. <br>
Risk: Processed transcripts and personalized analysis can be persisted into Apple Notes, Reminders, and local memory. <br>
Mitigation: Use the skill only when persistent records are desired, and disable or review Apple Notes, Reminders, and personalized analysis settings before processing sensitive content. <br>
Risk: Heartbeat auto-sync can repeatedly process newly discovered recordings without a per-file prompt. <br>
Mitigation: Keep heartbeat auto-sync disabled unless recurring processing is intended, and audit the generated HEARTBEAT task and sync log when enabling it. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ying-wen/voice-memo-sync) <br>
- [Voice Memo Sync README](artifact/README.md) <br>
- [Voice Memo Sync Architecture](artifact/docs/ARCHITECTURE.md) <br>
- [Apple Silicon](https://support.apple.com/en-us/116943) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown notes, transcript files, JSON source records, Apple Notes entries, Reminders tasks, and shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local-first processing by default; can create persistent local records and sync processed content to Apple Notes and Reminders.] <br>

## Skill Version(s): <br>
1.6.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
