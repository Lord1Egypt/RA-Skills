## Description: <br>
Skill Tester CN helps Claude Code evaluate other skills by analyzing skill definitions, generating test cases, running or simulating functional checks, scoring results, and producing a Markdown test report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhouchang1988](https://clawhub.ai/user/zhouchang1988) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to evaluate whether Claude Code skills trigger correctly, perform documented functions, handle edge cases, and produce a scored test report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Testing another skill may exercise real behavior, including scripts or actions with side effects. <br>
Mitigation: Use simulated or dry-run testing unless real execution is explicitly approved. <br>
Risk: Running tests against high-impact skills could delete files, spend money, publish content, or access sensitive accounts. <br>
Mitigation: Avoid using this tester on high-impact skills unless the environment is isolated and the actions are reviewed first. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhouchang1988/skill-tester-cn) <br>
- [Test report template](assets/test-report-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance] <br>
**Output Format:** [Markdown test report with scored tables and recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save a timestamped Markdown report in the current working directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
