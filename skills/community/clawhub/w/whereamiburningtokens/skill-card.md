## Description: <br>
Reads only ~/.openclaw/agents/main/sessions/sessions.json to show where OpenClaw tokens and estimated costs are going by session type. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whooshinglander](https://clawhub.ai/user/whooshinglander) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to inspect local session token usage, estimated spend, and category-level anomalies such as high-volume logging or costly scheduled tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local token usage and estimated cost summaries may reveal private workflow or spend details if shared. <br>
Mitigation: Use explicit prompts when invoking the skill and review generated summaries before sharing them. <br>
Risk: Broad token-cost prompts could activate the diagnostic skill unintentionally. <br>
Mitigation: Invoke the skill deliberately for token usage analysis and confirm the requested time window. <br>
Risk: The optional savings log writes a local record when the user explicitly asks to track savings. <br>
Mitigation: Request logging only when a persistent local token-diet record is desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/whooshinglander/whereamiburningtokens) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown table with concise diagnostic insight lines] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports token counts, estimated cost, percentages, and anomaly flags for the selected time window.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
