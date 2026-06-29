## Description: <br>
Analyzes home-entry or kindergarten drop-off video to identify crying expressions, clinging actions, resistance behaviors, and a mild, moderate, or severe separation-anxiety level for caregiver and teacher review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Parents, teachers, school operators, and agent users can use this skill to submit fixed-camera drop-off videos or URLs for structured visual behavior analysis and friendly follow-up suggestions. It supports current analysis and cloud history lookup, but its outputs should be treated as behavioral observations rather than clinical diagnosis or treatment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes video of minors and caregivers, which is highly sensitive personal data. <br>
Mitigation: Use only with explicit guardian consent, school approval when applicable, and a clear data-handling plan for retention, deletion, access control, and report export. <br>
Risk: The skill sends video files or URLs to the provider's cloud service for analysis and cloud report retrieval. <br>
Mitigation: Review the provider's cloud processing, retention, and deletion policies before deployment, and avoid submitting footage that is not necessary for the stated purpose. <br>
Risk: The skill silently creates or reuses a cloud-linked identity and stores account tokens for report history access. <br>
Mitigation: Deploy only in environments where automatic identity management and local token storage are acceptable, and restrict local workspace access accordingly. <br>
Risk: Behavior classifications may be wrong in cases such as play crying, environmental irritation, occlusion, or multiple children in view. <br>
Mitigation: Treat output as visual behavior support for human review, not a diagnosis, and confirm moderate or severe cases with caregivers, teachers, or qualified professionals. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/18072937735/skills/smyx-child-separation-anxiety-detection-analysis) <br>
- [Publisher Profile](https://clawhub.ai/user/18072937735) <br>
- [API Interface Documentation](references/api_doc.md) <br>
- [Shared Analysis API Documentation](skills/smyx_analysis/references/api_doc.md) <br>
- [Skill Demo](https://lifeemergence.com/sample.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or JSON analysis report with behavior metrics, anxiety-level classification, recommendations, report links, and optional saved output file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts local video files or public video URLs; history queries return cloud report lists as Markdown tables.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence; SKILL.md frontmatter lists 1.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
