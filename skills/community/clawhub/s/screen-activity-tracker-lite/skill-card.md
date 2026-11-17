## Description:

Screen Activity Tracker Lite helps an agent start, stop, summarize, and search recurring macOS screen activity tracking by capturing screenshots, analyzing them with a configured vision model, and storing local Markdown logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zeject](https://clawhub.ai/user/zeject)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill on macOS to record screen activity over time, generate brief AI descriptions of screenshots, and later summarize or search the local Markdown history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring full-screen screenshots may capture passwords, confidential work, or private personal information.

Mitigation: Use the skill only in contexts where full-screen recording is acceptable, avoid sensitive workflows while it is active, and confirm the tracking job can be stopped.

Risk: Screenshots are sent to the configured vision-model endpoint, and the provided default endpoint is plaintext HTTP.

Mitigation: Change the model URL to a trusted local or HTTPS endpoint before use and avoid sending regulated or confidential content to untrusted services.

Risk: Recurring capture can continue after initial setup if the scheduled job remains enabled.

Mitigation: Record the scheduler job ID, verify the current schedule, and disable or remove the job when tracking is no longer needed.

Risk: The screenshot dependency is installed from npm without a pinned version in the evidence.

Mitigation: Review and pin the screenshot dependency version according to the deployment environment's software supply-chain policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zeject/skills/screen-activity-tracker-lite)
- [Publisher profile](https://clawhub.ai/user/zeject)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown logs and plain-text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces recurring timestamped activity entries, screenshot references, daily summaries, and keyword search results using the configured local output directory.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
