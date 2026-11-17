## Description:

Research a topic via web search, auto-match a related GIF, and log structured notes to Bear using a customizable template.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and productivity-focused users use this skill to collect web research on a topic, assemble a templated Markdown note, optionally attach a related GIF, and create a Bear note through grizzly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research topics are sent to Brave and, when GIF matching is enabled, to Giphy.

Mitigation: Use non-sensitive topics and disable optional GIF lookup unless sharing the topic with Giphy is acceptable.

Risk: The skill relies on API keys for Brave and optional Giphy access.

Mitigation: Use narrowly scoped keys with quotas and rotate them if they may have been exposed.

Risk: The security summary says third-party API use and credential handling are under-disclosed.

Mitigation: Review the script and update release metadata so API use, credential handling, and expected network behavior are clear before routine deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/research-logger-v2)
- [Brave Search API endpoint used by the script](https://api.search.brave.com/res/v1/web/search)
- [Giphy Search API endpoint used by the script](https://api.giphy.com/v1/gifs/search)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown note content and command-line status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a topic argument and optional comma-separated tags; writes a Markdown note and can create a Bear note when grizzly is available.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
