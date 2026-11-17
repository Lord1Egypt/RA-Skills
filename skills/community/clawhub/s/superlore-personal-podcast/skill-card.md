## Description:

Pair OpenClaw with Superlore to create or upload private podcast episodes and use saved Sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adamjurgens](https://clawhub.ai/user/adamjurgens)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect OpenClaw with Superlore, create private podcast episodes from prompts, upload authorized audio, and optionally use saved Superlore Sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential-bearing requests may be sent to server-supplied absolute URLs without validating the destination.

Mitigation: Validate credential-bearing URLs against the expected Superlore HTTPS origin before sending tokens, and review the helper before installation.

Risk: The skill stores and uses a Superlore agent credential for episode, upload, or source access.

Mitigation: Approve only the minimal scopes needed for the workflow and confirm how to revoke or rotate the Superlore agent credential.

Risk: Generated listen URLs are private and may expose user audio if shared.

Mitigation: Treat returned listen URLs as private and avoid posting them in chat, logs, or shared memory.

## Reference(s):

- [Superlore OpenClaw Integration](https://superlore.ai/integrations/openclaw)
- [Superlore Agent Pairing](https://superlore.ai/agents)
- [ClawHub Skill Page](https://clawhub.ai/adamjurgens/skills/superlore-personal-podcast)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON helper output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The helper may store a Superlore agent credential locally with restrictive file permissions and may print private listen URLs.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
