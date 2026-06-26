## Description: <br>
Web Module Runner is a local command-line utility for logging, searching, and exporting notes about web module tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueyetianya](https://clawhub.ai/user/xueyetianya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers can use this skill to propose shell commands and workflows for recording, reviewing, searching, and exporting local notes about web module-related tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task notes and command arguments may include secrets, private code, customer data, or other sensitive project details. <br>
Mitigation: Avoid entering sensitive values and review local logs or exports before sharing them. <br>
Risk: The artifact uses broad build-runner language, while the security evidence describes the behavior as local command-history logging. <br>
Mitigation: Treat generated records as notes or history unless results are independently verified with the relevant build or analysis tools. <br>
Risk: Command use can create persistent local log and export files under the user's home directory. <br>
Mitigation: Run in an appropriate environment and remove or protect ~/.local/share/web-module-runner/ data when it is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xueyetianya/web-module-runner) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/xueyetianya) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; command output may include text, JSON, CSV, or TXT exports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands store local logs and exports under ~/.local/share/web-module-runner/ when executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
