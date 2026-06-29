## Description: <br>
Analyzes fixed-camera elder-care video to identify loneliness-related behaviors, produce a loneliness index, and suggest warm companionship actions without making medical diagnoses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External caregivers, elder-care platform operators, and authorized family-support workflows use this skill to analyze videos from solitary-living elder homes or private nursing-home rooms. It returns behavior statistics, loneliness-level output, report links, and companionship recommendations for human review and follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Highly private elder-care video or optional audio may be sent to a cloud API and associated with report history. <br>
Mitigation: Use only with informed consent from the monitored elder and authorized family, clear notice about cloud processing, and strict limits on who can query historical reports. <br>
Risk: Silent identity setup and local token persistence can reduce user control over identity linkage. <br>
Mitigation: Run only in controlled deployments that explicitly approve local identity and token persistence, restrict workspace access, and review identity handling before installation. <br>
Risk: Loneliness-related behavior output could be mistaken for a psychiatric diagnosis or trigger intrusive interventions. <br>
Mitigation: Present outputs as behavioral statistics and recommendations only, avoid medical diagnosis, support the elder's ability to turn off reminders, and route serious concerns to appropriate human or clinical support. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-elderly-loneliness-comfort-analysis) <br>
- [API documentation](references/api_doc.md) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [Markdown text containing structured JSON analysis, report links, and recommendations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include cloud report export links and warm-companionship action suggestions; output should be treated as behavioral support information, not a medical diagnosis.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence; artifact frontmatter reports 1.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
