## Description: <br>
AI-powered pest and disease detection for rose images or videos that identifies common issues such as black spot, powdery mildew, spider mites, and aphids, then returns severity and general control suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External gardeners, growers, and agents use this skill to analyze rose leaf, shoot, bud, image, or video inputs for common pests and diseases, severity, affected plant areas, and general care recommendations. It also supports retrieving cloud-hosted historical analysis reports for the provided open-id. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Rose photos, videos, image URLs, and the supplied open-id are sent to the publisher's cloud service for analysis and history retrieval. <br>
Mitigation: Use a non-sensitive open-id where possible and submit only media or URLs that are appropriate for remote processing. <br>
Risk: Service tokens may be cached locally in the workspace data directory and associated with the user-provided identifier. <br>
Mitigation: Use an isolated workspace for sensitive runs and clear cached credentials or tokens after use when they are no longer needed. <br>
Risk: The analysis provides visual garden-care guidance and may not be sufficient for severe or large-scale plant health decisions. <br>
Mitigation: Treat results as advisory and consult local plant-protection or agricultural experts for severe outbreaks or high-impact production decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/18072937735/smyx-rose-pest-disease-detection-analysis) <br>
- [API Interface Documentation](references/api_doc.md) <br>
- [SMYX Analysis API Documentation](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and structured JSON text, with optional saved output file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an open-id; accepts local image or video files and public media URLs; history queries return report records with links when available.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter says 1.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
