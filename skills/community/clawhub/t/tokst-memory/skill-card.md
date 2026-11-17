## Description:

Use TokST Cloud MCP for durable memory, shared context, and governed knowledge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anthemty](https://clawhub.ai/user/anthemty)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other agent users connect to TokST to retrieve shared context and store confirmed, reusable knowledge across conversations and authorized workspaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved information persists in a third-party cloud memory service.

Mitigation: Confirm the active workspace before saving, and do not store secrets or raw logs.

Risk: Sensitive or personal information may be retained in memory.

Mitigation: Review TokST dashboard settings and obtain approval before broad archival or access changes.

## Reference(s):

- [TokST Memory on ClawHub](https://clawhub.ai/anthemty/skills/tokst-memory)
- [TokST documentation](https://tokst.com/docs)
- [TokST MCP guide](https://tokst.com/docs/mcp)
- [TokST agent guide](https://tokst.com/llms.txt)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown memory records and concise text responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Memory titles and IDs may be returned to support review and continuation.]

## Skill Version(s):

0.9.0+revision.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
