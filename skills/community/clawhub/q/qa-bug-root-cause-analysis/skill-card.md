## Description: <br>
Guides agents through structured QA bug root cause analysis using symptom classification, 5 Whys, causal diagrams, and fishbone analysis to identify direct, indirect, and systemic causes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kokxi](https://clawhub.ai/user/kokxi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
QA engineers, developers, and incident reviewers use this skill to turn recurring or production bugs into structured root cause analyses, impact assessments, fix suggestions, and prevention measures. It is especially suited to cases where teams need to distinguish direct defects from process or system causes and improve test design. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bug descriptions, logs, environment details, or project files may contain sensitive production data. <br>
Mitigation: Redact secrets and unnecessary personal or production data before sharing evidence with an agent, and scope file inspection to the materials needed for the analysis. <br>
Risk: A root cause conclusion may be misleading if based only on symptoms or incomplete reproduction evidence. <br>
Mitigation: Validate hypotheses against logs, reproduction steps, and controlled changes before treating the conclusion as final. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kokxi/skills/qa-bug-root-cause-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Structured Markdown analysis with root cause, contributing factors, impact assessment, fix suggestions, and prevention measures] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include diagnostic checklists and hypothesis verification steps; no executable output is required.] <br>

## Skill Version(s): <br>
1.5.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
