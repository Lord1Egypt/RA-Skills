## Description:

Write, review, and export MBA and academic theses end-to-end as Word/DOCX, covering outline planning, node-by-node writing, chapter review, academic deep review, and formatted Word export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hehe973781230](https://clawhub.ai/user/hehe973781230)

### License/Terms of Use:

MIT-0

## Use Case:

External users, students, and developers use this skill to coordinate long-form MBA or academic thesis drafting, review, revision, and DOCX export through an OpenClaw-oriented multi-agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports overly broad local credential handling.

Mitigation: Review or patch credential handling before installation and run the skill in an isolated Python/OpenClaw environment.

Risk: The security evidence reports silent dependency installation.

Mitigation: Review dependency installation behavior before use and pin or preinstall approved dependencies in the target environment.

Risk: The security evidence reports unsafe state-file paths based on paper names.

Mitigation: Restrict paper names to safe identifiers and avoid path-like or shell-special characters.

Risk: The workflow may send thesis drafts, company details, prompts, or searches to external providers.

Mitigation: Avoid confidential thesis drafts or sensitive company information unless the user accepts the external-provider exposure.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hehe973781230/skills/thesis-workflow-v2)
- [ClawHub publisher profile](https://clawhub.ai/user/hehe973781230)
- [Loop design](references/loop-design.md)
- [Content hint fallback design](references/content-hint-fallback.md)
- [Chapter summary design](references/chapter-summary-design.md)
- [Thesis DOCX export sub-skill](thesis-docx-export/SKILL.md)
- [DOCX export checklist](thesis-docx-export/references/checklist.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance, CLI commands, workflow state files, review reports, and DOCX export artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces thesis workflow outputs with required human review checkpoints and guardrail checks before final Word export.]

## Skill Version(s):

2.1.2-beta.1 (source: server release metadata, SKILL.md metadata.clawdbot.version, README_EN.md, CHANGELOG-v2.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
