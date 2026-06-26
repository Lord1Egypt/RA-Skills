## Description: <br>
Send, compose, reply, reply-all, or forward emails with HTML formatting and attachments from a Ravi email account; it is not for reading incoming email or handling credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[raunaksingwi](https://clawhub.ai/user/raunaksingwi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users or agents with an authenticated Ravi CLI use this skill to draft and send new email, replies, reply-all responses, and forwards with HTML bodies and attachments. It should be paired with Ravi contact, inbox, and writing skills when resolving recipients, replying to existing messages, or drafting polished email content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated CLI use can send email from the user's Ravi account or upload selected local files without clearly declared approval boundaries. <br>
Mitigation: Require explicit user approval before each compose, reply, reply-all, forward, or attachment operation; confirm recipients, subject, body, and selected files before execution. <br>
Risk: The artifact does not declare where the Ravi CLI comes from, which account it sends from, or where credentials are stored. <br>
Mitigation: Confirm the CLI source, account identity, and credential storage model before installing the skill or granting it access to an authenticated Ravi environment. <br>
Risk: Bulk or repeated sends can hit Ravi account rate limits or create unintended outbound email volume. <br>
Mitigation: Honor the documented 60 emails per hour and 500 emails per day limits, parse retry_after_seconds on 429 responses, and avoid autonomous send loops. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/raunaksingwi/ravi-email-send) <br>
- [Ravi Messages API schema](https://ravi.id/docs/schema/messages.json) <br>
- [Ravi Attachments API schema](https://ravi.id/docs/schema/attachments.json) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, Guidance] <br>
**Output Format:** [Markdown guidance with inline bash command examples and HTML email body examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes Ravi CLI command patterns for composing, replying, reply-all, forwarding, recipient resolution, and rate-limit handling.] <br>

## Skill Version(s): <br>
2.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
