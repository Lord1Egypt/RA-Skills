## Description:

Decide how to split skill content between SKILL.md and reference files for context efficiency and reliable triggering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samber](https://clawhub.ai/user/samber)

### License/Terms of Use:

MIT-0

## Use Case:

Skill authors and agent developers use this skill to decide when content should stay in SKILL.md, move into references, or become deterministic scripts. It helps distinguish triggering problems from progressive disclosure problems and recommends structure based on observable load conditions and evaluation evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger wording may activate the skill for adjacent skill-structure questions.

Mitigation: Review the trigger description and narrow it before deployment if over-invocation would be costly.

Risk: The skill may propose edits to skill files and subagent-based evaluation workflows when refactoring is requested.

Mitigation: Review proposed file changes and evaluation results before applying them or publishing an updated skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/samber/skills/skill-progressive-disclosure-design)
- [Project homepage](https://github.com/samber/cc-skills)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with suggested file structure, pointer sentences, and optional command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include proposed edits to skill files and eval-oriented architecture checks when requested.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
