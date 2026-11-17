## Description:

Generate Vercel API commands for deployment management, including deployment status, build logs, domain SSL checks, recent deployments, rollbacks, and environment variable audits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loutai0307-prog](https://clawhub.ai/user/loutai0307-prog)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site operators use this skill to generate Vercel API curl commands for checking deployments, logs, domains, environment variables, and rollback actions before running those commands themselves.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated shell commands can become unsafe when project or deployment names contain unexpected quotes, semicolons, pipes, backticks, or command substitutions.

Mitigation: Use only trusted project and deployment identifiers, inspect generated commands before execution, and reject commands containing unexpected shell metacharacters.

Risk: Token setup guidance may encourage users to store Vercel tokens in shell profiles.

Mitigation: Avoid storing long-lived Vercel tokens in shell profiles; prefer short-lived or scoped credential handling appropriate for the user's environment.

Risk: Rollback command generation supports a production-changing action.

Mitigation: Require explicit human confirmation and deployment review before running rollback or promotion commands.

## Reference(s):

- [Vercel API endpoint](https://api.vercel.com)
- [Vercel account tokens](https://vercel.com/account/tokens)
- [ClawHub skill page](https://clawhub.ai/loutai0307-prog/skills/vercel-tool)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-style text with bash commands and inline setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands are generated for human review and execution; no credentials are stored by the skill.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
