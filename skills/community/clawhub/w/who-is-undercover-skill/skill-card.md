## Description:

谁是卧底 - 经典社交推理游戏的AI版本，支持4-10人游戏，包含智能AI对手和完整游戏机制。

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq5776569](https://clawhub.ai/user/qq5776569)

### License/Terms of Use:

MIT-0

## Use Case:

External users can run a Chinese social deduction party game through OpenClaw commands, playing with AI-simulated players for role assignment, descriptions, voting, and win checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Published files include an external InStreet integration with a hard-coded bearer token.

Mitigation: Review before installation; remove or rotate the token and keep any online integration disabled unless needed.

Risk: Documentation presents the normal skill as local-only while the published files also include network-enabled controller code.

Mitigation: Confirm the intended operating mode and disclose network behavior before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qq5776569/skills/who-is-undercover-skill)
- [Project homepage from ClawHub metadata](https://github.com/long5/who-is-undercover)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [OpenClaw command responses, game status summaries, and short markdown/plain-text messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js; supports local game commands and includes an InStreet integration that should be reviewed before use.]

## Skill Version(s):

1.0.2 (source: server release metadata); artifact frontmatter and package.json report 1.0.0

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
