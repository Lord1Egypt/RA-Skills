## Description:

Safety KB Query lets agents query a local safety-review SQLite knowledge base for regulations, standards, clauses, statistics, schema details, and data-quality issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyz9827](https://clawhub.ai/user/cyz9827)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agents, and safety/compliance users use this skill to search a local safety-regulation knowledge base, check whether referenced standards exist, inspect clauses, review database statistics, and identify data-quality issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose contents or schema details from whatever local SQLite database is configured as the knowledge base.

Mitigation: Install only when the agent should query the local safety-review knowledge base; keep KB_PATH unset or set only to the intended knowledge.db file.

Risk: Schema and info commands may reveal private or unrelated data if pointed at the wrong database.

Mitigation: Avoid using schema or info commands on databases that may contain private or unrelated data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cyz9827/skills/safety-kb-query)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON from the query script, with agent-facing Markdown or text summaries when presenting results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only query workflow for the configured local safety-review SQLite database.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
