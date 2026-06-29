## Description: <br>
Identifies key plant growth stages from images or videos and returns structured analysis for precision agriculture decision support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agricultural producers, agronomists, and developers use this skill to submit plant images or videos for plant growth-stage classification, structured reporting, and cloud report retrieval. The results can support precision agriculture decisions such as irrigation, fertilization, pest and disease control, and yield planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Images or videos are sent to a cloud analysis service. <br>
Mitigation: Use only media appropriate for the provider's retention and deletion practices, and avoid sensitive media unless those practices meet the user's requirements. <br>
Risk: The skill may silently create or reuse an internal identity, store session tokens locally, and retrieve account-linked report history. <br>
Mitigation: Install only where account-linked local persistence is acceptable, and review or clear local credential storage according to the deployment environment's policy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-plant-growth-stage-recognition-analysis) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>
- [API documentation](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown or JSON analysis report with optional report links; command-line output for history lists.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts local media file paths or public media URLs and can optionally save returned content to an output file.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence; artifact frontmatter says 1.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
