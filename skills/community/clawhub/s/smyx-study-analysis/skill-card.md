## Description: <br>
Analyzes children's or students' study videos to identify learning-behavior patterns, poor study habits, posture and focus issues, then returns structured reports and family education suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Parents, educators, and agent users can submit a local video file or video URL for cloud-based learning behavior analysis, including focus, posture, study habits, risk signals, and report links. The skill can also retrieve cloud-hosted historical analysis reports associated with the internally resolved user identity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends children's or students' study videos, video URLs, generated reports, and an internally resolved user identifier to the provider's cloud service. <br>
Mitigation: Use only with appropriate consent and data-handling approval, and avoid school, medical, counseling, or regulated child-data contexts unless the provider's controls have been reviewed. <br>
Risk: The skill silently creates and reuses local identity and token records. <br>
Mitigation: Run it in an isolated workspace where account state can be reviewed or cleared, and verify that persistent identity/token behavior matches the deployment policy. <br>
Risk: Historical report lookup is tied to the internally resolved cloud identity. <br>
Mitigation: Confirm the active account context before querying history and treat cloud results as the only source for report listings. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-study-analysis) <br>
- [API interface reference](artifact/references/api_doc.md) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Files, Guidance] <br>
**Output Format:** [Markdown or JSON structured analysis reports with risk notes, suggestions, and report links; optionally written to a local output file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include cloud report export links and historical report listings.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
