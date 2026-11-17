## Description:

Collect and send Telegram stickers smartly. Auto-import packs, tag by emotion, select contextually, and respect frequency limits (2-5 messages).

This skill is ready for commercial/non-commercial use.

## Publisher:

[bangyizhang](https://clawhub.ai/user/bangyizhang)

### License/Terms of Use:

MIT

## Use Case:

External developers and OpenClaw agent builders use this skill to manage Telegram sticker collections, tag stickers by emotion, choose context-appropriate sticker file IDs, and integrate sticker sending into agent conversations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Importing sticker packs reads the OpenClaw Telegram bot token and contacts Telegram.

Mitigation: Review before installing and run the import script only when bot-token access and Telegram API calls are acceptable.

Risk: Sticker collection data can include sticker file IDs, tags, usage counts, and optional context notes.

Mitigation: Keep stickers.json free of sensitive conversation text and restrict access to the local collection data.

Risk: Some documented features require manual agent logic or refer to files not present in this release.

Mitigation: Verify required files and workflows before deployment, especially sending, usage tracking, and frequency control.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bangyizhang/skills/tg-stickers)
- [Skill documentation](artifact/SKILL.md)
- [README](artifact/README.md)
- [Release notes](artifact/RELEASE_NOTES.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts may read or update stickers.json and may return a Telegram sticker file_id for agent use.]

## Skill Version(s):

0.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
