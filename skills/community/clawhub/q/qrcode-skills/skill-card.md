## Description:

Generate and decode QR codes locally from text, URLs, image files, and batch Excel/CSV/TXT inputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hinisal](https://clawhub.ai/user/hinisal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to generate QR code image files, decode QR code contents from local images or remote image URLs, and run batch QR workflows over Excel, CSV, or TXT files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install mutable Python or Node dependencies during first use.

Mitigation: Pin and review dependencies before installation, or install them in a restricted environment.

Risk: Decoding remote image URLs can fetch arbitrary network resources.

Mitigation: Prefer local image files and restrict network access when processing untrusted QR sources.

Risk: Batch decoding writes untrusted decoded QR contents into CSV or XLSX files.

Mitigation: Back up input files first and inspect spreadsheet outputs for formulas before opening them in spreadsheet software.

## Reference(s):

- [ClawHub qrcode skill page](https://clawhub.ai/hinisal/skills/qrcode-skills)
- [README.md](artifact/README.md)
- [README.zh-cn.md](artifact/README.zh-cn.md)
- [qr-scanner-wechat](https://github.com/AntFu/qr-scanner-wechat)
- [qrcode-remote-skills](https://github.com/caoliao/qrcode-remote-skills)

## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands]

**Output Format:** [Markdown status messages with local file paths, decoded text, and JSON script results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create PNG, SVG, ZIP, TXT, CSV, or XLSX outputs depending on the requested workflow.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
