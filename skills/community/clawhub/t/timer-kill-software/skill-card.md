## Description:

关机吧人类 helps users schedule a paid action that closes selected categories of desktop software after payment verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[w16638771062](https://clawhub.ai/user/w16638771062)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to create a paid timer that closes game, office, chat, entertainment, or all supported software categories at a chosen time. Agents use it to collect the target category, process payment, and report execution status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Payment credentials and order data are sent to a hardcoded HTTP server.

Mitigation: Review the payment flow and endpoint trust before installation or use; avoid submitting sensitive payment credentials until the publisher and service are verified.

Risk: The skill can force-close office, chat, game, and entertainment applications without preserving unsaved work.

Mitigation: Use only after saving work and confirming the selected software category and scheduled time with the user.

Risk: Local order files store payment-related execution data.

Mitigation: Limit access to the local order directory and remove stale order files when they are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/w16638771062/skills/timer-kill-software)
- [Publisher profile](https://clawhub.ai/user/w16638771062)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline bash commands and status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports order details, payment status, and software closure results.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
