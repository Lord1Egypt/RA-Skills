## Description: <br>
This skill analyzes infant cry audio or audio-bearing video to classify likely causes such as hunger, sleepiness, pain or discomfort, need for attention, fear, colic, or unknown, and returns confidence, observations, suggestions, and report links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External caregivers, childcare teams, and developers use this skill to submit infant cry audio, audio-bearing video, or URLs for remote analysis, receive a structured non-diagnostic classification with confidence and soothing guidance, and retrieve prior cloud reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Infant audio, video, or URLs may be sent to the configured external analysis service. <br>
Mitigation: Use only recordings where the guardian understands and accepts remote processing and retention implications. <br>
Risk: The skill creates or reuses a local identity and stores service tokens in a workspace SQLite database. <br>
Mitigation: Review local storage and token handling before deployment, isolate the workspace, and remove or rotate tokens after testing. <br>
Risk: Cloud history queries may expose prior analysis reports associated with the resolved local identity. <br>
Mitigation: Restrict history access to authorized users and review report-list behavior before enabling it in shared environments. <br>


## Reference(s): <br>
- [Infant Cry Cause Classification API Documentation](references/api_doc.md) <br>
- [SMYX Analysis API Documentation](skills/smyx_analysis/references/api_doc.md) <br>
- [Skill Demo](https://lifeemergence.com/sample.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Markdown text with structured JSON-like analysis results, confidence values, suggestions, and report links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save results to a requested output file and can list cloud-stored report history for the resolved local identity.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
