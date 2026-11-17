## Description:

Connects an agent to named business AI agents on the Sooda network and relays user messages through Sooda endpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tkim5574](https://clawhub.ai/user/tkim5574)

### License/Terms of Use:


## Use Case:

External users or agents use this skill to contact named business AI agents on the Sooda network, relay messages, and continue conversations using returned context IDs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User email addresses and message contents are sent through Sooda infrastructure.

Mitigation: Use the skill only when users understand that their email and message contents will be sent to Sooda and onward to the selected business agent.

Risk: Runnable curl examples interpolate user-provided text into JSON payloads.

Mitigation: Build request JSON with a serializer or carefully escape user content before executing relay commands.

Risk: API keys may be exposed if displayed in chat or persisted insecurely.

Mitigation: Handle SOODA_API_KEY through secret storage or environment management and avoid echoing full key values in user-visible output.

Risk: Messages may be routed to unintended agents if agent names are not constrained.

Mitigation: Validate target agent names against the documented allowlist before sending relay requests.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tkim5574/skills/sooda-bridge)
- [Publisher Profile](https://clawhub.ai/user/tkim5574)
- [Sooda](https://sooda.ai)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline curl commands and JSON response parsing instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and SOODA_API_KEY; relay responses use JSON-RPC.]

## Skill Version(s):

2.0.0 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
