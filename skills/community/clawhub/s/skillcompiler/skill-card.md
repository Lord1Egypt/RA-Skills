## Description:

Compiles prompts or multi-source content into reusable AI skill packages with evidence grading, honest boundaries, modular architecture, and validation guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qomob](https://clawhub.ai/user/qomob)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to convert reusable prompts, documents, URLs, media-derived content, or existing source material into structured skill packages. It is intended for skill compilation workflows, not one-shot question answering, translation, prompt wording optimization, or authoring unrelated skills from scratch.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may fetch URLs, clone repositories, or read user-selected local project files as part of compiling source material.

Mitigation: Use trusted or reviewed inputs, avoid private or sensitive sources unless required, and confirm any network or local-file access before use.

Risk: Untrusted source text can be transformed into new skill instructions and may carry misleading, unsafe, or overbroad behavior into the generated package.

Mitigation: Review generated skills before installing or running them, and keep evidence grading and honest-boundary sections intact.

Risk: Security evidence marks the release as suspicious because URL, file, and untrusted content handling need careful review.

Mitigation: Treat generated outputs as drafts, scan them before deployment, and restrict use to inputs and repositories the operator is comfortable processing.

## Reference(s):

- [Server-resolved source repository](https://github.com/qomob/SkillCompiler)
- [ClawHub skill listing](https://clawhub.ai/qomob/skills/skillcompiler)
- [Evidence grading reference](references/evidence-grading.md)
- [Honest boundaries reference](references/honest-boundaries.md)
- [Parallel extractors reference](references/parallel-extractors.md)
- [Meta-reflection reference](references/meta-reflection.md)
- [Ingestion pass reference](references/pass-ingestion.md)
- [Validation pass reference](references/pass-6-validate.md)
- [Skill output template](templates/skill-md-template.md)
- [Intermediate representation schema](schemas/ir-schema.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown skill package files with structured JSON schema guidance and validation reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated skill files, folder structure guidance, evidence grading, validation results, and review notes.]

## Skill Version(s):

1.2.2 (source: server release metadata; artifact frontmatter says 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
