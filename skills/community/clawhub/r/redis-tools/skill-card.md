## Description:

Lookup Redis commands by category, test Redis server connections, and monitor database key counts and memory usage, with offline cheatsheet support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to look up Redis command syntax, test a Redis endpoint, and inspect key counts or memory usage from a shell environment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Redis passwords passed as command-line arguments can be exposed through shell history or local process inspection.

Mitigation: Avoid passing sensitive Redis passwords on the command line; prefer a temporary low-privilege Redis ACL user, non-production endpoints, or an authentication method outside shell history and process arguments.

Risk: Testing or monitoring real Redis instances can expose operational data or affect production access patterns.

Mitigation: Review the skill before installing it for real Redis environments and use non-production endpoints or least-privilege credentials where possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xueyetianya/skills/redis-tools)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and terminal text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires bash; redis-cli is optional for the cheatsheet and required for connection testing and monitoring.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
