## Description:

Retrieves structured public Xiaohongshu data for keyword search, note details, creator posts, and note comments through the Guaikei API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content teams, marketers, and analysts use this skill to collect public Xiaohongshu search results, note details, creator post lists, and comments for content research, competitor monitoring, KOL screening, and trend analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends GUAIKEI_API_TOKEN in URL query parameters.

Mitigation: Use a limited-scope token where possible, avoid exposing command output or service logs, monitor quota usage, and rotate the token if logs or service access are a concern.

Risk: The skill sends Xiaohongshu keywords, note URLs, profile URLs, and returned public content through guaikei.com.

Mitigation: Confirm that third-party data processing is allowed for the use case, submit only public non-sensitive targets, and disclose the external API dependency to users.

Risk: The skill can collect large volumes of public social-media data.

Mitigation: Keep collection volumes proportionate to the task, respect applicable platform and organizational policies, and avoid unauthorized redistribution of collected data.

Risk: Server security evidence marks this release as suspicious.

Mitigation: Review the skill and scan results before deployment, with particular attention to credential handling and third-party data egress.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/engheng-art/skills/xhs-public-data-guaikei)
- [Guaikei API service](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Structured JSON responses with status, request metadata, results, and optional concise text guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0+ and GUAIKEI_API_TOKEN; successful runs may also save JSON result files under logs/.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence; artifact metadata reports 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
