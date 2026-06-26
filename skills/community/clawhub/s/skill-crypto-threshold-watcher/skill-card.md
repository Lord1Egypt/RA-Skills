## Description: <br>
Monitors crypto tokens against configurable price and volume thresholds and fires custom alerts when watched entry conditions are met. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Zero2Ai-hub](https://clawhub.ai/user/Zero2Ai-hub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to configure crypto watchlists and receive proactive alerts when selected tokens cross price, volume, or RSI thresholds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Telegram alerts may expose watchlist or trading strategy details to a third-party messaging service. <br>
Mitigation: Verify Telegram bot and chat settings, keep alert content non-sensitive, and include private strategy notes only when that disclosure is acceptable. <br>
Risk: Automated cron checks can repeatedly run the referenced threshold watcher without additional prompts. <br>
Mitigation: Confirm the hourly cron entry is intended and inspect or provide the referenced threshold-watcher.js script before installing the scheduled task. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Zero2Ai-hub/skill-crypto-threshold-watcher) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes watchlist configuration, threshold-check commands, alert examples, and trading pipeline integration guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
