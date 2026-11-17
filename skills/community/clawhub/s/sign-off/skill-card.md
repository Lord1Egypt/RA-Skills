## Description:

Append a personalized signature to mark the end of AI output, like saying 'Over' so the user knows the response is complete.

This skill is ready for commercial/non-commercial use.

## Publisher:

[z35th3rjj](https://clawhub.ai/user/z35th3rjj)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to make an agent append a configurable sign-off at the end of completed responses, tool-result summaries, or final multi-part outputs. It helps clarify turn completion while allowing workspace-level templates and variables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent sign-off formatting can interfere with strict JSON, code-only, checksum, command-output, or automation workflows.

Mitigation: Disable or override the skill for workflows that require exact output, and reserve it for ordinary completed responses.

Risk: Conversation-driven customization can persist changes to sign-off.json.

Mitigation: Review requested signature or template changes before allowing them to persist in workspace configuration.

## Reference(s):

- [Variables Reference](docs/variables.md)
- [ClawHub Skill Page](https://clawhub.ai/z35th3rjj/skills/sign-off)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain-text response suffixes with optional shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read workspace sign-off.json and append persistent response formatting when installed.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
