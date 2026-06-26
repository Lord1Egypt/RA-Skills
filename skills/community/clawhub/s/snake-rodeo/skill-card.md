## Description: <br>
Autoplay daemon for the Trifle Snake Rodeo game that connects to a live game server, authenticates with a Trifle token, and votes on snake directions using pluggable strategies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[okwme](https://clawhub.ai/user/okwme) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to run an automated Snake Rodeo player, inspect game state, submit manual votes, configure strategies, and build custom strategy behavior around the Snake Rodeo game. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run as a persistent authenticated game bot and automatically spend Snake Rodeo ball balance. <br>
Mitigation: Use a game-specific or throwaway Trifle token, review strategy settings before starting, set conservative balance limits, and pause or stop the daemon when finished. <br>
Risk: The package installs a mutable GitHub dependency for the strategy and game client library. <br>
Mitigation: Review or pin the snake-rodeo-agents dependency before use, especially in shared or production-like environments. <br>
Risk: Telegram logging can send game activity to an external chat when configured. <br>
Mitigation: Keep Telegram disabled unless needed and protect any Telegram bot token used for notifications. <br>


## Reference(s): <br>
- [Snake Rodeo Homepage](https://snake.rodeo) <br>
- [Trifle Game Site](https://trifle.life) <br>
- [snake-rodeo-agents Library](https://github.com/trifle-labs/snake-rodeo-agents) <br>
- [ClawHub Skill Page](https://clawhub.ai/okwme/snake-rodeo) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [CLI text output with command examples and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May start or control a persistent local daemon that reads Trifle authentication, polls game state, writes local state and logs, and submits game votes.] <br>

## Skill Version(s): <br>
3.2.1 (source: server release metadata and clawdhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
