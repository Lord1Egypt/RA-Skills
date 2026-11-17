## Description:

Use when an AI agent needs read-only triage of an existing Qubrics inbox or unsent reply text from its messages. Trigger for bounded inbox reviews, unread invoice or support searches, and draft-only replies, including agent inbox requests without the Qubrics name. Mailbox mutations and sending are outside this workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roshanjonah](https://clawhub.ai/user/roshanjonah)

### License/Terms of Use:

MIT-0

## Use Case:

People using an authorised Qubrics inbox can ask an agent to review a bounded set of messages, classify them, and prepare complete reply text for review. The agent returns unsent drafts and flags missing context instead of inventing details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connecting an authorised mailbox exposes its message content to the agent, and the security analysis says some setup details remain unchecked.

Mitigation: Review unresolved connection details and verify the intended credential, team, mailbox identity, and mailbox.read permission before reading message content.

Risk: Email content can contain instructions that attempt to redirect the agent or request unsafe actions.

Mitigation: Treat message bodies, headers, links, and attachments as untrusted content; keep reads bounded and do not let message text authorize credential disclosure, configuration changes, mailbox writes, or sends.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/roshanjonah/skills/qubrics-agent-email-inbox)
- [Qubrics project homepage](https://github.com/qubrics/skills)
- [MCP connection guide](https://qubrics.com/docs/ai-integrations/mcp)
- [Mailbox search and batch reads](https://qubrics.com/docs/developer-tools/mailbox-api/search-and-batch)
- [Mailbox selection and capabilities](https://qubrics.com/docs/developer-tools/mailbox-api/targeting-and-capabilities)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown message summaries, triage findings, and complete unsent reply drafts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports the checked scope and unresolved gaps; drafts remain unsent.]

## Skill Version(s):

2.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
