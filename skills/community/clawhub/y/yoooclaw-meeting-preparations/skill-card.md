## Description:

This skill helps users prepare for meetings by generating a concise briefing from recent phone notifications and, when relevant, recent web search results about the meeting topic and people of interest.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vivalavida-say-hi](https://clawhub.ai/user/vivalavida-say-hi)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and external users can use this skill shortly before a meeting to consolidate relevant recent notifications and public updates into an overview, key findings, and suggested discussion points.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill searches recent phone notifications, which may expose sensitive personal or business information.

Mitigation: Install and use it only where notification access is approved, and review generated briefings before sharing them outside the meeting context.

Risk: The skill may attempt to install an unpinned web-search dependency automatically if the dependency is missing.

Mitigation: Preinstall or approve the web-search dependency through a controlled process before use, or run the skill in a mode where web search is unavailable and clearly disclosed.

Risk: The briefing may combine notification content and web results into concise conclusions that omit context.

Mitigation: Treat the output as meeting preparation guidance and verify important claims against the underlying notifications or search sources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vivalavida-say-hi/skills/yoooclaw-meeting-preparations)
- [Publisher profile](https://clawhub.ai/user/vivalavida-say-hi)
- [byted-web-search dependency source](https://skills.volces.com/skills/bytedance/agentkit-samples)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown briefing in conversation text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The briefing is organized as meeting topic, global overview, key findings by theme, and suggested points to watch.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
