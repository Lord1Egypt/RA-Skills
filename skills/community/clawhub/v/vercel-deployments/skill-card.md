## Description:

Manage Vercel projects, deployments, domains, environment variables, and team resources via the Vercel REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect and manage Vercel projects, deployments, domains, environment variables, secrets, audit logs, and team resources from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires installing and allowlisting an external ClawLink plugin that mediates access to Vercel account actions and credentials.

Mitigation: Install only when the publisher and ClawLink are trusted, review OAuth scopes before connecting, and know how to revoke the Vercel connection and remove the plugin allowlist entry.

Risk: Write or destructive Vercel operations can change deployments, domains, environment variables, secrets, projects, or team access.

Mitigation: Preview write operations, confirm the exact target and effect with the user, and use the least-privileged Vercel account or team role practical.

Risk: Environment variable, secret, and domain changes can affect running production deployments.

Mitigation: Check the intended environment or domain status first, prefer read/list/get operations before changes, and confirm production-impacting updates explicitly.

## Reference(s):

- [Vercel REST API Documentation](https://vercel.com/docs/rest-api)
- [ClawLink OpenClaw Documentation](https://docs.claw-link.dev/openclaw)
- [ClawLink Verification](https://claw-link.dev/verify)
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/skills/vercel-deployments)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and structured tool-call parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Vercel resource identifiers, JSON parameters for ClawLink tool calls, previews, confirmations, and error summaries.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
