## Description:

Decode QR codes, trace redirects, inspect gated destinations, and explain what the link actually needs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vicky-v7](https://clawhub.ai/user/vicky-v7)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI-agent users use this skill to decode QR images, follow short-link redirect chains, detect app, login, WeChat, and WeCom gates, and produce a concise diagnosis with next steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Decoded QR codes and short links can point to attacker-controlled or sensitive destinations, and the skill is designed to make network requests to trace and inspect them.

Mitigation: Use a decode-first workflow, show the raw decoded URL before tracing, and avoid tracing private login links, payment links, invite links, internal company URLs, or untrusted QR images unless the operator accepts the request risk.

Risk: Redirect and gate inspection may disclose the operator's network origin or user-agent choices to destination services.

Mitigation: Limit inspection to necessary requests, keep curl timeouts and redirect caps, and prefer manual review or an isolated network environment for suspicious links.

Risk: Generated diagnoses can misclassify app gates, expired content, or login walls because they rely on headers, redirects, and sampled page content.

Mitigation: Present findings as a diagnosis with observed evidence and next steps, and recommend manual verification when gate type or content validity is uncertain.

## Reference(s):

- [QR Bridge on ClawHub](https://clawhub.ai/vicky-v7/skills/qr-bridge)
- [Publisher profile](https://clawhub.ai/user/vicky-v7)
- [README](artifact/README.md)
- [Chinese README](artifact/README_CN.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown diagnosis with JSON decoder output and inline shell or Python command blocks when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read local QR images, compile a Swift decoder, generate QR image files, and contact decoded or supplied URLs during trace and inspect steps.]

## Skill Version(s):

1.0.1 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
