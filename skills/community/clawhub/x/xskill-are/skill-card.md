## Description:

XSkill ARE evaluates AI agent skills across business value, prompt quality, robustness, safety, composability, and cost, producing structured scores, HRR tiers, and fatal-flaw reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qomob](https://clawhub.ai/user/qomob)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, marketplace reviewers, and skill maintainers use this skill to assess AI skill quality, reliability, safety, and readiness before release or adoption.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scores may be treated as authoritative even though scanner evidence says judge prompts may be influenced by evaluated skills.

Mitigation: Treat results as advisory, require source-grounded evidence checks, and add explicit untrusted-evidence boundaries before using scores for gating, purchasing, or safety decisions.

Risk: The described workflow may touch model configuration and stored evaluation results when integrated into a production system.

Mitigation: Scope model configuration access and database writes to the minimum required permissions, and review changes before connecting the skill to production marketplace decisions.

Risk: The skill has broad activation triggers and a primarily Chinese-language operating scope.

Mitigation: Clarify intended language coverage and trigger boundaries before deployment so the skill is invoked only for reliability evaluation tasks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qomob/skills/xskill-are)
- [Server-resolved source repository](https://github.com/qomob/xskill-are)
- [Output schema](artifact/references/output-schema.md)
- [Business rubric](artifact/references/rubric-business.md)
- [Prompt rubric](artifact/references/rubric-prompt.md)
- [Robustness rubric](artifact/references/rubric-robustness.md)
- [Safety rubric](artifact/references/rubric-safety.md)
- [Scoring formulas](artifact/references/scoring-formulas.md)
- [Multi-judge protocol](artifact/references/multi-judge-protocol.md)
- [Dynamic test specification](artifact/references/dynamic-test-spec.md)
- [Calibration protocol](artifact/references/calibration-protocol.md)
- [Degradation matrix](artifact/references/degradation-matrix.md)
- [Meta-reflection checklist](artifact/references/meta-reflection-checklist.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, guidance]

**Output Format:** [Structured JSON score and report objects with human-readable Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces advisory AIScore and AIReport outputs, including six dimension scores, HRR tier, fatal flaws, test cases, and meta-reflection status.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter reports 2.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
