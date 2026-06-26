## Description: <br>
Analyzes nighttime fixed-camera video for lights-off timing, early-morning activity, and deviations from a personal sleep-rhythm baseline, then returns a rhythm-anomaly reminder without making medical diagnoses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, care teams, family members, and developers use this skill to analyze home nighttime video for sleep-rhythm changes in people living alone and to retrieve structured historical reports for follow-up. It is intended to support check-ins and care workflows, not to provide a medical diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes highly private nighttime home video or video URLs through a cloud service. <br>
Mitigation: Install and run it only with explicit informed consent from the monitored person or guardian, and review the service's storage and access controls before use. <br>
Risk: The skill can create or reuse a persistent internal identity, persist tokens locally, and retrieve historical reports tied to that identity. <br>
Mitigation: Use it only in trusted environments, review token and report retention practices, and restrict access to generated reports and local runtime data. <br>
Risk: Sleep-rhythm anomalies can be caused by normal life events or health issues and may be misread as a diagnosis. <br>
Mitigation: Treat outputs as visual rhythm-change indicators for human follow-up, and route health concerns to qualified caregivers or clinicians. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-living-alone-rhythm-anomaly-analysis) <br>
- [Living-alone rhythm anomaly API documentation](references/api_doc.md) <br>
- [Analysis API error reference](skills/smyx_analysis/references/api_doc.md) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [Markdown text containing structured analysis results, anomaly indicators, recommendations, and report links; JSON is available for detailed output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include report export links and historical report lists retrieved from the configured cloud service.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
