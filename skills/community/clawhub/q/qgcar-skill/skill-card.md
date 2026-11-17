## Description:

Use when the user wants help with Qiguan campus bus tickets using the local qg CLI, including listing schedules, choosing Zhuhai/South/East campus routes, generating WeChat order-entry links, copying links, or troubleshooting qg/qg-list commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qybaihe](https://clawhub.ai/user/qybaihe)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to list Qiguan campus bus schedules and prepare WeChat order-entry links for supported Zhuhai, South Campus, and East Campus routes. The skill is intended to support schedule lookup and link generation, not passenger submission, order completion, or payment.

### Deployment Geography for Use:

Global; functional use is specific to supported Qiguan campus bus routes serving Zhuhai, South Campus, and East Campus.

## Known Risks and Mitigations:

Risk: The installer uses mutable remote code, global npm installation, and replacement of local Codex/OpenClaw skill directories.

Mitigation: Install only after trusting the publisher, reviewing the installer, and preferring an audited pinned release with checksum verification and an explicit destination.

Risk: Generated WeChat links are order-entry links and could be mistaken for completed bookings.

Mitigation: Tell users that passenger selection, order confirmation, and payment must be completed manually in WeChat.

Risk: Requests to automate passenger submission, identity data handling, order saving, or payment exceed the skill's safe boundary.

Mitigation: Limit use to schedule lookup and link generation, and refuse automation that would submit passenger information or trigger payment.

## Reference(s):

- [QG CLI Reference](references/qg-cli.md)
- [ClawHub Skill Page](https://clawhub.ai/qybaihe/skills/qgcar-skill)
- [qg-skill npm Package](https://www.npmjs.com/package/qg-skill)
- [Qiguan bus API endpoint](https://ebk.17u.cn/cxyopenapi)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands, schedule summaries, and plain copyable WeChat order-entry links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include qg/qg-list commands, route options, troubleshooting guidance, and order-entry links that require the user to complete passenger selection and payment in WeChat.]

## Skill Version(s):

0.1.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
