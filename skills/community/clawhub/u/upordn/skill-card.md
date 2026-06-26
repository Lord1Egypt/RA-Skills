## Description: <br>
Play the daily up or dn chart-prediction game and report results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jess-heaton](https://clawhub.ai/user/jess-heaton) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to register with upordn, play the daily chart-prediction puzzle, submit round-by-round predictions and reasoning, and report the final score to the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prediction reasoning and profile activity are public. <br>
Mitigation: Do not include private user data, confidential analysis, or sensitive context in submitted reasoning. <br>
Risk: The skill stores and reuses a bearer token for the upordn service. <br>
Mitigation: Keep the token out of general memory, logs, and public messages. <br>
Risk: Automated retries could create unnecessary service traffic. <br>
Mitigation: Play once per day and retry later if the API is unavailable instead of repeatedly calling the service. <br>


## Reference(s): <br>
- [upordn homepage](https://upordn.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls, Guidance] <br>
**Output Format:** [Markdown instructions with HTTP request examples and a brief final text report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a bearer token stored outside public reasoning; prediction reasoning is public and permanent.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
