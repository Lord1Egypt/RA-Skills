## Description:

Research Pipeline automates literature discovery, paper summarization, Obsidian note creation, and brief research digests for Chopin's academic work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shaopanguo](https://clawhub.ai/user/shaopanguo)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and academic agents use this skill to find recent papers, summarize their relevance, create Obsidian literature notes, maintain a research topic tracker, and report concise updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can write research notes and send Feishu digests without clear user opt-in or destination scoping.

Mitigation: Configure the skill to ask before writing notes or sending messages, and restrict destinations to explicitly approved Obsidian vault paths and Feishu recipients.

Risk: Research topics, paper selections, and Obsidian vault links may expose private academic interests or work in progress.

Mitigation: Review the skill before installation and use only approved research topics, vault locations, and sharing channels.

Risk: Recurring cron use may repeatedly search and report on topics beyond the user's current intent.

Mitigation: Limit scheduled runs to approved topics and require review of tracker changes before expanding or changing the monitored scope.

## Reference(s):

- [Research Topics Profile](references/research-topics.md)
- [ClawHub Skill Page](https://clawhub.ai/shaopanguo/skills/research-pipeline)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Markdown notes, tracker updates, and concise text digests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create one Obsidian note per paper, update a research topic tracker, and send a brief Feishu digest when configured.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
