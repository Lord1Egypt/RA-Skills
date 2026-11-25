## Description:

Memory and defence for AI agents: semantic recall, knowledge graph and decay, plus a memory firewall that scans and enforces against prompt injection, credential leaks and poisoning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jarvis-drakon](https://clawhub.ai/user/jarvis-drakon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use ShieldCortex for persistent local memory, semantic recall, and security checks that can filter unsafe memory or tool content. It also provides setup and configuration guidance for supported agent integrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates the skill suspicious because documented integrations use unpinned `npx` commands that can download and run changing packages.

Mitigation: Review package names and versions before enabling integrations that use `npx`; consider preinstalling reviewed versions where the skill documents this option.

Risk: ClawScan coverage was partial, unresolved local references remained, and executable files were not inspected.

Mitigation: Review the referenced package and local materials before installation; treat the scan as incomplete evidence rather than a full package assessment.

## Reference(s):

- [ShieldCortex documentation](https://shieldcortex.ai/docs)
- [ShieldCortex website](https://shieldcortex.ai)
- [ShieldCortex on npm](https://www.npmjs.com/package/shieldcortex)
- [Publisher GitHub profile](https://github.com/Drakon-Systems-Ltd)
- [Security audit waiver notes](https://github.com/Drakon-Systems-Ltd/ShieldCortex/blob/main/docs/security/audit-waivers.md)
- [ClawHub release page](https://clawhub.ai/jarvis-drakon/skills/shieldcortex)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown instructions with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Version-specific setup, security, and usage guidance for ShieldCortex.]

## Skill Version(s):

5.22.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
