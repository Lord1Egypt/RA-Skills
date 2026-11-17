## Description:

SmartClaws guides OpenClaw agents through understanding, setting up, and operating SmartClaws IoT telemetry and command workflows on SKALE, including jobs, plugin modes, permissions, encryption, and runtime tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eduv09](https://clawhub.ai/user/eduv09)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and OpenClaw operators use this skill to configure SmartClaws agents that publish or read IoT telemetry on SKALE. It helps set up group masters, device masters, device bridges, or user proxies with the right plugin mode, on-chain identity, workspace files, permissions, and operating guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow may expose high-impact SmartClaws permissions too broadly during installation or onboarding.

Mitigation: Use the skill only with a trusted SmartClaws deployment, add an explicit tool allowlist, and remove broad SmartClaws tool grants after setup.

Risk: Templates and setup guidance can enable reads, disclosures, registrations, role changes, key operations, publishing, and backups.

Mitigation: Require owner confirmation before writes, separate read and disclosure permissions, and keep authority allowlists in owner-adopted workspace instructions.

Risk: Incorrect addresses, identities, transaction statuses, or encrypted-channel assumptions could cause misleading operation or unintended on-chain actions.

Mitigation: Resolve names and permissions with SmartClaws plugin tools, report only returned tool results, and treat encrypted messages as stored only when the returned status is published.

Risk: Wallet files, private keys, backups, or configuration secrets could be mishandled during setup.

Mitigation: Do not read, print, or hand-copy wallet files or private keys; use wallet-info and backup tools rather than direct secret access.

## Reference(s):

- [SmartClaws ClawHub Skill Page](https://clawhub.ai/eduv09/skills/smartclaws)
- [SmartClaws Homepage](https://github.com/skalenetwork/smartclaws)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON/YAML configuration examples, and workspace file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance is setup-oriented and may include local file templates, operating contracts, permission checks, and tool-use instructions; it does not output wallet secrets.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
