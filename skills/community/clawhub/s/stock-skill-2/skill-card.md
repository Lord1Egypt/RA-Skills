## Description:

A Stock helps agents retrieve, format, and briefly interpret A-share market data including stock quotes, intraday prices, market summaries, sector boards, Dragon Tiger List activity, and abnormal order-book movements through the Aipmedia stock API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wwzzsl](https://clawhub.ai/user/wwzzsl)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to answer Chinese A-share market questions by calling the configured stock-data API, formatting returned JSON into tables, and adding short data interpretations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API key could be exposed to an unintended host if request destinations are not constrained.

Mitigation: Enforce an allowlist of /api/stock endpoints and verify the final origin is api.aipmedia.cn before attaching ASTOCK_API_KEY.

Risk: Unpinned npx tsx execution can introduce dependency or runner drift at install or runtime.

Mitigation: Replace unpinned npx tsx with a locked local dependency or a compiled runner before deployment.

Risk: The security verdict is suspicious and requires review before installation.

Mitigation: Review and scan the skill before deployment, using evidence.security guidance as the acceptance checklist.

## Reference(s):

- [A Stock ClawHub Skill Page](https://clawhub.ai/wwzzsl/skills/stock-skill-2)
- [Publisher Profile](https://clawhub.ai/user/wwzzsl)
- [Project Homepage](https://github.com/wwzzsl/skills.git)
- [API Fields Reference](references/api_fields.md)
- [Aipmedia API Portal](https://aipmedia.cn/)
- [Aipmedia Stock API](https://api.aipmedia.cn)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown tables and concise prose based on JSON API responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ASTOCK_API_KEY and uses the Aipmedia stock API for market data.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata); source skill frontmatter reports 1.0.0

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
