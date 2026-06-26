## Description: <br>
Helps users negotiate on Xianyu by analyzing listing prices, drafting seller messages, and, with explicit user approval, monitoring replies and sending follow-ups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Robertren](https://clawhub.ai/user/Robertren) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External marketplace buyers use this skill to evaluate second-hand Xianyu listings, prepare bargaining messages, manage multi-round negotiation, and optionally monitor seller replies after explicit consent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a logged-in Xianyu session and store local bargaining state. <br>
Mitigation: Install only when the user is comfortable granting the agent access to that session and keeping local bargain-state files. <br>
Risk: Cron monitoring and auto-follow-up can continue marketplace interactions after the initial request. <br>
Mitigation: Keep monitoring and follow-up behavior disabled unless the user intentionally enables them for a specific item or batch. <br>
Risk: Auto-accept or seller-facing replies could commit the user to a purchase decision. <br>
Mitigation: Require user review before any message that accepts a seller price, commits to buy, or materially changes the negotiation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Robertren/xianyu-bargain) <br>
- [Auto Bargain Guide](artifact/guides/auto-bargain.md) <br>
- [Batch Processing Guide](artifact/guides/batch-processing.md) <br>
- [LLM Analyzer Guide](artifact/guides/llm-analyzer.md) <br>
- [Xianyu Browser Guide](artifact/guides/xianyu-browser.md) <br>
- [Bargain Configuration Guide](artifact/references/config.md) <br>
- [Market Price References](artifact/references/market-prices.md) <br>
- [Advanced Bargaining Strategies](artifact/references/advanced-strategies.md) <br>
- [Message Template Library](artifact/references/message-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline JSON, JavaScript-style tool calls, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include price assessments, proposed seller messages, monitoring plans, and local bargain-state configuration; user confirmation is required before seller-facing messages or monitoring.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
