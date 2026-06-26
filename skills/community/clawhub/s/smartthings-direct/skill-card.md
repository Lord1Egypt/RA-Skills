## Description: <br>
Provides direct SmartThings hub control via the official SmartThings CLI for listing devices, reading status, executing capability commands, and running scenes without Home Assistant. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[keenranger](https://clawhub.ai/user/keenranger) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to let an agent resolve SmartThings devices, inspect current status, and issue direct SmartThings CLI commands for device or scene control. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated SmartThings commands can affect real devices, including locks, HVAC, alarms, cameras, scenes, comfort, privacy, or power use. <br>
Mitigation: Require explicit user confirmation before consequential commands and re-read device status after high-impact actions. <br>
Risk: OAuth refresh tokens or personal access tokens provide sensitive access to SmartThings resources. <br>
Mitigation: Use browser OAuth where practical, protect stored credentials, avoid exposing PAT values in prompts or logs, and expect short-lived PATs to be reissued. <br>
Risk: Fuzzy device matching can select the wrong device when labels are similar. <br>
Mitigation: Review the matched device ID, label, and room before sending a command, especially for scenes or devices with safety impact. <br>


## Reference(s): <br>
- [SmartThings CLI](https://github.com/SmartThingsCommunity/smartthings-cli) <br>
- [SmartThings Personal Access Tokens](https://account.smartthings.com/tokens) <br>
- [ClawHub release page](https://clawhub.ai/keenranger/smartthings-direct) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include SmartThings CLI commands, JSON/YAML output flags, device lookup guidance, authentication setup guidance, and safety confirmation guidance.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
