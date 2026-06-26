## Description: <br>
Generates structured JSON functional test cases for Agent Skills, covering activation, core capabilities, workflow, instruction clarity, and exception/security scenarios. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liyifm](https://clawhub.ai/user/liyifm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to generate traceable functional test cases for Agent Skills. It helps plan tests across routing, declared capabilities, multi-step behavior, instruction quality, and exception/security handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads every file under the selected skill folder or skill zip, which can expose secrets or unrelated private files if the target is too broad. <br>
Mitigation: Point it only at the intended skill package, avoid folders that contain secrets, and review the generated JSON before sharing it. <br>
Risk: Generated test cases may be incomplete or misleading if the target skill's instructions, scripts, or references are ambiguous. <br>
Mitigation: Review the generated cases against the source files and run the included validation command before relying on the output. <br>


## Reference(s): <br>
- [Skill Test Schema](references/test-schema.md) <br>
- [Agent Skills Specification](https://agentskills.io/specification) <br>
- [ClawHub Release Page](https://clawhub.ai/liyifm/skill-test-generate) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [JSON test case files with supporting Markdown-style guidance and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Validated JSON includes generated summary and verified fields after the bundled validation step.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and user changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
