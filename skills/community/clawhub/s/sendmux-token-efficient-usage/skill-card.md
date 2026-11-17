## Description:

Choose low-token Sendmux calls across MCP, CLI, SDKs, and HTTP by using snippets, counts, batches, deltas, cursors, ETags, and idempotency.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sendmux.ai](https://clawhub.ai/user/sendmux.ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this guide to choose efficient Sendmux email, mailbox, and management operations while limiting unnecessary data retrieval and repeated requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Send, delete, or management actions can change account data or send email.

Mitigation: Review each requested action before execution and grant management access only when needed.

Risk: Broad credentials or unnecessary mailbox reads can expose sensitive content.

Mitigation: Use scoped credentials where possible, keep secrets out of chat, and prefer snippets or targeted reads.

## Reference(s):

- [Sendmux skills homepage (listed in skill metadata)](https://github.com/Sendmux/skills)
- [ClawHub skill release](https://clawhub.ai/sendmux.ai/skills/sendmux-token-efficient-usage)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration instructions]

**Output Format:** [Markdown guidance with command and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommends scoped credentials, narrow reads, batching, and safe retries.]

## Skill Version(s):

1.0.11 (source: ClawHub release metadata; artifact frontmatter says 1.7.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
