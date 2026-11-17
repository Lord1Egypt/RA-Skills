## Description:

Make fictional text conversations that open as editable Textmock links, or edit and render an existing Textmock conversation through its browser API or Mac command.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hraness](https://clawhub.ai/user/hraness)

### License/Terms of Use:

MIT-0

## Use Case:

People and agents use this skill to create fictional iMessage-style conversation previews and to work with existing Textmock conversations. Developers can use its helper to encode a text-only conversation as an editable link.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security verdict is benign with medium confidence because the bundled helper was only partly interpreted during analysis.

Mitigation: Consider this unresolved evidence gap when deciding whether to install; the benign verdict does not mean risk-free.

Risk: Anyone who receives a full share link can read the conversation text encoded in it.

Mitigation: Use fictional content unless the user asks to share their own material, and avoid sending full links to unintended recipients.

## Reference(s):

- [Textmock](https://textmock.com)
- [Use Textmock from an agent](https://textmock.com/docs/agents)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, URLs]

**Output Format:** [Markdown guidance, JSON conversation input, and editable Textmock links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Links contain the conversation text in the URL fragment; anyone with the full link can read it.]

## Skill Version(s):

0.1.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
