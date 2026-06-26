## Description: <br>
Automates lead capture and tracking with Supabase storage and Make.com email workflows, managing conversations from new to qualified status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[big-roman123](https://clawhub.ai/user/big-roman123) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Sales teams and Clawd agent developers use this skill to capture leads from agent conversations, trigger first-response automation, track lead status, and log conversation history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles personal lead and conversation data using a full-power Supabase Service Role Key. <br>
Mitigation: Use a tightly scoped Supabase project or schema, protect the Service Role Key, and add privacy notice, consent or lawful-basis, retention, deletion, and audit controls before using real lead data. <br>
Risk: Lead deletion can be irreversible without documented recovery safeguards. <br>
Mitigation: Restrict deletion permissions and establish backup, recovery, and approval logging before production use. <br>
Risk: Lead data may flow through Make.com automation and related email services. <br>
Mitigation: Review Make.com and downstream email-service data handling, retention, and access controls before enabling automated replies. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/big-roman123/sales-bot) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Configuration instructions] <br>
**Output Format:** [JSON responses from TypeScript methods with configuration values for Supabase and Make.com workflows] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates, retrieves, updates, lists, and deletes lead records; logs conversations; and reports automation status.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, skill.json, package.json, SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
