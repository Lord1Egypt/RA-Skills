## Description: <br>
Create and manage StrawPoll polls, meeting polls, and ranking polls from the terminal using the strawpoll CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dedene](https://clawhub.ai/user/dedene) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to create, inspect, update, delete, and automate StrawPoll polls from an agent-assisted terminal workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a StrawPoll API key and may expose account access if credentials are stored insecurely. <br>
Mitigation: Protect the API key, prefer a keyring or secret manager, and avoid placing credentials in shared environment files. <br>
Risk: Update, delete, reset, or forced commands can modify or remove polls unexpectedly. <br>
Mitigation: Confirm poll IDs before state-changing commands and use --force only when the requested action is explicit. <br>
Risk: The skill depends on the upstream strawpoll CLI binary. <br>
Mitigation: Install it only when the upstream strawpoll CLI source and distribution channel are trusted. <br>


## Reference(s): <br>
- [strawpoll-cli flag reference](reference.md) <br>
- [strawpoll-cli repository](https://github.com/dedene/strawpoll-cli) <br>
- [StrawPoll](https://strawpoll.com/) <br>
- [StrawPoll API key settings](https://strawpoll.com/account/settings) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and CLI usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include JSON or plain TSV command-output guidance when scripting StrawPoll workflows.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
