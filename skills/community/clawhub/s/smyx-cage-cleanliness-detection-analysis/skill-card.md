## Description: <br>
Analyzes pet cage images or videos to estimate feces or urine coverage, produce a cleanliness score, and flag cages that need cleaning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Pet boarding centers, pet shops, animal hospitals, and breeding facilities use this skill to review fixed-camera cage-floor images or videos, estimate waste coverage, and generate cleaning alerts and reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cage images, videos, report queries, and identity-linked request data may be sent to the LifeEmergence cloud service. <br>
Mitigation: Use the skill only where cloud processing of this media and request data meets privacy, contractual, and compliance requirements. <br>
Risk: The skill can automatically create or reuse an identity and store authentication tokens locally. <br>
Mitigation: Review workspace data-directory placement and restrict access to local token and database files before deployment. <br>
Risk: Cloud history retrieval is identity-linked and offers limited user control. <br>
Mitigation: Limit who can trigger historical report queries and verify that identity-linked report access matches the deployment policy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-cage-cleanliness-detection-analysis) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>
- [API documentation](artifact/references/api_doc.md) <br>
- [SMYX analysis API documentation](artifact/skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or JSON analysis reports with report links and optional local output files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can query cloud-hosted historical reports and can save analysis output when an output path is provided.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
