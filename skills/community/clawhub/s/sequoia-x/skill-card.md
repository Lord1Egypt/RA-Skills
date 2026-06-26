## Description: <br>
Sequoia-X helps agents install, configure, and run an A-share quantitative stock-screening system with Akshare data, SQLite storage, and Feishu notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[djh06](https://clawhub.ai/user/djh06) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to set up Sequoia-X, run stock-selection strategies, adjust strategy parameters, and configure Feishu delivery for results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installation runs mutable external code from the live Sequoia-X GitHub project. <br>
Mitigation: Install only after trusting or reviewing the project, preferably pinned to a reviewed commit and run in an isolated Python environment. <br>
Risk: The skill requires a Feishu webhook that could expose notification access if mishandled. <br>
Mitigation: Keep the Feishu webhook private and store it only in the local .env file. <br>
Risk: The documented reset flow can delete the local SQLite database. <br>
Mitigation: Back up ~/sequoia-x/data/sequoia_v2.db before using the reset command. <br>


## Reference(s): <br>
- [Sequoia-X ClawHub page](https://clawhub.ai/djh06/sequoia-x) <br>
- [Strategy reference](references/strategies.md) <br>
- [Sequoia-X GitHub repository](https://github.com/sngyai/Sequoia-X.git) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash, environment-variable, and Python snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent guidance may include installation commands, run commands, strategy-parameter advice, and configuration steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
