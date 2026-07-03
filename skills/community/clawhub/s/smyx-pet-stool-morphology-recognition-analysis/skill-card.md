## Description: <br>
Analyzes dog toilet or outdoor walking-path images and videos through cloud APIs to report stool color, morphology, blood or mucus indicators, abnormal observations, and related history without providing diagnosis or treatment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and pet-care developers use this skill to submit dog stool images, videos, or URLs for structured morphology observations and historical report lookup. The output supports pet health monitoring workflows but should not be used as a veterinary diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pet toilet or walking-path images, videos, and report history are sent to the configured Life Emergence cloud service. <br>
Mitigation: Use only with media and report history that may be shared with that service, and avoid submitting sensitive bystander or location-identifying content when possible. <br>
Risk: The skill can silently reuse or create an internal account identity and store API keys or tokens in local workspace files or SQLite storage. <br>
Mitigation: Review or isolate data/smyx-api-key.txt and the workspace database before use, especially in shared workspaces. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/18072937735/skills/smyx-pet-stool-morphology-recognition-analysis) <br>
- [Skill Demo](https://lifeemergence.com/sample.html) <br>
- [API Documentation](references/api_doc.md) <br>
- [Analysis API Documentation](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and JSON-style structured analysis reports with optional saved output files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include report links and history tables returned by the configured cloud service.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
