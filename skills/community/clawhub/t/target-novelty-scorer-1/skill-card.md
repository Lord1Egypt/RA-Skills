## Description:

Scores the novelty of biological targets using a literature-mining-style Python workflow.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and research teams can use this skill to run a bounded target novelty scoring workflow and generate reviewable text, JSON, or CSV reports. Results require independent validation because security evidence says the implementation presents simulated biomedical literature scores as real PubMed or PMC analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can present simulated biomedical literature scores as real PubMed or PMC analysis.

Mitigation: Use it only for demonstration unless it is changed to query real sources, label provenance clearly, and validate results before any target-selection, literature-review, biomedical-reporting, investment, or research decision.

Risk: Generated CSV reports may be opened in spreadsheet software after using user-supplied target names.

Mitigation: Avoid opening CSV output from untrusted target names in spreadsheet software and write reports only to disposable workspace paths.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aipoch-ai/skills/target-novelty-scorer-1)
- [Audit Reference](references/audit-reference.md)
- [NCBI E-utilities API](https://eutils.ncbi.nlm.nih.gov/entrez/eutils)

## Skill Output:

**Output Type(s):** [Text, JSON, CSV, Shell commands, Guidance]

**Output Format:** [Markdown guidance with command examples and optional text, JSON, or CSV report output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write a report file when an output path is provided.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
