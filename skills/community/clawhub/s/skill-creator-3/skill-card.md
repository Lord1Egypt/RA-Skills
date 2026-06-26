## Description: <br>
Create new skills, modify and improve existing skills, and measure skill performance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luowanqian](https://clawhub.ai/user/luowanqian) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and skill authors use this skill to draft, revise, evaluate, benchmark, package, and improve agent skills. It supports workflows for creating SKILL.md files, running evaluation loops, reviewing outputs, and optimizing skill descriptions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Helper scripts can send skill content and evaluation data to Claude. <br>
Mitigation: Review the data before running evaluation or description-improvement workflows, and avoid sensitive repositories unless external processing is acceptable. <br>
Risk: The review viewer can start a local server and may terminate an existing process on the configured viewer port. <br>
Mitigation: Prefer static viewer mode or a foreground server in sensitive environments, and check whether the viewer port is already in use before launch. <br>
Risk: Generated or revised skill instructions may contain incorrect, overfitted, or misleading guidance. <br>
Mitigation: Review generated skill files, evaluation assertions, and benchmark results before packaging or deploying the skill. <br>


## Reference(s): <br>
- [Evaluation and benchmark schemas](references/schemas.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON snippets, shell commands, generated files, and review artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce SKILL.md drafts, eval definitions, benchmark summaries, HTML review pages, description candidates, and packaged skill files.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
