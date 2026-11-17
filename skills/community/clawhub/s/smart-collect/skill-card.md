## Description:

Smart Collect analyzes and summarizes URL content, saves structured Markdown notes to Obsidian, and schedules review reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nbutmickey](https://clawhub.ai/user/nbutmickey)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals and knowledge workers use this skill to collect web links, generate summaries and tags, store them as Obsidian Markdown notes, and receive scheduled review reminders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch arbitrary network URLs, including internal or private URLs if supplied.

Mitigation: Use only URLs you trust and avoid internal or private URLs.

Risk: Fetched content may be sent to DeepSeek when LLM configuration is enabled.

Mitigation: Do not process sensitive content with LLM configuration enabled unless that use is approved.

Risk: Unvalidated inputs can read or rewrite Markdown files outside the intended storage folder.

Mitigation: Use trusted storage paths and fix collection ID handling before relying on the skill with private Obsidian vaults or shared command inputs.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown notes, command-line text, and JSON-style configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May fetch web content and may call DeepSeek for summaries when LLM configuration is enabled.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
