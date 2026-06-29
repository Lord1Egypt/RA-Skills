## Description: <br>
Quantifies plant wilting severity from full-plant images or videos, using visual indicators such as leaf droop, stem straightness, and leaf turgidity with optional soil-moisture context to distinguish likely underwatering from overwatering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, growers, and smart-gardening developers use this skill to analyze plant media, estimate wilting severity, review likely water-stress causes, and retrieve prior cloud-generated reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Plant images, videos, submitted URLs, and report history are sent to Life Emergence cloud APIs for analysis and history lookup. <br>
Mitigation: Use only media appropriate for cloud processing, confirm user consent for uploads, and avoid sensitive or private plant-location media unless the deployment has approved the service. <br>
Risk: The skill automatically creates or reuses a persistent local identity and stores related session material locally. <br>
Mitigation: Review and clear the local smyx-common-claw.db and smyx-api-key.txt data before handling sensitive workflows or switching users. <br>
Risk: Water-stress cause classification can be uncertain when soil-moisture data or clear side-view imagery is unavailable. <br>
Mitigation: Treat watering or drainage guidance as advisory, and confirm soil condition and plant context before taking irreversible plant-care action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-plant-wilting-quantification-analysis) <br>
- [Skill usage demo](https://lifeemergence.com/sample.html) <br>
- [Plant wilting API documentation](references/api_doc.md) <br>
- [SMYX analysis API documentation](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown and JSON-formatted structured analysis reports, including report links when returned by the service.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports local media paths or submitted URLs and can write report output to a user-specified file.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata; artifact frontmatter lists 1.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
