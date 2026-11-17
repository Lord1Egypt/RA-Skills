## Description:

Trust and evidence verification engine for claims, sources, screenshots, profiles, offers, and suspicious messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[projectsnowwork](https://clawhub.ai/user/projectsnowwork)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users use Verifier to capture local verification cases, score provided evidence, and receive a verdict, confidence level, risk notes, missing-evidence guidance, and a recommended next verification step.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill advertises broad trust judgments while using simple rule-based scoring rather than independent verification.

Mitigation: Treat outputs as triage guidance, and require original-source evidence plus human review before consequential decisions.

Risk: Verification cases may contain sensitive details and are stored locally in plaintext without enforced private permissions.

Mitigation: Do not store passwords, tokens, private keys, or unnecessary personal details, and use a host where the OpenClaw memory directory is private to the user account.

## Reference(s):

- [Verifier Philosophy](references/philosophy.md)
- [ClawHub Skill Page](https://clawhub.ai/projectsnowwork/skills/verifier)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with optional JSON output from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores local verification cases under ~/.openclaw/workspace/memory/verifier/cases.json.]

## Skill Version(s):

1.0.0 (source: release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
