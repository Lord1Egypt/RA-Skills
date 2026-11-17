## Description:

Use this skill when a real estate investor, agent, or analyst needs to underwrite a residential rental property, compute NOI, cap rate, cash-on-cash return, DSCR, a 5-year pro-forma, sensitivity scenarios, and a go/no-go memo with deal-breaker flags.

This skill is ready for commercial/non-commercial use.

## Publisher:

[archlab-space](https://clawhub.ai/user/archlab-space)

### License/Terms of Use:

MIT-0

## Use Case:

External real estate investors, agents, and analysts use this skill to evaluate residential rental opportunities before submitting an offer, renegotiating, or walking away. It gathers property and financing assumptions, confirms them, then produces an underwriting memo with metrics, pro-forma projections, sensitivity analysis, red flags, and a verdict.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for property, financing, and personal capital details that may be private.

Mitigation: Use a property code instead of a full address when possible and avoid sharing unnecessary identifying or financial details.

Risk: The memo may rely on assumptions or user-provided figures that are incomplete, stale, or optimistic.

Mitigation: Independently verify rent comps, taxes, insurance quotes, HOA rules, STR regulations, financing terms, and inspection findings before using the memo to make an offer or financing decision.

Risk: The output could be mistaken for investment, tax, or legal advice.

Mitigation: Treat the memo as decision support only and review legal, tax, regulatory, and financing questions with qualified local professionals.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/archlab-space/skills/rental-property-underwriter)
- [README](artifact/README.md)
- [Changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown underwriting memo with tables and plain-English verdict]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes assumption confirmation, formulas for key metrics, a 5-year pro-forma, sensitivity matrix, deal-breaker flags, unresolved information, and a draft-only reminder that outputs are not investment, tax, or legal advice.]

## Skill Version(s):

0.1.2 (source: server release metadata and changelog, released 2026-05-28)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
