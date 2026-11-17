## Description:

AI running coach that monitors Strava training load, detects mileage spikes, intensity imbalances, and recovery gaps, and sends evidence-based alerts to Discord or Slack.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hhq0421](https://clawhub.ai/user/hhq0421)

### License/Terms of Use:


## Use Case:

External runners and training-focused developers use this skill to connect Strava activity data, run daily training-load checks, and generate weekly reports with alerts for workload spikes, intensity balance, and recovery gaps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Strava OAuth tokens and fitness activity data, with server evidence noting credential-scope and OAuth hardening weaknesses.

Mitigation: Review token-file handling, OAuth state handling, and local storage permissions before installing; grant only the required Strava read scopes.

Risk: The skill can send derived training and possible health-related alerts to Discord or Slack webhooks.

Mitigation: Use private notification channels, protect webhook URLs as secrets, and avoid sending reports to shared workspaces unless recipients are intended.

Risk: Training-load, injury-risk, recovery, and readiness recommendations are coaching information rather than medical advice.

Mitigation: Treat alerts as general guidance and consult qualified medical or coaching professionals for pain, injury, or health decisions.

Risk: Optional Oura integration can add sleep and readiness data to the skill's analysis.

Mitigation: Enable Oura access only when needed and review local CLI token access before use.

## Reference(s):

- [Strava API Reference](https://developers.strava.com/docs/reference/)
- [Evidence-Based Training Principles](artifact/references/training-principles.md)
- [ClawHub Skill Page](https://clawhub.ai/hhq0421/skills/strava-training-coach)
- [ClawHub Publisher Profile](https://clawhub.ai/user/hhq0421)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, notification text, and report summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May send derived training and health-adjacent alerts to Discord or Slack.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
