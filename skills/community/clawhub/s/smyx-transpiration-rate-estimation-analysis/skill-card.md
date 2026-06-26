## Description: <br>
Estimates a relative indoor-plant transpiration rate index from thermal leaf imagery, or RGB imagery with environmental context, and returns water-stress and root-activity assessment guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to submit indoor plant leaf media or media URLs to a vendor analysis service for a relative transpiration-rate estimate, root water-uptake vitality assessment, stress hints, care suggestions, and report links or history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uploads plant media or media URLs to a vendor service. <br>
Mitigation: Use it only with media and URLs that are acceptable to share with the vendor service; avoid private videos, sensitive local files, and internal URLs. <br>
Risk: The skill can silently create or reuse a cloud identity and query cloud-stored report history. <br>
Mitigation: Install only when that account and history behavior is acceptable for the user and workspace. <br>
Risk: Authentication tokens may be stored in a local SQLite database. <br>
Mitigation: Avoid shared workspaces for sensitive use and review or remove the local skill data store when the skill is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-transpiration-rate-estimation-analysis) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>
- [API documentation](references/api_doc.md) <br>
- [Analysis API documentation](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown and JSON-formatted structured analysis text, with optional report links and history tables.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts local plant media paths or public media URLs; history mode returns cloud report records associated with the resolved identity.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter says 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
