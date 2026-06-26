## Description: <br>
Track revenue across multiple Stripe accounts with automated daily reports, goal tracking, MRR/ARR metrics, and anomaly alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[son-of-poseidon](https://clawhub.ai/user/son-of-poseidon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business operators, founders, finance teams, and agents use this skill to consolidate Stripe charges, refunds, subscriptions, MRR/ARR, goals, and anomaly signals across multiple accounts for daily and period-based revenue reviews. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads a local Stripe secret key and accesses financial data for configured accounts. <br>
Mitigation: Use the most restricted read-only Stripe key available and keep ~/.config/stripe/api_key private with restrictive file permissions. <br>
Risk: Generated reports may contain sensitive revenue and subscription information. <br>
Mitigation: Limit report sharing to authorized recipients and review outputs before storing them in shared notes or systems. <br>
Risk: Automated nightly execution can repeatedly access live Stripe data without a human initiating each run. <br>
Mitigation: Enable the nightly cron only deliberately and review its schedule, target session, and payload before deployment. <br>


## Reference(s): <br>
- [Configuration template](references/config-template.json) <br>
- [ClawHub skill page](https://clawhub.ai/son-of-poseidon/revenue-dashboard) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON, Markdown reports, summary text, shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports may include financial metrics, goal status, anomaly flags, and per-account Stripe details.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
