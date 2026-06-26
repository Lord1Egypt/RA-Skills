## Description: <br>
Analyzes fixed-camera video of solo-living elders to count dazing, sighing, and self-talking behaviors, compare patterns with a personal baseline, and produce low, medium, or high emotional-risk reminders for caregivers or community workers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External caregivers, family members, community workers, and developers use this skill to process authorized elder-care camera video or report history and receive behavior-based emotional-risk summaries. It is intended for supportive monitoring and reminders, not medical diagnosis, mental-health screening scores, or treatment recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive in-home elder video and mental-health-adjacent reports may expose private personal data. <br>
Mitigation: Require explicit consent from the monitored person, use only authorized first-party video, and confirm encryption, retention, deletion, and access controls before deployment. <br>
Risk: Cloud service access, exported report links, and token handling are not fully bounded in the evidence. <br>
Mitigation: Verify the service operator and review how uploaded videos, tokens, report history, and exported links are stored, shared, revoked, and deleted. <br>
Risk: The skill requests an open-id and the security guidance warns against phone numbers as identifiers. <br>
Mitigation: Use a non-sensitive opaque identifier instead of a phone number or other directly identifying value wherever possible. <br>
Risk: The evidence flags an unresolved yaml dependency. <br>
Mitigation: Replace it with the intended maintained package and review dependency provenance before installation. <br>
Risk: Behavior-based emotional-risk output could be mistaken for a medical diagnosis. <br>
Mitigation: Present results only as behavior statistics and supportive reminders, and route diagnosis, screening scores, or treatment decisions to qualified professionals. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/smyx-elderly-loneliness-depression-analysis) <br>
- [API interface documentation](references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and JSON-formatted analysis reports, with optional Markdown tables for historical report lists.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include behavior counts, durations, baseline comparison, risk level, alert type, recommended action, and exported report links.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
