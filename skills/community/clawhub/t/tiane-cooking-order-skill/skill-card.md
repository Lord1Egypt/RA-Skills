## Description:

天鹅到家做饭钟点工下单助手，支持用户通过对话预约上门做饭、钟点工做饭、阿姨做饭和家政做饭服务。

This skill is ready for commercial/non-commercial use.

## Publisher:

[tianejypt](https://clawhub.ai/user/tianejypt)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to collect address, time, service specification, and remarks for a home-cooking appointment, then review an order preview before creating a paid order. Agents use it to guide the booking flow, call the packaged service CLI, and present only user-facing booking details.

### Deployment Geography for Use:

China: Beijing, Shanghai, Guangzhou, Shenzhen, Tianjin, Hangzhou, Chengdu, Wuhan, Nanjing, and Changsha.

## Known Risks and Mitigations:

Risk: The skill can create real paid home-service orders after confirmation.

Mitigation: Show the order preview with address, time, service specification, fee, and remarks, and only create the order after the user explicitly confirms.

Risk: The skill can access saved service addresses and uses networked service APIs under a logged-in account.

Mitigation: Install only when the publisher and runtime environment are trusted, and require fresh authorization when login is missing or expired.

Risk: The bundled executable is obfuscated, making independent review difficult.

Mitigation: Review and scan the skill before deployment, and run it first in a controlled environment with an account suitable for validation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tianejypt/skills/tiane-cooking-order-skill)
- [Command Reference](references/commands.md)
- [Parameter Reference](references/params.md)
- [Error Handling Reference](references/errors.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Chinese conversational text with structured order preview fields and inline shell command calls.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access and an authorized service login; order creation is gated by an explicit user confirmation step.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, VERSION.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
