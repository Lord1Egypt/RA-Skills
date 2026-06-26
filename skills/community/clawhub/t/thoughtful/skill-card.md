## Description: <br>
Your thoughtful companion for WhatsApp - remembers what matters, helps you stay present in your relationships. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[regalstreak](https://clawhub.ai/user/regalstreak) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to turn WhatsApp direct messages and selected groups into relationship-oriented summaries, reply reminders, follow-up cues, and draftable conversation starters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles very sensitive WhatsApp conversation data and stores message-derived files, prompts, task state, and CRM-style contact signals locally. <br>
Mitigation: Use it only with explicit consent and a narrow chat scope, review generated prompts before LLM use, and add clear retention controls for local data. <br>
Risk: Summary prompts may send private conversation content to an LLM. <br>
Mitigation: Limit included chats and contacts, redact sensitive content where possible, and confirm the LLM processing path is acceptable before using it with real private conversations. <br>
Risk: The release evidence warns that Telegram delivery is not scoped clearly enough and includes a hard-coded destination in the artifact behavior. <br>
Mitigation: Change or remove the Telegram destination before use and require the user to confirm every delivery channel and recipient. <br>
Risk: Recurring automation includes an unscoped process-kill step for wacli-readonly. <br>
Mitigation: Replace the process-kill step with scoped process management before enabling scheduled runs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/regalstreak/thoughtful) <br>
- [Publisher profile](https://clawhub.ai/user/regalstreak) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries, JSON tracking files, shell command workflows, and local prompt text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires wacli-readonly and stores message-derived state, CRM signals, and LLM prompt context locally.] <br>

## Skill Version(s): <br>
1.3.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
