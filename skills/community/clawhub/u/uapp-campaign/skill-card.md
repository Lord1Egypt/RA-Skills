## Description: <br>
Guides an agent through Umeng CLI calls to create and list promotion campaign links for mini-program, H5, and mini-game properties. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[squall0925](https://clawhub.ai/user/squall0925) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators managing Umeng mini-program, H5, or mini-game promotion assets use this skill to create campaign links and list existing campaigns or channels through umeng-cli. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on an external Umeng CLI login and sends trace telemetry that can include the skill name and appkey. <br>
Mitigation: Install and authenticate the CLI only in trusted environments, and review telemetry expectations before using the skill with a real appkey. <br>
Risk: The createCampaign workflow performs a real write action and the resulting promotion link is described as irreversible. <br>
Mitigation: Confirm the appkey, campaign name, channel name, and optional path with the user before execution, and do not automatically retry failed write calls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/squall0925/uapp-campaign) <br>
- [Umeng CLI project](https://github.com/umeng/umeng-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires umeng-cli, Umeng login, and a mini-program dataSourceId/appkey for business API calls.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
