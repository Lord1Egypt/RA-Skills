## Description: <br>
Generates a scheduled personalized morning market brief with index moves, hot sectors, portfolio diagnostics, macro and overseas market context, calendar items, and suggested actions, then sends it to Feishu. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[horizoncove](https://clawhub.ai/user/horizoncove) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Investors or operators who use Feishu for daily market monitoring can use this skill to compile a personalized trading-day brief from market data, web search, hot-sector notes, and USER.md portfolio data before the market opens. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can include portfolio data in scheduled Feishu messages. <br>
Mitigation: Use it only with an intended Feishu recipient, configure the recipient explicitly, and add opt-in plus preview or confirmation before outbound sends. <br>
Risk: The artifact includes a hard-coded Feishu recipient target. <br>
Mitigation: Replace hard-coded delivery targets with user-controlled configuration before deployment. <br>
Risk: Trading suggestions and market summaries may be incomplete, stale, or unsuitable for a user's circumstances. <br>
Mitigation: Treat the brief as informational, verify material facts against authoritative market sources, and avoid relying on it as financial advice. <br>


## Reference(s): <br>
- [Custom Morning Brief on ClawHub](https://clawhub.ai/horizoncove/yuheng-morning-brief) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown morning brief sent as a Feishu message] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes market data, portfolio diagnostics, news summaries, calendar items, and suggested actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
