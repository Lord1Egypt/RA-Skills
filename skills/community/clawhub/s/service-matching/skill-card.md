## Description: <br>
C+ service demand matching skill that analyzes a real Excel service ledger, extracts tenant needs from visit records, and recommends matching C+ services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[perrykono-debug](https://clawhub.ai/user/perrykono-debug) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Property service teams and tenant managers use this skill to analyze C+ service visit records, match tenant profiles and stated needs to service offerings, and prepare recommendations for follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read a tenant Excel ledger containing business, contact, contract, and follow-up information. <br>
Mitigation: Use the skill only with authorized workbooks, restrict file access, and redact tenant or contact details that are not needed for the task. <br>
Risk: The skill can save follow-up status and notes back into the workbook. <br>
Mitigation: Back up the workbook and require approval before any save or update operation. <br>
Risk: The skill can send tenant service recommendations to a configured WeCom webhook. <br>
Mitigation: Restrict webhook destinations, verify the recipient channel before sending, and require approval before outbound notifications. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown text with structured service recommendations and optional JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include tenant service recommendations, follow-up reminders, effectiveness summaries, and WeCom notification text.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
