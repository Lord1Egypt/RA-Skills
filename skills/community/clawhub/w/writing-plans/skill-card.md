## Description: <br>
Use when you have a spec or requirements for a multi-step task, before touching code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zlc000190](https://clawhub.ai/user/zlc000190) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to turn a spec or requirements for a multi-step coding task into a detailed Markdown implementation plan before editing code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create or update Markdown implementation plans under docs/plans/. <br>
Mitigation: Review the generated plan file and its diff before relying on it or committing it. <br>
Risk: Generated plans may include suggested commands or referenced follow-up skills. <br>
Mitigation: Review those commands and references before executing them or using the follow-up skills. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown plan saved under docs/plans/ with code and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes exact file paths, test commands, expected results, and execution handoff options.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
