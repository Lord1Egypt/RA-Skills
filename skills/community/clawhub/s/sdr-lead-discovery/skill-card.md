## Description: <br>
AI-driven lead discovery for B2B export. Searches web for potential buyers matching ICP, evaluates fit, and creates CRM records for follow-up. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ipythoning](https://clawhub.ai/user/ipythoning) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales and business development users use this skill to find potential B2B export buyers, research fit against an ICP, and prepare CRM follow-up records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can collect contact details and prospect research from external services. <br>
Mitigation: Define privacy, retention, correction, and deletion rules for collected contact data before use. <br>
Risk: The skill can create or update CRM records and outreach tags without an explicit approval step. <br>
Mitigation: Require human approval before CRM writes, hot-lead tagging, or outreach next-action changes. <br>
Risk: The skill can run on a daily schedule and call external services with stored credentials. <br>
Mitigation: Confirm the schedule is desired and use least-privilege Jina, CRM, and Supermemory credentials. <br>


## Reference(s): <br>
- [Lead Discovery on ClawHub](https://clawhub.ai/ipythoning/sdr-lead-discovery) <br>
- [Jina AI](https://jina.ai/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown lead report with inline shell commands and CRM follow-up fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses daily search limits, duplicate checks, ICP scoring, and contact-channel recommendations.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
