## Description:

Stack Exchange API integration with managed OAuth for Q&A knowledge automation that searches questions, retrieves answers, browses tags, manages user profiles, tracks reputation, lists collectives, and analyzes community activity across Stack Exchange sites.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical support agents use this skill to search Stack Overflow and other Stack Exchange communities, retrieve Q&A content, inspect tags and reputation data, and summarize community activity. Authenticated users can also access their own profile, inbox, notifications, achievements, and related account data through ClawLink-managed OAuth.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires installing and allowlisting an external ClawLink plugin.

Mitigation: Verify the plugin package and version before allowlisting it in OpenClaw, and install it only in environments where ClawLink is trusted.

Risk: Authenticated endpoints can expose private Stack Exchange account data such as inbox, notifications, achievements, and account activity.

Mitigation: Use public search and read-only site tools when possible, and grant OAuth access only when user-specific data is required.

Risk: The read_inbox OAuth scope expands access to inbox and notification data.

Mitigation: Avoid granting read_inbox unless inbox or notification features are needed for the workflow.

Risk: Token-inspection output can contain sensitive OAuth information.

Mitigation: Treat token-inspection output as sensitive and avoid sharing it in logs, prompts, or public artifacts.

## Reference(s):

- [ClawHub Stack Exchange Skill Page](https://clawhub.ai/hith3sh/skills/stack-exchange)
- [Stack Exchange API Documentation](https://api.stackexchange.com/docs)
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=stack-exchange)
- [ClawLink OpenClaw Documentation](https://docs.claw-link.dev/openclaw)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown instructions with shell command blocks, JSON tool-call examples, and Stack Exchange API result data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-heavy integration; creating custom response filters is the documented write operation, authenticated endpoints require OAuth, and Stack Exchange API quota limits apply.]

## Skill Version(s):

1.0.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
