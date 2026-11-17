## Description:

Rag Evaluator is a local command-line utility for logging, reviewing, searching, and exporting RAG evaluation, benchmark, prompt, cost, and usage records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain1](https://clawhub.ai/user/bytesagain1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI engineers use this skill to track RAG pipeline evaluation notes, benchmarks, prompt experiments, cost and usage data, and export local records for reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release metadata describes a Python SDK, while the artifact behaves as a local Bash logging and export CLI.

Mitigation: Review and present the release as a local plaintext logging utility, and verify public metadata before promotion or installation.

Risk: Prompt, evaluation, retrieved document, cost, usage, or credential-like entries may be stored in plaintext under ~/.local/share/rag-evaluator and included in full-history exports.

Mitigation: Do not log secrets, regulated data, proprietary prompts, retrieved documents, or credentials unless that local storage and export behavior is acceptable.

Risk: CSV, JSON, and text exports may expose sensitive logged content when opened in other tools or shared.

Mitigation: Review exported files before opening them in spreadsheet tools, attaching them to reports, or sharing them outside the intended audience.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bytesagain1/skills/rag-evaluator)

## Skill Output:

**Output Type(s):** [Text, Files, Shell commands, Configuration instructions]

**Output Format:** [Plain text stdout and local JSON, CSV, or TXT export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores command logs and exports under ~/.local/share/rag-evaluator by default.]

## Skill Version(s):

2.0.0 (source: SKILL.md frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
