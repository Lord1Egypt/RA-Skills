## Description:

ZFONT-CLI helps agents search ZFONT.CN for free commercial-use fonts, download selected font archives, optionally extract TTF, OTF, and TTC files, and provide installation or transfer guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lanmin-x](https://clawhub.ai/user/lanmin-x)

### License/Terms of Use:

MIT-0

## Use Case:

External users and design or development teams use this skill to find and retrieve free commercial-use font assets from ZFONT.CN. The agent can return either a downloaded archive or extracted font files with concise installation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: File and shell handling could expose local files or run unintended commands if parameters are manipulated.

Mitigation: Require confirmation before download, avoid shell interpolation, validate that only files created by the current workflow can be sent, and keep artifacts in a private per-run directory.

Risk: Downloaded and extracted font artifacts may remain after delivery.

Mitigation: Clean up downloaded archives and extracted files after the user receives the requested asset.

## Reference(s):

- [ZFONT.CN](https://zfont.cn/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown responses with downloadable ZIP or font files and concise installation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May download archives to temporary storage and optionally extract font files before delivery.]

## Skill Version(s):

1.5.3 (source: release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
