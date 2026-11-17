## Description:

Generate professional presentation slides from a topic or outline as complete decks that users can view, edit, and download in YouMind.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dophinl](https://clawhub.ai/user/dophinl)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to turn a presentation topic, outline, or key points into a generated slide deck through YouMind. It is intended for slide creation workflows that can tolerate sending the supplied topic or outline to YouMind.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may send presentation topics, outlines, or key points to YouMind.

Mitigation: Avoid sensitive or proprietary presentation content unless YouMind is trusted and approved for that use.

Risk: The skill can install a persistent global npm CLI.

Mitigation: Install and review a pinned @youmind-ai/cli version before enabling the skill in managed environments.

Risk: Broad slide and presentation triggers may activate this workflow for ordinary requests.

Mitigation: Confirm intent before sending user content to YouMind when a request is ambiguous.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dophinl/skills/youmind-slides-generator)
- [Setup guide](references/setup.md)
- [Error handling](references/error-handling.md)
- [Long-running tasks](references/long-running-tasks.md)
- [YouMind](https://youmind.com?utm_source=youmind-slides-generator)
- [YouMind CLI package](https://www.npmjs.com/package/@youmind-ai/cli)
- [YouMind API keys](https://youmind.com/settings/api-keys?utm_source=youmind-slides-generator)
- [YouMind skills gallery](https://youmind.com/skills?utm_source=youmind-slides-generator)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown status messages with shell commands and a YouMind result link]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a slide deck in a YouMind board and returns a link for viewing, editing, and downloading.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
