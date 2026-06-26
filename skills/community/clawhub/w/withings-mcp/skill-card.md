## Description: <br>
Connect an MCP-compatible agent to local Withings body measures, sleep, activity, workouts, and heart records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davidmosiah](https://clawhub.ai/user/davidmosiah) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and MCP-compatible agent users use this skill to install, configure, verify, and troubleshoot local Withings MCP access while preserving privacy boundaries for health data and OAuth tokens. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill connects agents to sensitive Withings health data and OAuth-token-backed local access. <br>
Mitigation: Keep token files private, avoid printing credentials or private user data, and run connection status or privacy-audit checks before data access. <br>
Risk: Live provider calls or write-capable actions could access or change user-linked data without adequate consent. <br>
Mitigation: Require explicit user approval before live provider calls or write-capable actions, and prefer dry-run or audit surfaces first. <br>
Risk: Health measurements may be misread as medical advice. <br>
Mitigation: Present Withings data as informational only and do not provide medical, legal, financial, or platform-policy advice. <br>


## Reference(s): <br>
- [Withings MCP repository](https://github.com/davidmosiah/withingsmcp) <br>
- [Withings connector documentation](https://wellness.delx.ai/connectors/withings) <br>
- [Withings MCP ClawHub listing](https://clawhub.ai/davidmosiah/withings-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include setup, status, privacy-audit, and dry-run guidance before live provider calls.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
