## Description: <br>
This skill classifies likely causes of infant crying from audio or audio-video input and returns structured results with confidence, suggested soothing hints, and report links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External parents, caregivers, daycare staff, and developers integrating smart baby-monitor workflows use this skill to submit infant cry audio or audio-video and receive a non-diagnostic classification of likely cause, confidence, and guidance hints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive infant audio, video, or media URLs may be sent to the provider's cloud service. <br>
Mitigation: Use the skill only with appropriate guardian consent and after confirming provider handling, retention, and deletion practices for child-monitoring data. <br>
Risk: The skill may create or reuse a local account identity and store tokens with limited user control. <br>
Mitigation: Review the workspace data directory before use, run the skill in an isolated workspace when possible, and remove or rotate stored identity data when access is no longer needed. <br>
Risk: Historical report lookup can expose cloud-stored analysis records and report links. <br>
Mitigation: Limit access to workspaces where the skill runs and confirm that report deletion or history controls meet the deployment's privacy requirements. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-infant-cry-cause-classification-analysis) <br>
- [Infant cry cause classification API documentation](references/api_doc.md) <br>
- [Analysis API documentation](skills/smyx_analysis/references/api_doc.md) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [Markdown and JSON text with report links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include cloud report export links and historical report lists.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter lists 1.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
