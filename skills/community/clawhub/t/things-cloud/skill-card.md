## Description:

Manage Things 3 tasks through Things Cloud using the maintained things-cloud-sdk CLI and MCP server, with dry-run safety for agent writes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pdurlej](https://clawhub.ai/user/pdurlej)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent inspect, search, and safely update Things 3 tasks through Things Cloud with MCP tools or CLI commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on external Things Cloud CLI and MCP tools that can access task data.

Mitigation: Install only after reviewing and trusting the referenced things-cloud-sdk project.

Risk: Things Cloud credentials may expose personal task data or allow task changes.

Mitigation: Prefer a revocable automation token, keep credentials out of repositories, and avoid storing credentials in skill files.

Risk: Agent-generated writes could create, edit, complete, or repeat the wrong task.

Mitigation: Use dry-run previews, summarize planned changes, require user confirmation, and use task UUIDs returned by Things Cloud output.

## Reference(s):

- [things-cloud-sdk](https://github.com/pdurlej/things-cloud-sdk)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Raw command output should remain JSON; summaries should include task title, UUID, view or status, and whether a write was a dry run or executed.]

## Skill Version(s):

0.1.2 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
