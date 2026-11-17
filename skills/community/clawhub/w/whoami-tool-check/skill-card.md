## Description:

Identity verification utility -- validate current user against expected roles, check sudo access, and audit user capabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and system operators use this skill to check the current execution identity and to reason about user access before running security-sensitive commands. Review the packaged behavior before relying on the broader audit claims.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documentation advertises sudo, role, capability, audit, and JSON checks that the packaged script does not implement.

Mitigation: Do not rely on the skill for access reviews or security audits unless those checks are implemented, tested, and reviewed before deployment.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text username output with Markdown command examples in the skill documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The included script prints the current username; advertised sudo, role, audit, and JSON modes are not implemented in the packaged script.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
