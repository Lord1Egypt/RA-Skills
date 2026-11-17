## Description:

Read and send emails from an existing Sendook inbox. Use when an AI agent needs to check for new emails, read messages, reply to conversations, or send new emails from a pre-configured inbox. Limited to message operations only -- no inbox creation, domain management, or webhook configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[obaid](https://clawhub.ai/user/obaid)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to let an agent read messages, inspect threads, send new emails, and reply from an authorized Sendook inbox. The skill is scoped to message and thread operations for an already configured inbox.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and send email through a configured Sendook inbox using the user's API key.

Mitigation: Install it only for an inbox the agent is authorized to process, use a least-privileged API key, keep SENDOOK_API_KEY private, and review agent actions before allowing replies or outbound emails.

Risk: Attachments may expose local files if an agent reads files that were not explicitly approved.

Mitigation: Confirm with the user before attaching any local file, attach only explicitly requested files, and keep attachment reads within the current project scope.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/obaid/skills/sendook-openclaw)
- [Skill homepage](https://github.com/obaid/sendook-skills)
- [Sendook Node SDK package](https://www.npmjs.com/package/@sendook/node)
- [Sendook Node SDK source](https://github.com/getrupt/sendook)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with TypeScript, JSON, and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SENDOOK_API_KEY and SENDOOK_INBOX_ID; limited to configured inbox message and thread operations.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
