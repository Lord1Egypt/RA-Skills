## Description: <br>
Detects flames and smoke in image or video inputs and returns structured warning-oriented analysis for monitored industrial, forest, warehouse, and similar sites. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security operators and developers use this skill to submit monitored images or videos for fire and smoke detection, review structured risk findings, and query prior detection reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Images, videos, and report queries are sent to the lifeemergence cloud service. <br>
Mitigation: Avoid sensitive media unless that backend and data flow are acceptable for the deployment. <br>
Risk: The skill can create or reuse a local identity and store authentication tokens. <br>
Mitigation: Use an isolated workspace and review or remove any workspace smyx-api-key.txt before use. <br>
Risk: Fire and smoke detection output is warning-oriented and may be incomplete or incorrect. <br>
Mitigation: Use results as an alerting aid and require professional confirmation and emergency response procedures for suspected fire events. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/18072937735/skills/smyx-fire-detection-analysis) <br>
- [Skill Demo](https://lifeemergence.com/sample.html) <br>
- [Fire Detection API Documentation](references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or JSON analysis output with report links and optional saved result files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports local file paths, public media URLs, historical report queries, and basic, standard, or JSON detail levels.] <br>

## Skill Version(s): <br>
1.0.12 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
