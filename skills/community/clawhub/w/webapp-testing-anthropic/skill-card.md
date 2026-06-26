## Description: <br>
Toolkit for interacting with and testing local web applications using Playwright. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pupuking723](https://clawhub.ai/user/pupuking723) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect, automate, and verify local web applications with Playwright, including static HTML and dynamic apps that need a local development server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper workflow can run local shell commands to start application servers. <br>
Mitigation: Use the skill only with trusted projects and server commands, and do not pass commands derived from untrusted input. <br>
Risk: Screenshots, DOM dumps, and console logs can capture sensitive data from authenticated or production-like sessions. <br>
Mitigation: Avoid collecting full-page browser artifacts from sensitive sessions unless there is a plan to redact and delete them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pupuking723/webapp-testing-anthropic) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline Python and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce browser screenshots, console logs, DOM inspection notes, and local automation scripts when the agent follows the skill.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
