## Description:

A comprehensive tool for creating, documenting, wrapping, and quality-checking professional-grade skills with standardized templates and best practices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[variyaone](https://clawhub.ai/user/variyaone)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use Skill Forge to create new skills, wrap existing tools, generate documentation, check quality, package releases, and manage dependency guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI includes unsafe command execution paths.

Mitigation: Review and patch command execution before installing or running it on third-party skills; prefer argument-array APIs over shell-composed commands.

Risk: Install, dependency, packaging, and OpenClaw paths can be risky when inputs are untrusted.

Mitigation: Avoid running check, install-deps, wrap, package --zip, or install --openclaw with untrusted skill names, dependency values, or tool paths until names are validated, paths are contained, and installs require clear confirmation.

Risk: The release security verdict is suspicious.

Mitigation: Treat the skill as requiring review and patching before execution, following the authoritative security guidance in the release evidence.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/variyaone/skills/skill-forge-va)
- [README](README.md)
- [Examples](references/examples.md)
- [OpenClaw hook documentation](hooks/openclaw/HOOK.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON examples, and generated skill files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify local skill directories and produce package/install commands for agent platforms.]

## Skill Version(s):

1.3.0 (source: server release evidence and _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
