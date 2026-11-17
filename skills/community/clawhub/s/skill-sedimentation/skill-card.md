## Description:

Skill Sedimentation helps an agent convert non-trivial task outcomes into reusable experience records, distilled guidance, and promotion candidates through a Trigger-Retrieve-Act-Reflect-Distill-Promote loop.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawhub-master](https://clawhub.ai/user/clawhub-master)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to capture useful task experience, distill it into persistent memory or skill guidance, and manage promotion decisions with thresholds, guard checks, and human veto points.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist task content into memory files, which may capture sensitive workspace information.

Mitigation: Require explicit approval before writes and avoid automatic post-task activation in sensitive workspaces.

Risk: The skill may modify memory or skill instructions, affecting future agent behavior.

Mitigation: Use human review for promotions and boundary changes, and inspect proposed diffs before accepting them.

Risk: Security evidence reports weak scoping and flawed safeguards around path and write-limit checks.

Mitigation: Fix and verify path and write-limit checks before using the skill in workspaces with sensitive content.

## Reference(s):

- [Artifact Skill Definition](artifact/SKILL.md)
- [ClawHub Skill Page](https://clawhub.ai/clawhub-master/skills/skill-sedimentation)
- [Publisher Profile](https://clawhub.ai/user/clawhub-master)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown records, structured JSON event examples, and implementation guidance with code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose persistent memory or skill-file writes; boundary-changing promotions should remain subject to explicit human review.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter reports 3.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
