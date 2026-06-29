## Description: <br>
Summarize Telegram channel messages by topic with structured output. Used by executor sub-agents spawned by telegram-parser. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sergeykolbasuk](https://clawhub.ai/user/sergeykolbasuk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators using a Telegram parsing workflow can use this skill to have executor agents turn channel message batches into concise, topic-grouped Russian summaries with structured handling for job postings and technical news. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Telegram credentials or message batches may expose channel content outside the intended scope. <br>
Mitigation: Before installing or running the workflow, confirm that only the intended channels and date ranges are available to the agent. <br>
Risk: Summaries may omit or condense details from Telegram posts. <br>
Mitigation: Use the generated digest for triage and review the original message batch when exact wording, links, or full context matter. <br>


## Reference(s): <br>
- [Telegram Summary on ClawHub](https://clawhub.ai/sergeykolbasuk/telegram-summary) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown-style structured summary text in Russian] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Summaries are grouped by topic, capped at about five topics per digest, and omit post links unless explicitly requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
