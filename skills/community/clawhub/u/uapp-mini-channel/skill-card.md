## Description: <br>
Helps agents query Umeng U-MiniProgram channel, campaign, and scene-source analytics through read-only umeng-cli OpenAPI calls for rankings, details, and trends. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[squall0925](https://clawhub.ai/user/squall0925) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and growth analysts use this skill to inspect mini-program acquisition sources, compare channel or campaign performance, and analyze trends. It is limited to mini-program, H5, and mini-game data, and does not cover Android or iOS app channel reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires umeng-cli account login and local credential caching. <br>
Mitigation: Use it only in approved environments and review local credential handling before deployment. <br>
Risk: The artifact instructs agents to send telemetry, including an AppKey-bearing trace, without a clear consent step. <br>
Mitigation: Remove or disable trace commands unless the organization has explicitly approved that reporting. <br>
Risk: Using the wrong identifier for channel or campaign detail queries can produce misleading zero-data results. <br>
Mitigation: Use getCustomerSourceOverview.data[].id for channel or campaign detail calls, not getSceneInfoList.code. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/squall0925/uapp-mini-channel) <br>
- [umeng-cli project homepage](https://github.com/umeng/umeng-cli) <br>
- [Umeng OpenAPI gateway](https://gateway.open.umeng.com/openapi) <br>
- [Umeng web console](https://web.umeng.com) <br>
- [Umeng scene value documentation](https://developer.umeng.com/docs/147615/detail/175369) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Markdown] <br>
**Output Format:** [Markdown with inline shell commands and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces read-only analytics workflows and interpretation guidance; requires umeng-cli login credentials and a dataSourceId appkey.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
