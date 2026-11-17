## Description:

Create personalized Chinese or multilingual greetings for holidays, birthdays, milestones, and customer care, then preview and send them through WeChat only after explicit confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhimibuhui](https://clawhub.ai/user/zhimibuhui)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to draft personalized greetings for personal, holiday, milestone, or customer-care scenarios and optionally deliver them through WeChat after reviewing a preview. It supports single-recipient, multi-recipient, and scheduled sends when the required gateway environment variables are configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send immediate or scheduled WeChat messages through a bearer-token gateway.

Mitigation: Run the delivery script in preview mode first, verify the exact text, recipients, schedule, and confirmation code, and execute only after explicit user confirmation.

Risk: An untrusted operations endpoint or mutable gateway environment variables could expose the token or redirect message delivery.

Mitigation: Use only a trusted HTTPS operations endpoint, keep WX_OPENCLAW_OPS_URL and WX_OPENCLAW_OPS_TOKEN out of untrusted user control, and use a narrowly scoped, revocable token.

Risk: Batch or customer-care greetings can become misleading, spam-like, or overly personal if unsupported details are added.

Mitigation: Use verified personal details only, avoid manipulative urgency or unsupported benefits, and re-preview whenever wording, recipients, punctuation, salutation, or schedule changes.

## Reference(s):

- [Blessing style guide](artifact/references/styles.md)
- [ClawHub skill page](https://clawhub.ai/zhimibuhui/skills/wechat-blessings)
- [Publisher profile](https://clawhub.ai/user/zhimibuhui)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with greeting text, inline bash commands, and JSON preview or execution payloads from the delivery script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 plus WX_OPENCLAW_OPS_URL and WX_OPENCLAW_OPS_TOKEN for execution; preview mode can generate a confirmation code before sending.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
