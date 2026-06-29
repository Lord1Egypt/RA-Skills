## Description: <br>
Claude Code skill testing framework that analyzes skill definitions, generates test cases, executes functional tests, and produces scored Markdown reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhouchang1988](https://clawhub.ai/user/zhouchang1988) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and skill maintainers use this skill to evaluate Claude Code skills by locating a target skill, parsing its definition, generating trigger, functional, and resource tests, and producing a scored test report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Active testing can run target-skill behavior against unknown skill content. <br>
Mitigation: Use simulated or static-only testing first for untrusted skills, and run active tests only in a controlled workspace. <br>
Risk: The skill can inspect other local skill definitions and bundled assets. <br>
Mitigation: Point it only at skills intended for review, and avoid directories that contain unrelated sensitive material. <br>
Risk: The skill can write timestamped Markdown reports to the current working directory. <br>
Mitigation: Confirm the report destination before testing, and review generated reports before sharing them. <br>


## Reference(s): <br>
- [README](README.md) <br>
- [Test report template](assets/test-report-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown test report with scored tables, findings, and recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write a timestamped report file in the current working directory when active testing is performed.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
