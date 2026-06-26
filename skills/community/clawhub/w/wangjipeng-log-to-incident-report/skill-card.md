## Description: <br>
Converts user-provided error logs into structured incident reports with root cause, impact, mitigation steps, action items, and confidence notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangjipeng977](https://clawhub.ai/user/wangjipeng977) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, site reliability engineers, and support teams use this skill to turn pasted error logs, stack traces, or system output into incident reports that summarize the timeline, likely root cause, impact, mitigation steps, and follow-up actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided logs may contain API keys, tokens, cookies, session IDs, private hostnames, personal data, or regulated information. <br>
Mitigation: Redact sensitive data before pasting logs into the agent context. <br>
Risk: The README includes API_KEY and write-mode examples that are not explained by the skill behavior. <br>
Mitigation: Treat those examples as template residue unless the publisher clarifies what service is used and whether any files are created or modified. <br>
Risk: Root cause and impact can be incomplete when the provided logs do not cover the full incident window. <br>
Mitigation: Review the report's confidence notes and supply additional logs or operational context before acting on conclusions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangjipeng977/wangjipeng-log-to-incident-report) <br>
- [Skill metadata source](https://github.com/MiniMax-AI/skills) <br>
- [Reference index](references/index.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, analysis, guidance] <br>
**Output Format:** [Markdown incident report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [States assumptions and uncertainty when the logs are incomplete or the impact cannot be determined.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
