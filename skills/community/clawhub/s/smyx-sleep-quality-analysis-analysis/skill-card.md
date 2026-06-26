## Description: <br>
AI-powered pet sleep quality analysis from a fixed bed or rest-area camera that sends videos to a remote service to estimate sleep and awake states, total sleep duration, roll-over or position-change counts, startle awakenings, and a 0-100 sleep-quality score. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External pet owners, animal-care staff, and developers use this skill to analyze fixed-camera pet sleep videos or video URLs, retrieve structured sleep-quality metrics, and list prior cloud-hosted reports. The outputs are sleep-health indicators only and are not medical diagnoses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send pet monitoring videos and user identifiers to remote Life Emergence services. <br>
Mitigation: Review privacy terms before use, avoid videos containing people or private spaces, and use a non-phone identifier if the service allows it. <br>
Risk: The skill can create or log in accounts and store account tokens or profile data locally. <br>
Mitigation: Use a dedicated service account or identifier where possible, restrict local file access, and clear stored tokens/profile data when the skill is no longer needed. <br>
Risk: Sleep-quality outputs may suggest possible pain, anxiety, or disease but are not medical diagnoses. <br>
Mitigation: Treat outputs as visual sleep indicators and consult a veterinarian for persistent or severe abnormalities. <br>


## Reference(s): <br>
- [Pet Sleep Quality Analysis API Documentation](references/api_doc.md) <br>
- [ClawHub Skill Listing](https://clawhub.ai/18072937735/smyx-sleep-quality-analysis-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries, Markdown report tables, JSON API responses, and shell command invocations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write analysis results to a local output file when requested; requires an open-id and can send pet monitoring videos and user identifiers to a remote service.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
