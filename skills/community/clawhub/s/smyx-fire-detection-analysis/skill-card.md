## Description: <br>
Detects flames and smoke in image or video scenes and returns structured fire-warning analysis for locations such as industrial parks, forests, and warehouses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, operators, and developers use this skill to submit surveillance images, videos, or media URLs for fire and smoke detection, confidence assessment, risk-level reporting, and historical report lookup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted images, videos, media URLs, and report history are handled by the publisher's cloud service. <br>
Mitigation: Use only with media and operational data approved for third-party cloud processing, especially for surveillance footage or regulated environments. <br>
Risk: The skill silently creates or reuses identity, logs into an external service, stores local tokens, and reads workspace identity files. <br>
Mitigation: Review or sandbox the skill before installation and avoid running it in workspaces with sensitive credentials or strict account-control requirements. <br>
Risk: Fire-detection results are advisory and may not be sufficient for emergency response decisions. <br>
Mitigation: Treat outputs as security warning support only and require professional on-site confirmation for suspected fire events. <br>


## Reference(s): <br>
- [Fire Detection API Documentation](artifact/references/api_doc.md) <br>
- [Shared Analysis API Documentation](artifact/skills/smyx_analysis/references/api_doc.md) <br>
- [Skill Demo](https://lifeemergence.com/sample.html) <br>
- [ClawHub Skill Page](https://clawhub.ai/18072937735/skills/smyx-fire-detection-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, files] <br>
**Output Format:** [Markdown text with structured JSON analysis and optional saved output file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include detection results, monitoring findings, recommendations, historical report data, and report links.] <br>

## Skill Version(s): <br>
1.0.11 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
