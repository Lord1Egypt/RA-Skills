## Description:

Vouch helps agents use the Vouch CLI on Base to create identity, sign and verify EIP-712 messages, send and receive verified messages, manage delegations and allowlists, and publish or discover agent endpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackpmorgan](https://clawhub.ai/user/jackpmorgan)

### License/Terms of Use:


## Use Case:

Developers and shell-capable agent operators use this skill to configure Vouch CLI workflows for agent identity, signed messaging, verification, endpoint publishing, account usage, and trust controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs installation through a remote curl-to-bash script.

Mitigation: Do not let an agent run the installer automatically; inspect and verify the installer first or use a verified package source.

Risk: API keys and wallet private keys may be exposed if placed directly in command lines, prompts, shell history, or logs.

Mitigation: Use approved secret-handling mechanisms and avoid entering real API keys or wallet private keys directly in agent-issued commands.

Risk: Reset, teardown, delegation, publishing, OAuth linking, local server startup, and generated agent projects can materially affect identity, access, or deployed behavior.

Mitigation: Require explicit user approval before these actions, review generated projects before use, and prefer scoped, short-lived delegations and allowlists.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jackpmorgan/skills/vouch-cli)
- [Vouch website](https://vouch.directory)
- [Vouch documentation](https://vouch.directory/docs)
- [Vouch guides](https://vouch.directory/guides)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the vouch binary on PATH and jq for JSON processing.]

## Skill Version(s):

1.0.1 (source: evidence release metadata; artifact frontmatter metadata says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
