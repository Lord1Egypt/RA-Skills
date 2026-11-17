## Description:

Helps UIBC finance-domain reviewers assess memory-transfer identity and accountability against TH-FIN-001/002 criteria.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT

## Use Case:

Reviewers and agents working on UIBC finance-domain migration judgments use this skill to draft criteria-based decision rules, reproducible evidence packages, and failure-handling and accountability statements. It also provides a local check of the criteria file's structure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Contest judging guidance may be mistaken for general financial or legal compliance advice.

Mitigation: Use only for TH-FIN-001/002 migration-judgment tasks and obtain human review before using financial, legal, or contractual outputs.

Risk: A passing structural check may be mistaken for proof that a migration judgment is correct.

Mitigation: Treat PASS/FAIL as a criteria-file completeness check; independently review the evidence and accountability conclusion.

## Reference(s):

- [FIN domain criteria (TH-FIN-001/002)](判据_FIN.md)
- [ClawHub skill listing](https://clawhub.ai/zhaoxinghua09-cell/skills/uibc-team-fin)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Text]

**Output Format:** [Markdown judgments and evidence guidance; plain-text PASS/FAIL checks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Criteria checker reports five structural checks and a summary; it does not establish substantive compliance.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
