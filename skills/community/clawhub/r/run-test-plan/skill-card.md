## Description: <br>
Execute YAML test plan, stop on first failure, output rich debug prompt. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and QA agents use this skill to execute YAML test plans, run setup and health checks, collect evidence, and produce debugging guidance when the first test fails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: YAML test plans can run local shell commands, start services, make network requests, and write evidence files. <br>
Mitigation: Review each plan before execution and run unfamiliar plans in a disposable workspace or container. <br>
Risk: Test output, logs, screenshots, or response captures can expose secrets or sensitive data. <br>
Mitigation: Keep secrets out of plans and captured evidence, and review logs and screenshots before sharing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/anderskev/run-test-plan) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, files, guidance] <br>
**Output Format:** [Markdown test results with command output, evidence file paths, and failure-debug prompts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stops on first failure and may write screenshots, response captures, and failure reports under docs/testing/evidence/.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
