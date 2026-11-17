## Description:

Helps agents use Ranla's CLI to manage account workflows, including campaigns, segments, and approvals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ranla](https://clawhub.ai/user/ranla)

### License/Terms of Use:

MIT-0

## Use Case:

People and agents working with a Ranla account use this skill to inspect and draft campaigns, build segments, choose workspaces, and review approval requests through the CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running the latest published CLI package can execute code that changes between invocations.

Mitigation: Review the CLI before use and prefer a pinned or globally installed reviewed version where possible.

Risk: Commands may act on the wrong workspace or approve sending, publishing, or spending.

Mitigation: Let the user choose the workspace and request explicit approval before consequential actions.

Risk: Account credentials may be exposed if handled outside the CLI sign-in flow.

Mitigation: Use browser sign-in and avoid exposing RANLA_API_KEY unless needed.

## Reference(s):

- [Ranla agent CLI guide](https://docs.ranla.ai/guides/agent-cli)
- [Ranla CLI on ClawHub](https://clawhub.ai/ranla/skills/ranla-cli)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Text]

**Output Format:** [Markdown with inline shell commands and approval summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CLI results can include JSON responses and links to pending approvals.]

## Skill Version(s):

1.0.0 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
