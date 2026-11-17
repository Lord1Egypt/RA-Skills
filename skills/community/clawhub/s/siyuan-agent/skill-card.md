## Description:

Interact with SiYuan notes via direct HTTP API for reading, writing, searching, managing blocks and documents, handling assets, and executing SQL queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eloklam](https://clawhub.ai/user/eloklam)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to search, read, export, and manage SiYuan notes through an authenticated HTTP API, including SELECT SQL queries and guarded write operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill grants broad SiYuan API authority through SIYUAN_TOKEN, and its generic direct API command can weaken documented safety controls around SQL and writes.

Mitigation: Use a local loopback SIYUAN_BASE when possible, avoid untrusted or plaintext remote hosts, protect SIYUAN_TOKEN, and review generic API calls before execution.

## Reference(s):

- [Siyuan Agent on ClawHub](https://clawhub.ai/eloklam/skills/siyuan-agent)
- [eloklam ClawHub profile](https://clawhub.ai/user/eloklam)
- [SiYuan](https://ld246.com/)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration]

**Output Format:** [JSON API responses, Markdown exports, and shell command invocations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIYUAN_TOKEN; SIYUAN_BASE defaults to local loopback unless configured.]

## Skill Version(s):

2.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
