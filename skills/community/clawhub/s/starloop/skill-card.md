## Description:

Starloop reads a StarFocus todo folder and returns a ranked Telegram Markdown recommendation for the next task to work on.

This skill is ready for commercial/non-commercial use.

## Publisher:

[homostellaris](https://clawhub.ai/user/homostellaris)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators working with StarFocus todo folders use this skill to choose the next tractable task by filtering, ranking, and summarizing todos. It also notes blocked high-priority work and can suggest a ClawHub skill search result as a possible fix.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may run an unpinned external CLI command with a search term derived from todo content.

Mitigation: Review the skill before installation; prefer a pinned, trusted CLI or non-executing API, and pass missing-capability queries as validated structured arguments.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/homostellaris/starfocus/tree/master/agent/skills/starloop)
- [ClawHub skill page](https://clawhub.ai/homostellaris/skills/starloop)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Telegram Markdown message with task filenames and optional inline shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns up to three candidate tasks and preserves each todo's full unique-ID-suffixed filename.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
