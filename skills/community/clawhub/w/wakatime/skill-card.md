## Description:

WakaTime API integration with managed OAuth for retrieving coding statistics, productivity metrics, language and editor usage, project time, and daily summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill in OpenClaw to connect WakaTime through ClawLink and retrieve read-only coding activity, productivity, project, language, editor, goal, insight, and summary data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and trusts an external ClawLink plugin that brokers OAuth access to WakaTime data.

Mitigation: Install only from a trusted ClawLink plugin source, prefer a pinned and reviewed plugin version when available, and review the plugin before deployment.

Risk: The artifact describes private WakaTime activity-data reads as safe and requiring no confirmation.

Mitigation: Require explicit user confirmation before retrieving profile, project, machine, goal, insight, or summary data.

## Reference(s):

- [WakaTime API Docs](https://wakatime.com/developers)
- [ClawLink Docs](https://docs.claw-link.dev/openclaw)
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=wakatime)
- [ClawHub WakaTime Skill](https://clawhub.ai/hith3sh/skills/wakatime)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with tool-call examples and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only WakaTime API data returned through ClawLink; OAuth scopes may limit summaries, goals, and insights.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
