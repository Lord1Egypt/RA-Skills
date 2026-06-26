## Description: <br>
Generates structured QA scenario drafts from requirements, covering main flows, exceptions, cross-platform cases, invalid input, recovery paths, and priorities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
QA engineers, developers, and product teams use this skill to turn requirements, user flows, and constraints into reviewable test scenario drafts and execution checklists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated scenarios may be mistaken for completed QA execution. <br>
Mitigation: Treat outputs as draft test design material and review or execute tests separately before relying on results. <br>
Risk: Input requirements or user flows may contain sensitive information. <br>
Mitigation: Run the skill only on files intended for processing and redact sensitive material unless it is required for test design. <br>
Risk: The local script can write to user-selected output paths and includes dormant audit modes controlled by the spec file. <br>
Mitigation: Choose output paths carefully and re-review the script and resources/spec.json before modifying modes or configuration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/52YuanChangXing/qa-scenario-synthesizer) <br>
- [README](README.md) <br>
- [Scenario specification](resources/spec.json) <br>
- [Output template](resources/template.md) <br>
- [Smoke test](tests/smoke-test.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, shell commands] <br>
**Output Format:** [Structured Markdown, with optional JSON output from the local script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are reviewable drafts based on local input; users choose any output file path when running the script.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
