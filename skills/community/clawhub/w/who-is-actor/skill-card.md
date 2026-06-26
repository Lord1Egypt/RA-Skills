## Description: <br>
Who Is Actor generates repository-level Git collaboration-pattern reports from read-only local Git history, focusing on aggregate commit cadence, churn, rework, conventional-commit compliance, and bus-factor signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wscats](https://clawhub.ai/user/wscats) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to inspect aggregate repository workflow patterns for a specific Git repository they are authorized to analyze. It is intended for repository-level process discussion, not contributor ranking or personnel decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes Git history that may include other contributors' metadata and sensitive commit text. <br>
Mitigation: Use it only on repositories you are authorized to analyze, prefer dry-run first, and keep raw commit messages, full paths, and contributor display names local-only. <br>
Risk: Aggregate repository metrics could be misused as personnel or performance signals. <br>
Mitigation: Do not use the report for performance reviews, rankings, compensation, hiring, firing, layoffs, or other personnel decisions; keep interpretation at the repository workflow level. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wscats/who-is-actor) <br>
- [Project repository](https://github.com/wscats/who-is-actor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with aggregate metrics and optional dry-run command preview] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Repository-level only; contributor display names and raw commit metadata are local-only intermediate values and are not included in model-bound prompts or the final report.] <br>

## Skill Version(s): <br>
1.0.15 (source: server release metadata and skill.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
