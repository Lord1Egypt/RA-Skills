## Description: <br>
Forecasts a stock's close at option expiration from LSE options-flow data and recommends ranked options strategies with confidence bands, probability of profit, and reward-to-risk. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nathanpua](https://clawhub.ai/user/nathanpua) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run an options forecast for a ticker and expiration, inspect market-implied close ranges, and generate ranked strategy ideas for further review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an LSE API key and contacts LSE market-data services. <br>
Mitigation: Install only when that data access is acceptable, store the API key outside prompts and shared logs, and review generated outputs before use. <br>
Risk: Generated options plays and probabilities are research outputs, not financial advice or account-changing actions. <br>
Mitigation: Verify prices independently, review assumptions before trading decisions, and treat the ranked plays as inputs to human analysis. <br>
Risk: The release uses unpinned Python dependency ranges. <br>
Mitigation: Pin and review dependencies before deploying the skill in sensitive or production environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nathanpua/skills/run-options-forecast) <br>
- [London Strategic Edge](https://londonstrategicedge.com) <br>
- [LSE Vault API endpoint](https://api.londonstrategicedge.com/vault) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Text report with optional JSON file output and HTML dashboard artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a ticker and optional expiration date; may contact LSE market-data services using an LSE API key.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
