## Description: <br>
Analyzes pet food-bowl videos from local files or network URLs to estimate feeding start and end times, eating speed, threshold status, and slow-feed intervention recommendations without providing disease diagnosis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to analyze pet feeding videos, generate structured eating-speed observations, and surface slow-feed intervention recommendations for smart feeder or pet health management workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pet videos or video URLs are sent to the provider's server for analysis. <br>
Mitigation: Use only videos appropriate for server-side processing by this third-party provider, and avoid submitting sensitive footage unless that data sharing is acceptable. <br>
Risk: The skill can automatically create or reuse an internal identity and use it to retrieve historical reports. <br>
Mitigation: Review identity expectations before installation, and clear local workspace token state when separating users or sessions matters. <br>
Risk: Authentication tokens may be stored locally under workspace data state. <br>
Mitigation: Review or clear data/smyx-api-key.txt and related workspace token database state during uninstall, handoff, or account separation. <br>
Risk: Eating-speed thresholds and intervention recommendations are health references, not diagnosis or treatment. <br>
Mitigation: Use outputs as behavioral observations and device-intervention guidance, and consult a veterinarian for medical concerns. <br>


## Reference(s): <br>
- [API Interface Documentation](references/api_doc.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/18072937735/skills/smyx-pet-eating-speed-slow-feed-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, json, shell commands, guidance] <br>
**Output Format:** [Markdown or JSON structured feeding analysis, with optional report links for historical results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include feeding timestamps, total duration, eating speed, threshold/risk status, intervention recommendations, and historical report links.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter reports 1.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
