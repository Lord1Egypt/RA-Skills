## Description: <br>
Analyzes gaze direction, head pose, and facial landmarks in video to quantify focus, distraction, or mind-wandering for classroom, office meeting, and driving attention scenarios. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Teachers, managers, safety officers, and developers use this skill to analyze authorized video files or public video URLs, generate structured focus reports, and list historical cloud reports. It can help review attention trends, distraction counts, and focus scores, but its reports should remain advisory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive video and identity data may be sent to external services. <br>
Mitigation: Use only videos you have authority and consent to analyze, and avoid sensitive classroom, workplace, or driving footage unless privacy requirements are satisfied. <br>
Risk: The skill may create or reuse an account, keep tokens locally, and expose historical report links. <br>
Mitigation: Review account behavior, token storage, and report-link access controls before installation or sharing outputs. <br>
Risk: Security evidence notes mismatched health-analysis artifacts in the package. <br>
Mitigation: Confirm the invoked service, endpoint behavior, and returned reports match the intended focus-analysis use case before relying on results. <br>


## Reference(s): <br>
- [API Interface Documentation](references/api_doc.md) <br>
- [Common Analysis API Documentation](skills/smyx_analysis/references/api_doc.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/18072937735/skills/smyx-focus-analysis) <br>
- [Publisher Profile](https://clawhub.ai/user/18072937735) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration] <br>
**Output Format:** [Markdown reports and tables, JSON responses, and Python command invocations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can save report output to a file and may return cloud report links for historical records.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata; artifact frontmatter lists 1.0.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
