## Description: <br>
Send SMS text messages directly from the user's Android device using the Termux API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jerryshane1983-tech](https://clawhub.ai/user/jerryshane1983-tech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and users running an agent on Android through Termux use this skill to send explicit SMS messages through the local Termux API after confirming the recipient and exact message text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send real SMS messages from the user's Android device, which may expose private information or incur carrier charges. <br>
Mitigation: Use only on a device the user controls, verify the recipient phone number and exact message text before each send, and consider carrier costs and privacy exposure. <br>
Risk: SMS sending depends on local Termux and Android permissions being configured correctly. <br>
Mitigation: Install Termux:API and the termux-api package, grant SMS permissions on the device, and confirm termux-sms-send is available before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jerryshane1983-tech/termux-sms) <br>
- [Publisher profile](https://clawhub.ai/user/jerryshane1983-tech) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an Android device with Termux, Termux:API, SMS permissions, and termux-sms-send available.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
