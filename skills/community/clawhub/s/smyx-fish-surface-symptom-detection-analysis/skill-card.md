## Description: <br>
Analyzes aquarium or underwater fish images and videos to identify visual surface symptoms including white spots, hyperemia, and fin rot, then returns symptom classifications, confidence scores, severity, locations, alert level, and non-medication guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External aquarists, aquarium operators, ornamental fish farms, and developers integrating smart aquarium workflows can use this skill to generate visual fish surface health reports from high-definition images or videos. The skill supports early symptom triage and alerting while directing users to consult qualified aquarium veterinary or professional staff for diagnosis and treatment decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fish images, videos, or supplied media URLs may be sent to an external LifeEmergence service. <br>
Mitigation: Deploy only with explicit user or venue authorization, disclose the external upload path, and require confirmation before sending media or URLs. <br>
Risk: The skill may create or reuse a linked account, retrieve cloud history, and store authentication tokens locally. <br>
Mitigation: Document identity, history retrieval, token storage, retention, and deletion behavior before deployment; require confirmation before history access. <br>
Risk: Visual symptom analysis can produce false positives from reflections, bubbles, substrate particles, or naturally spotted fish species. <br>
Mitigation: Use species baselines, surface false-positive risk flags in reports, and keep professional veterinary review as the authority for diagnosis and treatment. <br>
Risk: The skill could be misused to provide treatment or medication instructions beyond visual triage. <br>
Mitigation: Keep outputs limited to visual symptom classification, confidence, severity, non-medication actions, and disclaimers directing users to qualified aquarium veterinary or professional staff. <br>


## Reference(s): <br>
- [Fish Surface Symptom API Documentation](references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown reports and structured JSON-style analysis fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include symptom type, confidence, location, severity, composite scene, alert level, recommended non-medication actions, history tables, report links, and disclaimers.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
