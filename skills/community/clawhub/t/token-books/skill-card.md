## Description:

See where your AI money goes across OpenAI, Anthropic, Google, and other providers with per-provider breakdowns, per-model costs, budget tracking, and waste detection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theshadowrose](https://clawhub.ai/user/theshadowrose)

### License/Terms of Use:

MIT

## Use Case:

Developers, operators, and small teams use this skill to import exported AI billing data, analyze local spend across providers, track budgets, and generate dashboard reports for cost review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe HTML report generation can allow malicious or tampered billing data to run browser code when a generated dashboard is opened.

Mitigation: Use only billing exports you created or trust, and avoid opening generated dashboards from untrusted data until the HTML escaping issue is fixed.

Risk: Billing exports, imported JSON, and generated dashboards can expose sensitive financial and operational usage information.

Mitigation: Keep input and output files local and access-controlled, and review dashboards before sharing them outside the intended team.

Risk: Spend analysis can be inaccurate when imports are duplicated, costs are missing, timestamps differ by timezone, or model pricing is stale.

Mitigation: Spot-check imported data against provider dashboards, avoid overlapping imports, prefer provider-calculated costs, and update pricing configuration before relying on estimates.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/theshadowrose/skills/token-books)
- [README](artifact/README.md)
- [Limitations](artifact/LIMITATIONS.md)
- [License](artifact/LICENSE.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python CLI commands, configuration examples, JSON analysis output, and optional local HTML dashboard files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local exported billing data; no network access is described by the artifact documentation.]

## Skill Version(s):

1.0.0 (source: artifact/SKILL.md frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
