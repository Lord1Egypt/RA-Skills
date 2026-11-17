## Description:

Ruiping helps agents turn user-provided or searched Chinese news items into opinionated commentary with source context, trend analysis, affected-party impact, and decision guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leslietong2046-ship-it](https://clawhub.ai/user/leslietong2046-ship-it)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to evaluate current events, business news, policy changes, and industry developments by producing structured Chinese commentary and practical next-step guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Opinionated commentary may include incorrect facts, unsupported forecasts, or misleading financial and industry recommendations.

Mitigation: Require users to verify cited facts and sources, treat recommendations as commentary rather than professional advice, and apply human review before acting on high-impact decisions.

Risk: The artifact includes an unused, range-based requests dependency that can add packaging surface area in stricter environments.

Mitigation: Remove the dependency if unused or pin and scan it before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leslietong2046-ship-it/skills/ruiping-skill)
- [README](README.md)
- [Skill instructions](SKILL.md)
- [AI regulation example](examples/ai-regulation.md)
- [Tesla price-cut example](examples/tesla-price-cut.md)
- [Daily commentary example](references/examples/锐评日报_20260503.md)
- [Formatter script](scripts/ruiping.py)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Structured Markdown commentary in Chinese]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include source summaries, short conclusions, impact analysis, forecasts, audience-specific recommendations, and optional Markdown file output when the bundled formatter script is used.]

## Skill Version(s):

2.0.4 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
