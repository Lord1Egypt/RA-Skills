## Description: <br>
Release-day coordination helpers for cutover, verification, and rollback readiness. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JiaranI](https://clawhub.ai/user/JiaranI) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, release managers, and operations teams use this skill during deploy windows to plan rollout steps, verify gates, prepare rollback readiness, and capture release execution notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review flags the release as suspicious because maintainer workflows and high-impact ClawHub or GitHub actions can affect release operations. <br>
Mitigation: Install only in trusted maintainer contexts, review generated plans before execution, and use authenticated accounts only with explicit release targets. <br>


## Reference(s): <br>
- [Operations Checklist Template](templates/checklist.md) <br>
- [Release Execution Report Template](templates/report.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and checklist/report templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces concise rollout notes, gate checks, rollback preparation guidance, and reusable handoff artifacts.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
