## Description: <br>
Train, evaluate, and improve Agent skill files as reusable external capabilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use SkillOpt to improve agent skill documents through train and validation task suites, command-backed rollouts, scoring, validation gates, and export of a deployable best_skill.md. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Command-backed rollouts and command scorers can execute local shell commands. <br>
Mitigation: Use the skill only in trusted workspaces, review --agent-command values and task scorer command fields before running them, and treat imported task suites as executable code. <br>
Risk: Rollout files can contain prompts, model outputs, command output, stderr, task data, and scores. <br>
Mitigation: Avoid sensitive prompts or secrets unless you control where rollout logs are written and how they are retained. <br>
Risk: Skill edits can overfit train or validation examples or accidentally embed benchmark-specific answers. <br>
Mitigation: Keep train and validation splits separate, use validation only as an accept/reject gate, review accepted edits, and use a fresh holdout split for fragile or high-stakes skills. <br>


## Reference(s): <br>
- [SkillOpt Evaluation Reference](references/evaluation.md) <br>
- [ClawHub SkillOpt Release Page](https://clawhub.ai/harrylabsj/skillopt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, skill files, JSON summaries, JSONL task files, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create run directories containing source_skill.md, candidate skill files, rollout logs, scoring summaries, rejected edit notes, best_skill.md, and report.md.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
