## Description:

Convert agent execution plans into MADR-format Architecture Decision Records for audit trails and architecture progression.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rawc0der](https://clawhub.ai/user/rawc0der)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to convert GSD phase plans, Cursor CreatePlan files, or generic markdown plans into numbered MADR Architecture Decision Records and keep the ADR index current.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes ADR documentation files and may update an ADR index in the repository.

Mitigation: Review the generated ADR and index changes before committing them.

Risk: Sparse or ambiguous source plans can produce incomplete ADR sections or TODO markers.

Mitigation: Provide a clear source plan or decision description and review any TODO-marked sections before using the ADR as an architecture record.

## Reference(s):

- [MADR Template](references/madr-template.md)
- [ADR Index Template](assets/adr-index-template.md)
- [MADR Format](https://adr.github.io/madr/)
- [ClawHub Skill Page](https://clawhub.ai/rawc0der/skills/spec-to-adr)

## Skill Output:

**Output Type(s):** [markdown, text, guidance]

**Output Format:** [MADR markdown ADR files, an ADR index entry, and a concise text report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes ADR documentation files and may update an ADR index in the target repository.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
