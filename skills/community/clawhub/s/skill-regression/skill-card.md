## Description: <br>
Regression testing framework for AgentSkills that analyzes a target skill, runs script-layer assertions and AI-layer semantic scoring, and outputs a Markdown report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[songhonglei](https://clawhub.ai/user/songhonglei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to regression test AgentSkills with scripted assertions, LLM-based semantic checks, reruns of failed cases, and Markdown reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Test cases can run local shell commands from target TEST.md files. <br>
Mitigation: Run the skill only against trusted skill directories and review TEST.md commands before execution. <br>
Risk: Skill contents and test results may be sent to external LLM services. <br>
Mitigation: Use --skip-agent or local-only workflows for sensitive code and configure LLM endpoints deliberately. <br>
Risk: The optional report upload hook can send generated reports to a configured destination. <br>
Mitigation: Enable SR_REPORT_UPLOAD_HOOK only for trusted upload scripts and destinations. <br>
Risk: The OpenClaw backend can create a probe cron job during testing. <br>
Mitigation: Review and remove any OpenClaw probe cron job after testing. <br>


## Reference(s): <br>
- [TEST.md template](references/TEST_template.md) <br>
- [Report Structure Reference](references/report_structure.md) <br>
- [ClawHub skill page](https://clawhub.ai/songhonglei/skill-regression) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report with JSON result files and command-line output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write local run artifacts under a skill-regression workspace and optionally call a user-configured report upload hook.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence and artifact documentation) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
