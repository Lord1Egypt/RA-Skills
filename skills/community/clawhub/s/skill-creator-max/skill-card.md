## Description:

Builds new agent skills through a five-stage workflow that specifies, structures, implements, compresses, and independently tests the result.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vincentjiang06](https://clawhub.ai/user/vincentjiang06)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to create a new agent skill from an explicit request, with structured design, implementation checks, independent review, and a final decision record.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated validation harnesses may execute untrusted code.

Mitigation: Run the pipeline in a sandboxed workspace and do not validate untrusted dossiers or harnesses.

Risk: A floating install or update command can retrieve unreviewed code.

Mitigation: Review the skill before installation and pin its release or commit.

Risk: The workflow can change skill files and write decision or learning records.

Mitigation: Review proposed changes and records before relying on or deploying the resulting skill.

## Reference(s):

- [Skill release on ClawHub](https://clawhub.ai/vincentjiang06/skills/skill-creator-max)
- [Orchestration anchors](artifact/references/orchestration-anchors.md)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Code, Configuration, Guidance]

**Output Format:** [Agent skill files and structured JSON decision and evaluation records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or modifies skill files and writes decision and learning records.]

## Skill Version(s):

1.3.4 (source: skill frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
