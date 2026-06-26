## Description: <br>
Create and manage SimpleLogin email aliases from the command line. Protect your real email with secure, private aliases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mcclawd](https://clawhub.ai/user/mcclawd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to create, list, enable, disable, and delete SimpleLogin email aliases, and to create contacts for reverse-alias replies while keeping a real mailbox private. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a SimpleLogin API key to manage aliases and contacts. <br>
Mitigation: Provide the key only through SIMPLELOGIN_API_KEY or the declared secrets file, and avoid exposing command output that contains account or alias details. <br>
Risk: Disable and delete commands can stop mail forwarding or affect accounts tied to an alias. <br>
Mitigation: Review the target alias before running destructive or delivery-changing commands. <br>
Risk: Reverse-alias contact creation changes how replies are routed through an alias identity. <br>
Mitigation: Create contacts only for intended recipients and confirm the alias and contact email before sending mail through the returned reverse alias. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/mcclawd/simplelogin-cli) <br>
- [Publisher profile](https://clawhub.ai/user/mcclawd) <br>
- [SimpleLogin](https://simplelogin.io) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a SimpleLogin API key supplied through SIMPLELOGIN_API_KEY or the declared OpenClaw secrets file.] <br>

## Skill Version(s): <br>
3.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
