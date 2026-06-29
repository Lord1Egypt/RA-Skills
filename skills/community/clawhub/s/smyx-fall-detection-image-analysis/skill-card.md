## Description: <br>
Detects fall events in target areas from images or short videos for elder-care and nursing-home monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External caregivers, family members, and care-facility operators use this skill to submit local files or public URLs for fall-detection analysis and to retrieve cloud-hosted historical reports. Results are safety references and should be confirmed by a person before emergency or care decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private home, elder-care, or nursing-facility images and videos may be sent to a third-party cloud service for analysis. <br>
Mitigation: Use the skill only when that cloud data handling is acceptable, the publisher's service is trusted, and the people shown in the media have appropriate authorization or consent. <br>
Risk: The skill may create or reuse local identity state and store remote service tokens. <br>
Mitigation: Run it in a controlled workspace, restrict access to workspace data, and review or remove locally stored identity and token state when the skill is no longer needed. <br>
Risk: Fall-detection output may be incomplete or incorrect and is not a substitute for human confirmation. <br>
Mitigation: Treat reports as safety signals, review the underlying situation directly, and escalate suspected falls through the relevant care or emergency process. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/18072937735/skills/smyx-fall-detection-image-analysis) <br>
- [API Interface Documentation](references/api_doc.md) <br>
- [Analysis API Error Codes](skills/smyx_analysis/references/api_doc.md) <br>
- [Skill Demo](https://lifeemergence.com/sample.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Files] <br>
**Output Format:** [Markdown text with JSON-formatted structured analysis results, historical report lists, and report export links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write result text to an output file; supports image and short-video inputs within the documented size and format limits.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence; artifact frontmatter says 1.0.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
