## Description:

Performs deep, vendor-specific technical research on products or solutions and produces structured reports that separate public facts from technical derivations across hardware, software, co-design, and benchmarking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[outdog-hwh](https://clawhub.ai/user/outdog-hwh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical researchers, and solution evaluators use this skill to investigate a specific vendor, product model, and application scenario, then produce a structured technical research report with source labels, derivation labels, information gaps, and benchmarking notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can delegate broad web and browser scraping for vendor research.

Mitigation: Review the target, source list, and scraping scope before execution, and avoid pages that require login, paywalls, CAPTCHAs, or private access.

Risk: Quick-start mode can proceed with default research settings after minimal input.

Mitigation: Use the onboarding questionnaire for sensitive or high-impact research so the vendor, model, scenario, priority, and granularity are explicit.

Risk: Research outputs can mix public facts, derivations, and information gaps.

Mitigation: Require reviewers to check source labels, derivation labels, and information-gap tables before using the report for decisions.

Risk: The workflow may store local evidence and run metadata.

Mitigation: Do not provide confidential PDFs or proprietary source material unless retention, access, and deletion controls are in place.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/outdog-hwh/skills/targeted-tech-research)
- [Prompt templates](artifact/references/prompts.md)
- [Execution rules](artifact/references/rules.md)
- [Dynamic site whitelist](artifact/references/dynamic_sites_whitelist.json)
- [Report template](artifact/assets/report_template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown technical research reports with source labels, derivation labels, tables, appendices, and occasional shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include information-gap tables, credibility scorecards, reproducible research recipes, and local run metadata when available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
