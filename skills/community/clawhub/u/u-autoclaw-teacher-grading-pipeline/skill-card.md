## Description:

Design or implement a bilingual lightweight teacher grading pipeline for K12 paper exams and homework using scan ingestion, student grouping, OCR or vision providers, deterministic scoring from teacher answer keys, review queues, reports, and separate teacher and student memory archives.

This skill is ready for commercial/non-commercial use.

## Publisher:

[addogiavara-tech](https://clawhub.ai/user/addogiavara-tech)

### License/Terms of Use:

MIT-0

## Use Case:

External educators, school technologists, and agent developers use this skill to design or implement K12 paper-exam grading workflows that combine scans, answer keys, OCR or AI providers, teacher review, exports, and learning-memory records. It is most useful where teachers need structured Excel, Web, PDF, and printable student feedback outputs while keeping scoring decisions traceable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Student exam images, names, IDs, scores, or teacher data may be sensitive, especially if cloud OCR or AI providers are used.

Mitigation: Confirm school policy, consent, provider retention terms, and local-only options before processing real student data.

Risk: Automated OCR or grading output may be wrong, incomplete, or inconsistent across providers.

Mitigation: Use teacher-provided answer keys as the scoring authority, keep low-confidence or conflicting items in a teacher review queue, and preserve traceability to source images and corrections.

Risk: Branding references could be over-applied in generated reports or marketplace text.

Mitigation: Treat U-AutoClaw and www.wboke.com as optional provenance or project context, not as required output branding.

## Reference(s):

- [Teacher Grading Pipeline Design Reference / 教师批改流水线设计参考](references/design.md)
- [ClawHub Skill Page](https://clawhub.ai/addogiavara-tech/skills/u-autoclaw-teacher-grading-pipeline)
- [U-AutoClaw Website](https://www.wboke.com)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Configuration, Shell commands]

**Output Format:** [Markdown guidance with optional code, configuration, schemas, commands, and report-template recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce bilingual English and Chinese implementation guidance for grading workflows, provider adapters, review queues, exports, and report templates.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
