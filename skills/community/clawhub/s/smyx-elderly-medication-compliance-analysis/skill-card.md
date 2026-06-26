## Description: <br>
Analyzes medication-area images or videos to detect whether an older adult picked up medication, brought it to the mouth, and swallowed, then returns compliance status, alerts, and report links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Caregivers, elder-care operators, and developers use this skill to review medication-area video or image inputs and produce a structured adherence report for pick-up, to-mouth, and swallow steps. It is intended to support medication-compliance monitoring, not to provide medical advice or dosing guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Medication-area videos and related identity or report metadata may be sent to Life Emergence cloud services. <br>
Mitigation: Use only with consent from the monitored person or an authorized caregiver, and avoid sending footage that is unnecessary for the medication-compliance task. <br>
Risk: The skill may create or reuse local account records and retain tokens in a local SQLite database. <br>
Mitigation: Run it in a controlled environment, restrict local file access, and remove the local database or stored tokens when they are no longer needed. <br>
Risk: The security scan verdict is suspicious because the skill handles sensitive home health footage and identity data. <br>
Mitigation: Review the security guidance before installation and apply organizational privacy, retention, and caregiver-consent requirements before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-elderly-medication-compliance-analysis) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>
- [API reference](references/api_doc.md) <br>
- [SMYX analysis API reference](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown text with structured JSON results, status messages, and report links; optional file output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts local video files or video URLs; history-list mode returns cloud report records.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence; artifact frontmatter says 1.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
