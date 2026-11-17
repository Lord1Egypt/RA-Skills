## Description:

Guides agents in mapping legacy websites and building client-side browser-extension overlays that modernize their interfaces while preserving host behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theajmalrazaq](https://clawhub.ai/user/theajmalrazaq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this playbook to inspect legacy sites and build browser-extension overlays that provide a modern interface while keeping the host site and its authentication flow in place.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may save complete snapshots of authenticated pages containing personal or sensitive information; the security review is suspicious with medium confidence and scan coverage is incomplete.

Mitigation: Minimize and sanitize saved snapshots, and set access and retention limits. Treat the partial scan as insufficient to establish that the skill is safe.

## Reference(s):

- [Resurface source on GitHub (server-resolved provenance)](https://github.com/theajmalrazaq/resurface/tree/master/skills/resurface)
- [Obscura](https://github.com/h4ckf0r0day/obscura)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown playbook with code, shell, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
