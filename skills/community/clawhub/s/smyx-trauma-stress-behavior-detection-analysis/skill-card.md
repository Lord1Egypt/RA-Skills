## Description: <br>
Analyzes emergency-shelter video to flag visual indicators of acute stress, including stupor, tremor, unresponsiveness, and hypervigilance, and returns psychological crisis alerts for human responder review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Emergency command centers and licensed psychological rescue teams use this skill to analyze fixed-camera shelter or temporary-settlement video and prioritize human review and response. It is an aid for behavior-observation alerts, not a clinical diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive emergency-shelter video and personal identifiers may be submitted to a backend service or retained in local records. <br>
Mitigation: Deploy only in controlled emergency-response environments, limit access to authorized teams, confirm data retention and history-query permissions, and approve local SQLite storage of usernames, phone numbers, and tokens before use. <br>
Risk: A shipped API key may grant unintended backend access if reused as-is. <br>
Mitigation: Rotate or remove the bundled key before installation and provide credentials through an approved secret-management or configuration process. <br>
Risk: Behavior alerts could be mistaken for clinical diagnosis or trigger inappropriate response escalation. <br>
Mitigation: Use outputs only as visual behavior-observation alerts, require human review before dispatch escalation, and keep interventions with licensed psychological or medical responders. <br>


## Reference(s): <br>
- [Emergency scene API documentation](references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown text with JSON analysis payloads, report-list tables, and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include crisis levels, zone locations, responder suggestions, PFA prompts, report export links, and optional file output.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
