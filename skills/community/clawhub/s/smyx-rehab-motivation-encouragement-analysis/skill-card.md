## Description: <br>
Analyzes rehabilitation training video, with optional audio and history signals, to detect patient frustration or giving-up tendencies and produce encouragement actions, progress comparisons, clinician alerts, and summary reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Rehabilitation clinicians, care teams, and authorized home-care users use this skill to analyze training-session media for frustration signals, generate motivational feedback recommendations, and review historical rehab-motivation reports. It is intended to support adherence and timely human intervention, not to diagnose medical or psychological conditions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send rehabilitation video, optional audio, patient identifiers, and history-query data to configured Life Emergence/Open API services. <br>
Mitigation: Use it with real patients only after confirming consent, retention and deletion rules, report-link access controls, and whether the configured services are approved for the care setting. <br>
Risk: Evidence flags local token persistence, automatic account/login behavior, and cloud history access as broader authority than users may expect. <br>
Mitigation: Review workspace token storage, account permissions, and history-query scope before deployment; restrict access to authorized patients, caregivers, and clinicians. <br>
Risk: Motivational feedback could be misleading or harmful if it fabricates progress data, pressures the patient, or is treated as a diagnosis. <br>
Mitigation: Base encouragement only on verified training history, avoid pressure-based messages, and route clinical concerns or repeated significant distress to qualified rehabilitation or mental-health professionals. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-rehab-motivation-encouragement-analysis) <br>
- [API interface documentation](references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [CLI text or JSON analysis reports, with Markdown tables for historical report listings when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write an optional output file when an output path is supplied.] <br>

## Skill Version(s): <br>
1.0.2 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
