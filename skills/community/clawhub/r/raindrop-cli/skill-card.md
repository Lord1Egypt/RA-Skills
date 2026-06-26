## Description: <br>
Manage Raindrop.io bookmarks from the command line using the Raindrop REST API and a personal RAINDROP_TOKEN. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adorostkar](https://clawhub.ai/user/adorostkar) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to search, add, update, and remove Raindrop.io bookmarks from shell workflows while using a personal Raindrop.io token. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The submitted bundle references a raindrop command script that is not included. <br>
Mitigation: Before installing, verify which raindrop command will run in the environment and use only a trusted implementation. <br>
Risk: The skill can change or remove bookmarks using a personal RAINDROP_TOKEN. <br>
Mitigation: Store RAINDROP_TOKEN securely, keep it out of logs and shell history, and review update or remove actions before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/adorostkar/raindrop-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Raindrop.io bookmark identifiers and requires RAINDROP_TOKEN for authenticated operations.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
