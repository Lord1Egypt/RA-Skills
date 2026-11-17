## Description:

Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[soponcd](https://clawhub.ai/user/soponcd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to investigate bugs, test failures, build failures, performance issues, and integration problems through a root-cause-first debugging workflow before proposing a fix.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Diagnostic examples can expose credential-adjacent signing, keychain, environment, or identity metadata when copied into CI, production, or shared support channels.

Mitigation: Redact environment values and signing identity details, and avoid running or sharing those diagnostics in CI, production, or public support contexts unless the output has been reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/soponcd/skills/timeflow-systematic-debugging)
- [Systematic Debugging source homepage](https://github.com/soponcd/timeflow-skills/tree/main/teams/skills/systematic-debugging)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, code]

**Output Format:** [Markdown guidance with inline shell command and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Root-cause investigation workflow; no automated execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
