## Description:

WeRead (微信读书) lets an agent query a user's WeRead bookshelf, reading progress, highlights, notes, reviews, chapters, and export or sample reading notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenyqthu](https://clawhub.ai/user/chenyqthu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an OpenClaw agent retrieve, review, export, and reuse their personal WeRead reading data. It supports bookshelf lookup, reading statistics, note and highlight retrieval, daily review selection, and local JSON export.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores a live WeRead login cookie and can access private reading history.

Mitigation: Treat ~/.weread/cookie like a password: keep it private, avoid committing or syncing it, and delete or rotate it if exposed.

Risk: Normal use sends authenticated requests to WeRead/Tencent services.

Mitigation: Install only when that remote data flow is acceptable for the account, and review privacy expectations before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chenyqthu/skills/weread)
- [WeRead Web App](https://weread.qq.com)
- [OpenClaw Project](https://github.com/nicepkg/openclaw)

## Skill Output:

**Output Type(s):** [Text, JSON, Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [JSON command output and local JSON files, with optional plaintext note selections and Markdown-style setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include private bookshelf, reading progress, highlights, notes, reviews, and locally exported reading data.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
