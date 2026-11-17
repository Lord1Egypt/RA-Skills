## Description:

Monitors Amazon competitors by resolving brands or ASINs, analyzing traffic keywords and customer reviews, and producing competitor intelligence with action recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beyondbright](https://clawhub.ai/user/beyondbright)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, brand operators, and developers use this skill to monitor Amazon competitors by brand or ASIN, compare traffic keywords and review themes, estimate sales and revenue signals, and turn findings into positioning and advertising recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The executable imports an external data-layer dependency that is not packaged with the skill.

Mitigation: Install and run the skill only where that dependency is trusted, packaged or pinned, and not loaded from a shared writable path.

Risk: Competitor targets such as brands and ASINs may be sent to external commerce-data providers.

Mitigation: Use only data that the operator is authorized to analyze and review external API data-handling requirements before deployment.

Risk: Sales, revenue, keyword, and review-derived recommendations may be estimates or incomplete competitive signals.

Mitigation: Treat generated recommendations as decision support and review them against authoritative marketplace and business data before acting.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/beyondbright/skills/walter-competitor-monitor)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown or structured JSON-style report with console summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Analyzes one or more Amazon brands or ASINs per request; depends on external commerce-data access.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
