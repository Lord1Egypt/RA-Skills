## Description:

Searches the SumoNoteBook knowledge base and returns the three most relevant text previews as context for the agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sumo0221](https://clawhub.ai/user/sumo0221)

### License/Terms of Use:

MIT-0

## Use Case:

Users and agents use this skill to query a local SumoNoteBook Markdown knowledge base and include relevant notebook snippets as context when answering questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Retrieved snippets may surface private notebook content in agent context.

Mitigation: Avoid indexing confidential notes unless you are comfortable having them surfaced, and treat returned snippets as potentially private.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-style text with retrieved snippet previews and optional shell commands for maintenance checks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns up to three matching notebook snippets with relevance scores and preview text.]

## Skill Version(s):

1.0.0 (source: release evidence and artifact/SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
