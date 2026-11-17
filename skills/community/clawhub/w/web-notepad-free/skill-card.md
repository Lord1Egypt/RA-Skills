## Description: <br>
Web Notepad Free is a lightweight online form management skill for creating forms, configuring fields, and managing submissions through REST API and shell-command workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, individual site owners, and small teams use this skill to set up lightweight contact, event registration, survey, and feedback collection workflows without building a custom backend. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad activation wording could cause the skill to be used for Webhook or unrelated system-integration requests outside its supported form-management scope. <br>
Mitigation: Review the requested task before invoking the skill and limit use to form creation, submission management, querying, and field configuration workflows. <br>
Risk: The connected form account may contain important or sensitive submission data. <br>
Mitigation: Use a least-privilege API key, keep WEB_NOTEPAD_API_KEY in a secret manager or environment variable, and avoid hard-coding credentials. <br>
Risk: Delete operations can irreversibly remove forms and their submissions. <br>
Mitigation: Require explicit user confirmation and export or back up relevant data before deleting forms or submissions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/web-notepad-free) <br>
- [Skill homepage](https://skillhub.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with curl examples and JSON response structures] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses WEB_NOTEPAD_API_KEY for Bearer Token authentication; free-tier usage and feature limits apply.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
