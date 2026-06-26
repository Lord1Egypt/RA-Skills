## Description: <br>
Send scrolling text messages to RDA MSG Board via HTTP/JSON. Use for notifications, alerts, or status updates on physical LED matrix. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rdeangel](https://clawhub.ai/user/rdeangel) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and automation agents use this skill to send notifications, alerts, and status messages to configured RDA MSG Board LED matrix displays. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Board credentials may be stored locally and transmitted over plain HTTP with Basic Auth. <br>
Mitigation: Use a unique board password, keep the device on a trusted network, prefer HTTPS when supported, and avoid storing credentials in boards.yaml on shared or backed-up machines. <br>
Risk: Messages may appear on a public or shared physical display. <br>
Mitigation: Confirm the target board profile and message content before sending. <br>
Risk: User-provided message text is passed to a local command-line script. <br>
Mitigation: Invoke the script with an argv-style argument list when possible, or quote message text safely before shell execution. <br>


## Reference(s): <br>
- [RDA MSG Board skill release](https://clawhub.ai/rdeangel/rda-msg-board) <br>
- [RDA MSG Board project documentation](https://github.com/rdeangel/rda_msg_board) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command invocations and HTTP/JSON message parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute local Python scripts that send authenticated HTTP requests to configured LED boards.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
