## Description: <br>
Analyzes baby-monitor images or video to classify infant sleep posture, detect mouth or nose occlusion, and return visual risk alerts and reports without providing medical diagnosis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to analyze crib camera media for visual sleep-posture and mouth-or-nose occlusion signals, return low-to-critical risk levels, and retrieve prior monitoring reports. It is an auxiliary monitoring aid and should not be used as the sole real-time infant safety alarm. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive infant-monitor footage or URLs are sent to a cloud service and historical reports can be retrieved. <br>
Mitigation: Use only with guardian consent, trusted publisher and cloud endpoints, and appropriate privacy controls for child-monitoring media. <br>
Risk: The skill creates or reuses an internal identity and may persist backend tokens locally. <br>
Mitigation: Review identity and token handling before installation, restrict access to local configuration and report data, and avoid exposing internal identity values in user-facing output. <br>
Risk: Life-safety alert claims are not clearly bounded by the release evidence. <br>
Mitigation: Treat outputs as auxiliary visual risk signals and require adult supervision and independent safety checks for high-risk alerts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-infant-suffocation-risk-detection-analysis) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>
- [API documentation](references/api_doc.md) <br>
- [Analysis API documentation](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands] <br>
**Output Format:** [Markdown reports and JSON structured analysis, with shell commands for agent execution] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include risk levels, posture classification, occlusion status, event time, snapshot or report links, alert text, and historical report tables.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
