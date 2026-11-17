## Description:

Analyzes AI trends, industry disruption, and AI investment opportunities using a Wu Jun-inspired checklist focused on data advantage, application scenarios, commercial closure, and technical barriers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lj22503](https://clawhub.ai/user/lj22503)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to structure Chinese-language AI trend analysis, assess AI investment opportunities, and produce checklist-style reasoning for companies or industries. It is intended as a research framework and does not replace financial due diligence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AI trend and investment outputs could be mistaken for financial advice.

Mitigation: Treat outputs as a research checklist and pair them with independent due diligence, current market data, fundamentals analysis, and qualified financial review.

Risk: Technical forecasts and AI wave classifications can become outdated or uncertain.

Mitigation: Verify conclusions against current sources and revise assumptions before relying on the analysis.

Risk: Running the helper with --search may query an external searxng-based search tool if the sibling skill exists.

Mitigation: Use --search only when sending the topic to the configured search service is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lj22503/skills/wu-ai)
- [Publisher profile](https://clawhub.ai/user/lj22503)
- [AI trend analysis template](artifact/templates/ai-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Chinese-language Markdown checklists, investment-analysis guidance, and optional terminal text output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The helper script can optionally use --search to query a sibling searxng-based search tool when that dependency exists.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
