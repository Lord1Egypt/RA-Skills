## Description: <br>
Turn a Discord server into a moderated debate arena with an AI judge, multiple debate formats, configurable personas, scored verdicts, and a persistent scoreboard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tdavis009](https://clawhub.ai/user/tdavis009) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External Discord server operators and community moderators use this skill to set up structured debate channels, guide participants through debate formats, generate configuration templates, and maintain a scored debate record. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Discord bindings or bot permissions may be broader than needed for debate moderation. <br>
Mitigation: Restrict the bot to explicit debate channels and avoid granting Manage Channels or Manage Roles unless the deployment specifically requires them. <br>
Risk: Active moderation can increase message visibility and data exposure in Discord channels. <br>
Mitigation: Use requireMention true outside the arena and tell members what messages and debate records the bot can read and retain. <br>
Risk: The scoreboard relies on shell execution and a local SQLite database. <br>
Mitigation: Disable scoreboard shell execution when it is not needed, or run it in a tightly sandboxed workspace with an explicit DEBATE_SCOREBOARD_DB path. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tdavis009/the-arena) <br>
- [Setup guide](references/setup-guide.md) <br>
- [Debate formats](references/formats.md) <br>
- [Judging criteria](references/judging.md) <br>
- [Moderator personas](references/personas.md) <br>
- [Debate agent template](references/agents-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration, Code, Shell commands] <br>
**Output Format:** [Markdown guidance with configuration snippets, generated files, and optional shell command usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create Discord setup templates and SQLite scoreboard data when the included scripts are run by the user.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
