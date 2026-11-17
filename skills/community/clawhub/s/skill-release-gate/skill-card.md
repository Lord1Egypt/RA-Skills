## Description:

Provides a pre-publication checklist and offline PII, secret, and desensitization scans for skills, MCP servers, expert profiles, and documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and publishing teams use it to apply a release checklist, assign a publication tier, and run local PII, secret, and desensitization checks before publishing skills or related artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The offline scanners may miss secrets or fail to inspect some files, so a PASS result can be incomplete.

Mitigation: Run them on a sandboxed copy of the intended release directory, require independent checks before publication, and keep reports private.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/zhaoxinghua09-cell/skills/skill-release-gate)
- [Publisher ecosystem hub](https://zhaoxinghua09-cell.github.io/lgd-hub/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON]

**Output Format:** [Markdown guidance, shell commands, and structured JSON scan results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scan findings and exit codes depend on the files examined.]

## Skill Version(s):

1.0.12 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
