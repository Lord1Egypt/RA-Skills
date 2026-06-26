## Description: <br>
Reliable Feishu file sending workflow for avoiding missing attachments, mediaLocalRoots path issues, and combined text plus file delivery failures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yujunyanyanya](https://clawhub.ai/user/yujunyanyanya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to send generated or edited files to Feishu users reliably, especially when diagnosing missing attachments or Feishu file delivery failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Files outside allowed mediaLocalRoots may fail to send or may not appear to the recipient. <br>
Mitigation: Place files under the default workspace or another allowed mediaLocalRoots directory before sending. <br>
Risk: Adding broad directories such as /tmp to mediaLocalRoots can expand which local files the messaging system may send. <br>
Mitigation: Only whitelist directories that are intended for sharing and send files the user explicitly wants delivered. <br>
Risk: Combining explanatory text and an attachment in one Feishu outbound message can make attachments unreliable. <br>
Mitigation: Send any text first, then send the file as a separate attachment-only message. <br>


## Reference(s): <br>
- [Feishu file sending notes](references/feishu-file-sending-notes.md) <br>
- [ClawHub skill page](https://clawhub.ai/yujunyanyanya/yujunyanyanya-feishu-file-send) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration instructions] <br>
**Output Format:** [Markdown guidance with tool usage patterns and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides agents to send Feishu text and attachments as separate messages and to keep file paths inside allowed mediaLocalRoots.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
