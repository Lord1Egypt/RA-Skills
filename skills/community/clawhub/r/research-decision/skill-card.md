## Description:

Research Decision helps agents investigate complex technical choices or troubleshooting questions online, compare high-quality Chinese and English sources, and return evidence-backed recommendations, risks, and next steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnna2725](https://clawhub.ai/user/krishnna2725)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and technical decision makers use this skill to evaluate tools, upgrades, compatibility questions, architecture tradeoffs, community signals, and difficult bugs that require current web research and cross-source verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may perform web searches and local version or dependency checks, which can expose private logs, package names, repository details, or proprietary context if included in queries or inspection output.

Mitigation: Use it only where local inspection is acceptable, redact sensitive details before web searches, and avoid including private logs or proprietary context unless that disclosure is intended.

## Reference(s):

- [Query Patterns](references/query-patterns.md)
- [Issue Triage](references/issue-triage.md)
- [ClawHub skill page](https://clawhub.ai/krishnna2725/skills/research-decision)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown research report with cited conclusions and optional shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include source links, risk notes, known issues, workarounds, and next-step recommendations.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
