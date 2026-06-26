## Description: <br>
Queries Umeng U-App custom event data through umeng-cli call commands for seven read-only event and parameter analytics endpoints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[squall0925](https://clawhub.ai/user/squall0925) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and operators use this skill to inspect custom event lists, event counts, unique users, parameters, parameter value distributions, and daily trends for Umeng U-App properties. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill documentation tells the agent to send telemetry automatically, including an appkey when one is provided. <br>
Mitigation: Do not allow automatic umeng-cli trace calls with appkeys unless the user explicitly accepts that telemetry. <br>
Risk: The workflow requires Umeng credentials and appkeys to query application analytics. <br>
Mitigation: Use a least-privileged Umeng account and avoid exposing appkeys or cached credentials in logs, prompts, or shared outputs. <br>
Risk: The artifact offers both npm installation and a curl-to-shell installer path for umeng-cli. <br>
Mitigation: Prefer the npm install path from a trusted source and review installer behavior before running shell scripts from URLs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/squall0925/uapp-event) <br>
- [Umeng CLI project](https://github.com/umeng/umeng-cli) <br>
- [Umeng website](https://www.umeng.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Markdown, Configuration instructions] <br>
**Output Format:** [Markdown with inline shell commands and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires umeng-cli, an authenticated Umeng account, and an appkey for the target application.] <br>

## Skill Version(s): <br>
1.2.0 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
