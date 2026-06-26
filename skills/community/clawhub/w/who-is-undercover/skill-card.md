## Description: <br>
Who Is Undercover is an OpenClaw social deduction game skill that supports 4-10 players, AI opponents, multiplayer sessions, descriptions, voting, status checks, and game-ending commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qq5776569](https://clawhub.ai/user/qq5776569) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users install this skill to run a turn-based party deduction game where human players and AI opponents submit descriptions, vote on suspected undercover players, and continue until a winning side is determined. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release includes helper code for an external game service with an embedded API key. <br>
Mitigation: Remove and rotate the embedded key, load secrets from a controlled runtime secret store, and clearly disclose any external-service integration before installation. <br>
Risk: Status and helper scripts can reveal or alter game state, including roles, words, descriptions, or votes. <br>
Mitigation: Make status tooling read-only by default, limit role and word visibility to the owning player session, and keep mutable helper scripts out of normal gameplay paths unless explicitly enabled. <br>
Risk: Any active participant may be able to end a multiplayer game. <br>
Mitigation: Restrict game-ending actions to the creator, an administrator, or an explicit group-confirmed flow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qq5776569/who-is-undercover) <br>
- [Project homepage](https://github.com/long5/who-is-undercover) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Chat messages with command responses, game status summaries, role or word prompts, descriptions, vote results, and final game results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include per-session game state summaries and user-facing command guidance.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
