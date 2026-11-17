## Description:

This skill locally encodes text or URLs into PNG QR codes and decodes QR code contents from image files without requiring an external API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jisuapi](https://clawhub.ai/user/jisuapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create local PNG QR codes from text or URLs and decode QR code contents from local images without calling an external API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local path handling and input limits can let the skill read or overwrite more than users expect.

Mitigation: Install it in a contained environment, use a dedicated output directory, avoid untrusted paths or symlinked workspaces, and avoid very large QR rendering parameters until the security guidance is resolved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jisuapi/skills/qrcode2)
- [JisuAPI QR code API reference](https://www.jisuapi.com/api/qrcode/)

## Skill Output:

**Output Type(s):** [text, shell commands, files, guidance]

**Output Format:** [JSON command responses with local PNG image files for encoded QR codes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 plus the qrcode[pil] package for encoding and opencv-python for decoding.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
