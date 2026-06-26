## Description: <br>
Evaluates agent skills with the SRL framework and produces structured reliability scores, reports, and improvement guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vuact](https://clawhub.ai/user/vuact) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill reviewers use this skill to assess another agent skill's reliability, traceability, failure behavior, and reproducibility before relying on its outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads target skill files and can evaluate broad sets of skills, which may expose more local workspace content than intended. <br>
Mitigation: Use explicit target paths and avoid broad batch evaluation in sensitive workspaces unless that scope is intended. <br>
Risk: The workflow can write .srl-report.md and .srl-report.json files into target repositories. <br>
Mitigation: Review the target path and existing report files before allowing report output to be written. <br>


## Reference(s): <br>
- [SRL Framework Reference](references/srl-framework.md) <br>
- [SRL Scoring Criteria](references/scoring-criteria.md) <br>
- [SRL Evaluation Template](assets/SRL-EVAL-TEMPLATE.md) <br>
- [Skill Reliability Crisis Article](https://github.com/Vuact/Blog/blob/main/articles/Skill%20%E7%8B%82%E7%83%AD%E8%83%8C%E5%90%8E%EF%BC%8C%E6%B2%A1%E4%BA%BA%E5%91%8A%E8%AF%89%E4%BD%A0%E7%9A%84%E5%8F%AF%E9%9D%A0%E6%80%A7%E5%8D%B1%E6%9C%BA.md) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, json, shell commands, guidance] <br>
**Output Format:** [Structured JSON inputs followed by Markdown or JSON evaluation reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include SRL scores, evidence, warnings, and improvement suggestions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
