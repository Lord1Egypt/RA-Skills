## Description: <br>
Woop Daily guides a user through a five-minute conversational WOOP exercise that turns a wish into an if-then action plan. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[reffwu](https://clawhub.ai/user/reffwu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill when they want structured help turning a wish, goal, or habit into a concrete WOOP plan. The agent asks guided questions, handles review and reminder modes, and records completed practice history when the skill completes a WOOP session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill silently self-updates during startup. <br>
Mitigation: Remove the auto-update block or require explicit user confirmation before updating the installed skill. <br>
Risk: The skill stores sensitive personal reflection history under ~/.woop-daily by default. <br>
Mitigation: Make logging and history recall explicit opt-in, and provide clear controls for reviewing and deleting stored history. <br>
Risk: The skill can set reminders and run shell commands when reminder mode is requested. <br>
Mitigation: Review generated OpenClaw cron commands before execution and confirm the requested schedule with the user. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/reffwu/woop-daily) <br>
- [Project homepage](https://github.com/ReffWu/woop-daily) <br>
- [Conversation craft reference](references/conversation-craft.md) <br>
- [WOOP / MCII science background](references/science.md) <br>
- [Parable: the boy who built bridges](references/parable-fog-river.md) <br>
- [Skill design principles](references/skill-design-principles.md) <br>
- [Official WOOP practice resource](https://woopmylife.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Conversational Markdown with optional inline shell commands and JSONL or Markdown log entries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or append local WOOP history files and may propose OpenClaw cron reminder commands when the user requests reminders.] <br>

## Skill Version(s): <br>
2.2.0 (source: frontmatter, changelog, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
