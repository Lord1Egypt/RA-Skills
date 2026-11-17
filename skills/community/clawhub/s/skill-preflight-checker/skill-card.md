## Description:

Skill Preflight Checker helps agents assess skill safety before installation by checking publisher reputation, suspicious scripts, permission needs, isolated-install behavior, and install risk recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cp3d1455926-svg](https://clawhub.ai/user/cp3d1455926-svg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill before installing ClawHub, GitHub, or npm skills to inspect author reputation, package scripts, permissions, and suspicious behavior. The skill produces a preflight report with safety flags, risk level, and an install recommendation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some documented npm, Docker, extraction, and cleanup commands could modify or delete local files while inspecting untrusted packages.

Mitigation: Run checks only in a fresh temporary directory or isolated container without writable host mounts, and review commands before execution.

Risk: Unquoted or unvalidated package names in shell command examples could lead to unintended command behavior.

Mitigation: Quote and validate package names before running package inspection, install, extraction, or cleanup commands.

Risk: Installing or packing untrusted packages can trigger lifecycle behavior or expose the environment to package contents.

Mitigation: Prefer metadata inspection first, disable lifecycle scripts where possible, and require explicit user confirmation before any install or extraction step.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cp3d1455926-svg/skills/skill-preflight-checker)
- [README.md](README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes safety ratings and install recommendations; command examples should be reviewed before execution in an isolated temporary environment.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
