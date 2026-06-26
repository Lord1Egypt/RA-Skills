## Description: <br>
Learning creates customized learning-project skills with SKILL.md and reference files that guide a learner from planning through study, review, and completion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[balancegsr](https://clawhub.ai/user/balancegsr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate a structured learning-project skill for a chosen topic, including planning, progress tracking, study notes, module reviews, and completion artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can trigger broadly on normal learning or tutoring requests. <br>
Mitigation: Install it only when systematic learning-project generation is desired, and narrow or disable generic learning triggers if routine Q&A should take precedence. <br>
Risk: The skill may create persistent study-project files and generated skills in the workspace. <br>
Mitigation: Confirm the destination paths before delivery and review generated files before relying on them. <br>
Risk: The skill may inspect home-directory paths during installation-path discovery. <br>
Mitigation: Avoid home-directory scanning unless the user explicitly approves that discovery step. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/balancegsr/skill-creator-learning) <br>
- [README](README.md) <br>
- [Knowledge Type Strategy](references/strategies/README.md) <br>
- [Review Guide Template](references/templates/guides/review_guide.md) <br>
- [Framework Guide Template](references/templates/guides/framework_guide.md) <br>
- [Lite Skill Template](references/templates/skill/lite.md) <br>
- [Full Skill Template](references/templates/skill/full.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown skill files and reference files, with setup guidance and optional shell commands for delivery] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated learning projects may create persistent workspace files for plans, notes, summaries, and feedback.] <br>

## Skill Version(s): <br>
1.4.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
