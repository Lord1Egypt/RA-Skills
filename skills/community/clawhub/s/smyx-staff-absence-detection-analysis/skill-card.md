## Description: <br>
Real-time monitoring of personnel on-duty status in specific areas using computer vision and human pose estimation to detect leaving-post and absence events, support configurable thresholds, and return structured monitoring reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operations, safety, and facilities teams use this skill to analyze workplace camera images, videos, or media URLs for personnel absence and leaving-post events. It can also retrieve cloud-hosted historical reports associated with the automatically managed user identity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends workplace images, videos, or media URLs to the vendor's cloud service for analysis. <br>
Mitigation: Use only with media that the organization is authorized to process, and confirm employee notice, consent, retention, and vendor-processing requirements before deployment. <br>
Risk: Reports are tied to an automatically managed identity, and the skill can silently create or reuse that identity. <br>
Mitigation: Review whether silent identity creation and cloud history retrieval meet internal privacy and account-governance policies before enabling historical report queries. <br>
Risk: The security evidence says credentials or tokens may be stored and reused for cloud requests with limited user control. <br>
Mitigation: Run in an isolated agent workspace, restrict access to local skill data files, and rotate or revoke service credentials according to the vendor's process if the workspace is shared or decommissioned. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/18072937735/skills/smyx-staff-absence-detection-analysis) <br>
- [API documentation](artifact/references/api_doc.md) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown report text or structured JSON, with optional saved output files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports may include detection status, absence counts, duration statistics, recommendations, cloud report links, and historical report lists.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
