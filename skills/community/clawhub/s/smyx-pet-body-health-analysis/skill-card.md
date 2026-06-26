## Description: <br>
Analyzes pet images or videos to identify body-condition, skin, injury, and activity-state concerns and return a structured pet health report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to submit pet media for body-condition and health screening, then receive a structured analysis report or a Markdown table of historical reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pet or household media and user identifiers are sent to external services. <br>
Mitigation: Use only with consent, avoid media containing people or sensitive private spaces, and provide the minimum necessary user identifier. <br>
Risk: The security summary flags broad backend access, history lookup, token handling, and media upload with unclear disclosure. <br>
Mitigation: Install only when the publisher is trusted, review configured API endpoints before deployment, restrict credentials, and monitor access to retained analysis history. <br>
Risk: The analysis output may be mistaken for veterinary diagnosis. <br>
Mitigation: Present results as screening guidance only and direct users to consult a veterinarian for abnormal findings or health decisions. <br>


## Reference(s): <br>
- [Pet Health Analysis API Documentation](references/api_doc.md) <br>
- [Common Analysis API Documentation](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON] <br>
**Output Format:** [Markdown reports, Markdown history tables, and structured JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include report links returned by the remote analysis service.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata; artifact frontmatter is 1.0.4) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
