## Description: <br>
Run a comprehensive quarterly CRM audit covering list health, bounce monitoring, data quality, scoring calibration, engagement metrics, and property cleanup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tomgranot](https://clawhub.ai/user/tomgranot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
CRM operations, marketing operations, and RevOps teams use this skill to perform a recurring HubSpot database health audit, compare results with the previous quarter, and produce an action-oriented cleanup report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The audit may expose sensitive CRM contact, scoring, list, property, and engagement data. <br>
Mitigation: Run it only for HubSpot accounts you are authorized to audit, use a least-privilege read-only token, and store generated reports in an access-controlled location. <br>
Risk: Cleanup recommendations could lead to separate CRM changes if treated as automatic instructions. <br>
Mitigation: Treat report action items as proposals that require explicit owner approval before any list, property, scoring, or contact changes are made. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown guidance with inline commands and a report template] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a quarterly health report template and action-item guidance; the audit is described as read-only.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
