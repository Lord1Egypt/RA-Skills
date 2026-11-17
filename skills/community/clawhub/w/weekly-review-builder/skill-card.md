## Description:

Build a weekly review that refreshes project phase, bottleneck, and next steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunbinnju-star](https://clawhub.ai/user/sunbinnju-star)

### License/Terms of Use:

MIT-0

## Use Case:

External users and project operators use this skill to compress a week of logs, decisions, outputs, stale tasks, and blockers into an updated project state and next-week plan.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Proposed project-state updates could distort project memory if accepted without review.

Mitigation: Review the generated weekly review and writeback record against the source logs before accepting any project-memory update.

Risk: Missing or incomplete weekly logs can lead to low-confidence phase, bottleneck, or planning recommendations.

Mitigation: Require the skill to mark low confidence and request missing log recovery when evidence is insufficient.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sunbinnju-star/skills/weekly-review-builder)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Structured text or Markdown review with fields for current phase, bottleneck, next-week goal, next actions, risk check, project summary, confidence, and writeback record.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires weekly project logs and current project state; does not produce executable code or shell commands.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
