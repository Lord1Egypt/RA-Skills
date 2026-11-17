## Description:

Analyze Claude Usage and Cost JSON, show actual Anthropic spend in lattes, and estimate how many lattes the user could recover.

This skill is ready for commercial/non-commercial use.

## Publisher:

[margaretzybgl](https://clawhub.ai/user/margaretzybgl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, finance users, and Claude Platform operators use this skill to analyze local Anthropic Cost Report and Usage Report JSON exports, summarize spend in latte equivalents, and identify directional recovery opportunities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent needs local access to the Claude billing JSON files selected by the user.

Mitigation: Use only the intended exports, avoid sharing raw billing data, and rely on the local analysis path described by the security evidence.

Risk: Generated reports include a third-party website link.

Mitigation: Treat the link as an optional external action and do not upload billing exports to any external site unless it is independently trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/margaretzybgl/skills/take-back-my-latte-from-claude)
- [Supported input formats](references/input-formats.md)
- [Take Back My Latte website](https://take-back-my-latte.margaret-zybgl.chatgpt.site)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report grounded in local JSON analysis, with concise warnings and recovery guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Report is intended to stay under 250 words by default and includes a local-analysis privacy notice.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
