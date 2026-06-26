## Description: <br>
Using an in-cabin DMS camera, the system analyzes driver head pitch and yaw to detect sustained head-down or side-view behavior and output distracted-driving alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, fleet operators, and in-vehicle safety teams use this skill to analyze DMS driver-face videos or URLs for head-down and side-view distraction events, retrieve historical reports, and produce warning details for review or downstream fleet workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uploads driver-facing video and retrieves cloud-hosted reports, which can expose sensitive biometric or workplace monitoring data. <br>
Mitigation: Use only with informed consent, documented retention/deletion practices, and appropriate privacy controls for driver or employee video. <br>
Risk: The remote service may create or reuse an account identity and locally store tokens or profile data for report access. <br>
Mitigation: Use a dedicated non-sensitive open-id, protect local workspace storage, and review the publisher's endpoint, retention, encryption, and deletion handling before deployment. <br>
Risk: Head-pose detection can be less reliable when the face is obscured, lighting is poor, vibration is severe, or input video does not meet frame-rate and resolution expectations. <br>
Mitigation: Validate camera placement and video quality before operational use, and treat warnings as assistive signals rather than sole evidence for driver safety decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-driver-head-pose-abnormality-analysis) <br>
- [Driver head-pose API documentation](references/api_doc.md) <br>
- [Shared analysis API documentation](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [JSON or Markdown reports with command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save analysis output to a user-specified file and may render historical report results as a Markdown table.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
