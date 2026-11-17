## Description:

Snake Rodeo is an autoplay daemon for the Trifle Snake Rodeo game that connects to a live game server, authenticates via wallet, and votes on snake directions using pluggable AI strategies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[okwme](https://clawhub.ai/user/okwme)

### License/Terms of Use:

MIT

## Use Case:

Players and developers use Snake Rodeo to automate Trifle Snake Rodeo gameplay, inspect game state and balance, submit manual votes, and tune or build AI strategies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The daemon can spend live account game balance when it submits votes.

Mitigation: Use staging first, configure conservative balance and round-budget limits, and monitor daemon status before enabling live autoplay.

Risk: The package installs mutable dependency code from snake-rodeo-agents.

Mitigation: Pin snake-rodeo-agents to a reviewed commit or release before installation.

Risk: Telegram logging can expose gameplay or status data to Telegram and configured chat members, and bot tokens are sensitive.

Mitigation: Prefer the TELEGRAM_BOT_TOKEN environment variable, avoid storing bot tokens in settings, and only enable Telegram logging for trusted chats.

## Reference(s):

- [Snake Rodeo ClawHub listing](https://clawhub.ai/okwme/skills/snake-rodeo)
- [Snake Rodeo homepage](https://snake.rodeo)
- [Trifle Snake Rodeo](https://trifle.life)
- [snake-rodeo-agents library](https://github.com/trifle-labs/snake-rodeo-agents)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands, JavaScript examples, configuration keys, and daemon status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May start, stop, pause, resume, and inspect a local daemon that interacts with live or staging Snake Rodeo servers.]

## Skill Version(s):

3.2.1 (source: server-resolved release metadata and clawdhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
