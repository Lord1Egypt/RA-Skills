## Description:

Verify AI agent trust scores and reputation via Towel Protocol for agent-to-agent workflows, reputation lookups, credential imports, and trust-tier display.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leo-guinan](https://clawhub.ai/user/leo-guinan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to check external AI agent trust tiers before acting on agent output, to retrieve agent reputation profiles, and to add trust context to multi-agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled shell scripts can create private GitHub repositories, push data, and persist GitHub tokens when run with an authenticated GitHub CLI session.

Mitigation: Review scripts before execution, run them only with an intended GitHub account and organization, and rotate or remove tokens if a remote URL stores credentials.

Risk: Generated handshake seeds and agent identifiers may be committed or pushed by the artifact scripts.

Mitigation: Treat generated seeds as secrets, avoid sensitive internal agent identifiers, and remove or rotate any seed that has been committed or shared.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leo-guinan/skills/towel-protocol)
- [Towel Protocol](https://towel.metaspn.network)
- [Towel Protocol Spec](https://towel.metaspn.network/spec)
- [Verified List API](https://towel.metaspn.network/api/v1/list)
- [Verified List](https://towel.metaspn.network/list)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration]

**Output Format:** [Markdown with inline bash commands and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference public Towel Protocol API responses and local shell scripts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
