## Description:

Use when researchers need Chinese academic prose translated into publication-oriented English or English manuscript paragraphs and complete sections polished for SCI, SSCI, or interdisciplinary submission.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yila-ai](https://clawhub.ai/user/yila-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External researchers and academic authors use this skill to translate Chinese academic prose into publication-oriented English or polish English manuscript paragraphs and full sections while preserving scientific claims, numbers, citations, limitations, and conclusions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Language polishing can accidentally change claim strength, causal meaning, citations, or quantitative details.

Mitigation: Use the skill's preservation ledger and audit contract, and surface author queries when source meaning is ambiguous.

Risk: Users may expect bilingual output or non-English final prose even though the skill defaults to polished academic English.

Mitigation: State bilingual or non-English output requirements explicitly when invoking the skill.

## Reference(s):

- [Preservation invariants](references/invariants.md)
- [Output contract](references/output-contract.md)
- [Rhetorical routing](references/rhetorical-routing.md)
- [Corpus and distillation method](references/corpus-method.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown containing polished English, key changes, a preservation audit, and author queries when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to English-only output for Chinese input unless the user explicitly requests bilingual or non-English output.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
