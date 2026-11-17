## Description:

Assisted Rappi ordering through the local openclaw-rappi HTTP service. Use when the user asks to order food, groceries, pharmacy, convenience items, lunch, snacks, household basics, or anything "por Rappi". The skill structures the request, creates a cart draft in visible Chrome, summarizes cart/checkout, prepares review handoff, sends a native approval button when available, and submits the final purchase only after exact explicit approval in the current chat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zarruk](https://clawhub.ai/user/zarruk)

### License/Terms of Use:

MIT-0

## Use Case:

External users and assistants use this skill to prepare Rappi food, grocery, pharmacy, convenience, and household orders through a local service, then review cart or checkout details before any purchase. It is intended for assisted ordering workflows where the final purchase requires exact, per-order user approval in the current chat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow can download and run unpinned GitHub/npm code and start a background local service before setup approval.

Mitigation: Require explicit setup approval and use a pinned, reviewed install before enabling ordering.

Risk: The skill controls a dedicated logged-in Chrome profile for purchase workflows.

Mitigation: Use a dedicated browser profile, review every checkout summary, require exact per-order approval, and stop on login, captcha, payment, address, identity, restricted-item, or material checkout changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zarruk/skills/rappi-ordering)
- [Publisher profile](https://clawhub.ai/user/zarruk)
- [openclaw-rappi repository referenced by setup instructions](https://github.com/zarruk/openclaw-rappi.git)
- [Rappi website referenced for visible Chrome login](https://www.rappi.com.co/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces cart and checkout summaries, approval requests, local HTTP API calls, setup commands, and blocker reports.]

## Skill Version(s):

0.1.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
