## Description: <br>
Monitors fixed doorway or balcony video to count child indoor/outdoor transitions, calculate daily outdoor-activity duration, and return structured alerts and report links when time falls below a preset threshold. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and operators use this skill to analyze household doorway or balcony camera media for child entry/exit events, daily outdoor-time estimates, reminders, and historical reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive child and household video may be uploaded to a remote service for analysis. <br>
Mitigation: Use only with guardian consent, confirm the service operator and retention/deletion policy, and restrict deployment to approved cameras and media sources. <br>
Risk: Identity values, tokens, report history, and report export links may be created or reused during analysis and history queries. <br>
Mitigation: Review token storage and report-access controls before deployment, limit who can run history queries, and verify there is a clear deletion path for reports and identity records. <br>
Risk: URL inputs can cause the remote API service to fetch externally hosted household media. <br>
Mitigation: Disable URL input or enforce an allowlist and size/type validation when the skill is used in managed environments. <br>
Risk: Outdoor-time results are inferred from doorway transition events and may not represent true exercise, outdoor exposure, or medical status. <br>
Mitigation: Present results as estimates for caregiver review, keep medical claims out of user-facing output, and direct health concerns to qualified professionals. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-child-outdoor-activity-monitor-analysis) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>
- [API documentation](references/api_doc.md) <br>
- [Analysis API documentation](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown text containing structured JSON-style analysis results, reminders, history lists, and report links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include remote report export URLs and cloud history records returned by the API.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter says 1.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
