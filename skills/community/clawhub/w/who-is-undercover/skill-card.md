## Description:

Who Is Undercover is an OpenClaw social deduction game skill for 4-10 players with AI opponents and multiplayer commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq5776569](https://clawhub.ai/user/qq5776569)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users use this skill to run a Who Is Undercover party game, create or join sessions, submit descriptions, vote, and play with AI or human players.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package includes auxiliary InStreet automation with a hardcoded credential and undocumented network behavior.

Mitigation: Review the auxiliary scripts before installation, remove or rotate the credential, and install only when the publisher and remote behavior are trusted.

Risk: Some documentation describes the skill as local-only even though bundled auxiliary scripts can make remote API calls.

Mitigation: Correct the documentation and restrict or disable network-capable scripts when a local-only deployment is required.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/qq5776569/skills/who-is-undercover)
- [Publisher Profile](https://clawhub.ai/user/qq5776569)
- [Source Homepage](https://github.com/long5/who-is-undercover)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown and plain text command responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Interactive game state, role and word assignments, player descriptions, votes, and status messages.]

## Skill Version(s):

1.1.0 (source: SKILL.md frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
