## Description: <br>
Fetch and summarize Ultrahuman Ring/CGM metrics inside OpenClaw using the Ultrahuman MCP server (via mcporter). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[devpranoy](https://clawhub.ai/user/devpranoy) <br>

### License/Terms of Use: <br>


## Use Case: <br>
OpenClaw users with Ultrahuman credentials use this skill to retrieve daily or weekly Ultrahuman Ring and CGM metrics and turn them into concise health summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local MCP setup handles an Ultrahuman auth token and sensitive health metrics. <br>
Mitigation: Use a trusted local environment, keep tokens out of shared files and logs, and rotate the token if it may have been exposed. <br>
Risk: The skill depends on an external Ultrahuman MCP server repository that must be trusted by the user. <br>
Mitigation: Review or pin the external Ultrahuman-MCP repository before use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/devpranoy/ultrahuman-openclaw) <br>
- [Ultrahuman Developer Portal](https://vision.ultrahuman.com/developer) <br>
- [Ultrahuman MCP Server Repository](https://github.com/Monasterolo21/Ultrahuman-MCP) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text summaries with Markdown setup guidance and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Summaries focus on sleep, activity, recovery, VO2 max, HRV, and resting heart rate when available.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
