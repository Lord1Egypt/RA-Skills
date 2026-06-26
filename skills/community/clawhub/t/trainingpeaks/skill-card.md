## Description: <br>
Pull real-time training plans, workouts, fitness metrics (CTL/ATL/TSB), and personal records from TrainingPeaks using cookie-based authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rubengarciam](https://clawhub.ai/user/rubengarciam) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Athletes, coaches, and agents use this skill to retrieve TrainingPeaks training plans, workouts, athlete profiles, fitness metrics, and personal records for planning or analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles TrainingPeaks session cookies and cached bearer tokens that may grant access equivalent to the user's web session. <br>
Mitigation: Install only if that access level is acceptable, keep cookies and token files private, and refresh or revoke the TrainingPeaks session if exposure is suspected. <br>
Risk: Credentials may appear in command history, logs, environment variables, or local files if handled carelessly. <br>
Mitigation: Avoid sharing cookies, token files, command history, or logs containing credentials; prefer protected local storage with restrictive file permissions. <br>


## Reference(s): <br>
- [TrainingPeaks web app](https://app.trainingpeaks.com) <br>
- [TrainingPeaks API host](https://tpapi.trainingpeaks.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; CLI output is human-readable text or JSON when requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill may read and write TrainingPeaks credential files under ~/.trainingpeaks/ and use TP_AUTH_COOKIE when provided.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
