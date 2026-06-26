## Description: <br>
Evaluates project structure, delivery quality, and improvement opportunities with a nine-dimension rubric that includes process quality. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[youxiyin](https://clawhub.ai/user/youxiyin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and project maintainers use this skill to score project health, identify weak dimensions, propose concrete improvements, and generate Markdown evaluation reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may propose or make project edits that affect files or git history. <br>
Mitigation: Use read-only mode unless remediation is intended, and review the diff before approving changes. <br>
Risk: Generated evaluation reports may capture confidential project details. <br>
Mitigation: Avoid storing reports for confidential projects unless the memory/project-evals path is appropriate. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/youxiyin/wave-project-evaluator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown scorecards, edit previews, diffs, shell commands, and project evaluation reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write reports under memory/project-evals and may propose or perform remediation when the user approves changes.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
