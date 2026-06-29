## Description: <br>
Analyzes face images or videos using facial blood-flow and emotional features to produce stress-index, anxiety-tendency, and depression-tendency assessment results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to submit face media for psychological stress assessment and retrieve structured results or prior cloud reports. It is suited for mental-health monitoring workflows where results are treated as reference information, not clinical diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Face images or videos and psychological-assessment results are sent to the LifeEmergence cloud service. <br>
Mitigation: Use only with informed consent and a clear data-retention explanation for real personal, workplace, or student mental-health media. <br>
Risk: The skill can create or reuse a persistent identity and query prior cloud reports. <br>
Mitigation: Confirm that identity linkage and report-history access match the user's privacy expectations before deployment. <br>
Risk: Account tokens may be stored locally. <br>
Mitigation: Restrict local file access and review token storage practices before installing in shared or managed environments. <br>
Risk: Psychological stress results could be mistaken for clinical diagnosis. <br>
Mitigation: Present outputs as reference assessments and direct persistent or severe concerns to qualified professionals. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-psychological-stress-assessment-analysis) <br>
- [Skill Demo](https://lifeemergence.com/sample.html) <br>
- [API Interface Documentation](references/api_doc.md) <br>
- [Smyx Analysis API Documentation](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown or JSON assessment report with report links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May query cloud-hosted historical reports and can save structured output to a file.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata; artifact frontmatter lists 1.0.7) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
