## Description:

Super Lobster is a Feishu productivity automation skill that helps create Feishu documents, organize meeting notes into categorized todos, set document permissions, and support scheduled daily todo pushes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ybridge](https://clawhub.ai/user/ybridge)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators who use OpenClaw with Feishu can use this skill to generate daily todo documents, summarize meeting action items, classify tasks by work module, and share editable Feishu documents with a configured user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Embedded Feishu credentials and fixed recipient identifiers could expose a private integration or route generated documents to the wrong account.

Mitigation: Rotate the exposed Feishu secret, remove hard-coded credentials and OpenIDs, and require installer-owned configuration before installation.

Risk: Automatic document sharing and scheduled automation can change Feishu permissions or publish links without enough user awareness.

Mitigation: Require explicit confirmation before document sharing or scheduled execution, and review requested Feishu permissions against the intended workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ybridge/skills/wong-super-lobster)
- [ClawHub publisher profile](https://clawhub.ai/user/ybridge)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration examples, shell commands, and JavaScript/Feishu API snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The included script can create Feishu documents, convert markdown content to document blocks, set permissions for a fixed OpenID, and print the generated document link.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
