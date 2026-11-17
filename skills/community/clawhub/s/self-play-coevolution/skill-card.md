## Description:

Guides an agent through a self-play coevolution loop where proposer and critic roles iteratively improve proposals, detect regressions, and escalate checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to run a proposer/critic self-play loop that iteratively improves candidate responses, escalates checks, and records progress for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can keep local cross-session memory of notes and preferences.

Mitigation: Do not store secrets or sensitive personal details in notes or preferences, and review saved memory before sharing or deploying the skill.

Risk: The skill describes automatically reflecting on errors and proposing changes to its own instructions.

Mitigation: Require human review before applying any suggested SKILL.md or instruction change.

Risk: Self-play critique loops may produce persuasive but incorrect proposals or guidance.

Mitigation: Review outputs before using them in production decisions or incorporating them into downstream skills.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qq435912743/skills/self-play-coevolution)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with optional JSON run logs and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The coevolution runner returns JSON-compatible trace fields including rounds, scores, flaws, critic_level, convergence status, critic_escalations, and regression_caught.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
