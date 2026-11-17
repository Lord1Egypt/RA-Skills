## Description:

SiYuan Note local API helper for reading and writing notebooks, documents, blocks, searches, templates, and SQL queries in a local SiYuan workspace.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moxunjinmu](https://clawhub.ai/user/moxunjinmu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and SiYuan users use this skill to let an agent operate a local SiYuan Note instance, including creating documents, searching notes, appending or updating blocks, exporting Markdown, rendering templates, and running SQL queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent broad authenticated access to private local SiYuan notes.

Mitigation: Install only when the agent is trusted with the SiYuan API token and private note contents.

Risk: Write, delete, export, and SQL operations can modify or expose note data.

Mitigation: Confirm each destructive, export, or SQL action before execution and avoid broad or ambiguous prompts.

Risk: Documented proxy behavior may send note contents outside the local SiYuan instance if used intentionally.

Mitigation: Do not send note contents through proxy endpoints unless external network access is explicitly intended.

Risk: The helper script depends on Python requests and uses an API token from the local environment.

Mitigation: Run the helper in an isolated Python environment with reviewed dependencies and scoped environment variables.

## Reference(s):

- [SiYuan API reference](references/api.md)
- [Official SiYuan API documentation](https://github.com/siyuan-note/siyuan/blob/master/API_zh_CN.md)
- [ClawHub skill page](https://clawhub.ai/moxunjinmu/skills/siyuan-note)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration, markdown]

**Output Format:** [Markdown with inline shell commands, Python helper usage, JSON request examples, SQL snippets, and generated note content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require a local SiYuan instance and SIYUAN_TOKEN for authenticated operations.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
