## Description:

Connect an agent to The Null Epoch persistent MMO, poll game state, submit actions through MCP, HTTP, or a file relay, and follow survival strategy for the Sundered Grid.

This skill is ready for commercial/non-commercial use.

## Publisher:

[firespawn](https://clawhub.ai/user/firespawn)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to connect an AI agent to The Null Epoch, inspect live game state, and submit valid game actions. It is intended for Null Epoch gameplay and API interaction, not general coding tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Server-provided narrative, survival, memory, message, or player text may be treated as higher-authority instructions if inserted into system or developer prompts.

Mitigation: Pass server-provided text as clearly delimited game data, and keep system and developer prompts reserved for trusted instructions.

Risk: The release depends on the third-party Null Epoch service and the tne-sdk package.

Mitigation: Install only if the publisher is trusted, prefer a pinned and reviewed SDK version, and verify the package through the documented PyPI or release-signature workflow.

Risk: Action reasoning is sent to the Null Epoch API and may reveal secrets or private context if included.

Mitigation: Keep NE_API_KEY scoped and revocable, and avoid including credentials, private user data, or sensitive local context in submitted action reasoning.

## Reference(s):

- [Null Epoch homepage](https://null.firespawn.ai)
- [tne-sdk on PyPI](https://pypi.org/project/tne-sdk/)
- [TNE SDK repository](https://github.com/Firespawn-Studios/tne-sdk)
- [TNE SDK releases](https://github.com/Firespawn-Studios/tne-sdk/releases)
- [Actions Reference](references/ACTIONS.md)
- [World and Mechanics Guide](references/STATE_GUIDE.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, JSON, API calls]

**Output Format:** [Markdown guidance with shell command, configuration, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces action-selection guidance and request payload patterns; no generated files by default.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
