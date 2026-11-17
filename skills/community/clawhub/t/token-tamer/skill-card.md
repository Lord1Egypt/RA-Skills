## Description:

Token Tamer helps agents monitor, budget, and optimize AI API spending across providers by tracking calls, enforcing budgets, detecting waste, and recommending optimizations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theshadowrose](https://clawhub.ai/user/theshadowrose)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, teams, and researchers use this skill to add local AI API cost tracking, budget checks, reporting, and waste detection to provider-agnostic API workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Budget controls may under-report spending, so the skill should not be the only hard spending limit.

Mitigation: Keep provider-side budgets or billing alerts enabled and reconcile Token Tamer totals against provider dashboards before relying on enforcement.

Risk: The kill switch is application-level and advisory unless every API path calls the check and accounting issues are fixed.

Mitigation: Wrap all AI API calls with the pre-call budget check and treat provider-side controls as the authoritative backstop.

Risk: The local JSON usage file and task, session, or metadata fields may expose usage details or sensitive context.

Mitigation: Protect the usage file with appropriate filesystem permissions and avoid storing secrets, customer data, or sensitive prompts in logged fields.

Risk: Manual pricing data and self-reported token counts can become stale or incomplete.

Mitigation: Update model pricing regularly and compare logged totals with provider billing dashboards to identify drift.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/theshadowrose/skills/token-tamer)
- [Publisher profile](https://clawhub.ai/user/theshadowrose)
- [README](artifact/README.md)
- [Limitations](artifact/LIMITATIONS.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command snippets; the bundled scripts can also emit text or JSON reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local JSON usage data and user-configured model pricing; the artifact requires no external Python dependencies.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
