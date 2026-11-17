## Description:

Virtuoso Skill helps developers look up Cadence Virtuoso SKILL APIs, validate SKILL code, and get function recommendations from a bundled API database.

This skill is ready for commercial/non-commercial use.

## Publisher:

[keenone](https://clawhub.ai/user/keenone)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill while writing or debugging Cadence Virtuoso SKILL code to find supported API calls, inspect parameters, and catch undefined or mismatched function usage before submission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional web mode exposes an unauthenticated service.

Mitigation: Use CLI modes by default; when web mode is needed, bind it to localhost or restrict access with a firewall.

Risk: Web mode renders API database content unsafely.

Mitigation: Load only trusted API databases and avoid exposing web mode to untrusted users or networks.

## Reference(s):

- [Skill API Database](references/skill_api_database.json)
- [Virtuoso Skill on ClawHub](https://clawhub.ai/keenone/skills/virtuoso-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or terminal text with SKILL code examples and CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API search results, lint findings, suggested SKILL function calls, and web-mode setup guidance.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
