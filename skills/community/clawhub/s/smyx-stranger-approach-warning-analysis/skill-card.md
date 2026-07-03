## Description: <br>
Detects strangers near minors in images or videos, returns structured safety analysis, and can query cloud-hosted historical warning reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and safety operators use this skill to analyze surveillance images, videos, or media URLs for stranger proximity risks around minors and to retrieve prior warning reports from the publisher's cloud service. It is intended for homes, schools, childcare centers, and similar monitoring scenarios, with results used as safety reference material rather than a replacement for emergency or professional security response. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends images, videos, or media URLs that may involve minors to the publisher's cloud service. <br>
Mitigation: Use it only where consent, retention, deletion, and data-transfer requirements are understood and acceptable; avoid sending media that cannot leave the local environment. <br>
Risk: The skill creates or reuses a local identity and stores account tokens in a workspace SQLite database. <br>
Mitigation: Run it in an isolated workspace, review local data storage before deployment, and clear or revoke stored identities and tokens when access is no longer needed. <br>
Risk: Automated stranger-detection and warning results may be incomplete, incorrect, or delayed. <br>
Mitigation: Treat outputs as safety reference material, keep human review in the response loop, and do not rely on the skill as the only emergency or security control. <br>
Risk: The authoritative security verdict is suspicious because the skill is a cloud media-analysis wrapper with local identity and token handling. <br>
Mitigation: Complete a security review before production use, restrict runtime permissions and network access where possible, and avoid exposing unrelated secrets in the workspace. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/18072937735/skills/smyx-stranger-approach-warning-analysis) <br>
- [API Documentation](references/api_doc.md) <br>
- [Skill Demo](https://lifeemergence.com/sample.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown text with structured JSON analysis, warning summaries, history-report lists, and report links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save analysis output to a user-specified local file and may return links to cloud-hosted report exports.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
