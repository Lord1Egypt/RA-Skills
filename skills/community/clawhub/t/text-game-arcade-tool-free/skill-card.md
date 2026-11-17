## Description: <br>
文字游戏机免费版 helps an agent create and run local text games, including branching adventures, mystery stories, romance simulations, interactive fiction, character interactions, and save/load workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill for personal entertainment, interactive fiction drafting, plot practice, and text-game prototyping. It is intended for local, single-user text game generation and play rather than graphical game production or collaborative editing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests broad command execution capability for a text-game workflow. <br>
Mitigation: Review commands before execution and limit command use to explicit, user-approved save, configuration, export, or game-run actions. <br>
Risk: The skill presents itself as offline-only but includes network troubleshooting guidance. <br>
Mitigation: Disable or require approval for outbound network checks unless the user explicitly asks to diagnose connectivity. <br>
Risk: Generated stories and branching content can be inconsistent or misleading over long sessions. <br>
Mitigation: Treat generated game content as draft entertainment output and review important plot state, choices, and saved data before reuse. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/text-game-arcade-tool-free) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and plain text with occasional JSON, YAML, Python, and shell snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include interactive story scenes, choice lists, save/config examples, status-style JSON, and execution logs.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
