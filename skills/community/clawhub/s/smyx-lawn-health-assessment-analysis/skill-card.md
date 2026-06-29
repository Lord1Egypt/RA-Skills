## Description: <br>
Analyzes top-down lawn images, videos, or URLs to estimate yellowing, weed coverage, bare soil, and a composite lawn health score, with structured results and report links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Groundskeepers, facility managers, municipal greenway teams, and developers use this skill to assess turf condition from top-down drone, fixed-camera, or phone imagery. It returns visual metrics, a health score, maintenance-oriented guidance, and cloud report history when requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted media or URLs are sent to a cloud service for analysis. <br>
Mitigation: Use only non-sensitive public or approved lawn imagery, and avoid private or internal URLs unless the publisher documents retention and cleanup controls. <br>
Risk: Reports are associated with an automatically created or reused internal identity. <br>
Mitigation: Run the skill in an isolated workspace or account when handling sensitive projects, and review the publisher's account-handling practices before production use. <br>
Risk: Account tokens may be stored in a local SQLite database. <br>
Mitigation: Restrict workspace access and remove or rotate stored credentials before sharing, archiving, or decommissioning the workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-lawn-health-assessment-analysis) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>
- [API documentation](artifact/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown and JSON with structured report content, maintenance guidance, and report links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May upload submitted files or URLs to a cloud analysis service and may save output to a user-specified file.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence; artifact/SKILL.md frontmatter says 1.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
