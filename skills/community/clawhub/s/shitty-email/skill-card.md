## Description: <br>
Create and manage temporary disposable email inboxes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johanski](https://clawhub.ai/user/johanski) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, testers, and privacy-conscious users use this skill to create temporary inboxes, poll for incoming messages, retrieve verification content, extend inbox lifetime, and delete disposable inboxes when finished. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Temporary inboxes are unsuitable for password resets, account recovery, regulated data, private correspondence, or accounts requiring long-term control. <br>
Mitigation: Use the skill only for low-risk temporary signups, testing, and disposable verification flows. <br>
Risk: The inbox token controls access to messages for the inbox session. <br>
Mitigation: Treat the token like a temporary password, reuse it only for the intended session, and avoid sharing it in public logs or transcripts. <br>
Risk: Disposable messages may persist until the inbox expires or is deleted. <br>
Mitigation: Delete the inbox when finished and confirm messages are no longer needed before cleanup. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/johanski/shitty-email) <br>
- [Shitty Email service](https://shitty.email) <br>
- [Create or check inbox API](https://shitty.email/api/inbox) <br>
- [Retrieve email content API](https://shitty.email/api/email/{email_id}) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces temporary inbox details, polling instructions, email summaries, extracted verification codes or links, and cleanup guidance.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
