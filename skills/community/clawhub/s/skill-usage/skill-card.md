## Description: <br>
Installs and configures the OpenClaw Skill Usage plugin for local skill usage analytics and optional shared leaderboards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lucifinil](https://clawhub.ai/user/lucifinil) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to install, restart, and verify skill usage analytics, including local usage reports and explicitly requested shared leaderboards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing the plugin introduces a third-party npm package and requires restarting the OpenClaw Gateway. <br>
Mitigation: Install only when the operator trusts the publisher and has explicitly agreed to the restart, then verify the plugin with status and top-usage checks. <br>
Risk: Shared leaderboards can sync operational metadata such as skill names, channel labels, agent labels, timestamps, and routing identifiers. <br>
Mitigation: Keep analytics local unless shared reporting is explicitly requested, and disclose the synced metadata and TiDB Cloud Zero destination before enabling shared mode. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lucifinil/skill-usage) <br>
- [Publisher profile](https://clawhub.ai/user/lucifinil) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes setup, restart, verification, privacy, and optional join-token guidance.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
