## Description:

Guides agents in using a connected Vercel account to manage projects, deployments, domains, teams, and environment variables through Maton.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect and manage Vercel resources through an authorized connection, and to set up approved functions and triggers for recurring tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connecting Maton grants access to the authorized Vercel account.

Mitigation: Obtain approval for the connection and authorize only the access needed for the task.

Risk: Writes or deletions can change projects, environment variables, domains, and production deployments.

Mitigation: Confirm each action and its exact target before execution, especially destructive or production changes.

Risk: Deployed functions and triggers can run unattended or persistently forward events to a destination.

Mitigation: Require separate approval for functions, triggers, and destinations; verify the destination and data shared.

## Reference(s):

- [Vercel skill release](https://clawhub.ai/byungkyu/skills/vercel-api)
- [Maton](https://maton.ai)
- [Vercel REST API documentation](https://vercel.com/docs/rest-api)
- [Maton CLI manual](https://cli.maton.ai/manual)
- [Time trigger reference](artifact/references/time/triggers.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration instructions]

**Output Format:** [Markdown with command and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions depend on the user's authorized Vercel connection and require confirmation for writes and automation.]

## Skill Version(s):

1.2.5 (source: ClawHub release record)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
