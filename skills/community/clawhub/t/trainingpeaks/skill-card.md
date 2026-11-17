## Description:

Pulls real-time training plans, workouts, fitness metrics (CTL/ATL/TSB), and personal records from TrainingPeaks using cookie-based authentication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rubengarciam](https://clawhub.ai/user/rubengarciam)

### License/Terms of Use:


## Use Case:

External athletes, coaches, and developers use this skill to let an agent retrieve TrainingPeaks profile, workout, fitness, and personal-record data for training analysis and planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to handle and persist a live TrainingPeaks browser session cookie.

Mitigation: Treat the Production_tpAuth cookie like a password; keep it out of shared chats, logs, screenshots, shell history, and CI output.

Risk: The skill can access TrainingPeaks account data after authentication.

Mitigation: Install only if you are comfortable granting access to that account data, and remove ~/.trainingpeaks credentials when the skill is no longer needed.

## Reference(s):

- [TrainingPeaks ClawHub skill page](https://clawhub.ai/rubengarciam/skills/trainingpeaks)
- [TrainingPeaks application](https://app.trainingpeaks.com)
- [TrainingPeaks API endpoint](https://tpapi.trainingpeaks.com)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Human-readable CLI text with optional raw JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a TrainingPeaks session cookie and local credential cache under ~/.trainingpeaks.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
