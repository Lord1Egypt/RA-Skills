## Description:

Routes knowledge, judgment, writing, reflection, decision, AI-agent, product, learning, and long-term thinking questions through cognitive anchors, local recall, and optional wiki writeback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to route broad thinking, writing, decision, and knowledge-management questions through a personal Markdown wiki, selected cognitive anchors, local recall tools, and small explicit writebacks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may consult local second-brain or wiki materials for broad thinking and writing questions.

Mitigation: Install it only for workflows where that local consultation is desired, and review or customize the default vault paths and recall tools before use.

Risk: The default paths and receipt template may not match the user's setup or language preference.

Mitigation: Adjust the vault paths, recall commands, and receipt language during installation or before relying on the routing loop.

Risk: Wiki writeback could preserve an incorrect or premature conclusion if requested too broadly.

Mitigation: Use the documented explicit-writeback posture: write only when the user asks to save or update, keep edits small, and preserve existing content and frontmatter.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/harrylabsj/skills/second-brain-router)
- [ClawHub Publisher Profile](https://clawhub.ai/user/harrylabsj)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional shell command suggestions and small wiki file updates when explicitly requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read local wiki or recall-tool output; writes only after explicit user request.]

## Skill Version(s):

1.1.0 (source: server release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
