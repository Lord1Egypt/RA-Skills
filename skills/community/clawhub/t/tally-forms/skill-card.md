## Description: <br>
Manage Tally forms, submissions, respondents, fields, and form workflows from chat via the Tally API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and form administrators use this skill to inspect Tally forms and submissions, manage respondents and fields, and perform confirmed form workflow changes through ClawLink-backed Tally access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires OAuth-backed access to the user's Tally account through ClawLink. <br>
Mitigation: Install only when the user trusts ClawLink to broker Tally access and verify the Tally connection before calling tools. <br>
Risk: Form submissions and respondent data may contain personal information. <br>
Mitigation: Review returned data carefully and handle submissions, respondents, and field values according to applicable privacy practices. <br>
Risk: Write actions can change forms, notifications, workflows, submissions, or delete data irreversibly. <br>
Mitigation: Use previews and obtain explicit confirmation before executing form edits, notification changes, submissions, or deletions. <br>


## Reference(s): <br>
- [ClawHub Tally Skill Page](https://clawhub.ai/hith3sh/tally-forms) <br>
- [Tally Developer Docs](https://tally.so/developers) <br>
- [Tally Webhooks Help](https://tally.so/help/webhooks) <br>
- [ClawLink OpenClaw Docs](https://docs.claw-link.dev/openclaw) <br>
- [ClawLink Service](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=tally-forms) <br>
- [ClawLink Verification](https://claw-link.dev/verify) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON tool-call parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a connected Tally account through ClawLink; write actions are previewed and require explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
