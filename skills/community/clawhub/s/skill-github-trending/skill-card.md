## Description:

Fetches GitHub Trending repositories by daily, weekly, or monthly stars gained, with optional programming-language filtering and text or JSON output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[callmegod66](https://clawhub.ai/user/callmegod66)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve current GitHub Trending repositories, optionally scoped by time period and programming language, for summaries, lists, reports, or downstream JSON processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes outbound requests to public GitHub Trending pages and depends on the current GitHub HTML structure.

Mitigation: Run it only where outbound GitHub access is acceptable, retry transient failures, and review parser behavior if GitHub page structure changes.

## Reference(s):

- [GitHub Trending](https://github.com/trending)
- [ClawHub Skill Page](https://clawhub.ai/callmegod66/skills/skill-github-trending)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples; the script can emit human-readable text or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results include repository rank, full name, URL, description, language, total stars, stars gained, selected period, and UTC+8 timestamp when JSON output is used.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
