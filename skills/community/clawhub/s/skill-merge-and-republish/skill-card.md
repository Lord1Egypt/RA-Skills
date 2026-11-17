## Description:

Merge overlapping local skills into one canonical skill and republish the canonical skill to ClawHub.

This skill is ready for commercial/non-commercial use.

## Publisher:

[g-hanasq](https://clawhub.ai/user/g-hanasq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent maintainers use this skill to consolidate duplicated or overlapping local skills, preserve the canonical guidance, and publish the updated skill release to ClawHub.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can delete a local skill folder and publish updated skill behavior without an explicit safety gate.

Mitigation: Require the agent to show which skill will be kept and which folder will be retired, review the merged SKILL.md, and archive or commit a backup before deletion or publishing.

Risk: Merging unrelated skills could remove useful trigger boundaries or introduce confusing guidance.

Mitigation: Confirm the skills have substantially overlapping responsibilities and review the preserved guidance before accepting the merge.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/g-hanasq/skills/skill-merge-and-republish)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown status report with edited skill files and command results when actions are taken]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports the kept skill, retired skill, merged guidance, local commit, version bump, and ClawHub publish result.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
