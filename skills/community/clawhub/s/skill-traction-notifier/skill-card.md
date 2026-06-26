## Description: <br>
Monitors ClawHub for skills gaining traction by tracking downloads and stars, alerting when growth or popularity thresholds are exceeded. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Gabriel-Kaufman](https://clawhub.ai/user/Gabriel-Kaufman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to monitor ClawHub skill traction, review top movers, and surface surge alerts from CLI output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional scheduled execution can create repeated ClawHub API requests and persistent local logs. <br>
Mitigation: Review the cron schedule before enabling automation and keep the default scheduled random delay when running from a scheduler. <br>
Risk: Optional profile data is stored locally on disk. <br>
Mitigation: Avoid putting sensitive details in the local profile and use the documented environment variables to control storage paths when needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Gabriel-Kaufman/skill-traction-notifier) <br>
- [ClawHub skills catalog](https://clawhub.ai/skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text CLI output and Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Node.js; fetches public ClawHub skill statistics; stores optional local state, configuration, and profile data on disk.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
