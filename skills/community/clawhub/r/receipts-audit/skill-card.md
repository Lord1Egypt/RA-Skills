## Description:

Audits a document against provided sources by extracting factual claims, grading each against evidence, ranking unsupported or contradicted claims, recommending fixes or drops, and reporting an honesty score.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohitagw15856](https://clawhub.ai/user/mohitagw15856)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and review teams use this skill to fact-check reports, decks, posts, memos, or pages against the sources supplied with the audit and identify unsupported or contradicted factual claims.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The audit can mark true claims as unsupported when the user does not provide matching sources.

Mitigation: Provide the source set used by the document, and treat Unsupported as a sourcing gap rather than a finding of falsity.

Risk: Load-bearingness rankings and audience stakes can be inferred when not supplied, which may affect prioritization.

Mitigation: Provide audience stakes or review inferred stakes before using the ranking for publication or decision support.

## Reference(s):

- [Receipts Audit ClawHub skill page](https://clawhub.ai/mohitagw15856/skills/receipts-audit)
- [Receipts Audit homepage](https://mohitagw15856.github.io/pm-claude-skills/skill/receipts-audit.html)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown report with claim ledger tables, ranked failure list, fix-or-drop recommendations, and honesty score arithmetic]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Grades claims only against user-provided sources; if no sources are supplied, claims are marked unsupported.]

## Skill Version(s):

50.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
