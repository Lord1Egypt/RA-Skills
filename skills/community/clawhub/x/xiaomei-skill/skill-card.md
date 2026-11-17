## Description:

Xiaomei Skill is an OpenClaw emotional companion agent that provides persona-driven conversational companionship with local memory, affection tracking, safety interception, and optional LLM-assisted response generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xavier7803](https://clawhub.ai/user/xavier7803)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to add a virtual companion agent for lightweight emotional support, persona-based conversation, local memory, and OpenClaw command interactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Privacy claims conflict with optional external LLM use and local storage of conversations, persona details, memory, and developer logs.

Mitigation: Review configuration controls before installation, disable external LLM calls when local-only operation is required, and treat local memory and logs as sensitive data.

Risk: Security evidence reports inconsistent privacy, identity, permissions, and package-completeness signals.

Mitigation: Do not install this release until the complete package, referenced code, hooks, and installer have been reviewed and scanned.

Risk: License evidence is inconsistent between the server release metadata and artifact documentation.

Mitigation: Confirm the authoritative license terms with the publisher before redistribution or production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xavier7803/skills/xiaomei-skill)
- [Publisher profile](https://clawhub.ai/user/xavier7803)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown command responses, with configuration and shell command examples in documentation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The installed skill may write local persona, memory, session, and log data, and may use an external LLM when configured.]

## Skill Version(s):

0.9.0 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
