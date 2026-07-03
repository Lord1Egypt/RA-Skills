## Description: <br>
Analyzes pet feeding-bowl videos or video URLs through a cloud API to identify selective eating behaviors, summarize frequency, and provide feeding-adjustment suggestions without medical diagnosis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External pet care operators, smart feeder integrations, boarding centers, and veterinary inpatient teams use this skill to screen feeding-area footage for selective eating behavior. It helps identify patterns such as pushing kibble away, selecting treats, or sniffing and leaving, then returns behavior-focused feeding suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pet feeding media or video URLs are sent to the configured cloud analysis service. <br>
Mitigation: Use only media and URLs that the user is comfortable sharing with that service, and avoid sensitive background footage. <br>
Risk: The skill can create or reuse a backend identity and store local authentication tokens in a workspace SQLite database. <br>
Mitigation: Run it in a scoped workspace, limit access to local data files, and clear stored identity data when continued history access is not needed. <br>
Risk: Behavior analysis could be mistaken for medical guidance. <br>
Mitigation: Treat outputs as feeding-behavior references only and escalate health concerns to a qualified veterinary professional. <br>


## Reference(s): <br>
- [Pet Picky Eater Detection API Documentation](references/api_doc.md) <br>
- [Shared Analysis API Documentation](skills/smyx_analysis/references/api_doc.md) <br>
- [Skill Demo](https://lifeemergence.com/sample.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown report with structured JSON content and report links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write the generated report to a user-specified output file; results are feeding-behavior references, not medical diagnosis or treatment advice.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter reports 1.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
