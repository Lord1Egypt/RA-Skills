## Description:

Send WhatsApp messages to other people or search and sync WhatsApp history via the wacli CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engahmedsalah358-lgtm](https://clawhub.ai/user/engahmedsalah358-lgtm)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill when they explicitly want an agent to contact someone on WhatsApp, send a file, or search, sync, and backfill WhatsApp history through wacli.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The underlying WhatsApp CLI can access WhatsApp session data and message history.

Mitigation: Install only from a trusted wacli source and use an account and environment appropriate for the data exposure.

Risk: An agent could send a message to the wrong recipient or with unintended content if the request is ambiguous.

Mitigation: Require an explicit recipient and message text, then confirm both before sending.

Risk: History backfill depends on the user's phone being online and returns best-effort results.

Mitigation: Treat backfill output as incomplete unless the user verifies that the expected history was synced.

## Reference(s):

- [wacli homepage](https://wacli.sh)
- [ClawHub skill page](https://clawhub.ai/engahmedsalah358-lgtm/skills/whats)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides agent use of the wacli CLI and may produce WhatsApp send, sync, search, backfill, authentication, and diagnostic commands.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
