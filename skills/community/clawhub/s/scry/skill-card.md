## Description:

Research any topic across public and optional authenticated sources including Reddit, X, YouTube, GitHub, Hacker News, Bluesky, ArXiv, Dev.to, Polymarket, and more.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vihangd](https://clawhub.ai/user/vihangd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use Scry to gather and synthesize recent research signals for a topic across social, code, academic, news, and market sources. It is intended for multi-source research summaries, source statistics, and follow-up guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The default X/Twitter source path can attempt to use local browser session cookies without an explicit per-run opt-in.

Mitigation: Run with restricted sources or tier-1/public sources unless the user intentionally wants X/Twitter cookie-backed search.

Risk: Optional authenticated sources can expose local API keys or session-derived access to third-party services during research.

Mitigation: Prefer narrowly scoped API keys and review configured credentials before enabling optional sources.

## Reference(s):

- [ClawHub Scry skill page](https://clawhub.ai/vihangd/skills/scry)
- [Project homepage](https://github.com/khalidsh/scry-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown research summary with source statistics and concise attributions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke local scripts and web search; optional sources depend on available API keys, binaries, or local X/Twitter session credentials.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
