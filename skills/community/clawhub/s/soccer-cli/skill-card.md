## Description: <br>
A CLI to check soccer scores, game details, and player stats from your terminal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jrojas537](https://clawhub.ai/user/jrojas537) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to install and run a terminal soccer CLI for recent scores, match events, and player statistics using a user-provided API-Football key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer compiles and places a local executable in ~/.local/bin. <br>
Mitigation: Review the included source and installer before running it, and install only in environments where a user-local executable is acceptable. <br>
Risk: The CLI depends on an API-Football key stored in a local configuration file. <br>
Mitigation: Use a dedicated API-Football key with the minimum needed access and keep ~/.config/soccer-cli/config.yaml private. <br>
Risk: Server-resolved source provenance is unavailable for this release. <br>
Mitigation: Treat the artifact as the review source of record and do not rely on repository claims that are not present in server provenance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jrojas537/soccer-cli) <br>
- [API-Football](https://www.api-football.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with shell commands, YAML configuration snippets, and terminal table output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Go 1.18 or newer and a user-provided API-Football key stored in a local config file.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
