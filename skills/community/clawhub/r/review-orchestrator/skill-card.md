## Description: <br>
Coordinates multi-perspective code and design reviews across configurable cognitive modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leegitw](https://clawhub.ai/user/leegitw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to select review approaches, coordinate technical and creative review perspectives, and apply quality gates to implementation, architecture, documentation, or security-sensitive work. It produces review findings and gate results that can be saved under the workspace review directory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Repository diffs and target files may contain sensitive work-in-progress content that configured reviewer tools can inspect. <br>
Mitigation: Use the skill only in trusted workspaces, and use no-yolo or fallback-disabling options when broad nested reviewer access or external reviewer CLIs should not handle diff content. <br>
Risk: Quality gates may run local test commands from configuration. <br>
Mitigation: Review .openclaw/review-orchestrator.yaml or .claude/review-orchestrator.yaml before running gates, and keep configured test commands limited to expected project checks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/leegitw/review-orchestrator) <br>
- [Publisher profile](https://clawhub.ai/user/leegitw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and structured text with example commands, review findings, and quality gate results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write review outputs under docs/reviews/ and uses optional local configuration from .openclaw/review-orchestrator.yaml or .claude/review-orchestrator.yaml.] <br>

## Skill Version(s): <br>
1.5.1 (source: server release metadata and release changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
