## Description: <br>
Choose which Claude model responds to your Telegram chats. Pick Opus for depth, Sonnet for balance, or Haiku for speed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[josephtandle](https://clawhub.ai/user/josephtandle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Telegram chatbot operators and users use this skill to check and change which Claude model handles Telegram chat responses, choosing Opus, Sonnet, or Haiku based on quality and speed needs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Changing the active model can affect response quality, latency, and cost in the host environment. <br>
Mitigation: Use the status command to confirm the active model and choose Opus, Sonnet, or Haiku according to task needs and host cost policy. <br>
Risk: Model changes may apply only after a brief restart. <br>
Mitigation: Allow the routing service to restart before relying on the newly selected model. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/josephtandle/tg-model-switcher) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance, configuration] <br>
**Output Format:** [Markdown with Telegram slash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No executable code; commands report or change the active Claude model routing for Telegram chats.] <br>

## Skill Version(s): <br>
1.1.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
