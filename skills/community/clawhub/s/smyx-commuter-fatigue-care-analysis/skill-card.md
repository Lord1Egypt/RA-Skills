## Description: <br>
Analyzes fixed living-room camera video, with optional audio, from the first 30 minutes after a user arrives home to estimate after-work fatigue and suggest light smart-home comfort actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External smart-home users and developers use this skill to analyze home-arrival fatigue signals and produce a structured care report with fatigue level, recommended comfort actions, and historical report lookup guidance. It is intended for light wellness support, not medical diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may process private living-room video, optional audio, and personal identifiers through external services. <br>
Mitigation: Use only with informed consent, trusted service operators, and clear expectations for retention, deletion, access control, and account ownership. <br>
Risk: Cloud-accessible analysis history and local bearer-token storage may expose sensitive wellness and home-behavior data. <br>
Mitigation: Review credential handling and history storage before installation, restrict access to the account, and confirm that users can delete stored reports and revoke tokens. <br>
Risk: Fatigue scoring and comfort prompts could be mistaken for clinical assessment or overstep user boundaries. <br>
Mitigation: Present outputs as non-diagnostic wellness signals, keep interventions optional and rate-limited, and preserve pause, silence, and opt-out controls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/smyx-commuter-fatigue-care-analysis) <br>
- [Publisher profile](https://clawhub.ai/user/smyx-sunjinhui) <br>
- [API documentation](references/api_doc.md) <br>
- [Nested API documentation](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and JSON fatigue-care reports with command-line usage examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include fatigue index, fatigue level, posture, face and behavior signals, comfort actions, weekly trend summaries, and links to cloud-hosted historical reports.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
