## Description:

Sync, transcribe, and intelligently organize voice memos, audio/video files, and URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ying-wen](https://clawhub.ai/user/ying-wen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to turn Apple Voice Memos, local audio/video files, transcript files, and video URLs into structured transcripts, summaries, Apple Notes, reminders, and local memory records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private recordings and personal context may be copied into OpenClaw memory and used to generate notes or reminders.

Mitigation: Review configuration before installation, keep auto-sync disabled unless recurring processing is intended, and process only recordings the user intentionally provides.

Risk: Untrusted filenames, note content, transcript text, JSON or CSV fields, and remote URLs may flow into shell, AppleScript, or parser paths identified by the security evidence.

Mitigation: Avoid untrusted inputs until the script injection issues are fixed; require confirmation before processing remote URLs or writing to iCloud-backed apps.

Risk: The skill can write to Apple Notes and Reminders and can copy files from iCloud recording locations.

Mitigation: Run with the least needed macOS permissions, review generated notes and reminders before relying on them, and limit configured sync paths.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ying-wen/skills/voice-memo-sync)
- [Publisher profile](https://clawhub.ai/user/ying-wen)
- [Skill homepage](https://github.com/ying-wen/voice-memo-sync)
- [README.md](artifact/README.md)
- [Architecture](artifact/docs/ARCHITECTURE.md)
- [Sample output](artifact/examples/sample-output.md)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [Apple macOS](https://www.apple.com/macos/)
- [Apple Silicon support](https://support.apple.com/en-us/116943)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown notes and summaries, transcript text, JSON source metadata, shell command snippets, and YAML configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates local voice-memo memory files and can write Apple Notes or Reminders when configured.]

## Skill Version(s):

1.6.1 (source: server release, skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
