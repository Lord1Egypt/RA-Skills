## Description: <br>
Tracks input and output token usage across conversation turns, summarizes cumulative usage and estimated cost, and warns when configured budgets are approached or exceeded. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xhmqq616](https://clawhub.ai/user/xhmqq616) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to track token consumption, estimate Claude API costs, review usage history, and apply simple token budgets during agent conversations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may keep local usage totals and history in .usage-tracker.json. <br>
Mitigation: Configure the storage path deliberately and avoid recording prompts or usage metadata in shared or sensitive directories. <br>
Risk: Token and cost estimates are approximate and based on the pricing table embedded in the artifact. <br>
Mitigation: Use the estimates for budget awareness and confirm billing-critical numbers against the provider's current usage and pricing records. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xhmqq616/token-usage-tracker) <br>
- [Publisher profile](https://clawhub.ai/user/xhmqq616) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript examples and optional CLI text or JSON output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May maintain local token usage totals and history in .usage-tracker.json unless configured otherwise.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
