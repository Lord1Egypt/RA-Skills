## Description:

Analyzes primary-market investment opportunities for VC, PE, strategic capital, industrial capital, and government-guided funds using founder, industry, government-fit, financial, industrial-capability, comparison, sensitivity, and memo workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[perrykono-debug](https://clawhub.ai/user/perrykono-debug)

### License/Terms of Use:

MIT-0

## Use Case:

Investment professionals, corporate strategy teams, and government-guided fund teams use this skill to evaluate private-market projects, compare investment targets, surface diligence gaps, and draft investment memos or report-ready summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can save investment analyses, preferences, and corrections across sessions without clear opt-in controls.

Mitigation: Disable or constrain memory and self-improvement behavior unless retention is explicitly intended, and define storage and deletion controls before using sensitive information.

Risk: Confidential deal materials, founder diligence, financial projections, or internal investment notes may be exposed if used with unconstrained tools or persistent memory.

Mitigation: Avoid non-public information unless the deployment has approved confidentiality controls, tool restrictions, and retention limits.

Risk: Investment conclusions may be misleading when public data is incomplete, stale, or estimated.

Mitigation: Require source checks, label estimates clearly, and treat outputs as diligence support rather than final investment decisions.

## Reference(s):

- [AGENTS.md - investment analyst workspace](references/agents.md)
- [IDENTITY.md - industrial investment analyst identity](references/identity.md)
- [SOUL.md - investment analysis workflow](references/soul.md)
- [TOOLS.md - investment analyst tool notes](references/tools.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Markdown investment memos, comparison tables, JSON-like scoring blocks, and optional report-ready exports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should distinguish sourced facts from estimates and include diligence gaps, confidence levels, and investment risks.]

## Skill Version(s):

1.2.0 (source: server release evidence and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
