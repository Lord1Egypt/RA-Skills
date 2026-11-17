## Description:

Downloads PDF files from specified Telegram Web channels and organizes them into local folders based on message headers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[koppakanagaharsha-lang](https://clawhub.ai/user/koppakanagaharsha-lang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to automate collection of study-material PDFs from Telegram channels into a local folder structure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses an authenticated Telegram Web session and persists a local browser profile.

Mitigation: Use a dedicated Telegram session and non-sensitive browser profile, and isolate or clear the profile after use.

Risk: Downloaded PDFs and channel-controlled filenames or folders may be unsafe or misleading.

Mitigation: Save downloads to a dedicated non-sensitive folder, treat PDFs as untrusted, and prefer a revised version with attachment-origin, file-type, file-size, and path-traversal checks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/koppakanagaharsha-lang/skills/telegram-pdf-scraper)
- [ClawHub publisher profile](https://clawhub.ai/user/koppakanagaharsha-lang)

## Skill Output:

**Output Type(s):** [Files, Text]

**Output Format:** [Downloaded PDF files organized in local folders with status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a Telegram Web session and a local browser profile; downloaded PDFs should be treated as untrusted.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
