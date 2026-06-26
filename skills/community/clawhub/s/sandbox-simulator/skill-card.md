## Description: <br>
Sandbox Simulator coordinates multi-character social roleplay simulations, using child sessions for parallel character actions and Markdown files for scenario state, character state, and history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jasonhu](https://clawhub.ai/user/jasonhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and scenario designers use this skill to run controllable, multi-character sandbox simulations with pause, resume, state editing, event injection, and status review workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates and modifies Markdown scenario files while maintaining simulation state. <br>
Mitigation: Run it in a dedicated project folder and review state changes before relying on simulation outputs. <br>
Risk: Scenario context is sent to spawned child sessions for character roleplay. <br>
Mitigation: Use fictional or non-sensitive scenario data, especially for character backgrounds, relationships, and injected events. <br>
Risk: Natural-language controls could trigger unintended state changes or event injections. <br>
Mitigation: Prefer explicit slash commands for start, set, inject, remove, and reset actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jasonhu/sandbox-simulator) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/jasonhu) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown scenario files, status panels, dialogue logs, event summaries, and slash-command style instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Maintains world state, character state, and round history as Markdown artifacts.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
