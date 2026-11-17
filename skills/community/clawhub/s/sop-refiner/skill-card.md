## Description:

Sop Refiner helps agents refine existing SOPs by removing redundancy, adding exception paths, rollback and recovery steps, and quality gates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Operations teams, process owners, and agents use this skill to turn existing SOP text and pain-point feedback into a conservative review draft with current issues, deletions, additions, exception paths, rollback and recovery steps, and an updated outline.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SOP drafts may include incorrect, incomplete, or misleading process guidance if the source material is incomplete.

Mitigation: Review the draft before adoption and resolve the skill's confirmation items before using the output as an execution checklist.

Risk: Input SOPs may contain sensitive operational or personal data.

Mitigation: Keep inputs local and redact sensitive material before using the skill, consistent with the server security guidance.

Risk: The bundled script includes inactive local audit modes that inspect local files when intentionally enabled.

Mitigation: Use the default structured SOP drafting mode unless local file audit behavior is specifically intended and reviewed.

Risk: Recommendations could be mistaken for approval to change permissions, bypass safety checks, or modify external systems.

Mitigation: Treat outputs as review drafts; preserve approval boundaries and use dry-run or review-only plans for any high-risk operational change.

## Reference(s):

- [Sop Refiner on ClawHub](https://clawhub.ai/52yuanchangxing/skills/sop-refiner)
- [Publisher profile: 52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or JSON report, with optional local shell command usage documented for script execution.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Structured sections include current issues, suggested deletions, suggested additions, exception paths, rollback and recovery, updated outline, confirmation items, and next steps.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
