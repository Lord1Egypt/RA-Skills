## Description: <br>
Analyzes fixed aquarium camera images or video to detect fish gasping, rapid mouth movement, and increased gill-cover motion, then reports visual warning signals for ammonia-poisoning or hypoxia risk. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, aquarium operators, and aquaculture teams use this skill to analyze aquarium or pond camera footage for early visual warning signs of fish gasping, abnormal respiration, and possible hypoxia or ammonia-related water-quality risk. The skill produces structured alerts, suggested non-drug response actions, and report links without presenting a veterinary diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Aquarium media or supplied URLs may be processed by the publisher's cloud service. <br>
Mitigation: Use only footage and URLs appropriate for that third-party service, and avoid private camera feeds or internal URLs unless the publisher and its retention controls are trusted. <br>
Risk: The skill creates or reuses an internal user identity and can query prior cloud reports. <br>
Mitigation: Review account, token, and report-access behavior before installation, and limit deployment to environments where this identity model is acceptable. <br>
Risk: Visual warning results may be mistaken for a definitive fish-health or water-quality diagnosis. <br>
Mitigation: Treat outputs as visual risk warnings only; confirm water quality with tests and consult an aquarium veterinarian or aquaculture technician when severe or repeated alerts occur. <br>
Risk: Poor camera coverage, surface disturbance, or plant occlusion can produce unreliable detections. <br>
Mitigation: Require clear footage covering the water surface and mid-water area, and return an unreliable-signal result when tracking quality is insufficient. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/18072937735/skills/smyx-fish-gasping-ammonia-warning-analysis) <br>
- [Publisher profile](https://clawhub.ai/user/18072937735) <br>
- [API documentation](references/api_doc.md) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown or JSON structured analysis report with alert levels, observed metrics, recommendations, and report links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports local file or URL inputs, optional report export, and cloud history listing.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
