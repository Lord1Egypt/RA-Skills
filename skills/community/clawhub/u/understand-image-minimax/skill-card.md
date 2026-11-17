## Description:

Analyzes images with the Minimax Coding Plan VLM API using an API key provided in MINIMAX_API_KEY.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xbos1314](https://clawhub.ai/user/xbos1314)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to ask questions about images supplied as URLs, local files, or Base64 data and receive a text answer from Minimax.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch arbitrary image URLs or read local paths and send the resulting image data to Minimax without explicit upload confirmation.

Mitigation: Use only images approved for third-party processing, avoid sensitive local paths and untrusted URLs, and run it in a restricted environment with a dedicated MINIMAX_API_KEY.

Risk: The security summary notes missing image validation, URL/IP protections, and file or response size limits.

Mitigation: Review inputs before execution and add validation, URL/IP protections, and size limits before broader deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xbos1314/skills/understand-image-minimax)
- [Minimax API host](https://api.minimaxi.com)

## Skill Output:

**Output Type(s):** [Text, Analysis, Shell commands]

**Output Format:** [Plain text response with command-line status and errors]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and MINIMAX_API_KEY; supports JPEG, PNG, GIF, WebP, URL, local file path, and Base64 data URL inputs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
