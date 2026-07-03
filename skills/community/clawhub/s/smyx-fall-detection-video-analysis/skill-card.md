## Description: <br>
Detects whether anyone has fallen within a target area, supports video stream analysis, and is suitable for real-time safety monitoring of elderly people living alone. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, caregivers, and safety-monitoring operators use this skill to analyze local or URL-based video for possible fall events in monitored home areas and to review cloud-generated historical reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fall-detection videos or video URLs may be sent to the provider's cloud service. <br>
Mitigation: Use only footage that is approved for cloud processing, and avoid private household video unless consent, retention, and access expectations are acceptable. <br>
Risk: The skill can create or reuse a local account identity and store or send identity tokens. <br>
Mitigation: Run it in an isolated agent environment, review stored credential and identity files after use, and remove tokens when they are no longer needed. <br>
Risk: Cloud history-report queries may expose previously analyzed fall-detection reports linked to the local identity. <br>
Mitigation: Restrict history queries to trusted users and validate that returned report links are appropriate before sharing them. <br>
Risk: Fall-detection output is a safety alert aid and may be incorrect or incomplete. <br>
Mitigation: Treat alerts as prompts for human confirmation and urgent follow-up rather than as a substitute for caregiver or medical assessment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-fall-detection-video-analysis) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>
- [Fall detection API documentation](references/api_doc.md) <br>
- [Analysis API documentation](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and JSON/text responses from video analysis and history-report queries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include structured fall-detection results, monitoring suggestions, status messages, saved output files, and report links.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
