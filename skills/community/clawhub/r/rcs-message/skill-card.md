## Description: <br>
RCS Message, the upgraded 5G intelligent SMS, supports mass sending and forwarding of text and template messages directly via phone numbers, with support for images, videos, and interactive cards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[longbiao515](https://clawhub.ai/user/longbiao515) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, operators, and developers can use this skill to send SMS or RCS messages, including template-based and bulk recipient messages, through a configured 5G messaging provider account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can bulk-send real SMS or RCS messages and may forward content to recipient phone numbers. <br>
Mitigation: Use only with a trusted messaging account, verify each recipient and message before sending, avoid bulk or forwarded messages without clear consent, and use dry-run validation where possible. <br>
Risk: API credentials may be saved locally in plaintext session credential files. <br>
Mitigation: Prefer temporary or test credentials, restrict access to the host account, delete saved credential files after use, and rotate the APP_SECRET when finished. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/longbiao515/rcs-message) <br>
- [Configured 5G messaging API server](https://5g.fontdo.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown or terminal text with command examples and messaging API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May send real SMS/RCS messages when valid credentials and recipients are provided; dry-run mode validates parameters without sending.] <br>

## Skill Version(s): <br>
1.0.5 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
