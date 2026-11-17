## Description:

Tracks macOS screen activity by scheduling periodic screenshots, analyzing them with a vision model, and writing searchable activity logs to local Markdown files or SiYuan.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zeject](https://clawhub.ai/user/zeject)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create a searchable personal activity timeline from recurring screen captures, daily summaries, and keyword searches. It is most relevant for users who intentionally want ongoing screen activity tracking on macOS.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent screenshot capture can record sensitive screen contents.

Mitigation: Use only on accounts, displays, and workspaces where continuous full-screen capture is acceptable, and keep screen recording permissions scoped to trusted terminals.

Risk: Captured images and summaries can be sent to configured vision model or SiYuan endpoints.

Mitigation: Configure only trusted HTTPS or strictly local endpoints, and verify where screenshots, summaries, and uploads are stored before starting tracking.

Risk: Advertised privacy blacklist behavior may be misleading or disabled.

Mitigation: Do not rely on the blacklist for sensitive apps until fixed; stop tracking before using banking, password manager, 2FA, or other sensitive applications.

Risk: Configuration can contain service URLs, notebook IDs, and API tokens.

Mitigation: Protect config.json, avoid committing secrets, and rotate exposed SiYuan tokens.

Risk: The skill depends on an external screenshot CLI.

Mitigation: Pin or independently verify the peekaboo dependency before installation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zeject/skills/screen-activity-tracker)
- [Publisher Profile](https://clawhub.ai/user/zeject)
- [README_EN.md](artifact/README_EN.md)
- [SKILL.md](artifact/SKILL.md)
- [config.example.json](artifact/config.example.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown, plain text, JSON snippets, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces cron scheduling guidance, local or SiYuan activity logs, daily summaries, and keyword search results.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
