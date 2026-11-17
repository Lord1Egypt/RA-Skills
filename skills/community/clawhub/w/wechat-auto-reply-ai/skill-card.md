## Description:

Monitors WeChat on macOS with OCR and uses a configurable Gemini persona to generate and send automatic replies through UI automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jarryxin](https://clawhub.ai/user/jarryxin)

### License/Terms of Use:

MIT-0

## Use Case:

Users running WeChat on macOS use this skill to monitor selected contacts, analyze chat screenshots with a vision/text model, and send persona-guided replies or location links through UI automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The dashboard can expose chat data and automation controls without authentication.

Mitigation: Bind the dashboard to localhost, add authentication, and do not expose it to a LAN or WAN.

Risk: Shell-based automation and unsanitized dashboard rendering can increase command and content handling risk.

Mitigation: Remove shell=True command strings where practical and sanitize content before dashboard rendering.

Risk: The skill can send WeChat messages automatically while holding Screen Recording and Accessibility permissions.

Mitigation: Review code before installation, use an approval or dry-run mode before sending messages, and avoid granting these permissions on machines with sensitive data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jarryxin/skills/wechat-auto-reply-ai)
- [Publisher profile](https://clawhub.ai/user/jarryxin)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions, configuration values, and generated chat reply text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires macOS WeChat, Screen Recording and Accessibility permissions, OpenClaw CLI tools, Flask for the dashboard, and a Gemini API key for model calls.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
