## Description: <br>
Standard SSH command templates for a remote operator machine (bird reads, Puppeteer runs, inbox-style messaging). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Highlander89](https://clawhub.ai/user/Highlander89) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to apply standard SSH command templates for checking a remote operator machine and sending inbox-style messages after configuring REMOTE_TARGET and replacing placeholders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs SSH commands on a remote machine, so incorrect targets or placeholder commands can affect systems outside the local agent environment. <br>
Mitigation: Set REMOTE_TARGET intentionally, use a least-privileged SSH account, and inspect or replace each TODO command before execution. <br>
Risk: The message script interpolates user-supplied message text into a remote shell command. <br>
Mitigation: Do not pass secrets or untrusted text to msg-sapconet.sh unless the script is changed to pass the message safely, such as via stdin or robust shell escaping. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Highlander89/remote-ssh-bridge) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and script references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled scripts are templates that require REMOTE_TARGET and command placeholders to be reviewed before use.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
