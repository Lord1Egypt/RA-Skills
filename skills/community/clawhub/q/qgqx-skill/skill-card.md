## Description:

This skill launches the single-file HTML strategy game 七国群雄传 (Seven Kingdoms Tactics), a 三国群英传-style isometric turn-based wargame.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hmily741963](https://clawhub.ai/user/hmily741963)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to launch a browser-based Seven Warring States strategy game, choose campaign or skirmish mode, and play against AI, on the same device, or through optional network play.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional multiplayer relay is inconsistently described and lacks basic protections, so enabling network play can expose users to untrusted servers, room participants, or networks.

Mitigation: Prefer local single-player or same-device play; only run net-server.js or enter a remote WebSocket server when the server, participants, and network are trusted, and do not expose the relay broadly on the Internet.

Risk: The skill copies bundled game files into the workspace and browser play can store progress in localStorage.

Mitigation: Run it in a workspace where copied HTML files are expected, and clear the browser's site storage for the game if saved progress should be removed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hmily741963/skills/qgqx-skill)
- [ClawHub publisher profile](https://clawhub.ai/user/hmily741963)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell commands and copied HTML game files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a playable local HTML game copy; optional WebSocket relay setup is only needed for separate-device network play.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
