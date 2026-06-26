## Description: <br>
Send and receive files peer-to-peer using the sendme protocol from iroh.computer. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[muninn-huginn](https://clawhub.ai/user/muninn-huginn) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to send files or folders to another machine, or to receive files from a trusted sendme ticket. It is intended for peer-to-peer transfer workflows where the sender can remain online until download completion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A sendme ticket grants access to the transfer while the sender is online. <br>
Mitigation: Keep tickets private and share them only with the intended recipient. <br>
Risk: Receiving a ticket from an untrusted sender can place unexpected files in the current directory. <br>
Mitigation: Receive only from trusted senders and run receive commands from a directory where new files are expected. <br>
Risk: The sender process must remain online and exposes the selected file or folder until the transfer is complete. <br>
Mitigation: Confirm the exact file or folder before sending and stop the sender process after the transfer completes. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/muninn-huginn/sendme-skill) <br>
- [Iroh Sendme](https://www.iroh.computer/sendme) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Guidance] <br>
**Output Format:** [Markdown with inline bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides commands and operational guidance for sending and receiving files; the send command returns a ticket that must be shared with the recipient.] <br>

## Skill Version(s): <br>
0.1.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
