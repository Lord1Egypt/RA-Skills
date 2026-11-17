## Description:

Provides an OpenClaw party-game skill for playing Who Is Undercover with 4-10 participants, AI opponents, turn-based descriptions, voting, and game status commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq5776569](https://clawhub.ai/user/qq5776569)

### License/Terms of Use:

MIT-0

## Use Case:

External users can run this ClawHub/OpenClaw skill to play the Who Is Undercover social deduction game with AI-controlled participants. The skill supports starting or joining games, submitting descriptions, voting, checking status, and ending a game.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled integration scripts include an exposed InStreet API credential.

Mitigation: Remove the credential from the package, rotate it, and require users to provide their own secret through supported configuration before installation.

Risk: External network integration is under-disclosed.

Mitigation: Document or remove the InStreet and Feishu network integration, and require review of network permissions before deployment.

Risk: Status behavior may mutate or export hidden game state unexpectedly.

Mitigation: Constrain status handlers to read-only behavior and verify they do not reveal private role or word state during active games.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qq5776569/skills/who-is-undercover-publish)
- [Metadata homepage](https://github.com/long5/who-is-undercover)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-style chat responses with inline slash commands and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stateful turn-based game responses; no token cap stated.]

## Skill Version(s):

1.0.0 (source: server release metadata, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
