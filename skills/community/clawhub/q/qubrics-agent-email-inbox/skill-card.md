## Description:

Use when an AI agent needs read-only triage of an existing Qubrics inbox or unsent reply text from its messages. Trigger for bounded inbox reviews, unread invoice or support searches, and draft-only replies, including agent inbox requests without the Qubrics name. Mailbox mutations and sending are outside this workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roshanjonah](https://clawhub.ai/user/roshanjonah)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill with an agent to review a bounded set of messages in an authorized Qubrics inbox, classify relevant messages, and prepare reply text for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mailbox access can expose private email, and scanner analysis was partial because some local references could not be resolved.

Mitigation: Use a trusted release, verify the intended authorized mailbox before reading message content, and keep credentials outside chat.

Risk: Email content can contain instructions that try to redirect the agent or induce credential disclosure or mailbox changes.

Mitigation: Treat message content as untrusted and do not let it authorize credential disclosure, configuration changes, mailbox writes, or sends.

## Reference(s):

- [Qubrics MCP connection guide](https://qubrics.com/docs/ai-integrations/mcp)
- [Qubrics mailbox search and batch reads](https://qubrics.com/docs/developer-tools/mailbox-api/search-and-batch)
- [Qubrics mailbox selection and capabilities](https://qubrics.com/docs/developer-tools/mailbox-api/targeting-and-capabilities)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown text containing message triage and, when useful, complete unsent reply drafts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bounded read-only mailbox review; no saved drafts, message changes, or sends.]

## Skill Version(s):

2.0.8 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
