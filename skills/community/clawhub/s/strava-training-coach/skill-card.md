## Description: <br>
AI running coach that monitors Strava training load for dangerous mileage spikes, intensity imbalances, and recovery gaps, then sends Discord or Slack alerts before potential injuries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hhq0421](https://clawhub.ai/user/hhq0421) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Runners and coaches use this skill to check Strava activity history for training-load spikes, intensity imbalance, recovery gaps, and weekly trend summaries. It also helps set up recurring checks that send concise alerts to Discord or Slack. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Strava read/activity access and stores access tokens locally. <br>
Mitigation: Grant only the needed Strava scope, keep the local config directory private, and revoke or delete tokens when you stop using the skill. <br>
Risk: Training summaries and alerts may be sent to a Discord or Slack channel through a webhook. <br>
Mitigation: Use a private channel, keep webhook URLs secret, and rotate or revoke webhooks if they are exposed. <br>
Risk: Optional Oura integration can include sleep and readiness signals in coaching alerts. <br>
Mitigation: Enable Oura only when you intend to share those signals with the skill and your selected notification channel. <br>
Risk: Automated scheduled checks can continue sending alerts after the user no longer wants monitoring. <br>
Mitigation: Disable any cron or scheduler entry when monitoring is no longer needed. <br>
Risk: Training recommendations may not account for personal medical history, acute injury, or clinical advice. <br>
Mitigation: Treat alerts as informational coaching prompts and defer to qualified medical or coaching guidance for pain, illness, or injury decisions. <br>


## Reference(s): <br>
- [Evidence-Based Training Principles for Injury-Free Running](references/training-principles.md) <br>
- [Strava API Reference](https://developers.strava.com/docs/reference/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, plus text alerts and summary reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Strava credentials and a Discord or Slack webhook; Oura sleep/readiness signals are optional.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
