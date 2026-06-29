## Description: <br>
Assesses ornamental fish color brightness from camera images or videos by extracting HSV saturation and brightness, comparing them with species-specific baselines, and returning a vibrancy score and husbandry guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Aquarium keepers, public aquarium teams, and ornamental fish farms use this skill to evaluate fish color vibrancy from fixed-camera, smart-aquarium, or side-shot media. It returns color metrics, a 0-100 vibrancy score, trend context, and non-diagnostic management suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fish images or videos may be sent to the LifeEmergence cloud service for analysis. <br>
Mitigation: Install only where cloud processing of the media is acceptable, and avoid sending sensitive aquarium, facility, or bystander imagery. <br>
Risk: The skill can create or reuse a local account record and tokens. <br>
Mitigation: Review token storage and retention before deployment, and run the skill in an isolated workspace when possible. <br>
Risk: Cloud history can be queried automatically for matching history requests. <br>
Mitigation: Require deployment policy or user confirmation for history lookups when prior reports may contain sensitive operational details. <br>
Risk: Broad local-file and remote-URL media inputs can send unexpected content to the service. <br>
Mitigation: Use trusted files and URLs, and prefer versions that restrict remote media URLs to trusted sources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-fish-color-brightness-assessment-analysis) <br>
- [API interface documentation](references/api_doc.md) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [Structured JSON or Markdown report with HSV values, vibrancy score, trend fields, recommended actions, and report links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can save analysis output to a file and can return cloud-backed historical report lists when requested.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
