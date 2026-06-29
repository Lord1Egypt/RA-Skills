## Description: <br>
AI-powered pet eye anomaly detection from close-up facial images or video that flags redness, abnormal tearing, and pupil or cornea opacity for home checks, boarding inspections, veterinary triage, and senior pet cataract monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and pet-care operators use this skill to analyze pet face images or videos for visible eye abnormality alerts, structured results, and report links. It is intended for visual screening support and does not replace professional veterinary diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pet images, videos, or supplied media URLs are sent to lifeemergence.com cloud services for analysis. <br>
Mitigation: Use the skill only with media the user is comfortable sharing with that service, and prefer deployments where retention and deletion practices are documented. <br>
Risk: The skill may create or reuse an internal account identity and store local account or token data. <br>
Mitigation: Review and protect the local data directory, including smyx-common-claw.db and smyx-api-key.txt, before using it with sensitive household media. <br>
Risk: History queries can retrieve account-linked reports with limited user control. <br>
Mitigation: Enable history retrieval only where account-linked report access is expected and appropriate for the user. <br>
Risk: Visual anomaly alerts can be mistaken for a veterinary diagnosis. <br>
Mitigation: Present results as screening support only and direct users to a veterinarian for diagnosis or urgent symptoms. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-eye-anomaly-detection-analysis) <br>
- [API documentation](references/api_doc.md) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, guidance] <br>
**Output Format:** [Markdown text with structured JSON report content and optional saved output file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include report export links and account-linked history results from the cloud API.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence and target metadata; artifact frontmatter says 1.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
