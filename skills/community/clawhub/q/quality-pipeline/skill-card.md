## Description:

A Chinese-language multi-layer quality assurance pipeline for cross-checking formal deliverables such as academic papers, official documents, and reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luaqnyin](https://clawhub.ai/user/luaqnyin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators of Chinese-language writing workflows use this skill to run layered QA on formal deliverables, including existence checks, authenticity checks, formatting and citation review, hallucination review, expert-style review, and final delivery readiness.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can trigger broad review steps and additional review agents, which may expose more files or consume more review effort than intended.

Mitigation: Confirm the target file scope, citation and style requirements, and whether multi-agent review should run before invoking the full pipeline.

Risk: The skill is tuned for Chinese-language academic, document, and report QA, so results may be less useful for non-Chinese or unrelated deliverables.

Mitigation: Use it for the documented Chinese-language deliverable types, or explicitly restate the expected standards when applying it elsewhere.

## Reference(s):

- [Anti-Hallucination Checklist](references/anti-hallucination.md)
- [Statistical Tables Standard](references/statistical-tables.md)
- [Writing Standards](references/writing-standards.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-style review results, checklists, scores, and revision instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask separate review agents to inspect deliverables and summarize pass/fail findings.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
