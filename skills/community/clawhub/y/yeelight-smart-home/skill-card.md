## Description:

Control, organize, diagnose, design, and personalize a Yeelight smart home, and answer product questions using a locally installed Yeelight runtime.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yeelight](https://clawhub.ai/user/yeelight)

### License/Terms of Use:

MIT-0

## Use Case:

Yeelight smart-home users and their assistants use this skill to inspect and control devices, organize homes and rooms, plan lighting, manage scenes and automations, troubleshoot issues, and answer product questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Smart-home controls and configuration can change devices or persistent settings.

Mitigation: Install only if local Yeelight control is intended; review destructive requests and follow the runtime's safety checks.

Risk: An untrusted or outdated local runtime could handle sensitive home operations.

Mitigation: Install and maintain the Yeelight runtime from an official source.

Risk: Local personalization and operation lessons may retain information the user does not want stored.

Mitigation: Use memory pause or forget controls when retention is not wanted.

## Reference(s):

- [Yeelight Smart Home release](https://clawhub.ai/yeelight/skills/yeelight-smart-home)
- [Skill reference guide](artifact/references/README.md)
- [Safety and confirmation](artifact/references/safety-and-confirmation.md)
- [Capability boundaries](artifact/references/capability-boundaries.md)
- [Memory and personalization](artifact/references/memory-and-personalization.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Concise natural-language text with structured Markdown when useful]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Distinguishes verified results, partial failures, and proposals; shows full JSON only on request.]

## Skill Version(s):

0.1.16 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
