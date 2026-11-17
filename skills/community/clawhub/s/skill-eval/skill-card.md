## Description:

Autonomous engine that systematically evaluates and ranks agent skills across models using rubric grading, error taxonomy, and improvement feedback loops.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jensen-srp](https://clawhub.ai/user/jensen-srp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and evaluation engineers use this skill to design, run, grade, compare, and improve agent-skill evaluations across one or more execution models.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may execute untrusted skills or local script steps during evaluation.

Mitigation: Use a controlled evaluation workspace with trusted repository contents before running local commands.

Risk: The skill may propose persistent changes to knowledge-base files, SKILL-EVAL.md, or SKILL.md.

Mitigation: Require human review before accepting generated methodology, knowledge-base, or skill changes.

Risk: Unrelated credentials could be exposed if evaluations run in a shared workspace.

Mitigation: Run evaluations with disposable outputs and no unrelated credentials available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jensen-srp/skills/skill-eval)
- [Publisher profile](https://clawhub.ai/user/jensen-srp)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON configuration examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces evaluation reports, leaderboard artifacts, grading summaries, and proposed skill improvements.]

## Skill Version(s):

0.4.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
