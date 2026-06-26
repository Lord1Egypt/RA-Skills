## Description: <br>
Evaluates agent skill files against a skill quality standard, checks referenced files, and produces scores plus improvement suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lj22503](https://clawhub.ai/user/lj22503) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill authors use this skill to review new, modified, or batches of skill files for metadata quality, structure, referenced-file consistency, and actionable improvement suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad activation wording may cause the skill to run when a user only mentions skill review or optimization. <br>
Mitigation: Invoke it explicitly for skill review tasks and narrow activation wording if deployed in an environment where ordinary mentions should not trigger it. <br>
Risk: Review or optimization suggestions could introduce incorrect or misleading guidance if applied without inspection. <br>
Mitigation: Review generated findings and proposed edits before applying them, and scan the resulting skill before deployment. <br>


## Reference(s): <br>
- [Skill Optimizer on ClawHub](https://clawhub.ai/lj22503/skill-optimizer-v2) <br>
- [Skill Evaluation Checklist](references/checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown-style reports with scored findings, checklists, suggestions, and command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose changes to skill files; users should review suggestions before applying them.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata; SKILL.md frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
