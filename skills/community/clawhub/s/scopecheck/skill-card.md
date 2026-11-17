## Description:

Analyze an OpenClaw SKILL.md and extract its permission scope, including environment variables, CLI tools, filesystem paths, and network URLs, then compare declared requirements against detected usage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mirni](https://clawhub.ai/user/mirni)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use Scopecheck to inspect SKILL.md files for declared and detected permission scope. It helps identify undeclared environment variables, command-line tools, filesystem paths, and network URLs before a skill is deployed or reviewed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned Python dependencies can change behavior across installations.

Mitigation: Use pinned dependency versions or a lockfile for production use.

Risk: The analyzer receives raw SKILL.md content through the local API.

Mitigation: Submit only SKILL.md content intended for local analysis.

## Reference(s):

- [Scopecheck ClawHub skill page](https://clawhub.ai/mirni/skills/scopecheck)
- [mirni publisher profile](https://clawhub.ai/user/mirni)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The local API response includes declared scope, detected scope, and undeclared access findings.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
