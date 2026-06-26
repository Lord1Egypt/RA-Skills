## Description: <br>
Operate SNU's Canvas LMS (etl.snu.ac.kr) through CLI commands to inspect configuration, list courses, assignments, files, and announcements, run bot or serve modes, and troubleshoot Canvas API issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guzus](https://clawhub.ai/user/guzus) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Students, instructors, or operators with an existing lx-agent setup use this skill to run Canvas LMS tasks through the local CLI bridge while keeping authentication and URL handling out of chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill delegates live LMS access and token handling to a local lx-agent repository that is not bundled in the reviewed package. <br>
Mitigation: Install only after reviewing and trusting the local repository referenced by LX_AGENT_ROOT. <br>
Risk: Canvas API tokens could be exposed if users paste credentials into chat or logs. <br>
Mitigation: Keep tokens in local configuration or environment variables and never send token values through chat. <br>
Risk: Bot and serve modes may start long-running processes. <br>
Mitigation: Run those modes only when an operator intentionally wants a persistent service and can monitor startup errors. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/guzus/snu-canvas-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and concise command-result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands are routed through the bundled bridge script and should avoid exposing secret token values.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
