## Description:

Sync and access voice notes from Voicenotes.com, including recordings, transcripts, AI summaries, markdown sync, and transcript search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shawnhansen](https://clawhub.ai/user/shawnhansen)

### License/Terms of Use:


## Use Case:

Developers and other Voicenotes users use this skill to verify their Voicenotes connection, fetch recordings as JSON, and sync transcripts, summaries, tags, and note metadata into local markdown files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Voicenotes API token can grant access to private voice notes and account data if exposed.

Mitigation: Keep VOICENOTES_TOKEN out of logs, dotfiles, and shared command history, and rotate the token if it is exposed.

Risk: Synced markdown files may contain private transcripts, summaries, tags, and note metadata.

Mitigation: Write synced notes only to a private output directory and avoid syncing them into shared or untrusted folders.

## Reference(s):

- [Voicenotes](https://voicenotes.com)
- [Voicenotes Obsidian Sync Settings](https://voicenotes.com/app?obsidian=true#settings)
- [Voicenotes Obsidian Sync API](https://api.voicenotes.com/api/integrations/obsidian-sync)
- [ClawHub Skill Page](https://clawhub.ai/shawnhansen/skills/voicenotes)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, Markdown, Guidance]

**Output Format:** [Markdown with inline bash commands and generated JSON or markdown files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a VOICENOTES_TOKEN environment variable; markdown sync writes local files to the configured output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
