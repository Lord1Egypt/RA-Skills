## Description: <br>
Detects wet clothing and abnormal excretion in care images or videos, then returns structured alert reports, caregiver guidance, and report links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External caregivers and care teams use this skill to analyze nursing home, home-care, bedside-care, or infant-care images and videos for advisory incontinence status alerts. It can also retrieve cloud-hosted historical reports for follow-up review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Care images, videos, URLs, identity values, and report metadata may be sent to lifeemergence.com/open.lifeemergence.com services. <br>
Mitigation: Use with real patients or infants only after confirming consent, retention terms, access controls, and authorized report retrieval. <br>
Risk: The skill may create or reuse a local identity and store service tokens in the workspace data directory. <br>
Mitigation: Review local workspace data storage before deployment, restrict access to the workspace, and remove or rotate stored tokens when access changes. <br>
Risk: Generated reports are advisory and may affect care timing if treated as a definitive diagnosis. <br>
Mitigation: Require caregiver review and timely human confirmation before making clinical or hygiene-care decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-incontinence-alert-analysis) <br>
- [Incontinence alert analysis API documentation](references/api_doc.md) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, guidance] <br>
**Output Format:** [Markdown or JSON structured care analysis reports with alert status, care suggestions, and report links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save output to a user-specified file; historical report listings are returned as structured text from the cloud service.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata; artifact frontmatter says 1.0.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
