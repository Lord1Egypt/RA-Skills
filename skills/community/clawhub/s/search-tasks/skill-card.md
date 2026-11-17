## Description:

Search and browse tasks on OpenAnt, including available work, bounties, open tasks, task filters, specific task details, and escrow status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ant-1984](https://clawhub.ai/user/ant-1984)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to find, filter, and inspect OpenAnt tasks and bounty details through read-only CLI queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill authorizes running an unpinned npm package through npx @latest.

Mitigation: Pin @openant-ai/cli to a reviewed version and avoid automatic upgrades during routine task browsing.

Risk: The skill tells the agent to execute read-only queries without user confirmation.

Mitigation: Run with only the OpenAnt credentials and filesystem access needed for task browsing, and keep command patterns limited to status, list, get, and escrow queries.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands are intended to be read-only OpenAnt task queries and should append --json for structured output.]

## Skill Version(s):

0.1.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
