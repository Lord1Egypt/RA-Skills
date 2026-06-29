## Description: <br>
Utilizes vision and radar technology for contactless detection of falls and produces structured monitoring reports for elderly home safety scenarios. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and care teams can use this skill to analyze elderly fall risk from monitoring images, videos, or media URLs and to query cloud-hosted historical fall detection reports. Its outputs are advisory safety-monitoring reports and should not replace human confirmation or emergency response procedures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive home-monitoring images, videos, or media URLs may be sent to the Life Emergence cloud service for analysis. <br>
Mitigation: Use only approved media with appropriate consent, avoid unnecessary private-room footage, and confirm the publisher's retention and deletion controls before deployment. <br>
Risk: The skill can create or reuse local identity records and stored tokens. <br>
Mitigation: Run it in a controlled workspace, protect the local data directory, and rotate or remove stored credentials according to the publisher's account guidance. <br>
Risk: Fall detection and alarm claims may be over-relied on in safety-critical situations. <br>
Mitigation: Treat outputs as advisory, confirm suspected falls through direct contact or human review, and maintain an independent emergency response procedure. <br>
Risk: Historical report queries may expose cloud reports associated with the resolved user identity. <br>
Mitigation: Restrict access to trusted operators and verify the active account context before querying or sharing report links. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-elderly-fall-detection-analysis) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>
- [API 接口文档](references/api_doc.md) <br>
- [smyx_analysis API接口文档](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown and JSON analysis results with report links and optional saved output files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May output a current analysis report, a cloud historical-report list, or a report export link.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata; artifact frontmatter lists 1.0.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
