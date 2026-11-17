## Description:

Selection Agent supports product-selection research across keyword research, SEO analysis, competitor analysis, and TrendPlus data, with Chinese and English trigger terms and a required AGENT_CONFIG.md setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lygjoey](https://clawhub.ai/user/lygjoey)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, SEO, and product-growth teams use this skill to run product-selection research that combines keyword, competitor, advertising, and deduplication signals into prioritized opportunities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to read broad local secrets and run unaudited external code before research.

Mitigation: Install only in a controlled environment where /tmp/powerful-trendplus is trusted, immutable, and owned by the user; use least-privilege credentials and require explicit confirmation before secret access, writes, internal database use, or third-party API calls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lygjoey/skills/selection-agent)
- [Publisher profile](https://clawhub.ai/user/lygjoey)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and structured JSON research records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses configured external APIs and credentials; results depend on the trusted local project and available data-source access.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
