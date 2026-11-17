## Description:

Assess your Agent deployment against security risks using Trent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trent-ai-release](https://clawhub.ai/user/trent-ai-release)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to audit OpenClaw deployments, identify misconfigurations and chained attack paths, and receive severity-rated findings with fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends redacted OpenClaw metadata and packaged local skill/code archives to Trent for analysis.

Mitigation: Review the generated .skill archives and proceed only if sharing that material with Trent is acceptable.

Risk: Custom TRENT_CHAT_API_URL or TRENT_AGENT_API_URL values can receive the Trent API key.

Mitigation: Use the default Trent endpoints, or set custom endpoints only when they are trusted and intended to receive TRENT_API_KEY.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/trent-ai-release/skills/trentclaw)
- [Trent](https://trent.ai)
- [Trent OpenClaw API key setup](https://trent.ai/openclaw/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance, Analysis]

**Output Format:** [Markdown with severity-grouped findings, inline bash snippets, JSON summaries, and diff snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings are grouped by CRITICAL, HIGH, MEDIUM, and LOW severity.]

## Skill Version(s):

1.4.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
