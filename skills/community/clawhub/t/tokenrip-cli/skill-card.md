## Description:

The `rip` CLI skill helps agents manage Tokenrip workspaces, artifacts, tasks, reviews, connections, deployments, search, and team sharing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[silostack](https://clawhub.ai/user/silostack)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to guide an AI agent through managing shared Tokenrip workspaces and their artifacts, tasks, reviews, and integrations with the `rip` CLI. It is intended for Tokenrip operations rather than local file management, web browsing, direct database access, or Git.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stored provider connections can reach external endpoints.

Mitigation: Restrict connections to the endpoints and users needed for the task.

Risk: Automatic task permissions can allow actions beyond the immediate task.

Mitigation: Keep automatic task permissions narrow and review proposed actions before they are sent or published.

Risk: Hosted skills may install persistent stubs, and shared links can expose retained artifact versions.

Mitigation: Review hosted skills before installing them and check version visibility before sharing links.

Risk: Deleting rows or pruning artifact versions is permanent; the external CLI and server implementations were not included for verification.

Mitigation: Review targets before deletion or pruning, prefer reviewed package versions, and account for the unverified external components when assessing deployment.

## Reference(s):

- [Tokenrip website](https://tokenrip.com)
- [Tokenrip CLI on ClawHub](https://clawhub.ai/silostack/skills/tokenrip-cli)
- [Tokenrip CLI npm package](https://www.npmjs.com/package/@tokenrip/cli)
- [Connections](artifact/references/connections.md)
- [Output and provenance](artifact/references/output-and-provenance.md)
- [Setup and identity](artifact/references/setup-and-identity.md)
- [Skills](artifact/references/skills.md)
- [Tasks](artifact/references/tasks.md)
- [Workspaces](artifact/references/workspaces.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API calls, Markdown, Code, Configuration]

**Output Format:** [Markdown guidance with `rip` CLI command examples and structured artifact content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide the agent to create or update workspace documents, code, CSV data, PDFs, tables, tasks, and deployments.]

## Skill Version(s):

2.6.19 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
