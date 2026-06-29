## Description: <br>
Identifies bird species in images or videos, covering more than 500 common species and producing structured recognition results with confidence information and report links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Ecological observers, birdwatchers, conservation teams, and agents assisting them use this skill to identify bird species from uploaded images, videos, or public media URLs. The skill can also retrieve prior cloud-hosted bird recognition reports for the resolved user identity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Uploaded images and videos are sent to the Life Emergence cloud service for analysis. <br>
Mitigation: Use only media that is appropriate for cloud processing and avoid sensitive personal media unless the user accepts the service handling described in the security evidence. <br>
Risk: The skill silently creates or reuses a local identity and stores service tokens in workspace data. <br>
Mitigation: Review the skill before installation, restrict workspace access where possible, and clear local identity or token data when the skill is no longer needed. <br>


## Reference(s): <br>
- [Bird Recognition API Documentation](references/api_doc.md) <br>
- [Common AI Analysis API Documentation](skills/smyx_analysis/references/api_doc.md) <br>
- [Skill Demo](https://lifeemergence.com/sample.html) <br>
- [ClawHub Skill Page](https://clawhub.ai/18072937735/skills/smyx-bird-recognition-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Markdown or JSON report text, including recognition results, confidence details, recommendations, and report links when available] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can save results to a requested output file and can list historical cloud reports associated with the internally resolved identity.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
